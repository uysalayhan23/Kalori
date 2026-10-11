#!/usr/bin/env python3
"""Audit generated packaged-foods.js offline. No third-party packages."""
import argparse,json,re,sys
from pathlib import Path

PREFIX="globalThis.KaloriPackagedFoods="
def audit(path,max_bytes=5_000_000,min_products=0):
    raw=Path(path).read_text(encoding="utf-8")
    pos=raw.find(PREFIX)
    if pos<0:raise ValueError("Expected generated KaloriPackagedFoods assignment")
    payload=raw[pos+len(PREFIX):].strip()
    if not payload.endswith(";"):raise ValueError("Unterminated catalog")
    entries=json.loads(payload[:-1])
    if not isinstance(entries,list):raise ValueError("Catalog must be array")
    seen=set();errors=[];counts={"products":len(entries),"macros_complete":0,"barcode_duplicates":0}
    for i,p in enumerate(entries):
        name=p.get("name","")
        barcode=p.get("barcode","")
        if not isinstance(name,str) or not name.strip():errors.append(str(i)+": empty name")
        if not isinstance(barcode,str) or not re.fullmatch(r"\d{8,14}",barcode):errors.append(str(i)+": invalid barcode")
        if barcode in seen:counts["barcode_duplicates"]+=1
        seen.add(barcode)
        if p.get("verification")!="community_reported":errors.append(str(i)+": invalid verification")
        if p.get("store"):errors.append(str(i)+": unverified store promoted as confirmed")
        if p.get("sourceReference")!="https://world.openfoodfacts.org/product/"+barcode:
            errors.append(str(i)+": bad provenance URL")
        kcal=p.get("kcal")
        if isinstance(kcal,bool) or not isinstance(kcal,(int,float)) or not 0<=kcal<=900:
            errors.append(str(i)+": invalid kcal")
        for key in ("protein","fat","carbs"):
            val=p.get(key)
            if val is not None and (isinstance(val,bool) or not isinstance(val,(int,float)) or not 0<=val<=100):
                errors.append(str(i)+": invalid "+key)
        if all(isinstance(p.get(k),(int,float)) for k in ("protein","fat","carbs")):
            counts["macros_complete"]+=1
    if len(entries)<min_products:errors.append(f"Catalog has {len(entries)} products; at least {min_products} required")
    counts["file_bytes"]=Path(path).stat().st_size
    if counts["file_bytes"]>max_bytes:errors.append("APK/web size budget exceeded")
    if counts["barcode_duplicates"]:errors.append("duplicate barcodes")
    return counts,errors

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",default="packaged-foods.js")
    p.add_argument("--max-bytes",type=int,default=5_000_000)
    p.add_argument("--min-products",type=int,default=0,help="For release gating; default 0 to permit empty development catalogs")
    args=p.parse_args()
    if args.min_products<0:p.error("min-products must be nonnegative")
    counts,errors=audit(args.input,args.max_bytes,args.min_products)
    print(json.dumps({"counts":counts,"errors":errors[:40],"error_count":len(errors)},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=="__main__":sys.exit(main())
