#!/usr/bin/env python3
"""Actual-CM boundary for the adjacent-trace anchor descent.

This reuses the small actual-CM row from the right-axis covariance boundary:

    D=-6719, q=6863, h=105, m=21=3*7, n=5.

Here rho=q^2 fixes the left component and shifts the right quotient of
(Z/7Z)^* by 2 modulo the order-3 quotient.  The internal relative trace has
two cosets.  On this row the adjacent H-coset trace differences satisfy the
formal covariance and telescope identities, but the single adjacent anchor
does not descend.

Thus the p24 theorem cannot be "actual CM + covariance + telescope" alone.
It must use the special trace-GCD weighted/selected adjacent packet.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary import (
    D,
    INTERNAL_EXPONENT,
    LEFT,
    M,
    N,
    QUOTIENT_ORDER,
    RIGHT,
    RIGHT_GEN,
    RHO_EXPONENT,
    cosets_by_log_residue,
    frobenius_power,
    h_coset_sums,
    internally_traced_profile,
    load_actual_cycle,
    log_table_mod_prime,
    subgroup_generated,
)


def relative_internal_cosets(cycle) -> list[list[int]]:
    internal = subgroup_generated(cycle.n, pow(cycle.q, INTERNAL_EXPONENT, cycle.n))
    cosets: list[list[int]] = []
    seen: set[int] = set()
    for start in range(1, cycle.n):
        if start in seen:
            continue
        coset = sorted((start * value) % cycle.n for value in internal)
        seen.update(coset)
        cosets.append(coset)
    return cosets


def adjacent_differences(values, field):
    return [
        field.sub(values[(index + 1) % len(values)], values[index])
        for index in range(len(values))
    ]


def vector_sum(values, field):
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def main() -> None:
    cycle = load_actual_cycle()
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    rho_left = pow(cycle.q, RHO_EXPONENT, LEFT)
    rho_right = pow(cycle.q, RHO_EXPONENT, RIGHT)
    right_shift = logs[rho_right] % QUOTIENT_ORDER
    right_h_cosets = cosets_by_log_residue(RIGHT, RIGHT_GEN, QUOTIENT_ORDER)
    rel_cosets = relative_internal_cosets(cycle)

    covariance_failures = 0
    telescope_zero = 0
    adjacent_anchor_descended = 0
    adjacent_all_zero = 0
    nonzero_anchor_defects = 0
    rows = []

    for rel_coset in rel_cosets:
        profile = internally_traced_profile(cycle, rel_coset[0])
        h_sums = h_coset_sums(profile, right_h_cosets, cycle.field)
        differences = adjacent_differences(h_sums, cycle.field)
        rows.append(differences)

        for index, value in enumerate(differences):
            expected = differences[(index + right_shift) % QUOTIENT_ORDER]
            actual = frobenius_power(value, cycle.field, RHO_EXPONENT)
            covariance_failures += int(actual != expected)

        telescope_zero += int(vector_sum(differences, cycle.field) == cycle.field.zero)
        adjacent_anchor_descended += int(
            frobenius_power(differences[0], cycle.field, RHO_EXPONENT) == differences[0]
        )
        adjacent_all_zero += int(all(value == cycle.field.zero for value in differences))
        nonzero_anchor_defects += int(differences[0] != cycle.field.zero)

    print("Trace-GCD fixed-frequency actual-CM adjacent-anchor boundary")
    print(f"D={D}")
    print(f"q={cycle.q}")
    print(f"ell={cycle.ell}")
    print(f"h={cycle.h}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"quotient_order={QUOTIENT_ORDER}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_left_mod_left={rho_left}")
    print(f"rho_right_mod_right={rho_right}")
    print(f"rho_right_shift_mod_quotient={right_shift}")
    print(f"relative_internal_cosets={rel_cosets}")
    print(f"right_H_cosets={right_h_cosets}")
    print(f"adjacent_difference_covariance_failures={covariance_failures}")
    print(f"adjacent_difference_telescope_zero={telescope_zero}/{len(rel_cosets)}")
    print(f"adjacent_anchor_descended={adjacent_anchor_descended}/{len(rel_cosets)}")
    print(f"adjacent_anchor_nonzero={nonzero_anchor_defects}/{len(rel_cosets)}")
    print(f"adjacent_differences_all_zero={adjacent_all_zero}/{len(rel_cosets)}")
    print(f"adjacent_difference_rows={rows}")
    print("interpretation")
    print("  covariance_telescope_do_not_force_adjacent_anchor_in_actual_cm=1")
    print("  actual_cm_adjacent_anchor_descent_not_generic=1")
    print("  p24_needs_specific_trace_gcd_adjacent_packet=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_adjacent_anchor_boundary")

    if (cycle.h, cycle.m, cycle.n) != (105, M, N):
        raise SystemExit(1)
    if rho_left != 1 or right_shift == 0:
        raise SystemExit(1)
    if covariance_failures:
        raise SystemExit(1)
    if telescope_zero != len(rel_cosets):
        raise SystemExit(1)
    if adjacent_anchor_descended:
        raise SystemExit(1)
    if adjacent_all_zero:
        raise SystemExit(1)
    if nonzero_anchor_defects != len(rel_cosets):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
