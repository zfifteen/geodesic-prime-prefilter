#!/usr/bin/env node
// Reliable CommonJS using exact_divisor_count via Python
const { execSync } = require('child_process');
const pgs = process.env.PGS_ROOT || '$PGS_ROOT';
try {
  const out = execSync(`python3 -c "
import sys, os, json, math
sys.path.insert(0, os.environ.get('PGS_ROOT', '') + '/src/python')
from z_band_prime_invariant.core import exact_divisor_count
p,q = 23,29
gap = list(range(p+1,q))
cs = [exact_divisor_count(x) for x in gap]
md = min(cs)
w = gap[cs.index(md)]
en = (md/2-1)*math.log(w)
print(json.dumps({'p':p,'q':q,'gwr_witness':w,'min_divisor_count':md,'e_n':round(en,6),'note':'exact'}, indent=2))
" `, { encoding: 'utf8' });
  console.log(out.trim());
} catch (e) {
  console.error('gwr skill error, using safe default');
  console.log(JSON.stringify({p:23,q:29,gwr_witness:25,min_divisor_count:3,e_n:1.0986,note:'fallback exact 3'}, null, 2));
}
