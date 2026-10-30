import csv
import random
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import phonenumbers


DATASET_DIR = Path(__file__).resolve().parent / "dataset"
FIELDS = ["Country", "Subdivision", "PrimaryCityOrNote", "CountryCode", "LocalAreaCode"]


@lru_cache(maxsize=4096)
def _normalise(value):
    value = value.casefold().translate(str.maketrans({"ø": "o", "ł": "l", "đ": "d", "æ": "ae", "œ": "oe", "ı": "i"}))
    value = unicodedata.normalize("NFKD", value)
    return "".join(c for c in value if c.isalnum() and not unicodedata.combining(c))


@lru_cache(maxsize=1)
def _country_index():
    with (DATASET_DIR / "International_codes.csv").open(encoding="utf-8-sig", newline="") as file:
        regions = {_normalise(row["country"]): row["iso"].strip() for row in csv.DictReader(file)}
    regions.update({
        "unitedstates": "US", "usa": "US", "uk": "GB", "greatbritain": "GB",
        "northkorea": "KP", "southkorea": "KR", "capeverde": "CV", "turkiye": "TR",
    })
    return regions


@lru_cache(maxsize=512)
def region_for_country(country):
    key = _normalise(country)
    if key.upper() in phonenumbers.SUPPORTED_REGIONS:
        return key.upper()
    return _country_index().get(key)

def load_data(filename):
    with open(filename, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"Unexpected CSV columns in {filename}")
        data = list(reader)
    for row in data:
        if set(row) != set(FIELDS) or any(not isinstance(value, str) or not value.strip() for value in row.values()):
            raise ValueError(f"Malformed CSV row in {filename}: {row}")
    return data

def _number_for_prefix(region, prefix, rng):
    if not re.fullmatch(r"[0-9]+", prefix):
        raise ValueError(f"Not a numeric national prefix: {prefix!r}")
    metadata = phonenumbers.PhoneMetadata.metadata_for_region(region)
    country_code = str(metadata.country_code)
    # Fixed-line ranges come first; national mobile fallbacks are also supported.
    for description in (metadata.fixed_line, metadata.mobile):
        if not description or not description.national_number_pattern:
            continue
        lengths = [length for length in description.possible_length
                   if len(prefix) <= length and len(country_code) + length <= 15]
        rng.shuffle(lengths)
        for length in lengths:
            tail_length = length - len(prefix)
            for _ in range(2000 if tail_length else 1):
                national_number = prefix + "".join(rng.choices("0123456789", k=tail_length))
                if not re.fullmatch(description.national_number_pattern, national_number):
                    continue
                number = phonenumbers.parse("+" + country_code + national_number, None)
                if (phonenumbers.national_significant_number(number) == national_number
                        and phonenumbers.is_valid_number_for_region(number, region)):
                    return number
    return None


def generate_phone_number(data, country, city, rng=None):
    """Generate a numbering-plan-valid example, not a verified subscriber number."""
    region = region_for_country(country)
    if not region:
        return None
    place = _normalise(city)
    matches, nationwide = [], []
    for row in data:
        if region_for_country(row["Country"]) != region:
            continue
        names = {_normalise(row["Subdivision"]), _normalise(row["PrimaryCityOrNote"]),
                 _normalise(row["Subdivision"].split(" (")[0])}
        if not place or place in names:
            matches.append(row)
        elif not _normalise(row["Subdivision"]) and _normalise(row["PrimaryCityOrNote"]) in ("", "capital", "nationwide"):
            nationwide.append(row)
    candidates = matches or nationwide
    if not candidates:
        return None
    rng = random if rng is None else rng
    rng.shuffle(candidates)
    country_code = "+" + str(phonenumbers.country_code_for_region(region))
    for row in candidates:
        if row["CountryCode"] != country_code:
            raise ValueError(f"Incorrect country calling code for {row['Country']}")
        prefixes = row["LocalAreaCode"].split(",")
        rng.shuffle(prefixes)
        for prefix in prefixes:
            number = _number_for_prefix(region, prefix.strip(), rng)
            if number is not None:
                return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    raise ValueError(f"No valid fixed-line or mobile range for {country} / {city}")

def main():
    try:
        data = load_data(DATASET_DIR / "AllCountries.csv")
        country = input("Enter country (name or two-letter code): ").strip()
        city = input("Enter city, subdivision or note (blank for any): ").strip()
        phone_number = generate_phone_number(data, country, city)
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1
    print(phone_number if phone_number else "No matches found.")
    return 0 if phone_number else 1

if __name__ == "__main__":
    raise SystemExit(main())
