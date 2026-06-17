#!/usr/bin/env python3
"""V2 branch contract for value-side p25 theorem claims.

The unified H0/conductor-39 target is fixed.  This gate sharpens the value
side: a divisor/additive theorem avoids branch ambiguity, while a value
theorem must carry support-period-156 branch/root/telescoping context.  Ambient
period-780 values and direct F_p order-39-root shortcuts are not source-stage
closers for p25.
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
class ValueBranchClaim:
    name: str
    shape: str
    direct_fp_order39_root: bool
    sqrt_minus39_scalar: bool
    degree6_orbit: bool
    descent_to_fp: bool
    h90_boundary: bool
    arithmetic_source: bool
    finite_value_or_divisor: bool
    divisor_additive: bool
    value_level: bool
    support_period156_context: bool
    ambient_period780_only: bool
    mu11_power_or_quotient_only: bool
    decision: str
    closes_source_stage: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class Period156ValueBranchContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_mod_39: int
    p_order_mod39: int
    p_cubed_is_minus_one_mod39: bool
    sqrt_minus39_in_fp: bool
    support_period: int
    ambient_period: int
    support_denominator_gcd_fp_star: int
    ambient_denominator_gcd_fp_star: int
    small_period_gcds_fp_star: tuple[tuple[int, int], ...]
    direct_fp_order39_root_available: bool
    support_value_root_unique_fp_star: bool
    ambient_value_branch_count_fp_star: int
    claims: tuple[ValueBranchClaim, ...]
    evidence_markers_ok: int
    accepted_source_stage_shapes: int
    repair_rows: int
    rejected_shortcuts: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "legacy_degree6_descent",
            "research/p25/archive/notes/p25_ksy_y_conductor39_degree6_value_descent_packet_20260614.md",
            "ksy_y_conductor39_degree6_value_descent_packet_rows=1/1",
        ),
        marker(
            "legacy_period_value_scout",
            "research/p25/evidence/p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md",
            "ksy_y_siegel_robert_period_value_primary_source_scout_rows=1/1",
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
    direct_root: bool = False,
    sqrt_scalar: bool = False,
    degree6: bool = False,
    descent: bool = False,
    h90: bool = False,
    source: bool = False,
    finite: bool = False,
    divisor: bool = False,
    value: bool = False,
    period156: bool = False,
    ambient780: bool = False,
    mu11_power: bool = False,
) -> ValueBranchClaim:
    if direct_root:
        decision = "reject_direct_Fp_order39_root_shortcut"
        closes = False
        missing = "ord_39(p)=6, so primitive 39th roots first occur over degree 6"
    elif sqrt_scalar:
        decision = "reject_sqrt_minus39_scalar_shortcut"
        closes = False
        missing = "(-39/p)=-1, so sqrt(-39) is not an F_p scalar"
    elif ambient780:
        decision = "repair_ambient_period780_mu11_branch"
        closes = False
        missing = "period-156 branch/root/telescoping context; ambient route has 11 F_p branches"
    elif mu11_power:
        decision = "repair_mu11_power_or_quotient_not_value"
        closes = False
        missing = (
            "actual period-156 branch/root/telescoping data; an 11th power or "
            "mu_11 quotient does not select one F_p value"
        )
    elif degree6 and not descent and not h90:
        decision = "repair_degree6_orbit_without_descent"
        closes = False
        missing = "conjugate/norm descent back to F_p or Hilbert-90 ratio boundary"
    elif h90 and not finite:
        decision = "repair_boundary_without_value_or_divisor_theorem"
        closes = False
        missing = "finite value identity or divisor/additive theorem for one legal row"
    elif finite and value and not period156:
        decision = "repair_value_theorem_without_period156_context"
        closes = False
        missing = "support-period-156 branch/root/telescoping context"
    elif finite and not source:
        decision = "repair_finite_payload_without_arithmetic_source"
        closes = False
        missing = "arithmetic source theorem"
    elif finite and source and divisor and h90:
        decision = "source_stage_win_danger3_framing_missing"
        closes = True
        missing = "DANGER3 finite-identity/non-CM framing and extraction"
    elif finite and source and value and period156:
        decision = "source_stage_win_danger3_framing_missing"
        closes = True
        missing = "DANGER3 finite-identity/non-CM framing and extraction"
    else:
        decision = "repair_incomplete_value_branch_claim"
        closes = False
        missing = "finite source theorem plus H90 boundary or period-156 value context"

    return ValueBranchClaim(
        name=name,
        shape=shape,
        direct_fp_order39_root=direct_root,
        sqrt_minus39_scalar=sqrt_scalar,
        degree6_orbit=degree6,
        descent_to_fp=descent,
        h90_boundary=h90,
        arithmetic_source=source,
        finite_value_or_divisor=finite,
        divisor_additive=divisor,
        value_level=value,
        support_period156_context=period156,
        ambient_period780_only=ambient780,
        mu11_power_or_quotient_only=mu11_power,
        decision=decision,
        closes_source_stage=closes,
        first_missing_or_falsifier=missing,
        ok=True,
    )


def claim_rows() -> tuple[ValueBranchClaim, ...]:
    return (
        claim(
            "divisor_additive_with_h90_source",
            "finite divisor/additive identity for one legal row with H90 boundary",
            h90=True,
            source=True,
            finite=True,
            divisor=True,
        ),
        claim(
            "period156_value_with_source",
            "finite value identity for one legal row with support-period-156 context",
            source=True,
            finite=True,
            value=True,
            period156=True,
        ),
        claim(
            "ambient780_value_only",
            "ambient period-780 value theorem for the product",
            source=True,
            finite=True,
            value=True,
            ambient780=True,
        ),
        claim(
            "ambient780_mu11_power_only",
            "ambient period-780 value only after taking an 11th power or quotienting by mu_11",
            source=True,
            finite=True,
            value=True,
            mu11_power=True,
        ),
        claim(
            "value_without_period156_context",
            "bare finite value theorem with no support-period branch data",
            source=True,
            finite=True,
            value=True,
        ),
        claim(
            "direct_fp_order39_root",
            "choose a primitive order-39 root directly in F_p",
            direct_root=True,
        ),
        claim(
            "sqrt_minus39_scalar",
            "collapse chi_3 tensor chi_13 using sqrt(-39) as an F_p scalar",
            sqrt_scalar=True,
        ),
        claim(
            "degree6_orbit_no_descent",
            "compute in F_{p^6} but omit conjugate/norm descent back to F_p",
            degree6=True,
        ),
        claim(
            "degree6_norm_value_no_period156",
            "descend a degree-6 value to F_p but omit support-period-156 context",
            degree6=True,
            descent=True,
            source=True,
            finite=True,
            value=True,
        ),
        claim(
            "h90_boundary_without_value",
            "identify the H90 boundary or Norm_156(Y_507) but no finite theorem",
            h90=True,
        ),
        claim(
            "finite_payload_no_source",
            "local finite payload for one legal row with no arithmetic source theorem",
            h90=True,
            finite=True,
            divisor=True,
        ),
    )


def build_contract() -> Period156ValueBranchContract:
    markers = evidence_markers()
    order39 = multiplicative_order_mod(P25 % 39, 39)
    support_gcd = gcd(4**SUPPORT_PERIOD - 1, P25 - 1)
    ambient_gcd = gcd(4**AMBIENT_PERIOD - 1, P25 - 1)
    periods = (39, 78, 156, 312, 507, 780)
    small_gcds = tuple((period, gcd(4**period - 1, P25 - 1)) for period in periods)
    rows = claim_rows()
    accepted = sum(row.closes_source_stage for row in rows)
    repair = sum(row.decision.startswith("repair_") for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    current_closers = 0
    markers_ok = sum(row.ok for row in markers)
    row_ok = (
        markers_ok == len(markers)
        and P25 % 39 == 23
        and order39 == 6
        and pow(P25, 3, 39) == 38
        and pow((-39) % P25, (P25 - 1) // 2, P25) == P25 - 1
        and support_gcd == 1
        and ambient_gcd == 11
        and small_gcds == ((39, 1), (78, 1), (156, 1), (312, 1), (507, 1), (780, 11))
        and len(rows) == 11
        and accepted == 2
        and repair == 7
        and rejected == 2
        and current_closers == 0
        and all(row.ok for row in rows)
    )
    return Period156ValueBranchContract(
        evidence_markers=markers,
        p_mod_39=P25 % 39,
        p_order_mod39=order39,
        p_cubed_is_minus_one_mod39=pow(P25, 3, 39) == 38,
        sqrt_minus39_in_fp=pow((-39) % P25, (P25 - 1) // 2, P25) == 1,
        support_period=SUPPORT_PERIOD,
        ambient_period=AMBIENT_PERIOD,
        support_denominator_gcd_fp_star=support_gcd,
        ambient_denominator_gcd_fp_star=ambient_gcd,
        small_period_gcds_fp_star=small_gcds,
        direct_fp_order39_root_available=order39 == 1,
        support_value_root_unique_fp_star=support_gcd == 1,
        ambient_value_branch_count_fp_star=ambient_gcd,
        claims=rows,
        evidence_markers_ok=markers_ok,
        accepted_source_stage_shapes=accepted,
        repair_rows=repair,
        rejected_shortcuts=rejected,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for row in contract.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mod_39={contract.p_mod_39}")
    print(f"  p_order_mod39={contract.p_order_mod39}")
    print(f"  p_cubed_is_minus_one_mod39={int(contract.p_cubed_is_minus_one_mod39)}")
    print(f"  sqrt_minus39_in_fp={int(contract.sqrt_minus39_in_fp)}")
    print(f"  support_period={contract.support_period}")
    print(f"  ambient_period={contract.ambient_period}")
    print(f"  gcd_4^156_minus_1_with_Fp_star={contract.support_denominator_gcd_fp_star}")
    print(f"  gcd_4^780_minus_1_with_Fp_star={contract.ambient_denominator_gcd_fp_star}")
    print(f"  small_period_gcds_fp_star={contract.small_period_gcds_fp_star}")
    print(f"  direct_fp_order39_root_available={int(contract.direct_fp_order39_root_available)}")
    print(f"  support_value_root_unique_fp_star={int(contract.support_value_root_unique_fp_star)}")
    print(f"  ambient_value_branch_count_fp_star={contract.ambient_value_branch_count_fp_star}")
    print("claim_rows")
    for row in contract.claims:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source={int(row.arithmetic_source)} finite={int(row.finite_value_or_divisor)} "
            f"divisor={int(row.divisor_additive)} value={int(row.value_level)} "
            f"h90={int(row.h90_boundary)} degree6={int(row.degree6_orbit)} "
            f"descent={int(row.descent_to_fp)} period156={int(row.support_period156_context)} "
            f"ambient780={int(row.ambient_period780_only)} "
            f"mu11_power={int(row.mu11_power_or_quotient_only)} "
            f"closes={int(row.closes_source_stage)}"
        )
        print(f"    shape={row.shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  accepted_source_stage_shapes={contract.accepted_source_stage_shapes}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  rejected_shortcuts={contract.rejected_shortcuts}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print("interpretation")
    print("  divisor_additive_route_avoids_value_branch_ambiguity=1")
    print("  support_period156_value_route_has_unique_Fp_star_root=1")
    print("  ambient_period780_value_route_has_mu11_ambiguity=1")
    print("  direct_Fp_order39_root_and_sqrt_minus39_shortcuts_are_dead=1")
    print(f"p25_v2_period156_value_branch_contract_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
