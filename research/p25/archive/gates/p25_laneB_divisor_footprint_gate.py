#!/usr/bin/env python3
"""Divisor footprint gate for the p25 Lane B local pullback.

The local pullback tells us how to read the working Jacobi-carry model from
the actual p25 local sources.  This gate profiles the resulting divisor as a
finite packet:

* total degree and row/column marginals;
* support and value distribution;
* Fourier support over C_3 x C_c;
* whether the packet is separable as A(r)+B(c), or genuinely coupled.

The raw Jacobi-carry packet is expected to have a scalar/trivial character
component.  That component is not a failure: it is the global normalization or
polar part that an arithmetic embedding still has to supply.  The useful test
is that the non-scalar footprint has no pure right-axis character and remains a
genuine 151 x 677-style coupling.

The first target is exhaustive for C_3 x C_13.  C_3 x C_53 is sampled by
representative carries, because the structural formulas are the same but the
rows are larger.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_literal_jacobi_packet_model import (
    admissible_pairs,
    carry_packet,
    representative_pairs,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class FootprintCase:
    name: str
    c_axis: int
    exhaustive: bool


CASES = (
    FootprintCase("tiny_C3xC13", 13, True),
    FootprintCase("prime_axis_C3xC53", 53, False),
)


def factor_distinct(n: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.add(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors.add(n)
    return factors


def primitive_root(modulus: int) -> int:
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // p, modulus) != 1 for p in factor_distinct(modulus - 1)):
            return candidate
    raise RuntimeError("no primitive root")


def packet_matrix(packet: list[int], c_axis: int) -> list[list[int]]:
    return [packet[r * c_axis : (r + 1) * c_axis] for r in range(RIGHT_DEGREE)]


def row_sums(matrix: list[list[int]], modulus: int) -> list[int]:
    return [sum(row) % modulus for row in matrix]


def column_sums(matrix: list[list[int]], modulus: int) -> list[int]:
    return [
        sum(matrix[r][c] for r in range(RIGHT_DEGREE)) % modulus
        for c in range(len(matrix[0]))
    ]


def value_histogram(packet: list[int], modulus: int) -> dict[int, int]:
    hist: dict[int, int] = {}
    for value in packet:
        value %= modulus
        hist[value] = hist.get(value, 0) + 1
    return dict(sorted(hist.items()))


def remove_scalar_component(packet: list[int], modulus: int) -> tuple[list[int], int]:
    mean = sum(packet) * pow(len(packet), -1, modulus) % modulus
    return [(value - mean) % modulus for value in packet], mean


def separable_as_row_plus_column(matrix: list[list[int]], modulus: int) -> bool:
    c_axis = len(matrix[0])
    for r in range(RIGHT_DEGREE):
        for c in range(c_axis):
            if (
                matrix[r][c]
                - matrix[r][0]
                - matrix[0][c]
                + matrix[0][0]
            ) % modulus:
                return False
    return True


def finite_difference_rank(matrix: list[list[int]], modulus: int) -> int:
    """Rank of the mixed second-difference rows over the prime field."""
    c_axis = len(matrix[0])
    rows: list[list[int]] = []
    for r in range(1, RIGHT_DEGREE):
        rows.append(
            [
                (
                    matrix[r][c]
                    - matrix[r][0]
                    - matrix[0][c]
                    + matrix[0][0]
                )
                % modulus
                for c in range(1, c_axis)
            ]
        )
    return rank_mod(rows, modulus)


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    mat = [row[:] for row in matrix if any(value % modulus for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % modulus, -1, modulus)
        mat[rank] = [(value * inv) % modulus for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % modulus
            if factor:
                mat[row] = [
                    (value - factor * pivot_value) % modulus
                    for value, pivot_value in zip(mat[row], mat[rank])
                ]
        rank += 1
    return rank


def dft(packet: list[int], c_axis: int, modulus: int) -> list[int]:
    root = primitive_root(modulus)
    zeta_r = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zeta_c = pow(root, (modulus - 1) // c_axis, modulus)
    out: list[int] = []
    for a in range(RIGHT_DEGREE):
        for b in range(c_axis):
            total = 0
            for r in range(RIGHT_DEGREE):
                for c in range(c_axis):
                    total += (
                        packet[r * c_axis + c]
                        * pow(zeta_r, a * r, modulus)
                        * pow(zeta_c, b * c, modulus)
                    )
            out.append(total % modulus)
    return out


def fourier_support_profile(packet: list[int], c_axis: int, modulus: int) -> tuple[int, int, int, int]:
    coeffs = dft(packet, c_axis, modulus)
    nonzero = 0
    right_nontrivial_c_zero = 0
    right_zero_c_nonzero = 0
    mixed = 0
    for a in range(RIGHT_DEGREE):
        for b in range(c_axis):
            value = coeffs[a * c_axis + b]
            if not value:
                continue
            nonzero += 1
            if a != 0 and b == 0:
                right_nontrivial_c_zero += 1
            elif a == 0 and b != 0:
                right_zero_c_nonzero += 1
            elif a != 0 and b != 0:
                mixed += 1
    return nonzero, right_nontrivial_c_zero, right_zero_c_nonzero, mixed


def audit_packet(
    c_axis: int,
    modulus: int,
    u_value: int,
    v_value: int,
    *,
    scalar_normalize: bool = False,
) -> dict[str, object]:
    packet = carry_packet(c_axis, u_value, v_value, modulus)
    scalar_component = 0
    if scalar_normalize:
        packet, scalar_component = remove_scalar_component(packet, modulus)
    matrix = packet_matrix(packet, c_axis)
    hist = value_histogram(packet, modulus)
    support = sum(1 for value in packet if value % modulus)
    rows = row_sums(matrix, modulus)
    columns = column_sums(matrix, modulus)
    nonzero_columns = sum(1 for value in columns if value)
    fourier = fourier_support_profile(packet, c_axis, modulus)
    return {
        "u": u_value,
        "v": v_value,
        "scalar_component": scalar_component,
        "degree": sum(packet) % modulus,
        "integer_degree": sum(value if value <= modulus // 2 else value - modulus for value in packet),
        "support": support,
        "hist": hist,
        "row_sums": rows,
        "column_nonzero": nonzero_columns,
        "column_sum_set_size": len(set(columns)),
        "separable": int(separable_as_row_plus_column(matrix, modulus)),
        "mixed_difference_rank": finite_difference_rank(matrix, modulus),
        "fourier_nonzero": fourier[0],
        "fourier_right_nontrivial_c_zero": fourier[1],
        "fourier_right_zero_c_nonzero": fourier[2],
        "fourier_mixed": fourier[3],
    }


def audit_case(case: FootprintCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = admissible_pairs(case.c_axis) if case.exhaustive else representative_pairs(case.c_axis)
    raw_profiles = [audit_packet(case.c_axis, modulus, u, v) for u, v in pairs]
    norm_profiles = [
        audit_packet(case.c_axis, modulus, u, v, scalar_normalize=True)
        for u, v in pairs
    ]
    canonical_raw = audit_packet(case.c_axis, modulus, RIGHT_DEGREE, 1)
    canonical_norm = audit_packet(
        case.c_axis, modulus, RIGHT_DEGREE, 1, scalar_normalize=True
    )
    raw_degree_nonzero = all(profile["degree"] != 0 for profile in raw_profiles)
    raw_row_sums_equal = all(len(set(profile["row_sums"])) == 1 for profile in raw_profiles)
    raw_no_forbidden = all(profile["fourier_right_nontrivial_c_zero"] == 0 for profile in raw_profiles)
    raw_coupled = all(profile["separable"] == 0 for profile in raw_profiles)
    raw_mixed_rank_positive = all(profile["mixed_difference_rank"] > 0 for profile in raw_profiles)
    norm_degree_zero = all(profile["degree"] == 0 for profile in norm_profiles)
    norm_row_sums_zero = all(set(profile["row_sums"]) == {0} for profile in norm_profiles)
    norm_no_forbidden = all(profile["fourier_right_nontrivial_c_zero"] == 0 for profile in norm_profiles)
    norm_coupled = all(profile["separable"] == 0 for profile in norm_profiles)
    norm_mixed_rank_positive = all(profile["mixed_difference_rank"] > 0 for profile in norm_profiles)
    ok = (
        raw_degree_nonzero
        and raw_row_sums_equal
        and raw_no_forbidden
        and raw_coupled
        and raw_mixed_rank_positive
        and norm_degree_zero
        and norm_row_sums_zero
        and norm_no_forbidden
        and norm_coupled
        and norm_mixed_rank_positive
    )
    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"pairs_checked={len(pairs)} exhaustive={int(case.exhaustive)} "
            f"raw_degree_nonzero={sum(int(p['degree'] != 0) for p in raw_profiles)}/{len(raw_profiles)} "
            f"raw_equal_row_sums={sum(int(len(set(p['row_sums'])) == 1) for p in raw_profiles)}/{len(raw_profiles)} "
            f"raw_no_forbidden_fourier={sum(int(p['fourier_right_nontrivial_c_zero'] == 0) for p in raw_profiles)}/{len(raw_profiles)} "
            f"raw_nonseparable={sum(int(p['separable'] == 0) for p in raw_profiles)}/{len(raw_profiles)} "
            f"raw_mixed_rank_positive={sum(int(p['mixed_difference_rank'] > 0) for p in raw_profiles)}/{len(raw_profiles)} "
            f"norm_degree_zero={sum(int(p['degree'] == 0) for p in norm_profiles)}/{len(norm_profiles)} "
            f"norm_zero_row_sums={sum(int(set(p['row_sums']) == {0}) for p in norm_profiles)}/{len(norm_profiles)} "
            f"norm_nonseparable={sum(int(p['separable'] == 0) for p in norm_profiles)}/{len(norm_profiles)} "
            f"norm_mixed_rank_positive={sum(int(p['mixed_difference_rank'] > 0) for p in norm_profiles)}/{len(norm_profiles)} "
            f"ok={int(ok)}"
        ),
        f"  canonical_raw_profile={canonical_raw}",
        f"  canonical_scalar_normalized_profile={canonical_norm}",
    ]
    return lines, ok


def main() -> int:
    print("p25 Lane B divisor footprint gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"divisor_footprint_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  raw_carry_divisors_have_a_nonzero_scalar_component=1")
    print("  scalar_normalization_makes_degree_and_row_marginals_zero=1")
    print("  normalized_divisors_kill_pure_right_axis_fourier_slots=1")
    print("  normalized_divisors_remain_genuinely_coupled_not_one_axis_sums=1")
    print("  embedding_object_must_supply_global_normalization_plus_coupled_151x677_local_part=1")
    print("conclusion=reported_p25_laneB_divisor_footprint_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
