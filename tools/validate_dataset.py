"""Check every stored calling code and prefix against the pinned numbering metadata."""

import argparse
import csv
import random
import re
import sys
from pathlib import Path

import phonenumbers

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from generate_phone_number import FIELDS, generate_phone_number, load_data, region_for_country

REGIONAL_FILES = (
    "NorthAmerica.csv", "LatinAmerica.csv", "Australia.csv", "Africa.csv",
    "Asia.csv", "Arabia.csv", "Europe.csv", "Balcans.csv",
)


def validate(rebuild=False):
    regions = {name: load_data(ROOT / "dataset" / name) for name in REGIONAL_FILES}
    combined = [row for name in REGIONAL_FILES for row in regions[name]]
    if rebuild:
        with (ROOT / "dataset" / "AllCountries.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS, quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writeheader()
            writer.writerows(combined)
    if load_data(ROOT / "dataset" / "AllCountries.csv") != combined:
        raise ValueError("AllCountries.csv differs from the regional files; run with --rebuild")

    with (ROOT / "dataset" / "International_codes.csv").open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["country", "iso", "code"]:
            raise ValueError("Incorrect International_codes.csv header")
        international = list(reader)
    for row in international:
        if set(row) != {"country", "iso", "code"} or any(not value or value != value.strip() for value in row.values()):
            raise ValueError(f"Malformed international entry: {row}")
        if row["iso"] not in phonenumbers.SUPPORTED_REGIONS:
            raise ValueError(f"Unsupported territory identifier: {row}")
        if row["code"] != "+" + str(phonenumbers.country_code_for_region(row["iso"])):
            raise ValueError(f"Incorrect international calling code: {row}")

    checked = set()
    for filename, rows in regions.items():
        for line, row in enumerate(rows, 2):
            region = region_for_country(row["Country"])
            if region is None or row["CountryCode"] != "+" + str(phonenumbers.country_code_for_region(region)):
                raise ValueError(f"{filename}:{line}: incorrect country calling code")
            prefixes = row["LocalAreaCode"].split(",")
            if len(prefixes) != len(set(prefixes)) or any(not re.fullmatch(r"[0-9]+", prefix) for prefix in prefixes):
                raise ValueError(f"{filename}:{line}: invalid or repeated prefix")
            for prefix in prefixes:
                key = (region, prefix)
                if key in checked:
                    continue
                single_prefix = dict(row, LocalAreaCode=prefix)
                for seed in (0, 41):
                    text = generate_phone_number([single_prefix], row["Country"], row["Subdivision"], random.Random(seed))
                    number = phonenumbers.parse(text, None)
                    if (not phonenumbers.is_valid_number_for_region(number, region)
                            or not phonenumbers.national_significant_number(number).startswith(prefix)
                            or len(phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)[1:]) > 15
                            or phonenumbers.number_type(number) not in (
                                phonenumbers.PhoneNumberType.FIXED_LINE, phonenumbers.PhoneNumberType.MOBILE,
                                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE)):
                        raise ValueError(f"{filename}:{line}: implausible generated number {text}")
                checked.add(key)
    print(f"OK: {len(combined)} regional records, {len({row['Country'] for row in combined})} countries, "
          f"{len(international)} international entries, {len(checked)} distinct country/prefix pairs")
    print(f"Every prefix generated valid fixed-line or mobile examples with two seeds; phonenumbers {phonenumbers.__version__}.")
    print("Numbering-plan validity does not establish current subscriber assignment or exact city location.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true", help="rebuild AllCountries.csv before checking")
    args = parser.parse_args()
    validate(args.rebuild)
