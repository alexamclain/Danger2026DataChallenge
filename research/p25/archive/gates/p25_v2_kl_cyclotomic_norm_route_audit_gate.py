#!/usr/bin/env python3
"""Audit the Kubert-Lang cyclotomic-norm route against the p25 kernel."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


MARKER = "p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1"


@dataclass(frozen=True)
class Audit:
    evidence_markers_ok: int
    evidence_markers_total: int
    required_fragments_ok: int
    required_fragments_total: int
    row_ok: bool


EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    (
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    (
        "evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
        "p25_v2_kubert_lang_selector_boundary_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_primitive_word_source_split_20260617.md",
        "p25_v2_kl_primitive_word_source_split_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
)

REQUIRED_FRAGMENTS = (
    "Kubert-Lang cyclotomic-norm route is support, not a source-stage closer",
    "modular/Robert-unit norm and regulator-level theorem",
    "does not select one p25 support-156 row",
    "does not provide a scalar-fixed finite F_p value/additive payload",
    "does not recover exact-P without C,D,K,orientation or the 75-atom/theta2 selector",
    "current_source_stage_closers = 0",
    "current_exactp_upstream_theorems = 0",
    MARKER,
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def has_fragment(text: str, fragment: str) -> bool:
    compact_text = re.sub(r"\s+", " ", text)
    compact_fragment = re.sub(r"\s+", " ", fragment)
    return compact_fragment in compact_text


def main() -> int:
    root = research_root()
    evidence_ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        evidence_ok += int(path.exists() and marker in path.read_text())

    note = root / "evidence/p25_v2_kl_cyclotomic_norm_route_audit_20260617.md"
    note_text = note.read_text() if note.exists() else ""
    fragments_ok = sum(has_fragment(note_text, fragment) for fragment in REQUIRED_FRAGMENTS)
    row_ok = (
        evidence_ok == len(EVIDENCE_MARKERS)
        and fragments_ok == len(REQUIRED_FRAGMENTS)
    )
    audit = Audit(
        evidence_markers_ok=evidence_ok,
        evidence_markers_total=len(EVIDENCE_MARKERS),
        required_fragments_ok=fragments_ok,
        required_fragments_total=len(REQUIRED_FRAGMENTS),
        row_ok=row_ok,
    )
    print("p25 v2 KL cyclotomic norm route audit")
    print(f"evidence_markers_ok={audit.evidence_markers_ok}/{audit.evidence_markers_total}")
    print(f"required_fragments_ok={audit.required_fragments_ok}/{audit.required_fragments_total}")
    print(f"{MARKER if audit.row_ok else 'p25_v2_kl_cyclotomic_norm_route_audit_rows=0/1'}")
    return 0 if audit.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
