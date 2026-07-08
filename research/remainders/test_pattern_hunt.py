from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
from pattern_hunt import record_features, primorial_level

def test_core():
    rec={"p":29,"g":2,"k":1,"n":30,"remainder_vector":[0,0,0,2,0,30,30],"is_current_min_d":True,"distance_to_next_prime":1}
    assert record_features(rec)["p_mod_30"]==29
    assert primorial_level(30)==30

def test_runner_tiny():
    j=HERE/"correlations/enriched/tiny_enriched.jsonl"
    if not j.is_file(): pytest.skip("no tiny")
    o=HERE/"correlations/investigation/pattern_partition_tiny_test.json"
    p=subprocess.run([sys.executable,str(HERE/"pattern_hunt.py"),"--jsonl",str(j),"--output",str(o)],cwd=str(ROOT),capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    assert "zero_pattern_code" in json.loads(o.read_text())["joint_features"]
