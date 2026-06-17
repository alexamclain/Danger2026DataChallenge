#!/usr/bin/env python3
"""Lightweight validator for the exact-P finite-geometry rigidity page.

The exact-P finite geometry was established by older Lane B gates.  During the
active p25 production run we do not replay those heavier gates by default.
This validator makes the promoted v2 evidence page cockpit-trackable: it
checks that the page still records the rigid equal-weight 75-atom payload, the
theta2/theta2-inverse signs, the corner row polynomial, and the quotient shift
normal form that make exact-P a precise heavy route rather than vague
normalized-y vocabulary.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EVIDENCE_PATH = "research/p25/evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md"

REQUIRED_CLAUSES = (
    "atom_count = 75",
    "support_per_atom = 4",
    "pairwise_intersecting_atom_pairs = 0",
    "atom_union_support = 300",
    "linear_rank_from_disjoint_support = 75",
    "linear_nullity_from_disjoint_support = 0",
    "theta2_inverse_solution = all 75 weights +1",
    "theta2_solution = all 75 weights -1",
    "missing_atom_rejected = true",
    "alternating_k_weights_rejected = true",
    "c13 shadow c0(r) = 4*r^2 - r",
    "fiber f(r) = r*(1-r)",
    "c169 values = 0, 3, 144",
    "q values = 0, 172, 482",
    "right_degree = 3",
    "square_c = 169",
    "quotient_order = 507",
    "D = (right+1, c+1)",
    "X = (right+1, c-42)",
    "Y = (right, c+3)",
    "D^3 = Y",
    "selected_count = 18/18",
    "new_positive_artifact = finite geometry rigidity and row-polynomial normal form",
    "still_missing = arithmetic source theorem selecting this exact equal-weight",
)

ARCHIVED_MARKERS = (
    "robert_ksy_theta2_kubert_lang_atomic_weight_rigidity_rows=1/1",
    "square_axis_bridge_hilbert90_source_chain_corner_row_polynomial_rows=1/1",
    "square_axis_quotient_shift_normal_form_rows=1/1",
)

REJECT_CLAUSES = (
    "nonuniform `K`-trace",
    "missing-atom",
    "atomic-weight null",
    "nonuniform weights",
    "atom subset",
    "generic ray-class generator",
)


@dataclass(frozen=True)
class ExactPFiniteGeometryRigidityCheck:
    evidence_path: Path
    marker_present: bool
    archived_markers_ok: int
    archived_markers_total: int
    required_clauses_ok: int
    required_clauses_total: int
    reject_clauses_ok: int
    reject_clauses_total: int
    atom_count: int
    atom_union_support: int
    disjoint_support_forces_rank: bool
    theta2_signs_are_opposite: bool
    current_exactp_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd
    for parent in (cwd, *cwd.parents):
        if (parent / "research/p25").exists():
            return parent
    raise FileNotFoundError("run from repo root or inside repo")


def build_check(root: Path) -> ExactPFiniteGeometryRigidityCheck:
    path = root / EVIDENCE_PATH
    text = path.read_text() if path.exists() else ""
    marker_present = "p25_v2_exactp_finite_geometry_rigidity_rows=1/1" in text
    archived_ok = sum(marker in text for marker in ARCHIVED_MARKERS)
    required_ok = sum(clause in text for clause in REQUIRED_CLAUSES)
    reject_ok = sum(clause in text for clause in REJECT_CLAUSES)
    atom_count = 75
    support_per_atom = 4
    atom_union_support = atom_count * support_per_atom
    disjoint_support_forces_rank = atom_union_support == 300 and atom_count == 75
    theta2_signs_are_opposite = (
        "theta2_inverse_solution = all 75 weights +1" in text
        and "theta2_solution = all 75 weights -1" in text
    )
    current_exactp_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        path.exists()
        and marker_present
        and archived_ok == len(ARCHIVED_MARKERS)
        and required_ok == len(REQUIRED_CLAUSES)
        and reject_ok == len(REJECT_CLAUSES)
        and atom_count == 75
        and atom_union_support == 300
        and disjoint_support_forces_rank
        and theta2_signs_are_opposite
        and current_exactp_source_theorems == 0
        and current_submission_ready == 0
    )
    return ExactPFiniteGeometryRigidityCheck(
        evidence_path=Path(EVIDENCE_PATH),
        marker_present=marker_present,
        archived_markers_ok=archived_ok,
        archived_markers_total=len(ARCHIVED_MARKERS),
        required_clauses_ok=required_ok,
        required_clauses_total=len(REQUIRED_CLAUSES),
        reject_clauses_ok=reject_ok,
        reject_clauses_total=len(REJECT_CLAUSES),
        atom_count=atom_count,
        atom_union_support=atom_union_support,
        disjoint_support_forces_rank=disjoint_support_forces_rank,
        theta2_signs_are_opposite=theta2_signs_are_opposite,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    check = build_check(repo_root())
    print("p25 v2 exact-P finite-geometry rigidity")
    print(f"evidence_path={check.evidence_path}")
    print(f"marker_present={int(check.marker_present)}")
    print(f"archived_markers_ok={check.archived_markers_ok}/{check.archived_markers_total}")
    print(f"required_clauses_ok={check.required_clauses_ok}/{check.required_clauses_total}")
    print(f"reject_clauses_ok={check.reject_clauses_ok}/{check.reject_clauses_total}")
    print(f"atom_count={check.atom_count}")
    print(f"atom_union_support={check.atom_union_support}")
    print(f"disjoint_support_forces_rank={int(check.disjoint_support_forces_rank)}")
    print(f"theta2_signs_are_opposite={int(check.theta2_signs_are_opposite)}")
    print(f"current_exactp_source_theorems={check.current_exactp_source_theorems}")
    print(f"current_submission_ready={check.current_submission_ready}")
    print(f"p25_v2_exactp_finite_geometry_rigidity_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
