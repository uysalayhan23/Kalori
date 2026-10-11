#!/usr/bin/env python3
"""Offline no-dependency tests for OFF importer. Run: python -m unittest discover -s tests -p 'test_*.py'"""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from import_openfoodfacts import row_to_product

class OFFTests(unittest.TestCase):
    def valid(self):
        return {"code":"8691234567890","product_name_tr":"Test gofret",
                "brands":"Örnek Marka","stores":"Örnek mağaza","countries_tags":"en:turkey",
                "energy-kcal_100g":"490","proteins_100g":"7.2",
                "fat_100g":"21","carbohydrates_100g":"68"}
    def test_parses_and_preserves_nutrients(self):
        obj=row_to_product(self.valid())
        self.assertEqual(obj["kcal"],490)
        self.assertEqual(obj["protein"],7.2)
        self.assertEqual(obj["verification"],"community_reported")
        self.assertEqual(obj["store"],"")
        self.assertEqual(obj["reportedStores"],"Örnek mağaza")
        self.assertEqual(obj["barcode"],"8691234567890")
    def test_brand_survives_import(self):
        obj=row_to_product(self.valid())
        self.assertEqual(obj["brand"],"Örnek Marka")
    def test_country_tags_with_spaces(self):
        row=self.valid();row["countries_tags"]="en:france, en:turkey"
        self.assertIsNotNone(row_to_product(row))
    def test_not_marking_stores_verified(self):
        obj=row_to_product(self.valid())
        self.assertNotIn("Örnek mağaza",obj["name"])
    def test_missing_energy_rejected(self):
        row=self.valid();row["energy-kcal_100g"]=""
        self.assertIsNone(row_to_product(row))
    def test_non_turkey_rejected(self):
        row=self.valid();row["countries_tags"]="en:france"
        self.assertIsNone(row_to_product(row))
    def test_missing_macro_preserved_null(self):
        row=self.valid();row["fat_100g"]=""
        self.assertIsNone(row_to_product(row)["fat"])
    def test_bad_barcode_rejected(self):
        row=self.valid();row["code"]="bad"
        self.assertIsNone(row_to_product(row))
if __name__=="__main__":unittest.main()
