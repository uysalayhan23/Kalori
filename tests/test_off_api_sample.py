#!/usr/bin/env python3
"""Offline mapping tests for the bounded OFF API importer: no network requests."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from fetch_off_turkey_sample import from_api
from import_openfoodfacts import row_to_product

class APISampleTests(unittest.TestCase):
    def test_maps_off_v2_nutriments_and_provenance(self):
        item={"code":"8691234567890","product_name_tr":"Örnek Gofret",
              "brands":"Örnek Marka","countries_tags":["en:turkey","en:germany"],
              "stores":"Örnek mağaza","nutriments":{"energy-kcal_100g":490,"proteins_100g":7,
              "fat_100g":21,"carbohydrates_100g":68}}
        product=row_to_product(from_api(item))
        self.assertEqual(product["kcal"],490)
        self.assertEqual(product["brand"],"Örnek Marka")
        self.assertEqual(product["store"],"")
        self.assertEqual(product["verification"],"community_reported")
        self.assertEqual(product["sourceReference"],"https://world.openfoodfacts.org/product/8691234567890")
    def test_api_missing_energy_is_not_invented(self):
        item={"code":"8691234567890","product_name":"Örnek","countries_tags":["en:turkey"],"nutriments":{}}
        self.assertIsNone(row_to_product(from_api(item)))
    def test_api_non_turkey_is_rejected(self):
        item={"code":"8691234567890","product_name":"Example","countries_tags":["en:france"],
              "nutriments":{"energy-kcal_100g":300}}
        self.assertIsNone(row_to_product(from_api(item)))

if __name__=="__main__":unittest.main()
