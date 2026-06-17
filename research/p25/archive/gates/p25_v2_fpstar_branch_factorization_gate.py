#!/usr/bin/env python3
"""Audit the F_p^* branch factorization behind p25 value claims."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
P_MINUS_1_FACTORS = ((2, 2), (11, 1), (23, 1), (9881422924901185770751, 1))
P_PLUS_1_FACTORS = ((2, 1), (3, 1), (4703, 1), (21578093, 1), (16423310748511, 1))
POWER_EXPONENTS = (2, 3, 4, 5, 6, 11, 13, 22, 39, 44, 75, 156, 169, 507, 780)
ROOT_GROUPS = (2, 3, 4, 5, 6, 11, 13, 22, 39, 44, 75, 156, 169, 507, 780)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class BranchRow:
    order: int
    kernel_fp_star: int
    root_group_in_fp: bool
    route: str


EVIDENCE_INPUTS = (
    (
        "power_scalar_inventory",
        "evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
        "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
    ),
    (
        "period156_branch_contract",
        "evidence/p25_v2_period156_value_branch_contract_20260616.md",
        "p25_v2_period156_value_branch_contract_rows=1/1",
    ),
    (
        "power_normalized_intake",
        "evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
        "p25_v2_power_normalized_theorem_intake_rows=1/1",
    ),
    (
        "degree6_descent",
        "evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
        "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def factor_product(factors: tuple[tuple[int, int], ...]) -> int:
    product = 1
    for prime, exponent in factors:
        product *= prime**exponent
    return product


def order_mod(a: int, modulus: int) -> int:
    if gcd(a, modulus) != 1:
        raise ValueError("order undefined")
    value = 1
    for order in range(1, 2 * modulus + 1):
        value = (value * a) % modulus
        if value == 1:
            return order
    raise ValueError("order search exhausted")


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    rows: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        rows.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(rows)


def branch_route(order: int, kernel: int, exists: bool) -> str:
    if kernel == 1:
        return "unique_power_value"
    if order in (156,):
        return "support_period_power_has_mu4_kernel_but_value_branch_is_unique"
    if order in (780,):
        return "ambient_period_power_has_mu4_kernel_and_mu11_branch_debt"
    if exists:
        return "repair_scalar_or_branch"
    return "reject_as_fp_scalar_but_power_may_still_need_route"


def branch_rows() -> tuple[BranchRow, ...]:
    rows: list[BranchRow] = []
    for order in ROOT_GROUPS:
        kernel = gcd(order, P25 - 1)
        exists = (P25 - 1) % order == 0
        rows.append(BranchRow(order, kernel, exists, branch_route(order, kernel, exists)))
    return tuple(rows)


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[BranchRow, ...], bool]:
    markers = evidence_markers(root)
    rows = branch_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and factor_product(P_MINUS_1_FACTORS) == P25 - 1
        and factor_product(P_PLUS_1_FACTORS) == P25 + 1
        and P25 % 8 == 5
        and order_mod(P25 % 39, 39) == 6
        and order_mod(P25 % 507, 507) == 78
        and order_mod(P25 % 780, 780) == 12
        and tuple((row.order, row.kernel_fp_star, row.root_group_in_fp) for row in rows)
        == (
            (2, 2, True),
            (3, 1, False),
            (4, 4, True),
            (5, 1, False),
            (6, 2, False),
            (11, 11, True),
            (13, 1, False),
            (22, 22, True),
            (39, 1, False),
            (44, 44, True),
            (75, 1, False),
            (156, 4, False),
            (169, 1, False),
            (507, 1, False),
            (780, 4, False),
        )
        and sum(row.kernel_fp_star == 1 for row in rows) == 7
        and sum(row.root_group_in_fp for row in rows) == 5
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 Fp-star branch factorization")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print("factorization")
    print(f"  p_minus_1_factors={P_MINUS_1_FACTORS}")
    print(f"  p_plus_1_factors={P_PLUS_1_FACTORS}")
    print("orders")
    print(f"  ord_39(p)={order_mod(P25 % 39, 39)}")
    print(f"  ord_507(p)={order_mod(P25 % 507, 507)}")
    print(f"  ord_780(p)={order_mod(P25 % 780, 780)}")
    print("branch_rows")
    for row in rows:
        print(
            f"  n={row.order}: kernel={row.kernel_fp_star} "
            f"mu_n_in_Fp={int(row.root_group_in_fp)} route={row.route}"
        )
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"unique_power_orders={sum(row.kernel_fp_star == 1 for row in rows)}")
    print(f"root_groups_present={sum(row.root_group_in_fp for row in rows)}")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_fpstar_branch_factorization_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
