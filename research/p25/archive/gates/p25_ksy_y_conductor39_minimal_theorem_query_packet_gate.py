#!/usr/bin/env python3
"""Minimal conductor-39 theorem-query packet for the p25 moonshot.

The subsqrt route packet makes the accepted finite payloads operational.  The
smallest theorem-source target now lives one step upstream: a theorem must turn
the certified mixed X_1(39) source U_chi/W/H0 into a finite-field value or
divisor identity.  This packet gives that source theorem its own compact query
surface and first falsifiers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_conductor39_source_theorem_intake_gate import (
    Conductor39SourceTheoremClaim,
    classify_claim,
)


REPO = Path(__file__).resolve().parents[2]
SOURCE_CERTIFICATE_STACK = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_conductor39_source_certificate_stack_20260614.md"
)
SOURCE_CERTIFICATE_STACK_MARKER = (
    "ksy_y_conductor39_source_certificate_stack_rows=1/1"
)
SOURCE_THEOREM_INTAKE = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_conductor39_source_theorem_intake_20260614.md"
)
SOURCE_THEOREM_INTAKE_MARKER = (
    "ksy_y_conductor39_source_theorem_intake_rows=1/1"
)
ARITHMETIC_PRODUCER_ROUTE_PACKET = (
    REPO
    / "research"
    / "p25"
    / "p25_ksy_y_subsqrt_arithmetic_producer_route_packet_20260614.md"
)
ARITHMETIC_PRODUCER_ROUTE_MARKER = (
    "ksy_y_subsqrt_arithmetic_producer_route_packet_rows=1/1"
)


@dataclass(frozen=True)
class MinimalTheoremQueryRow:
    name: str
    theorem_query: str
    candidate_command: str
    expected_decision: str
    source_identified: bool
    source_theorem_closes: bool
    submission_ready: bool
    first_missing_clause: str
    first_falsifier: str
    continue_recommendation: str
    ok: bool


@dataclass(frozen=True)
class Conductor39MinimalTheoremQueryPacket:
    source_certificate_stack_ok: bool
    source_theorem_intake_ok: bool
    arithmetic_producer_route_ok: bool
    query_rows: tuple[MinimalTheoremQueryRow, ...]
    query_count: int
    candidate_commands: int
    source_identified_rows: int
    source_theorem_closing_rows: int
    rejected_rows: int
    conditional_rows: int
    helper_only_rows: int
    submission_ready_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def candidate_command(
    name: str,
    *,
    source_object: str = "U_chi",
    theorem_body: bool = True,
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    sparse_formal: bool = False,
    proper_axis_projection: bool = False,
    additive_separated: bool = False,
    yang_lift: bool = True,
    descent: bool = True,
    output_kind: str = "source-object",
    finite_or_divisor: bool = False,
    period_156: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> str:
    parts = [
        "PYTHONPATH=research/p25",
        "PYTHONDONTWRITEBYTECODE=1",
        "python3",
        "research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py",
        "--candidate",
        f"--name {name}",
        f"--source-object {source_object}",
        f"--output-kind {output_kind}",
    ]
    if theorem_body:
        parts.append("--theorem-body")
    if emits:
        parts.append("--emits-conductor39")
    if mixed:
        parts.append("--mixed-tensor")
    if legal:
        parts.append("--legal-unit")
    if sparse_formal:
        parts.append("--sparse-formal")
    if proper_axis_projection:
        parts.append("--proper-axis-projection")
    if additive_separated:
        parts.append("--additive-separated")
    if yang_lift:
        parts.append("--yang-lift")
    if descent:
        parts.append("--descent")
    if finite_or_divisor:
        parts.append("--finite-or-divisor")
    if period_156:
        parts.append("--period-156")
    if danger3:
        parts.append("--danger3-framing")
    if extraction:
        parts.append("--extraction")
    if vpp:
        parts.append("--vpp-verified")
    return " ".join(parts)


def claim(
    name: str,
    *,
    source_object: str = "U_chi",
    theorem_body: bool = True,
    emits: bool = True,
    mixed: bool = True,
    legal: bool = True,
    sparse_formal: bool = False,
    proper_axis_projection: bool = False,
    additive_separated: bool = False,
    yang_lift: bool = True,
    descent: bool = True,
    output_kind: str = "source-object",
    finite_or_divisor: bool = False,
    period_156: bool = False,
    danger3: bool = False,
    extraction: bool = False,
    vpp: bool = False,
) -> Conductor39SourceTheoremClaim:
    return Conductor39SourceTheoremClaim(
        name=name,
        theorem_body_verified=theorem_body,
        source_object=source_object,
        emits_conductor39_object=emits,
        preserves_mixed_tensor=mixed,
        yang_yu_legal_unit=legal,
        sparse_formal_gauge_only=sparse_formal,
        proper_axis_or_projection_only=proper_axis_projection,
        additive_separated=additive_separated,
        yang_distribution_to_507=yang_lift,
        frobenius_or_hilbert90_descent=descent,
        output_kind=output_kind,
        finite_field_identity_or_divisor_theorem=finite_or_divisor,
        period_156_context=period_156,
        danger3_framing=danger3,
        extraction_to_A_x0=extraction,
        concrete_vpp_verified_triple=vpp,
    )


def query_rows() -> tuple[MinimalTheoremQueryRow, ...]:
    specs = (
        (
            "certified_source_object_only",
            "Does the snippet only identify U_chi/W/H0 and Yang lift, without a value/divisor theorem?",
            dict(),
            "source object is useful but still lacks a finite-field value/divisor theorem",
            "claim stops at source certification",
            "continue only if upgraded to value/divisor theorem",
        ),
        (
            "period_value_without_period156",
            "Does the snippet give a finite value for the source but omit support-period branch control?",
            dict(output_kind="value", finite_or_divisor=True, period_156=False),
            "finite values need period-156 branch/root/telescoping context",
            "ambient or bare value leaves branch ambiguity",
            "ask for period-156 fixedness/telescoping",
        ),
        (
            "period156_value_policy_missing",
            "Does the snippet give a finite-field value identity with the period-156 context?",
            dict(output_kind="value", finite_or_divisor=True, period_156=True),
            "this closes the conductor-39 source theorem stage, upstream of DANGER3 policy",
            "DANGER3 finite-identity/non-CM framing still absent",
            "route to DANGER3 framing and cross-level extraction",
        ),
        (
            "divisor_theorem_policy_missing",
            "Does the snippet give a divisor/additive identity for U_chi/W/H0?",
            dict(output_kind="divisor-additive", finite_or_divisor=True),
            "this closes the conductor-39 source theorem stage, upstream of DANGER3 policy",
            "DANGER3 finite-identity/non-CM framing still absent",
            "route to DANGER3 framing and cross-level extraction",
        ),
        (
            "formal_sparse_gauge_no_boundary",
            "Is the claim only a sparse one-coset H0 gauge without a Hilbert-90 or ratio boundary?",
            dict(source_object="legal_sparse_h90_gauge", sparse_formal=True, descent=False, output_kind="source-object"),
            "formal sparse gauges are not theorem closures without the boundary",
            "sparse gauge has no Hilbert-90 or ratio boundary",
            "kill as a standalone producer",
        ),
        (
            "prime13_projection_shadow",
            "Does the claim collapse to a prime-13/projection or additive-separated source?",
            dict(source_object="projection", emits=False, mixed=False, legal=False, proper_axis_projection=True, yang_lift=False, descent=False, output_kind="divisor-additive"),
            "projection shadows erase the mixed chi_3 tensor chi_13 source",
            "proper axis/projection only",
            "kill unless the mixed tensor is restored",
        ),
        (
            "extraction_ready_unverified",
            "Has the conductor-39 theorem route reached concrete A,x0 but not official vpp.py?",
            dict(output_kind="divisor-additive", finite_or_divisor=True, danger3=True, extraction=True),
            "ready to extract and verify a concrete triple, still not a submission",
            "official vpp.py verification missing",
            "run official vpp.py and archive certificate output",
        ),
        (
            "verified_pomerance_triple",
            "Has the theorem route produced a concrete p25 triple verified by official vpp.py?",
            dict(output_kind="divisor-additive", finite_or_divisor=True, danger3=True, extraction=True, vpp=True),
            "verified triple is the only submission-ready conductor-39 endpoint",
            "none",
            "archive and submit",
        ),
    )
    rows: list[MinimalTheoremQueryRow] = []
    for name, query_text, kwargs, expected_note, falsifier, recommendation in specs:
        c = claim(name, **kwargs)
        decision = classify_claim(c)
        cmd = candidate_command(name, **kwargs)
        rows.append(
            MinimalTheoremQueryRow(
                name=name,
                theorem_query=query_text,
                candidate_command=cmd,
                expected_decision=decision.decision,
                source_identified=decision.conductor39_source_identified,
                source_theorem_closes=decision.theorem_source_closed,
                submission_ready=decision.submission_ready,
                first_missing_clause=decision.first_missing_clause,
                first_falsifier=falsifier,
                continue_recommendation=recommendation,
                ok=decision.row_ok and bool(expected_note),
            )
        )
    return tuple(rows)


def profile_minimal_theorem_query_packet() -> Conductor39MinimalTheoremQueryPacket:
    stack_ok = marker_present(
        SOURCE_CERTIFICATE_STACK,
        SOURCE_CERTIFICATE_STACK_MARKER,
    )
    intake_ok = marker_present(
        SOURCE_THEOREM_INTAKE,
        SOURCE_THEOREM_INTAKE_MARKER,
    )
    producer_ok = marker_present(
        ARITHMETIC_PRODUCER_ROUTE_PACKET,
        ARITHMETIC_PRODUCER_ROUTE_MARKER,
    )
    rows = query_rows()
    candidate_commands = sum("conductor39_source_theorem_intake_gate.py" in row.candidate_command for row in rows)
    source_identified = sum(row.source_identified for row in rows)
    source_closing = sum(row.source_theorem_closes for row in rows)
    rejected = sum(row.expected_decision.startswith("reject_") for row in rows)
    conditional = sum(row.expected_decision.startswith("conditional_") for row in rows)
    helper_only = sum(row.expected_decision == "conductor39_source_identified_value_or_divisor_theorem_missing" for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    row_ok = (
        stack_ok
        and intake_ok
        and producer_ok
        and len(rows) == 8
        and candidate_commands == 8
        and source_identified == 6
        and source_closing == 4
        and rejected == 2
        and conditional == 1
        and helper_only == 1
        and submission_ready == 1
        and tuple(row.expected_decision for row in rows)
        == (
            "conductor39_source_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "reject_formal_sparse_gauge_without_boundary",
            "reject_loses_mixed_tensor",
            "ready_to_extract_and_verify_concrete_triple",
            "submission_ready_verified_triple",
        )
        and all(row.ok for row in rows)
    )
    return Conductor39MinimalTheoremQueryPacket(
        source_certificate_stack_ok=stack_ok,
        source_theorem_intake_ok=intake_ok,
        arithmetic_producer_route_ok=producer_ok,
        query_rows=rows,
        query_count=len(rows),
        candidate_commands=candidate_commands,
        source_identified_rows=source_identified,
        source_theorem_closing_rows=source_closing,
        rejected_rows=rejected,
        conditional_rows=conditional,
        helper_only_rows=helper_only,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_minimal_theorem_query_packet()
    print("p25 KSY-y conductor-39 minimal theorem-query packet gate")
    print("dependencies")
    print(f"  source_certificate_stack_ok={int(profile.source_certificate_stack_ok)}")
    print(f"  source_theorem_intake_ok={int(profile.source_theorem_intake_ok)}")
    print(f"  arithmetic_producer_route_ok={int(profile.arithmetic_producer_route_ok)}")
    print("query_rows")
    for row in profile.query_rows:
        print(
            "  "
            f"{row.name}: decision={row.expected_decision} "
            f"source={int(row.source_identified)} "
            f"closes={int(row.source_theorem_closes)} "
            f"submission={int(row.submission_ready)} "
            f"missing={row.first_missing_clause}"
        )
        print(f"    query={row.theorem_query}")
        print(f"    falsifier={row.first_falsifier}")
        print(f"    recommendation={row.continue_recommendation}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  query_count={profile.query_count}")
    print(f"  candidate_commands={profile.candidate_commands}")
    print(f"  source_identified_rows={profile.source_identified_rows}")
    print(f"  source_theorem_closing_rows={profile.source_theorem_closing_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  helper_only_rows={profile.helper_only_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  smallest_live_source_query_is_U_chi_or_W_or_H0_value_divisor_theorem=1")
    print("  source_certification_without_value_or_divisor_theorem_is_helper_only=1")
    print("  formal_sparse_gauge_and_prime_projection_shortcuts_are_rejected=1")
    print("  conductor39_source_theorem_closure_still_needs_DANGER3_extraction_and_vpp=1")
    print(f"ksy_y_conductor39_minimal_theorem_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 minimal theorem-query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
