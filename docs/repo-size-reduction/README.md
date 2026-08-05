# Repo size reduction

**Goal:** fresh `git clone` under **100 MB**.

**Plan (execution surface):** open [`index.html`](./index.html) in a browser.

**Status:** plan documented; cleanup **not** executed yet.

## Why this exists

Measured baseline (2026-08-04):

| Layer | Size | Files |
| --- | --- | --- |
| Working tree | ~10 GB | ~185k |
| Git pack / clone scale | ~469 MB | — |
| GitHub reported size | ~335 MB | — |
| HEAD tracked tip | ~1.0 GB | 8,212 |
| Code + prose core | ~14 MB | ~1,900 |

Most clone weight is committed experiment dumps and evidence JSON. Most IDE pain is local Mathlib (`.lake`) and Java vendor trees.

## Phase order (short)

0. Backup  
1. IDE excludes / local disk relief  
2. Sibling `prime-gap-structure-artifacts`  
3. Move or archive bulk  
4. `git rm --cached` + stronger `.gitignore`  
5. Optional viz/website trim  
6. History rewrite **or** clean slim remote (**required** for clone &lt; 100 MB)  
7. Verify + stay-thin policy  

Details, path lists, gates, and commands live in `index.html`.
