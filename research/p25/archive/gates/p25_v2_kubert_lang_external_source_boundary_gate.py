#!/usr/bin/env python3
"""External-source boundary for the p25 Kubert-Lang exact-P route.

This gate records the narrow value of the external Kubert-Lang sources now
identified online: they are real source anchors for modular-unit generator and
congruence vocabulary, but they do not by themselves emit the p25 primitive
word or orientation packet.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceBoundaryRow:
    name: str
    source_kind: str
    url: str
    provides_general_kl_framework: bool
    provides_p25_primitive_word: bool
    provides_p25_orientation_or_theta2_payload: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class KubertLangExternalSourceBoundary:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceBoundaryRow, ...]
    evidence_markers_ok: int
    general_framework_rows: int
    p25_primitive_word_rows: int
    p25_orientation_payload_rows: int
    repair_rows: int
    accepted_future_hook_rows: int
    current_kl_source_theorems: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "kubert_lang_selector_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
            "p25_v2_kubert_lang_selector_boundary_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
        marker(
            "theta2_period156_support_contract",
            "research/p25/evidence/p25_v2_theta2_period156_support_contract_20260616.md",
            "p25_v2_theta2_period156_support_contract_rows=1/1",
        ),
        marker(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
    )


def source_rows() -> tuple[SourceBoundaryRow, ...]:
    return (
        SourceBoundaryRow(
            name="kubert_lang_iv_eudml_gdz",
            source_kind="primary bibliographic/full-text anchor",
            url="https://eudml.org/doc/162977",
            provides_general_kl_framework=True,
            provides_p25_primitive_word=False,
            provides_p25_orientation_or_theta2_payload=False,
            decision="source_anchor_general_generators_not_p25_hook",
            first_missing_or_falsifier="exact p25 primitive word z^121*(1+z+z^2)*(1-z^263) with orientation or theta2 payload",
            ok=True,
        ),
        SourceBoundaryRow(
            name="kubert_lang_modular_units_book",
            source_kind="primary book/source anchor",
            url="https://books.google.com/books/about/Modular_Units.html?id=BwwzmZjjVdgC",
            provides_general_kl_framework=True,
            provides_p25_primitive_word=False,
            provides_p25_orientation_or_theta2_payload=False,
            decision="book_anchor_general_theory_not_p25_hook",
            first_missing_or_falsifier="row-labeled mixed C3 x C169 selector, primitive bridge word, or accepted theta2/theta2-inverse payload",
            ok=True,
        ),
        SourceBoundaryRow(
            name="accessible_theorem_k_summary",
            source_kind="secondary theorem-K summary",
            url="https://afolsom.people.amherst.edu/Folsom-ModUnitsSel-MRL.pdf",
            provides_general_kl_framework=True,
            provides_p25_primitive_word=False,
            provides_p25_orientation_or_theta2_payload=False,
            decision="necessary_congruence_screen_not_selector_theorem",
            first_missing_or_falsifier="generic KL quadratic congruence conditions do not select the p25 six-term primitive word",
            ok=True,
        ),
        SourceBoundaryRow(
            name="modern_gamma1_generators_context",
            source_kind="secondary/contextual modern source",
            url="https://www.numdam.org/item/10.5802/ahl.160.pdf",
            provides_general_kl_framework=True,
            provides_p25_primitive_word=False,
            provides_p25_orientation_or_theta2_payload=False,
            decision="notation_context_not_exactp_source",
            first_missing_or_falsifier="conductor and orientation data for the p25 exact-P packet",
            ok=True,
        ),
        SourceBoundaryRow(
            name="future_exact_kl_hit",
            source_kind="required future hook",
            url="local:p25_exactp_primitive_word",
            provides_general_kl_framework=True,
            provides_p25_primitive_word=True,
            provides_p25_orientation_or_theta2_payload=True,
            decision="accepted_if_arithmetic_source_theorem_present",
            first_missing_or_falsifier="DANGER3 framing and extraction after theorem hit",
            ok=True,
        ),
    )


def build_boundary() -> KubertLangExternalSourceBoundary:
    markers = evidence_markers()
    rows = source_rows()
    general = sum(row.provides_general_kl_framework for row in rows)
    primitive = sum(row.provides_p25_primitive_word for row in rows)
    orientation_payload = sum(row.provides_p25_orientation_or_theta2_payload for row in rows)
    repairs = sum(row.decision != "accepted_if_arithmetic_source_theorem_present" for row in rows)
    accepted = sum(row.decision == "accepted_if_arithmetic_source_theorem_present" for row in rows)
    current_source_theorems = 0
    expected = (
        "source_anchor_general_generators_not_p25_hook",
        "book_anchor_general_theory_not_p25_hook",
        "necessary_congruence_screen_not_selector_theorem",
        "notation_context_not_exactp_source",
        "accepted_if_arithmetic_source_theorem_present",
    )
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 5
        and tuple(row.decision for row in rows) == expected
        and general == 5
        and primitive == 1
        and orientation_payload == 1
        and repairs == 4
        and accepted == 1
        and current_source_theorems == 0
        and all(row.ok for row in rows)
    )
    return KubertLangExternalSourceBoundary(
        evidence_markers=markers,
        rows=rows,
        evidence_markers_ok=sum(row.ok for row in markers),
        general_framework_rows=general,
        p25_primitive_word_rows=primitive,
        p25_orientation_payload_rows=orientation_payload,
        repair_rows=repairs,
        accepted_future_hook_rows=accepted,
        current_kl_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    boundary = build_boundary()
    print("p25 v2 Kubert-Lang external source boundary")
    for marker_row in boundary.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in boundary.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    source_kind={row.source_kind}")
        print(f"    url={row.url}")
        print(f"    general_kl={int(row.provides_general_kl_framework)}")
        print(f"    p25_word={int(row.provides_p25_primitive_word)}")
        print(f"    p25_orientation_payload={int(row.provides_p25_orientation_or_theta2_payload)}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={boundary.evidence_markers_ok}/{len(boundary.evidence_markers)}")
    print(f"  general_framework_rows={boundary.general_framework_rows}")
    print(f"  p25_primitive_word_rows={boundary.p25_primitive_word_rows}")
    print(f"  p25_orientation_payload_rows={boundary.p25_orientation_payload_rows}")
    print(f"  repair_rows={boundary.repair_rows}")
    print(f"  accepted_future_hook_rows={boundary.accepted_future_hook_rows}")
    print(f"  current_kl_source_theorems={boundary.current_kl_source_theorems}")
    print("interpretation")
    print("  external_kl_sources_are_framework_not_current_p25_hook=1")
    print("  exactp_kl_ask_is_the_rigid_primitive_word_plus_orientation_or_theta2_payload=1")
    print(f"p25_v2_kubert_lang_external_source_boundary_rows={int(boundary.row_ok)}/1")
    return 0 if boundary.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
