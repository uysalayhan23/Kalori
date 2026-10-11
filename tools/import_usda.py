#!/usr/bin/env python3
"""Convert manually selected USDA FoodData Central details into a compact, auditable catalog.
No network access, no dependency beyond Python 3; explicit Turkish mapping is mandatory.
Input: --foods usda_details.json  --mapping mappings.json --output verified-foods.json
USDA data are CC0. Never commit API keys.
"""
import argparse,json,datetime,pathlib,sys

NUTRIENTS={"protein":1003,"fat":1004,"carbs":1005}
ENERGY_PREFERENCE=(2048,2047,1008)

def nutrient_map(record):
    out={}
    for item in record.get("foodNutrients",[]):
        n=item.get("nutrient") or {}
        nid=n.get("id",item.get("nutrientId"))
        unit=n.get("unitName",item.get("unitName",""))
        amount=item.get("amount",item.get("value"))
        if nid is None or amount is None:continue
        try:
            nid=int(nid);amount=float(amount)
        except (ValueError,TypeError):continue
        out[nid]=(amount,str(unit).lower())
    return out

def translate(record,mapping):
    if record.get("dataType") not in ("Foundation","SR Legacy","Survey (FNDDS)"):
        raise ValueError("Unsupported data type / branded serving-based record")
    refid=record.get("fdcId")
    if not isinstance(refid,int):raise ValueError("Missing FDC ID")
    n=nutrient_map(record)
    missing=[k for k,v in NUTRIENTS.items() if v not in n or n[v][1]!="g"]
    if missing:raise ValueError("Missing macros or unit mismatch: "+",".join(missing))
    energy=next(((v,n[k][0]) for k,v in enumerate(ENERGY_PREFERENCE) if v in n and n[v][1]=="kcal"),None)
    if energy is None:raise ValueError("Missing kcal/100g energy (2048/2047/1008)")
    nutrient_id,kcal=energy
    macros={key:round(n[nid][0],3) for key,nid in NUTRIENTS.items()}
    if any(x<0 or x>100 for x in macros.values()) or not (0<=kcal<=900):
        raise ValueError("Nutrient outside plausible bounds")
    if not mapping.get("name_tr") or not mapping.get("category"):
        raise ValueError("Human-reviewed Turkish name and category are required")
    if not mapping.get("preparation_confirmed") or not mapping.get("per_100g_confirmed"):
        raise ValueError("Preparation state and unit basis must be manually confirmed")
    return dict(id="usda-"+str(refid),name=mapping["name_tr"],category=mapping["category"],
                kcal=round(kcal,3),protein=macros["protein"],fat=macros["fat"],carbs=macros["carbs"],
                source="USDA FoodData Central",verification="source_matched",
                sourceReference="https://fdc.nal.usda.gov/food-details/"+str(refid)+"/nutrients",
                fdcId=refid,energyNutrientId=nutrient_id,sourceDescription=record.get("description"),
                dataType=record["dataType"],basis="100 g edible portion",preparation=mapping["preparation"],
                checkedDate=datetime.date.today().isoformat())

def main():
    p=argparse.ArgumentParser();p.add_argument("--foods",required=True);p.add_argument("--mapping",required=True);p.add_argument("--output",required=True);args=p.parse_args()
    payload=json.loads(pathlib.Path(args.foods).read_text(encoding="utf-8"))
    records=payload if isinstance(payload,list) else payload.get("foods",[payload])
    mapping=json.loads(pathlib.Path(args.mapping).read_text(encoding="utf-8"))
    indexed={str(x.get("fdcId")):x for x in records}
    out=[];errors=[]
    for fdcid,meta in mapping.items():
        if fdcid not in indexed:errors.append(fdcid+": FDC record missing");continue
        try:out.append(translate(indexed[fdcid],meta))
        except (ValueError,KeyError) as exc:errors.append(fdcid+": "+str(exc))
    if errors:
        print("\n".join(errors),file=sys.stderr);return 1
    if not out:print("No reviewed mappings; refusing empty output",file=sys.stderr);return 1
    pathlib.Path(args.output).write_text(json.dumps({"version":1,"source":"USDA FDC","foods":out},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Exported",len(out),"source-matched records")
    return 0
if __name__=="__main__":sys.exit(main())
