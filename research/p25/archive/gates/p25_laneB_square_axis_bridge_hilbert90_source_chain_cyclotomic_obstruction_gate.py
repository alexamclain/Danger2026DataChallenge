#!/usr/bin/env python3
"""Cyclotomic-unit obstruction for p25 Hilbert-90 source chains.

The primitive-word gate gives the positive target

    C = -(1 + z + z^-121),     (1 - z^122) C = F.

This gate checks the simplest cyclotomic-unit shortcuts for that three-term
word.  It is not an arithmetic progression / length-three geometric segment,
not a signed product of two first-order cyclotomic edges, and it is not itself
the boundary of any edge quotient in C_507.  The first boundary F does have
sparse edge quotients, but the minimum support is three and occurs only for
the recorded +/-122 primitive steps.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd

from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (
    primitive_word_profile,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


N = QUOTIENT_ORDER
MODULUS = 2029
Poly = dict[int, int]
Items = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class EdgeAntiderivativeProfile:
    possible_direction_count: int
    minimal_support: int | None
    best_directions: tuple[int, ...]
    best_prefix: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ChainCyclotomicRow:
    orientation_mask: int
    boundary_step_d: int
    chain_word: Items
    first_boundary_word: Items
    chain_is_arithmetic_progression: bool
    chain_edge_antiderivative: EdgeAntiderivativeProfile
    first_boundary_edge_antiderivative: EdgeAntiderivativeProfile


@dataclass(frozen=True)
class ChainCyclotomicProfile:
    row_count: int
    rows: tuple[ChainCyclotomicRow, ...]
    two_edge_product_chain_matches: int
    two_edge_product_first_boundary_matches: int
    all_chains_are_not_arithmetic_progressions: bool
    all_chains_have_no_edge_antiderivative: bool
    all_first_boundaries_have_unique_minimal_edge_pair: bool
    all_two_edge_product_shortcuts_absent: bool


def support(poly: Poly) -> tuple[int, ...]:
    return tuple(sorted(poly))


def is_arithmetic_progression(poly: Poly) -> bool:
    points = set(poly)
    if len(points) != 3 or len(set(poly.values())) != 1:
        return False
    for base in points:
        for step in range(1, N):
            if {base, (base + step) % N, (base + 2 * step) % N} == points:
                return True
    return False


def cycle_values(direction: int) -> tuple[tuple[int, ...], ...]:
    cycles: list[tuple[int, ...]] = []
    for start in range(gcd(direction, N)):
        cycle: list[int] = []
        value = start
        while True:
            cycle.append(value)
            value = (value + direction) % N
            if value == start:
                break
        cycles.append(tuple(cycle))
    return tuple(cycles)


def antiderivative_support(target: Poly, direction: int) -> int | None:
    total_support = 0
    for cycle in cycle_values(direction):
        if sum(target.get(value, 0) for value in cycle) % MODULUS:
            return None
        prefix_values: list[int] = []
        running = 0
        for index, value in enumerate(cycle):
            if index:
                running = (running + target.get(value, 0)) % MODULUS
            prefix_values.append(running)
        total_support += len(cycle) - Counter(prefix_values).most_common(1)[0][1]
    return total_support


def edge_antiderivative_profile(target: Poly) -> EdgeAntiderivativeProfile:
    possible = tuple(
        (support_value, direction)
        for direction in range(1, N)
        for support_value in (antiderivative_support(target, direction),)
        if support_value is not None
    )
    if not possible:
        return EdgeAntiderivativeProfile(0, None, (), ())
    possible_sorted = tuple(sorted(possible))
    minimum = possible_sorted[0][0]
    best = tuple(direction for support_value, direction in possible_sorted if support_value == minimum)
    return EdgeAntiderivativeProfile(
        possible_direction_count=len(possible_sorted),
        minimal_support=minimum,
        best_directions=best,
        best_prefix=possible_sorted[:10],
    )


def translate_shapes(poly: Poly) -> set[Items]:
    return {
        tuple(sorted(((point - base) % N, coefficient) for point, coefficient in poly.items()))
        for base in poly
    }


def signed_translate_shapes(poly: Poly) -> set[Items]:
    out: set[Items] = set()
    for sign in (-1, 1):
        out |= translate_shapes({point: sign * coefficient for point, coefficient in poly.items()})
    return out


def multiply_two_edges(first_step: int, first_sign: int, second_step: int, second_sign: int) -> Poly:
    out: Poly = {}
    for left_point, left_coeff in ((0, 1), (first_step, first_sign)):
        for right_point, right_coeff in ((0, 1), (second_step, second_sign)):
            point = (left_point + right_point) % N
            out[point] = out.get(point, 0) + left_coeff * right_coeff
            if out[point] == 0:
                del out[point]
    return dict(sorted(out.items()))


def two_edge_product_match_counts(chain_targets: tuple[Poly, ...], first_targets: tuple[Poly, ...]) -> tuple[int, int]:
    chain_shapes = set().union(*(signed_translate_shapes(target) for target in chain_targets))
    first_shapes = set().union(*(signed_translate_shapes(target) for target in first_targets))
    chain_matches = 0
    first_matches = 0
    for first_step in range(1, N):
        for second_step in range(1, N):
            for first_sign in (-1, 1):
                for second_sign in (-1, 1):
                    product = multiply_two_edges(first_step, first_sign, second_step, second_sign)
                    shapes = translate_shapes(product)
                    chain_matches += int(bool(shapes & chain_shapes))
                    first_matches += int(bool(shapes & first_shapes))
    return chain_matches, first_matches


def cyclotomic_profile() -> ChainCyclotomicProfile:
    primitive = primitive_word_profile()
    rows: list[ChainCyclotomicRow] = []
    chain_targets: list[Poly] = []
    first_targets: list[Poly] = []
    for primitive_row in primitive.rows:
        chain = dict(primitive_row.chain_word)
        first = dict(primitive_row.first_boundary_word)
        chain_targets.append(chain)
        first_targets.append(first)
        rows.append(
            ChainCyclotomicRow(
                orientation_mask=primitive_row.orientation_mask,
                boundary_step_d=primitive_row.boundary_step_d,
                chain_word=primitive_row.chain_word,
                first_boundary_word=primitive_row.first_boundary_word,
                chain_is_arithmetic_progression=is_arithmetic_progression(chain),
                chain_edge_antiderivative=edge_antiderivative_profile(chain),
                first_boundary_edge_antiderivative=edge_antiderivative_profile(first),
            )
        )
    chain_product_matches, first_product_matches = two_edge_product_match_counts(
        tuple(chain_targets),
        tuple(first_targets),
    )
    return ChainCyclotomicProfile(
        row_count=len(rows),
        rows=tuple(rows),
        two_edge_product_chain_matches=chain_product_matches,
        two_edge_product_first_boundary_matches=first_product_matches,
        all_chains_are_not_arithmetic_progressions=all(not row.chain_is_arithmetic_progression for row in rows),
        all_chains_have_no_edge_antiderivative=all(
            row.chain_edge_antiderivative.possible_direction_count == 0 for row in rows
        ),
        all_first_boundaries_have_unique_minimal_edge_pair=all(
            row.first_boundary_edge_antiderivative.minimal_support == 3
            and row.first_boundary_edge_antiderivative.best_directions == (122, 385)
            for row in rows
        ),
        all_two_edge_product_shortcuts_absent=chain_product_matches == 0 and first_product_matches == 0,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain cyclotomic-obstruction gate")
    profile = cyclotomic_profile()
    expected_edge_profile = EdgeAntiderivativeProfile(
        possible_direction_count=468,
        minimal_support=3,
        best_directions=(122, 385),
        best_prefix=((3, 122), (3, 385), (6, 61), (6, 446), (12, 223), (12, 284), (14, 81), (14, 426), (15, 77), (15, 430)),
    )
    row_ok = (
        profile.row_count == 4
        and profile.two_edge_product_chain_matches == 0
        and profile.two_edge_product_first_boundary_matches == 0
        and profile.all_chains_are_not_arithmetic_progressions
        and profile.all_chains_have_no_edge_antiderivative
        and profile.all_first_boundaries_have_unique_minimal_edge_pair
        and profile.all_two_edge_product_shortcuts_absent
        and all(row.chain_edge_antiderivative == EdgeAntiderivativeProfile(0, None, (), ()) for row in profile.rows)
        and all(row.first_boundary_edge_antiderivative == expected_edge_profile for row in profile.rows)
    )

    print(
        "cyclotomic_obstruction_summary: "
        f"row_count={profile.row_count} "
        f"two_edge_chain_matches={profile.two_edge_product_chain_matches} "
        f"two_edge_first_boundary_matches={profile.two_edge_product_first_boundary_matches} "
        f"all_chains_not_AP={int(profile.all_chains_are_not_arithmetic_progressions)} "
        f"all_chains_have_no_edge_antiderivative={int(profile.all_chains_have_no_edge_antiderivative)} "
        f"first_boundary_minimal_edge_pair={int(profile.all_first_boundaries_have_unique_minimal_edge_pair)}"
    )
    print("cyclotomic_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("interpretation")
    print("  active_three_term_chain_is_not_a_length_three_geometric_or_AP_segment=1")
    print("  active_three_term_chain_is_not_a_signed_product_of_two_cyclotomic_edges=1")
    print("  four_point_Hilbert90_potential_is_not_a_signed_product_of_two_cyclotomic_edges=1")
    print("  active_chain_has_no_edge_antiderivative_in_C507=1")
    print("  first_boundary_has_minimal_edge_antiderivatives_only_at_plusminus_122_with_support_three=1")
    print("  producer_must_supply_the_three_term_chain_not_only_a_basic_edge_or_two_edge_unit=1")
    print(f"square_axis_bridge_hilbert90_source_chain_cyclotomic_obstruction_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_cyclotomic_obstruction_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
