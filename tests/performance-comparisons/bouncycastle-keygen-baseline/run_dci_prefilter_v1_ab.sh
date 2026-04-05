#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$ROOT_DIR/build"
CLASSES_DIR="$BUILD_DIR/classes"
BASELINE_BC_SOURCE_DIR="$ROOT_DIR/vendor/bc-java-r1rv83"
MODIFIED_BC_SOURCE_DIR="$ROOT_DIR/vendor/bc-java-r1rv83-dci-prefilter-v1"
BASELINE_JAR_PATH="$BASELINE_BC_SOURCE_DIR/prov/build/libs/bcprov-jdk18on-1.83.jar"
MODIFIED_JAR_PATH="$MODIFIED_BC_SOURCE_DIR/prov/build/libs/bcprov-jdk18on-1.83.jar"
BASELINE_SOURCE_PATH="$ROOT_DIR/src/BouncyCastleKeygenBaseline.java"
MODIFIED_SOURCE_PATH="$ROOT_DIR/src/BouncyCastleKeygenDciPrefilterV1Benchmark.java"
BASELINE_OUTPUT_PATH="$ROOT_DIR/results/bcprov-jdk18on-1.83-source-r1rv83-rsa4096-direct-core-seed-byte-42-runs-100-fresh-baseline.json"
MODIFIED_OUTPUT_PATH="$ROOT_DIR/results/bcprov-jdk18on-1.83-source-r1rv83-dci-prefilter-v1-rsa4096-direct-core-seed-byte-42-runs-100.json"
REPORT_PATH="$ROOT_DIR/results/BOUNCY_CASTLE_DCI_PREFILTER_V1_AB_REPORT.md"
SAMPLE_BEHAVIOR_JSON="$ROOT_DIR/results/bcprov-jdk18on-1.83-source-r1rv83-prime-sample-behavior-seed-byte-42.json"
BC_BUILD_JAVA_HOME="/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home"
BC_RUNTIME_JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"

mkdir -p "$CLASSES_DIR" "$(dirname "$BASELINE_OUTPUT_PATH")"

if [ ! -d "$BASELINE_BC_SOURCE_DIR" ]; then
  echo "Missing baseline Bouncy Castle source tree: $BASELINE_BC_SOURCE_DIR" >&2
  exit 1
fi

if [ ! -d "$MODIFIED_BC_SOURCE_DIR" ]; then
  echo "Missing modified Bouncy Castle source tree: $MODIFIED_BC_SOURCE_DIR" >&2
  exit 1
fi

JAVA_HOME="$BC_BUILD_JAVA_HOME" PATH="$BC_BUILD_JAVA_HOME/bin:$PATH" \
  "$BASELINE_BC_SOURCE_DIR/gradlew" -p "$BASELINE_BC_SOURCE_DIR" :prov:jar --console=plain

JAVA_HOME="$BC_BUILD_JAVA_HOME" PATH="$BC_BUILD_JAVA_HOME/bin:$PATH" \
  "$MODIFIED_BC_SOURCE_DIR/gradlew" -p "$MODIFIED_BC_SOURCE_DIR" :prov:jar --console=plain

if [ ! -f "$BASELINE_JAR_PATH" ]; then
  echo "Expected baseline jar not found: $BASELINE_JAR_PATH" >&2
  exit 1
fi

if [ ! -f "$MODIFIED_JAR_PATH" ]; then
  echo "Expected modified jar not found: $MODIFIED_JAR_PATH" >&2
  exit 1
fi

jar tf "$BASELINE_JAR_PATH" | grep -q '^org/bouncycastle/util/BigIntegers.class$'
jar tf "$BASELINE_JAR_PATH" | grep -q '^org/bouncycastle/crypto/generators/RSAKeyPairGenerator.class$'
jar tf "$MODIFIED_JAR_PATH" | grep -q '^org/bouncycastle/util/BigIntegers.class$'
jar tf "$MODIFIED_JAR_PATH" | grep -q '^org/bouncycastle/crypto/generators/RSAKeyPairGenerator.class$'

BC_BUILD_JAVA_VERSION="$("$BC_BUILD_JAVA_HOME/bin/java" -version 2>&1 | head -n 1)"
BC_RUNTIME_JAVA_VERSION="$("$BC_RUNTIME_JAVA_HOME/bin/java" -version 2>&1 | head -n 1)"
BASELINE_BUILT_JAR_SHA256="$(shasum -a 256 "$BASELINE_JAR_PATH" | awk '{print $1}')"
MODIFIED_BUILT_JAR_SHA256="$(shasum -a 256 "$MODIFIED_JAR_PATH" | awk '{print $1}')"

JAVA_HOME="$BC_RUNTIME_JAVA_HOME" PATH="$BC_RUNTIME_JAVA_HOME/bin:$PATH" \
  javac -cp "$BASELINE_JAR_PATH" -d "$CLASSES_DIR" "$BASELINE_SOURCE_PATH"

JAVA_HOME="$BC_RUNTIME_JAVA_HOME" PATH="$BC_RUNTIME_JAVA_HOME/bin:$PATH" \
  javac -cp "$MODIFIED_JAR_PATH" -d "$CLASSES_DIR" "$MODIFIED_SOURCE_PATH"

JAVA_HOME="$BC_RUNTIME_JAVA_HOME" PATH="$BC_RUNTIME_JAVA_HOME/bin:$PATH" \
  java \
    -Dbc.build.java.version="$BC_BUILD_JAVA_VERSION" \
    -Dbc.runtime.java.version="$BC_RUNTIME_JAVA_VERSION" \
    -Dbc.built.jar.sha256="$BASELINE_BUILT_JAR_SHA256" \
    -cp "$BASELINE_JAR_PATH:$CLASSES_DIR" \
    BouncyCastleKeygenBaseline \
    "$BASELINE_OUTPUT_PATH"

