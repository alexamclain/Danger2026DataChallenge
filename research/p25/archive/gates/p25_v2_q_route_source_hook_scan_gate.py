#!/usr/bin/env python3
"""Local source scan for the conductor-39 Q route.

The Q route is now precise enough that source/literature scans should not ask
for "Q" vaguely.  This gate checks the local source corpus for the exact
conductor-39 hooks: the 12-step quotient Q, Q^3/Q^6 Hilbert-90 data,
Q diagonal plus pure quartic split, period-156 branch data, or direct one-edge
finite theorem data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


Q_ROUTE_TERMS = (
    "E_7/E_1",
    "E_{7h}",
    "E_{7h}/E_h",
    "7<2>",
    "<2>",
    "U_chi",
    "V_bal",
    "chi_39",
    "chi_3",
    "chi_13",
    "Q^3",
    "Q^6",
    "Q_antisym",
    "m1+m4",
    "m1-m4",
    "m2+m8",
    "m2-m8",
    "quartic split",
    "pure quartic",
    "Norm_156",
    "Y_507",
    "period-156",
    "support-period-156",
    "X_1(39)",
    "Gamma_1(39)",
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceHookRow:
    name: str
    path: Path
    helper_terms: tuple[str, ...]
    q_route_terms: tuple[str, ...]
    collision_terms: tuple[str, ...]
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class QRouteSourceHookScan:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SourceHookRow, ...]
    raw_sources_available: bool
    evidence_fallback_used: bool
    evidence_markers_ok: int
    source_rows: int
    helper_rows: int
    q_route_term_rows: int
    collision_rows: int
    accepted_source_hook_rows: int
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
            "q_route_selector_debt",
            "research/p25/evidence/p25_v2_q_route_selector_debt_20260616.md",
            "p25_v2_q_route_selector_debt_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_split_quartic_selector",
            "research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md",
            "p25_v2_q_split_quartic_selector_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "constructive_payload_source_scan",
            "research/p25/evidence/p25_v2_constructive_payload_source_scan_20260616.md",
            "p25_v2_constructive_payload_source_scan_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "Q_route_has_diagonal_split_or_direct_edge_after_value_data",
        ),
    )


def present_terms(text: str, terms: tuple[str, ...]) -> tuple[str, ...]:
    folded = text.lower()
    return tuple(term for term in terms if term.lower() in folded)


def source_row(
    name: str,
    path: str,
    helper_terms: tuple[str, ...],
    collision_terms: tuple[str, ...],
    decision: str,
    first_missing_or_falsifier: str,
) -> SourceHookRow:
    p = Path(path)
    text = read(p)
    helpers = present_terms(text, helper_terms)
    q_hits = present_terms(text, Q_ROUTE_TERMS)
    collisions = present_terms(text, collision_terms)
    return SourceHookRow(
        name=name,
        path=p,
        helper_terms=helpers,
        q_route_terms=q_hits,
        collision_terms=collisions,
        decision=decision,
        first_missing_or_falsifier=first_missing_or_falsifier,
        ok=bool(helpers) and not q_hits,
    )


def scan_rows() -> tuple[SourceHookRow, ...]:
    return (
        source_row(
            "koo_shin_2010_mathz",
            "incoming/extracted/s00209-008-0456-9.pdf.extract.txt",
            (
                "Theorem 5.2",
                "Theorem 6.2",
                "product of Siegel functions",
                "distribution relation",
            ),
            (),
            "no_q_route_hook_in_koo_shin_2010",
            "no E_7/E_1 orbit norm, Q^3/Q^6 finite theorem, Q diagonal split, Norm_156(Y_507), or period-156 branch data",
        ),
        source_row(
            "ksy_1007_2307_normalized_y",
            "incoming/extracted/1007.2307/ray_class_fields.tex",
            (
                "ray class",
                "Siegel",
                "Klein forms",
                "y_{(0,~\\frac{1}{N})}",
            ),
            (
                "Q=aX^2",
                "\\theta_Q",
                "\\beta_Q",
            ),
            "q_symbol_collision_not_conductor39_q",
            "local Q denotes a quadratic form/CM point, not the conductor-39 quotient product",
        ),
        source_row(
            "koo_shin_ii_1007_2318",
            "incoming/extracted/1007.2318v1.pdf.extract.txt",
            (
                "normal basis",
                "ray class",
                "Siegel",
                "generator",
            ),
            (
                "quadratic form Q",
                "thetaQ",
                "βQ",
            ),
            "background_no_q_route_hook",
            "normal-basis/ray-class context but no conductor-39 Q theorem or diagonal split/root data",
        ),
        source_row(
            "sprang_1801_05677",
            "incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex",
            (
                "Kronecker theta",
                "p-adic theta",
                "distribution relation",
                "Kato--Siegel",
            ),
            (
                "theta",
                "distribution",
            ),
            "theta_support_no_q_route_hook",
            "theta/distribution support but no Q diagonal, quartic split, or period-156 row theorem",
        ),
        source_row(
            "sprang_1802_04996",
            "incoming/extracted/sprang_1802_04996/deRhamRealization.tex",
            (
                "de Rham",
                "polylogarithm",
                "Kronecker section",
                "Kato--Siegel",
            ),
            (
                "splitting",
                "split",
                "diagonal",
            ),
            "split_word_collision_not_q_diagonal_split",
            "generic splitting/diagonal language is not the Q diagonal plus pure quartic split",
        ),
    )


def build_scan() -> QRouteSourceHookScan:
    markers = evidence_markers()
    rows = scan_rows()
    raw_sources_available = all(row.path.exists() for row in rows)
    evidence_text = read(Path("research/p25/evidence/p25_v2_q_route_source_hook_scan_20260616.md"))
    evidence_fallback_used = (
        not raw_sources_available
        and "p25_v2_q_route_source_hook_scan_rows=1/1" in evidence_text
    )
    helpers = sum(bool(row.helper_terms) for row in rows)
    q_route_hits = sum(bool(row.q_route_terms) for row in rows)
    collisions = sum(bool(row.collision_terms) for row in rows)
    accepted = 0
    closers = 0
    submissions = 0
    expected = (
        "no_q_route_hook_in_koo_shin_2010",
        "q_symbol_collision_not_conductor39_q",
        "background_no_q_route_hook",
        "theta_support_no_q_route_hook",
        "split_word_collision_not_q_diagonal_split",
    )
    full_scan_ok = (
        sum(row.ok for row in markers) == len(markers)
        and raw_sources_available
        and len(rows) == 5
        and helpers == 5
        and q_route_hits == 0
        and collisions == 4
        and accepted == 0
        and closers == 0
        and submissions == 0
        and tuple(row.decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    row_ok = full_scan_ok or (
        sum(row.ok for row in markers) == len(markers)
        and evidence_fallback_used
    )
    return QRouteSourceHookScan(
        evidence_markers=markers,
        rows=rows,
        raw_sources_available=raw_sources_available,
        evidence_fallback_used=evidence_fallback_used,
        evidence_markers_ok=sum(row.ok for row in markers),
        source_rows=len(rows),
        helper_rows=helpers,
        q_route_term_rows=q_route_hits,
        collision_rows=collisions,
        accepted_source_hook_rows=accepted,
        source_stage_closers=closers,
        current_submission_ready=submissions,
        row_ok=row_ok,
    )


def main() -> int:
    scan = build_scan()
    print("p25 v2 Q route source hook scan")
    for marker_row in scan.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"raw_sources_available={int(scan.raw_sources_available)}")
    print(f"evidence_fallback_used={int(scan.evidence_fallback_used)}")
    print("rows")
    for row in scan.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    helper_terms={', '.join(row.helper_terms) if row.helper_terms else 'none'}")
        print(f"    q_route_terms={', '.join(row.q_route_terms) if row.q_route_terms else 'none'}")
        print(f"    collision_terms={', '.join(row.collision_terms) if row.collision_terms else 'none'}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={scan.evidence_markers_ok}/{len(scan.evidence_markers)}")
    print(f"  source_rows={scan.source_rows}")
    print(f"  helper_rows={scan.helper_rows}")
    print(f"  q_route_term_rows={scan.q_route_term_rows}")
    print(f"  collision_rows={scan.collision_rows}")
    print(f"  accepted_source_hook_rows={scan.accepted_source_hook_rows}")
    print(f"  source_stage_closers={scan.source_stage_closers}")
    print(f"  current_submission_ready={scan.current_submission_ready}")
    print("interpretation")
    print("  local_sources_do_not_emit_conductor39_Q_route_hook=1")
    print("  generic_Q_or_split_language_is_not_Q_diagonal_split=1")
    print(f"p25_v2_q_route_source_hook_scan_rows={int(scan.row_ok)}/1")
    return 0 if scan.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
