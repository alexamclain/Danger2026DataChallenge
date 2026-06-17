#!/usr/bin/env python3
"""Validate the v2 priority-1 packet fixture contract.

The old priority-1 packet fixtures are still useful, but v2 demotes
twisted-H90 and curved-corner to support surfaces.  This gate reclassifies the
archived fixture set against the current theorem kernel so future source or
expert answers can be tested without reopening the old lane semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


FIXTURE_DIR = Path("archive/fixtures/priority1_divisor_additive_packet_fixtures")
MARKER = "p25_v2_priority1_packet_fixture_contract_rows=1/1"

REQUIRED_FIELDS = (
    "name",
    "lane",
    "claim_is_current_evidence",
    "theorem_body_verified",
    "output_kind",
    "arithmetic_source_theorem",
    "finite_or_divisor",
    "period156_context",
    "danger3_framing",
    "h0_product_multiplier",
    "h0_residue_sets_exact",
    "h0_h90_boundary",
    "conductor39_source_object",
    "conductor39_emits_object",
    "conductor39_preserves_mixed_tensor",
    "conductor39_yang_yu_legal_unit",
    "conductor39_sparse_formal_gauge_only",
    "conductor39_projection_or_axis_only",
    "conductor39_additive_separated",
    "conductor39_yang_distribution_to_507",
    "conductor39_frobenius_or_hilbert90_descent",
    "twisted_uses_degree6_orbit",
    "twisted_uses_pure_norm",
    "twisted_uses_pair_sum",
    "twisted_uses_signed_shadow",
    "twisted_uses_quotient_or_ratio",
    "twisted_uses_hilbert90_boundary",
    "curved_payload_shape_verified",
    "curved_unit_triangle",
)

EXPECTED_DECISIONS = {
    "h0_divisor_close.json": "current_first_pass_positive_packet",
    "h0_missing_boundary.json": "repair_h0_boundary_missing",
    "conductor39_divisor_close.json": "current_first_pass_positive_packet",
    "twisted_divisor_close.json": "support_packet_requires_source_snippet",
    "twisted_missing_period.json": "repair_period156_context_missing",
    "curved_corner_divisor_close.json": "support_packet_requires_source_snippet",
    "curved_missing_period.json": "repair_period156_context_missing",
    "projection_reject.json": "reject_projection_or_axis_only",
}

LEGAL_ROW_HASHES = {
    1: "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e",
    2: "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9",
    4: "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6",
    8: "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87",
}

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    (
        "evidence/p25_v2_support_lane_status_demotion_20260616.md",
        "p25_v2_support_lane_status_demotion_rows=1/1",
    ),
)


@dataclass(frozen=True)
class FixtureRow:
    filename: str
    lane: str
    decision: str
    expected: str
    missing_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    current_evidence_claim: bool
    ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "archive").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: expected JSON object")
    return data


def classify(data: dict[str, object]) -> str:
    lane = data["lane"]
    source_ok = (
        data["theorem_body_verified"]
        and data["output_kind"] == "divisor-additive"
        and data["arithmetic_source_theorem"]
        and data["finite_or_divisor"]
    )
    if data["conductor39_projection_or_axis_only"]:
        return "reject_projection_or_axis_only"
    if lane == "h0":
        if not data["h0_h90_boundary"]:
            return "repair_h0_boundary_missing"
        if (
            source_ok
            and data["h0_product_multiplier"] in (1, 2, 4, 8)
            and data["h0_residue_sets_exact"]
        ):
            return "current_first_pass_positive_packet"
        return "repair_h0_row_or_source_clause_missing"
    if lane == "conductor39":
        if not data["conductor39_preserves_mixed_tensor"]:
            return "repair_mixed_tensor_missing"
        if (
            source_ok
            and data["conductor39_source_object"] == "U_chi"
            and data["conductor39_emits_object"]
            and data["conductor39_yang_yu_legal_unit"]
            and data["conductor39_yang_distribution_to_507"]
            and data["conductor39_frobenius_or_hilbert90_descent"]
        ):
            return "current_first_pass_positive_packet"
        return "repair_conductor39_clause_missing"
    if lane in ("twisted_h90", "curved_corner"):
        if not data["period156_context"]:
            return "repair_period156_context_missing"
        if source_ok:
            return "support_packet_requires_source_snippet"
        return "repair_support_payload_missing"
    return "reject_unknown_lane"


def fixture_row(root: Path, filename: str, expected: str) -> FixtureRow:
    path = root / FIXTURE_DIR / filename
    data = read_json(path)
    fields = set(data)
    required = set(REQUIRED_FIELDS)
    decision = classify(data)
    return FixtureRow(
        filename=filename,
        lane=str(data["lane"]),
        decision=decision,
        expected=expected,
        missing_fields=tuple(sorted(required - fields)),
        unknown_fields=tuple(sorted(fields - required)),
        current_evidence_claim=bool(data["claim_is_current_evidence"]),
        ok=(
            path.exists()
            and not (required - fields)
            and not (fields - required)
            and decision == expected
            and data["claim_is_current_evidence"] is False
        ),
    )


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        ok += int(path.exists() and marker in path.read_text())
    return ok, len(EVIDENCE_MARKERS)


def main() -> int:
    root = research_root()
    rows = tuple(
        fixture_row(root, filename, expected)
        for filename, expected in EXPECTED_DECISIONS.items()
    )
    evidence_ok, evidence_total = evidence_markers_ok(root)
    current_first_pass = sum(
        row.decision == "current_first_pass_positive_packet" for row in rows
    )
    support_only = sum(
        row.decision == "support_packet_requires_source_snippet" for row in rows
    )
    repair = sum(row.decision.startswith("repair_") for row in rows)
    reject = sum(row.decision.startswith("reject_") for row in rows)
    theorem_text = (root / "evidence/p25_v2_self_contained_theorem_statement_20260616.md").read_text()
    snippet_text = (root / "evidence/p25_v2_source_snippet_intake_20260616.md").read_text()
    legal_hashes_ok = sum(
        row_hash in theorem_text and row_hash in snippet_text
        for row_hash in LEGAL_ROW_HASHES.values()
    )
    h0_positive_hash_bound = all(
        row.lane != "h0"
        or row.decision != "current_first_pass_positive_packet"
        or LEGAL_ROW_HASHES[read_json(root / FIXTURE_DIR / row.filename)["h0_product_multiplier"]]
        in theorem_text
        for row in rows
    )
    row_ok = (
        evidence_ok == evidence_total
        and len(rows) == 8
        and all(row.ok for row in rows)
        and legal_hashes_ok == 4
        and h0_positive_hash_bound
        and current_first_pass == 2
        and support_only == 2
        and repair == 3
        and reject == 1
        and sum(row.current_evidence_claim for row in rows) == 0
    )
    print("p25 v2 priority-1 packet fixture contract")
    print(f"fixture_dir={(root / FIXTURE_DIR)}")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print(f"legal_row_hashes_ok={legal_hashes_ok}/4")
    print(f"h0_positive_hash_bound={int(h0_positive_hash_bound)}")
    print("fixture_rows")
    for row in rows:
        print(
            f"  {row.filename}: lane={row.lane} decision={row.decision} "
            f"expected={row.expected} current_evidence={int(row.current_evidence_claim)}"
        )
        print(f"    missing_fields={row.missing_fields}")
        print(f"    unknown_fields={row.unknown_fields}")
    print("counts")
    print(f"fixture_rows={len(rows)}")
    print(f"legal_row_hashes_bound={legal_hashes_ok}")
    print(f"current_first_pass_positive_packets={current_first_pass}")
    print(f"support_only_positive_packets={support_only}")
    print(f"repair_packets={repair}")
    print(f"reject_packets={reject}")
    print("current_priority1_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"{MARKER if row_ok else 'p25_v2_priority1_packet_fixture_contract_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
