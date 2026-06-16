#!/usr/bin/env python3
"""Unified expert-answer router for the current p25 subsqrt moonshot.

The workbench now has two complementary intake surfaces:

* local ray-source claims, screened by the ray-local modular-unit pullback
  router; and
* source/value theorem claims, screened by the conductor-39 expert-answer
  smoke packet.

This gate keeps those surfaces joined without identifying them.  A local
151-by-677 pullback explanation is useful only if it reaches a finite raw or
curved payload, and even then it is helper-only until a value/divisor theorem
appears.  A conductor-39 or H0 value theorem can close the source stage, but
still routes through DANGER3 framing, cross-level extraction, and official
vpp.py verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_atom_terminology_guardrail_gate import (
    profile_atom_terminology_guardrail,
)
from p25_ksy_y_conductor39_expert_answer_smoke_gate import (
    ExpertAnswerSmokeRow,
    profile_expert_answer_smoke,
)
from p25_ksy_y_external_bridge_resolution_queue_gate import (
    profile_external_bridge_resolution_queue,
)
from p25_laneB_ray_local_modular_unit_pullback_router_gate import (
    PullbackCandidate,
    PullbackDecision,
    classify_candidate as classify_pullback_candidate,
    profile_ray_local_modular_unit_pullback_router,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class UnifiedExpertAnswerRow:
    name: str
    answer_family: str
    local_router: str
    decision: str
    source_stage_closed: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    continue_or_kill: str
    ok: bool


@dataclass(frozen=True)
class UnifiedExpertAnswerRouter:
    atom_guardrail_ok: bool
    ray_local_router_ok: bool
    conductor39_minimal_query_ok: bool
    curved_corner_minimal_closing_ask_ok: bool
    conductor39_expert_smoke_ok: bool
    external_resolution_ok: bool
    rows: tuple[UnifiedExpertAnswerRow, ...]
    row_count: int
    local_pullback_rows: int
    source_value_rows: int
    downstream_rows: int
    guardrail_rows: int
    helper_only_rows: int
    conditional_rows: int
    rejected_rows: int
    source_stage_closed_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    placeholder_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def pullback_base() -> dict[str, bool]:
    return {
        "theorem_body_verified": True,
        "ray_local_inert_right_source": True,
        "split_c_axis_source": True,
        "source_coupling_not_separated": True,
        "residue_rectangles_constant": True,
        "mixed_rank2_non_degenerate": True,
        "avoids_degenerate_u_plus_2v": True,
        "not_x_only_even_table": True,
        "active_c_side_odd_orientation": True,
        "orientation_not_plain_c_character": True,
        "coupled_d_segment": True,
        "primitive_k_trace": True,
        "recorded_t_edge_2_113": True,
        "raw_kernel_gauge_only": True,
        "raw_vector_or_bridge_harness": False,
        "curved_corner_shape": False,
        "curved_corner_unit_triangle": False,
        "finite_value_or_divisor_theorem": False,
        "period156_context": False,
        "arithmetic_source_theorem": False,
        "danger3_framing": False,
        "same_j_x18112_bridge": False,
        "x16_surface": False,
        "concrete_A_x0": False,
        "official_vpp": False,
    }


def row_from_pullback(
    decision: PullbackDecision,
    *,
    continue_or_kill: str,
) -> UnifiedExpertAnswerRow:
    return UnifiedExpertAnswerRow(
        name=decision.candidate.name,
        answer_family="ray_local_pullback",
        local_router="p25_laneB_ray_local_modular_unit_pullback_router_gate.py",
        decision=decision.decision,
        source_stage_closed=decision.source_stage_closed,
        danger3_unblocked=decision.danger3_unblocked,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        continue_or_kill=continue_or_kill,
        ok=decision.ok,
    )


def smoke_row_by_name(rows: tuple[ExpertAnswerSmokeRow, ...], name: str) -> ExpertAnswerSmokeRow:
    for row in rows:
        if row.name == name:
            return row
    raise KeyError(name)


def row_from_smoke(
    smoke: ExpertAnswerSmokeRow,
    *,
    family: str,
    continue_or_kill: str,
) -> UnifiedExpertAnswerRow:
    return UnifiedExpertAnswerRow(
        name=smoke.name,
        answer_family=family,
        local_router="p25_ksy_y_conductor39_expert_answer_smoke_gate.py",
        decision=smoke.actual_decision,
        source_stage_closed=smoke.source_stage_closed,
        danger3_unblocked=smoke.danger3_unblocked,
        extraction_ready=smoke.extraction_ready,
        submission_ready=smoke.submission_ready,
        first_missing_or_falsifier=smoke.actual_missing_or_falsifier,
        continue_or_kill=continue_or_kill,
        ok=smoke.ok,
    )


def unified_rows(smoke_rows: tuple[ExpertAnswerSmokeRow, ...]) -> tuple[UnifiedExpertAnswerRow, ...]:
    local_base = pullback_base()
    no_payload = classify_pullback_candidate(
        PullbackCandidate("expert_ray_local_no_payload_yet", **local_base)
    )
    raw_bridge = classify_pullback_candidate(
        PullbackCandidate(
            "expert_ray_local_raw_bridge_helper",
            **{**local_base, "raw_vector_or_bridge_harness": True},
        )
    )
    curved_corner = classify_pullback_candidate(
        PullbackCandidate(
            "expert_ray_local_curved_corner_helper",
            **{
                **local_base,
                "curved_corner_shape": True,
                "curved_corner_unit_triangle": True,
            },
        )
    )
    return (
        row_from_pullback(
            no_payload,
            continue_or_kill="continue only after a raw theta31/bridge vector or curved-corner payload appears",
        ),
        row_from_pullback(
            raw_bridge,
            continue_or_kill="keep as finite helper; ask for finite value/divisor theorem",
        ),
        row_from_pullback(
            curved_corner,
            continue_or_kill="keep as unit-triangle 75-atom helper; ask for finite value/divisor theorem",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "smoke_Uchi_divisor_identity"),
            family="conductor39_value_theorem",
            continue_or_kill="continue to DANGER3 finite-identity framing",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "smoke_canonical_H0_ratio_identity"),
            family="h90_or_h0_value_theorem",
            continue_or_kill="continue to DANGER3 finite-identity framing",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "smoke_policy_yes_extraction_missing"),
            family="danger3_policy",
            continue_or_kill="continue to cross-level extraction and concrete A,x0",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "smoke_x1_8112_surface_halving_missing"),
            family="x1_8112_x16",
            continue_or_kill="continue to halving chain or direct x0, then official vpp.py",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "smoke_reject_generator_or_projection_only"),
            family="projection_guardrail",
            continue_or_kill="kill unless the mixed tensor and ray-local coupling are restored",
        ),
        row_from_smoke(
            smoke_row_by_name(smoke_rows, "verified_pomerance_triple_requires_real_values"),
            family="official_vpp_boundary",
            continue_or_kill="do not smoke-test submission without concrete A,x0",
        ),
    )


def profile_unified_expert_answer_router() -> UnifiedExpertAnswerRouter:
    atom = profile_atom_terminology_guardrail()
    ray = profile_ray_local_modular_unit_pullback_router()
    minimal_query_ok = marker_present(
        RESEARCH / "p25_ksy_y_conductor39_minimal_theorem_query_packet_20260614.md",
        "ksy_y_conductor39_minimal_theorem_query_packet_rows=1/1",
    )
    curved_corner_minimal_ok = marker_present(
        RESEARCH / "p25_ksy_y_curved_corner_minimal_closing_ask_packet_20260614.md",
        "ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1",
    )
    smoke = profile_expert_answer_smoke()
    external = profile_external_bridge_resolution_queue()
    rows = unified_rows(smoke.smoke_rows)
    local = sum(row.answer_family == "ray_local_pullback" for row in rows)
    source_value = sum(
        row.answer_family in {"conductor39_value_theorem", "h90_or_h0_value_theorem"}
        for row in rows
    )
    downstream = sum(row.answer_family in {"danger3_policy", "x1_8112_x16"} for row in rows)
    guardrails = sum(row.answer_family == "projection_guardrail" for row in rows)
    helper = sum(row.decision.startswith("helper_only_") for row in rows)
    conditional = sum(row.decision.startswith("conditional_") for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    placeholders = sum(row.decision == "not_smoked_without_concrete_A_x0" for row in rows)
    expected_decisions = (
        "conditional_no_raw_harness_or_curved_corner_payload",
        "helper_only_raw_bridge_payload_value_theorem_missing",
        "helper_only_curved_corner_payload_value_theorem_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "danger3_unblocked_extraction_missing",
        "x16_surface_reached_halving_or_vpp_missing",
        "reject_loses_mixed_tensor",
        "not_smoked_without_concrete_A_x0",
    )
    row_ok = (
        atom.row_ok
        and ray.row_ok
        and minimal_query_ok
        and curved_corner_minimal_ok
        and smoke.row_ok
        and external.row_ok
        and len(rows) == 9
        and local == 3
        and source_value == 2
        and downstream == 2
        and guardrails == 1
        and helper == 2
        and conditional == 1
        and rejected == 1
        and source_closed == 3
        and danger3 == 2
        and extraction == 0
        and submission == 0
        and placeholders == 1
        and tuple(row.decision for row in rows) == expected_decisions
        and all(row.ok for row in rows)
        and atom.atom_count == 75
        and not atom.atoms_are_search_candidates
    )
    return UnifiedExpertAnswerRouter(
        atom_guardrail_ok=atom.row_ok,
        ray_local_router_ok=ray.row_ok,
        conductor39_minimal_query_ok=minimal_query_ok,
        curved_corner_minimal_closing_ask_ok=curved_corner_minimal_ok,
        conductor39_expert_smoke_ok=smoke.row_ok,
        external_resolution_ok=external.row_ok,
        rows=rows,
        row_count=len(rows),
        local_pullback_rows=local,
        source_value_rows=source_value,
        downstream_rows=downstream,
        guardrail_rows=guardrails,
        helper_only_rows=helper,
        conditional_rows=conditional,
        rejected_rows=rejected,
        source_stage_closed_rows=source_closed,
        danger3_unblocked_rows=danger3,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        placeholder_rows=placeholders,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_unified_expert_answer_router()
    print("p25 KSY-y unified expert-answer router gate")
    print("dependencies")
    print(f"  atom_guardrail_ok={int(profile.atom_guardrail_ok)}")
    print(f"  ray_local_router_ok={int(profile.ray_local_router_ok)}")
    print(f"  conductor39_minimal_query_ok={int(profile.conductor39_minimal_query_ok)}")
    print(
        "  curved_corner_minimal_closing_ask_ok="
        f"{int(profile.curved_corner_minimal_closing_ask_ok)}"
    )
    print(f"  conductor39_expert_smoke_ok={int(profile.conductor39_expert_smoke_ok)}")
    print(f"  external_resolution_ok={int(profile.external_resolution_ok)}")
    print("answer_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: family={row.answer_family} decision={row.decision} "
            f"source_closed={int(row.source_stage_closed)} "
            f"danger3={int(row.danger3_unblocked)} "
            f"extraction={int(row.extraction_ready)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
        print(f"    next={row.continue_or_kill}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  local_pullback_rows={profile.local_pullback_rows}")
    print(f"  source_value_rows={profile.source_value_rows}")
    print(f"  downstream_rows={profile.downstream_rows}")
    print(f"  guardrail_rows={profile.guardrail_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  source_stage_closed_rows={profile.source_stage_closed_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  placeholder_rows={profile.placeholder_rows}")
    print("interpretation")
    print("  ray_local_pullback_yes_is_helper_only_until_value_theorem=1")
    print("  unit_triangle_curved_corner_yes_uses_minimal_closing_ask_packet=1")
    print("  conductor39_or_H0_value_yes_closes_source_stage_not_submission=1")
    print("  projection_or_generator_only_answers_are_killed=1")
    print("  verified_triple_boundary_requires_real_A_x0_and_official_vpp=1")
    print(f"ksy_y_unified_expert_answer_router_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("unified expert-answer router regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
