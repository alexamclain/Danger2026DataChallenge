#!/usr/bin/env python3
"""Diamond-conjugacy gate for p25 Lane B right eigenvectors.

The C-axis Fourier payload gate says that both right-character eigenvectors
carry every nontrivial C-character.  This gate checks whether those two vectors
are independent arbitrary payloads, or whether the packet imposes a sharper
diamond symmetry.

For every admissible prime-axis packet, and representative C_169 packets:

    E_2 = - < -1 > E_1

where <-1> is inversion on the C-axis.  The degenerate line u + 2v == 0 mod c
is exactly the anti-invariant case E_1 = -<-1>E_1, hence E_1 = E_2 and the
right-character module drops to rank 1.

Producer-facing consequence: a candidate only has to supply one full C-axis
right-character vector, but its prescribed negative-inversion conjugate must be
independent.  If the vector is anti-invariant, it lands on the bad line.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import rank_mod
from p25_laneB_literal_jacobi_packet_model import (
    admissible_pairs,
    representative_pairs,
)
from p25_laneB_mixed_character_module_gate import (
    decompose_packet,
    is_degenerate_line,
)
from p25_laneB_right_eigenbasis_gate import right_eigenvectors
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class DiamondCase:
    name: str
    c_axis: int
    exhaustive: bool


CASES = (
    DiamondCase("tiny_C3xC13", 13, True),
    DiamondCase("prime_axis_C3xC53", 53, True),
    DiamondCase("square_axis_C3xC169", 169, False),
)


def negative_inversion(vector: list[int], modulus: int) -> list[int]:
    c_axis = len(vector)
    return [(-vector[(-index) % c_axis]) % modulus for index in range(c_axis)]


def coordinate_support(vector: list[int], modulus: int) -> int:
    return sum(1 for value in vector if value % modulus)


def audit_case(case: DiamondCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = (
        admissible_pairs(case.c_axis)
        if case.exhaustive
        else representative_pairs(case.c_axis)
    )

    conjugacy_hits = 0
    anti_invariant_hits = 0
    degenerate_count = 0
    degenerate_self_conjugate_hits = 0
    nondegenerate_independent_conjugate_hits = 0
    rank_counts: dict[int, int] = {}
    support_counts: dict[tuple[int, int], int] = {}
    canonical_summary: str | None = None

    for u_value, v_value in pairs:
        _matrix, _pure_c, mixed = decompose_packet(
            case.c_axis, modulus, u_value, v_value
        )
        _eigen_0, eigen_1, eigen_2 = right_eigenvectors(
            mixed, case.c_axis, modulus
        )
        conjugate = negative_inversion(eigen_1, modulus)
        conjugacy = eigen_2 == conjugate
        anti_invariant = eigen_1 == conjugate
        degenerate = is_degenerate_line(case.c_axis, u_value, v_value)
        eigen_rank = rank_mod([eigen_1, eigen_2], modulus)
        support_pair = (
            coordinate_support(eigen_1, modulus),
            coordinate_support(eigen_2, modulus),
        )

        conjugacy_hits += int(conjugacy)
        anti_invariant_hits += int(anti_invariant)
        degenerate_count += int(degenerate)
        degenerate_self_conjugate_hits += int(
            degenerate
            and conjugacy
            and anti_invariant
            and eigen_1 == eigen_2
            and eigen_rank == 1
        )
        nondegenerate_independent_conjugate_hits += int(
            (not degenerate)
            and conjugacy
            and (not anti_invariant)
            and eigen_1 != eigen_2
            and eigen_rank == 2
        )
        rank_counts[eigen_rank] = rank_counts.get(eigen_rank, 0) + 1
        support_counts[support_pair] = support_counts.get(support_pair, 0) + 1

        if u_value == RIGHT_DEGREE and v_value == 1:
            canonical_summary = (
                f"canonical_theta_3_1: eigen_rank={eigen_rank} "
                f"support_pair={support_pair} "
                f"negative_inversion_conjugacy={int(conjugacy)} "
                f"anti_invariant={int(anti_invariant)}"
            )

    pair_count = len(pairs)
    expected_degenerate = 2 * (case.c_axis - 1) if case.exhaustive else degenerate_count
    row_ok = (
        conjugacy_hits == pair_count
        and anti_invariant_hits == degenerate_count
        and degenerate_count == expected_degenerate
        and degenerate_self_conjugate_hits == degenerate_count
        and nondegenerate_independent_conjugate_hits == pair_count - degenerate_count
        and canonical_summary is not None
    )

    degenerate_denominator = degenerate_count if degenerate_count else 1
    nondegenerate_count = pair_count - degenerate_count
    nondegenerate_denominator = nondegenerate_count if nondegenerate_count else 1
    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"pairs_checked={pair_count} exhaustive={int(case.exhaustive)} "
            f"negative_inversion_conjugacy_hits={conjugacy_hits}/{pair_count} "
            f"anti_invariant_hits={anti_invariant_hits}/{pair_count} "
            f"degenerate_line_pairs={degenerate_count} "
            f"expected_degenerate_line_pairs={expected_degenerate} "
            f"degenerate_self_conjugate_hits={degenerate_self_conjugate_hits}/{degenerate_denominator} "
            f"nondegenerate_independent_conjugate_hits={nondegenerate_independent_conjugate_hits}/{nondegenerate_denominator} "
            f"rank_counts={dict(sorted(rank_counts.items()))} "
            f"ok={int(row_ok)}"
        ),
        f"  support_counts={dict(sorted(support_counts.items()))}",
        f"  {canonical_summary}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B diamond-conjugacy gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"diamond_conjugacy_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  second_right_eigenvector_is_negative_C_axis_inversion_of_the_first=1")
    print("  producer_payload_compresses_to_one_C_axis_vector_plus_prescribed_conjugate=1")
    print("  anti_invariant_vectors_are_exactly_the_degenerate_E1_equals_E2_line=1")
    print("  nondegenerate_producer_vector_must_not_be_negative_inversion_anti_invariant=1")
    print("conclusion=reported_p25_laneB_diamond_conjugacy_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
