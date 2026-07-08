#!/usr/bin/env python3
"""
S1 lemma consistency gate per strategist.
- FAIL on false Step E string.
- REQUIRE Sub-lemma 4c.2 + |R_ns| > L_eff + explicit L_lower derivation / bridge (M-2π(M)-4s or L_lower > L_eff) vs Step C.
- Drive the real audit_square_branches.py (shipped) with small limit; require its output contains "Auditing square branches" and no "BOUND VIOLATION".
No hard-coded transient session paths. Portable for normal clones. Runs real project tool.
"""
import sys, os, subprocess

PROOF = "PROOF.md"

def find_audit_script():
    # gate lives in docs/proof-enhancements/psp-closure/scripts/verify_...
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, "audit_square_branches.py")
    if os.path.exists(candidate):
        return candidate
    # fallback relative
    return os.path.join(here, "audit_square_branches.py")

def main():
    with open(PROOF) as f: proof = f.read()
    if "M > π(⌊r − √r⌋) + 2⌊√(M/2)⌋" in proof:
        print("FAIL: contains false Step E string"); sys.exit(1)
    if "Sub-lemma 4c.2 — Short-interval ℓ saturation" not in proof:
        print("FAIL: missing Sub-lemma 4c.2"); sys.exit(1)
    if "|R_ns| > L_eff" not in proof:
        print("FAIL: missing |R_ns| > L_eff"); sys.exit(1)
    # require explicit bridge/derivation from prior ineq (L_lower or M-2π-4s >0 or L_lower > L_eff)
    has_bridge = ("L_lower > L_eff" in proof) or ("M - 2π(M) - 4" in proof) or ("M - 2 * π(M) - 4" in proof) or ("L_lower - L_eff" in proof)
    has_lower = ("M - π(M) - 2" in proof) or ("L_lower = M" in proof)
    if not (has_bridge and has_lower):
        print("FAIL: missing explicit L_lower derivation or L_lower > L_eff bridge from prior inequalities"); sys.exit(1)

    # Drive real audit (portable, no hard-coded session path)
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

    print("PASS S1 gate (real audit driven, no transient hardcode, derivation present)")
    sys.exit(0)

if __name__=="__main__": main()
