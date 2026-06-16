#!/usr/bin/env python3
"""Actual-CM boundary for the left-paired H-coboundary hope.

The p24 order-7 target is a paired profile, not a raw right-resolvent
profile:

    G_s = <A_1, B_s>.

A tempting repair of the right-axis covariance boundary is that inserting a
nontrivial left character might kill the H-trace leakage.  This tests that
hope on the same pinned actual-CM row as the covariance boundary,

    D = -6719, q = 6863, h = 105, m = 21 = 3 * 7, n = 5.

Here rho=Frob_q^2 fixes the left component and shifts the right quotient.
For every left frequency u in {0,1,2}, every relative internal coset, and
every nontrivial right quotient character, the Gauss-normalized projection is
rho-fixed but nonzero.  Thus left pairing by itself does not supply the
paired H-potential; the missing theorem must use the specific trace-GCD
weighted product/section structure.
"""

from __future__ import annotations

from trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary import (
    INTERNAL_EXPONENT,
    LEFT,
    QUOTIENT_ORDER,
    RHO_EXPONENT,
    RIGHT,
    RIGHT_GEN,
    cosets_by_log_residue,
    frobenius_power,
    h_coset_sums,
    load_actual_cycle,
    log_table_mod_prime,
    quotient_projection,
    right_gauss_sum,
    subgroup_generated,
)


def additive_resolvent(cycle, left_frequency: int, right_frequency: int, rel_frequency: int):
    field = cycle.field
    total = field.zero
    for index, j_value in enumerate(cycle.cycle):
        left = index % LEFT
        right = index % RIGHT
        rel = index // cycle.m
        weight = field.mul(
            field.pow(cycle.zeta_quotient, (left_frequency * left) % LEFT),
            field.pow(cycle.zeta_right, (right_frequency * right) % RIGHT),
        )
        weight = field.mul(
            weight,
            field.pow(cycle.zeta_rel, (rel_frequency * rel) % cycle.n),
        )
        total = field.add(total, field.mul(weight, field.embed(j_value)))
    return total


def internally_traced_left_profile(cycle, left_frequency: int, rel_coset_rep: int):
    field = cycle.field
    internal = subgroup_generated(cycle.n, pow(cycle.q, INTERNAL_EXPONENT, cycle.n))
    profile = [field.zero for _ in range(RIGHT)]
    for right_frequency in range(1, RIGHT):
        total = field.zero
        for rel_multiplier in internal:
            total = field.add(
                total,
                additive_resolvent(
                    cycle,
                    left_frequency,
                    right_frequency,
                    (rel_coset_rep * rel_multiplier) % cycle.n,
                ),
            )
        profile[right_frequency] = total
    return profile


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


