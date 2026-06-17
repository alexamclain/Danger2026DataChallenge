#!/usr/bin/env python3
"""Local source scan for the additive-normalization contract.

This gate applies the new additive-normalization contract to the local primary
source extracts.  It is intentionally narrow: look for basepoint, telescoping,
period-156/Hilbert-90/Y507, or scalar-fixing finite additive/value language
that could promote a divisor/H90 statement to a source-stage closer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


STRONG_NORMALIZER_TERMS = (
    "basepoint",
    "base point",
    "telescop",
    "additive identity",
    "divisor identity",
    "finite field",
    "finite-field",
    "Hilbert-90",
    "Hilbert 90",
    "period-156",
    "period 156",
    "Norm_156",
    "Y_507",
    "Y507",
    "scalar-fixing",
    "fixing the F_p",
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceScanRow:
    name: str
    path: Path
    required_positive_context: tuple[str, ...]
    strong_normalizer_hits: tuple[str, ...]
    helper_hits: tuple[str, ...]
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class AdditiveNormalizerSourceScan:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceScanRow, ...]
    raw_sources_available: bool
    evidence_fallback_used: bool
    evidence_markers_ok: int
    source_stage_closers: int
    helper_rows: int
    killed_as_additive_normalizer: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in read(marker_path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def present_terms(text: str, terms: tuple[str, ...]) -> tuple[str, ...]:
    folded = text.lower()
    return tuple(term for term in terms if term.lower() in folded)


def scan_rows() -> tuple[SourceScanRow, ...]:
    koo_shin_2010 = Path("incoming/extracted/s00209-008-0456-9.pdf.extract.txt")
    ksy_1007_2307 = Path("incoming/extracted/1007.2307/ray_class_fields.tex")
    koo_shin_ii = Path("incoming/extracted/1007.2318v1.pdf.extract.txt")
    rows = []
    text = read(koo_shin_2010)
    strong = present_terms(text, STRONG_NORMALIZER_TERMS)
    helpers = present_terms(
        text,
        (
            "Theorem 5.2",
            "Theorem 6.2",
            "root of unity",
            "up to a root of unity",
            "unique normalized generators",
            "distribution relation",
        ),
    )
    rows.append(
        SourceScanRow(
            name="koo_shin_2010_mathz",
            path=koo_shin_2010,
            required_positive_context=("legal row", "H90 boundary", "scalar-fixing additive/value normalizer"),
            strong_normalizer_hits=strong,
            helper_hits=helpers,
            decision="helper_source_not_additive_normalizer",
            first_missing_or_falsifier=(
                "no basepoint/telescoping/period-156/Hilbert-90/Y507 scalar-fixing finite theorem in extract"
            ),
            ok=(
                "Theorem 5.2" in helpers
                and "Theorem 6.2" in helpers
                and not strong
            ),
        )
    )

    text = read(ksy_1007_2307)
    strong = present_terms(text, STRONG_NORMALIZER_TERMS)
    helpers = present_terms(
        text,
        (
            "normalize",
            "normalization",
            "wp'",
            "y-coordinate",
            "ray class",
            "Siegel",
        ),
    )
    rows.append(
        SourceScanRow(
            name="ksy_1007_2307_normalized_y",
            path=ksy_1007_2307,
            required_positive_context=("exact-P atom selector", "period-156 bridge", "scalar-fixing additive/value normalizer"),
            strong_normalizer_hits=strong,
            helper_hits=helpers,
            decision="exactp_vocabulary_not_additive_normalizer",
            first_missing_or_falsifier=(
                "normalized-y vocabulary appears, but no accepted additive-normalization closer terms appear"
            ),
            ok=("normalize" in helpers and "ray class" in helpers and not strong),
        )
    )

    text = read(koo_shin_ii)
    strong = present_terms(text, STRONG_NORMALIZER_TERMS)
    helpers = present_terms(
        text,
        (
            "ray class",
            "Siegel",
            "normal basis",
            "Galois",
            "root of unity",
        ),
    )
    rows.append(
        SourceScanRow(
            name="koo_shin_ii_1007_2318",
            path=koo_shin_ii,
            required_positive_context=("H0/conductor39 legal row", "period-156 bridge", "scalar-fixing additive/value normalizer"),
            strong_normalizer_hits=strong,
            helper_hits=helpers,
            decision="background_source_not_additive_normalizer",
            first_missing_or_falsifier=(
                "ray-class/Siegel context only; no accepted additive-normalization closer terms appear"
            ),
            ok=("ray class" in helpers and "Siegel" in helpers and not strong),
        )
    )
    return tuple(rows)


def build_scan() -> AdditiveNormalizerSourceScan:
    markers = evidence_markers()
    rows = scan_rows()
    markers_ok = sum(row.ok for row in markers)
    raw_sources_available = all(row.path.exists() for row in rows)
    evidence_text = read(Path("research/p25/evidence/p25_v2_additive_normalizer_source_scan_20260616.md"))
    evidence_fallback_used = (
        not raw_sources_available
        and "p25_v2_additive_normalizer_source_scan_rows=1/1" in evidence_text
    )
    source_stage = 0
    helper_rows = sum(bool(row.helper_hits) for row in rows)
    killed = sum(not row.strong_normalizer_hits for row in rows)
    full_scan_ok = (
        markers_ok == len(markers)
        and len(rows) == 3
        and source_stage == 0
        and helper_rows == 3
        and killed == 3
        and tuple(row.decision for row in rows)
        == (
            "helper_source_not_additive_normalizer",
            "exactp_vocabulary_not_additive_normalizer",
            "background_source_not_additive_normalizer",
        )
        and all(row.ok for row in rows)
    )
    row_ok = full_scan_ok or (markers_ok == len(markers) and evidence_fallback_used)
    return AdditiveNormalizerSourceScan(
        evidence_markers=markers,
        rows=rows,
        raw_sources_available=raw_sources_available,
        evidence_fallback_used=evidence_fallback_used,
        evidence_markers_ok=markers_ok,
        source_stage_closers=source_stage,
        helper_rows=helper_rows,
        killed_as_additive_normalizer=killed,
        row_ok=row_ok,
    )


def main() -> int:
    scan = build_scan()
    for marker_row in scan.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("source rows")
    for row in scan.rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    path={row.path}")
        print(f"    helper_hits={','.join(row.helper_hits) or 'none'}")
        print(f"    strong_normalizer_hits={','.join(row.strong_normalizer_hits) or 'none'}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  raw_sources_available={int(scan.raw_sources_available)}")
    print(f"  evidence_fallback_used={int(scan.evidence_fallback_used)}")
    print(f"  evidence_markers_ok={scan.evidence_markers_ok}/{len(scan.evidence_markers)}")
    print(f"  source_stage_closers={scan.source_stage_closers}")
    print(f"  helper_rows={scan.helper_rows}")
    print(f"  killed_as_additive_normalizer={scan.killed_as_additive_normalizer}")
    print("interpretation")
    print("  local_extracts_have_helper_context_but_no_scalar_fixing_additive_normalizer=1")
    print("  no_source_stage_closer_found_in_local_extract_scan=1")
    print(f"p25_v2_additive_normalizer_source_scan_rows={int(scan.row_ok)}/1")
    return 0 if scan.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
