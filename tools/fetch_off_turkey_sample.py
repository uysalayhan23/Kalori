#!/usr/bin/env python3
"""Fetch ONE bounded Open Food Facts Turkey search page and export to packaged-foods.js.
This is a manually run data-acquisition tool, NOT a scheduled task or APK build.
Requires internet, uses one search request (OFF rate limits apply).
"""
import argparse,json,sys,urllib.parse,urllib.request,os,tempfile
from pathlib import Path
from import_openfoodfacts import row_to_product

API="https://world.openfoodfacts.org/api/v2/search"
FIELDS="code,product_name_tr,product_name,brands,stores,countries_tags,nutriments,quantity,last_modified_t"
def from_api(item):
    n=item.get("nutriments") or {}
    return {"code":item.get("code") or "",
      "product_name_tr":item.get("product_name_tr") or "",
      "product_name":item.get("product_name") or "",
      "brands":item.get("brands") or "", "stores":item.get("stores") or "",
      "countries_tags":",".join(item.get("countries_tags") or []),
      "energy-kcal_100g":n.get("energy-kcal_100g"),
      "proteins_100g":n.get("proteins_100g"), "fat_100g":n.get("fat_100g"),
      "carbohydrates_100g":n.get("carbohydrates_100g"),
      "quantity":item.get("quantity") or "",
      "last_modified_datetime":str(item.get("last_modified_t") or "")}
def main():
    p=argparse.ArgumentParser(description="Single bounded OFF Turkey sample search")
    p.add_argument("--output",default="packaged-foods.js")
    p.add_argument("--page-size",type=int,default=100)
    p.add_argument("--page",type=int,default=1)
    p.add_argument("--max-bytes",type=int,default=5_000_000)
    args=p.parse_args()
    if not 1<=args.page_size<=100:p.error("page-size must be 1..100")
    if not 1<=args.page<=10000:p.error("page must be positive")
    if not 1024<=args.max_bytes<=100_000_000:p.error("invalid size budget")
    query=urllib.parse.urlencode({"countries_tags":"en:turkey","page":args.page,
                                   "page_size":args.page_size,"fields":FIELDS})
    request=urllib.request.Request(API+"?"+query,
       headers={"User-Agent":"KaloriApp/0.1 (https://github.com/uysalayhan23/Kalori; educational offline catalog)",
                "Accept":"application/json"})
    try:
        with urllib.request.urlopen(request,timeout=35) as response:
            raw=response.read(3_000_001)
            if len(raw)>3_000_000:raise ValueError("API payload unexpectedly large")
    except Exception as exc:
        p.exit(2,f"OFF API unavailable: {exc}\n")
    response=json.loads(raw)
    items=response.get("products")
    if not isinstance(items,list):p.error("Unexpected OFF response")
    products={}
    for item in items:
        if not isinstance(item,dict):continue
        normalized=row_to_product(from_api(item))
        if normalized:products[normalized["barcode"]]=normalized
    if not products:p.exit(3,"No usable Turkey products found. Existing catalog unchanged.\n")
    ordered=sorted(products.values(),key=lambda x:(x["name"].casefold(),x["barcode"]))
    output="/* Open Food Facts ODbL https://world.openfoodfacts.org/ - community data; not verified shop availability. */\n"
    output+="globalThis.KaloriPackagedFoods="+json.dumps(ordered,ensure_ascii=False,separators=(",",":"))+";\n"
    if len(output.encode("utf-8"))>args.max_bytes:p.exit(4,"Output exceeds size budget; existing file unchanged.\n")
    target=Path(args.output)
    if target.exists():
        existing=target.read_text(encoding="utf-8")
        prefix="globalThis.KaloriPackagedFoods="
        if prefix not in existing or not existing.strip().endswith(";"):
            p.exit(5,"Existing catalog is unrecognized; refusing to overwrite.\\n")
        try:
            previous=json.loads(existing.split(prefix,1)[1].strip()[:-1])
            if not isinstance(previous,list):raise ValueError("catalog must be an array")
            for entry in previous:
                if not isinstance(entry,dict) or not isinstance(entry.get("barcode"),str):
                    raise ValueError("invalid existing product")
                products.setdefault(entry["barcode"],entry)
        except (ValueError,TypeError) as exc:
            p.exit(5,f"Existing catalog invalid; refusing to overwrite: {exc}\\n")
        ordered=sorted(products.values(),key=lambda x:(x["name"].casefold(),x["barcode"]))
        output="/* Open Food Facts ODbL https://world.openfoodfacts.org/ - community data; not verified shop availability. */\\n"
        output+="globalThis.KaloriPackagedFoods="+json.dumps(ordered,ensure_ascii=False,separators=(",",":"))+";\\n"
        if len(output.encode("utf-8"))>args.max_bytes:
            p.exit(4,"Merged output exceeds size budget; existing file unchanged.\\n")
    target.parent.mkdir(parents=True,exist_ok=True)
    handle=tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",dir=target.parent,delete=False,suffix=".tmp")
    try:
        with handle as out:out.write(output)
        os.replace(handle.name,target)
    finally:
        if os.path.exists(handle.name):os.unlink(handle.name)
    print(json.dumps({"products_exported":len(ordered),"search_page":args.page,
                      "page_size":args.page_size,"output":args.output},ensure_ascii=False))
if __name__=="__main__":main()
