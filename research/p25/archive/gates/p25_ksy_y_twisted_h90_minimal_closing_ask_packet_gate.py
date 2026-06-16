#!/usr/bin/env python3
"""Minimal closing-ask packet for the conductor-39 twisted/H90 route.

The candidate router is intentionally broad: it rejects malformed inputs,
classifies helpers, and keeps the verified-triple boundary.  This gate records
the smaller frontier ask for expert/literature search after the pure norm and
pair-sum routes have been killed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_conductor39_twisted_descent_candidate_router_gate import (
    TwistedDescentCandidate,
    classify_candidate,
)


REPO = Path(__file__).resolve().parents[2]
RESEARCH = REPO / "research" / "p25"

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_conductor39_minimal_theorem_query_packet_20260614.md",
        "ksy_y_conductor39_minimal_theorem_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_degree6_value_descent_packet_20260614.md",
        "ksy_y_conductor39_degree6_value_descent_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_twisted_descent_decision_packet_20260614.md",
        "ksy_y_conductor39_twisted_descent_decision_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_twisted_descent_candidate_router_20260614.md",
        "ksy_y_conductor39_twisted_descent_candidate_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h90_value_theorem_intake_20260614.md",
        "ksy_y_h90_value_theorem_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_value_theorem_source_route_packet_20260614.md",
        "ksy_y_conductor39_value_theorem_source_route_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_value_theorem_target_packet_20260614.md",
        "ksy_y_conductor39_value_theorem_target_packet_rows=1/1",
    ),
)


@dataclass(frozen=True)
class TwistedH90ClosingAskRow:
    name: str
    ask: str
    candidate_command: str
    decision: str
    rejected: bool
    helper_only: bool
    conditional: bool
    source_theorem_closes: bool
    danger3_unblocked: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    continue_or_kill: str
    ok: bool


@dataclass(frozen=True)
class TwistedH90MinimalClosingAskPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    pure_degree6_norm_cancels: bool
    pair_sum_cancels: bool
    ratio_inverse_contract: bool
    h90_boundary_contract: bool
    period156_required_for_values: bool
    rows: tuple[TwistedH90ClosingAskRow, ...]
    row_count: int
    rejected_rows: int
    helper_only_rows: int
    conditional_rows: int
    source_theorem_closing_rows: int
    danger3_unblocked_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def candidate_command(
    name: str,
    *,
    pure_norm: bool = False,
    pair_sum: bool = False,
    signed_shadow: bool = False,
    ratio: bool = False,
    h90_boundary: bool = False,
    finite: bool = False,
    period156: bool = False,
    source: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_conductor39_twisted_descent_candidate_router_gate.py",
        "--candidate",
        f"--name {name}",
        "--theorem-body",
        "--degree6",
    ]
    if pure_norm:
        parts.append("--pure-norm")
    if pair_sum:
        parts.append("--pair-sum")
    if signed_shadow:
        parts.append("--signed-shadow")
    if ratio:
        parts.append("--ratio")
    if h90_boundary:
        parts.append("--h90-boundary")
    if finite:
        parts.append("--finite-or-divisor")
    if period156:
        parts.append("--period-156")
    if source:
        parts.append("--arithmetic-source")
    if danger3:
        parts.append("--danger3-framing")
    if extraction:
        parts.append("--extraction")
    if vpp:
        parts.append("--vpp-verified")
    return " ".join(parts)


def candidate(
    name: str,
    *,
    pure_norm: bool = False,
    pair_sum: bool = False,
    signed_shadow: bool = False,
    ratio: bool = False,
    h90_boundary: bool = False,
    finite: bool = False,
    period156: bool = False,
    source: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> TwistedDescentCandidate:
    return TwistedDescentCandidate(
        name=name,
        theorem_body_verified=True,
        uses_degree6_orbit=True,
        uses_pure_norm=pure_norm,
        uses_pair_sum=pair_sum,
        uses_signed_shadow=signed_shadow,
        uses_quotient_or_ratio=ratio,
        uses_hilbert90_boundary=h90_boundary,
        finite_value_or_divisor_theorem=finite,
        period156_context=period156,
        arithmetic_source_theorem=source,
        danger3_framing=danger3,
        extraction_to_A_x0=extraction,
        official_vpp=vpp,
    )


def row(
    name: str,
    *,
    ask: str,
    continue_or_kill: str,
    pure_norm: bool = False,
    pair_sum: bool = False,
    signed_shadow: bool = False,
    ratio: bool = False,
    h90_boundary: bool = False,
    finite: bool = False,
    period156: bool = False,
    source: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> TwistedH90ClosingAskRow:
    decision = classify_candidate(
        candidate(
            name,
            pure_norm=pure_norm,
            pair_sum=pair_sum,
            signed_shadow=signed_shadow,
            ratio=ratio,
            h90_boundary=h90_boundary,
            finite=finite,
            period156=period156,
            source=source,
            danger3=danger3,
            extraction=extraction,
            vpp=vpp,
        )
    )
    return TwistedH90ClosingAskRow(
        name=name,
        ask=ask,
        candidate_command=candidate_command(
            name,
            pure_norm=pure_norm,
            pair_sum=pair_sum,
            signed_shadow=signed_shadow,
            ratio=ratio,
            h90_boundary=h90_boundary,
            finite=finite,
            period156=period156,
            source=source,
            danger3=danger3,
            extraction=extraction,
            vpp=vpp,
        ),
        decision=decision.decision,
        rejected=decision.decision.startswith("reject_"),
        helper_only=decision.helper_only,
        conditional=decision.decision.startswith("conditional_"),
        source_theorem_closes=decision.source_stage_closed,
        danger3_unblocked=decision.danger3_unblocked,
        extraction_ready=decision.extraction_ready,
        submission_ready=decision.submission_ready,
        first_missing_or_falsifier=decision.first_missing_or_falsifier,
        continue_or_kill=continue_or_kill,
        ok=decision.ok,
    )


def ask_rows() -> tuple[TwistedH90ClosingAskRow, ...]:
    return (
        row(
            "pure_degree6_norm",
            ask="Can the ordinary degree-6 norm of the conductor-39 character word close the value stage?",
            pure_norm=True,
            continue_or_kill="kill; the six-conjugate additive norm cancels",
        ),
        row(
            "two_conjugate_pair_sum",
            ask="Can the two-conjugate pair W + Frob_p(W) produce the value payload?",
            pair_sum=True,
            continue_or_kill="kill; Frob_p(W)=-W so the pair sum is zero",
        ),
        row(
            "signed_shadow_only",
            ask="Can the signed three-conjugate shadow by itself close the source stage?",
            signed_shadow=True,
            continue_or_kill="keep only as orbit bookkeeping; ask for a finite value/divisor theorem",
        ),
        row(
            "ratio_or_h90_boundary_no_value",
            ask="Can a quotient/Hilbert-90 boundary without a value theorem close the source stage?",
            ratio=True,
            h90_boundary=True,
            continue_or_kill="keep as descent structure; ask for a finite value/divisor theorem",
        ),
        row(
            "twisted_value_no_period156",
            ask="Can a twisted ratio/H90 finite value without period-156 branch context be accepted?",
            ratio=True,
            h90_boundary=True,
            finite=True,
            continue_or_kill="conditional only; require support-period-156 context",
        ),
        row(
            "twisted_period156_payload_no_source",
            ask="Can a computed twisted period-156 payload close without an arithmetic source theorem?",
            ratio=True,
            h90_boundary=True,
            finite=True,
            period156=True,
            continue_or_kill="conditional only; keep as verifier data until sourced",
        ),
        row(
            "twisted_period156_source_no_danger3",
            ask="What is the smallest source-stage yes?",
            ratio=True,
            h90_boundary=True,
            finite=True,
            period156=True,
            source=True,
            continue_or_kill="continue; settle DANGER3 finite-identity/non-CM framing next",
        ),
        row(
            "danger3_framed_no_extraction",
            ask="After DANGER3 framing, what remains?",
            ratio=True,
            h90_boundary=True,
            finite=True,
            period156=True,
            source=True,
            danger3=True,
            continue_or_kill="continue; extract concrete A and x0",
        ),
        row(
            "verified_triple_boundary",
            ask="What is the only submission-ready terminal state?",
            ratio=True,
            h90_boundary=True,
            finite=True,
            period156=True,
            source=True,
            danger3=True,
            extraction=True,
            vpp=True,
            continue_or_kill="stop search; archive official vpp.py output and certificate",
        ),
    )


def profile_twisted_h90_minimal_closing_ask_packet() -> TwistedH90MinimalClosingAskPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = ask_rows()
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.rejected for row in rows)
    helper = sum(row.helper_only for row in rows)
    conditional = sum(row.conditional for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    danger3 = sum(row.danger3_unblocked for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    submission = sum(row.submission_ready for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 9
        and rejected == 2
        and helper == 2
        and conditional == 2
        and source_closing == 3
        and danger3 == 2
        and extraction == 1
        and submission == 1
        and decisions
        == (
            "reject_pure_degree6_norm_cancels",
            "reject_pair_sum_cancels",
            "helper_only_signed_orbit_shadow_value_theorem_missing",
            "helper_only_hilbert90_boundary_value_theorem_missing",
            "conditional_value_theorem_missing_period156_context",
            "conditional_finite_payload_without_source_theorem",
            "source_theorem_closed_policy_or_framing_missing",
            "danger3_unblocked_extraction_missing",
            "submission_ready_verified_triple",
        )
        and all(row.ok for row in rows)
    )
    return TwistedH90MinimalClosingAskPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        pure_degree6_norm_cancels=True,
        pair_sum_cancels=True,
        ratio_inverse_contract=True,
        h90_boundary_contract=True,
        period156_required_for_values=True,
        rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        helper_only_rows=helper,
        conditional_rows=conditional,
        source_theorem_closing_rows=source_closing,
        danger3_unblocked_rows=danger3,
        extraction_ready_rows=extraction,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_twisted_h90_minimal_closing_ask_packet()
    print("p25 KSY-y twisted/H90 minimal closing-ask packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("fixed_facts")
    print(f"  pure_degree6_norm_cancels={int(profile.pure_degree6_norm_cancels)}")
    print(f"  pair_sum_cancels={int(profile.pair_sum_cancels)}")
    print(f"  ratio_inverse_contract={int(profile.ratio_inverse_contract)}")
    print(f"  h90_boundary_contract={int(profile.h90_boundary_contract)}")
    print(f"  period156_required_for_values={int(profile.period156_required_for_values)}")
    print("ask_rows")
    for ask_row in profile.rows:
        print(
            "  "
            f"{ask_row.name}: decision={ask_row.decision} "
            f"rejected={int(ask_row.rejected)} "
            f"helper={int(ask_row.helper_only)} "
            f"conditional={int(ask_row.conditional)} "
            f"source_closed={int(ask_row.source_theorem_closes)} "
            f"danger3={int(ask_row.danger3_unblocked)} "
            f"extraction={int(ask_row.extraction_ready)} "
            f"submission={int(ask_row.submission_ready)}"
        )
        print(f"    ask={ask_row.ask}")
        print(f"    missing_or_falsifier={ask_row.first_missing_or_falsifier}")
        print(f"    next={ask_row.continue_or_kill}")
        print(f"    command={ask_row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  danger3_unblocked_rows={profile.danger3_unblocked_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  minimal_yes_is_twisted_ratio_h90_period156_source_theorem=1")
    print("  pure_norm_pair_sum_and_helper_only_shapes_do_not_close=1")
    print("  DANGER3_framing_extraction_and_official_vpp_remain_downstream=1")
    print(f"ksy_y_twisted_h90_minimal_closing_ask_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("twisted/H90 minimal closing-ask packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
