#!/usr/bin/env python3
"""Power-map and scalar ambiguity inventory for p25 value snippets.

The current target is one nonzero support-156 product value in F_p.  Several
near-miss theorem shapes give only a power of that value or give the value up
to a root-of-unity scalar.  This gate records which power maps on F_p^* are
bijective for p25 and which leave a kernel that must be fixed by extra
orientation, branch, or scalar data.
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
class PowerMapRow:
    exponent: int
    kernel_size: int
    bijective_on_fp_star: bool
    decision: str
    first_missing_or_use: str
    row_ok: bool


@dataclass(frozen=True)
class ScalarRow:
    scalar_group: str
    order: int
    exists_in_fp: bool
    decision: str
    first_missing_or_falsifier: str
    row_ok: bool


@dataclass(frozen=True)
class PowerScalarAmbiguityInventory:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_mods: tuple[tuple[int, int], ...]
    power_rows: tuple[PowerMapRow, ...]
    scalar_rows: tuple[ScalarRow, ...]
    unique_power_rows: int
    ambiguous_power_rows: int
    fp_scalar_groups_present: int
    fp_scalar_groups_absent: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "period156_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
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


def power_row(exponent: int) -> PowerMapRow:
    kernel = gcd(exponent, P25 - 1)
    if kernel == 1:
        decision = f"normalize_unique_{exponent}th_root_then_apply_source_snippet_intake"
        use = "exact power value determines the target value uniquely in F_p^*"
    else:
        decision = f"repair_power_kernel_size_{kernel}_orientation_or_branch_missing"
        use = f"kernel of x -> x^{exponent} on F_p^* has size {kernel}"
    return PowerMapRow(
        exponent=exponent,
        kernel_size=kernel,
        bijective_on_fp_star=kernel == 1,
        decision=decision,
        first_missing_or_use=use,
        row_ok=True,
    )


def scalar_row(name: str, order: int) -> ScalarRow:
    exists = (P25 - 1) % order == 0
    if exists:
        decision = f"repair_{name}_scalar_not_fixed"
        missing = f"explicit scalar/branch/orientation selecting one of {order} F_p scalars"
    else:
        decision = f"reject_{name}_as_Fp_scalar"
        missing = f"mu_{order} is not contained in F_p^* for p25"
    return ScalarRow(
        scalar_group=name,
        order=order,
        exists_in_fp=exists,
        decision=decision,
        first_missing_or_falsifier=missing,
        row_ok=True,
    )


def build_inventory() -> PowerScalarAmbiguityInventory:
    markers = evidence_markers()
    powers = tuple(power_row(exponent) for exponent in (2, 3, 4, 5, 6, 11, 13, 22, 39, 44, 156, 780))
    scalars = (
        scalar_row("mu2_sign", 2),
        scalar_row("mu3", 3),
        scalar_row("mu4_quartic", 4),
        scalar_row("mu6", 6),
        scalar_row("mu11_ambient_branch", 11),
        scalar_row("mu13", 13),
        scalar_row("mu22", 22),
        scalar_row("mu39", 39),
        scalar_row("mu44", 44),
        scalar_row("mu156", 156),
    )
    unique = sum(row.bijective_on_fp_star for row in powers)
    ambiguous = len(powers) - unique
    present = sum(row.exists_in_fp for row in scalars)
    absent = len(scalars) - present
    current_closers = 0
    p_mods = tuple((modulus, P25 % modulus) for modulus in (3, 4, 8, 11, 13, 39, 44, 156))
    marker_ok = sum(row.ok for row in markers)
    row_ok = (
        marker_ok == len(markers)
        and p_mods == ((3, 2), (4, 1), (8, 5), (11, 1), (13, 10), (39, 23), (44, 1), (156, 101))
        and tuple((row.exponent, row.kernel_size) for row in powers)
        == ((2, 2), (3, 1), (4, 4), (5, 1), (6, 2), (11, 11), (13, 1), (22, 22), (39, 1), (44, 44), (156, 4), (780, 4))
        and tuple((row.scalar_group, row.exists_in_fp) for row in scalars)
        == (
            ("mu2_sign", True),
            ("mu3", False),
            ("mu4_quartic", True),
            ("mu6", False),
            ("mu11_ambient_branch", True),
            ("mu13", False),
            ("mu22", True),
            ("mu39", False),
            ("mu44", True),
            ("mu156", False),
        )
        and unique == 4
        and ambiguous == 8
        and present == 5
        and absent == 5
        and current_closers == 0
        and all(row.row_ok for row in powers)
        and all(row.row_ok for row in scalars)
    )
    return PowerScalarAmbiguityInventory(
        evidence_markers=markers,
        p_mods=p_mods,
        power_rows=powers,
        scalar_rows=scalars,
        unique_power_rows=unique,
        ambiguous_power_rows=ambiguous,
        fp_scalar_groups_present=present,
        fp_scalar_groups_absent=absent,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    inventory = build_inventory()
    for row in inventory.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mods={inventory.p_mods}")
    print("power_maps")
    for row in inventory.power_rows:
        print(
            "  "
            f"e={row.exponent}: kernel={row.kernel_size} "
            f"bijective={int(row.bijective_on_fp_star)} decision={row.decision}"
        )
        print(f"    first_missing_or_use={row.first_missing_or_use}")
    print("scalar_groups")
    for row in inventory.scalar_rows:
        print(
            "  "
            f"{row.scalar_group}: order={row.order} exists_in_fp={int(row.exists_in_fp)} "
            f"decision={row.decision}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in inventory.evidence_markers)}/{len(inventory.evidence_markers)}")
    print(f"  unique_power_rows={inventory.unique_power_rows}")
    print(f"  ambiguous_power_rows={inventory.ambiguous_power_rows}")
    print(f"  fp_scalar_groups_present={inventory.fp_scalar_groups_present}")
    print(f"  fp_scalar_groups_absent={inventory.fp_scalar_groups_absent}")
    print(f"  current_source_stage_closers={inventory.current_source_stage_closers}")
    print("interpretation")
    print("  exact_cube_5th_13th_or_39th_power_values_are_uniquely_invertible=1")
    print("  square_fourth_11th_22nd_44th_156th_or_780th_power_values_need_branch_data=1")
    print("  primitive_order_39_scalar_is_not_in_Fp_even_though_39th_power_map_is_bijective=1")
    print("  mu11_and_mu44_scalar_ambiguities_exist_in_Fp_and_do_not_close_source_stage=1")
    print(f"p25_v2_power_scalar_ambiguity_inventory_rows={int(inventory.row_ok)}/1")
    return 0 if inventory.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
