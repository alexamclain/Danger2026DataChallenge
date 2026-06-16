#!/usr/bin/env python3
"""Official vpp.py submission archive contract for p25."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_cross_level_extraction_gap_gate import P25
from p25_ksy_y_post_surface_halving_vpp_intake_gate import (
    profile_post_surface_halving_vpp_intake,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
RESEARCH = REPO_ROOT / "research" / "p25"
P24_CERT = REPO_ROOT / "data" / "p24" / "p24_cert.lean"
VPP = SRC / "vpp.py"

sys.path.insert(0, str(SRC))
from vpp import pp_verify  # noqa: E402


P24 = 1000000000000000000000007
P24_A = 38923582678463553756710
P24_X0 = 843367907077058108520461
EXPECTED_LOCAL_VPP_SHA256 = "e52b5d00cdd7c1a2f689528026570fe8917537c931130bf32cd2a51838cde3d6"


DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_post_surface_halving_vpp_intake_20260614.md",
        "ksy_y_post_surface_halving_vpp_intake_rows=1/1",
    ),
)


@dataclass(frozen=True)
class OfficialVppArchiveCandidate:
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
    current_evidence: bool


@dataclass(frozen=True)
class OfficialVppArchiveDecision:
    candidate: OfficialVppArchiveCandidate
    decision: str
    concrete_triple_present: bool
    official_vpp_verified: bool
    archive_complete: bool
    submission_ready: bool
    current_submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class VppSubmissionArchiveContract:
    dependency_markers_present: int
    dependency_markers_total: int
    post_surface_halving_ok: bool
    p: int
    local_vpp_sha256: str
    local_vpp_hash_expected: bool
    p24_vpp_true: bool
    p24_bad_rejected: bool
    p24_cert_present: bool
    rows: tuple[OfficialVppArchiveDecision, ...]
    row_count: int
    current_evidence_rows: int
    concrete_triple_rows: int
    official_vpp_verified_rows: int
    archive_complete_rows: int
    submission_boundary_rows: int
    current_submission_ready_rows: int
    rejected_rows: int
    incomplete_archive_rows: int
    row_ok: bool


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def classify_candidate(candidate: OfficialVppArchiveCandidate) -> OfficialVppArchiveDecision:
    concrete = candidate.has_p and candidate.p_is_p25 and candidate.has_A and candidate.has_x0
    if not concrete:
        return OfficialVppArchiveDecision(
            candidate=candidate,
            decision="reject_missing_concrete_p25_triple",
            concrete_triple_present=False,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="concrete p25 p,A,x0 triple",
            next_action="supply p=10^25+13 plus concrete A and x0",
            ok=True,
        )

    if not candidate.official_vpp_executed:
        return OfficialVppArchiveDecision(
            candidate=candidate,
            decision="concrete_triple_official_vpp_missing",
            concrete_triple_present=True,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="official vpp.py execution",
            next_action="run python3 src/vpp.py p A x0 and capture stdout/stderr",
            ok=True,
        )

    if not candidate.official_vpp_stdout_true:
        return OfficialVppArchiveDecision(
            candidate=candidate,
            decision="reject_official_vpp_not_true",
            concrete_triple_present=True,
            official_vpp_verified=False,
            archive_complete=False,
            submission_ready=False,
            current_submission_ready=False,
            first_missing_or_falsifier="official vpp.py stdout True",
            next_action="discard or debug the concrete payload; do not submit",
            ok=True,
        )

    archive_requirements = (
        (candidate.command_logged, "exact verifier command"),
        (candidate.verifier_sha256_recorded, "src/vpp.py sha256"),
        (candidate.run_dir_or_source_recorded, "hit run dir or theorem source provenance"),
        (candidate.environment_recorded, "machine/date/git/environment record"),
        (candidate.triple_file_archived, "triple file containing p,A,x0"),
        (candidate.vpp_log_archived, "vpp stdout/stderr log"),
        (candidate.lean_certificate_generated, "Lean certificate generated by official lean_vpp.py"),
        (candidate.lean_certificate_checked, "Lean certificate checked"),
    )
    for present, missing in archive_requirements:
        if not present:
            decision = {
                "exact verifier command": "archive_incomplete_command_missing",
                "src/vpp.py sha256": "archive_incomplete_verifier_hash_missing",
                "hit run dir or theorem source provenance": "archive_incomplete_source_provenance_missing",
                "machine/date/git/environment record": "archive_incomplete_environment_missing",
                "triple file containing p,A,x0": "archive_incomplete_triple_file_missing",
                "vpp stdout/stderr log": "archive_incomplete_vpp_log_missing",
                "Lean certificate generated by official lean_vpp.py": "vpp_verified_lean_certificate_missing",
                "Lean certificate checked": "lean_certificate_unchecked",
            }[missing]
            return OfficialVppArchiveDecision(
                candidate=candidate,
                decision=decision,
                concrete_triple_present=True,
                official_vpp_verified=True,
                archive_complete=False,
                submission_ready=False,
                current_submission_ready=False,
                first_missing_or_falsifier=missing,
                next_action="complete the archive bundle before calling the run finished",
                ok=True,
            )

    return OfficialVppArchiveDecision(
        candidate=candidate,
        decision="submission_archive_complete",
        concrete_triple_present=True,
        official_vpp_verified=True,
        archive_complete=True,
        submission_ready=True,
        current_submission_ready=candidate.current_evidence,
        first_missing_or_falsifier="none",
        next_action="submit/report the p25 triple and preserve the archive bundle",
        ok=True,
    )


def candidate(name: str, **overrides: bool) -> OfficialVppArchiveCandidate:
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
        "current_evidence": False,
    }
    base.update(overrides)
    return OfficialVppArchiveCandidate(name=name, **base)


def regression_candidates() -> tuple[OfficialVppArchiveCandidate, ...]:
    return (
        candidate("missing_triple", has_A=False, has_x0=False),
        candidate("concrete_triple_vpp_not_run", official_vpp_executed=False, official_vpp_stdout_true=False),
        candidate("concrete_triple_vpp_false", official_vpp_stdout_true=False),
        candidate("vpp_true_command_missing", command_logged=False),
        candidate("vpp_true_hash_missing", verifier_sha256_recorded=False),
        candidate("vpp_true_source_missing", run_dir_or_source_recorded=False),
        candidate("vpp_true_environment_missing", environment_recorded=False),
        candidate("vpp_true_triple_file_missing", triple_file_archived=False),
        candidate("vpp_true_log_missing", vpp_log_archived=False),
        candidate("vpp_true_lean_missing", lean_certificate_generated=False, lean_certificate_checked=False),
        candidate("vpp_true_lean_unchecked", lean_certificate_checked=False),
        candidate("complete_archive_boundary"),
    )


def profile_vpp_submission_archive_contract() -> VppSubmissionArchiveContract:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    post_surface = profile_post_surface_halving_vpp_intake()
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
        "archive_incomplete_verifier_hash_missing",
        "archive_incomplete_source_provenance_missing",
        "archive_incomplete_environment_missing",
        "archive_incomplete_triple_file_missing",
        "archive_incomplete_vpp_log_missing",
        "vpp_verified_lean_certificate_missing",
        "lean_certificate_unchecked",
        "submission_archive_complete",
    )
    current = sum(row.candidate.current_evidence for row in rows)
    concrete = sum(row.concrete_triple_present for row in rows)
    vpp_verified = sum(row.official_vpp_verified for row in rows)
    archive_complete = sum(row.archive_complete for row in rows)
    submission = sum(row.submission_ready for row in rows)
    current_submission = sum(row.current_submission_ready for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    incomplete_archive = sum(
        row.decision.startswith("archive_incomplete_")
        or row.decision in {"vpp_verified_lean_certificate_missing", "lean_certificate_unchecked"}
        for row in rows
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and post_surface.row_ok
        and P25 == 10**25 + 13
        and vpp_sha == EXPECTED_LOCAL_VPP_SHA256
        and p24_true
        and p24_bad
        and P24_CERT.exists()
        and len(rows) == 12
        and current == 0
        and concrete == 11
        and vpp_verified == 9
        and archive_complete == 1
        and submission == 1
        and current_submission == 0
        and rejected == 2
        and incomplete_archive == 8
        and decisions == expected
        and all(row.ok for row in rows)
    )
    return VppSubmissionArchiveContract(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        post_surface_halving_ok=post_surface.row_ok,
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
        archive_complete_rows=archive_complete,
        submission_boundary_rows=submission,
        current_submission_ready_rows=current_submission,
        rejected_rows=rejected,
        incomplete_archive_rows=incomplete_archive,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_vpp_submission_archive_contract()
    print("p25 KSY-y official vpp submission archive contract gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  post_surface_halving_ok={int(profile.post_surface_halving_ok)}")
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
            f"triple={int(row.concrete_triple_present)} "
            f"vpp={int(row.official_vpp_verified)} "
            f"archive={int(row.archive_complete)} "
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
    print(f"  archive_complete_rows={profile.archive_complete_rows}")
    print(f"  submission_boundary_rows={profile.submission_boundary_rows}")
    print(f"  current_submission_ready_rows={profile.current_submission_ready_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  incomplete_archive_rows={profile.incomplete_archive_rows}")
    print("interpretation")
    print("  concrete_triple_must_pass_official_vpp_before_submission=1")
    print("  vpp_true_still_needs_command_hash_env_logs_and_lean_archive=1")
    print("  p24_good_and_bad_regressions_guard_the_local_vpp_copy=1")
    print(f"ksy_y_official_vpp_submission_archive_contract_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("official vpp submission archive contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
