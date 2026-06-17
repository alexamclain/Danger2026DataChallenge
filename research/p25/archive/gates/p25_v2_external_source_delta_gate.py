#!/usr/bin/env python3
"""Validate the external source delta after the current theorem kernel."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MARKER = "p25_v2_external_source_delta_20260617_rows=1/1"

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
        "p25_v2_source_theorem_acceptance_automaton_rows=1/1",
    ),
    (
        "evidence/p25_v2_kato_siegel_divisor_scout_20260617.md",
        "p25_v2_kato_siegel_divisor_scout_rows=1/1",
    ),
    (
        "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
        "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
        "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
)

SOURCE_URLS = (
    "https://arxiv.org/html/2311.14620v2",
    "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
    "https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4",
    "https://link.springer.com/article/10.1007/s11139-019-00223-3",
    "https://ar5iv.labs.arxiv.org/html/1009.2253",
)

REQUIRED_FRAGMENTS = (
    "beilinson_kato_distributions_2025",
    "scholl_kato_euler_systems",
    "kubert_lang_siegel_units_generators",
    "koo_robert_shin_yoon_cm_siegel_invariants",
    "shin_siegel_ramachandra_generation",
    "support_distribution_not_p25_payload",
    "support_divisor_norm_not_scalar_fixed_row",
    "support_generator_not_selected_finite_identity",
    "repair_cm_class_field_not_challenge_finite_identity",
    "support_value_generator_not_period156_row",
    "current_external_source_stage_closers = 0",
    MARKER,
)


@dataclass(frozen=True)
class SourceRow:
    name: str
    source_kind: str
    useful_for: str
    missing: str
    decision: str


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def rows() -> tuple[SourceRow, ...]:
    return (
        SourceRow(
            name="beilinson_kato_distributions_2025",
            source_kind="Siegel distribution / modular-symbol package",
            useful_for="distribution and Manin-relation framework around Siegel units",
            missing="one p25 legal row, scalar-fixed finite F_p payload, and extraction bridge",
            decision="support_distribution_not_p25_payload",
        ),
        SourceRow(
            name="scholl_kato_euler_systems",
            source_kind="Kato-Siegel functions, modular units, norm relations",
            useful_for="divisor and norm-relation source language",
            missing="selected support-156 row plus finite additive/value/telescoping payload",
            decision="support_divisor_norm_not_scalar_fixed_row",
        ),
        SourceRow(
            name="kubert_lang_siegel_units_generators",
            source_kind="Siegel-unit generator theorem",
            useful_for="modular-unit generator and divisor vocabulary",
            missing="p25 row selector, arithmetic finite theorem, and scalar/branch normalization",
            decision="support_generator_not_selected_finite_identity",
        ),
        SourceRow(
            name="koo_robert_shin_yoon_cm_siegel_invariants",
            source_kind="CM-field theta/Siegel invariant generation",
            useful_for="CM class-field and Galois-action context",
            missing="non-CM DANGER3 finite identity or p25 row theorem over F_p",
            decision="repair_cm_class_field_not_challenge_finite_identity",
        ),
        SourceRow(
            name="shin_siegel_ramachandra_generation",
            source_kind="Siegel-Ramachandra ray-class generation",
            useful_for="value-generator source family",
            missing="support-period-156 H0/Y507 row theorem with branch/telescoping payload",
            decision="support_value_generator_not_period156_row",
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
    note = root / "evidence/p25_v2_external_source_delta_20260617.md"
    note_text = note.read_text() if note.exists() else ""
    evidence_ok, evidence_total = evidence_markers_ok(root)
    source_url_ok = sum(url in note_text for url in SOURCE_URLS)
    fragment_ok = sum(fragment in note_text for fragment in REQUIRED_FRAGMENTS)
    source_rows = rows()
    support_rows = sum(row.decision.startswith("support_") for row in source_rows)
    repair_rows = sum(row.decision.startswith("repair_") for row in source_rows)
    source_stage_closers = 0
    row_ok = (
        evidence_ok == evidence_total
        and source_url_ok == len(SOURCE_URLS)
        and fragment_ok == len(REQUIRED_FRAGMENTS)
        and len(source_rows) == 5
        and support_rows == 4
        and repair_rows == 1
        and source_stage_closers == 0
    )
    print("p25 v2 external source delta 20260617")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print(f"source_urls_ok={source_url_ok}/{len(SOURCE_URLS)}")
    print(f"note_fragments_ok={fragment_ok}/{len(REQUIRED_FRAGMENTS)}")
    print("rows")
    for row in source_rows:
        print(
            f"  {row.name}: decision={row.decision} "
            f"useful_for={row.useful_for} missing={row.missing}"
        )
    print("counts")
    print(f"external_source_rows={len(source_rows)}")
    print(f"support_rows={support_rows}")
    print(f"repair_rows={repair_rows}")
    print("current_external_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"{MARKER if row_ok else 'p25_v2_external_source_delta_20260617_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
