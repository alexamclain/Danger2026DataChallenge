#!/usr/bin/env python3
"""Subsqrt budget ladder for the p25 KSY/Yang/H90 moonshot.

The moonshot is only useful if the theorem-side objects stay far below the
Pomerance sqrt scale while the DANGER3 finish line remains a concrete verified
triple.  This gate recomputes the current compact finite budgets and ties them
to the period-156 value route and downstream extraction ladder.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

from p25_ksy_y_period156_value_source_route_packet_gate import (
    profile_period156_value_source_route_packet,
)
from p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate import (
    profile_ksy_yang_h90_bridge_spine,
)
from p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate import (
    profile_minimal_producer_spine,
)
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import (
    theta2_support_resolvent_profile,
)
from p25_laneB_robert_ksy_theta2_telescoping_certificate_gate import (
    profile_telescoping_certificate,
)
from p25_ksy_y_danger3_extraction_surface_gate import (
    profile_danger3_extraction_surface,
)


P25 = 10**25 + 13
SQRT_FLOOR = isqrt(P25)


@dataclass(frozen=True)
class SubsqrtBudgetRow:
    name: str
    count: int
    budget_kind: str
    source_gate: str
    current_checkpoint: bool
    below_sqrt: bool
    sqrt_margin_floor: int
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class MoonshotAcceptanceRow:
    name: str
    accepted_state: str
    value_source_closed: bool
    danger3_policy_required: bool
    cross_level_required: bool
    extraction_required: bool
    vpp_required: bool
    current_submission_ready: bool
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class SubsqrtMoonshotBudgetLadder:
    p: int
    sqrt_floor: int
    bridge_spine_ok: bool
    minimal_spine_ok: bool
    support_resolvent_ok: bool
    telescoping_ok: bool
    period156_route_ok: bool
    extraction_surface_ok: bool
    budget_rows: tuple[SubsqrtBudgetRow, ...]
    acceptance_rows: tuple[MoonshotAcceptanceRow, ...]
    current_budget_rows: int
    current_max_budget: int
    current_max_budget_name: str
    current_max_margin_floor: int
    all_current_budgets_below_sqrt: bool
    historical_ambient_budget_below_sqrt: bool
    period156_unique_root: bool
    ambient780_has_mu11_ambiguity: bool
    current_submission_ready_rows: int
    row_ok: bool


def budget_row(
    name: str,
    count: int,
    budget_kind: str,
    source_gate: str,
    current_checkpoint: bool,
    first_missing_clause: str,
) -> SubsqrtBudgetRow:
    below = 0 < count < SQRT_FLOOR
    margin = SQRT_FLOOR // count if count > 0 else 0
    return SubsqrtBudgetRow(
        name=name,
        count=count,
        budget_kind=budget_kind,
        source_gate=source_gate,
        current_checkpoint=current_checkpoint,
        below_sqrt=below,
        sqrt_margin_floor=margin,
        first_missing_clause=first_missing_clause,
        ok=below,
    )


def profile_subsqrt_moonshot_budget_ladder() -> SubsqrtMoonshotBudgetLadder:
    bridge = profile_ksy_yang_h90_bridge_spine()
    spine = profile_minimal_producer_spine()
    resolvent = theta2_support_resolvent_profile()
    telescoping = profile_telescoping_certificate()
    period = profile_period156_value_source_route_packet()
    extraction = profile_danger3_extraction_surface()

    budget_rows = (
        budget_row(
            "quotient_factor_input_cells",
            spine.quotient_factor_input_cells,
            "source-factor input cells",
            "p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py",
            True,
            "arithmetic producer theorem for the finite spine",
        ),
        budget_row(
            "source_quotient_packet_support",
            spine.source_packet_support,
            "signed cells on C3 x C169",
            "p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py",
            True,
            "challenge-legal source theorem for the packet",
        ),
        budget_row(
            "quotient_factor_support_budget",
            spine.factor_certificate_support_budget,
            "factor support budget",
            "p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py",
            True,
            "arithmetic producer theorem for the quotient factors",
        ),
        budget_row(
            "ksy_fixed_atoms",
            bridge.atom_count,
            "fixed normalized-y atoms",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "exact theorem selecting the whole product, not one atom",
        ),
        budget_row(
            "h90_positive_factor_count",
            bridge.h90_positive_factor_count,
            "positive Hilbert-90 factors",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "finite-field value/divisor identity for the H0 product",
        ),
        budget_row(
            "h90_negative_factor_count",
            bridge.h90_negative_factor_count,
            "negative Hilbert-90 factors",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "finite-field value/divisor identity for the H0 product",
        ),
        budget_row(
            "quotient_y507_support",
            bridge.quotient_y507_support,
            "Y_507 quotient support",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "value/divisor theorem for Y_507 carrying the bridge",
        ),
        budget_row(
            "h90_potential_support",
            bridge.h90_potential_support,
            "sparse Hilbert-90 potential support",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "legal finite-field identity for canonical H0 or translate",
        ),
        budget_row(
            "raw_siegel_footprint",
            bridge.raw_siegel_term_count,
            "raw Siegel footprint terms",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "arithmetic theorem selecting the exact K-traced product",
        ),
        budget_row(
            "period_norm_support",
            bridge.period_norm_support,
            "period-norm support cells",
            "p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py",
            True,
            "period-156 value theorem for the norm object",
        ),
        budget_row(
            "telescoping_compact_budget",
            spine.telescoping_compact_budget,
            "compact linear cell checks",
            "p25_laneB_robert_ksy_theta2_minimal_producer_spine_gate.py",
            True,
            "arithmetic source, DANGER3 framing, and extraction",
        ),
        budget_row(
            "support_resolvent_union_support",
            resolvent.support_resolvent_union_support,
            "shifted support union cells",
            "p25_laneB_robert_ksy_theta2_support_resolvent_gate.py",
            True,
            "theorem-side source identity and finite-field framing",
        ),
        budget_row(
            "support_resolvent_term_budget",
            resolvent.support_resolvent_term_budget,
            "expanded support-resolvent terms",
            "p25_laneB_robert_ksy_theta2_support_resolvent_gate.py",
            True,
            "DANGER3 extraction to concrete A,x0",
        ),
        budget_row(
            "old_ambient_resolvent_shadow",
            resolvent.old_ambient_term_budget,
            "old ambient-period shadow terms",
            "p25_laneB_robert_ksy_theta2_support_resolvent_gate.py",
            False,
            "not the selected route; period-156 is sharper",
        ),
    )

    acceptance_rows = (
        MoonshotAcceptanceRow(
            name="finite_spine_payload",
            accepted_state="compact KSY/Yang/H90 finite payload under sqrt",
            value_source_closed=False,
            danger3_policy_required=True,
            cross_level_required=True,
            extraction_required=True,
            vpp_required=True,
            current_submission_ready=False,
            first_missing_clause="challenge-legal arithmetic producer theorem",
            ok=True,
        ),
        MoonshotAcceptanceRow(
            name="period156_value_theorem",
            accepted_state="exact P/Y507/H0 finite-field value identity with period-156 context",
            value_source_closed=True,
            danger3_policy_required=True,
            cross_level_required=True,
            extraction_required=True,
            vpp_required=True,
            current_submission_ready=False,
            first_missing_clause="DANGER3 finite-identity/non-CM framing",
            ok=True,
        ),
        MoonshotAcceptanceRow(
            name="danger3_policy_unblocked",
            accepted_state="policy-accepted finite-field identity route",
            value_source_closed=True,
            danger3_policy_required=False,
            cross_level_required=True,
            extraction_required=True,
            vpp_required=True,
            current_submission_ready=False,
            first_missing_clause="X_1(8112)/X_1(16) bridge and concrete A,x0",
            ok=True,
        ),
        MoonshotAcceptanceRow(
            name="x16_surface_reached",
            accepted_state="X_1(16) y, A, and xP16 surface",
            value_source_closed=True,
            danger3_policy_required=False,
            cross_level_required=False,
            extraction_required=True,
            vpp_required=True,
            current_submission_ready=False,
            first_missing_clause="valid halving chain from xP16 to x0",
            ok=True,
        ),
        MoonshotAcceptanceRow(
            name="verified_pomerance_triple",
            accepted_state="concrete p25 (p,A,x0) verified by official vpp.py",
            value_source_closed=True,
            danger3_policy_required=False,
            cross_level_required=False,
            extraction_required=False,
            vpp_required=False,
            current_submission_ready=True,
            first_missing_clause="none",
            ok=True,
        ),
    )

    current_rows = tuple(row for row in budget_rows if row.current_checkpoint)
    current_max = max(current_rows, key=lambda row: row.count)
    current_submission_ready = period.submission_ready_rows
    row_ok = (
        P25 == 10**25 + 13
        and SQRT_FLOOR == 3162277660168
        and bridge.row_ok
        and spine.row_ok
        and resolvent.row_ok
        and telescoping.row_ok
        and period.row_ok
        and extraction.row_ok
        and len(budget_rows) == 14
        and len(current_rows) == 13
        and all(row.ok for row in budget_rows)
        and current_max.name == "support_resolvent_term_budget"
        and current_max.count == 46800
        and current_max.sqrt_margin_floor == SQRT_FLOOR // 46800
        and resolvent.support_resolvent_union_support == 11700
        and telescoping.compact_linear_cell_check_budget == 975
        and telescoping.expanded_resolvent_term_budget == 46800
        and resolvent.old_ambient_term_budget == 234000
        and period.support_root_gcd_fp_star == 1
        and period.ambient_root_gcd_fp_star == 11
        and period.submission_ready_rows == 0
        and extraction.x16_surface.k == 42
        and extraction.submission_ready_rows == 1
        and sum(row.current_submission_ready for row in acceptance_rows) == 1
        and not any(row.current_submission_ready for row in acceptance_rows[:-1])
    )

    return SubsqrtMoonshotBudgetLadder(
        p=P25,
        sqrt_floor=SQRT_FLOOR,
        bridge_spine_ok=bridge.row_ok,
        minimal_spine_ok=spine.row_ok,
        support_resolvent_ok=resolvent.row_ok,
        telescoping_ok=telescoping.row_ok,
        period156_route_ok=period.row_ok,
        extraction_surface_ok=extraction.row_ok,
        budget_rows=budget_rows,
        acceptance_rows=acceptance_rows,
        current_budget_rows=len(current_rows),
        current_max_budget=current_max.count,
        current_max_budget_name=current_max.name,
        current_max_margin_floor=current_max.sqrt_margin_floor,
        all_current_budgets_below_sqrt=all(row.below_sqrt for row in current_rows),
        historical_ambient_budget_below_sqrt=budget_rows[-1].below_sqrt,
        period156_unique_root=period.support_root_gcd_fp_star == 1,
        ambient780_has_mu11_ambiguity=period.ambient_root_gcd_fp_star == 11,
        current_submission_ready_rows=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_subsqrt_moonshot_budget_ladder()
    print("p25 KSY-y subsqrt moonshot budget ladder gate")
    print("dependencies")
    print(f"  bridge_spine_ok={int(profile.bridge_spine_ok)}")
    print(f"  minimal_spine_ok={int(profile.minimal_spine_ok)}")
    print(f"  support_resolvent_ok={int(profile.support_resolvent_ok)}")
    print(f"  telescoping_ok={int(profile.telescoping_ok)}")
    print(f"  period156_route_ok={int(profile.period156_route_ok)}")
    print(f"  extraction_surface_ok={int(profile.extraction_surface_ok)}")
    print("scale")
    print(f"  p={profile.p}")
    print(f"  sqrt_floor={profile.sqrt_floor}")
    print("budget_rows")
    for row in profile.budget_rows:
        print(
            "  "
            f"{row.name}: count={row.count} current={int(row.current_checkpoint)} "
            f"below_sqrt={int(row.below_sqrt)} margin={row.sqrt_margin_floor} "
            f"kind={row.budget_kind} missing={row.first_missing_clause}"
        )
    print("acceptance_rows")
    for row in profile.acceptance_rows:
        print(
            "  "
            f"{row.name}: value={int(row.value_source_closed)} "
            f"policy_required={int(row.danger3_policy_required)} "
            f"cross_level_required={int(row.cross_level_required)} "
            f"extraction_required={int(row.extraction_required)} "
            f"vpp_required={int(row.vpp_required)} "
            f"submission={int(row.current_submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  current_budget_rows={profile.current_budget_rows}")
    print(f"  current_max_budget_name={profile.current_max_budget_name}")
    print(f"  current_max_budget={profile.current_max_budget}")
    print(f"  current_max_margin_floor={profile.current_max_margin_floor}")
    print(f"  all_current_budgets_below_sqrt={int(profile.all_current_budgets_below_sqrt)}")
    print(f"  historical_ambient_budget_below_sqrt={int(profile.historical_ambient_budget_below_sqrt)}")
    print(f"  period156_unique_root={int(profile.period156_unique_root)}")
    print(f"  ambient780_has_mu11_ambiguity={int(profile.ambient780_has_mu11_ambiguity)}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  finite_moonshot_checkpoints_are_subsqrt_but_not_submission_ready=1")
    print("  period156_value_route_is_the_selected_value_route_over_ambient780=1")
    print("  support_resolvent_term_budget_46800_is_current_max_budget=1")
    print("  DANGER3_still_requires_framing_extraction_and_official_vpp=1")
    print(f"ksy_y_subsqrt_moonshot_budget_ladder_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("subsqrt moonshot budget ladder regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
