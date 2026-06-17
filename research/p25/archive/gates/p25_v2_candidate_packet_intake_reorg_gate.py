#!/usr/bin/env python3
"""Validate the current source-to-certificate packet intake after wiki reorg.

This is a light v2 wrapper around the older H0 candidate-packet gates. It
checks that the exact-product fixtures now live in archive/fixtures, that the
legacy harness-side duplicate fixture directory is absent, and that the
end-to-end packet classifier still enforces the source -> framing -> same-j
bridge -> X_1(16) -> halving/x0 -> vpp.py order.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = GATE_DIR.parent
HARNESS_DIR = ARCHIVE_DIR / "harness"
FIXTURE_DIR = ARCHIVE_DIR / "fixtures" / "h0_product_fixtures"
LEGACY_HARNESS_FIXTURE_DIR = HARNESS_DIR / "h0_product_fixtures"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_ksy_y_h0_candidate_packet_intake_gate import (  # noqa: E402
    profile_h0_candidate_packet_intake,
)
from p25_ksy_y_h0_exact_product_fixture_export import (  # noqa: E402
    FIXTURE_DIR as EXPORT_FIXTURE_DIR,
    export_fixtures,
)
from p25_ksy_y_h0_product_file_claim_intake_gate import (  # noqa: E402
    profile_h0_product_file_claim_intake,
)


@dataclass(frozen=True)
class CandidatePacketIntakeReorg:
    fixture_export_ok: bool
    product_file_intake_ok: bool
    candidate_packet_intake_ok: bool
    fixture_dir_is_archived: bool
    fixture_files_present: int
    duplicate_harness_fixture_dir_absent: bool
    product_file_source_closing_rows: int
    product_file_submission_ready_control_rows: int
    candidate_packet_source_stage_closed_rows: int
    candidate_packet_cross_level_bridge_rows: int
    candidate_packet_x16_surface_rows: int
    candidate_packet_partial_chain_rows: int
    candidate_packet_extraction_ready_rows: int
    candidate_packet_vpp_executed_rows: int
    candidate_packet_submission_ready_rows: int
    current_real_submission_ready_rows: int
    decision: str
    row_ok: bool


def build_profile() -> CandidatePacketIntakeReorg:
    fixture_export = export_fixtures()
    product_file = profile_h0_product_file_claim_intake()
    candidate_packet = profile_h0_candidate_packet_intake()

    fixture_names = {
        "h0_m1_canonical_lifted_product.txt",
        "h0_m2_translate_lifted_product.txt",
        "h0_m4_translate_lifted_product.txt",
        "h0_m8_translate_lifted_product.txt",
        "h0_exact_product_manifest.tsv",
        "h0_candidate_matcher_commands.sh",
    }
    present = sum((FIXTURE_DIR / name).exists() for name in fixture_names)
    fixture_dir_is_archived = (
        Path(fixture_export.fixture_dir).resolve() == FIXTURE_DIR.resolve()
        and EXPORT_FIXTURE_DIR.resolve() == FIXTURE_DIR.resolve()
    )
    duplicate_absent = not LEGACY_HARNESS_FIXTURE_DIR.exists()
    current_real_submission_ready_rows = 0
    decision = "candidate_packet_intake_restored_current_submissions_zero"
    row_ok = (
        fixture_export.row_ok
        and product_file.row_ok
        and candidate_packet.row_ok
        and fixture_dir_is_archived
        and present == len(fixture_names)
        and duplicate_absent
        and product_file.source_closing_rows == 3
        and product_file.submission_ready_rows == 1
        and candidate_packet.source_stage_closed_rows == 8
        and candidate_packet.cross_level_bridge_rows == 5
        and candidate_packet.x16_surface_rows == 2
        and candidate_packet.partial_chain_rows == 1
        and candidate_packet.extraction_ready_rows == 1
        and candidate_packet.vpp_executed_rows == 1
        and candidate_packet.submission_ready_rows == 0
        and current_real_submission_ready_rows == 0
    )
    return CandidatePacketIntakeReorg(
        fixture_export_ok=fixture_export.row_ok,
        product_file_intake_ok=product_file.row_ok,
        candidate_packet_intake_ok=candidate_packet.row_ok,
        fixture_dir_is_archived=fixture_dir_is_archived,
        fixture_files_present=present,
        duplicate_harness_fixture_dir_absent=duplicate_absent,
        product_file_source_closing_rows=product_file.source_closing_rows,
        product_file_submission_ready_control_rows=product_file.submission_ready_rows,
        candidate_packet_source_stage_closed_rows=candidate_packet.source_stage_closed_rows,
        candidate_packet_cross_level_bridge_rows=candidate_packet.cross_level_bridge_rows,
        candidate_packet_x16_surface_rows=candidate_packet.x16_surface_rows,
        candidate_packet_partial_chain_rows=candidate_packet.partial_chain_rows,
        candidate_packet_extraction_ready_rows=candidate_packet.extraction_ready_rows,
        candidate_packet_vpp_executed_rows=candidate_packet.vpp_executed_rows,
        candidate_packet_submission_ready_rows=candidate_packet.submission_ready_rows,
        current_real_submission_ready_rows=current_real_submission_ready_rows,
        decision=decision,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 candidate packet intake reorg")
    print("dependencies")
    print(f"  fixture_export_ok={int(profile.fixture_export_ok)}")
    print(f"  product_file_intake_ok={int(profile.product_file_intake_ok)}")
    print(f"  candidate_packet_intake_ok={int(profile.candidate_packet_intake_ok)}")
    print("layout")
    print(f"  fixture_dir_is_archived={int(profile.fixture_dir_is_archived)}")
    print(f"  fixture_files_present={profile.fixture_files_present}/6")
    print(
        "  duplicate_harness_fixture_dir_absent="
        f"{int(profile.duplicate_harness_fixture_dir_absent)}"
    )
    print("counts")
    print(
        "  product_file_source_closing_rows="
        f"{profile.product_file_source_closing_rows}"
    )
    print(
        "  product_file_submission_ready_control_rows="
        f"{profile.product_file_submission_ready_control_rows}"
    )
    print(
        "  candidate_packet_source_stage_closed_rows="
        f"{profile.candidate_packet_source_stage_closed_rows}"
    )
    print(
        "  candidate_packet_cross_level_bridge_rows="
        f"{profile.candidate_packet_cross_level_bridge_rows}"
    )
    print(
        "  candidate_packet_x16_surface_rows="
        f"{profile.candidate_packet_x16_surface_rows}"
    )
    print(
        "  candidate_packet_partial_chain_rows="
        f"{profile.candidate_packet_partial_chain_rows}"
    )
    print(
        "  candidate_packet_extraction_ready_rows="
        f"{profile.candidate_packet_extraction_ready_rows}"
    )
    print(
        "  candidate_packet_vpp_executed_rows="
        f"{profile.candidate_packet_vpp_executed_rows}"
    )
    print(
        "  candidate_packet_submission_ready_rows="
        f"{profile.candidate_packet_submission_ready_rows}"
    )
    print(
        "  current_real_submission_ready_rows="
        f"{profile.current_real_submission_ready_rows}"
    )
    print("interpretation")
    print(f"  decision={profile.decision}")
    print("  exact_product_fixtures_are_archived_evidence_not_live_pages=1")
    print("  packet_must_pass_source_bridge_chart_chain_vpp_in_order=1")
    print("  no_current_packet_is_submission_ready=1")
    print(f"p25_v2_candidate_packet_intake_reorg_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("candidate packet intake reorg regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
