#!/usr/bin/env python3
"""Frontier gate for the Sprang/Kronecker exact-specialization route.

The preceding Sprang checks left one live door: an even-D theorem could still
close the p25 payload if it emits the exact mixed row-labeled P/theta2 data.
This gate records what the current primary-source clauses do and do not supply,
and it prevents the moonshot from drifting back into broad kernel/torsion
language after those shadows have been falsified.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_sprang_distribution_shape_boundary_gate import (
    D_STEP,
    T_EDGE,
    add,
    profile_sprang_distribution_shape_boundary,
    scale,
    target_positive,
    translate,
)
from p25_ksy_y_sprang_even_d_specialization_contract_gate import (
    profile_sprang_even_d_specialization_contract,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class SprangFrontierRow:
    name: str
    current_source_status: str
    finite_falsifier: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class SprangExactSpecializationFrontier:
    target_positive_layer: tuple[Coord, ...]
    target_negative_layer: tuple[Coord, ...]
    target_total_support: int
    d_step_order: int
    three_d: Coord
    d2_nonzero_terms: int
    d2_image_support_on_odd_quotient: int
    source_contract_ok: bool
    shape_boundary_ok: bool
    current_source_direct_closing_rows: int
    killed_current_source_rows: tuple[SprangFrontierRow, ...]
    live_external_exact_payload_row: SprangFrontierRow
    shift_active_search_to_kl_without_new_sprang_source: bool
    row_ok: bool


def d2_torsion_image_on_odd_quotient() -> tuple[Coord, ...]:
    """Any hom C2 x C2 -> C3 x C169 is trivial."""
    return ((0, 0), (0, 0), (0, 0))


def profile_sprang_exact_specialization_frontier() -> SprangExactSpecializationFrontier:
    source = profile_sprang_even_d_specialization_contract()
    shape = profile_sprang_distribution_shape_boundary()
    positive = target_positive()
    negative = translate(positive)
    total_support = len(set(positive) | set(negative))
    d2_image = d2_torsion_image_on_odd_quotient()

    killed = (
        SprangFrontierRow(
            name="sprang_1801_even_d_omega_surface",
            current_source_status="real even-D differential surface",
            finite_falsifier="omega^D/dlog language does not select base, D-segment, T edge, or K trace",
            decision="keep_as_vocabulary_not_payload",
            ok=source.even_d_surface_rows == 1 and source.direct_closing_rows == 0,
        ),
        SprangFrontierRow(
            name="sprang_1801_distribution_kernel_sum",
            current_source_status="full sums over isogeny kernels and D'-torsion translations",
            finite_falsifier=(
                "target D segment has order 507 and 3D=(0,9), so the three "
                "visible atoms are not a subgroup/coset distribution"
            ),
            decision="kill_literal_kernel_distribution_as_closer",
            ok=shape.d_visible_order == 507
            and shape.d_after_three == (0, 9)
            and shape.d_segment_is_not_order3_subgroup,
        ),
        SprangFrontierRow(
            name="sprang_d2_nonzero_torsion_shadow",
            current_source_status="abstract D=2 nonzero torsion has three terms",
            finite_falsifier=(
                "every hom from C2 x C2 to the odd quotient C3 x C169 is zero, "
                "so the image support is one point, not the p25 row-labeled triple"
            ),
            decision="kill_literal_D2_torsion_image_as_closer",
            ok=len(d2_image) == 3
            and len(set(d2_image)) == 1
            and len(set(positive)) == 3
            and shape.d2_literal_torsion_selector_killed,
        ),
        SprangFrontierRow(
            name="sprang_1802_kato_siegel_thetaD2_import",
            current_source_status="Kato-Siegel comparison is prime-to-6 in the displayed theorem",
            finite_falsifier="D=2 cannot be imported as theta_D from that clause without a replacement theorem",
            decision="kill_direct_thetaD2_import_keep_kronecker_variant",
            ok=source.prime_to_6_blocked_rows == 1 and source.rejected_rows >= 2,
        ),
        SprangFrontierRow(
            name="sprang_1802_cohomology_formula",
            current_source_status="de Rham/Eisenstein-class formula",
            finite_falsifier="cohomology output is not a finite p25 P/theta2 divisor or value identity",
            decision="kill_as_direct_product_closer",
            ok=source.cohomology_output_rows == 1 and source.direct_closing_rows == 0,
        ),
    )

    live = SprangFrontierRow(
        name="future_exact_mixed_row_labeled_specialization",
        current_source_status="not present in inspected Sprang clauses",
        finite_falsifier="must emit exact positive layer, T-translate orientation, and K-traced P/theta2 payload",
        decision="continue_only_on_named_source_theorem_or_formula_hit",
        ok=shape.target_profile.equals_target
        and shape.target_profile.preserves_row_graph
        and shape.target_profile.preserves_t_edge
        and total_support == 6,
    )

    shift_to_kl = (
        source.row_ok
        and shape.row_ok
        and source.direct_closing_rows == 0
        and all(row.ok for row in killed)
        and live.ok
    )

    row_ok = (
        shift_to_kl
        and source.conditional_rows == 2
        and source.hypothetical_closing_rows == 1
        and len(killed) == 5
        and positive == ((0, 31), (1, 25), (2, 28))
        and negative == ((0, 138), (1, 141), (2, 144))
        and add(D_STEP, scale(D_STEP, 2)) not in {scale(D_STEP, i) for i in range(3)}
        and T_EDGE == (2, 113)
    )

    return SprangExactSpecializationFrontier(
        target_positive_layer=positive,
        target_negative_layer=negative,
        target_total_support=total_support,
        d_step_order=shape.d_visible_order,
        three_d=shape.d_after_three,
        d2_nonzero_terms=len(d2_image),
        d2_image_support_on_odd_quotient=len(set(d2_image)),
        source_contract_ok=source.row_ok,
        shape_boundary_ok=shape.row_ok,
        current_source_direct_closing_rows=source.direct_closing_rows,
        killed_current_source_rows=killed,
        live_external_exact_payload_row=live,
        shift_active_search_to_kl_without_new_sprang_source=shift_to_kl,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_sprang_exact_specialization_frontier()
    print("p25 KSY-y Sprang exact-specialization frontier gate")
    print("target")
    print(f"  positive={profile.target_positive_layer}")
    print(f"  negative={profile.target_negative_layer}")
    print(f"  total_support={profile.target_total_support}")
    print(f"  D_step_order={profile.d_step_order}")
    print(f"  three_D={profile.three_d}")
    print("literal_D2_shadow")
    print(f"  d2_nonzero_terms={profile.d2_nonzero_terms}")
    print(
        "  d2_image_support_on_odd_quotient="
        f"{profile.d2_image_support_on_odd_quotient}"
    )
    print("current_sprang_source_rows")
    for row in profile.killed_current_source_rows:
        print(
            "  "
            f"{row.name}: ok={int(row.ok)} decision={row.decision} "
            f"status={row.current_source_status}"
        )
        print(f"    falsifier={row.finite_falsifier}")
    live = profile.live_external_exact_payload_row
    print("live_row")
    print(f"  {live.name}: ok={int(live.ok)} decision={live.decision}")
    print(f"    obligation={live.finite_falsifier}")
    print("counts")
    print(f"  source_contract_ok={int(profile.source_contract_ok)}")
    print(f"  shape_boundary_ok={int(profile.shape_boundary_ok)}")
    print(
        "  current_source_direct_closing_rows="
        f"{profile.current_source_direct_closing_rows}"
    )
    print(
        "  shift_active_search_to_KL_without_new_Sprang_source="
        f"{int(profile.shift_active_search_to_kl_without_new_sprang_source)}"
    )
    print("interpretation")
    print("  broad_Sprang_kernel_or_D2_torsion_language_is_drained=1")
    print("  Sprang_continues_only_on_exact_mixed_row_labeled_theorem_hit=1")
    print("  otherwise_next_front_door_is_Kubert_Lang_or_KSY_exact_product=1")
    print(
        "ksy_y_sprang_exact_specialization_frontier_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Sprang exact-specialization frontier regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
