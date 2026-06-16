#!/usr/bin/env python3
"""Reality check for p25 KSY/Yang/H90 finite payloads.

This gate keeps three notions separate:

* fixed product atoms and finite verifier fixtures we already have,
* theorem shapes that would close the source stage if supplied, and
* the final DANGER3 submission boundary.

It is intentionally conservative: current fixtures and computed payloads are
not counted as arithmetic source theorems.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_atom_terminology_guardrail_gate import (
    profile_atom_terminology_guardrail,
)
from p25_ksy_y_h0_period156_value_compatibility_gate import (
    profile_h0_period156_value_compatibility,
)
from p25_ksy_y_h0_translate_value_compatibility_gate import (
    profile_h0_translate_value_compatibility,
)
from p25_ksy_y_period156_value_source_route_packet_gate import (
    profile_period156_value_source_route_packet,
)
from p25_ksy_y_post_local_source_value_side_queue_gate import (
    profile_post_local_source_value_side_queue,
)
from p25_ksy_y_twisted_h90_candidate_packet_intake_gate import (
    profile_twisted_h90_candidate_packet_intake,
)
from p25_ksy_y_twisted_h90_packet_fixture_export_gate import (
    profile_twisted_h90_packet_fixture_export,
)


@dataclass(frozen=True)
class ValuePayloadRealityRow:
    name: str
    evidence_kind: str
    decision: str
    current_evidence_exists: bool
    source_stage_closes: bool
    current_source_theorem_exists: bool
    computed_payload_only: bool
    rejected: bool
    conditional: bool
    submission_boundary: bool
    current_submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class ValuePayloadRealityProfile:
    atom_guardrail_ok: bool
    value_side_queue_ok: bool
    period156_route_ok: bool
    h0_period156_ok: bool
    h0_translate_ok: bool
    twisted_packet_intake_ok: bool
    twisted_fixture_export_ok: bool
    atom_count: int
    atoms_are_search_candidates: bool
    support_period_root_gcd: int
    ambient_period_root_gcd: int
    legal_h0_translate_rows: int
    twisted_fixture_count: int
    rows: tuple[ValuePayloadRealityRow, ...]
    row_count: int
    current_evidence_rows: int
    source_closing_shape_rows: int
    current_source_theorem_rows: int
    computed_payload_only_rows: int
    rejected_rows: int
    conditional_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def reality_rows() -> tuple[ValuePayloadRealityRow, ...]:
    return (
        ValuePayloadRealityRow(
            name="fixed_75_atom_product",
            evidence_kind="terminology_guardrail",
            decision="fixed_product_factors_not_search_candidates",
            current_evidence_exists=True,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="arithmetic identity selecting the whole 75-atom product",
            next_action="do not enumerate atoms; route claims through exact product/value theorem intake",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="stable_payload_fixtures",
            evidence_kind="finite_target_fixture",
            decision="finite_target_not_arithmetic_source_theorem",
            current_evidence_exists=True,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=True,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            next_action="use fixtures only as exact target/verifier inputs for future theorem hits",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="finite_verifier_payload_without_source",
            evidence_kind="computed_payload",
            decision="conditional_finite_payload_without_source_theorem",
            current_evidence_exists=True,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=True,
            rejected=False,
            conditional=True,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="arithmetic producer theorem, not just a finite payload",
            next_action="ask whether a source proves the payload, value, or divisor identity",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="exact_p_value_with_period156_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_value_source_stage_then_need_danger3",
            current_evidence_exists=False,
            source_stage_closes=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="named theorem giving exact P, mixed graph, finite identity, and period-156 context",
            next_action="classify through period-156 value source-route packet",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="h0_value_boundary_period156_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_h0_value_source_stage_then_need_danger3",
            current_evidence_exists=False,
            source_stage_closes=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="H0/Y507 value theorem with boundary to Norm_156(Y_507) and period-156 context",
            next_action="classify through H0 period-156 value compatibility gate",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="h0_divisor_boundary_shape",
            evidence_kind="source_theorem_shape",
            decision="would_close_h0_divisor_source_stage_then_need_danger3",
            current_evidence_exists=False,
            source_stage_closes=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="H0/H0-translate divisor or additive identity with legal boundary",
            next_action="classify through H0 translate value-compatibility gate",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="ambient_780_value_shadow",
            evidence_kind="rejected_shadow",
            decision="reject_ambient_780_mu11_branch",
            current_evidence_exists=True,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=True,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="gcd(4^780 - 1, p - 1) = 11",
            next_action="discard unless it descends to support period 156",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="generic_field_generation_or_cm_shadow",
            evidence_kind="rejected_shadow",
            decision="reject_generic_generation_not_value_or_finite_identity",
            current_evidence_exists=True,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=True,
            conditional=False,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="exact p25 finite product/value/divisor identity",
            next_action="use as vocabulary only; do not count as DANGER3 framing",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="source_closed_no_danger3",
            evidence_kind="post_source_stage",
            decision="source_theorem_closed_policy_or_framing_missing",
            current_evidence_exists=False,
            source_stage_closes=True,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=True,
            submission_boundary=False,
            current_submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing, bridge, extraction, and vpp",
            next_action="route through twisted/H90 candidate-packet intake",
            ok=True,
        ),
        ValuePayloadRealityRow(
            name="official_vpp_boundary",
            evidence_kind="submission_boundary",
            decision="submission_ready_only_after_concrete_official_vpp",
            current_evidence_exists=False,
            source_stage_closes=False,
            current_source_theorem_exists=False,
            computed_payload_only=False,
            rejected=False,
            conditional=False,
            submission_boundary=True,
            current_submission_ready=False,
            first_missing_or_falsifier="concrete p25 A,x0 passing official DANGER3 vpp.py",
            next_action="on hit or extraction output, run official verifier before calling victory",
            ok=True,
        ),
    )


def profile_value_payload_reality_check() -> ValuePayloadRealityProfile:
    atom = profile_atom_terminology_guardrail()
    value_queue = profile_post_local_source_value_side_queue()
    period = profile_period156_value_source_route_packet()
    h0 = profile_h0_period156_value_compatibility()
    h0_translate = profile_h0_translate_value_compatibility()
    packet = profile_twisted_h90_candidate_packet_intake()
    fixtures = profile_twisted_h90_packet_fixture_export()
    rows = reality_rows()

    current_evidence = sum(row.current_evidence_exists for row in rows)
    source_shapes = sum(row.source_stage_closes for row in rows)
    current_sources = sum(row.current_source_theorem_exists for row in rows)
    computed_only = sum(row.computed_payload_only for row in rows)
    rejected = sum(row.rejected for row in rows)
    conditional = sum(row.conditional for row in rows)
    submission_boundary = sum(row.submission_boundary for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)

    row_ok = (
        atom.row_ok
        and value_queue.row_ok
        and period.row_ok
        and h0.row_ok
        and h0_translate.row_ok
        and packet.row_ok
        and fixtures.row_ok
        and atom.atom_count == 75
        and not atom.atoms_are_search_candidates
        and value_queue.active_closing_target_rows == 1
        and value_queue.ambient_780_rejected_rows == 1
        and period.support_root_gcd_fp_star == 1
        and period.ambient_root_gcd_fp_star == 11
        and period.closing_value_rows == 3
        and period.submission_ready_rows == 0
        and h0.source_closing_rows == 3
        and h0.value_closing_rows == 2
        and h0.divisor_closing_rows == 1
        and h0_translate.legal_translate_rows == 4
        and h0_translate.source_closing_rows == 5
        and h0_translate.submission_ready_rows == 0
        and packet.submission_ready_rows == 1
        and fixtures.fixture_count == 5
        and fixtures.submission_ready_rows == 1
        and len(rows) == 10
        and current_evidence == 5
        and source_shapes == 4
        and current_sources == 0
        and computed_only == 2
        and rejected == 2
        and conditional == 2
        and submission_boundary == 1
        and current_submission == 0
        and all(row.ok for row in rows)
    )

    return ValuePayloadRealityProfile(
        atom_guardrail_ok=atom.row_ok,
        value_side_queue_ok=value_queue.row_ok,
        period156_route_ok=period.row_ok,
        h0_period156_ok=h0.row_ok,
        h0_translate_ok=h0_translate.row_ok,
        twisted_packet_intake_ok=packet.row_ok,
        twisted_fixture_export_ok=fixtures.row_ok,
        atom_count=atom.atom_count,
        atoms_are_search_candidates=atom.atoms_are_search_candidates,
        support_period_root_gcd=period.support_root_gcd_fp_star,
        ambient_period_root_gcd=period.ambient_root_gcd_fp_star,
        legal_h0_translate_rows=h0_translate.legal_translate_rows,
        twisted_fixture_count=fixtures.fixture_count,
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current_evidence,
        source_closing_shape_rows=source_shapes,
        current_source_theorem_rows=current_sources,
        computed_payload_only_rows=computed_only,
        rejected_rows=rejected,
        conditional_rows=conditional,
        submission_boundary_rows=submission_boundary,
        current_submission_ready_rows=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_value_payload_reality_check()
    print("p25 KSY-y value-payload reality-check gate")
    print("dependencies")
    print(f"  atom_guardrail_ok={int(profile.atom_guardrail_ok)}")
    print(f"  value_side_queue_ok={int(profile.value_side_queue_ok)}")
    print(f"  period156_route_ok={int(profile.period156_route_ok)}")
    print(f"  h0_period156_ok={int(profile.h0_period156_ok)}")
    print(f"  h0_translate_ok={int(profile.h0_translate_ok)}")
    print(f"  twisted_packet_intake_ok={int(profile.twisted_packet_intake_ok)}")
    print(f"  twisted_fixture_export_ok={int(profile.twisted_fixture_export_ok)}")
    print("invariants")
    print(f"  atom_count={profile.atom_count}")
    print(f"  atoms_are_search_candidates={int(profile.atoms_are_search_candidates)}")
    print(f"  support_period_root_gcd={profile.support_period_root_gcd}")
    print(f"  ambient_period_root_gcd={profile.ambient_period_root_gcd}")
    print(f"  legal_h0_translate_rows={profile.legal_h0_translate_rows}")
    print(f"  twisted_fixture_count={profile.twisted_fixture_count}")
    print("reality_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: kind={row.evidence_kind} decision={row.decision} "
            f"current={int(row.current_evidence_exists)} "
            f"source_shape={int(row.source_stage_closes)} "
            f"current_source={int(row.current_source_theorem_exists)} "
            f"computed_only={int(row.computed_payload_only)} "
            f"rejected={int(row.rejected)} "
            f"conditional={int(row.conditional)} "
            f"submission_boundary={int(row.submission_boundary)} "
            f"current_submission={int(row.current_submission_ready)} "
            f"missing={row.first_missing_or_falsifier}"
        )
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  source_closing_shape_rows={profile.source_closing_shape_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  computed_payload_only_rows={profile.computed_payload_only_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  75_atoms_are_fixed_payload_factors_not_75_trials=1")
    print("  finite_payload_fixtures_are_targets_not_source_theorems=1")
    print("  current_source_theorem_rows_remain_zero=1")
    print("  official_vpp_verified_A_x0_is_the_submission_boundary=1")
    print(f"ksy_y_value_payload_reality_check_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("value-payload reality-check regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
