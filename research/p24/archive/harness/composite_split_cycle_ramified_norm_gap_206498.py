#!/usr/bin/env python3
"""Ramified-prime extension of the p24 split-cycle norm-gap search.

The previous gap closure to norm 206498 searched signed split-prime-power
products only.  The earlier norm-66254 audit had separately checked the
ramified prime 599, but the widened window had not.  This script adds the
ramified class above 599 to the same exhaustive norm search.
"""

from __future__ import annotations

import argparse
import math

import sympy as sp
from cypari2 import Pari

from composite_split_cycle_audit import (
    CLASS_NUMBER,
    D_K,
    GENERATOR_PRIME,
    TARGET_INDICES,
    PrimeLog,
    class_log,
    exhaustive_norm_search,
    split_prime_logs,
)


RAMIFIED_PRIME = 599
KNOWN_RECOVERY_NORM = 206_498


def ramified_prime_log() -> PrimeLog:
    pari = Pari()
    pari.allocatemem(512 * 1024 * 1024)
    nucomp_l = int((abs(D_K) // 4) ** 0.25) + 1
    generator = pari.qfbprimeform(D_K, GENERATOR_PRIME)
    form = pari.qfbprimeform(D_K, RAMIFIED_PRIME)
    log_value = class_log(pari, generator, form, nucomp_l)
    index = math.gcd(CLASS_NUMBER, log_value)
    return PrimeLog(RAMIFIED_PRIME, log_value, CLASS_NUMBER // index, index)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--norm-bound", type=int, default=KNOWN_RECOVERY_NORM - 1)
    parser.add_argument("--show", type=int, default=8)
    args = parser.parse_args()

    rows = split_prime_logs(args.norm_bound)
    ramified = ramified_prime_log()
    rows_with_ramified = sorted(rows + [ramified], key=lambda row: row.ell)
    exhaustive = exhaustive_norm_search(rows_with_ramified, args.norm_bound)

    print("p24 composite split-cycle ramified norm-gap audit")
    print(f"D_K={D_K}")
    print(f"class_number={CLASS_NUMBER}")
    print(f"class_number_factorization={sp.factorint(CLASS_NUMBER)}")
    print(f"norm_bound={args.norm_bound}")
    print(f"split_prime_logs={len(rows)}")
    print(
        f"ramified_prime={ramified.ell} log={ramified.log} "
        f"index={ramified.index} order={ramified.order}"
    )
    print(f"rows_with_ramified={len(rows_with_ramified)}")
    print()

    print(f"exhaustive_signed_split_or_ramified_prime_power_products_norm_le_{args.norm_bound}")
    for index in TARGET_INDICES:
        selected = [hit for hit in exhaustive if hit.index == index]
        print(f"  index_{index}")
        for hit in selected[: min(args.show, 8)]:
            print(
                f"    norm={hit.norm:8d} order={hit.order:12d} "
                f"signed_prime_powers={hit.signed_primes!s:24s} log={hit.log}"
            )
        if not selected:
            print("    none")
    print()

    recovery_hits = [hit for hit in exhaustive if hit.index == 66_254]
    print("interpretation")
    print(f"  ramified_prime_599_included=1")
    print(
        "  no_order_3107441_representative_below_known_norm_with_599="
        f"{int(not recovery_hits)}"
    )
    print("conclusion=reported_composite_split_cycle_ramified_norm_gap_206498")

    if recovery_hits:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
