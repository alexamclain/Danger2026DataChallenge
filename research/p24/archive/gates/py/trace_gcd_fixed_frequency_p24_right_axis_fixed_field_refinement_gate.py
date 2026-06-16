#!/usr/bin/env python3
"""Right-axis fixed-field refinement for the p24 anchor descent target.

The seven-coset covariance/descent gate only needs the anchor H-coset sum to
be fixed by rho=p^780.  It does not need the anchor to descend all the way to
L=F_p(mu_157).

This matters because on the right 211-cyclotomic layer, rho has order 7, so
the rho-fixed right-period subfield has degree 5.  Thus "rho-fixed" is weaker
than "left-only".  The pure H-periods themselves form a covariant seven-tuple
but are not rho-fixed coset-by-coset; they still leak order-7 spectrum.  The
actual CM/Lang theorem must force the anchor of the traced G_chi profile into
the rho-fixed field, not merely invoke the formal cyclotomic H-periods.
"""

from __future__ import annotations

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


P24 = 10**24 + 7
LEFT = 157
RIGHT = 211
RIGHT_GEN = 2
H_STEP = 7
ORDER7 = 7
RHO_EXPONENT = 780
RIGHT_MODEL_Q = 113  # ord_211(113)=35 and 113=1 mod 7.
RIGHT_MODEL_DEGREE = 35
SEED = 20260606


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(q: int) -> int:
    factors = factor_distinct(q - 1)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if rows[row][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, q)
        rows[rank] = [value * inv % q for value in rows[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def log_table_mod_prime(modulus: int, generator: int) -> dict[int, int]:
    logs: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad generator")
    return logs


def h_coset(coset_index: int, logs: dict[int, int]) -> list[int]:
    return [
        value
        for value in range(1, RIGHT)
        if logs[value] % H_STEP == coset_index
    ]


def add_all(field: ExtensionField, values: list[FpE]) -> FpE:
    total = field.zero
    for value in values:
        total = field.add(total, value)
    return total


def automorphism(value: FpE, field: ExtensionField, frobenius_power: int) -> FpE:
    return field.pow(value, field.q**frobenius_power)


def fixed_dimension(field: ExtensionField, frobenius_power: int) -> int:
    columns: list[FpE] = []
    for index in range(field.degree):
        basis = tuple(1 if i == index else 0 for i in range(field.degree))
        columns.append(field.sub(automorphism(basis, field, frobenius_power), basis))
    matrix = [
        [columns[col][row] for col in range(field.degree)]
        for row in range(field.degree)
    ]
    return field.degree - rank_mod(matrix, field.q)


def profile_projection(
    profile: list[FpE],
    zeta7: int,
    character_index: int,
    field: ExtensionField,
) -> FpE:
    total = field.zero
    for coset, value in enumerate(profile):
        weight = pow(zeta7, (-character_index * coset) % ORDER7, field.q)
        total = field.add(total, field.scalar_mul(weight, value))
    return total


def projection_leak_count(profile: list[FpE], zeta7: int, field: ExtensionField) -> int:
    return sum(
        int(profile_projection(profile, zeta7, index, field) != field.zero)
        for index in range(1, ORDER7)
    )


def main() -> None:
    logs = log_table_mod_prime(RIGHT, RIGHT_GEN)
    p_log = logs[P24 % RIGHT]
    rho_right = pow(P24, RHO_EXPONENT, RIGHT)
    rho_log = logs[rho_right]
    rho_shift = rho_log % ORDER7

    q_order = int(sp.n_order(RIGHT_MODEL_Q % RIGHT, RIGHT))
    q_to_rho_power = next(
        exponent
        for exponent in range(q_order)
        if pow(RIGHT_MODEL_Q, exponent, RIGHT) == rho_right
    )
    rho_order_on_right_model = q_order // sp.gcd(q_order, q_to_rho_power)
    right_fixed_degree = fixed_dimension(
        ExtensionField(
            RIGHT_MODEL_Q,
            RIGHT_MODEL_DEGREE,
            find_irreducible_modulus(RIGHT_MODEL_Q, RIGHT_MODEL_DEGREE, SEED),
        ),
        q_to_rho_power,
    )

    field = ExtensionField(
        RIGHT_MODEL_Q,
        RIGHT_MODEL_DEGREE,
        find_irreducible_modulus(RIGHT_MODEL_Q, RIGHT_MODEL_DEGREE, SEED),
    )
    zeta211 = primitive_root_of_order(field, RIGHT, SEED)
    zeta7 = pow(primitive_root(RIGHT_MODEL_Q), (RIGHT_MODEL_Q - 1) // ORDER7, RIGHT_MODEL_Q)

    periods = [
        add_all(field, [field.pow(zeta211, residue) for residue in h_coset(coset, logs)])
        for coset in range(ORDER7)
    ]
    covariance_failures = 0
    for coset, value in enumerate(periods):
        covariance_failures += int(
            automorphism(value, field, q_to_rho_power)
            != periods[(coset + rho_shift) % ORDER7]
        )
    period_equal_cosets = len(set(periods)) == 1
    period_anchor_fixed = automorphism(periods[0], field, q_to_rho_power) == periods[0]
    period_projection_leaks = projection_leak_count(periods, zeta7, field)

    constant_fixed = [field.embed(1)] * ORDER7
    constant_covariance_failures = sum(
        int(
            automorphism(value, field, q_to_rho_power)
            != constant_fixed[(coset + rho_shift) % ORDER7]
        )
        for coset, value in enumerate(constant_fixed)
    )
    constant_projection_leaks = projection_leak_count(constant_fixed, zeta7, field)

    p24_right_fixed_degree = 35 // 7
    p24_left_degree = int(sp.n_order(P24 % LEFT, LEFT))
    p24_rho_fixed_e_degree = p24_left_degree * p24_right_fixed_degree

    print("Trace-GCD fixed-frequency p24 right-axis fixed-field refinement gate")
    print(f"p24={P24}")
    print(f"left={LEFT}")
    print(f"right={RIGHT}")
    print(f"right_primitive_root={RIGHT_GEN}")
    print(f"p24_mod_211={P24 % RIGHT}")
    print(f"p24_log_base2_mod_211={p_log}")
    print(f"rho_exponent={RHO_EXPONENT}")
    print(f"rho_mod_211={rho_right}")
    print(f"rho_log_base2_mod_211={rho_log}")
    print(f"rho_log_mod_order7_quotient={rho_shift}")
    print(f"right_model_q={RIGHT_MODEL_Q}")
    print(f"right_model_ord_211_q={q_order}")
    print(f"right_model_q_frobenius_power_for_rho={q_to_rho_power}")
    print(f"rho_order_on_right_model={rho_order_on_right_model}")
    print(f"right_model_rho_fixed_dimension={right_fixed_degree}")
    print(f"p24_left_degree={p24_left_degree}")
    print(f"p24_right_rho_fixed_degree={p24_right_fixed_degree}")
    print(f"p24_rho_fixed_E_degree={p24_rho_fixed_e_degree}")
    print(f"pure_H_period_covariance_failures={covariance_failures}")
    print(f"pure_H_period_anchor_fixed={int(period_anchor_fixed)}")
    print(f"pure_H_period_equal_cosets={int(period_equal_cosets)}")
    print(f"pure_H_period_nontrivial_projection_leaks={period_projection_leaks}/6")
    print(f"constant_fixed_profile_covariance_failures={constant_covariance_failures}")
    print(f"constant_fixed_profile_nontrivial_projection_leaks={constant_projection_leaks}/6")
    print("interpretation")
    print("  rho_fixed_field_is_larger_than_left_mu157_field=1")
    print("  anchor_descent_to_rho_fixed_field_is_the_exact_finite_need=1")
    print("  descent_all_the_way_to_left_field_is_sufficient_but_stronger=1")
    print("  pure_right_H_periods_are_covariant_but_not_anchor_descended=1")
    print("  traced_G_chi_must_cancel_the_nonfixed_right_period_part=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_right_axis_fixed_field_refinement_gate")

    if (p_log, rho_log, rho_shift) != (198, 90, 6):
        raise SystemExit(1)
    if (q_order, q_to_rho_power, rho_order_on_right_model) != (35, 15, 7):
        raise SystemExit(1)
    if right_fixed_degree != 5:
        raise SystemExit(1)
    if (p24_left_degree, p24_right_fixed_degree, p24_rho_fixed_e_degree) != (156, 5, 780):
        raise SystemExit(1)
    if covariance_failures:
        raise SystemExit(1)
    if period_anchor_fixed or period_equal_cosets or period_projection_leaks != 6:
        raise SystemExit(1)
    if constant_covariance_failures or constant_projection_leaks:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
