#!/usr/bin/env python3
"""Local source-window scan for the p25 KSY-y front doors.

This is a narrow scan over durable source evidence already pulled into the p25
workbench.  It does not try to rediscover every theorem; it checks the exact
windows or archived source-verdict rows that prior passes identified and
records whether any of them already hits the four positive front doors from
the source-family router.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_source_frontdoor_router_gate import profile_source_frontdoor_router


RESEARCH = Path("research/p25")
REPO = Path(__file__).resolve().parents[2]

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_source_frontdoor_router_20260614.md",
        "ksy_y_source_frontdoor_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_priority1_primary_source_verdict_20260613.md",
        "ksy_y_priority1_primary_source_verdict_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_koo_shin_source_clause_matrix_20260614.md",
        "ksy_y_h0_koo_shin_source_clause_matrix_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_koo_shin_ii_section5_delta_boundary_20260614.md",
        "ksy_y_koo_shin_ii_section5_delta_boundary_rows=1/1",
    ),
)


@dataclass(frozen=True)
class LocalSourceWindowRow:
    name: str
    source_family: str
    path: Path
    start_line: int
    end_line: int
    required_terms: tuple[str, ...]
    frontdoor_tested: str
    decision: str
    current_evidence: bool
    source_closing_hit: bool
    direct_closer_rejected: bool
    continue_as_context: bool
    external_exact_upgrade_needed: bool
    first_missing_or_falsifier: str
    next_action: str
    file_present: bool
    required_terms_present: bool
    ok: bool


@dataclass(frozen=True)
class FrontdoorLocalSourceScanProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    source_frontdoor_router_ok: bool
    rows: tuple[LocalSourceWindowRow, ...]
    row_count: int
    file_present_rows: int
    required_terms_present_rows: int
    current_evidence_rows: int
    local_source_closing_hits: int
    direct_closer_rejected_rows: int
    continue_as_context_rows: int
    external_exact_upgrade_rows: int
    source_certified_only_rows: int
    formula_or_distribution_context_rows: int
    generic_generation_context_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def read_window(path: Path, start_line: int, end_line: int) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(errors="replace").splitlines()
    return "\n".join(lines[start_line - 1 : end_line])


def terms_present(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def source_row(
    *,
    name: str,
    source_family: str,
    path: str,
    start_line: int,
    end_line: int,
    required_terms: tuple[str, ...],
    frontdoor_tested: str,
    decision: str,
    source_closing_hit: bool,
    direct_closer_rejected: bool,
    continue_as_context: bool,
    external_exact_upgrade_needed: bool,
    first_missing_or_falsifier: str,
    next_action: str,
) -> LocalSourceWindowRow:
    source_path = Path(path)
    window = read_window(source_path, start_line, end_line)
    present = source_path.exists() and source_path.stat().st_size > 0
    required = terms_present(window, required_terms)
    return LocalSourceWindowRow(
        name=name,
        source_family=source_family,
        path=source_path,
        start_line=start_line,
        end_line=end_line,
        required_terms=required_terms,
        frontdoor_tested=frontdoor_tested,
        decision=decision,
        current_evidence=True,
        source_closing_hit=source_closing_hit,
        direct_closer_rejected=direct_closer_rejected,
        continue_as_context=continue_as_context,
        external_exact_upgrade_needed=external_exact_upgrade_needed,
        first_missing_or_falsifier=first_missing_or_falsifier,
        next_action=next_action,
        file_present=present,
        required_terms_present=required,
        ok=present and required and not source_closing_hit,
    )


def scan_rows() -> tuple[LocalSourceWindowRow, ...]:
    return (
        source_row(
            name="sprang_1801_distribution_relation",
            source_family="Sprang 1801 Appendix distribution relation",
            path=str(REPO / "research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md"),
            start_line=22,
            end_line=29,
            required_terms=(
                "Sprang 1801 Appendix distribution relation",
                "PaperEisensteinPoincare.tex:1714-1798",
                "conditional_additive_section_distribution_not_exact_P",
            ),
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="conditional_additive_section_distribution_not_exact_P",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=True,
            external_exact_upgrade_needed=True,
            first_missing_or_falsifier="specialization to exact K-traced normalized-y product P",
            next_action="search only for a theorem that specializes this distribution to the exact p25 product",
        ),
        source_row(
            name="sprang_1802_d_variant_kato_siegel",
            source_family="Sprang 1802 D-variant / Kato-Siegel comparison",
            path=str(REPO / "research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md"),
            start_line=31,
            end_line=38,
            required_terms=(
                "Sprang 1802 D-variant",
                "deRhamRealization.tex:1100-1182",
                "conditional_derham_dlog_not_d2_product",
            ),
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="conditional_derham_dlog_not_d2_product",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=True,
            external_exact_upgrade_needed=True,
            first_missing_or_falsifier="D=2 multiplicative product identity for the exact p25 payload",
            next_action="keep dlog vocabulary; reject direct theta_D import unless a D=2 product theorem is supplied",
        ),
        source_row(
            name="ksy_1007_2307_normalized_y_formula",
            source_family="Koo-Shin-Yoon normalized-y formula",
            path=str(REPO / "research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md"),
            start_line=48,
            end_line=54,
            required_terms=(
                "KSY Equation (3.4)",
                "source.tex:420-466",
                "formula_language_not_product_distribution",
            ),
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="formula_language_not_product_distribution",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=True,
            external_exact_upgrade_needed=True,
            first_missing_or_falsifier="product/distribution theorem selecting all 75 p25 atoms",
            next_action="use as atom vocabulary only until upgraded to the exact 75-atom product theorem",
        ),
        source_row(
            name="ksy_1007_2307_single_generator",
            source_family="Koo-Shin-Yoon single torsion generator",
            path=str(REPO / "research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md"),
            start_line=64,
            end_line=70,
            required_terms=(
                "KSY Schertz-style primitive generator",
                "source.tex:1160-1280",
                "single_value_generator_not_k_traced_product",
            ),
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="single_value_generator_not_k_traced_product",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=False,
            external_exact_upgrade_needed=False,
            first_missing_or_falsifier="upgrade from one generator to exact K-traced p25 product",
            next_action="kill as direct closer; keep only as class-field generator context",
        ),
        source_row(
            name="koo_shin_2010_theorem62_h0_legality",
            source_family="Koo-Shin 2010 Theorem 6.2",
            path=str(REPO / "incoming/extracted/s00209-008-0456-9.pdf.extract.txt"),
            start_line=1988,
            end_line=2045,
            required_terms=("Theorem 6.2 A product", "is an element of K(X1(N))", "ordq"),
            frontdoor_tested="h0_exact_divisor_boundary_theorem",
            decision="source_certified_value_or_divisor_missing",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=True,
            external_exact_upgrade_needed=True,
            first_missing_or_falsifier="finite-field value/divisor theorem for one exact H0 product",
            next_action="ask only value-period156 or divisor/additive H0 upgrade questions",
        ),
        source_row(
            name="koo_shin_2010_theorem9x_generators",
            source_family="Koo-Shin 2010 ray-class generator clauses",
            path=str(REPO / "incoming/extracted/s00209-008-0456-9.pdf.extract.txt"),
            start_line=4316,
            end_line=4638,
            required_terms=("Theorem 9.8", "Theorem 9.10", "K(N)"),
            frontdoor_tested="generic_modular_unit_or_cm_generation",
            decision="reject_generic_generation_not_exact_p",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=False,
            external_exact_upgrade_needed=False,
            first_missing_or_falsifier="exact H0/conductor39/twisted/exact-75 finite identity",
            next_action="kill as direct closer; keep only as ray-class vocabulary",
        ),
        source_row(
            name="koo_shin_ii_section5_delta_context",
            source_family="Koo-Shin II Section 5 Delta/ring-class context",
            path=str(REPO / "incoming/extracted/1007.2318v1.pdf.extract.txt"),
            start_line=1516,
            end_line=1777,
            required_terms=("Theorem 5.1", "Lemma 5.3", "Theorem 5.4"),
            frontdoor_tested="generic_modular_unit_or_cm_generation",
            decision="reject_prime_power_delta_context_not_p25_product",
            source_closing_hit=False,
            direct_closer_rejected=True,
            continue_as_context=False,
            external_exact_upgrade_needed=False,
            first_missing_or_falsifier="mixed C3 x C169 p25 product or H0/conductor39 divisor identity",
            next_action="keep as prime-power class-field context only",
        ),
    )


def profile_frontdoor_local_source_scan() -> FrontdoorLocalSourceScanProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    frontdoor = profile_source_frontdoor_router()
    rows = scan_rows()
    file_present = sum(row.file_present for row in rows)
    required = sum(row.required_terms_present for row in rows)
    current = sum(row.current_evidence for row in rows)
    source_hits = sum(row.source_closing_hit for row in rows)
    direct_reject = sum(row.direct_closer_rejected for row in rows)
    context = sum(row.continue_as_context for row in rows)
    external_upgrade = sum(row.external_exact_upgrade_needed for row in rows)
    source_certified = sum(row.decision == "source_certified_value_or_divisor_missing" for row in rows)
    formula_context = sum(
        row.decision
        in {
            "conditional_additive_section_distribution_not_exact_P",
            "conditional_derham_dlog_not_d2_product",
            "formula_language_not_product_distribution",
        }
        for row in rows
    )
    generic_context = sum(
        row.decision
        in {
            "single_value_generator_not_k_traced_product",
            "reject_generic_generation_not_exact_p",
            "reject_prime_power_delta_context_not_p25_product",
        }
        for row in rows
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and frontdoor.row_ok
        and len(rows) == 7
        and file_present == 7
        and required == 7
        and current == 7
        and source_hits == 0
        and direct_reject == 7
        and context == 4
        and external_upgrade == 4
        and source_certified == 1
        and formula_context == 3
        and generic_context == 3
        and all(row.ok for row in rows)
    )
    return FrontdoorLocalSourceScanProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        source_frontdoor_router_ok=frontdoor.row_ok,
        rows=rows,
        row_count=len(rows),
        file_present_rows=file_present,
        required_terms_present_rows=required,
        current_evidence_rows=current,
        local_source_closing_hits=source_hits,
        direct_closer_rejected_rows=direct_reject,
        continue_as_context_rows=context,
        external_exact_upgrade_rows=external_upgrade,
        source_certified_only_rows=source_certified,
        formula_or_distribution_context_rows=formula_context,
        generic_generation_context_rows=generic_context,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_frontdoor_local_source_scan()
    print("p25 KSY-y front-door local source scan gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  source_frontdoor_router_ok={int(profile.source_frontdoor_router_ok)}")
    print("source_windows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: family={row.source_family} "
            f"path={row.path}:{row.start_line}-{row.end_line} "
            f"decision={row.decision} "
            f"file={int(row.file_present)} terms={int(row.required_terms_present)} "
            f"source_hit={int(row.source_closing_hit)} "
            f"context={int(row.continue_as_context)} "
            f"external_upgrade={int(row.external_exact_upgrade_needed)}"
        )
        print(f"    frontdoor={row.frontdoor_tested}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  file_present_rows={profile.file_present_rows}")
    print(f"  required_terms_present_rows={profile.required_terms_present_rows}")
    print(f"  current_evidence_rows={profile.current_evidence_rows}")
    print(f"  local_source_closing_hits={profile.local_source_closing_hits}")
    print(f"  direct_closer_rejected_rows={profile.direct_closer_rejected_rows}")
    print(f"  continue_as_context_rows={profile.continue_as_context_rows}")
    print(f"  external_exact_upgrade_rows={profile.external_exact_upgrade_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  formula_or_distribution_context_rows={profile.formula_or_distribution_context_rows}")
    print(f"  generic_generation_context_rows={profile.generic_generation_context_rows}")
    print("interpretation")
    print("  local_source_windows_have_zero_source_closing_frontdoor_hits=1")
    print("  current_positive_use_is_context_or_source_certification_only=1")
    print("  next_search_must_find_external_exact_divisor_or_period156_value_upgrade=1")
    print(f"ksy_y_frontdoor_local_source_scan_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("front-door local source scan regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
