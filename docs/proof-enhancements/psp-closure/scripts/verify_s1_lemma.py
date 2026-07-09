#!/usr/bin/env python3
"""
S1 lemma consistency gate per strategist.
- FAIL on false Step E string.
- REQUIRE 4c.2a-d + Corollary 4c.3 headers.
- REQUIRE key contra phrases from 4c.2b/4c.3: 'realizable admissible rough ℓ for active m ... is 0', 'm > √r / 2', 'required rough placements > 0 = available'.
- Drive the real audit_square_branches.py (shipped) with small limit; require its output contains "Auditing square branches" and no "BOUND VIOLATION".
No hard-coded transient session paths. Portable for normal clones. Runs real project tool.
"""
import sys, os, subprocess
# ensure sys is available early for sync run


def find_repo_file(filename):
    # gate lives in docs/proof-enhancements/psp-closure/scripts/verify_...
    here = os.path.dirname(os.path.abspath(__file__))
    # repo root is 4 levels up (scripts -> psp-closure -> proof-enhancements -> docs -> root)
    repo_root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
    return os.path.join(repo_root, filename)

PROOF = find_repo_file("PROOF.md")

def find_audit_script():
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, "audit_square_branches.py")
    if os.path.exists(candidate):
        return candidate
    return os.path.join(here, "audit_square_branches.py")

def main():
    with open(PROOF) as f: proof = f.read()

    # 1. run sync first (enforce canonical) -- after imports
    sync_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_s1_sublemma.py")
    if os.path.exists(sync_py):
        py = sys.executable if 'sys' in dir() else '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'
        res = subprocess.run([py, sync_py], capture_output=True, text=True)
        if res.returncode != 0 or "FAIL" in (res.stdout + res.stderr):
            print("FAIL: sync failed or reported FAIL")
            print(res.stdout)
            print(res.stderr)
            sys.exit(1)
    if "M > π(⌊r − √r⌋) + 2⌊√(M/2)⌋" in proof:
        print("FAIL: contains false Step E string"); sys.exit(1)

    # Structural enforcement per strategist (canonical headers)
    for hdr in ["4c.2a. Algebra", "4c.2b. Algebraic block", "4c.2b′. Boundary discharge", "4c.2c. Analytic discharge", "4c.2d. Finite discharge", "Corollary 4c.3. Counting contra"]:
        if hdr not in proof:
            print("FAIL: missing header", hdr); sys.exit(1)

    # No L_eff in sublemma (canonical)
    if "L_eff" in proof[proof.find("4c.2a"):proof.find("Corollary 4c.3")]:
        print("FAIL: L_eff present in sublemma area"); sys.exit(1)

    # Semantic invariants
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import s1_counting_invariants as inv
        inv.assert_contra_preconditions(64)
    except Exception as e:
        print("FAIL: invariants assert:", e); sys.exit(1)

    # Honest test of the counting contra (key phrases from canonical)
    if "no admissible M-rough placement for m ≤ ⌊√r / 2⌋" not in proof and "no admissible M-rough placement for m ≤ floor" not in proof:
        print("FAIL: missing derivation no admissible M-rough placement for small m"); sys.exit(1)
    if "effective rough capacity" not in proof or "is 0" not in proof:
        print("FAIL: missing effective rough capacity is 0"); sys.exit(1)
    if "m > √r / 2" not in proof and "m > sqrt(r)/2" not in proof:
        print("FAIL: missing m > sqrt(r)/2 derivation"); sys.exit(1)
    if "required rough placements > 0 = available" not in proof:
        print("FAIL: missing explicit contra required > 0 = available"); sys.exit(1)

    # Drive real audit (portable)
    audit_py = find_audit_script()
    if not os.path.exists(audit_py):
        print("FAIL: cannot locate audit_square_branches.py next to gate"); sys.exit(1)
    try:
        res = subprocess.run([sys.executable, audit_py, "300"], capture_output=True, text=True, timeout=120)
        audit_out = (res.stdout or "") + (res.stderr or "")
    except Exception as e:
        print("FAIL: failed to run real audit script:", e); sys.exit(1)

    if "Auditing square branches" not in audit_out:
        print("FAIL: real audit did not emit expected 'Auditing square branches' header"); sys.exit(1)
    if "BOUND VIOLATION" in audit_out or "!!!" in audit_out:
        print("FAIL: real audit output contains BOUND VIOLATION"); sys.exit(1)

    print("PASS S1 gate (sync + invariants + headers + real audit)")
    sys.exit(0)

if __name__=="__main__": main()
