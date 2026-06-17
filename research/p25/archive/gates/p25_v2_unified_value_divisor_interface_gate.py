#!/usr/bin/env python3
"""V2 interface for the missing unified value/divisor theorem.

The first-pass target is now fixed.  This gate records exactly what kind of
theorem would move the project: a finite value/divisor identity for one legal
support-156 product, with the right boundary and period context, emitted by an
arithmetic source theorem.  It also records common near misses that do not
close source stage.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class TheoremInterfaceRow:
    name: str
    kind: str
    target: str
    accepted_payload: str
    decision: str
    closes_source_stage: bool
    feeds_unified_target: bool
    still_needs_danger3: bool
    still_needs_extraction: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class UnifiedValueDivisorInterface:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[TheoremInterfaceRow, ...]
    support_period: int
    h90_support: int
    positive_factor_count: int
    negative_factor_count: int
    target_rows: int
    support_root_gcd_fp_star: int
    ambient_root_gcd_fp_star: int
    evidence_markers_ok: int
    source_closing_rows: int
    repair_or_rejected_rows: int
    downstream_rows: int
    current_source_theorem_rows: int
    current_submission_ready_rows: int
    preferred_next_ask: str
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_target",
            "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
            "p25_v2_h0_conductor39_unified_target_rows=1/1",
        ),
        marker(
            "source_theorem_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "p25_v2_unified_source_theorem_gap_rows=1/1",
        ),
        marker(
            "submission_extraction",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "h0_interface",
            "research/p25/evidence/p25_v2_h0_theorem_interface_contract_20260616.md",
            "All nine gates returned their expected `rows=1/1` markers",
        ),
        marker(
            "conductor39_interface",
            "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
            "All seven gates returned their expected `rows=1/1` markers",
        ),
        marker(
            "exactp_spine",
            "research/p25/evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
            "p25_v2_exactp_to_unified_target_spine_rows=1/1",
        ),
        marker(
            "orbit_minimality",
            "research/p25/evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md",
            "p25_v2_conductor39_doubling_orbit_minimality_rows=1/1",
        ),
        marker(
            "first_pass_triage_zero",
            "research/p25/evidence/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_20260614.md",
            "current_source_theorem_rows       = 0",
        ),
        marker(
            "h90_value_intake",
            "research/p25/archive/notes/p25_ksy_y_h90_value_theorem_intake_20260614.md",
            "ksy_y_h90_value_theorem_intake_rows=1/1",
        ),
    )


def interface_rows() -> tuple[TheoremInterfaceRow, ...]:
    return (
        TheoremInterfaceRow(
            name="unified_divisor_additive_theorem",
            kind="accepted_source_closer",
            target="one legal support-156 H0/conductor-39 product",
            accepted_payload=(
                "finite divisor/additive identity with Hilbert-90 boundary "
                "(1-Frob_p)H = Norm_156(Y_507), emitted by an arithmetic source theorem"
            ),
            decision="source_theorem_closed_policy_or_framing_missing",
            closes_source_stage=True,
            feeds_unified_target=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="unified_period156_value_theorem",
            kind="accepted_source_closer",
            target="one legal support-156 H0/conductor-39 product",
            accepted_payload=(
                "finite value identity with period-156 branch/root/telescoping "
                "context and boundary Norm_156(Y_507), emitted by an arithmetic source theorem"
            ),
            decision="source_theorem_closed_policy_or_framing_missing",
            closes_source_stage=True,
            feeds_unified_target=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 finite-identity/non-CM framing",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="exactp_upstream_theorem",
            kind="accepted_stronger_upstream_closer",
            target="compact exact-P C,D,K,orientation or period-156 theta2 payload",
            accepted_payload=(
                "challenge-legal exact-P arithmetic theorem feeding the 75->300->12->312->156 bridge"
            ),
            decision="source_theorem_closed_policy_or_framing_missing",
            closes_source_stage=True,
            feeds_unified_target=True,
            still_needs_danger3=True,
            still_needs_extraction=True,
            submission_ready=False,
            first_missing_or_falsifier="DANGER3 framing and extraction after upstream theorem",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="source_legality_only",
            kind="repair_or_reject",
            target="H0 or conductor-39 source word",
            accepted_payload="source certification, ray-class generation, or unit vocabulary only",
            decision="live_target_identified_value_or_divisor_theorem_missing",
            closes_source_stage=False,
            feeds_unified_target=False,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="finite value/divisor theorem",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="boundary_only",
            kind="repair_or_reject",
            target="Norm_156(Y_507) or H90 boundary",
            accepted_payload="boundary or period norm without finite value/divisor identity",
            decision="live_target_identified_value_or_divisor_theorem_missing",
            closes_source_stage=False,
            feeds_unified_target=False,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="finite value/divisor identity for the legal product",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="value_without_period156_context",
            kind="repair_or_reject",
            target="ambient value claim",
            accepted_payload="value theorem without support-period branch/root/telescoping data",
            decision="conditional_missing_period_156_context",
            closes_source_stage=False,
            feeds_unified_target=False,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="period-156 context; ambient 780 route has mu_11 ambiguity",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="formal_one_coset_or_projection",
            kind="repair_or_reject",
            target="formal one-coset H, prime-axis projection, or C169 projection",
            accepted_payload="nearby product with wrong legality or lost mixed tensor",
            decision="reject_illegal_or_insufficient_target",
            closes_source_stage=False,
            feeds_unified_target=False,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="legal support-156 product preserving H0/conductor-39 mixed structure",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="seed_or_proper_suborbit_shortcut",
            kind="repair_or_reject",
            target="E_7/E_1 seed or proper doubling suborbit",
            accepted_payload="short source shortcut without full 12-step norm or legality repair",
            decision="reject_not_standalone_X1_39_unit",
            closes_source_stage=False,
            feeds_unified_target=False,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="full 12-step doubling norm or explicit Yang/Yu legality repair",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="finite_payload_without_source",
            kind="repair_or_reject",
            target="computed finite verifier payload",
            accepted_payload="exact finite target data with no arithmetic source theorem",
            decision="conditional_finite_identity_without_arithmetic_source",
            closes_source_stage=False,
            feeds_unified_target=True,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="post_source_theorem_no_extraction",
            kind="downstream",
            target="source theorem after DANGER3 framing",
            accepted_payload="theorem-stage win with no concrete A,x0 extraction",
            decision="danger3_unblocked_extraction_missing",
            closes_source_stage=True,
            feeds_unified_target=True,
            still_needs_danger3=False,
            still_needs_extraction=True,
            submission_ready=False,
            first_missing_or_falsifier="same-j X1(8112), practical X1(16), halving/direct x0, vpp.py",
            ok=True,
        ),
        TheoremInterfaceRow(
            name="official_vpp_verified_triple",
            kind="downstream",
            target="concrete p25 (p,A,x0)",
            accepted_payload="official src/vpp.py verifies the concrete triple",
            decision="submission_ready",
            closes_source_stage=True,
            feeds_unified_target=True,
            still_needs_danger3=False,
            still_needs_extraction=False,
            submission_ready=True,
            first_missing_or_falsifier="none",
            ok=True,
        ),
    )


def profile_unified_value_divisor_interface() -> UnifiedValueDivisorInterface:
    markers = evidence_markers()
    rows = interface_rows()
    marker_count = sum(item.ok for item in markers)
    source_closing = sum(row.closes_source_stage and row.kind.startswith("accepted") for row in rows)
    repairs = sum(row.kind == "repair_or_reject" for row in rows)
    downstream = sum(row.kind == "downstream" for row in rows)
    current_source = 0
    current_submission = 0
    row_ok = (
        len(markers) == 9
        and marker_count == 9
        and len(rows) == 11
        and source_closing == 3
        and repairs == 6
        and downstream == 2
        and current_source == 0
        and current_submission == 0
        and all(row.ok for row in rows)
        and tuple(row.decision for row in rows)
        == (
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "live_target_identified_value_or_divisor_theorem_missing",
            "live_target_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "reject_illegal_or_insufficient_target",
            "reject_not_standalone_X1_39_unit",
            "conditional_finite_identity_without_arithmetic_source",
            "danger3_unblocked_extraction_missing",
            "submission_ready",
        )
    )
    return UnifiedValueDivisorInterface(
        evidence_markers=markers,
        rows=rows,
        support_period=156,
        h90_support=156,
        positive_factor_count=78,
        negative_factor_count=78,
        target_rows=4,
        support_root_gcd_fp_star=1,
        ambient_root_gcd_fp_star=11,
        evidence_markers_ok=marker_count,
        source_closing_rows=source_closing,
        repair_or_rejected_rows=repairs,
        downstream_rows=downstream,
        current_source_theorem_rows=current_source,
        current_submission_ready_rows=current_submission,
        preferred_next_ask=(
            "finite divisor/additive theorem, or period-156 value theorem, for one "
            "legal support-156 H0/conductor-39 product with Norm_156(Y_507) boundary"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_unified_value_divisor_interface()
    print("p25 v2 unified value/divisor theorem interface gate")
    print("evidence_markers")
    for marker in profile.evidence_markers:
        print(f"  {marker.name}: ok={int(marker.ok)} path={marker.path}")
    print("fixed_target")
    print(f"  support_period={profile.support_period}")
    print(f"  h90_support={profile.h90_support}")
    print(f"  positive_factor_count={profile.positive_factor_count}")
    print(f"  negative_factor_count={profile.negative_factor_count}")
    print(f"  target_rows={profile.target_rows}")
    print(f"  support_root_gcd_Fp_star={profile.support_root_gcd_fp_star}")
    print(f"  ambient_root_gcd_Fp_star={profile.ambient_root_gcd_fp_star}")
    print("interface_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: kind={row.kind} decision={row.decision} "
            f"closes_source={int(row.closes_source_stage)} "
            f"feeds_unified={int(row.feeds_unified_target)} "
            f"danger3={int(row.still_needs_danger3)} "
            f"extraction={int(row.still_needs_extraction)} "
            f"submission={int(row.submission_ready)}"
        )
        print(f"    target={row.target}")
        print(f"    payload={row.accepted_payload}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  repair_or_rejected_rows={profile.repair_or_rejected_rows}")
    print(f"  downstream_rows={profile.downstream_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print("interpretation")
    print("  divisor_additive_route_is_preferred_because_it_avoids_value_branch_ambiguity=1")
    print("  period156_value_route_is_acceptable_with_branch_root_telescoping_context=1")
    print("  source_legality_boundary_selector_and_seed_shortcuts_are_not_closers=1")
    print(f"  preferred_next_ask={profile.preferred_next_ask}")
    print(f"p25_v2_unified_value_divisor_interface_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("unified value/divisor theorem interface regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
