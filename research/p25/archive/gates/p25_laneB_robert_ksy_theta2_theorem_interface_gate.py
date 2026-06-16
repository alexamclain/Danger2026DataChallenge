#!/usr/bin/env python3
"""Theorem-interface classifier for the p25 normalized-y KSY route.

The finite verifier path is now strong enough that future theorem or
literature hits should be triaged by a small contract:

* primary target: a challenge-legal divisor/additive identity for the
  normalized-y product over K_trace, D_segment, and T;
* support-period value route: possible only if the theorem also supplies the
  period-156 fixedness/telescoping context, where the F_p root is unique;
* finite-only shadows: source packets, quotient factors, and theta2 footprints
  are valid verifier payloads but do not prove arithmetic production;
* shortcuts that treat D as a hidden subgroup norm, ignore T, use post-hoc
  coefficient filtering, or confuse q-cycle/source coordinates are rejected.

This is not the missing theorem.  It is an executable intake rubric for the
next proof/literature pass.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import gcd, lcm

from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
    source_centers,
)
from p25_laneB_robert_ksy_theta2_resolvent_gate import P25, SQRT_FLOOR
from p25_laneB_robert_ksy_theta2_support_resolvent_gate import SUPPORT_PERIOD
from p25_laneB_robert_ksy_y_half_edge_footprint_gate import (
    half_step,
    inverse_step,
    normalized_y_exponent_footprint,
    symmetric_edge_ring,
)
from p25_laneB_robert_ksy_y_projection_gate import add_rings, scale_ring
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    add_coord,
    scale_coord,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
QuotientCoord = tuple[int, int]


@dataclass(frozen=True)
class TheoremInterfaceRow:
    name: str
    classification: str
    required_output: str
    finite_status: str
    first_falsifier_or_debt: str
    recommendation: str
    classification_ok: bool


@dataclass(frozen=True)
class TheoremInterfaceProfile:
    base_class: QuotientCoord
    d_class: QuotientCoord
    t_class: QuotientCoord
    quotient_packet_exact: bool
    k_trace_is_honest_norm: bool
    d_segment_is_not_subgroup_norm: bool
    t_edge_not_absorbed_by_k: bool
    forward_product_is_theta2_inverse: bool
    reversed_product_is_theta2: bool
    bridge_fixed_by_support_period: bool
    theta2_fixed_by_support_period: bool
    all_proper_period_divisors_fail: bool
    support_denominator_gcd_p25_minus_1: int
    ambient_denominator_gcd_p25_minus_1: int
    source_centers_support: int
    y_evaluation_support: int
    theta2_support: int
    bridge_support: int
    compact_telescoping_budget: int
    expanded_support_resolvent_budget: int
    accepted_theorem_targets: tuple[TheoremInterfaceRow, ...]
    finite_only_payloads: tuple[TheoremInterfaceRow, ...]
    conditional_value_routes: tuple[TheoremInterfaceRow, ...]
    rejected_shortcuts: tuple[TheoremInterfaceRow, ...]
    theorem_brief: str
    first_falsifier_suite: tuple[str, ...]
    next_lit_search_query_shape: str
    row_ok: bool


def coord_order(step: Coord, right_order: int = RIGHT_ORDER, c_order: int = C_ORDER) -> int:
    right_component = 1 if step[0] % right_order == 0 else right_order // gcd(right_order, step[0])
    c_component = 1 if step[1] % c_order == 0 else c_order // gcd(c_order, step[1])
    return lcm(right_component, c_component)


def quotient_class(coord: Coord) -> QuotientCoord:
    return (coord[0] % 3, coord[1] % C_ORDER)


def quotient_add(left: QuotientCoord, right: QuotientCoord) -> QuotientCoord:
    return ((left[0] + right[0]) % 3, (left[1] + right[1]) % C_ORDER)


def quotient_scale(step: QuotientCoord, scalar: int) -> QuotientCoord:
    return ((step[0] * scalar) % 3, (step[1] * scalar) % C_ORDER)


def quotient_source_packet(
    base_class: QuotientCoord,
    d_class: QuotientCoord,
    t_class: QuotientCoord,
) -> tuple[tuple[QuotientCoord, int], ...]:
    packet: dict[QuotientCoord, int] = {}
    for index in range(3):
        positive = quotient_add(base_class, quotient_scale(d_class, index))
        negative = quotient_add(positive, t_class)
        packet[positive] = packet.get(positive, 0) + 1
        packet[negative] = packet.get(negative, 0) - 1
    return tuple(sorted((coord, value) for coord, value in packet.items() if value))


def add_ring_entry(ring: Ring, coord: Coord, coefficient: int) -> None:
    ring[coord] = ring.get(coord, 0) + coefficient
    if ring[coord] == 0:
        del ring[coord]


def double_pushforward(ring: Ring) -> Ring:
    out: Ring = {}
    for coord, coefficient in ring.items():
        add_ring_entry(out, scale_coord(coord, 2), coefficient)
    return dict(sorted(out.items()))


def pushforward_power(ring: Ring, exponent: int) -> Ring:
    right_scale = pow(2, exponent, RIGHT_ORDER)
    c_scale = pow(2, exponent, C_ORDER)
    out: Ring = {}
    for coord, coefficient in ring.items():
        add_ring_entry(
            out,
            ((right_scale * coord[0]) % RIGHT_ORDER, (c_scale * coord[1]) % C_ORDER),
            coefficient,
        )
    return dict(sorted(out.items()))


def proper_divisors(value: int) -> tuple[int, ...]:
    return tuple(candidate for candidate in range(1, value) if value % candidate == 0)


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def y_evaluation_support(centers: Ring, t_step: Coord) -> int:
    left = set(centers)
    right = {add_coord(point, t_step) for point in centers}
    return len(left | right)


def profile_theorem_interface() -> TheoremInterfaceProfile:
    base_q = quotient_class(BASE_POINT)
    d_q = quotient_class(D_SHIFT)
    t_q = quotient_class(BRIDGE_SHIFT)
    packet = quotient_source_packet(base_q, d_q, t_q)
    expected_packet = (
        ((0, 31), 1),
        ((0, 138), -1),
        ((1, 25), 1),
        ((1, 141), -1),
        ((2, 28), 1),
        ((2, 144), -1),
    )

    k_trace = {scale_coord(KERNEL_SHIFT, index) for index in range(25)}
    d_after_three = scale_coord(D_SHIFT, 3)
    d_visible_after_three = quotient_scale(d_q, 3)
    centers = source_centers(BASE_POINT, KERNEL_SHIFT, D_SHIFT, 25, 3)
    forward = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    reversed_product = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
        reverse=True,
    )
    half = half_step(BRIDGE_SHIFT)
    center_base = add_coord(BASE_POINT, half)
    half_shift = inverse_step(half)
    theta2_inverse = normalized_y_exponent_footprint(center_base, half_shift)
    theta2 = scale_ring(theta2_inverse, -1)
    bridge = symmetric_edge_ring(center_base, half_shift)
    four_minus_double_bridge = add_rings(scale_ring(bridge, 4), scale_ring(double_pushforward(bridge), -1))

    support_denominator = 4 ** SUPPORT_PERIOD - 1
    ambient_denominator = 4 ** 780 - 1
    bridge_fixed = pushforward_power(bridge, SUPPORT_PERIOD) == bridge
    theta2_fixed = pushforward_power(theta2, SUPPORT_PERIOD) == theta2
    proper_fail = all(pushforward_power(theta2, period) != theta2 for period in proper_divisors(SUPPORT_PERIOD))
    y_support = y_evaluation_support(centers, BRIDGE_SHIFT)
    compact_budget = len(centers) + len(bridge) + len(theta2) + len(bridge) + len(theta2)
    expanded_budget = len(theta2) * SUPPORT_PERIOD

    k_trace_norm = (
        coord_order(KERNEL_SHIFT) == 25
        and len(k_trace) == 25
        and all(point[1] == 0 for point in k_trace)
        and all(quotient_class(point) == (0, 0) for point in k_trace)
    )
    d_not_norm = (
        coord_order(D_SHIFT) == 12675
        and lcm(3 // gcd(3, d_q[0]), C_ORDER // gcd(C_ORDER, d_q[1])) == 507
        and d_after_three == (66, 9)
        and d_visible_after_three == (0, 9)
    )
    theta2_shape_ok = (
        forward == theta2_inverse
        and reversed_product == theta2
        and theta2 == four_minus_double_bridge
        and len(forward) == 300
        and coefficient_counts(forward) == ((-4, 75), (-1, 75), (1, 75), (4, 75))
    )

    primary_targets = (
        TheoremInterfaceRow(
            "normalized_y_product_divisor_identity",
            "primary theorem target",
            (
                "prove prod_{A in base*K_trace*D_segment} "
                "y(A)/y(A+T)=theta2^-1 as divisor/additive data"
            ),
            "feeds theta2 inverse into the existing certificate chain",
            (
                "must handle D as a short non-subgroup segment with "
                "visible 3D=(0,9), not as an order-3 norm"
            ),
            "continue",
            theta2_shape_ok and k_trace_norm and d_not_norm,
        ),
        TheoremInterfaceRow(
            "reversed_normalized_y_product_divisor_identity",
            "primary theorem target",
            (
                "prove prod_{A in base*K_trace*D_segment} "
                "y(A+T)/y(A)=theta2 as divisor/additive data"
            ),
            "feeds theta2 into the existing bridge certificate chain",
            "orientation/sign must be recorded explicitly",
            "continue",
            theta2_shape_ok and reversed_product == theta2,
        ),
        TheoremInterfaceRow(
            "compact_ksy_theta2_from_arithmetic_identity",
            "compact theorem target",
            "derive center_base=(44,166), half_shift=(56,28), and orientation",
            "accepted by the compact theta2/telescoping skeleton",
            "must arise from a theorem, not hand-selected finite expansion",
            "continue",
            center_base == (44, 166)
            and half_shift == (56, 28)
            and compact_budget == 975
            and bridge_fixed
            and theta2_fixed,
        ),
    )

    finite_only = (
        TheoremInterfaceRow(
            "six_cell_source_quotient_packet",
            "finite-only payload",
            "emit the six signed source-quotient cells plus primitive K",
            "accepted finite verifier shadow",
            "does not by itself prove the arithmetic source of the packet",
            "use as theorem output only if accompanied by a producer identity",
            packet == expected_packet and len(packet) == 6,
        ),
        TheoremInterfaceRow(
            "quotient_factor_classes",
            "finite-only payload",
            "emit base=(1,25), D=(1,3), T=(2,113), primitive K",
            "accepted finite verifier shadow",
            "must explain why those quotient classes are selected",
            "use as compact theorem shadow",
            base_q == (1, 25) and d_q == (1, 3) and t_q == (2, 113),
        ),
        TheoremInterfaceRow(
            "sparse_theta2_divisor_payload",
            "finite-only payload",
            "emit exact 300-term theta2 or theta2^-1 divisor footprint",
            "accepted if output is divisor/additive data",
            "plain bridge has support 150 and is not theta2",
            "use as direct theorem payload if the theorem proves the footprint",
            len(theta2) == 300 and len(bridge) == 150 and bridge != theta2,
        ),
    )

    conditional = (
        TheoremInterfaceRow(
            "support_period_value_theta2_with_fixedness",
            "conditional value-level route",
            "emit theta2 value data plus the period-156 fixedness/telescoping context",
            "support-period denominator has unique F_p root",
            "must prove support-period fixedness; proper period divisors fail",
            "continue only with the full period-156 certificate context",
            gcd(support_denominator, P25 - 1) == 1
            and bridge_fixed
            and theta2_fixed
            and proper_fail,
        ),
        TheoremInterfaceRow(
            "ambient_780_value_unit_without_branch",
            "conditional old route",
            "use the ambient 780-term denominator on multiplicative values",
            "not accepted without branch/root selection",
            "gcd(4^780-1,p-1)=11 gives eleven value branches",
            "avoid unless the theorem selects a branch",
            gcd(ambient_denominator, P25 - 1) == 11,
        ),
    )

    rejected = (
        TheoremInterfaceRow(
            "fake_D_order3_norm",
            "reject",
            "treat the length-3 D segment as an order-3 subgroup norm",
            "finite arithmetic shape rejects this premise",
            "raw order(D)=12675, visible order(D)=507, visible 3D=(0,9)",
            "kill",
            d_not_norm,
        ),
        TheoremInterfaceRow(
            "K_trace_only_or_truncated_D_product",
            "reject",
            "drop or shorten the D segment while keeping the K trace",
            "theta2 product requires all three D-segment points",
            "D length 3 is required for the exact theta2 footprint",
            "kill",
            len(centers) == 75 and y_support == 150,
        ),
        TheoremInterfaceRow(
            "T_absorbed_or_missing_edge",
            "reject",
            "treat T as absorbed by the K quotient or omit the edge",
            "T is nontrivial in the quotient",
            f"T class is {t_q}, not (0,0)",
            "kill",
            t_q == (2, 113),
        ),
        TheoremInterfaceRow(
            "posthoc_abs4_coefficient_filter",
            "reject without theorem",
            "select the abs-4 layer after expansion and call it a producer",
            "layer selection is a finite filter, not an arithmetic identity",
            "the whole theta2 footprint has support 300 before any filter",
            "kill unless a theorem supplies the selector",
            len(theta2) == 300 and coefficient_counts(theta2) == ((-4, 75), (-1, 75), (1, 75), (4, 75)),
        ),
        TheoremInterfaceRow(
            "formal_two_norm_or_inverse_transport",
            "reject",
            "use only formal [2] norm or inverse-doubling transport",
            "multiplication by 2 has no useful kernel on C75 x C169",
            "theta2 equals (4-[2])B; the theorem must produce theta2, not a formal norm",
            "kill",
            gcd(2, RIGHT_ORDER) == 1 and gcd(2, C_ORDER) == 1 and theta2 == four_minus_double_bridge,
        ),
        TheoremInterfaceRow(
            "q_cycle_packet_as_source_packet",
            "reject",
            "submit old q-cycle coordinates as the source quotient packet",
            "source packet uses (q mod 3, q mod 169)",
            "coordinate convention mismatch was already a stable falsifier",
            "kill",
            packet == expected_packet,
        ),
    )

    all_rows = primary_targets + finite_only + conditional + rejected
    row_ok = (
        base_q == (1, 25)
        and d_q == (1, 3)
        and t_q == (2, 113)
        and packet == expected_packet
        and k_trace_norm
        and d_not_norm
        and theta2_shape_ok
        and bridge_fixed
        and theta2_fixed
        and proper_fail
        and gcd(support_denominator, P25 - 1) == 1
        and gcd(ambient_denominator, P25 - 1) == 11
        and len(centers) == 75
        and y_support == 150
        and len(theta2) == 300
        and len(bridge) == 150
        and compact_budget == 975
        and expanded_budget == 46800
        and expanded_budget < SQRT_FLOOR
        and all(row.classification_ok for row in all_rows)
    )

    return TheoremInterfaceProfile(
        base_class=base_q,
        d_class=d_q,
        t_class=t_q,
        quotient_packet_exact=packet == expected_packet,
        k_trace_is_honest_norm=k_trace_norm,
        d_segment_is_not_subgroup_norm=d_not_norm,
        t_edge_not_absorbed_by_k=t_q != (0, 0),
        forward_product_is_theta2_inverse=forward == theta2_inverse,
        reversed_product_is_theta2=reversed_product == theta2,
        bridge_fixed_by_support_period=bridge_fixed,
        theta2_fixed_by_support_period=theta2_fixed,
        all_proper_period_divisors_fail=proper_fail,
        support_denominator_gcd_p25_minus_1=gcd(support_denominator, P25 - 1),
        ambient_denominator_gcd_p25_minus_1=gcd(ambient_denominator, P25 - 1),
        source_centers_support=len(centers),
        y_evaluation_support=y_support,
        theta2_support=len(theta2),
        bridge_support=len(bridge),
        compact_telescoping_budget=compact_budget,
        expanded_support_resolvent_budget=expanded_budget,
        accepted_theorem_targets=primary_targets,
        finite_only_payloads=finite_only,
        conditional_value_routes=conditional,
        rejected_shortcuts=rejected,
        theorem_brief=(
            "Prove a challenge-legal KSY/Siegel-unit normalized-y product "
            "identity over the true K trace, the short non-subgroup D segment, "
            "and the nontrivial T edge, emitting theta2/theta2^-1 as "
            "divisor/additive data; value data should use the period-156 "
            "telescoping context where the F_p root is unique."
        ),
        first_falsifier_suite=(
            "visible 3D=(0,9) proves D is not an order-3 norm",
            "T=(2,113) is nontrivial in the quotient",
            "the product needs 75 centers, 150 y-values, and 300 g-divisor terms",
            "plain bridge has support 150 and is not theta2",
            "ambient 780 value normalization has 11 unresolved F_p branches",
            "support-period 156 value normalization has gcd(4^156-1,p-1)=1",
            "q-cycle/source-packet coordinate confusion is rejected",
        ),
        next_lit_search_query_shape=(
            "Kubert-Lang/Siegel-unit distribution theorem for a D=2 "
            "normalized-y product over a subgroup trace times a short "
            "non-subgroup arithmetic segment with support-period telescoping"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY normalized-y theorem-interface gate")
    profile = profile_theorem_interface()
    print(f"theorem_interface_profile={profile}")
    print("accepted_theorem_targets")
    for row in profile.accepted_theorem_targets:
        print(f"  {row.name}: ok={int(row.classification_ok)} class={row.classification}")
    print("finite_only_payloads")
    for row in profile.finite_only_payloads:
        print(f"  {row.name}: ok={int(row.classification_ok)} class={row.classification}")
    print("conditional_value_routes")
    for row in profile.conditional_value_routes:
        print(f"  {row.name}: ok={int(row.classification_ok)} class={row.classification}")
    print("rejected_shortcuts")
    for row in profile.rejected_shortcuts:
        print(f"  {row.name}: ok={int(row.classification_ok)} class={row.classification}")
    print("theorem_interface_laws")
    print("  normalized_y_product_identity_is_primary_theorem_target=1")
    print("  source_packet_factor_classes_and_sparse_theta2_are_finite_payloads_not_proofs=1")
    print("  support_period_value_route_has_unique_Fp_root_but_requires_period_context=1")
    print("  ambient_780_value_route_still_has_11_branch_ambiguity=1")
    print("  fake_D_norm_T_absorption_posthoc_filter_and_coordinate_confusion_are_rejected=1")
    print("interpretation")
    print("  next_lit_search_should_target_the_normalized_y_product_identity_not_generic_CM_data=1")
    print("  this_gate_is_an_intake_rubric_not_the_missing_theorem=1")
    print(f"robert_ksy_theta2_theorem_interface_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_theorem_interface_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
