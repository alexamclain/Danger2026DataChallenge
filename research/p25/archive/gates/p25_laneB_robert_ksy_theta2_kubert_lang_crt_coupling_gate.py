#!/usr/bin/env python3
"""CRT coupling gate for the p25 KSY theta2 Kubert-Lang packet.

The exponent-matrix precheck showed that the six-cell source packet passes the
first Kubert-Lang congruence screen both at the mixed level 507 and after
projecting to the prime-power C169 axis.  This gate records the missing data:
the packet is not a C169 pullback or row/product artifact.  It is a graph lift
in C3 x C169, and a theorem-level producer must preserve that row selector.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd

from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_LEVEL,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    c_axis_projection,
    source_packet,
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class RowLiftCounts:
    total_lifts: int
    kl_congruence_lifts: int
    balanced_lifts: int
    balanced_kl_lifts: int
    d_segment_t_edge_lifts: int
    fixed_t_edge_lifts: int
    exact_base_d_t_lifts: int
    c_quadratic_ok_lifts: int
    mixed_quadratic_ok_lifts: int


@dataclass(frozen=True)
class KLCrtCouplingProfile:
    source_support: tuple[tuple[Coord, int, int], ...]
    positive_segment: tuple[tuple[Coord, int], ...]
    negative_segment: tuple[tuple[Coord, int], ...]
    d_step: Coord
    t_step: Coord
    d_q_step: int
    t_q_step: int
    d_q_order: int
    t_q_order: int
    three_d_q_step: int
    row_marginals: tuple[tuple[int, int], ...]
    c_projection_support: tuple[tuple[int, int], ...]
    c_pullback_support_size: int
    product_of_marginals_support_size: int
    row_lift_counts: RowLiftCounts
    c_projection_loses_row_selector: bool
    c_pullback_is_not_target: bool
    product_marginals_are_zero: bool
    graph_selector_ok: bool
    congruence_screen_is_not_selector: bool
    next_debt: str
    row_ok: bool


def add_coord(left: Coord, right: Coord) -> Coord:
    return (
        (left[0] + right[0]) % QUOTIENT_RIGHT_ORDER,
        (left[1] + right[1]) % C_ORDER,
    )


def q_from_coord(coord: Coord) -> int:
    right_class, c_log = coord
    return (
        C_ORDER * right_class + QUOTIENT_RIGHT_ORDER * c_log
    ) % QUOTIENT_LEVEL


def order_of_step(step: int, modulus: int) -> int:
    return modulus // gcd(step, modulus)


def row_marginals(packet: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(
        (row, sum(coefficient for (right, _c_log), coefficient in packet.items() if right == row))
        for row in range(QUOTIENT_RIGHT_ORDER)
    )


def c_projection_support(packet: Ring) -> tuple[tuple[int, int], ...]:
    projected = c_axis_projection(packet)
    return tuple(sorted((coord[1], coefficient) for coord, coefficient in projected.items()))


def c_pullback(packet: Ring) -> Ring:
    out: Ring = {}
    for c_log, coefficient in c_projection_support(packet):
        for row in range(QUOTIENT_RIGHT_ORDER):
            out[(row, c_log)] = coefficient
    return dict(sorted(out.items()))


def product_of_marginals(packet: Ring) -> Ring:
    rows = dict(row_marginals(packet))
    c_projection = dict(c_projection_support(packet))
    out: Ring = {}
    for row, row_weight in rows.items():
        for c_log, c_weight in c_projection.items():
            coefficient = row_weight * c_weight
            if coefficient:
                out[(row, c_log)] = coefficient
    return dict(sorted(out.items()))


def kl_congruence_ok(packet: Ring) -> bool:
    exponent_sum = sum(packet.values())
    quadratic_right = sum(
        coefficient * ((coord[0] * C_ORDER) % QUOTIENT_LEVEL) ** 2
        for coord, coefficient in packet.items()
    ) % QUOTIENT_LEVEL
    quadratic_c = sum(
        coefficient * ((coord[1] * QUOTIENT_RIGHT_ORDER) % QUOTIENT_LEVEL) ** 2
        for coord, coefficient in packet.items()
    ) % QUOTIENT_LEVEL
    quadratic_mixed = sum(
        coefficient
        * ((coord[0] * C_ORDER) % QUOTIENT_LEVEL)
        * ((coord[1] * QUOTIENT_RIGHT_ORDER) % QUOTIENT_LEVEL)
        for coord, coefficient in packet.items()
    ) % QUOTIENT_LEVEL
    return (
        exponent_sum % 12 == 0
        and quadratic_right == 0
        and quadratic_c == 0
        and quadratic_mixed == 0
    )


def c_quadratic_ok(packet: Ring) -> bool:
    return (
        sum(
            coefficient * ((coord[1] * QUOTIENT_RIGHT_ORDER) % QUOTIENT_LEVEL) ** 2
            for coord, coefficient in packet.items()
        )
        % QUOTIENT_LEVEL
        == 0
    )


def mixed_quadratic_ok(packet: Ring) -> bool:
    return (
        sum(
            coefficient
            * ((coord[0] * C_ORDER) % QUOTIENT_LEVEL)
            * ((coord[1] * QUOTIENT_RIGHT_ORDER) % QUOTIENT_LEVEL)
            for coord, coefficient in packet.items()
        )
        % QUOTIENT_LEVEL
        == 0
    )


def balanced(packet: Ring) -> bool:
    return all(total == 0 for _row, total in row_marginals(packet))


def positive_and_negative_segments(packet: Ring) -> tuple[tuple[Coord, ...], tuple[Coord, ...]]:
    positives = tuple(sorted((coord for coord, coefficient in packet.items() if coefficient > 0), key=lambda coord: coord[1]))
    negatives = tuple(sorted((coord for coord, coefficient in packet.items() if coefficient < 0), key=lambda coord: coord[1]))
    return positives, negatives


def d_segment_t_edge_shape(packet: Ring) -> bool:
    positives, negatives = positive_and_negative_segments(packet)
    if len(positives) != 3 or len(negatives) != 3:
        return False
    positive_d_ok = all(
        add_coord(positives[index], (1, 3)) == positives[index + 1]
        for index in range(2)
    )
    edge_deltas = {
        (
            (negative[0] - positive[0]) % QUOTIENT_RIGHT_ORDER,
            (negative[1] - positive[1]) % C_ORDER,
        )
        for positive, negative in zip(positives, negatives)
    }
    return positive_d_ok and len(edge_deltas) == 1


def fixed_t_edge_shape(packet: Ring) -> bool:
    positives, negatives = positive_and_negative_segments(packet)
    return d_segment_t_edge_shape(packet) and all(
        add_coord(positive, (2, 113)) == negative
        for positive, negative in zip(positives, negatives)
    )


def exact_base_d_t_shape(packet: Ring) -> bool:
    positives, _negatives = positive_and_negative_segments(packet)
    return fixed_t_edge_shape(packet) and positives[0] == (1, 25)


def row_lift_counts(packet: Ring) -> RowLiftCounts:
    c_entries = tuple(sorted((c_log, coefficient) for (_row, c_log), coefficient in packet.items()))
    total_lifts = 0
    kl_lifts = 0
    balanced_lifts = 0
    balanced_kl_lifts = 0
    d_segment_t_edge_lifts = 0
    fixed_t_edge_lifts = 0
    exact_base_d_t_lifts = 0
    c_quadratic_lifts = 0
    mixed_quadratic_lifts = 0
    for rows in product(range(QUOTIENT_RIGHT_ORDER), repeat=len(c_entries)):
        lift = {
            (row, c_log): coefficient
            for row, (c_log, coefficient) in zip(rows, c_entries)
        }
        total_lifts += 1
        kl_ok = kl_congruence_ok(lift)
        balanced_ok = balanced(lift)
        kl_lifts += int(kl_ok)
        balanced_lifts += int(balanced_ok)
        balanced_kl_lifts += int(kl_ok and balanced_ok)
        d_segment_t_edge_lifts += int(d_segment_t_edge_shape(lift))
        fixed_t_edge_lifts += int(fixed_t_edge_shape(lift))
        exact_base_d_t_lifts += int(exact_base_d_t_shape(lift))
        c_quadratic_lifts += int(c_quadratic_ok(lift))
        mixed_quadratic_lifts += int(mixed_quadratic_ok(lift))
    return RowLiftCounts(
        total_lifts=total_lifts,
        kl_congruence_lifts=kl_lifts,
        balanced_lifts=balanced_lifts,
        balanced_kl_lifts=balanced_kl_lifts,
        d_segment_t_edge_lifts=d_segment_t_edge_lifts,
        fixed_t_edge_lifts=fixed_t_edge_lifts,
        exact_base_d_t_lifts=exact_base_d_t_lifts,
        c_quadratic_ok_lifts=c_quadratic_lifts,
        mixed_quadratic_ok_lifts=mixed_quadratic_lifts,
    )


def profile_crt_coupling() -> KLCrtCouplingProfile:
    packet = source_packet()
    positives, negatives = positive_and_negative_segments(packet)
    source_support = tuple(
        (coord, q_from_coord(coord), coefficient)
        for coord, coefficient in sorted(packet.items())
    )
    positive_segment = tuple((coord, q_from_coord(coord)) for coord in positives)
    negative_segment = tuple((coord, q_from_coord(coord)) for coord in negatives)
    d_step = (
        (positives[1][0] - positives[0][0]) % QUOTIENT_RIGHT_ORDER,
        (positives[1][1] - positives[0][1]) % C_ORDER,
    )
    t_step = (
        (negatives[0][0] - positives[0][0]) % QUOTIENT_RIGHT_ORDER,
        (negatives[0][1] - positives[0][1]) % C_ORDER,
    )
    d_q_step = q_from_coord(d_step)
    t_q_step = q_from_coord(t_step)
    pullback = c_pullback(packet)
    product_marginal = product_of_marginals(packet)
    lifts = row_lift_counts(packet)
    c_projection = c_projection_support(packet)
    graph_selector_ok = (
        positives == ((1, 25), (2, 28), (0, 31))
        and negatives == ((0, 138), (1, 141), (2, 144))
        and d_step == (1, 3)
        and t_step == (2, 113)
    )
    congruence_screen_is_not_selector = (
        lifts.kl_congruence_lifts > 1
        and lifts.balanced_kl_lifts > 1
        and lifts.exact_base_d_t_lifts == 1
    )
    c_projection_loses_row_selector = (
        len(c_projection) == len(packet)
        and lifts.total_lifts == QUOTIENT_RIGHT_ORDER ** len(c_projection)
    )
    c_pullback_is_not_target = pullback != packet and len(pullback) == 18
    product_marginals_are_zero = product_marginal == {}
    row_ok = (
        source_support
        == (
            ((0, 31), 93, 1),
            ((0, 138), 414, -1),
            ((1, 25), 244, 1),
            ((1, 141), 85, -1),
            ((2, 28), 422, 1),
            ((2, 144), 263, -1),
        )
        and positive_segment == (((1, 25), 244), ((2, 28), 422), ((0, 31), 93))
        and negative_segment == (((0, 138), 414), ((1, 141), 85), ((2, 144), 263))
        and d_q_step == 178
        and t_q_step == 170
        and order_of_step(d_q_step, QUOTIENT_LEVEL) == QUOTIENT_LEVEL
        and order_of_step(t_q_step, QUOTIENT_LEVEL) == QUOTIENT_LEVEL
        and (3 * d_q_step) % QUOTIENT_LEVEL == 27
        and row_marginals(packet) == ((0, 0), (1, 0), (2, 0))
        and c_projection == ((25, 1), (28, 1), (31, 1), (138, -1), (141, -1), (144, -1))
        and c_pullback_is_not_target
        and product_marginals_are_zero
        and lifts
        == RowLiftCounts(
            total_lifts=729,
            kl_congruence_lifts=261,
            balanced_lifts=93,
            balanced_kl_lifts=93,
            d_segment_t_edge_lifts=9,
            fixed_t_edge_lifts=3,
            exact_base_d_t_lifts=1,
            c_quadratic_ok_lifts=729,
            mixed_quadratic_ok_lifts=729,
        )
        and graph_selector_ok
        and congruence_screen_is_not_selector
        and c_projection_loses_row_selector
    )
    return KLCrtCouplingProfile(
        source_support=source_support,
        positive_segment=positive_segment,
        negative_segment=negative_segment,
        d_step=d_step,
        t_step=t_step,
        d_q_step=d_q_step,
        t_q_step=t_q_step,
        d_q_order=order_of_step(d_q_step, QUOTIENT_LEVEL),
        t_q_order=order_of_step(t_q_step, QUOTIENT_LEVEL),
        three_d_q_step=(3 * d_q_step) % QUOTIENT_LEVEL,
        row_marginals=row_marginals(packet),
        c_projection_support=c_projection,
        c_pullback_support_size=len(pullback),
        product_of_marginals_support_size=len(product_marginal),
        row_lift_counts=lifts,
        c_projection_loses_row_selector=c_projection_loses_row_selector,
        c_pullback_is_not_target=c_pullback_is_not_target,
        product_marginals_are_zero=product_marginals_are_zero,
        graph_selector_ok=graph_selector_ok,
        congruence_screen_is_not_selector=congruence_screen_is_not_selector,
        next_debt=(
            "a theorem source must emit the graph lift "
            "(1,25)->(2,28)->(0,31) and its T=(2,113) translate; "
            "C169 congruences alone leave many legal row lifts"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang CRT-coupling gate")
    profile = profile_crt_coupling()
    print(f"crt_coupling_profile={profile}")
    print("mixed_level_packet")
    print(f"  source_support={profile.source_support}")
    print(f"  positive_segment={profile.positive_segment}")
    print(f"  negative_segment={profile.negative_segment}")
    print(
        "  "
        f"D_step={profile.d_step} q_step={profile.d_q_step} order={profile.d_q_order} "
        f"3D_q={profile.three_d_q_step}"
    )
    print(
        "  "
        f"T_step={profile.t_step} q_step={profile.t_q_step} order={profile.t_q_order}"
    )
    print("projection_falsifiers")
    print(f"  row_marginals={profile.row_marginals}")
    print(f"  C169_projection={profile.c_projection_support}")
    print(f"  full_C169_pullback_support={profile.c_pullback_support_size}")
    print(f"  product_of_row_and_C_marginals_support={profile.product_of_marginals_support_size}")
    print("row_lift_enumeration")
    print(f"  {profile.row_lift_counts}")
    print("interpretation")
    print("  C169_projection_passes_congruences_but_loses_the_row_selector=1")
    print("  full_C169_pullback_has_18_cells_not_the_six_cell_packet=1")
    print("  row_product_marginals_are_zero_so_no_product_reconstruction_exists=1")
    print("  KL_quadratic_congruences_leave_many_row_lifts_and_do_not_select_the_target=1")
    print("  target_is_a_graph_lift_with_D=(1,3)_and_T=(2,113)=1")
    print("  theorem_search_must_preserve_the_mixed_C3xC169_graph_data=1")
    print(f"robert_ksy_theta2_kubert_lang_crt_coupling_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
