#!/usr/bin/env python3
"""Validate the Kato-Siegel divisor-source scout.

This gate records a narrow literature/proof pass against the live primary row
ask.  Kato-Siegel functions are close to the desired shape because they give
canonical modular units with prescribed divisors.  The p25 close still needs a
row-selected finite F_p value/additive payload and challenge framing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceRow:
    name: str
    source_url: str
    useful_content: str
    p25_gap: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "live_theorem_ask",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "constructive_payload_contract",
        "evidence/p25_v2_constructive_value_payload_contract_20260616.md",
        "p25_v2_constructive_value_payload_contract_rows=1/1",
    ),
    (
        "source_snippet_intake",
        "evidence/p25_v2_source_snippet_intake_20260616.md",
        "p25_v2_source_snippet_intake_rows=1/1",
    ),
    (
        "additive_normalization",
        "evidence/p25_v2_additive_normalization_contract_20260616.md",
        "p25_v2_additive_normalization_contract_rows=1/1",
    ),
    (
        "source_stage_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    rows: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        rows.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(rows)


def source_rows() -> tuple[SourceRow, ...]:
    return (
        SourceRow(
            "scholl_kato_siegel_functions",
            "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            "canonical Kato-Siegel functions with prescribed divisors and norm compatibility",
            "does not select the p25 support-156 row or give finite F_p scalar/value data",
            "repair_divisor_theorem_not_finite_row_payload",
        ),
        SourceRow(
            "beilinson_kato_distribution_note",
            "https://arxiv.org/pdf/2311.14620",
            "constructs functions with explicit torsion-point divisors using Kato-Siegel functions",
            "divisor construction is not an evaluable p25 row value and warns against overclaiming canonical form",
            "repair_divisor_only_not_source_stage_close",
        ),
        SourceRow(
            "koo_robert_shin_yoon_siegel_invariants",
            "https://arxiv.org/pdf/1508.05602",
            "records Siegel-Ramachandra invariant value and class-field/Galois-action language",
            "class-field generation/special-value language is not the p25 support-156 finite row theorem",
            "support_value_framework_not_p25_hook",
        ),
        SourceRow(
            "beeson_roots_of_modular_units",
            "https://www.sas.rochester.edu/mth/people/faculty/tucker-amanda/assets/pdf/roots_of_modular_units.pdf",
            "bounds the level of a modular-unit root when such a root is again modular",
            "root-level control does not choose the p25 row root/sign or finite scalar",
            "support_root_guardrail_not_closer",
        ),
        SourceRow(
            "kubert_lang_units",
            "https://eudml.org/doc/162791",
            "anchors modular-unit generator theory and full-set vocabulary",
            "generator theory alone does not emit the row-specific finite theorem",
            "support_generator_framework_not_closer",
        ),
    )


def canonical_pages_ok(root: Path) -> bool:
    checks = (
        ("frontier.md", "Kato-Siegel divisor-source scout"),
        ("lanes/h0.md", "Kato-Siegel divisor-source scout"),
        ("lanes/conductor39.md", "Kato-Siegel divisor-source scout"),
    )
    for rel, needle in checks:
        path = root / rel
        if not path.exists() or needle not in path.read_text():
            return False
    return True


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[SourceRow, ...], bool]:
    markers = evidence_markers(root)
    rows = source_rows()
    decisions = tuple(row.decision for row in rows)
    row_ok = (
        all(marker.ok for marker in markers)
        and canonical_pages_ok(root)
        and len(rows) == 5
        and decisions
        == (
            "repair_divisor_theorem_not_finite_row_payload",
            "repair_divisor_only_not_source_stage_close",
            "support_value_framework_not_p25_hook",
            "support_root_guardrail_not_closer",
            "support_generator_framework_not_closer",
        )
        and all(row.source_url.startswith("https://") for row in rows)
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 Kato-Siegel divisor-source scout")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"canonical_pages_ok={int(canonical_pages_ok(root))}")
    print("source_rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    source={row.source_url}")
        print(f"    useful_content={row.useful_content}")
        print(f"    p25_gap={row.p25_gap}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"primary_external_sources_checked={len(rows)}")
    print("divisor_source_theorems_found=1")
    print("finite_p25_row_value_theorems_found=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_kato_siegel_divisor_scout_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
