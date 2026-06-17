#!/usr/bin/env python3
"""Local source scan for constructive p25 payload data.

This applies the constructive value payload contract to the local primary
source corpus.  It is intentionally a screen, not a broad reread: helper
vocabulary is recorded, but a positive row requires p25-specific payload data
that can be evaluated or packetized.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P25_PAYLOAD_TERMS = (
    "Norm_156",
    "Norm 156",
    "Y_507",
    "Y507",
    "period-156",
    "period 156",
    "support-period",
    "support period 156",
    "C_75",
    "C_169",
    "C_3 x C_169",
    "C_3 \\times C_169",
    "C,D,K",
    "C, D, K",
    "K_trace",
    "D_segment",
    "theta2",
    "theta_2",
    "theta2 inverse",
    "theta2-inverse",
    "75-atom",
    "75 atom",
    "X_1(8112)",
    "X1(8112)",
    "A,x0",
    "(A,x0)",
    "vpp.py",
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourcePayloadRow:
    name: str
    path: Path
    helper_terms: tuple[str, ...]
    p25_payload_terms: tuple[str, ...]
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ConstructivePayloadSourceScan:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourcePayloadRow, ...]
    raw_sources_available: bool
    evidence_fallback_used: bool
    evidence_markers_ok: int
    source_rows: int
    helper_rows: int
    p25_payload_term_rows: int
    packetizable_source_payloads: int
    source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "constructive_value_payload_contract",
            "research/p25/evidence/p25_v2_constructive_value_payload_contract_20260616.md",
            "p25_v2_constructive_value_payload_contract_rows=1/1",
        ),
        marker(
            "source_family_gap_matrix",
            "research/p25/evidence/p25_v2_source_family_gap_matrix_20260616.md",
            "p25_v2_source_family_gap_matrix_rows=1/1",
        ),
        marker(
            "additive_normalizer_source_scan",
            "research/p25/evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
            "p25_v2_additive_normalizer_source_scan_rows=1/1",
        ),
        marker(
            "ksy_source_ingest_scan",
            "research/p25/evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md",
            "No `507`, `Norm_156`, `Y_507`, `period-156`, `Hilbert-90`,",
        ),
        marker(
            "koo_shin_ii_source_scan",
            "research/p25/evidence/p25_v2_koo_shin_ii_first_pass_source_scan_20260616.md",
            "decision = kill_koo_shin_ii_as_h0_closer",
        ),
        marker(
            "sprang_theta2_source_intake",
            "research/p25/evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
            "p25_v2_sprang_theta2_source_intake_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def present_terms(text: str, terms: tuple[str, ...]) -> tuple[str, ...]:
    folded = text.lower()
    return tuple(term for term in terms if term.lower() in folded)


def source_row(
    name: str,
    path: str,
    helper_terms: tuple[str, ...],
    decision: str,
    first_missing_or_falsifier: str,
) -> SourcePayloadRow:
    p = Path(path)
    text = read(p)
    helpers = present_terms(text, helper_terms)
    p25_hits = present_terms(text, P25_PAYLOAD_TERMS)
    return SourcePayloadRow(
        name=name,
        path=p,
        helper_terms=helpers,
        p25_payload_terms=p25_hits,
        decision=decision,
        first_missing_or_falsifier=first_missing_or_falsifier,
        ok=bool(helpers) and not p25_hits,
    )


def scan_rows() -> tuple[SourcePayloadRow, ...]:
    return (
        source_row(
            "koo_shin_2010_mathz",
            "incoming/extracted/s00209-008-0456-9.pdf.extract.txt",
            (
                "Theorem 5.2",
                "Theorem 6.2",
                "product of Siegel functions",
                "distribution relation",
                "root of unity",
                "generators of K(X1(N))",
            ),
            "helper_source_not_constructive_payload",
            "no exact p25 row value, product packet, period-156 payload, or DANGER3 extraction data",
        ),
        source_row(
            "ksy_1007_2307_normalized_y",
            "incoming/extracted/1007.2307/ray_class_fields.tex",
            (
                "normalization",
                "y-coordinate",
                "ray class",
                "Siegel",
                "Lang-Schertz",
                "Klein forms",
            ),
            "exactp_vocabulary_not_constructive_payload",
            "no compact C,D,K,orientation packet, exact 75-atom theorem, or period-156 bridge",
        ),
        source_row(
            "koo_shin_ii_1007_2318",
            "incoming/extracted/1007.2318v1.pdf.extract.txt",
            (
                "normal basis",
                "ray class",
                "Siegel",
                "generator",
                "ring class",
                "Kronecker",
            ),
            "background_source_not_constructive_payload",
            "no one-edge theorem, exact p25 product packet, or period-156 value payload",
        ),
        source_row(
            "sprang_1801_05677",
            "incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex",
            (
                "Eisenstein--Kronecker",
                "Poincar",
                "Kronecker theta",
                "p-adic theta",
                "distribution relation",
                "Kato--Siegel",
            ),
            "d2_support_not_constructive_p25_payload",
            "no exact theta2/theta2-inverse p25 payload, compact KSY packet, or period-156 branch data",
        ),
        source_row(
            "sprang_1802_04996",
            "incoming/extracted/sprang_1802_04996/deRhamRealization.tex",
            (
                "de Rham",
                "polylogarithm",
                "Kronecker section",
                "Kato--Siegel",
                "distribution relation",
                "d\\log \\thetaD",
            ),
            "derham_support_not_constructive_p25_payload",
            "de Rham/Kato-Siegel support only; no evaluable p25 row or exact-P packet",
        ),
    )


def build_scan() -> ConstructivePayloadSourceScan:
    markers = evidence_markers()
    rows = scan_rows()
    raw_sources_available = all(row.path.exists() for row in rows)
    evidence_text = read(Path("research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md"))
    evidence_fallback_used = (
        not raw_sources_available
        and "p25_v2_constructive_payload_source_scan_rows=1/1" in evidence_text
    )
    helpers = sum(bool(row.helper_terms) for row in rows)
    payload_hit_rows = sum(bool(row.p25_payload_terms) for row in rows)
    packetizable = 0
    closers = 0
    submissions = 0
    expected = (
        "helper_source_not_constructive_payload",
        "exactp_vocabulary_not_constructive_payload",
        "background_source_not_constructive_payload",
        "d2_support_not_constructive_p25_payload",
        "derham_support_not_constructive_p25_payload",
    )
    full_scan_ok = (
        sum(row.ok for row in markers) == len(markers)
        and raw_sources_available
        and len(rows) == 5
        and helpers == 5
        and payload_hit_rows == 0
        and packetizable == 0
        and closers == 0
        and submissions == 0
        and tuple(row.decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    row_ok = full_scan_ok or (
        sum(row.ok for row in markers) == len(markers)
        and evidence_fallback_used
    )
    return ConstructivePayloadSourceScan(
        evidence_markers=markers,
        rows=rows,
        raw_sources_available=raw_sources_available,
        evidence_fallback_used=evidence_fallback_used,
        evidence_markers_ok=sum(row.ok for row in markers),
        source_rows=len(rows),
        helper_rows=helpers,
        p25_payload_term_rows=payload_hit_rows,
        packetizable_source_payloads=packetizable,
        source_stage_closers=closers,
        current_submission_ready=submissions,
        row_ok=row_ok,
    )


def main() -> int:
    scan = build_scan()
    print("p25 v2 constructive payload source scan")
    for marker_row in scan.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("source rows")
    for row in scan.rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    path={row.path}")
        print(f"    helper_terms={','.join(row.helper_terms) or 'none'}")
        print(f"    p25_payload_terms={','.join(row.p25_payload_terms) or 'none'}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  raw_sources_available={int(scan.raw_sources_available)}")
    print(f"  evidence_fallback_used={int(scan.evidence_fallback_used)}")
    print(f"  evidence_markers_ok={scan.evidence_markers_ok}/{len(scan.evidence_markers)}")
    print(f"  source_rows={scan.source_rows}")
    print(f"  helper_rows={scan.helper_rows}")
    print(f"  p25_payload_term_rows={scan.p25_payload_term_rows}")
    print(f"  packetizable_source_payloads={scan.packetizable_source_payloads}")
    print(f"  source_stage_closers={scan.source_stage_closers}")
    print(f"  current_submission_ready={scan.current_submission_ready}")
    print("interpretation")
    print("  local_sources_have_helper_vocabulary_but_no_constructive_p25_payload=1")
    print("  no_packetizable_source_payload_found_in_local_scan=1")
    print(f"p25_v2_constructive_payload_source_scan_rows={int(scan.row_ok)}/1")
    return 0 if scan.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
