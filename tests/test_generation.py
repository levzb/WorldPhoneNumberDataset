import random
import tempfile
import unittest
from pathlib import Path

import phonenumbers

from generate_phone_number import DATASET_DIR, generate_phone_number, load_data


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data(DATASET_DIR / "AllCountries.csv")

    def example(self, country, city, region, prefixes, length=None):
        for seed in range(3):
            text = generate_phone_number(self.data, country, city, random.Random(seed))
            self.assertIsNotNone(text, (country, city))
            number = phonenumbers.parse(text, None)
            self.assertTrue(phonenumbers.is_valid_number_for_region(number, region), text)
            national = phonenumbers.national_significant_number(number)
            self.assertTrue(any(national.startswith(prefix) for prefix in prefixes), text)
            if length is not None:
                self.assertEqual(len(national), length, text)

    def test_country_and_city_corrections(self):
        cases = [
            ("Egypt", "Giza", "EG", ["2"], None),
            ("Egypt", "Luxor", "EG", ["95"], 9),
            ("Colombia", "Bogotá", "CO", ["601"], 10),
            ("Nigeria", "Lagos", "NG", ["201"], 10),
            ("Paraguay", "Ciudad del Este", "PY", ["61"], None),
            ("United Kingdom", "Aberdeen", "GB", ["1224"], 10),
            ("Japan", "Tokyo", "JP", ["3"], 9),
            ("Vietnam", "Can Tho", "VN", ["292"], 10),
            ("United States", "Newark", "US", ["862", "973"], 10),
        ]
        for case in cases:
            with self.subTest(country=case[0], city=case[1]):
                self.example(*case)

    def test_significant_leading_zeros(self):
        self.example("Italy", "Rome", "IT", ["06"])
        self.example("Benin", "Cotonou", "BJ", ["0121"], 10)
        self.example("Gabon", "Libreville", "GA", ["0144"], 8)

    def test_lookup_aliases_and_subdivisions(self):
        self.example("US", "los angeles", "US", ["213", "323"], 10)
        self.example("United States of America", "Birmingham", "US", ["205", "659"], 10)
        self.example("Germany", "Berlin", "DE", ["30"])
        self.example("India", "Mumbai", "IN", ["22"], 10)
        self.example("Cote d'Ivoire", "Abidjan", "CI", ["2720"], 10)
        self.example("Canada", "montreal", "CA", ["514", "438"], 10)

    def test_national_ranges_without_city_codes(self):
        self.example("Singapore", "Jurong", "SG", ["6"], 8)
        self.example("Hong Kong", "Kowloon", "HK", ["2", "3"], 8)
        self.example("Macau", "Taipa", "MO", ["28"], 8)
        self.example("Chad", "Moundou", "TD", ["63"], 8)

    def test_unknown_locations_do_not_pick_an_unrelated_city(self):
        self.assertIsNone(generate_phone_number(self.data, "Unknown country", "London"))
        self.assertIsNone(generate_phone_number(self.data, "United Kingdom", "Not a real city"))
        self.assertIsNone(generate_phone_number(self.data, "Canada", "London, England"))

    def test_records_and_duplicate_locations_are_preserved(self):
        self.assertEqual(len(self.data), 1317)
        self.assertEqual(len({row["Country"] for row in self.data}), 116)
        self.assertGreater(sum(row["Country"] == "Brazil" and row["Subdivision"] == "Natal" for row in self.data), 1)

    def test_invalid_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("Country,Subdivision,PrimaryCityOrNote,CountryCode,LocalAreaCode\nIndia,Mumbai,+91,22\n")
            with self.assertRaises(ValueError):
                load_data(path)

    def test_invalid_prefix_does_not_produce_garbage(self):
        row = dict(next(row for row in self.data if row["Country"] == "Italy"))
        row["LocalAreaCode"] = "2-digit to 5-digit"
        with self.assertRaises(ValueError):
            generate_phone_number([row], "Italy", row["Subdivision"])


if __name__ == "__main__":
    unittest.main()
