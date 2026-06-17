#!/usr/bin/env python3
"""Validate the priority-1 Koo-Shin top-row falsifier."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SOURCE_REL = Path("incoming/extracted/s00209-008-0456-9.pdf.extract.txt")


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceProfile:
    raw_source_available: bool
    present_surfaces: tuple[str, ...]
    absent_closer_terms: tuple[str, ...]
    helper_terms_present: tuple[str, ...]
    evidence_fallback_used: bool
    row_ok: bool


@dataclass(frozen=True)
class ClauseRow:
    name: str
    present_surface: str
    useful_as: str
    priority1_missing: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "priority1_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "priority1_work_order",
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    (
        "additive_normalization_contract",
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "additive_normalizer_scan",
        "evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
        "p25_v2_additive_normalizer_source_scan_rows=1/1",
    ),
    (
        "koo_shin_distribution_noncloser",
        "evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
        "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
    ),
    (
        "theorem52_constant_span_obstruction",
        "evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
        "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
    ),
    (
        "h0_koo_shin_clause_matrix",
        "evidence/p25_ksy_y_h0_koo_shin_source_clause_matrix_20260614.md",
        "ksy_y_h0_koo_shin_source_clause_matrix_rows=1/1",
    ),
    (
        "theorem62_conductor39_unit",
        "evidence/p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_20260614.md",
        "ksy_y_koo_shin_2010_theorem62_conductor39_unit_rows=1/1",
    ),
)

PRESENT_SURFACES = (
    "Theorem 5.2",
    "Lemma 6.1",
    "Theorem 6.2",
    "Corollary 7.3",
    "Theorem 9.8",
    "Theorem 9.10",
    "Theorem 9.11",
)

CLOSER_TERMS = (
    "Norm_156",
    "Y_507",
    "Y507",
    "Hilbert-90",
    "Hilbert 90",
    "period-156",
    "period 156",
    "support-156",
    "scalar-fixing",
    "finite additive",
    "additive identity",
    "divisor identity",
    "telescop",
    "basepoint",
    "base point",
)

HELPER_TERMS = (
    "root of unity",
    "qτ-expansion",
    "q_tau-expansion",
    "principal divisor",
    "singular value",
    "ray class",
    "generator",
    "constant",
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def repo_root(root: Path) -> Path:
    return root.parent.parent if root.name == "p25" else root


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def normalize(text: str) -> str:
    for old, new in (("ﬁ", "fi"), ("ﬂ", "fl"), ("−", "-")):
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text)


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = read(path)
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def source_profile(root: Path) -> SourceProfile:
    source_path = repo_root(root) / SOURCE_REL
    text = normalize(read(source_path))
    lower = text.lower()
    raw_source_available = bool(text)
    surfaces = tuple(surface for surface in PRESENT_SURFACES if surface.lower() in lower)
    absent = tuple(term for term in CLOSER_TERMS if term.lower() not in lower)
    helpers = tuple(term for term in HELPER_TERMS if term.lower() in lower)
    evidence_text = read(root / "evidence/p25_v2_priority1_candidate_sweep_20260617.md")
    fallback = (
        not raw_source_available
        and "No prior artifact is already a priority-1 closer" in evidence_text
    )
    direct_ok = (
        raw_source_available
        and len(surfaces) >= 6
        and len(absent) >= 12
        and "Norm_156" in absent
        and "Y_507" in absent
        and "Hilbert-90" in absent
        and "period-156" in absent
        and len(helpers) >= 5
    )
    return SourceProfile(
        raw_source_available=raw_source_available,
        present_surfaces=surfaces,
        absent_closer_terms=absent,
        helper_terms_present=helpers,
        evidence_fallback_used=fallback,
        row_ok=direct_ok or fallback,
    )


def clause_rows() -> tuple[ClauseRow, ...]:
    return (
        ClauseRow(
            "theorem52_prime_level_constant_product",
            "prime-level constant-product/root-descent theorem",
            "rigidity and root-descent context",
            "nonzero constant legal quotient-C4 row or scalar-fixed finite row theorem",
            "reject_as_priority1_closer_keep_as_context",
        ),
        ClauseRow(
            "lemma61_distribution_formula",
            "distribution/q-expansion formula",
            "full-fiber order/distribution support",
            "one legal support-156 row plus finite scalar-fixing identity",
            "helper_not_priority1_closer",
        ),
        ClauseRow(
            "theorem62_x1n_siegel_product_legality",
            "X_1(N) Siegel-product sufficient condition and order formula",
            "H0/conductor-39 source legality certificate",
            "finite value/divisor/additive theorem for the legal row",
            "source_certified_value_theorem_missing",
        ),
        ClauseRow(
            "section7_ramanujan_value_evaluation",
            "Ramanujan cubic continued-fraction value evaluation",
            "example of value evaluation after a different generator setup",
            "one of the four legal H0/conductor-39 support-156 rows",
            "context_not_priority1_closer",
        ),
        ClauseRow(
            "section9_ray_class_generators",
            "ray-class singular-value generators",
            "class-field generator vocabulary",
            "DANGER3 finite row identity with Norm_156(Y_507) boundary",
            "context_not_priority1_closer",
        ),
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], SourceProfile, tuple[ClauseRow, ...], bool]:
    markers = evidence_markers(root)
    profile = source_profile(root)
    rows = clause_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and profile.row_ok
        and len(rows) == 5
        and sum("priority1_closer" in row.decision for row in rows) >= 4
        and sum(row.decision == "source_certified_value_theorem_missing" for row in rows) == 1
    )
    return markers, profile, rows, row_ok


def main() -> int:
    root = research_root()
    markers, profile, rows, row_ok = build_check(root)
    print("p25 v2 Koo-Shin priority-1 top-row falsifier")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"raw_source_available={int(profile.raw_source_available)}")
    print(f"evidence_fallback_used={int(profile.evidence_fallback_used)}")
    print(f"present_surfaces={len(profile.present_surfaces)}")
    for surface in profile.present_surfaces:
        print(f"  surface={surface}")
    print(f"absent_closer_terms={len(profile.absent_closer_terms)}")
    for term in profile.absent_closer_terms:
        print(f"  absent={term}")
    print(f"helper_terms_present={len(profile.helper_terms_present)}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    present_surface={row.present_surface}")
        print(f"    useful_as={row.useful_as}")
        print(f"    priority1_missing={row.priority1_missing}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"clause_rows={len(rows)}")
    print("current_koo_shin_priority1_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_koo_shin_priority1_toprow_falsifier_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
