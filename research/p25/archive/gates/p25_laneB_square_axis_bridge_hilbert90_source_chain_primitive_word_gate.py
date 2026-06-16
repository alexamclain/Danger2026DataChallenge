#!/usr/bin/env python3
"""Primitive-coordinate word for p25 Hilbert-90 source chains.

The bridge already has a primitive raw D-coordinate normal form.  This gate
records the corresponding quotient C_507 word for the newly pinned
support-three Hilbert-90 source chains.

In the primitive D coordinate modulo the C_25 trace kernel, the canonical
source chain is

    C = -(1 + z + z^-121).

The rigid first boundary is the edge 1 - z^122.  The product has one internal
cancellation and gives a four-point Hilbert-90 potential; applying the
inversion boundary gives exactly the six-point bridge word.  Scanning all
nonzero first-boundary steps shows that the recorded step is unique for each
active chain.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate import (
    boundary,
    inversion_boundary,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_coefficient_rigidity_gate import (
    coefficient_rigidity_profile,
)
from p25_laneB_square_axis_bridge_primitive_d_coordinate_gate import solve_d_exponent
from p25_laneB_square_axis_bridge_raw_source_character_gate import C_ORDER
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Poly = dict[int, int]
Items = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class PrimitiveWordRow:
    orientation_mask: int
    boundary_direction_q: int
    boundary_step_d: int
    q_values: tuple[int, ...]
    chain_word: Items
    first_boundary_word: Items
    bridge_word: Items
    first_boundary_support_distribution: tuple[tuple[int, int], ...]
    bridge_recovery_steps: tuple[int, ...]
    unique_bridge_recovery_step: bool


@dataclass(frozen=True)
class PrimitiveWordProfile:
    bridge_word: Items
    canonical_chain_word: Items
    canonical_boundary_step: int
    canonical_first_boundary_word: Items
    row_count: int
    rows: tuple[PrimitiveWordRow, ...]
    all_rows_recover_bridge: bool
    all_rows_have_unique_recovery_step: bool
    all_rows_have_sparse_boundary_distribution: bool


def d_residue_from_q(q_value: int) -> int:
    """Map a quotient class into the primitive D-coordinate quotient C_507."""

    # Use the same-layer raw representative.  Adding a C_25 kernel layer changes
    # the raw D exponent by a multiple of 507, so the residue is well-defined.
    return solve_d_exponent((q_value % 75, q_value % C_ORDER)) % QUOTIENT_ORDER


def to_d_word(poly: Poly) -> Poly:
    out: Poly = {}
    for q_value, coefficient in poly.items():
        residue = d_residue_from_q(q_value)
        out[residue] = out.get(residue, 0) + coefficient
        if out[residue] == 0:
            del out[residue]
    return dict(sorted(out.items()))


def as_items(poly: Poly) -> Items:
    return tuple(sorted(poly.items()))


def d_boundary(poly: Poly, step: int) -> Poly:
    out = dict(poly)
    for residue, coefficient in poly.items():
        shifted = (residue + step) % QUOTIENT_ORDER
        out[shifted] = out.get(shifted, 0) - coefficient
        if out[shifted] == 0:
            del out[shifted]
    return dict(sorted(out.items()))


def d_inversion_boundary(poly: Poly) -> Poly:
    out: Poly = {}
    for residue in range(QUOTIENT_ORDER):
        value = poly.get(residue, 0) - poly.get((-residue) % QUOTIENT_ORDER, 0)
        if value:
            out[residue] = value
    return dict(sorted(out.items()))


def recovery_steps(chain_word: Poly, bridge_word: Poly) -> tuple[int, ...]:
    hits: list[int] = []
    for step in range(1, QUOTIENT_ORDER):
        if d_inversion_boundary(d_boundary(chain_word, step)) == bridge_word:
            hits.append(step)
    return tuple(hits)


def support_distribution(chain_word: Poly) -> tuple[tuple[int, int], ...]:
    distribution = Counter(
        len(d_boundary(chain_word, step))
        for step in range(1, QUOTIENT_ORDER)
    )
    return tuple(sorted(distribution.items()))


def primitive_word_row(row) -> PrimitiveWordRow:
    chain_q = dict(zip(row.q_values, row.recorded_coefficients))
    first_q = boundary(chain_q, row.boundary_direction_q)
    bridge_q = inversion_boundary(first_q)
    chain_word = to_d_word(chain_q)
    first_word = to_d_word(first_q)
    bridge_word = to_d_word(bridge_q)
    boundary_step = d_residue_from_q(row.boundary_direction_q)
    hits = recovery_steps(chain_word, bridge_word)
    return PrimitiveWordRow(
        orientation_mask=row.orientation_mask,
        boundary_direction_q=row.boundary_direction_q,
        boundary_step_d=boundary_step,
        q_values=row.q_values,
        chain_word=as_items(chain_word),
        first_boundary_word=as_items(first_word),
        bridge_word=as_items(bridge_word),
        first_boundary_support_distribution=support_distribution(chain_word),
        bridge_recovery_steps=hits,
        unique_bridge_recovery_step=hits == (boundary_step,),
    )


def primitive_word_profile() -> PrimitiveWordProfile:
    bridge_word = to_d_word(bridge_coefficients())
    rows = tuple(primitive_word_row(row) for row in coefficient_rigidity_profile().rows)
    return PrimitiveWordProfile(
        bridge_word=as_items(bridge_word),
        canonical_chain_word=rows[0].chain_word,
        canonical_boundary_step=rows[0].boundary_step_d,
        canonical_first_boundary_word=rows[0].first_boundary_word,
        row_count=len(rows),
        rows=rows,
        all_rows_recover_bridge=all(row.bridge_word == as_items(bridge_word) for row in rows),
        all_rows_have_unique_recovery_step=all(row.unique_bridge_recovery_step for row in rows),
        all_rows_have_sparse_boundary_distribution=all(
            row.first_boundary_support_distribution == ((4, 6), (6, 500))
            for row in rows
        ),
    )


def main() -> int:
    print("p25 Lane B square-axis bridge Hilbert-90 source-chain primitive-word gate")
    profile = primitive_word_profile()
    expected_bridge = ((121, 1), (122, 1), (123, 1), (384, -1), (385, -1), (386, -1))
    expected_rows = (
        PrimitiveWordRow(1, 197, 122, (0, 172, 482), ((0, -1), (1, -1), (386, -1)), ((0, -1), (122, 1), (123, 1), (386, -1)), expected_bridge, ((4, 6), (6, 500)), (122,), True),
        PrimitiveWordRow(1, 310, 385, (172, 197, 369), ((1, 1), (122, 1), (123, 1)), ((0, -1), (122, 1), (123, 1), (386, -1)), expected_bridge, ((4, 6), (6, 500)), (385,), True),
        PrimitiveWordRow(6, 197, 122, (138, 310, 335), ((384, -1), (385, -1), (506, -1)), ((0, 1), (121, 1), (384, -1), (385, -1)), expected_bridge, ((4, 6), (6, 500)), (122,), True),
        PrimitiveWordRow(6, 310, 385, (0, 25, 335), ((0, 1), (121, 1), (506, 1)), ((0, 1), (121, 1), (384, -1), (385, -1)), expected_bridge, ((4, 6), (6, 500)), (385,), True),
    )
    row_ok = (
        profile.bridge_word == expected_bridge
        and profile.canonical_chain_word == ((0, -1), (1, -1), (386, -1))
        and profile.canonical_boundary_step == 122
        and profile.canonical_first_boundary_word == ((0, -1), (122, 1), (123, 1), (386, -1))
        and profile.row_count == 4
        and profile.rows == expected_rows
        and profile.all_rows_recover_bridge
        and profile.all_rows_have_unique_recovery_step
        and profile.all_rows_have_sparse_boundary_distribution
    )

    print(
        "primitive_word_summary: "
        f"bridge_word={profile.bridge_word} "
        f"canonical_chain_word={profile.canonical_chain_word} "
        f"canonical_boundary_step={profile.canonical_boundary_step} "
        f"canonical_first_boundary_word={profile.canonical_first_boundary_word}"
    )
    print("primitive_word_rows")
    for row in profile.rows:
        print(f"  {row}")
    print("formal_word")
    print("  canonical_chain = -(1 + z + z^-121) in C_507")
    print("  first_boundary = (1 - z^122) * canonical_chain")
    print("  the z^1 term cancels, leaving a four-point Hilbert-90 potential")
    print("  inversion_boundary(first_boundary) = z^121*(1 + z + z^2) - z^384*(1 + z + z^2)")
    print("interpretation")
    print("  active_source_chain_has_a_three_term_primitive_D_quotient_word=1")
    print("  rigid_197_310_boundary_becomes_the_unique_primitive_step_plusminus_122=1")
    print("  first_boundary_cancellation_is_the_local_mechanism_for_the_four_block_potential=1")
    print("  producer_can_target_this_three_term_word_before_the_raw_K_trace_is_attached=1")
    print(f"square_axis_bridge_hilbert90_source_chain_primitive_word_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
