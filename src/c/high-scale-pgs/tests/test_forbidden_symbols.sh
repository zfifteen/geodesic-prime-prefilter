#!/bin/sh
set -eu

ROOT="$1"
BIN="$2"
LIB="$3"

SOURCE_PATHS="$ROOT/include $ROOT/src"
FORBIDDEN_SOURCE="
mpz_nextprime
mpz_probab_prime_p
BN_generate_prime
BN_is_prime
z5d_
Miller
miller
trial
"

for token in $FORBIDDEN_SOURCE; do
    if grep -R -n "$token" $SOURCE_PATHS >/tmp/pgs_forbidden_source.out 2>/dev/null; then
        echo "forbidden source token: $token"
        cat /tmp/pgs_forbidden_source.out
        exit 1
    fi
done

FORBIDDEN_SYMBOLS="
__gmpz_nextprime
__gmpz_probab_prime_p
BN_generate_prime
BN_is_prime
z5d_
"

for token in $FORBIDDEN_SYMBOLS; do
    if nm -g "$BIN" "$LIB" 2>/dev/null | grep "$token" >/tmp/pgs_forbidden_symbol.out; then
        echo "forbidden linked symbol: $token"
        cat /tmp/pgs_forbidden_symbol.out
        exit 1
    fi
done

printf "PGS forbidden-symbol tests passed\n"
