#!/usr/bin/env python3
"""Power-normalized theorem intake for the p25 first-pass target.

Some source snippets may prove an exact power value rather than the row value
itself.  For p25, only power maps with trivial kernel on F_p^* can be promoted
to the ordinary source-snippet intake without extra branch/orientation data.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013
SOURCE_ROUTE_EXPONENTS = (3, 5, 13, 39, 75, 169, 507)
AMBIGUOUS_EXPONENTS = (2, 4, 6, 11, 22, 44, 156, 780)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class PowerRoute:
    exponent: int
    kernel_size: int
    inverse_exponent_mod_pminus1: int | None
    decision: str
    required_clauses: tuple[str, ...]
    source_stage_shape_if_theorem_present: bool
    currently_in_hand: bool
    ok: bool


@dataclass(frozen=True)
class NearMiss:
    name: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class PowerNormalizedTheoremIntake:
    evidence_markers: tuple[EvidenceMarker, ...]
    source_routes: tuple[PowerRoute, ...]
    ambiguous_routes: tuple[PowerRoute, ...]
    near_misses: tuple[NearMiss, ...]
    source_route_count: int
    ambiguous_route_count: int
    current_power_source_theorems: int
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
            "self_contained_theorem_statement",
            "research/p25/evidence/p25_v2_self_contained_theorem_statement_20260616.md",
            "p25_v2_self_contained_theorem_statement_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def source_power_route(exponent: int) -> PowerRoute:
    kernel = gcd(exponent, P25 - 1)
    inverse = pow(exponent, -1, P25 - 1)
    return PowerRoute(
        exponent=exponent,
        kernel_size=kernel,
        inverse_exponent_mod_pminus1=inverse,
        decision=f"normalize_unique_{exponent}th_root_then_apply_source_snippet_intake",
        required_clauses=(
            "one_exact_oriented_row_R_m",
            "arithmetic_source_theorem",
            f"exact_finite_Fp_value_for_R_m_power_{exponent}",
            "Norm_156_Y_507_boundary_or_accepted_period156_bridge",
            "post_root_source_snippet_intake",
        ),
        source_stage_shape_if_theorem_present=True,
        currently_in_hand=False,
        ok=kernel == 1,
    )


def ambiguous_power_route(exponent: int) -> PowerRoute:
    kernel = gcd(exponent, P25 - 1)
    return PowerRoute(
        exponent=exponent,
        kernel_size=kernel,
        inverse_exponent_mod_pminus1=None,
        decision=f"repair_power_kernel_size_{kernel}_branch_or_orientation_missing",
        required_clauses=(
            "one_exact_oriented_row_R_m",
            "arithmetic_source_theorem",
            f"exact_finite_Fp_value_for_R_m_power_{exponent}",
            "extra_branch_orientation_or_scalar_data_selecting_one_kernel_root",
        ),
        source_stage_shape_if_theorem_present=False,
        currently_in_hand=False,
        ok=kernel > 1,
    )


def near_misses() -> tuple[NearMiss, ...]:
    return (
        NearMiss(
            name="exact_power_value_without_source",
            decision="repair_arithmetic_source_theorem_missing",
            first_missing_or_falsifier="local finite value or packet is not a source-stage theorem",
            ok=True,
        ),
        NearMiss(
            name="exact_power_value_without_row",
            decision="repair_oriented_row_selection_missing",
            first_missing_or_falsifier="power value must be attached to one legal row m in {1,2,4,8}",
            ok=True,
        ),
        NearMiss(
            name="power_value_up_to_fp_scalar",
            decision="repair_constant_normalization_missing",
            first_missing_or_falsifier="exact power still needs scalar-fixed finite value data",
            ok=True,
        ),
        NearMiss(
            name="ambient_period780_power_only",
            decision="repair_period156_branch_selection_missing",
            first_missing_or_falsifier="ambient-period output still has the mu_11 branch problem",
            ok=True,
        ),
    )


def build_intake() -> PowerNormalizedTheoremIntake:
    markers = evidence_markers()
    source_routes = tuple(source_power_route(exponent) for exponent in SOURCE_ROUTE_EXPONENTS)
    ambiguous_routes = tuple(ambiguous_power_route(exponent) for exponent in AMBIGUOUS_EXPONENTS)
    misses = near_misses()
    current_power_source_theorems = sum(row.currently_in_hand for row in source_routes)
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and tuple((row.exponent, row.kernel_size, row.inverse_exponent_mod_pminus1) for row in source_routes)
        == (
            (3, 1, 6_666_666_666_666_666_666_666_675),
            (5, 1, 4_000_000_000_000_000_000_000_005),
            (13, 1, 7_692_307_692_307_692_307_692_317),
            (39, 1, 5_897_435_897_435_897_435_897_443),
            (75, 1, 266_666_666_666_666_666_666_667),
            (169, 1, 5_207_100_591_715_976_331_360_953),
            (507, 1, 5_069_033_530_571_992_110_453_655),
        )
        and tuple((row.exponent, row.kernel_size, row.inverse_exponent_mod_pminus1) for row in ambiguous_routes)
        == (
            (2, 2, None),
            (4, 4, None),
            (6, 2, None),
            (11, 11, None),
            (22, 22, None),
            (44, 44, None),
            (156, 4, None),
            (780, 4, None),
        )
        and all(row.source_stage_shape_if_theorem_present for row in source_routes)
        and not any(row.source_stage_shape_if_theorem_present for row in ambiguous_routes)
        and current_power_source_theorems == 0
        and current_submission_ready == 0
        and all(row.ok for row in source_routes)
        and all(row.ok for row in ambiguous_routes)
        and all(row.ok for row in misses)
    )
    return PowerNormalizedTheoremIntake(
        evidence_markers=markers,
        source_routes=source_routes,
        ambiguous_routes=ambiguous_routes,
        near_misses=misses,
        source_route_count=len(source_routes),
        ambiguous_route_count=len(ambiguous_routes),
        current_power_source_theorems=current_power_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    intake = build_intake()
    print("p25 v2 power-normalized theorem intake")
    for row in intake.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("source_power_routes")
    for row in intake.source_routes:
        print(
            f"  e={row.exponent}: kernel={row.kernel_size} "
            f"inv={row.inverse_exponent_mod_pminus1} "
            f"decision={row.decision} source_stage_if_theorem={int(row.source_stage_shape_if_theorem_present)}"
        )
        print(f"    required_clauses={','.join(row.required_clauses)}")
    print("ambiguous_power_routes")
    for row in intake.ambiguous_routes:
        print(
            f"  e={row.exponent}: kernel={row.kernel_size} "
            f"inv={row.inverse_exponent_mod_pminus1} "
            f"decision={row.decision} source_stage_if_theorem={int(row.source_stage_shape_if_theorem_present)}"
        )
    print("near_misses")
    for row in intake.near_misses:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in intake.evidence_markers)}/{len(intake.evidence_markers)}")
    print(f"  source_power_routes={intake.source_route_count}")
    print(f"  ambiguous_power_routes={intake.ambiguous_route_count}")
    print(f"  current_power_source_theorems={intake.current_power_source_theorems}")
    print(f"  current_submission_ready={intake.current_submission_ready}")
    print(f"p25_v2_power_normalized_theorem_intake_rows={int(intake.row_ok)}/1")
    return 0 if intake.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
