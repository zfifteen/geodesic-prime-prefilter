"""Partition-first remainder pattern hunt."""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def zero_pattern_code(vec):
    c=0
    for i,v in enumerate(vec[:7]):
        if int(v)==0: c |= 1<<i
    return c

def primorial_level(n):
    n=int(n)
    if n<=0: return 0
    for p in (2310,210,30,6,2):
        if n%p==0: return p
    return 0

def gap_size_regime(g):
    g=int(g)
    if g<=2: return "twin_g2"
    if g<=6: return "small_g3_6"
    if g<=20: return "medium_g7_20"
    if g<=100: return "large_g21_100"
    return "xlarge_g101plus"

def norm_position_bin(k,g,n_bins=10):
    if g<=0: return 0
    return min(max(int(k)*n_bins//int(g),0),n_bins-1)

def record_features(rec):
    vec=rec["remainder_vector"]; p=int(rec["p"]); g=int(rec["g"]); k=int(rec.get("k",0))
    n=int(rec.get("n",p+k))
    dist=int(rec.get("distance_to_next_prime",rec.get("termination_distance",99)))
    is_gwr=bool(rec.get("is_current_min_d") or rec.get("is_gwr_winner"))
    return {"p_mod_30":p%30,"position_bin":norm_position_bin(k,g),"gap_regime":gap_size_regime(g),
            "zero_pattern_code":zero_pattern_code(vec),"primorial_level":primorial_level(n),
            "is_gwr":is_gwr,"dist_eq_1":dist==1}

def aggregate_cells(records):
    cells={}; pat={}; gc=gd=0
    for feat in records:
        key=(feat["p_mod_30"],feat["position_bin"],feat["gap_regime"])
        cell=cells.setdefault(key,{"p_mod_30":key[0],"position_bin":key[1],"gap_regime":key[2],
            "count":0,"dist_eq_1":0,"gwr_count":0,"gwr_dist_eq_1":0,"primorial_level_hist":{}})
        cell["count"]+=1; gc+=1
        if feat["dist_eq_1"]: cell["dist_eq_1"]+=1; gd+=1
        if feat["is_gwr"]:
            cell["gwr_count"]+=1
            if feat["dist_eq_1"]: cell["gwr_dist_eq_1"]+=1
        pl=str(feat["primorial_level"])
        cell["primorial_level_hist"][pl]=cell["primorial_level_hist"].get(pl,0)+1
        pat[(*key,feat["zero_pattern_code"])]=pat.get((*key,feat["zero_pattern_code"]),0)+1
    cl=[]
    for cell in cells.values():
        c=cell["count"]
        cell["dist_eq_1_rate"]=cell["dist_eq_1"]/c if c else 0
        cell["gwr_rate"]=cell["gwr_count"]/c if c else 0
        cell["gwr_dist_eq_1_rate"]=cell["gwr_dist_eq_1"]/cell["gwr_count"] if cell["gwr_count"] else 0
        cl.append(cell)
    cl.sort(key=lambda x:(-x["count"],x["p_mod_30"],x["position_bin"],x["gap_regime"]))
    top=[{"p_mod_30":a,"position_bin":b,"gap_regime":c,"zero_pattern_code":z,"count":n}
         for (a,b,c,z),n in sorted(pat.items(),key=lambda x:-x[1])[:50]]
    return {"record_count":gc,"global_dist_eq_1_rate":gd/gc if gc else 0,"cell_count":len(cl),"cells":cl,"top_zero_pattern_codes":top}

def structural_laws(summary):
    laws=[]; base=summary["global_dist_eq_1_rate"]
    p29=[c for c in summary["cells"] if c["p_mod_30"]==29 and c["position_bin"]==0 and c["gap_regime"]!="twin_g2"]
    if p29: laws.append({"id":"p29_doorstep_decoy","records":sum(c["count"] for c in p29),"mean_gwr_rate":sum(c["gwr_rate"] for c in p29)/len(p29)})
    interior=[c for c in summary["cells"] if c["position_bin"]<=8 and c["count"]>=300]
    hi=sorted([{**c,"lift":c["dist_eq_1_rate"]/base} for c in interior if base and c["dist_eq_1_rate"]/base>=1.5], key=lambda x:-x["lift"])[:12]
    if hi: laws.append({"id":"interior_high_lift","cells":hi})
    null=[c for c in summary["cells"] if c["count"]>=500 and c["dist_eq_1_rate"]<base*0.85][:8]
    if null: laws.append({"id":"null_low_termination_cells","cells":null})
    return laws

def run_probe(jsonl: Path, out: Path, max_records=None):
    feats=[]
    with jsonl.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            feats.append(record_features(json.loads(line)))
            if max_records and len(feats)>=max_records: break
    agg=aggregate_cells(feats)
    payload={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"source_jsonl":str(jsonl.resolve()),
        "surface_label":"pattern_hunt_surface_max_p_400000",
        "repro_command":f"python research/remainders/pattern_hunt.py --jsonl {jsonl} --output {out}",
        "partition_keys":["p_mod_30","position_bin","gap_regime"],
        "joint_features":["zero_pattern_code","primorial_level"],
        "summary":agg,"structural_laws":structural_laws(agg)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload,indent=2), encoding="utf-8")
    return payload

def main():
    here=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser()
    ap.add_argument("--jsonl", type=Path, default=here/"output/pattern_hunt_surface/raw_records.jsonl")
    ap.add_argument("--output", type=Path, default=here/"correlations/investigation/pattern_partition_summary.json")
    ap.add_argument("--max-records", type=int, default=None)
    args=ap.parse_args()
    if not args.jsonl.is_file():
        print("missing jsonl", file=sys.stderr); return 1
    p=run_probe(args.jsonl,args.output,args.max_records)
    print(json.dumps({"records":p["summary"]["record_count"],"cells":p["summary"]["cell_count"]}))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
