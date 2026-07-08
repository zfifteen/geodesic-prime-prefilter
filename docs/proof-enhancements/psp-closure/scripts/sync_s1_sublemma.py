#!/usr/bin/env python3
"""
Sync canonical s1-sublemma-4c2.md into PROOF.md and psp-closure/README.md
between fixed markers. Gate runs this and FAILs on drift.
"""
import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
CANON = os.path.join(REPO, 'docs/proof-enhancements/psp-closure/s1-sublemma-4c2.md')
PROOF = os.path.join(REPO, 'PROOF.md')
README = os.path.join(REPO, 'docs/proof-enhancements/psp-closure/README.md')

BEGIN = '<!-- BEGIN S1-SUBLEMMA-4C2 -->'
END = '<!-- END S1-SUBLEMMA-4C2 -->'

def load_canon():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "s1-sublemma-4c2.md"),
        os.path.join(os.path.abspath(os.path.join(here, "..", "..", "..", "..")), "docs/proof-enhancements/psp-closure/s1-sublemma-4c2.md"),
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c) as f: return f.read().strip()
    raise FileNotFoundError("canonical not found at " + str(candidates))

def sync_file(path, content):
    with open(path) as f:
        txt = f.read()
    pat = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END), re.S)
    if not pat.search(txt):
        print(f"FAIL: no markers in {path}")
        sys.exit(1)
    new = pat.sub(BEGIN + '\n' + content + '\n' + END, txt)
    if new == txt:
        print(f"OK: {path} in sync")
        return False
    with open(path, 'w') as f:
        f.write(new)
    print(f"UPDATED: {path}")
    return True

def main():
    canon = load_canon()
    changed = False
    changed |= sync_file(PROOF, canon)
    changed |= sync_file(README, canon)
    if changed:
        print("Changes applied; re-run to verify.")
        # For gate, we can exit non-zero if we want strict, but here we updated.
    else:
        print("All in sync.")
    sys.exit(0 if not changed else 2)  # 2 to signal updated if gate wants

if __name__ == "__main__":
    main()