def main() -> None:
    cycle = load_actual_cycle()
    field = cycle.field
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    h_cosets = cosets_by_log_residue(RIGHT, RIGHT_GEN, QUOTIENT_ORDER)
    rel_cosets = relative_internal_cosets(cycle)
    rho_right = pow(cycle.q, RHO_EXPONENT, RIGHT)

    covariance_failures_by_left: list[int] = []
    equal_h_coset_sums_by_left: list[int] = []
    anchor_descended_by_left: list[int] = []
    nonzero_normalized_by_left: list[int] = []
    fixed_normalized_by_left: list[int] = []
    checked_projections_by_left: list[int] = []

    for left_frequency in range(LEFT):
        covariance_failures = 0
        equal_h_coset_sums = 0
        anchor_descended = 0
        nonzero_normalized = 0
        fixed_normalized = 0
        checked_projections = 0

        for rel_coset in rel_cosets:
            profile = internally_traced_left_profile(cycle, left_frequency, rel_coset[0])
            for right_frequency in range(1, RIGHT):
                actual = frobenius_power(profile[right_frequency], field, RHO_EXPONENT)
                expected = profile[(rho_right * right_frequency) % RIGHT]
                covariance_failures += int(actual != expected)

            sums = h_coset_sums(profile, h_cosets, field)
            equal_h_coset_sums += int(len(set(sums)) == 1)
            anchor_descended += int(
                frobenius_power(sums[0], field, RHO_EXPONENT) == sums[0]
            )

            for character_index in range(1, QUOTIENT_ORDER):
                tau = right_gauss_sum(cycle, logs, character_index)
                projection = quotient_projection(
                    profile,
                    logs,
                    cycle.zeta_quotient,
                    field,
                    character_index,
                )
                normalized = field.div(projection, tau)
                nonzero_normalized += int(normalized != field.zero)
                fixed_normalized += int(
                    frobenius_power(normalized, field, RHO_EXPONENT) == normalized
                )
                checked_projections += 1

        covariance_failures_by_left.append(covariance_failures)
        equal_h_coset_sums_by_left.append(equal_h_coset_sums)
        anchor_descended_by_left.append(anchor_descended)
        nonzero_normalized_by_left.append(nonzero_normalized)
        fixed_normalized_by_left.append(fixed_normalized)
        checked_projections_by_left.append(checked_projections)

    nontrivial_left_profiles = (LEFT - 1) * len(rel_cosets)
    nontrivial_left_projection_count = sum(checked_projections_by_left[1:])
    nontrivial_left_equal = sum(equal_h_coset_sums_by_left[1:])
    nontrivial_left_descended = sum(anchor_descended_by_left[1:])
    nontrivial_left_nonzero = sum(nonzero_normalized_by_left[1:])
    nontrivial_left_fixed = sum(fixed_normalized_by_left[1:])

    print("Trace-GCD fixed-frequency actual-CM left-paired H-coboundary boundary")
    print(f"D={cycle.D}")
    print(f"q={cycle.q}")
    print(f"ell={cycle.ell}")
    print(f"h={cycle.h}")
    print(f"m={cycle.m}")
    print(f"n={cycle.n}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"quotient_order={QUOTIENT_ORDER}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_left_mod_left={pow(cycle.q, RHO_EXPONENT, LEFT)}")
    print(f"rho_right_mod_right={rho_right}")
    print(f"rho_right_log_mod_quotient={logs[rho_right] % QUOTIENT_ORDER}")
    print(f"relative_internal_cosets={rel_cosets}")
    print(f"covariance_failures_by_left_frequency={covariance_failures_by_left}")
    print(f"equal_H_coset_sums_by_left_frequency={equal_h_coset_sums_by_left}")
    print(f"anchor_descended_by_left_frequency={anchor_descended_by_left}")
    print(
        "gauss_normalized_nonzero_by_left_frequency="
        f"{nonzero_normalized_by_left}/{checked_projections_by_left}"
    )
    print(
        "gauss_normalized_fixed_by_left_frequency="
        f"{fixed_normalized_by_left}/{checked_projections_by_left}"
    )
    print(
        "nontrivial_left_equal_H_coset_sums="
        f"{nontrivial_left_equal}/{nontrivial_left_profiles}"
    )
    print(
        "nontrivial_left_anchor_descended="
        f"{nontrivial_left_descended}/{nontrivial_left_profiles}"
    )
    print(
        "nontrivial_left_gauss_normalized_nonzero="
        f"{nontrivial_left_nonzero}/{nontrivial_left_projection_count}"
    )
    print(
        "nontrivial_left_gauss_normalized_fixed="
        f"{nontrivial_left_fixed}/{nontrivial_left_projection_count}"
    )
    print("interpretation")
    print("  actual_cm_left_pairing_preserves_covariance=1")
    print("  nontrivial_left_pairing_does_not_force_H_coboundary=1")
    print("  paired_profile_theorem_needs_trace_gcd_weighted_product_structure=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_actual_cm_left_paired_h_boundary")

    if (cycle.h, cycle.m, cycle.n) != (105, 21, 5):
        raise SystemExit(1)
    if pow(cycle.q, RHO_EXPONENT, LEFT) != 1:
        raise SystemExit(1)
    if any(covariance_failures_by_left):
        raise SystemExit(1)
    if nontrivial_left_equal or nontrivial_left_descended:
        raise SystemExit(1)
    if nontrivial_left_nonzero != nontrivial_left_projection_count:
        raise SystemExit(1)
    if nontrivial_left_fixed != nontrivial_left_projection_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
