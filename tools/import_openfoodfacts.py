#!/usr/bin/env python3
"""Stream an Open Food Facts TSV dump into a compact JS food catalog.

Usage:
  python tools/import_openfoodfacts.py --input en.openfoodfacts.org.products.csv --output packaged-foods.js
The OFF export file is tab-separated (despite the .csv extension). No network or pip.
Only rows tagged as Turkey, with a real product name, barcode and reported kcal/100 g
(or kcal/100 ml) are retained. Do not infer a store from a brand.
License: Open Food Facts ODbL; attribution/share-alike obligations apply.
"""
import argparse,csv,json,re,sys,datetime
from pathlib import Path

FIELDS=("code","product_name_tr","product_name","brands","stores","countries_tags",
        "energy-kcal_100g","proteins_100g","fat_100g","carbohydrates_100g",
        "quantity","last_modified_datetime")
def safe_number(raw, max_value):
    try:
        value=float(raw)
        if value!=value or not 0<=value<=max_value:return None
        return round(value,3)
    except (TypeError,ValueError):return None

def row_to_product(row):
    countries=(row.get("countries_tags") or "").lower().split(",")
    if "en:turkey" not in countries and "tr:turkiye" not in countries:return None
    barcode=(row.get("code") or "").strip()
    name=(row.get("product_name_tr") or row.get("product_name") or "").strip()
    if not re.fullmatch(r"\d{8,14}",barcode) or not name:return None
    kcal=safe_number(row.get("energy-kcal_100g"),900)
    if kcal is None:return None
    # Explicitly filter missing / impossible high values, without inventing values.
    if kcal == 0 and any(safe_number(row.get(k),100) not in (None,0) for k in ("proteins_100g","fat_100g","carbohydrates_100g")):return None
    nutrition={key:safe_number(row.get(column),100) for key,column in
               (("protein","proteins_100g"),("fat","fat_100g"),("carbs","carbohydrates_100g"))}
    brand=(row.get("brands") or "").split(",")[0].strip()[:90]
    stores=(row.get("stores") or "").strip()
    # 'stores' is crowdsourced historical metadata, NOT verified current availability.
    return {"id":"off-"+barcode,"barcode":barcode,"name":name[:160],
            "brand":brand,"store":"","reportedStores":stores[:200],
            "category":"Paketli market ürünleri","kcal":kcal,**nutrition,
            "quantity":(row.get("quantity") or "")[:80],
            "source":"Open Food Facts","verification":"community_reported",
            "sourceReference":"https://world.openfoodfacts.org/product/"+barcode,
            "basis":"100 g or 100 ml, as reported by OFF",
            "lastModified":(row.get("last_modified_datetime") or "")[:30]}

def run():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True);p.add_argument("--output",required=True)
    p.add_argument("--limit",type=int,default=40000)
    args=p.parse_args()
    if not 1<=args.limit<=300000:p.error("limit out of range")
    products={};count=0
    with open(args.input,encoding="utf-8",newline="") as fh:
        rows=csv.DictReader(fh,delimiter="\t")
        if not {"code","countries_tags","energy-kcal_100g"}.issubset(rows.fieldnames or []):
            p.error("Wrong format or missing required Open Food Facts TSV columns")
        for row in rows:
            count+=1
            f=row_to_product(row)
            if f:products[f["barcode"]]=f
            if len(products)>=args.limit:break
    ordered=sorted(products.values(),key=lambda f:(f["name"].casefold(),f["barcode"]))
    out="/* Open Food Facts, ODbL, https://world.openfoodfacts.org/; community-contributed nutrition values. */\n"
    out+="globalThis.KaloriPackagedFoods="+json.dumps(ordered,ensure_ascii=False,separators=(",",":"))+";\n"
    Path(args.output).write_text(out,encoding="utf-8")
    print(json.dumps({"rows_read":count,"products_exported":len(ordered),
                      "output":args.output},ensure_ascii=False))
if __name__=="__main__":run()
