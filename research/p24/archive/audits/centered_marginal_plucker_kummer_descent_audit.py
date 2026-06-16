#!/usr/bin/env python3
"""Descent audit for centered determinant/Plucker payloads.

The centered certificate target is the right determinant sequence

    Delta_C(t), t mod right.

A determinant-level Kummer theorem could try to construct individual powers

    Theta(t) = unit(t) * Delta_C(t)^e

that descend on Frobenius orbits.  If no informative exponent makes the
values constant on the small actual-CM orbits, the honest centered payload is
the orbit product/norm rather than individual Plucker-Kummer values.
"""

from __future__ import annotations

import argparse
from math import gcd, lcm

import sympy as sp

from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import product_mod, scan
from hermitian_mixed_frobenius_orbit_audit import q_orbits


def primitive_root(modulus: int) -> int:
    return int(sp.primitive_root(modulus))


def discrete_log_table(q: int) -> tuple[int, dict[int, int]]:
    generator = primitive_root(q)
    table: dict[int, int] = {}
    value = 1
    for exponent in range(q - 1):
        table[value] = exponent
        value = value * generator % q
    if len(table) != q - 1:
        raise RuntimeError("primitive root table did not cover F_q^*")
    return generator, table


def smallest_constancy_exponent(logs: list[int], modulus: int) -> int:
    if len(logs) <= 1:
        return 1
    base = logs[0]
    exponent = 1
    for value in logs[1:]:
        diff = (value - base) % modulus
        if diff == 0:
            continue
        exponent = lcm(exponent, modulus // gcd(modulus, diff))
    return exponent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible centered Plucker/Kummer row found")
    sequence = normalized_right_sequence(row)
    if any(value == 0 for value in sequence):
        raise SystemExit("target has zero determinant; descent audit expects units")

    generator, logs = discrete_log_table(row.q)
    modulus = row.q - 1
    orbits = [[0]] + q_orbits(row.right, row.q)
    right_order = int(sp.n_order(row.q % row.right, row.right))
    tested_exponents = sorted({
        1,
        right_order,
        row.right,
        (row.q - 1) // max(right_order, 1),
    })

    print("Centered marginal Plucker/Kummer descent audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"right_order={right_order}")
    print(f"primitive_root_mod_q={generator}")
    print(f"tested_exponents={tested_exponents}")
    print(f"right_values={sequence}")
    print()

    raw_descended = 0
    raw_descended_nontrivial = 0
    small_power_descended = 0
    small_power_descended_nontrivial = 0
    orbit_product_nonzero = 0
    informative_exponents: list[int] = []
    for orbit in orbits:
        values = [sequence[index] % row.q for index in orbit]
        orbit_logs = [logs[value] for value in values]
        orbit_product = product_mod(values, row.q)
        raw_ok = len(set(values)) == 1
        min_exponent = smallest_constancy_exponent(orbit_logs, modulus)
        tested_profiles = [
            (exponent, len({pow(value, exponent, row.q) for value in values}) == 1)
            for exponent in tested_exponents
        ]
        is_nontrivial_orbit = len(orbit) > 1
        raw_descended += int(raw_ok)
        raw_descended_nontrivial += int(is_nontrivial_orbit and raw_ok)
        orbit_product_nonzero += int(orbit_product != 0)
        if min_exponent < modulus:
            informative_exponents.append(min_exponent)
        small_power_ok = any(ok and exponent < modulus for exponent, ok in tested_profiles)
        small_power_descended += int(small_power_ok)
        small_power_descended_nontrivial += int(is_nontrivial_orbit and small_power_ok)
        print(f"orbit={orbit}")
        print(f"  values={values}")
        print(f"  raw_descends={int(raw_ok)}")
        print(f"  logs={orbit_logs}")
        print(f"  smallest_constancy_exponent={min_exponent}")
        print(f"  smallest_exponent_is_trivial={int(min_exponent == modulus)}")
        print(f"  tested_power_descents={tested_profiles}")
        print(f"  orbit_product={orbit_product}")
        print(f"  orbit_product_nonzero={int(orbit_product != 0)}")

    print()
    nontrivial_orbit_count = sum(1 for orbit in orbits if len(orbit) > 1)
    print(f"raw_descended_orbits={raw_descended}/{len(orbits)}")
    print(
        "raw_descended_nontrivial_orbits="
        f"{raw_descended_nontrivial}/{nontrivial_orbit_count}"
    )
    print(
        "tested_small_power_descended_orbits="
        f"{small_power_descended}/{len(orbits)}"
    )
    print(
        "tested_small_power_descended_nontrivial_orbits="
        f"{small_power_descended_nontrivial}/{nontrivial_orbit_count}"
    )
    print(f"orbit_product_nonzero_count={orbit_product_nonzero}/{len(orbits)}")
    print(f"informative_min_exponents={informative_exponents}")
    print("interpretation")
    print("  raw_or_small_power_descent_would_support_individual_plucker_kummer_payload=1")
    print("  only_trivial_exponents_mean_orbit_products_are_the_safe_payload=1")
    print("  orbit_product_nonzero_is_the_existing_centered_resultant_factor_surface=1")
    print("conclusion=reported_centered_marginal_plucker_kummer_descent_audit")


if __name__ == "__main__":
    main()
