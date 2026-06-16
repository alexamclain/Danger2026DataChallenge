#!/usr/bin/env python3
"""Rigidity of the p25 Robert/Siegel translated odd quotient skeleton.

The skeleton gate says a Robert/Siegel producer should emit

    base * K_trace * D_segment * (1 - T).

This gate checks that the visible quotient part is rigid.  On `C_3 x C_169`,
scan all nonzero directions `D` and edges `T` such that

    base + {0,D,2D}

is the positive bridge layer and translating it by `T` gives the negative
bridge layer.  The only factorizations are the recorded segment and its
reversal; both use the same quotient edge `(2,113)`.

So the arithmetic target is not merely "some translated odd quotient": it must
recover the specific `D=(1,3)` segment (up to reversal) and the specific
edge `T=(2,113)`.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_bridge_edge_quotient_contract_gate import (
    signed_cells,
    visible_cells,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class QuotientFactorization:
    base: Coord
    d_step: Coord
    edge_step: Coord
    reversed_recorded_segment: bool


@dataclass(frozen=True)
class TranslatedOddQuotientRigidityProfile:
    positive_layer: tuple[Coord, ...]
    negative_layer: tuple[Coord, ...]
    recorded_d_step: Coord
    recorded_edge_step: Coord
    positive_ap_factorizations: tuple[tuple[Coord, Coord], ...]
    signed_factorizations: tuple[QuotientFactorization, ...]
    unique_edge_steps: tuple[Coord, ...]
    only_recorded_segment_up_to_reversal: bool
    only_recorded_edge: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % 3, (left[1] + right[1]) % C_ORDER)


def scale_coord(step: Coord, scale: int) -> Coord:
    return ((step[0] * scale) % 3, (step[1] * scale) % C_ORDER)


def line_from(base: Coord, d_step: Coord) -> set[Coord]:
    return {add_coord(base, scale_coord(d_step, index)) for index in range(3)}


def all_quotient_coords() -> tuple[Coord, ...]:
    return tuple((right, c_value) for right in range(3) for c_value in range(C_ORDER))


def rigidity_profile() -> TranslatedOddQuotientRigidityProfile:
    positive = set(visible_cells(signed_cells(1)))
    negative = set(visible_cells(signed_cells(-1)))
    recorded_d = (D_SHIFT[0] % 3, D_SHIFT[1])
    recorded_edge = (BRIDGE_SHIFT[0] % 3, BRIDGE_SHIFT[1])
    coords = all_quotient_coords()

    ap_factorizations: list[tuple[Coord, Coord]] = []
    signed_factorizations: list[QuotientFactorization] = []
    for base in coords:
        for d_step in coords:
            if d_step == (0, 0):
                continue
            positive_line = line_from(base, d_step)
            if positive_line != positive:
                continue
            ap_factorizations.append((base, d_step))
            for edge_step in coords:
                if edge_step == (0, 0):
                    continue
                if {add_coord(point, edge_step) for point in positive_line} != negative:
                    continue
                signed_factorizations.append(
                    QuotientFactorization(
                        base=base,
                        d_step=d_step,
                        edge_step=edge_step,
                        reversed_recorded_segment=d_step == scale_coord(recorded_d, -1),
                    )
                )

    return TranslatedOddQuotientRigidityProfile(
        positive_layer=tuple(sorted(positive)),
        negative_layer=tuple(sorted(negative)),
        recorded_d_step=recorded_d,
        recorded_edge_step=recorded_edge,
        positive_ap_factorizations=tuple(ap_factorizations),
        signed_factorizations=tuple(signed_factorizations),
        unique_edge_steps=tuple(sorted({factor.edge_step for factor in signed_factorizations})),
        only_recorded_segment_up_to_reversal={
            factor.d_step for factor in signed_factorizations
        }
        == {recorded_d, scale_coord(recorded_d, -1)},
        only_recorded_edge=tuple(sorted({factor.edge_step for factor in signed_factorizations}))
        == (recorded_edge,),
    )


def main() -> int:
    print("p25 Lane B Robert/Siegel translated odd quotient rigidity gate")
    profile = rigidity_profile()
    row_ok = (
        profile.positive_layer == ((0, 31), (1, 25), (2, 28))
        and profile.negative_layer == ((0, 138), (1, 141), (2, 144))
        and profile.recorded_d_step == (1, 3)
        and profile.recorded_edge_step == (2, 113)
        and profile.positive_ap_factorizations
        == (((0, 31), (2, 166)), ((1, 25), (1, 3)))
        and profile.signed_factorizations
        == (
            QuotientFactorization(
                base=(0, 31),
                d_step=(2, 166),
                edge_step=(2, 113),
                reversed_recorded_segment=True,
            ),
            QuotientFactorization(
                base=(1, 25),
                d_step=(1, 3),
                edge_step=(2, 113),
                reversed_recorded_segment=False,
            ),
        )
        and profile.unique_edge_steps == ((2, 113),)
        and profile.only_recorded_segment_up_to_reversal
        and profile.only_recorded_edge
    )

    print(f"translated_odd_quotient_rigidity_profile={profile}")
    print("rigidity_laws")
    print("  positive_layer_has_only_recorded_AP_segment_and_reversal=1")
    print("  signed_bridge_has_only_edge_(2,113)=1")
    print("  no_other_D_segment_or_translated_edge_can_match_the_visible_bridge=1")
    print("interpretation")
    print("  robert_siegel_candidate_must_recover_D_equals_(1,3)_up_to_reversal=1")
    print("  robert_siegel_candidate_must_recover_edge_equals_(2,113)=1")
    print(f"robert_translated_odd_quotient_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_translated_odd_quotient_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
