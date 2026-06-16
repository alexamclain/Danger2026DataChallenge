#!/usr/bin/env python3
"""Square-axis digit selector gate for p25 Lane B.

The local graph-residue gate writes the C_169 boundary residual as the
triangular exponent comb

    q = 43*(h+1) + 172*s + 9*t  mod 507.

This gate rewrites the same comb as a digit predicate.  Since 507 = 12*43 - 9
and all residual q-values lie below 507, write

    q = 43*m + r, 0 <= r < 43.

Then the residual classes are exactly:

    1 <= m <= 11,  m mod 4 != 0,
    r in {0, 9, 18},
    r/9 <= (m - 1) mod 4.

Equivalently, after grouping the high digit by h = (m-1) mod 4 and low digit
t = r/9, the selector is the lower-triangular 3 by 3 matrix t <= h.  This is a
compact digit rule, but not a proper-modulus congruence shortcut.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod

from p25_laneB_divisor_footprint_gate import rank_mod
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    triangular_parameters,
)


BASE_DIGIT = 43
ODD_RANK_FIELD = 1_000_003


@dataclass(frozen=True)
class DivisorProjectionProfile:
    modulus: int
    residual_residues: int
    lifted_count: int
    exact: bool


def residual_q_values() -> list[int]:
    return sorted(q_value for *_prefix, q_value in triangular_parameters())


def digit_rule(q_value: int) -> bool:
    m_value, r_value = divmod(q_value, BASE_DIGIT)
    if not (1 <= m_value <= 11):
        return False
    if m_value % 4 == 0:
        return False
    if r_value % 9:
        return False
    t_value = r_value // 9
    h_value = (m_value - 1) % 4
    return 0 <= t_value <= h_value


def digit_rows(q_values: list[int]) -> list[tuple[int, int, int, int, int, int]]:
    rows: list[tuple[int, int, int, int, int, int]] = []
    for q_value in q_values:
        m_value, r_value = divmod(q_value, BASE_DIGIT)
        t_value = r_value // 9
        h_value = (m_value - 1) % 4
        s_value = (m_value - (h_value + 1)) // 4
        rows.append((q_value, m_value, r_value, h_value, s_value, t_value))
    return rows


def triangular_matrix() -> list[list[int]]:
    return [[int(t_value <= h_value) for t_value in range(3)] for h_value in range(3)]


def mixed_second_difference_nonzero(matrix: list[list[int]]) -> bool:
    return any(
        (
            matrix[h][t]
            - matrix[h][0]
            - matrix[0][t]
            + matrix[0][0]
        )
        != 0
        for h in range(1, 3)
        for t in range(1, 3)
    )


def projection_profile(q_values: list[int], modulus: int) -> DivisorProjectionProfile:
    q_set = set(q_values)
    residues = {q_value % modulus for q_value in q_values}
    lifted = {candidate for candidate in range(QUOTIENT_ORDER) if candidate % modulus in residues}
    return DivisorProjectionProfile(
        modulus=modulus,
        residual_residues=len(residues),
        lifted_count=len(lifted),
        exact=lifted == q_set,
    )


def proper_divisors(n_value: int) -> list[int]:
    return [divisor for divisor in range(1, n_value) if n_value % divisor == 0]


def main() -> int:
    print("p25 Lane B square-axis digit selector gate")
    print(f"quotient_order={QUOTIENT_ORDER} base_digit={BASE_DIGIT}")
    q_values = residual_q_values()
    q_set = set(q_values)
    digit_hits = [q_value for q_value in range(QUOTIENT_ORDER) if digit_rule(q_value)]
    digit_rows_list = digit_rows(q_values)
    matrix = triangular_matrix()
    rank_f2 = rank_mod(matrix, 2)
    rank_odd = rank_mod(matrix, ODD_RANK_FIELD)
    mixed_nonzero = mixed_second_difference_nonzero(matrix)
    h_counts = [0, 0, 0]
    s_counts = [0, 0, 0]
    t_counts = [0, 0, 0]
    high_digits: list[int] = []
    low_residues: list[int] = []
    for _q_value, m_value, r_value, h_value, s_value, t_value in digit_rows_list:
        h_counts[h_value] += 1
        s_counts[s_value] += 1
        t_counts[t_value] += 1
        high_digits.append(m_value)
        low_residues.append(r_value)
    projections = [projection_profile(q_values, divisor) for divisor in proper_divisors(QUOTIENT_ORDER)]
    proper_exact_count = sum(int(profile.exact) for profile in projections)
    smallest_lifted = min(profile.lifted_count for profile in projections)
    product_projection_count = prod(len({q_value % modulus for q_value in q_values}) for modulus in (3, 13, 43))

    row_ok = (
        len(q_values) == 18
        and digit_hits == q_values
        and h_counts == [3, 6, 9]
        and s_counts == [6, 6, 6]
        and t_counts == [9, 6, 3]
        and sorted(set(high_digits)) == [1, 2, 3, 5, 6, 7, 9, 10, 11]
        and sorted(set(low_residues)) == [0, 9, 18]
        and matrix == [[1, 0, 0], [1, 1, 0], [1, 1, 1]]
        and rank_f2 == 3
        and rank_odd == 3
        and mixed_nonzero
        and proper_exact_count == 0
        and smallest_lifted == 54
        and product_projection_count == 81
    )
    print(
        f"digit_selector: "
        f"q_count={len(q_values)}/18 "
        f"digit_hits={len(digit_hits)}/18 "
        f"h_counts={h_counts} "
        f"s_counts={s_counts} "
        f"t_counts={t_counts} "
        f"high_digits={sorted(set(high_digits))} "
        f"low_residues={sorted(set(low_residues))} "
        f"triangular_matrix={matrix} "
        f"rank_f2={rank_f2} "
        f"rank_odd={rank_odd} "
        f"mixed_second_difference_nonzero={int(mixed_nonzero)} "
        f"proper_exact_moduli={proper_exact_count} "
        f"best_proper_modulus_lifted_count={smallest_lifted} "
        f"product_projection_count_mod_3_13_43={product_projection_count} "
        f"ok={int(row_ok)}"
    )
    print("digit_rows")
    for q_value, m_value, r_value, h_value, s_value, t_value in digit_rows_list:
        print(
            f"  q={q_value}: m={m_value} r={r_value} h={h_value} s={s_value} t={t_value}"
        )
    print("proper_modulus_projection_profiles")
    for profile in projections:
        print(
            f"  mod {profile.modulus}: "
            f"residual_residues={profile.residual_residues} "
            f"lifted_count={profile.lifted_count} "
            f"exact={int(profile.exact)}"
        )
    print("digit_selector_law")
    print("  q = 43*m + r, 0 <= r < 43")
    print("  1 <= m <= 11 and m mod 4 != 0")
    print("  r = 9*t with 0 <= t <= (m-1) mod 4")
    print(f"square_axis_digit_selector_rows={int(row_ok)}/1")
    print("interpretation")
    print("  triangular_comb_is_a_compact_base43_digit_selector=1")
    print("  selector_has_lower_triangular_h_by_t_coupling_rank_three=1")
    print("  no_proper_modulus_of_507_recovers_the_18_classes=1")
    print("  producer_must_realize_digit_coupling_not_only_modular_projection=1")
    print("conclusion=reported_p25_laneB_square_axis_digit_selector_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
