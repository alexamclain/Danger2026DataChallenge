#!/usr/bin/env python3
"""Degree-6 value descent ambiguity for p25 value-route claims.

The period-156 branch contract already records that primitive conductor-39
value language naturally lives over degree 6 for p25.  This gate makes the
corresponding intake rule explicit: a value/orbit computed over F_{p^6} is
repair unless it descends to the selected F_p support-156 row or supplies an
equivalent Hilbert-90 ratio boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013
SUPPORT_PERIOD = 156
AMBIENT_PERIOD = 780


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class Degree6Claim:
    name: str
    shape: str
    degree6_expression: bool
    descent_to_fp: bool
    selected_legal_row: bool
    period156_context: bool
    h90_boundary: bool
    direct_fp_shortcut: bool
    decision: str
    first_missing_or_falsifier: str
    continue_lane: bool
    ok: bool


@dataclass(frozen=True)
class Degree6ValueDescentAmbiguity:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_mod_3: int
    p_mod_13: int
    p_mod_39: int
    order_mod3: int
    order_mod13: int
    order_mod39: int
    p_cubed_is_minus_one_mod39: bool
    sqrt_minus39_in_fp: bool
    support_period: int
    ambient_period: int
    support_denominator_gcd_fp_star: int
    ambient_denominator_gcd_fp_star: int
    claims: tuple[Degree6Claim, ...]
    evidence_markers_ok: int
    normalize_rows: int
    repair_rows: int
    reject_rows: int
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
            "norm_only_descent_ambiguity",
            "research/p25/evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
            "p25_v2_norm_only_descent_ambiguity_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def multiplicative_order_mod(n: int, modulus: int) -> int:
    if gcd(n, modulus) != 1:
        raise ValueError("order is defined only for units")
    value = 1
    for order in range(1, modulus + 1):
        value = (value * n) % modulus
        if value == 1:
            return order
    raise ValueError("order search exhausted")


def claim(
    name: str,
    shape: str,
    *,
    degree6: bool = False,
    descent: bool = False,
    selected: bool = False,
    period156: bool = False,
    h90: bool = False,
    direct_fp: bool = False,
) -> Degree6Claim:
    if direct_fp:
        decision = "reject_direct_fp_order39_or_sqrt_minus39_shortcut"
        missing = "ord_39(p)=6 and sqrt(-39) is not in F_p"
        continue_lane = False
    elif degree6 and descent and selected and (period156 or h90):
        decision = "normalize_value_descent_then_apply_source_snippet_intake"
        missing = "same theorem data after explicit F_p descent and row selection"
        continue_lane = True
    elif degree6 and not descent:
        decision = "repair_degree6_orbit_without_descent"
        missing = "conjugate/norm descent back to F_p or Hilbert-90 ratio boundary"
        continue_lane = True
    elif degree6 and descent and not selected:
        decision = "repair_descent_without_selected_legal_row"
        missing = "legal support-156 row selection after descent"
        continue_lane = True
    elif degree6 and descent and selected and not (period156 or h90):
        decision = "repair_period156_or_h90_context_missing"
        missing = "support-period-156 branch/root/telescoping context or H90 boundary"
        continue_lane = True
    else:
        decision = "repair_incomplete_degree6_value_claim"
        missing = "degree-6 expression plus explicit F_p descent and selected legal row"
        continue_lane = True

    return Degree6Claim(
        name=name,
        shape=shape,
        degree6_expression=degree6,
        descent_to_fp=descent,
        selected_legal_row=selected,
        period156_context=period156,
        h90_boundary=h90,
        direct_fp_shortcut=direct_fp,
        decision=decision,
        first_missing_or_falsifier=missing,
        continue_lane=continue_lane,
        ok=True,
    )


def claim_rows() -> tuple[Degree6Claim, ...]:
    return (
        claim(
            "degree6_value_with_explicit_fp_descent",
            "F_{p^6} value/orbit plus explicit descent to one selected legal F_p row",
            degree6=True,
            descent=True,
            selected=True,
            period156=True,
        ),
        claim(
            "degree6_value_orbit_without_descent",
            "F_{p^6} value/orbit for conductor 39 with no conjugate/norm descent",
            degree6=True,
        ),
        claim(
            "primitive_root_expression_degree6_only",
            "formula in primitive 13th or 39th roots over F_{p^6}, but no F_p descent",
            degree6=True,
        ),
        claim(
            "degree6_norm_without_selected_row",
            "degree-6 norm/descent to F_p, but no selected legal support-156 row",
            degree6=True,
            descent=True,
        ),
        claim(
            "degree6_selected_row_without_period156_or_h90",
            "degree-6 descent to a selected row, but no period-156 or H90 boundary context",
            degree6=True,
            descent=True,
            selected=True,
        ),
        claim(
            "direct_fp_order39_root_shortcut",
            "choose a primitive order-39 root directly in F_p",
            direct_fp=True,
        ),
        claim(
            "sqrt_minus39_scalar_shortcut",
            "collapse the chi_3 tensor chi_13 structure using sqrt(-39) in F_p",
            direct_fp=True,
        ),
    )


def build_contract() -> Degree6ValueDescentAmbiguity:
    markers = evidence_markers()
    rows = claim_rows()
    order3 = multiplicative_order_mod(P25 % 3, 3)
    order13 = multiplicative_order_mod(P25 % 13, 13)
    order39 = multiplicative_order_mod(P25 % 39, 39)
    support_gcd = gcd(4**SUPPORT_PERIOD - 1, P25 - 1)
    ambient_gcd = gcd(4**AMBIENT_PERIOD - 1, P25 - 1)
    markers_ok = sum(row.ok for row in markers)
    normalize = sum(row.decision.startswith("normalize_") for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    rejects = sum(row.decision.startswith("reject_") for row in rows)
    current_closers = 0
    row_ok = (
        markers_ok == len(markers)
        and P25 % 3 == 2
        and P25 % 13 == 10
        and P25 % 39 == 23
        and order3 == 2
        and order13 == 6
        and order39 == 6
        and pow(P25, 3, 39) == 38
        and pow((-39) % P25, (P25 - 1) // 2, P25) == P25 - 1
        and support_gcd == 1
        and ambient_gcd == 11
        and len(rows) == 7
        and normalize == 1
        and repairs == 4
        and rejects == 2
        and current_closers == 0
        and tuple(row.decision for row in rows)
        == (
            "normalize_value_descent_then_apply_source_snippet_intake",
            "repair_degree6_orbit_without_descent",
            "repair_degree6_orbit_without_descent",
            "repair_descent_without_selected_legal_row",
            "repair_period156_or_h90_context_missing",
            "reject_direct_fp_order39_or_sqrt_minus39_shortcut",
            "reject_direct_fp_order39_or_sqrt_minus39_shortcut",
        )
        and all(row.ok for row in rows)
    )
    return Degree6ValueDescentAmbiguity(
        evidence_markers=markers,
        p_mod_3=P25 % 3,
        p_mod_13=P25 % 13,
        p_mod_39=P25 % 39,
        order_mod3=order3,
        order_mod13=order13,
        order_mod39=order39,
        p_cubed_is_minus_one_mod39=pow(P25, 3, 39) == 38,
        sqrt_minus39_in_fp=pow((-39) % P25, (P25 - 1) // 2, P25) == 1,
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        support_denominator_gcd_fp_star=support_gcd,
        ambient_denominator_gcd_fp_star=ambient_gcd,
        claims=rows,
        evidence_markers_ok=markers_ok,
        normalize_rows=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for row in contract.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mod_3={contract.p_mod_3}")
    print(f"  p_mod_13={contract.p_mod_13}")
    print(f"  p_mod_39={contract.p_mod_39}")
    print(f"  order_mod3={contract.order_mod3}")
    print(f"  order_mod13={contract.order_mod13}")
    print(f"  order_mod39={contract.order_mod39}")
    print(f"  p_cubed_is_minus_one_mod39={int(contract.p_cubed_is_minus_one_mod39)}")
    print(f"  sqrt_minus39_in_fp={int(contract.sqrt_minus39_in_fp)}")
    print(f"  support_period={contract.support_period}")
    print(f"  ambient_period={contract.ambient_period}")
    print(f"  gcd_4^156_minus_1_with_Fp_star={contract.support_denominator_gcd_fp_star}")
    print(f"  gcd_4^780_minus_1_with_Fp_star={contract.ambient_denominator_gcd_fp_star}")
    print("claim_rows")
    for row in contract.claims:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"degree6={int(row.degree6_expression)} descent={int(row.descent_to_fp)} "
            f"selected={int(row.selected_legal_row)} period156={int(row.period156_context)} "
            f"h90={int(row.h90_boundary)} direct_fp={int(row.direct_fp_shortcut)} "
            f"continue={int(row.continue_lane)}"
        )
        print(f"    shape={row.shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  normalize_rows={contract.normalize_rows}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  reject_rows={contract.reject_rows}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print("interpretation")
    print("  primitive_order39_value_language_is_degree6=1")
    print("  degree6_value_orbit_without_descent_is_repair=1")
    print("  explicit_fp_descent_still_routes_to_source_snippet_intake=1")
    print("  direct_fp_order39_or_sqrt_minus39_shortcuts_are_reject=1")
    print(f"p25_v2_degree6_value_descent_ambiguity_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
