#!/usr/bin/env python3
"""Validate the external finite-normalization scout for p25."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MARKER = "p25_v2_external_finite_normalization_scout_rows=1/1"

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_kato_siegel_divisor_scout_20260617.md",
        "p25_v2_kato_siegel_divisor_scout_rows=1/1",
    ),
    (
        "evidence/p25_v2_external_source_delta_20260617.md",
        "p25_v2_external_source_delta_20260617_rows=1/1",
    ),
    (
        "evidence/p25_v2_local_source_hook_coverage_audit_20260617.md",
        "p25_v2_local_source_hook_coverage_audit_rows=1/1",
    ),
)

SOURCE_URLS = (
    "https://swc-math.github.io/notes/files/01MazurPW.pdf",
    "https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4",
    "https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_11",
    "https://perso.ens-lyon.fr/francois.brunault/recherche/reg_siegel.pdf",
    "https://hdaniels.people.amherst.edu/Uniformity.pdf",
)

REQUIRED_FRAGMENTS = (
    "kato_siegel_canonical_thetaD",
    "kubert_lang_siegel_unit_generators",
    "siegel_robert_class_field_units",
    "brunault_siegel_unit_regulators",
    "daniels_modular_curve_models",
    "support_canonical_divisor_not_p25_row_payload",
    "support_generators_not_finite_normalizer",
    "support_class_field_units_not_challenge_row",
    "support_regulator_not_finite_fp_payload",
    "support_model_computation_not_p25_theorem",
    "finite_normalization_closers = 0",
    MARKER,
)


@dataclass(frozen=True)
class SourceRow:
    name: str
    useful: str
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
            name="kato_siegel_canonical_thetaD",
            useful="canonical theta_D divisor and isogeny/base-change normalization",
            missing="p25 support-156 row selector, Norm_156(Y_507) row boundary, and finite F_p payload",
            decision="support_canonical_divisor_not_p25_row_payload",
        ),
        SourceRow(
            name="kubert_lang_siegel_unit_generators",
            useful="generator, q-expansion, and root-of-q-product framework for modular units",
            missing="selected p25 row theorem plus scalar-fixed finite value/additive normalizer",
            decision="support_generators_not_finite_normalizer",
        ),
        SourceRow(
            name="siegel_robert_class_field_units",
            useful="values of modular functions defining units in class fields",
            missing="non-CM DANGER3 finite identity or p25 finite row theorem over F_p",
            decision="support_class_field_units_not_challenge_row",
        ),
        SourceRow(
            name="brunault_siegel_unit_regulators",
            useful="explicit logarithmic/regulator formulas for Siegel units",
            missing="row-selected finite F_p value, additive telescoping payload, or period-156 branch bridge",
            decision="support_regulator_not_finite_fp_payload",
        ),
        SourceRow(
            name="daniels_modular_curve_models",
            useful="worked use of Siegel functions and modular units to compute modular-curve models and j-maps",
            missing="p25 X1(8112)/X1(16) extraction payload or source theorem for one support-156 row",
            decision="support_model_computation_not_p25_theorem",
        ),
    )


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        ok += int(path.exists() and marker in path.read_text(errors="replace"))
    return ok, len(EVIDENCE_MARKERS)


def main() -> int:
    root = research_root()
    note = root / "evidence/p25_v2_external_finite_normalization_scout_20260617.md"
    note_text = note.read_text(errors="replace") if note.exists() else ""
    evidence_ok, evidence_total = evidence_markers_ok(root)
    source_url_ok = sum(url in note_text for url in SOURCE_URLS)
    fragment_ok = sum(fragment in note_text for fragment in REQUIRED_FRAGMENTS)
    source_rows = rows()
    support_rows = sum(row.decision.startswith("support_") for row in source_rows)
    finite_normalization_closers = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == evidence_total
        and source_url_ok == len(SOURCE_URLS)
        and fragment_ok == len(REQUIRED_FRAGMENTS)
        and len(source_rows) == 5
        and support_rows == 5
        and finite_normalization_closers == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 external finite-normalization scout")
    print(f"evidence_markers_ok={evidence_ok}/{evidence_total}")
    print(f"source_urls_ok={source_url_ok}/{len(SOURCE_URLS)}")
    print(f"note_fragments_ok={fragment_ok}/{len(REQUIRED_FRAGMENTS)}")
    print("rows")
    for row in source_rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    useful={row.useful}")
        print(f"    missing={row.missing}")
    print("counts")
    print(f"source_rows={len(source_rows)}")
    print(f"support_rows={support_rows}")
    print(f"finite_normalization_closers={finite_normalization_closers}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"{MARKER if row_ok else 'p25_v2_external_finite_normalization_scout_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