JAVA_HOME="$BC_RUNTIME_JAVA_HOME" PATH="$BC_RUNTIME_JAVA_HOME/bin:$PATH" \
  java \
    -Dbc.build.java.version="$BC_BUILD_JAVA_VERSION" \
    -Dbc.runtime.java.version="$BC_RUNTIME_JAVA_VERSION" \
    -Dbc.built.jar.sha256="$MODIFIED_BUILT_JAR_SHA256" \
    -cp "$MODIFIED_JAR_PATH:$CLASSES_DIR" \
    BouncyCastleKeygenDciPrefilterV1Benchmark \
    "$MODIFIED_OUTPUT_PATH"

python3 - "$BASELINE_OUTPUT_PATH" "$MODIFIED_OUTPUT_PATH" "$REPORT_PATH" "$SAMPLE_BEHAVIOR_JSON" <<'PY'
import json
import pathlib
import sys

baseline_path = pathlib.Path(sys.argv[1])
modified_path = pathlib.Path(sys.argv[2])
report_path = pathlib.Path(sys.argv[3])
sample_behavior_path = pathlib.Path(sys.argv[4])

baseline = json.loads(baseline_path.read_text())
modified = json.loads(modified_path.read_text())

baseline_summary = baseline["summary"]
modified_summary = modified["summary"]

baseline_total_ms = float(baseline_summary["total_time_ms"])
modified_total_ms = float(modified_summary["total_time_ms"])
baseline_mean_ms = float(baseline_summary["mean_time_ms"])
modified_mean_ms = float(modified_summary["mean_time_ms"])
baseline_median_ms = float(baseline_summary["median_time_ms"])
modified_median_ms = float(modified_summary["median_time_ms"])
baseline_min_ms = float(baseline_summary["min_time_ms"])
modified_min_ms = float(modified_summary["min_time_ms"])
baseline_max_ms = float(baseline_summary["max_time_ms"])
modified_max_ms = float(modified_summary["max_time_ms"])

speedup = baseline_total_ms / modified_total_ms
reduction_percent = (1.0 - (modified_total_ms / baseline_total_ms)) * 100.0
baseline_throughput = 1000.0 / baseline_mean_ms
modified_throughput = 1000.0 / modified_mean_ms

sample_reference = "./" + sample_behavior_path.name
baseline_reference = "./" + baseline_path.name
modified_reference = "./" + modified_path.name

report = f"""# Bouncy Castle DCI Prefilter V1 A/B Report

Date: {modified["completed_at_utc"][:10]}

This report compares a fresh paired baseline run of source-built BC `r1rv83` against a source-built BC `r1rv83` build patched with the DCI concrete-factor prefilter inside `BigIntegers.createRandomPrime()`.

This experiment measures the real DCI prefilter path. It does not include the earlier RSA upper-band optimization.

## Headline Result

- Fresh paired baseline total time: `{baseline_total_ms:.6f}` ms
- DCI-prefilter total time: `{modified_total_ms:.6f}` ms
- Relative speed: `{speedup:.6f}x`
- Wall-clock reduction: `{reduction_percent:.6f}%`

## A/B Comparison

| Metric | Fresh baseline | DCI prefilter v1 |
|---|---:|---:|
| Total time (ms) | `{baseline_total_ms:.6f}` | `{modified_total_ms:.6f}` |
| Mean time (ms) | `{baseline_mean_ms:.6f}` | `{modified_mean_ms:.6f}` |
| Median time (ms) | `{baseline_median_ms:.6f}` | `{modified_median_ms:.6f}` |
| Min time (ms) | `{baseline_min_ms:.6f}` | `{modified_min_ms:.6f}` |
| Max time (ms) | `{baseline_max_ms:.6f}` | `{modified_max_ms:.6f}` |
| Throughput (keypairs/s) | `{baseline_throughput:.6f}` | `{modified_throughput:.6f}` |

## Setup

- Workload: direct-core `org.bouncycastle.crypto.generators.RSAKeyPairGenerator`
- RSA size: `4096` bits
- Timed iterations: `100`
- Warmup iterations: `0`
- Public exponent: `65537`
- Certainty: `144`
- RNG: `SHA1PRNG`
- Seed bytes: `[42]`
- Build JDK: `{baseline["provenance"]["bc_build_java_version"]}`
- Runtime JDK: `{baseline["provenance"]["bc_runtime_java_version"]}`

The modified build is a pure `createRandomPrime()` DCI-prefilter patch:

- BC raw candidate construction unchanged
- BC `3..743` small-prime product walk unchanged
- DCI primary ladder: odd primes `> 743` through `200003`
- DCI tail ladder: odd primes `> 200003` through `300007`
- Chunk size: `256`
- No deep tail
- No upper-band logic
- No RSA-local changes
- No later probable-prime or key-validation changes

## Prior Sample-Behavior Result

The prior no-patch sample-behavior probe at [`{sample_behavior_path.name}`]({sample_reference}) found:

- exact helper fidelity to BC for the first `1024` outputs on both `256`-bit and `2048`-bit panels
- `0.0` drift on the recorded coarse emitted-prime metrics after adding this exact DCI ladder at the `createRandomPrime()` surface

## Artifacts

- Fresh paired baseline JSON: [`{baseline_path.name}`]({baseline_reference})
- DCI-prefilter JSON: [`{modified_path.name}`]({modified_reference})
- Sample-behavior JSON: [`{sample_behavior_path.name}`]({sample_reference})
"""

report_path.write_text(report, encoding="utf-8")
print(f"wrote {report_path}")
PY
