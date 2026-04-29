#!/bin/sh
set -eu

BIN="$1"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

if "$BIN" --help >"$TMPDIR/help.out" 2>"$TMPDIR/help.err"; then
    :
else
    echo "help command failed"
    exit 1
fi
test -s "$TMPDIR/help.out"
test ! -s "$TMPDIR/help.err"

if "$BIN" "" >"$TMPDIR/invalid.out" 2>"$TMPDIR/invalid.err"; then
    echo "invalid scale unexpectedly succeeded"
    exit 1
fi
test ! -s "$TMPDIR/invalid.out"
grep -q "invalid scale syntax" "$TMPDIR/invalid.err"

if "$BIN" --candidate-bound 0 10^3 >"$TMPDIR/bound.out" 2>"$TMPDIR/bound.err"; then
    echo "invalid bound unexpectedly succeeded"
    exit 1
fi
test ! -s "$TMPDIR/bound.out"
grep -q "invalid candidate bound" "$TMPDIR/bound.err"

if "$BIN" --candidate-bound 8 10^3 >"$TMPDIR/unresolved.out" 2>"$TMPDIR/unresolved.err"; then
    echo "unresolved chamber unexpectedly succeeded"
    exit 1
fi
test ! -s "$TMPDIR/unresolved.out"
grep -q "PGS chamber unresolved" "$TMPDIR/unresolved.err"

"$BIN" 10^3 >"$TMPDIR/success.out" 2>"$TMPDIR/success.err"
test "$(cat "$TMPDIR/success.out")" = '{"n":"1000","q":"1009"}'
test ! -s "$TMPDIR/success.err"

if "$BIN" 10^1233 >"$TMPDIR/huge.out" 2>"$TMPDIR/huge.err"; then
    echo "huge chamber unexpectedly succeeded"
    exit 1
fi
test ! -s "$TMPDIR/huge.out"
grep -q "PGS chamber unresolved" "$TMPDIR/huge.err"

printf "PGS CLI tests passed\n"
