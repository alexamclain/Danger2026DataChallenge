#!/usr/bin/env python3
"""Validate the priority-1 source lookup capsule."""

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
class LookupRow:
    name: str
    source_family: str
    positive_hook: str
    first_falsifier: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "priority1_work_order",
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    (
        "priority1_candidate_sweep",
        "evidence/p25_v2_priority1_candidate_sweep_20260617.md",
        "p25_v2_priority1_candidate_sweep_rows=1/1",
    ),
    (
        "minimal_expert_ask",
        "evidence/p25_v2_minimal_expert_ask_20260616.md",
        "p25_v2_minimal_expert_ask_rows=1/1",
    ),
    (
        "first_pass_expert_intake",
        "evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
        "p25_v2_first_pass_expert_intake_packet_rows=1/1",
    ),
    (
        "source_stage_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    (
        "koo_shin_noncloser",
        "evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
        "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
    ),
    (
        "period156_value_hook",
        "evidence/p25_v2_period156_value_source_hook_20260616.md",
        "p25_v2_period156_value_source_hook_rows=1/1",
    ),
    (
        "q_route_source_hook_scan",
        "evidence/p25_v2_q_route_source_hook_scan_20260616.md",
        "p25_v2_q_route_source_hook_scan_rows=1/1",
    ),
    (
        "kubert_lang_selector_boundary",
        "evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
        "p25_v2_kubert_lang_selector_boundary_rows=1/1",
    ),
    (
        "schertz_scholl_external_boundary",
        "evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md",
        "p25_v2_schertz_scholl_external_source_boundary_rows=1/1",
    ),
    (
        "sprang_theta2_intake",
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
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
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def lookup_rows() -> tuple[LookupRow, ...]:
    return (
        LookupRow(
            "koo_shin_h0_or_conductor39_divisor_additive",
            "Koo-Shin 2010 / H0 / conductor 39",
            "finite scalar-fixed divisor/additive theorem for one legal row with Norm_156(Y_507) boundary",
            "Theorem 6.2 legality, Lemma 6.1 distribution, or Theorem 5.2 constant-product context without finite scalar-fixing identity",
            "search_as_priority1_frontdoor",
        ),
        LookupRow(
            "h0_y507_support_period156_value",
            "Koo-Shin / Schertz-Shin-Scholl value side",
            "support-period-156 finite value theorem for canonical H0 or Y_507 with branch/root/telescoping data",
            "ambient-period-780 value, mu_11 quotient, class-field generation, or value up to unspecified F_p^* scalar",
            "search_as_priority2_value_side",
        ),
        LookupRow(
            "conductor39_q_or_yang_h90_hook",
            "conductor 39 / Yang / Hilbert-90 / Q support",
            "finite Q or Q^3 theorem plus diagonal split/root, or direct mixed U_chi/W theorem normalizing to one edge",
            "Q source-only, Q^6 boundary-only, diagonal aggregate without pure quartic split, or split without oriented root/sign",
            "search_as_support_only_until_selector_paid",
        ),
        LookupRow(
            "quartic_or_row_labeled_normalizer",
            "row-labeled, reciprocal, quartic selector, or power-value presentations",
            "exact row label/phase/orientation or R_m^e value with inverse recovery, plus scalar-fixed finite theorem",
            "selector-only, unordered orbit, reciprocal with wrong boundary sign, or power value without row selector",
            "accept_only_if_normalizes_to_one_row",
        ),
        LookupRow(
            "kubert_lang_exactp_upstream",
            "Kubert-Lang / exact-P mixed selector",
            "theorem emitting the exact primitive word, mixed C_3 x C_169 selector, orientation, or accepted theta2 bridge",
            "generic modular-unit generation, exponent balance, or prime-power projection without the exact p25 selector",
            "keep_as_heavy_upstream_only",
        ),
        LookupRow(
            "sprang_theta2_sparse_packet",
            "Sprang / Kato-Siegel / theta2",
            "sparse p25 theta2 or theta2-inverse divisor-additive payload with period-156 branch and extraction bridge",
            "full distribution/kernel identity, D=2 support vocabulary, or theta language without sparse selector and branch data",
            "search_only_for_exact_specialization",
        ),
    )


def source_pages_ok(root: Path) -> bool:
    checks = (
        ("sources/koo-shin-2010.md", "source-certification asset, not yet a closer"),
        ("sources/kubert-lang.md", "not a direct closer on its own"),
        ("sources/schertz-scholl.md", "None of these currently closes p25 directly"),
        ("sources/sprang.md", "not the p25 closer as written"),
    )
    for rel, needle in checks:
        path = root / rel
        if not path.exists() or needle not in path.read_text():
            return False
    return True


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[LookupRow, ...], bool]:
    markers = evidence_markers(root)
    rows = lookup_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and source_pages_ok(root)
        and len(rows) == 6
        and sum(row.decision.startswith("search_as") for row in rows) == 3
        and sum("normalizes_to_one_row" in row.decision for row in rows) == 1
        and sum("heavy_upstream" in row.decision for row in rows) == 1
        and sum("exact_specialization" in row.decision for row in rows) == 1
        and all("source" not in row.decision or "only" in row.decision for row in rows)
    )
    return markers, rows, row_ok


def main() -> int:
    markers, rows, row_ok = build_check(research_root())
    print("p25 v2 priority-1 source lookup capsule")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"source_pages_ok={int(source_pages_ok(research_root()))}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    source_family={row.source_family}")
        print(f"    positive_hook={row.positive_hook}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"lookup_rows={len(rows)}")
    print("current_priority1_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_priority1_source_lookup_capsule_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
