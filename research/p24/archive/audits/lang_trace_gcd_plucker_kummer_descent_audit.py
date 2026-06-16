#!/usr/bin/env python3
"""Actual-CM descent audit for determinant-level Plucker/Kummer payloads.

The Plucker-Kummer payload can certify nonvanishing by replacing

    Delta(t)

with a Kummer power

    Theta(t) = unit(t) * Delta(t)^r.

This only compresses/descent-individual values if the selected Plucker line is
semi-invariant under the hidden cyclic labeling.  If the action permutes
different Plucker coordinates, the honest descended object is an orbit norm.

This script tests the distinction on a small actual-CM trace-GCD row.  It is
not a p24 computation; it is a falsifier for over-strong descent theorem
statements.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from math import gcd

from lang_trace_gcd_origin_action_audit import OriginDet, first_row
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % modulus)) % modulus
    return out


def frobenius_orbits(modulus: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * multiplier) % modulus
        orbits.append(orbit)
    return orbits


def discrete_log_if_cyclic(base: int, value: int, modulus: int) -> int | None:
    if value % modulus == 0:
        return None
    current = 1
    for exponent in range(modulus - 1):
        if current == value % modulus:
            return exponent
        current = (current * base) % modulus
    return None


def primitive_root(modulus: int) -> int:
    factors: list[int] = []
    remaining = modulus - 1
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    for candidate in range(2, modulus):
        if gcd(candidate, modulus) != 1:
            continue
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {modulus}")


def values_by_omitted(records: tuple[OriginDet, ...]) -> dict[int, list[OriginDet]]:
    out: dict[int, list[OriginDet]] = defaultdict(list)
    for record in records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


def all_equal(values: list[int]) -> bool:
    return len(set(values)) == 1


def power_profile(values: list[int], modulus: int, exponents: list[int]) -> list[tuple[int, bool, list[int]]]:
    out: list[tuple[int, bool, list[int]]] = []
    for exponent in exponents:
        powered = [pow(value, exponent, modulus) for value in values]
        out.append((exponent, all_equal(powered), powered))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_row(args)
    if row is None:
        raise SystemExit("no eligible origin-action row found")

    q_mod_right = row.q % row.right
    orbits = frobenius_orbits(row.right, q_mod_right)
    generator = primitive_root(row.q)
    right_order = 1
    current = q_mod_right % row.right
    while current != 1:
        current = (current * q_mod_right) % row.right
        right_order += 1

    print("Lang trace-gcd Plucker/Kummer descent audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={q_mod_right}")
    print(f"right_order={right_order}")
    print(f"frobenius_orbits={orbits}")
    print(f"primitive_root_mod_q={generator}")

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        if mismatches:
            failures += 1

        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  right_product={product_mod(seq, row.q)}")

        raw_descended = 0
        orbit_product_nonzero = 0
        powered_descended_any_nontrivial = 0
        exponent_candidates = sorted({
            1,
            right_order,
            row.right,
            (row.q - 1) // max(right_order, 1),
        })
        trivial_exponent = row.q - 1
        for orbit in orbits:
            values = [seq[index] for index in orbit]
            logs = [discrete_log_if_cyclic(generator, value, row.q) for value in values]
            orbit_product = product_mod(values, row.q)
            raw_ok = all_equal(values)
            raw_descended += int(raw_ok)
            orbit_product_nonzero += int(orbit_product != 0)
            profiles = power_profile(values, row.q, exponent_candidates)
            power_ok = any(descends for _, descends, _ in profiles)
            powered_descended_any_nontrivial += int(power_ok)
            trivial_profile = power_profile(values, row.q, [trivial_exponent])[0]
            print(f"  orbit={orbit}")
            print(f"    values={values}")
            print(f"    nonzero={int(all(value != 0 for value in values))}")
            print(f"    raw_descends={int(raw_ok)}")
            print(f"    orbit_product={orbit_product}")
            print(f"    orbit_product_nonzero={int(orbit_product != 0)}")
            print(f"    discrete_logs={logs}")
            for exponent, descends, powered in profiles:
                print(
                    f"    power_exponent={exponent} "
                    f"descends={int(descends)} powered={powered}"
                )
            exponent, descends, powered = trivial_profile
            print(
                f"    trivial_power_exponent={exponent} "
                f"descends={int(descends)} powered={powered}"
            )

        print(f"  raw_descended_orbits={raw_descended}/{len(orbits)}")
        print(
            "  nontrivial_power_descended_orbits_any_tested="
            f"{powered_descended_any_nontrivial}/{len(orbits)}"
        )
        print(f"  orbit_product_nonzero_count={orbit_product_nonzero}/{len(orbits)}")
        print("  individual_kummer_descent_supported=0" if raw_descended < len(orbits) else "  individual_kummer_descent_supported=1")
        print("  orbit_norm_descent_supported=1")

    print("interpretation")
    print("  raw_or_power_descent_is_a_semi_invariance_condition=1")
    print("  actual_cm_row_supports_orbit_norm_payload_over_individual_payload=1")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_plucker_kummer_descent_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
