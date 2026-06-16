#!/usr/bin/env python3
"""Export canonical payload fixtures for the p25 KSY/Hilbert-90 intake.

The universal intake harness gives future theorem hits a single front door.
This exporter writes stable text fixtures for the file-based modes and records
the exact command shapes for argument-based modes.  It also verifies that the
positive fixtures pass and the near-miss fixtures fail.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

from p25_laneB_robert_ksy_theta2_candidate_harness import (
    theta2_sparse_entries,
    theta2_target_rings,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    packet_entries,
    q_cycle_confusion_packet,
    target_source_quotient_packet,
)
from p25_laneB_robert_ksy_theta2_universal_producer_intake import (
    default_universal_producer_intake_profile,
    run_candidate,
)


FIXTURE_DIR = Path(__file__).with_name("producer_payload_fixtures")


@dataclass(frozen=True)
class FixtureFile:
    name: str
    path: str
    line_count: int
    sha256: str


@dataclass(frozen=True)
class FixtureExportProfile:
    fixture_dir: str
    written_files: tuple[FixtureFile, ...]
    default_universal_intake_ok: bool
    source_packet_fixture_ok: bool
    theta2_sparse_fixture_ok: bool
    theta2_inverse_sparse_fixture_ok: bool
    q_cycle_reject_fixture_rejected: bool
    plain_bridge_reject_fixture_rejected: bool
    row_ok: bool


def write_rows(path: Path, rows: tuple[tuple[int, int, int], ...]) -> FixtureFile:
    text = "".join(f"{left} {right} {coefficient}\n" for left, right, coefficient in rows)
    path.write_text(text)
    return FixtureFile(
        name=path.name,
        path=str(path),
        line_count=len(rows),
        sha256=sha256(text.encode()).hexdigest(),
    )


def write_text(path: Path, text: str) -> FixtureFile:
    path.write_text(text)
    return FixtureFile(
        name=path.name,
        path=str(path),
        line_count=len(text.splitlines()),
        sha256=sha256(text.encode()).hexdigest(),
    )


def namespace(**overrides: object) -> SimpleNamespace:
    values: dict[str, object] = {
        "mode": None,
        "eps": None,
        "branch": None,
        "packet": None,
        "sparse_source": None,
        "k_multiplier": 1,
        "base_right_class": None,
        "base_right": None,
        "base_c": None,
        "d_right_class": None,
        "d_right": None,
        "d_c": None,
        "t_right_class": None,
        "t_right": None,
        "t_c": None,
        "k_right": None,
        "k_c": None,
        "center_right": None,
        "center_c": None,
        "half_right": None,
        "half_c": None,
        "invert": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def candidate_ok(**kwargs: object) -> bool:
    _mode, ok, _profile = run_candidate(namespace(**kwargs))
    return ok


def export_fixtures() -> FixtureExportProfile:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    bridge, theta2, theta2_inverse = theta2_target_rings()
    source_packet_path = FIXTURE_DIR / "source_packet_target.txt"
    q_cycle_path = FIXTURE_DIR / "source_packet_q_cycle_reject.txt"
    theta2_path = FIXTURE_DIR / "theta2_sparse_target.txt"
    theta2_inverse_path = FIXTURE_DIR / "theta2_inverse_sparse_target.txt"
    plain_bridge_path = FIXTURE_DIR / "theta2_sparse_plain_bridge_reject.txt"

    files = [
        write_rows(source_packet_path, packet_entries(target_source_quotient_packet())),
        write_rows(q_cycle_path, packet_entries(q_cycle_confusion_packet())),
        write_rows(theta2_path, theta2_sparse_entries(theta2)),
        write_rows(theta2_inverse_path, theta2_sparse_entries(theta2_inverse)),
        write_rows(plain_bridge_path, theta2_sparse_entries(bridge)),
    ]
    commands = """# P25 KSY/Hilbert-90 universal producer intake fixture commands

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode hilbert90-signs --eps 1 --branch -1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode source-packet --packet research/p25/producer_payload_fixtures/source_packet_target.txt --k-multiplier 1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode quotient-factor --base-right-class 1 --base-c 25 --d-right-class 1 --d-c 3 --t-right-class 2 --t-c 113 --k-multiplier 1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode source-factor --base-right 25 --base-c 25 --k-right 57 --k-c 0 --d-right 22 --d-c 3 --t-right 38 --t-c 113

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode compact-theta2 --center-right 44 --center-c 166 --half-right 56 --half-c 28

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode compact-theta2 --center-right 44 --center-c 166 --half-right 56 --half-c 28 --invert

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode theta2-sparse --sparse-source research/p25/producer_payload_fixtures/theta2_sparse_target.txt

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode theta2-sparse --sparse-source research/p25/producer_payload_fixtures/theta2_inverse_sparse_target.txt
"""
    files.append(write_text(FIXTURE_DIR / "universal_intake_commands.sh", commands))

    source_packet_ok = candidate_ok(
        mode="source-packet",
        packet=source_packet_path,
        k_multiplier=1,
    )
    theta2_ok = candidate_ok(mode="theta2-sparse", sparse_source=theta2_path)
    theta2_inverse_ok = candidate_ok(
        mode="theta2-sparse",
        sparse_source=theta2_inverse_path,
    )
    q_cycle_ok = candidate_ok(
        mode="source-packet",
        packet=q_cycle_path,
        k_multiplier=1,
    )
    plain_bridge_ok = candidate_ok(
        mode="theta2-sparse",
        sparse_source=plain_bridge_path,
    )
    default_profile = default_universal_producer_intake_profile()
    row_ok = (
        default_profile.row_ok
        and source_packet_ok
        and theta2_ok
        and theta2_inverse_ok
        and not q_cycle_ok
        and not plain_bridge_ok
        and tuple(file.line_count for file in files[:5]) == (6, 6, 300, 300, 150)
    )
    return FixtureExportProfile(
        fixture_dir=str(FIXTURE_DIR),
        written_files=tuple(files),
        default_universal_intake_ok=default_profile.row_ok,
        source_packet_fixture_ok=source_packet_ok,
        theta2_sparse_fixture_ok=theta2_ok,
        theta2_inverse_sparse_fixture_ok=theta2_inverse_ok,
        q_cycle_reject_fixture_rejected=not q_cycle_ok,
        plain_bridge_reject_fixture_rejected=not plain_bridge_ok,
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY/Hilbert-90 payload fixture export")
    profile = export_fixtures()
    print(f"payload_fixture_export_profile={profile}")
    print("fixture_laws")
    print("  source_packet_theta2_and_theta2_inverse_positive_fixtures_pass=1")
    print("  q_cycle_packet_and_plain_bridge_theta2_reject_fixtures_fail=1")
    print("  exported_fixture_line_counts_are_6_6_300_300_150=1")
    print("interpretation")
    print("  theorem_hits_can_now_be_compared_against_stable_payload_files=1")
    print("  fixtures_are_finite_targets_not_arithmetic_producer_proofs=1")
    print(f"robert_ksy_theta2_payload_fixture_export_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_payload_fixture_export")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
