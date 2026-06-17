#!/usr/bin/env python3
"""Common-scalar filter for p25 row-anchor claims."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
PM1_FACTORS = {2: 2, 11: 1, 23: 1, 9881422924901185770751: 1}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


@dataclass(frozen=True)
class AnchorRow:
    name: str
    coefficient_sum: int | None
    branch_exponent: int | None
    required_input: str
    decision: str
    missing_or_falsifier: str
    ok: bool

    @property
    def branch_gcd(self) -> int:
        if self.coefficient_sum is not None:
            return gcd(self.coefficient_sum, PM1)
        if self.branch_exponent is not None:
            return gcd(self.branch_exponent, PM1)
        return PM1

    @property
    def fixes_common_scalar(self) -> bool:
        return self.branch_gcd == 1


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "row_value_reconstruction_basis",
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    EvidenceMarker(
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    EvidenceMarker(
        "priority1_divisor_additive_work_order",
        "evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md",
        "p25_v2_priority1_divisor_additive_work_order_rows=1/1",
    ),
    EvidenceMarker(
        "fpstar_branch_factorization",
        "evidence/p25_v2_fpstar_branch_factorization_20260617.md",
        "p25_v2_fpstar_branch_factorization_rows=1/1",
    ),
    EvidenceMarker(
        "extended_unique_power_intake",
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    EvidenceMarker(
        "q_square_payload_router",
        "evidence/p25_v2_q_square_payload_router_20260616.md",
        "p25_v2_q_square_payload_router_rows=1/1",
    ),
)


def branch_exponent(power: int) -> int:
    return pow(4, power) - 1


def rows() -> tuple[AnchorRow, ...]:
    return (
        AnchorRow(
            name="zero_lattice_or_quotient",
            coefficient_sum=0,
            branch_exponent=None,
            required_input="exact quotient, H90 coboundary, or boundary-zero relation",
            decision="transfer_only_never_first_anchor",
            missing_or_falsifier="common F_p^* scalar is invisible because coefficient sum is zero",
            ok=gcd(0, PM1) == PM1,
        ),
        AnchorRow(
            name="direct_one_edge",
            coefficient_sum=1,
            branch_exponent=None,
            required_input="exact scalar-fixed finite theorem for one legal row R_m",
            decision="anchors_common_scalar_if_source_theorem_present",
            missing_or_falsifier="arithmetic source theorem and extraction still required",
            ok=gcd(1, PM1) == 1,
        ),
        AnchorRow(
            name="pair_diagonal_or_q_square",
            coefficient_sum=2,
            branch_exponent=None,
            required_input="exact finite value for 2*R_m, diagonal-plus-split, or Q-square row",
            decision="two_root_payload_not_anchor",
            missing_or_falsifier="oriented square root/sign or direct one-row theorem",
            ok=gcd(2, PM1) == 2,
        ),
        AnchorRow(
            name="projector_or_all_four_edge",
            coefficient_sum=4,
            branch_exponent=None,
            required_input="projector basis, all-four product, or 4*R_m payload",
            decision="four_root_or_selector_repair",
            missing_or_falsifier="fourth-root/scalar selection plus row selector",
            ok=gcd(4, PM1) == 4,
        ),
        AnchorRow(
            name="q6_or_sixfold_boundary",
            coefficient_sum=6,
            branch_exponent=None,
            required_input="Q^6 boundary or sixfold mixed source payload",
            decision="boundary_repair_not_anchor",
            missing_or_falsifier="two branches remain and source-side selector is missing",
            ok=gcd(6, PM1) == 2,
        ),
        AnchorRow(
            name="unit_power_values",
            coefficient_sum=3,
            branch_exponent=None,
            required_input="exact finite theorem for R_m^e with e in {3,5,13,39,75,169,507}",
            decision="anchors_after_inverse_exponent_if_exact_and_row_labeled",
            missing_or_falsifier="must be one oriented legal row with source theorem and boundary/period bridge",
            ok=all(gcd(exponent, PM1) == 1 for exponent in (3, 5, 13, 39, 75, 169, 507)),
        ),
        AnchorRow(
            name="mu11_ambiguous_power",
            coefficient_sum=11,
            branch_exponent=None,
            required_input="exact value only up to an 11th root or mu_11 quotient",
            decision="eleven_branch_repair",
            missing_or_falsifier="branch/scalar selection needed before row intake",
            ok=gcd(11, PM1) == 11,
        ),
        AnchorRow(
            name="support_period156_value",
            coefficient_sum=None,
            branch_exponent=branch_exponent(156),
            required_input="support-period-156 value theorem with legal-row bridge",
            decision="unique_period_branch_if_source_supplies_exact_payload",
            missing_or_falsifier="still needs theorem body and row bridge; uniqueness alone is not source",
            ok=gcd(branch_exponent(156), PM1) == 1,
        ),
        AnchorRow(
            name="ambient_period780_value",
            coefficient_sum=None,
            branch_exponent=branch_exponent(780),
            required_input="ambient-period-780 value theorem or mu_11 quotient",
            decision="ambient_eleven_branch_repair",
            missing_or_falsifier="period-156 branch/root/telescoping or additive normalization",
            ok=gcd(branch_exponent(780), PM1) == 11,
        ),
    )


def main() -> int:
    anchor_rows = rows()
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    anchor_decisions = sum(row.fixes_common_scalar for row in anchor_rows)
    transfer_only = sum(row.coefficient_sum == 0 for row in anchor_rows)
    root_debt = sum(row.branch_gcd not in (1, PM1) for row in anchor_rows)
    source_stage_closers = 0
    submission_ready = 0
    overall_ok = (
        P25 % 8 == 5
        and PM1_FACTORS == {2: 2, 11: 1, 23: 1, 9881422924901185770751: 1}
        and markers_ok == len(EVIDENCE_MARKERS)
        and len(anchor_rows) == 9
        and all(row.ok for row in anchor_rows)
        and anchor_decisions == 3
        and transfer_only == 1
        and root_debt == 5
        and source_stage_closers == 0
        and submission_ready == 0
    )

    print("p25 v2 common-scalar anchor filter")
    print(f"p={P25}")
    print(f"p_minus_1={PM1}")
    print(f"p_minus_1_factors={PM1_FACTORS}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in anchor_rows:
        total = row.coefficient_sum
        branch = row.branch_exponent
        label = f"coefficient_sum={total}" if total is not None else f"branch_exponent=4^{156 if row.name == 'support_period156_value' else 780}-1"
        print(f"  {row.name}: decision={row.decision} ok={int(row.ok)}")
        print(f"    {label}")
        print(f"    branch_gcd={row.branch_gcd}")
        print(f"    fixes_common_scalar={int(row.fixes_common_scalar)}")
        print(f"    required_input={row.required_input}")
        print(f"    missing_or_falsifier={row.missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"  anchor_filter_rows={len(anchor_rows)}")
    print(f"  scalar_fixing_rows={anchor_decisions}")
    print(f"  transfer_only_rows={transfer_only}")
    print(f"  root_or_branch_debt_rows={root_debt}")
    print(f"  current_source_stage_closers={source_stage_closers}")
    print(f"  current_submission_ready={submission_ready}")
    print("interpretation")
    print("  coefficient_sum_zero_cannot_anchor=1")
    print("  gcd_one_exact_values_are_anchor_candidates=1")
    print("  nonunit_gcd_values_retain_root_or_branch_debt=1")
    print(f"p25_v2_common_scalar_anchor_filter_rows={int(overall_ok)}/1")
    if not overall_ok:
        raise SystemExit("common-scalar anchor filter failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
