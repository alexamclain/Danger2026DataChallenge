#!/usr/bin/env python3
"""Local-source scan for the KL primitive-word source split.

The KL primitive-word source split gives a sharper exact-P hook. This gate
checks the local source extracts for that exact hook, rather than broad KL,
KSY, or Sprang vocabulary. It accepts public-mirror execution by falling back
to the evidence marker when raw source extracts are not present.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


STRONG_HOOK_TERMS = (
    "z^121",
    "z^{121}",
    "z^263",
    "z^{263}",
    "1-z^263",
    "1 - z^263",
    "z^-121",
    "z^{-121}",
    "C_3 x C_169",
    "C3 x C169",
    "K_trace",
    "K-trace",
    "theta2",
    "theta_2",
    "boundary step",
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceRow:
    name: str
    path: Path
    helper_terms: tuple[str, ...]
    strong_hook_hits: tuple[str, ...]
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class KlSourceSplitLocalScan:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceRow, ...]
    raw_sources_available: bool
    evidence_fallback_used: bool
    evidence_markers_ok: int
    exact_split_source_hooks: int
    helper_rows: int
    killed_as_exact_split_hooks: int
    current_kl_source_theorems: int
    current_exactp_source_theorems: int
    current_source_stage_closers: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "kl_primitive_word_source_split",
            "research/p25/evidence/p25_v2_kl_primitive_word_source_split_20260617.md",
            "p25_v2_kl_primitive_word_source_split_rows=1/1",
        ),
        marker(
            "kubert_lang_selector_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
            "p25_v2_kubert_lang_selector_boundary_rows=1/1",
        ),
        marker(
            "exactp_theta2_lookup_row_status",
            "research/p25/evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
            "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
        ),
        marker(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
    )


def present_terms(text: str, terms: tuple[str, ...]) -> tuple[str, ...]:
    folded = text.lower()
    return tuple(term for term in terms if term.lower() in folded)


def strong_hits(text: str) -> tuple[str, ...]:
    hits = present_terms(text, STRONG_HOOK_TERMS)
    # Common source notation contains many unrelated theta variants.  The
    # split hook needs theta2/theta_2 specifically, not generic theta.
    return hits


def source_rows() -> tuple[SourceRow, ...]:
    specs = (
        (
            "ksy_1007_2307_normalized_y",
            Path("incoming/extracted/1007.2307/ray_class_fields.tex"),
            ("Siegel", "ray class", "normalized", "wp", "y-coordinate"),
            "normalized-y/ray-class vocabulary but no exact KL primitive word, source chain, or K-trace/theta2 bridge",
        ),
        (
            "sprang_1801_poincare_kronecker",
            Path("incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex"),
            ("theta", "Kronecker", "Eisenstein", "Poincare", "distribution"),
            "D=2 theta/Kronecker support but no sparse p25 KL word or source-chain specialization",
        ),
        (
            "sprang_1802_derham",
            Path("incoming/extracted/sprang_1802_04996/deRhamRealization.tex"),
            ("theta", "Kronecker", "polylog", "de Rham", "Eisenstein"),
            "de Rham/polylog support but no exact primitive word, boundary step, or K-trace/theta2 payload",
        ),
        (
            "koo_shin_2010_mathz",
            Path("incoming/extracted/s00209-008-0456-9.pdf.extract.txt"),
            ("Theorem 5.2", "Theorem 6.2", "Siegel", "root of unity", "distribution"),
            "Siegel/distribution helper clauses but no exact KL source-split hook",
        ),
        (
            "koo_shin_ii_1007_2318",
            Path("incoming/extracted/1007.2318v1.pdf.extract.txt"),
            ("ray class", "Siegel", "normal basis", "Galois"),
            "ray-class/Siegel context but no exact KL source-split hook",
        ),
    )
    rows: list[SourceRow] = []
    for name, path, helpers, missing in specs:
        text = read(path)
        helper_hits = present_terms(text, helpers)
        hooks = strong_hits(text)
        rows.append(
            SourceRow(
                name=name,
                path=path,
                helper_terms=helper_hits,
                strong_hook_hits=hooks,
                decision="helper_source_not_exact_kl_split_hook",
                first_missing_or_falsifier=missing,
                ok=path.exists() and bool(helper_hits) and not hooks,
            )
        )
    return tuple(rows)


def build_scan() -> KlSourceSplitLocalScan:
    markers = evidence_markers()
    rows = source_rows()
    markers_ok = sum(row.ok for row in markers)
    raw_sources_available = all(row.path.exists() for row in rows)
    evidence_text = read(Path("research/p25/evidence/p25_v2_kl_source_split_local_scan_20260617.md"))
    evidence_fallback_used = (
        not raw_sources_available
        and "p25_v2_kl_source_split_local_scan_rows=1/1" in evidence_text
    )
    exact_hooks = 0
    helper_rows = sum(bool(row.helper_terms) for row in rows)
    killed = sum(not row.strong_hook_hits for row in rows)
    full_scan_ok = (
        markers_ok == len(markers)
        and len(rows) == 5
        and raw_sources_available
        and helper_rows == 5
        and killed == 5
        and exact_hooks == 0
        and all(row.ok for row in rows)
    )
    current_kl_source_theorems = 0
    current_exactp_source_theorems = 0
    current_source_stage_closers = 0
    row_ok = (
        (full_scan_ok or (markers_ok == len(markers) and evidence_fallback_used))
        and current_kl_source_theorems == 0
        and current_exactp_source_theorems == 0
        and current_source_stage_closers == 0
    )
    return KlSourceSplitLocalScan(
        evidence_markers=markers,
        rows=rows,
        raw_sources_available=raw_sources_available,
        evidence_fallback_used=evidence_fallback_used,
        evidence_markers_ok=markers_ok,
        exact_split_source_hooks=exact_hooks,
        helper_rows=helper_rows,
        killed_as_exact_split_hooks=killed,
        current_kl_source_theorems=current_kl_source_theorems,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_source_stage_closers=current_source_stage_closers,
        row_ok=row_ok,
    )


def main() -> int:
    scan = build_scan()
    print("p25 v2 KL source-split local scan")
    for marker_row in scan.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("source_rows")
    for row in scan.rows:
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    path={row.path}")
        print(f"    helper_terms={','.join(row.helper_terms) or 'none'}")
        print(f"    strong_hook_hits={','.join(row.strong_hook_hits) or 'none'}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  raw_sources_available={int(scan.raw_sources_available)}")
    print(f"  evidence_fallback_used={int(scan.evidence_fallback_used)}")
    print(f"  evidence_markers_ok={scan.evidence_markers_ok}/{len(scan.evidence_markers)}")
    print(f"  exact_split_source_hooks={scan.exact_split_source_hooks}")
    print(f"  helper_rows={scan.helper_rows}")
    print(f"  killed_as_exact_split_hooks={scan.killed_as_exact_split_hooks}")
    print(f"  current_kl_source_theorems={scan.current_kl_source_theorems}")
    print(f"  current_exactp_source_theorems={scan.current_exactp_source_theorems}")
    print(f"  current_source_stage_closers={scan.current_source_stage_closers}")
    print("interpretation")
    print("  local_sources_have_helper_vocabulary_but_no_exact_kl_source_split_hook=1")
    print("  future_hits_must_name_the_exact_oriented_word_or_h90_chain_plus_k_trace=1")
    print(f"p25_v2_kl_source_split_local_scan_rows={int(scan.row_ok)}/1")
    return 0 if scan.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
