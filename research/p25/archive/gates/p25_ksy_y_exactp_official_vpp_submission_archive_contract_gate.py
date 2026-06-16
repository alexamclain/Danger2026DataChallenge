#!/usr/bin/env python3
"""Exact-P official vpp.py submission archive contract for p25.

The generic archive contract says what a verified `(p,A,x0)` triple needs.
This exact-P layer adds route provenance: if the triple is claimed to come
from the exact 75-atom product path, the exact-P source, bridge, surface, and
halving packets must also be archived.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_exactp_post_surface_halving_vpp_intake_gate import (
    profile_exactp_post_surface_halving_vpp_intake,
)
from p25_ksy_y_official_vpp_submission_archive_contract_gate import (
    EXPECTED_LOCAL_VPP_SHA256,
    P24_A,
    P24_CERT,
    P24_X0,
    OfficialVppArchiveCandidate,
    OfficialVppArchiveDecision,
    classify_candidate as classify_generic_archive_candidate,
    profile_vpp_submission_archive_contract,
    pp_verify,
    sha256_file,
    VPP,
)
from p25_ksy_y_cross_level_extraction_gap_gate import P25


REPO_ROOT = Path(__file__).resolve().parents[2]
RESEARCH = REPO_ROOT / "research" / "p25"

P24 = 1000000000000000000000007

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_exactp_post_surface_halving_vpp_intake_20260614.md",
        "ksy_y_exactp_post_surface_halving_vpp_intake_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_official_vpp_submission_archive_contract_20260614.md",
        "ksy_y_official_vpp_submission_archive_contract_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_20260614.md",
        "ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_exactp_post_bridge_x16_surface_intake_20260614.md",
        "ksy_y_exactp_post_bridge_x16_surface_intake_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExactPOfficialVppArchiveCandidate:
    name: str
    has_p: bool
    p_is_p25: bool
    has_A: bool
    has_x0: bool
    official_vpp_executed: bool
    official_vpp_stdout_true: bool
    command_logged: bool
    verifier_sha256_recorded: bool
    run_dir_or_source_recorded: bool
    environment_recorded: bool
    triple_file_archived: bool
    vpp_log_archived: bool
    lean_certificate_generated: bool
    lean_certificate_checked: bool
    exactp_source_or_policy_recorded: bool
    exactp_bridge_packet_archived: bool
    exactp_surface_packet_archived: bool
    exactp_halving_packet_archived: bool
    exactp_route_environment_crossref: bool
    current_evidence: bool


@dataclass(frozen=True)
class ExactPOfficialVppArchiveDecision:
    candidate: ExactPOfficialVppArchiveCandidate
    generic_decision: OfficialVppArchiveDecision
    decision: str
    concrete_triple_present: bool
    official_vpp_verified: bool
    generic_archive_complete: bool
    exactp_route_archive_complete: bool
    submission_ready: bool
    current_submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class ExactPVppSubmissionArchiveContract:
    dependency_markers_present: int
    dependency_markers_total: int
    exactp_halving_intake_ok: bool
    generic_archive_contract_ok: bool
    p: int
    local_vpp_sha256: str
    local_vpp_hash_expected: bool
    p24_vpp_true: bool
    p24_bad_rejected: bool
    p24_cert_present: bool
    rows: tuple[ExactPOfficialVppArchiveDecision, ...]
    row_count: int
    current_evidence_rows: int
    concrete_triple_rows: int
    official_vpp_verified_rows: int
    generic_archive_complete_rows: int
    exactp_route_archive_complete_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    rejected_rows: int
    incomplete_generic_archive_rows: int
    incomplete_exactp_archive_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def generic_candidate(candidate: ExactPOfficialVppArchiveCandidate) -> OfficialVppArchiveCandidate:
    return OfficialVppArchiveCandidate(
        name=candidate.name,
        has_p=candidate.has_p,
        p_is_p25=candidate.p_is_p25,
        has_A=candidate.has_A,
        has_x0=candidate.has_x0,
        official_vpp_executed=candidate.official_vpp_executed,
        official_vpp_stdout_true=candidate.official_vpp_stdout_true,
        command_logged=candidate.command_logged,
        verifier_sha256_recorded=candidate.verifier_sha256_recorded,
        run_dir_or_source_recorded=candidate.run_dir_or_source_recorded,
        environment_recorded=candidate.environment_recorded,
        triple_file_archived=candidate.triple_file_archived,
        vpp_log_archived=candidate.vpp_log_archived,
        lean_certificate_generated=candidate.lean_certificate_generated,
        lean_certificate_checked=candidate.lean_certificate_checked,
        current_evidence=candidate.current_evidence,
    )


def classify_candidate(candidate: ExactPOfficialVppArchiveCandidate) -> ExactPOfficialVppArchiveDecision:
    generic = classify_generic_archive_candidate(generic_candidate(candidate))
    if generic.decision != "submission_archive_complete":
        incomplete_generic = generic.official_vpp_verified and not generic.archive_complete
        return ExactPOfficialVppArchiveDecision(
            candidate=candidate,
            generic_decision=generic,
            decision=generic.decision,
            concrete_triple_present=generic.concrete_triple_present,
            official_vpp_verified=generic.official_vpp_verified,
            generic_archive_complete=generic.archive_complete,
            exactp_route_archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier=generic.first_missing_or_falsifier,
            next_action=(
                "complete the generic official-vpp archive before exact-P route provenance"
                if incomplete_generic
                else generic.next_action
            ),
            ok=generic.ok,
        )

    exactp_requirements = (
        (candidate.exactp_source_or_policy_recorded, "exact-P source theorem, policy answer, or production-hit bypass note"),
        (candidate.exactp_bridge_packet_archived, "exact-P X_1(8112) bridge packet"),
        (candidate.exactp_surface_packet_archived, "exact-P X_1(16) surface packet"),
        (candidate.exactp_halving_packet_archived, "exact-P halving/vpp packet"),
        (candidate.exactp_route_environment_crossref, "cross-reference from exact-P route packets to archive environment"),
    )
    for present, missing in exactp_requirements:
        if not present:
            decision = {
                "exact-P source theorem, policy answer, or production-hit bypass note": "exactp_archive_incomplete_source_or_policy_missing",
                "exact-P X_1(8112) bridge packet": "exactp_archive_incomplete_bridge_packet_missing",
                "exact-P X_1(16) surface packet": "exactp_archive_incomplete_surface_packet_missing",
                "exact-P halving/vpp packet": "exactp_archive_incomplete_halving_packet_missing",
                "cross-reference from exact-P route packets to archive environment": "exactp_archive_incomplete_environment_crossref_missing",
            }[missing]
            return ExactPOfficialVppArchiveDecision(
                candidate=candidate,
                generic_decision=generic,
                decision=decision,
                concrete_triple_present=True,
                official_vpp_verified=True,
                generic_archive_complete=True,
                exactp_route_archive_complete=False,
                submission_ready=False,
                current_submission_ready=False,
                first_missing_or_falsifier=missing,
                next_action="complete exact-P route archive provenance before calling this route finished",
                ok=True,
            )

    return ExactPOfficialVppArchiveDecision(
        candidate=candidate,
        generic_decision=generic,
        decision="exactp_submission_archive_complete",
        concrete_triple_present=True,
        official_vpp_verified=True,
        generic_archive_complete=True,
        exactp_route_archive_complete=True,
        submission_ready=True,
        current_submission_ready=candidate.current_evidence,
        first_missing_or_falsifier="none",
        next_action="submit/report the p25 triple and preserve the exact-P archive bundle",
        ok=True,
    )


def candidate(name: str, **overrides: bool) -> ExactPOfficialVppArchiveCandidate:
    base = {
        "has_p": True,
        "p_is_p25": True,
        "has_A": True,
        "has_x0": True,
        "official_vpp_executed": True,
        "official_vpp_stdout_true": True,
        "command_logged": True,
        "verifier_sha256_recorded": True,
        "run_dir_or_source_recorded": True,
        "environment_recorded": True,
        "triple_file_archived": True,
        "vpp_log_archived": True,
        "lean_certificate_generated": True,
        "lean_certificate_checked": True,
        "exactp_source_or_policy_recorded": True,
        "exactp_bridge_packet_archived": True,
        "exactp_surface_packet_archived": True,
        "exactp_halving_packet_archived": True,
        "exactp_route_environment_crossref": True,
        "current_evidence": False,
    }
    base.update(overrides)
    return ExactPOfficialVppArchiveCandidate(name=name, **base)


def regression_candidates() -> tuple[ExactPOfficialVppArchiveCandidate, ...]:
    return (
        candidate("missing_triple", has_A=False, has_x0=False),
        candidate("concrete_triple_vpp_not_run", official_vpp_executed=False, official_vpp_stdout_true=False),
        candidate("concrete_triple_vpp_false", official_vpp_stdout_true=False),
        candidate("generic_archive_command_missing", command_logged=False),
        candidate("generic_archive_lean_unchecked", lean_certificate_checked=False),
        candidate("exactp_source_or_policy_missing", exactp_source_or_policy_recorded=False),
        candidate("exactp_bridge_packet_missing", exactp_bridge_packet_archived=False),
        candidate("exactp_surface_packet_missing", exactp_surface_packet_archived=False),
        candidate("exactp_halving_packet_missing", exactp_halving_packet_archived=False),
        candidate("exactp_environment_crossref_missing", exactp_route_environment_crossref=False),
        candidate("exactp_complete_archive_boundary"),
    )


def profile_exactp_vpp_submission_archive_contract() -> ExactPVppSubmissionArchiveContract:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    exactp_halving = profile_exactp_post_surface_halving_vpp_intake()
    generic_archive = profile_vpp_submission_archive_contract()
    vpp_sha = sha256_file(VPP)
    p24_true = pp_verify(P24, P24_A, P24_X0)
    p24_bad = not pp_verify(P24, P24_A, P24_X0 + 1)
    rows = tuple(classify_candidate(row) for row in regression_candidates())
    decisions = tuple(row.decision for row in rows)
    expected = (
        "reject_missing_concrete_p25_triple",
        "concrete_triple_official_vpp_missing",
        "reject_official_vpp_not_true",
        "archive_incomplete_command_missing",
        "lean_certificate_unchecked",
        "exactp_archive_incomplete_source_or_policy_missing",
        "exactp_archive_incomplete_bridge_packet_missing",
        "exactp_archive_incomplete_surface_packet_missing",
        "exactp_archive_incomplete_halving_packet_missing",
        "exactp_archive_incomplete_environment_crossref_missing",
        "exactp_submission_archive_complete",
    )
    current = sum(row.candidate.current_evidence for row in rows)
    concrete = sum(row.concrete_triple_present for row in rows)
    vpp_verified = sum(row.official_vpp_verified for row in rows)
    generic_complete = sum(row.generic_archive_complete for row in rows)
    exactp_complete = sum(row.exactp_route_archive_complete for row in rows)
    submission = sum(row.submission_ready for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    incomplete_generic = sum(
        row.decision.startswith("archive_incomplete_")
        or row.decision in {"vpp_verified_lean_certificate_missing", "lean_certificate_unchecked"}
        for row in rows
    )
    incomplete_exactp = sum(row.decision.startswith("exactp_archive_incomplete_") for row in rows)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and exactp_halving.row_ok
        and generic_archive.row_ok
        and P25 == 10**25 + 13
        and vpp_sha == EXPECTED_LOCAL_VPP_SHA256
        and p24_true
        and p24_bad
        and P24_CERT.exists()
        and len(rows) == 11
        and current == 0
        and concrete == 10
        and vpp_verified == 8
        and generic_complete == 6
        and exactp_complete == 1
        and submission == 1
        and current_submission == 0
        and rejected == 2
        and incomplete_generic == 2
        and incomplete_exactp == 5
        and decisions == expected
        and all(row.ok for row in rows)
    )
    return ExactPVppSubmissionArchiveContract(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        exactp_halving_intake_ok=exactp_halving.row_ok,
        generic_archive_contract_ok=generic_archive.row_ok,
        p=P25,
        local_vpp_sha256=vpp_sha,
        local_vpp_hash_expected=vpp_sha == EXPECTED_LOCAL_VPP_SHA256,
        p24_vpp_true=p24_true,
        p24_bad_rejected=p24_bad,
        p24_cert_present=P24_CERT.exists(),
        rows=rows,
        row_count=len(rows),
        current_evidence_rows=current,
        concrete_triple_rows=concrete,
        official_vpp_verified_rows=vpp_verified,
        generic_archive_complete_rows=generic_complete,
        exactp_route_archive_complete_rows=exactp_complete,
        submission_boundary_rows=submission,
        current_submission_ready_rows=current_submission,
        rejected_rows=rejected,
        incomplete_generic_archive_rows=incomplete_generic,
        incomplete_exactp_archive_rows=incomplete_exactp,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_exactp_vpp_submission_archive_contract()
    print("p25 KSY-y exact-P official vpp submission archive contract gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  exactp_halving_intake_ok={int(profile.exactp_halving_intake_ok)}")
    print(f"  generic_archive_contract_ok={int(profile.generic_archive_contract_ok)}")
    print("verifier_regression")
    print(f"  p={profile.p}")
    print(f"  local_vpp_sha256={profile.local_vpp_sha256}")
    print(f"  local_vpp_hash_expected={int(profile.local_vpp_hash_expected)}")
    print(f"  p24_vpp_true={int(profile.p24_vpp_true)}")
    print(f"  p24_bad_rejected={int(profile.p24_bad_rejected)}")
    print(f"  p24_cert_present={int(profile.p24_cert_present)}")
    print("archive_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.candidate.name}: decision={row.decision} "
            f"generic={row.generic_decision.decision} "
            f"triple={int(row.concrete_triple_present)} "
            f"vpp={int(row.official_vpp_verified)} "
            f"generic_archive={int(row.generic_archive_complete)} "
            f"exactp_archive={int(row.exactp_route_archive_complete)} "
            f"submission={int(row.submission_ready)} "
            f"current={int(row.current_submission_ready)}"
        )
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  concrete_triple_rows={profile.concrete_triple_rows}")
    print(f"  official_vpp_verified_rows={profile.official_vpp_verified_rows}")
    print(f"  generic_archive_complete_rows={profile.generic_archive_complete_rows}")
    print(f"  exactp_route_archive_complete_rows={profile.exactp_route_archive_complete_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  incomplete_generic_archive_rows={profile.incomplete_generic_archive_rows}")
    print(f"  incomplete_exactp_archive_rows={profile.incomplete_exactp_archive_rows}")
    print("interpretation")
    print("  exactP_route_archive_extends_but_does_not_replace_official_vpp_archive=1")
    print("  exactP_source_bridge_surface_halving_packets_must_be_archived=1")
    print("  production_hit_bypass_must_be_explicit_if_no_exactP_source_theorem=1")
    print("  complete_archive_boundary_is_not_current_evidence=1")
    print(
        "ksy_y_exactp_official_vpp_submission_archive_contract_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("exact-P official vpp submission archive contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
