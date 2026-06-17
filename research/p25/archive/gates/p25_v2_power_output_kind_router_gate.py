#!/usr/bin/env python3
"""Route power-value versus power-divisor theorem snippets for p25.

The power/scalar inventory says which maps x -> x^e are bijective on F_p^*.
That is enough to normalize an exact finite value for R^e when gcd(e,p-1)=1.
It is not enough to promote a divisor/H90 boundary-only theorem for R^e:
without finite value/additive normalization, the constant/scalar problem has
not been fixed.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OutputKindRow:
    name: str
    exponent: int
    output_kind: str
    exact_finite_value: bool
    divisor_or_additive: bool
    h90_boundary_multiplier: int | None
    finite_normalization: bool
    selected_branch_or_scalar: bool
    kernel_size: int
    inverse_exponent_mod_pminus1: int | None
    decision: str
    first_missing_or_use: str
    row_ok: bool


@dataclass(frozen=True)
class PowerOutputKindRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[OutputKindRow, ...]
    unique_value_normalize_rows: int
    ambiguous_value_repair_rows: int
    power_boundary_repair_rows: int
    scaled_boundary_reject_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "coefficient6_root_normalization",
            "research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md",
            "p25_v2_coefficient6_root_normalization_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def inverse_exponent(exponent: int) -> int | None:
    return pow(exponent, -1, P25 - 1) if gcd(exponent, P25 - 1) == 1 else None


def output_row(
    name: str,
    exponent: int,
    output_kind: str,
    *,
    exact_value: bool = False,
    divisor: bool = False,
    boundary_multiplier: int | None = None,
    finite_normalization: bool = False,
    selected_branch: bool = False,
) -> OutputKindRow:
    kernel = gcd(exponent, P25 - 1)
    inv = inverse_exponent(exponent)
    if exact_value and kernel == 1:
        decision = "normalize_unique_power_value_then_apply_source_snippet_intake"
        use = f"raise the exact value to inverse exponent {inv} modulo p-1"
    elif exact_value and selected_branch:
        decision = "normalize_selected_power_value_then_apply_source_snippet_intake"
        use = "branch/scalar data selects the root despite a nontrivial power-map kernel"
    elif exact_value:
        decision = "repair_power_value_branch_or_scalar_missing"
        use = f"kernel of x -> x^{exponent} on F_p^* has size {kernel}"
    elif divisor and finite_normalization and kernel == 1:
        decision = "normalize_power_divisor_with_value_data_then_intake"
        use = "finite normalization converts the powered theorem to an exact value before rooting"
    elif divisor:
        decision = "repair_power_divisor_value_normalization_missing"
        use = "divisor/H90 data for R^e does not by itself fix the finite value of R"
    elif boundary_multiplier is not None and boundary_multiplier != 1:
        decision = "reject_scaled_boundary_as_current_target"
        use = "eW is not the current W boundary unless the theorem powers back to the row"
    else:
        decision = "repair_incomplete_power_output"
        use = "exact value or finite divisor/additive theorem data is missing"
    return OutputKindRow(
        name=name,
        exponent=exponent,
        output_kind=output_kind,
        exact_finite_value=exact_value,
        divisor_or_additive=divisor,
        h90_boundary_multiplier=boundary_multiplier,
        finite_normalization=finite_normalization,
        selected_branch_or_scalar=selected_branch,
        kernel_size=kernel,
        inverse_exponent_mod_pminus1=inv,
        decision=decision,
        first_missing_or_use=use,
        row_ok=True,
    )


def row_profile() -> tuple[OutputKindRow, ...]:
    return (
        output_row("exact_value_power3", 3, "value", exact_value=True),
        output_row("exact_value_power5", 5, "value", exact_value=True),
        output_row("exact_value_power13", 13, "value", exact_value=True),
        output_row("exact_value_power39", 39, "value", exact_value=True),
        output_row("exact_value_power11_with_branch", 11, "value", exact_value=True, selected_branch=True),
        output_row("exact_value_power11_no_branch", 11, "value", exact_value=True),
        output_row("divisor_additive_power3_with_value_normalization", 3, "divisor-additive", divisor=True, boundary_multiplier=3, finite_normalization=True),
        output_row("divisor_h90_power3_no_value", 3, "divisor-h90", divisor=True, boundary_multiplier=3),
        output_row("boundary_power3_only", 3, "boundary", boundary_multiplier=3),
        output_row("divisor_h90_power11_no_branch", 11, "divisor-h90", divisor=True, boundary_multiplier=11),
        output_row("scaled_boundary_power11_as_current", 11, "boundary", boundary_multiplier=11),
    )


def build_router() -> PowerOutputKindRouter:
    markers = evidence_markers()
    rows = row_profile()
    unique_value = sum(row.decision == "normalize_unique_power_value_then_apply_source_snippet_intake" for row in rows)
    ambiguous = sum(row.decision == "repair_power_value_branch_or_scalar_missing" for row in rows)
    boundary_repair = sum(row.decision == "repair_power_divisor_value_normalization_missing" for row in rows)
    scaled_reject = sum(row.decision == "reject_scaled_boundary_as_current_target" for row in rows)
    current_closers = 0
    marker_ok = sum(row.ok for row in markers)
    row_ok = (
        marker_ok == len(markers)
        and len(rows) == 11
        and tuple((row.exponent, row.kernel_size, row.inverse_exponent_mod_pminus1 is not None) for row in rows)
        == (
            (3, 1, True),
            (5, 1, True),
            (13, 1, True),
            (39, 1, True),
            (11, 11, False),
            (11, 11, False),
            (3, 1, True),
            (3, 1, True),
            (3, 1, True),
            (11, 11, False),
            (11, 11, False),
        )
        and unique_value == 4
        and ambiguous == 1
        and boundary_repair == 2
        and scaled_reject == 2
        and rows[4].decision == "normalize_selected_power_value_then_apply_source_snippet_intake"
        and rows[6].decision == "normalize_power_divisor_with_value_data_then_intake"
        and current_closers == 0
        and all(row.row_ok for row in rows)
    )
    return PowerOutputKindRouter(
        evidence_markers=markers,
        rows=rows,
        unique_value_normalize_rows=unique_value,
        ambiguous_value_repair_rows=ambiguous,
        power_boundary_repair_rows=boundary_repair,
        scaled_boundary_reject_rows=scaled_reject,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    for row in router.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("output_rows")
    for row in router.rows:
        print(
            "  "
            f"{row.name}: e={row.exponent} kind={row.output_kind} "
            f"kernel={row.kernel_size} inv={row.inverse_exponent_mod_pminus1} "
            f"exact_value={int(row.exact_finite_value)} divisor={int(row.divisor_or_additive)} "
            f"boundary_multiplier={row.h90_boundary_multiplier} "
            f"finite_normalization={int(row.finite_normalization)} "
            f"selected_branch={int(row.selected_branch_or_scalar)} decision={row.decision}"
        )
        print(f"    first_missing_or_use={row.first_missing_or_use}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in router.evidence_markers)}/{len(router.evidence_markers)}")
    print(f"  unique_value_normalize_rows={router.unique_value_normalize_rows}")
    print(f"  ambiguous_value_repair_rows={router.ambiguous_value_repair_rows}")
    print(f"  power_boundary_repair_rows={router.power_boundary_repair_rows}")
    print(f"  scaled_boundary_reject_rows={router.scaled_boundary_reject_rows}")
    print(f"  current_source_stage_closers={router.current_source_stage_closers}")
    print("interpretation")
    print("  exact_power_value_with_bijective_power_map_can_normalize=1")
    print("  divisor_or_boundary_power_without_finite_normalization_does_not_close=1")
    print("  scaled_h90_boundary_eW_is_not_the_current_W_boundary=1")
    print(f"p25_v2_power_output_kind_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
