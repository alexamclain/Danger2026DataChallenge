#!/usr/bin/env python3
"""Guard the conductor-39 packet path against rowless promotion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MARKER = "p25_v2_conductor39_row_binding_overlay_rows=1/1"

LEGAL_ROWS = {
    1: ("7H -> 4H", "eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e"),
    2: ("7H -> H", "97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9"),
    4: ("2H -> H", "28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6"),
    8: ("2H -> 4H", "ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87"),
}

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_priority1_packet_fixture_contract_20260617.md",
        "p25_v2_priority1_packet_fixture_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_priority1_clause_necessity_matrix_20260617.md",
        "p25_v2_priority1_clause_necessity_matrix_rows=1/1",
    ),
    (
        "evidence/p25_v2_self_contained_theorem_statement_20260616.md",
        "p25_v2_self_contained_theorem_statement_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_graph_normal_form_20260616.md",
        "p25_v2_source_graph_normal_form_rows=1/1",
    ),
    (
        "evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
        "p25_v2_conductor39_yang_h90_interface_contract_rows=1/1",
    ),
)


@dataclass(frozen=True)
class Candidate:
    name: str
    row_m: int | None
    edge: str | None
    row_hash: str | None
    has_mixed_packet: bool
    has_finite_theorem: bool
    decision: str
    ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        ok += int(path.exists() and marker in path.read_text())
    return ok, len(EVIDENCE_MARKERS)


def classify(candidate: Candidate) -> str:
    if not candidate.has_mixed_packet:
        return "reject_not_conductor39_packet"
    if not candidate.has_finite_theorem:
        return "repair_finite_theorem_missing"
    if candidate.row_m not in LEGAL_ROWS:
        return "repair_row_binding_missing"
    edge, row_hash = LEGAL_ROWS[candidate.row_m]
    if candidate.edge != edge:
        return "repair_edge_label_mismatch"
    if candidate.row_hash != row_hash:
        return "repair_row_hash_mismatch"
    return "row_bound_priority1_packet"


def candidates() -> tuple[Candidate, ...]:
    rows: list[Candidate] = [
        Candidate(
            name="archived_conductor39_fixture_shape",
            row_m=None,
            edge=None,
            row_hash=None,
            has_mixed_packet=True,
            has_finite_theorem=True,
            decision="repair_row_binding_missing",
            ok=False,
        ),
        Candidate(
            name="missing_finite_theorem",
            row_m=1,
            edge=LEGAL_ROWS[1][0],
            row_hash=LEGAL_ROWS[1][1],
            has_mixed_packet=True,
            has_finite_theorem=False,
            decision="repair_finite_theorem_missing",
            ok=False,
        ),
        Candidate(
            name="wrong_edge_label",
            row_m=1,
            edge=LEGAL_ROWS[2][0],
            row_hash=LEGAL_ROWS[1][1],
            has_mixed_packet=True,
            has_finite_theorem=True,
            decision="repair_edge_label_mismatch",
            ok=False,
        ),
        Candidate(
            name="wrong_row_hash",
            row_m=1,
            edge=LEGAL_ROWS[1][0],
            row_hash=LEGAL_ROWS[2][1],
            has_mixed_packet=True,
            has_finite_theorem=True,
            decision="repair_row_hash_mismatch",
            ok=False,
        ),
        Candidate(
            name="not_conductor39_packet",
            row_m=1,
            edge=LEGAL_ROWS[1][0],
            row_hash=LEGAL_ROWS[1][1],
            has_mixed_packet=False,
            has_finite_theorem=True,
            decision="reject_not_conductor39_packet",
            ok=False,
        ),
    ]
    for m, (edge, row_hash) in LEGAL_ROWS.items():
        rows.append(
            Candidate(
                name=f"row_bound_m{m}",
                row_m=m,
                edge=edge,
                row_hash=row_hash,
                has_mixed_packet=True,
                has_finite_theorem=True,
                decision="row_bound_priority1_packet",
                ok=True,
            )
        )
    return tuple(rows)


def main() -> int:
    root = research_root()
    evidence_ok, evidence_total = evidence_markers_ok(root)
    text = "\n".join(
        (root / rel).read_text()
        for rel, _marker in EVIDENCE_MARKERS
        if (root / rel).exists()
    )
    row_hashes_bound = sum(row_hash in text for _edge, row_hash in LEGAL_ROWS.values())
    rows = candidates()
    classified = tuple((row, classify(row)) for row in rows)
    positives = sum(actual == "row_bound_priority1_packet" for _row, actual in classified)
    repairs = sum(actual.startswith("repair_") for _row, actual in classified)
    rejects = sum(actual.startswith("reject_") for _row, actual in classified)
    archived_fixture_repair = any(
        row.name == "archived_conductor39_fixture_shape"
        and actual == "repair_row_binding_missing"
        for row, actual in classified
    )
    row_ok = (
        evidence_ok == evidence_total
        and row_hashes_bound == 4
        and len(rows) == 9
        and positives == 4
        and repairs == 4
        and rejects == 1
        and archived_fixture_repair
        and all(actual == row.decision for row, actual in classified)
    )
    print("p25 v2 conductor-39 row-binding overlay")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print(f"legal_row_hashes_bound={row_hashes_bound}/4")
    print("rows")
    for row, actual in classified:
        print(
            f"  {row.name}: m={row.row_m} edge={row.edge} "
            f"decision={actual} expected={row.decision}"
        )
    print("counts")
    print(f"candidate_rows={len(rows)}")
    print(f"row_bound_positive_packets={positives}")
    print(f"repair_rows={repairs}")
    print(f"reject_rows={rejects}")
    print(f"archived_conductor39_fixture_requires_row_binding={int(archived_fixture_repair)}")
    print("current_conductor39_row_bound_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"{MARKER if row_ok else 'p25_v2_conductor39_row_binding_overlay_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
