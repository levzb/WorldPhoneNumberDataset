# WorldPhoneNumberDataset

Phone prefixes for 116 countries, with a Python generator for plausible international-format phone numbers.

The regional files contain **1317 records**. `International_codes.csv` contains **236 country/territory entries**, including aliases. Data was reviewed on **2026-10-30** against ITU numbering plans, regulator publications and libphonenumber 9.0.42 metadata; see [review notes and sources](docs/numbering-review.md) and the [country-by-country source index](docs/country-review.csv).

---

## Features

- **Big Phone Code Database**: Includes multiple CSV files organized by regions (e.g., Africa, Europe, Asia, etc.).
- **Phone Number Generator**: Looks up countries, cities and subdivisions, then samples a valid fixed-line or mobile range with the correct national length.

---

## Note

The regional files cover a selection of places, not every country or city. A prefix can describe a city, a wider region, or a national fixed/mobile range. Where an exact local allocation is unavailable or the numbering plan is non-geographic, a plausible national range is retained instead of inventing a city code. These cases are documented in the review notes.

Generated numbers pass the pinned numbering-plan rules. This does not mean that a number is assigned, reachable, or uniquely tied to the requested city. Number portability also limits geographic precision.

---

## Files

- `Africa.csv`: Phone codes for African countries.
- `Asia.csv`: Phone codes for Asian countries.
- `Europe.csv`: Phone codes for European countries.
- `NorthAmerica.csv`: Phone codes for North American countries.
- `LatinAmerica.csv`: Phone codes for Latin American countries.
- `Australia.csv`: Phone codes for Australia.
- `Balcans.csv`: Phone codes for Balkan countries.
- `AllCountries.csv`: A single file that combines the data from all the regional files above for convenience.
- `Arabia.csv`: Additional Middle Eastern and North African records; also included in the combined file.
- `International_codes.csv`: Country calling codes and region identifiers.
- `generate_phone_number.py`: Python script to generate phone numbers.
- `tools/validate_dataset.py`: Checks every calling code and prefix, and can rebuild the combined file.

The regional CSV schema stays the same:

```text
Country,Subdivision,PrimaryCityOrNote,CountryCode,LocalAreaCode
```

`CountryCode` is the international calling code, including `+`. `LocalAreaCode` contains one or more comma-separated **national leading prefixes**, without the country code. It can include part of the local number for a narrower regional match. Keep these values as strings: Italy, Benin and Gabon have significant leading zeros. Text such as `2-digit to 5-digit` is not a prefix.

All original regional records, including duplicate places, are retained. `AllCountries.csv` contains the regional files in order, with one header.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/levzb/WorldPhoneNumberDataset.git
   cd WorldPhoneNumberDataset
   ```

2. Install the dependency, preferably in a virtual environment, and run the script:
   ```bash
   python -m pip install -r requirements.txt
   python generate_phone_number.py
   ```

3. Enter a country name or two-letter region code, then a city, subdivision or note. Matching ignores case and common accent differences. A blank place selects any record for that country. Country-wide rows can serve places without a separate city code; an unsupported city otherwise returns `No matches found.`

---

## Example

**Input:**
```
Enter country (name or two-letter code): US
Enter city, subdivision or note (blank for any): Los Angeles
```

The result begins with `+1 213` or `+1 323`, with a valid ten-digit national number. The subscriber digits are random.

## Validation

```bash
python -m unittest discover -s tests -v
python tools/validate_dataset.py
```

The validator checks all 1006 distinct country/prefix pairs, significant zeros, permitted lengths, country ownership and valid fixed/mobile ranges. It also checks that the combined CSV exactly matches all regional files. The same checks run in GitHub Actions.

After editing regional files, rebuild the combined file and validate it:

```bash
python tools/validate_dataset.py --rebuild
```

---

## License

This project is open-source and available under the MIT License. Feel free to use and modify it.
