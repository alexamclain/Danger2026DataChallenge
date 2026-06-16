#!/usr/bin/env python3
"""External front-door source scout for the p25 KSY-y moonshot.

The local source scan says the workbench cache has no source-closing theorem.
This gate records the first external/front-door scout: which primary source
families remain useful, which are direct-closer kills, and what exact payload
each would still need to supply before entering the priority-1 intake.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_frontdoor_local_source_scan_gate import (
    profile_frontdoor_local_source_scan,
)
from p25_ksy_y_source_frontdoor_router_gate import profile_source_frontdoor_router


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_source_frontdoor_router_20260614.md",
        "ksy_y_source_frontdoor_router_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_frontdoor_local_source_scan_20260614.md",
        "ksy_y_frontdoor_local_source_scan_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ExternalFrontdoorSourceRow:
    name: str
    source_family: str
    source_url: str
    source_kind: str
    frontdoor_tested: str
    decision: str
    visible_source_closing_hit: bool
    promising_context: bool
    direct_closer_kill: bool
    needs_exact_p25_specialization: bool
    needs_period156_context: bool
    needs_arithmetic_source_theorem: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class ExternalFrontdoorSourceScoutProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    source_frontdoor_router_ok: bool
    local_source_scan_ok: bool
    rows: tuple[ExternalFrontdoorSourceRow, ...]
    row_count: int
    visible_source_closing_hits: int
    promising_context_rows: int
    direct_closer_kill_rows: int
    exact_p25_specialization_needed_rows: int
    period156_needed_rows: int
    arithmetic_source_needed_rows: int
    primary_or_publisher_source_rows: int
    exact_frontdoor_search_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def external_rows() -> tuple[ExternalFrontdoorSourceRow, ...]:
    return (
        ExternalFrontdoorSourceRow(
            name="kubert_lang_full_set_units",
            source_family="Kubert-Lang modular units",
            source_url="https://eudml.org/doc/162791",
            source_kind="primary_metadata",
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="context_modular_unit_generators_exact_mixed_product_missing",
            visible_source_closing_hit=False,
            promising_context=True,
            direct_closer_kill=False,
            needs_exact_p25_specialization=True,
            needs_period156_context=False,
            needs_arithmetic_source_theorem=True,
            first_missing_or_falsifier="exact mixed C3 x C169 exponent matrix or divisor identity for P/H0/U_chi",
            next_action="use only as modular-unit language until a p25-specific exponent/product theorem appears",
            ok=True,
        ),
        ExternalFrontdoorSourceRow(
            name="kubert_lang_modular_units_book",
            source_family="Kubert-Lang book-level modular-unit theory",
            source_url="https://books.google.com/books/about/Modular_Units.html?id=BwwzmZjjVdgC",
            source_kind="publisher_book_metadata",
            frontdoor_tested="generic_modular_unit_or_cm_generation",
            decision="broad_modular_unit_theory_not_exact_frontdoor",
            visible_source_closing_hit=False,
            promising_context=True,
            direct_closer_kill=True,
            needs_exact_p25_specialization=True,
            needs_period156_context=False,
            needs_arithmetic_source_theorem=True,
            first_missing_or_falsifier="one of the four exact p25 front-door identities",
            next_action="do not cite broad generator theory as closure; search inside it only for exact product identities",
            ok=True,
        ),
        ExternalFrontdoorSourceRow(
            name="schertz_klein_quotient_generators",
            source_family="Schertz elliptic-unit/Klein-form quotients",
            source_url="https://www.numdam.org/item/JTNB_1997__9_2_383_0.pdf",
            source_kind="primary_pdf",
            frontdoor_tested="exact_75_atom_value_or_divisor_theorem",
            decision="context_elliptic_unit_quotient_generator_exact_p25_identity_missing",
            visible_source_closing_hit=False,
            promising_context=True,
            direct_closer_kill=False,
            needs_exact_p25_specialization=True,
            needs_period156_context=True,
            needs_arithmetic_source_theorem=True,
            first_missing_or_falsifier="quotient identified with exact P/H0/U_chi plus period-156 or divisor boundary",
            next_action="continue only if a Schertz-style quotient is specialized to the p25 front-door payload",
            ok=True,
        ),
        ExternalFrontdoorSourceRow(
            name="scholl_kato_siegel_functions",
            source_family="Kato-Siegel theta / Robert generalization",
            source_url="https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            source_kind="primary_expository_pdf",
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="context_norm_compatible_kato_siegel_direct_D2_missing",
            visible_source_closing_hit=False,
            promising_context=True,
            direct_closer_kill=True,
            needs_exact_p25_specialization=True,
            needs_period156_context=False,
            needs_arithmetic_source_theorem=True,
            first_missing_or_falsifier="D=2 exact product/divisor specialization for the p25 normalized-y payload",
            next_action="keep Kato-Siegel divisor language; reject ordinary prime-to-6 theta_D import as direct closer",
            ok=True,
        ),
        ExternalFrontdoorSourceRow(
            name="ksy_normalized_y_ray_class_generators",
            source_family="Koo-Shin-Yoon normalized y ray-class generators",
            source_url="https://arxiv.org/abs/1007.2307",
            source_kind="primary_preprint",
            frontdoor_tested="exact_75_atom_product_divisor_theorem",
            decision="context_normalized_y_generator_exact_75_product_missing",
            visible_source_closing_hit=False,
            promising_context=True,
            direct_closer_kill=True,
            needs_exact_p25_specialization=True,
            needs_period156_context=True,
            needs_arithmetic_source_theorem=True,
            first_missing_or_falsifier="product/distribution theorem selecting all 75 p25 atoms with orientation",
            next_action="use as normalized-y vocabulary only unless upgraded to exact p25 product theorem",
            ok=True,
        ),
    )


def profile_external_frontdoor_source_scout() -> ExternalFrontdoorSourceScoutProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    frontdoor = profile_source_frontdoor_router()
    local_scan = profile_frontdoor_local_source_scan()
    rows = external_rows()
    visible_hits = sum(row.visible_source_closing_hit for row in rows)
    context = sum(row.promising_context for row in rows)
    kills = sum(row.direct_closer_kill for row in rows)
    exact = sum(row.needs_exact_p25_specialization for row in rows)
    period = sum(row.needs_period156_context for row in rows)
    source = sum(row.needs_arithmetic_source_theorem for row in rows)
    primary = sum(
        row.source_kind
        in {
            "primary_metadata",
            "primary_pdf",
            "primary_expository_pdf",
            "primary_preprint",
            "publisher_book_metadata",
        }
        for row in rows
    )
    exact_frontdoor = sum(
        row.frontdoor_tested
        in {
            "exact_75_atom_product_divisor_theorem",
            "exact_75_atom_value_or_divisor_theorem",
        }
        for row in rows
    )
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and frontdoor.row_ok
        and local_scan.row_ok
        and len(rows) == 5
        and visible_hits == 0
        and context == 5
        and kills == 3
        and exact == 5
        and period == 2
        and source == 5
        and primary == 5
        and exact_frontdoor == 4
        and all(row.ok for row in rows)
    )
    return ExternalFrontdoorSourceScoutProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        source_frontdoor_router_ok=frontdoor.row_ok,
        local_source_scan_ok=local_scan.row_ok,
        rows=rows,
        row_count=len(rows),
        visible_source_closing_hits=visible_hits,
        promising_context_rows=context,
        direct_closer_kill_rows=kills,
        exact_p25_specialization_needed_rows=exact,
        period156_needed_rows=period,
        arithmetic_source_needed_rows=source,
        primary_or_publisher_source_rows=primary,
        exact_frontdoor_search_rows=exact_frontdoor,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_external_frontdoor_source_scout()
    print("p25 KSY-y external front-door source scout gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  source_frontdoor_router_ok={int(profile.source_frontdoor_router_ok)}")
    print(f"  local_source_scan_ok={int(profile.local_source_scan_ok)}")
    print("external_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: source={row.source_family} kind={row.source_kind} "
            f"frontdoor={row.frontdoor_tested} decision={row.decision} "
            f"visible_hit={int(row.visible_source_closing_hit)} "
            f"context={int(row.promising_context)} kill={int(row.direct_closer_kill)} "
            f"exact_needed={int(row.needs_exact_p25_specialization)} "
            f"period156={int(row.needs_period156_context)}"
        )
        print(f"    url={row.source_url}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  visible_source_closing_hits={profile.visible_source_closing_hits}")
    print(f"  promising_context_rows={profile.promising_context_rows}")
    print(f"  direct_closer_kill_rows={profile.direct_closer_kill_rows}")
    print(f"  exact_p25_specialization_needed_rows={profile.exact_p25_specialization_needed_rows}")
    print(f"  period156_needed_rows={profile.period156_needed_rows}")
    print(f"  arithmetic_source_needed_rows={profile.arithmetic_source_needed_rows}")
    print(f"  primary_or_publisher_source_rows={profile.primary_or_publisher_source_rows}")
    print(f"  exact_frontdoor_search_rows={profile.exact_frontdoor_search_rows}")
    print("interpretation")
    print("  external_scout_has_zero_visible_source_closing_hits=1")
    print("  all_external_context_requires_exact_p25_specialization=1")
    print("  next_query_targets_are_exact_product_or_divisor_theorems_not_generic_generation=1")
    print(f"ksy_y_external_frontdoor_source_scout_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("external front-door source scout regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
