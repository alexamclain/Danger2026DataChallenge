#!/usr/bin/env python3
"""Ray-local theta_{3,1} pullback falsifier for p25 Lane B.

This is a producer-facing harness for the p25 Lane B labs.  It does not
construct the missing CM-Artin or modular-unit object.  Instead, it packages
the finite obligations that such an object must satisfy on the actual local
sources exposed by the negative trace.

With no arguments, the script runs the synthetic canonical C_3 x C_13 control.
With ``--case square_axis_C3xC169`` it runs the larger square-axis opportunity
whose anchor descent is only degree 13.  With ``--raw-y PATH``, it reads a
candidate raw vector and checks it against the same contract for the selected
case.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from math import gcd
from pathlib import Path

from p25_laneB_c_axis_fourier_payload_gate import c_fourier_support, c_root_powers
from p25_laneB_canonical_half_arc_gate import support_interval, template_bits
from p25_laneB_diamond_conjugacy_gate import negative_inversion
from p25_laneB_divisor_footprint_gate import (
    packet_matrix,
    rank_mod,
    remove_scalar_component,
)
from p25_laneB_kummer_sign_descent_gate import kummer_class
from p25_laneB_literal_jacobi_packet_model import carry_packet
from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    PullbackCase,
    precompute_source_logs,
    quotient_coordinates,
)
from p25_laneB_punctured_hd_anchor_gate import make_context, primitive_root
from p25_laneB_right_eigenbasis_gate import right_eigenvectors
from p25_laneB_square_axis_digit_selector_gate import digit_rule
from p25_laneB_square_axis_local_graph_residue_gate import triangular_parameters
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    q_from_coord,
    selected_terms,
)
from p25_selected_defect_value_gate import (
    RIGHT_DEGREE,
    raw_producer_conditions,
    selected_defect,
    split_prime_for,
    value_conditions_hold,
)


@dataclass(frozen=True)
class CandidateAudit:
    name: str
    modulus: int
    scale: int | None
    source_coordinate_hits: int
    block_constancy_hits: int
    residue_rectangle_constancy_hits: int
    quotient_scale_hits: int
    zero_rectangle_hits: int
    carrying_rectangle_hits: int
    raw_carry_one_positions: int
    zone_carry_rectangles: dict[str, int]
    eigen_rank: int
    eigen_conjugacy: bool
    eigen_support: tuple[int | None, int | None, int]
    c_fourier_support_size: int
    selected_defect_ok: bool
    raw_product_ok: bool
    expected_kummer_degree: int
    kummer_descent_ok: bool
    ok: bool


def case_by_name(name: str) -> PullbackCase:
    by_name = {case.name: case for case in PULLBACK_CASES}
    if name not in by_name:
        raise ValueError(f"unknown Lane B pullback case: {name}")
    return by_name[name]


def tiny_case() -> PullbackCase:
    return case_by_name("tiny_C3xC13")


def zone_name(c_axis: int, c_index: int) -> str:
    m_value = (c_axis - 1) // 4
    if c_index <= m_value:
        return "zero"
    if c_index <= 2 * m_value:
        return "one_hot"
    if c_index <= 3 * m_value:
        return "two_hot"
    return "all_rows"


def local_coordinates(case: PullbackCase) -> list[tuple[int, int]]:
    source_logs = precompute_source_logs(case)
    return [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]


def synthetic_raw_y(
    case: PullbackCase, coordinates: list[tuple[int, int]], modulus: int
) -> list[int]:
    packet = carry_packet(case.c_axis, RIGHT_DEGREE, 1, modulus)
    inv_b = pow(case.b_trace % modulus, -1, modulus)
    return [
        packet[right * case.c_axis + c_index] * inv_b % modulus
        for right, c_index in coordinates
    ]


def parse_raw_y(path: Path, expected_length: int, modulus: int) -> list[int]:
    values = [int(token) % modulus for token in re.findall(r"-?\d+", path.read_text())]
    if len(values) != expected_length:
        raise ValueError(
            f"{path} contains {len(values)} integers, expected {expected_length}"
        )
    return values


def quotient_sums(
    raw_y: list[int],
    coordinates: list[tuple[int, int]],
    case: PullbackCase,
    modulus: int,
) -> list[int]:
    packet = [0] * (RIGHT_DEGREE * case.c_axis)
    for value, (right, c_index) in zip(raw_y, coordinates):
        packet[right * case.c_axis + c_index] += value
        packet[right * case.c_axis + c_index] %= modulus
    return packet


def block_value_sets(
    raw_y: list[int],
    coordinates: list[tuple[int, int]],
    case: PullbackCase,
) -> dict[tuple[int, int], set[int]]:
    values: dict[tuple[int, int], set[int]] = {}
    for value, coordinate in zip(raw_y, coordinates):
        values.setdefault(coordinate, set()).add(value)
    if len(values) != RIGHT_DEGREE * case.c_axis:
        raise AssertionError("coordinate quotient does not cover C_3 x C_c")
    return values


def quotient_scale(
    quotient: list[int], expected: list[int], modulus: int
) -> int | None:
    scale: int | None = None
    for value, target in zip(quotient, expected):
        if target % modulus == 0:
            if value % modulus:
                return None
            continue
        current = value * pow(target, -1, modulus) % modulus
        if scale is None:
            if current == 0:
                return None
            scale = current
        elif current != scale:
            return None
    return scale


def decompose_arbitrary_packet(
    packet: list[int], c_axis: int, modulus: int
) -> tuple[list[list[int]], list[int], list[list[int]]]:
    normalized, _scalar = remove_scalar_component(packet, modulus)
    matrix = packet_matrix(normalized, c_axis)
    inv_right = pow(RIGHT_DEGREE, -1, modulus)
    pure_c = [
        sum(matrix[right][c_index] for right in range(RIGHT_DEGREE))
        * inv_right
        % modulus
        for c_index in range(c_axis)
    ]
    mixed = [
        [
            (matrix[right][c_index] - pure_c[c_index]) % modulus
            for c_index in range(c_axis)
        ]
        for right in range(RIGHT_DEGREE)
    ]
    return matrix, pure_c, mixed


def expected_zone_carry_rectangles(c_axis: int) -> dict[str, int]:
    m_value = (c_axis - 1) // 4
    return {
        "zero": 0,
        "one_hot": m_value,
        "two_hot": 2 * m_value,
        "all_rows": RIGHT_DEGREE * m_value,
    }


def expected_support(c_axis: int) -> tuple[int, int, int]:
    m_value = (c_axis - 1) // 4
    return (m_value + 1, 3 * m_value, 2 * m_value)


def kummer_class_order(c_axis: int, class_index: int) -> int:
    if class_index % c_axis == 0:
        return 1
    return c_axis // gcd(c_axis, class_index)


def expected_kummer_degree(c_axis: int) -> int:
    if c_axis == 169:
        return 13
    return c_axis


def square_axis_boundary_residual_audit(
    quotient: list[int], modulus: int
) -> tuple[list[str], bool]:
    base_c = 13
    square_c = base_c * base_c
    if len(quotient) != RIGHT_DEGREE * square_c:
        raise AssertionError("square-axis residual audit expects C_3 x C_169")

    square_prediction_hits = 0
    residual_prediction_hits = 0
    residual_ones = 0
    residual_by_row = [0, 0, 0]
    residual_by_h = [0, 0, 0]
    residual_by_fiber = [0 for _ in range(base_c)]
    negative_residuals = 0
    oversize_residuals = 0
    boundary_positive_hits = 0
    boundary_positive_total = 0
    boundary_zero_hits = 0
    boundary_zero_total = 0
    nonboundary_zero_hits = 0
    nonboundary_zero_total = 0
    residual_trace_hits = 0
    observed_residual_qs: list[int] = []

    for right in range(RIGHT_DEGREE):
        for residue in range(base_c):
            trace_bit = template_bits(base_c, residue)[right]
            residual_trace = 0
            for fiber in range(base_c):
                c_index = residue + base_c * fiber
                observed = int(quotient[right * square_c + c_index] % modulus != 0)
                h_value = (right - residue) % RIGHT_DEGREE
                boundary = 9 - 3 * h_value
                base_bit = template_bits(base_c, fiber)[h_value]
                predicted_residual = int(trace_bit == 1 and fiber == boundary)
                predicted_square = base_bit + predicted_residual
                residual = observed - base_bit

                square_prediction_hits += int(observed == predicted_square)
                residual_prediction_hits += int(residual == predicted_residual)
                residual_ones += int(residual == 1)
                negative_residuals += int(residual < 0)
                oversize_residuals += int(residual > 1)
                if residual == 1:
                    residual_by_row[right] += 1
                    residual_by_h[h_value] += 1
                    residual_by_fiber[fiber] += 1
                    observed_residual_qs.append((square_c * right + RIGHT_DEGREE * c_index) % (RIGHT_DEGREE * square_c))
                if fiber == boundary and trace_bit:
                    boundary_positive_total += 1
                    boundary_positive_hits += int(residual == 1)
                elif fiber == boundary:
                    boundary_zero_total += 1
                    boundary_zero_hits += int(residual == 0)
                else:
                    nonboundary_zero_total += 1
                    nonboundary_zero_hits += int(residual == 0)
                residual_trace += residual
            residual_trace_hits += int(residual_trace == trace_bit)

    observed_residual_qs = sorted(observed_residual_qs)
    expected_residual_qs = sorted(q_value for *_prefix, q_value in triangular_parameters())
    quotient_shift_qs = sorted(
        q_from_coord(right, c_index)
        for _s_value, _h_value, _t_value, right, c_index in selected_terms()
    )
    quotient_shift_set_match = observed_residual_qs == quotient_shift_qs
    quotient_shift_hits = sum(int(q_value in set(observed_residual_qs)) for q_value in quotient_shift_qs)
    quotient_shift_layer_counts = [0, 0, 0]
    quotient_shift_h_counts = [0, 0, 0]
    quotient_shift_t_counts = [0, 0, 0]
    for s_value, h_value, t_value, _right, _c_index in selected_terms():
        quotient_shift_layer_counts[s_value] += 1
        quotient_shift_h_counts[h_value] += 1
        quotient_shift_t_counts[t_value] += 1
    digit_rule_hits = sum(int(digit_rule(q_value)) for q_value in observed_residual_qs)
    expected_digit_rule_hits = sum(int(digit_rule(q_value)) for q_value in expected_residual_qs)
    no_borrow_hits = 0
    for q_value in observed_residual_qs:
        m_value, r_value = divmod(q_value, 43)
        if r_value % 9:
            continue
        t_value = r_value // 9
        h_value = (m_value - 1) % 4
        no_borrow_hits += int(0 <= h_value <= 2 and 0 <= t_value <= 2 and t_value <= h_value)
    observed_q_set_match = observed_residual_qs == expected_residual_qs
    row_ok = (
        square_prediction_hits == RIGHT_DEGREE * square_c
        and residual_prediction_hits == RIGHT_DEGREE * square_c
        and residual_ones == 18
        and residual_by_row == [6, 6, 6]
        and residual_by_h == [3, 6, 9]
        and residual_by_fiber == [0, 0, 0, 9, 0, 0, 6, 0, 0, 3, 0, 0, 0]
        and negative_residuals == 0
        and oversize_residuals == 0
        and boundary_positive_hits == boundary_positive_total == 18
        and boundary_zero_hits == boundary_zero_total == 21
        and nonboundary_zero_hits == nonboundary_zero_total == 468
        and residual_trace_hits == RIGHT_DEGREE * base_c
        and observed_q_set_match
        and quotient_shift_set_match
        and quotient_shift_hits == 18
        and quotient_shift_layer_counts == [6, 6, 6]
        and quotient_shift_h_counts == [3, 6, 9]
        and quotient_shift_t_counts == [9, 6, 3]
        and digit_rule_hits == expected_digit_rule_hits == 18
        and no_borrow_hits == 18
    )
    lines = [
        (
            "  square_axis_boundary_residual: "
            f"square_prediction_hits={square_prediction_hits}/{RIGHT_DEGREE * square_c} "
            f"residual_prediction_hits={residual_prediction_hits}/{RIGHT_DEGREE * square_c} "
            f"residual_ones={residual_ones}/18 "
            f"residual_by_row={residual_by_row} "
            f"residual_by_h={residual_by_h} "
            f"residual_by_fiber={residual_by_fiber} "
            f"negative_residuals={negative_residuals} "
            f"oversize_residuals={oversize_residuals} "
            f"boundary_positive_hits={boundary_positive_hits}/{boundary_positive_total} "
            f"boundary_zero_hits={boundary_zero_hits}/{boundary_zero_total} "
            f"nonboundary_zero_hits={nonboundary_zero_hits}/{nonboundary_zero_total} "
            f"residual_trace_hits={residual_trace_hits}/{RIGHT_DEGREE * base_c} "
            f"observed_q_count={len(observed_residual_qs)}/18 "
            f"observed_q_set_match={int(observed_q_set_match)} "
            f"quotient_shift_set_match={int(quotient_shift_set_match)} "
            f"quotient_shift_hits={quotient_shift_hits}/18 "
            f"quotient_shift_layers={quotient_shift_layer_counts} "
            f"quotient_shift_h_counts={quotient_shift_h_counts} "
            f"quotient_shift_t_counts={quotient_shift_t_counts} "
            f"digit_rule_hits={digit_rule_hits}/18 "
            f"no_borrow_hits={no_borrow_hits}/18 "
            f"ok={int(row_ok)}"
        ),
        f"    observed_residual_qs={observed_residual_qs}",
        f"    expected_residual_qs={expected_residual_qs}",
        f"    quotient_shift_qs={quotient_shift_qs}",
    ]
    return lines, row_ok


def anchor_kummer_ok(c_axis: int) -> tuple[bool, int]:
    ctx = make_context(RIGHT_DEGREE * c_axis)
    generator = primitive_root(ctx.value_field_l)
    anchor = (ctx.base_field_q - 2) % ctx.value_field_l
    anchor_row = kummer_class("anchor", anchor, c_axis, ctx.value_field_l, generator)
    neg_anchor_row = kummer_class(
        "-anchor", -anchor, c_axis, ctx.value_field_l, generator
    )
    sign_row = kummer_class("-1", -1, c_axis, ctx.value_field_l, generator)
    expected_degree = expected_kummer_degree(c_axis)
    return (
        sign_row.class_index == 0
        and neg_anchor_row.class_index == anchor_row.class_index
        and kummer_class_order(c_axis, anchor_row.class_index) == expected_degree
        and kummer_class_order(c_axis, neg_anchor_row.class_index) == expected_degree
        and not anchor_row.base_has_root
        and not neg_anchor_row.base_has_root
        and anchor_row.minimal_extension_degree == expected_degree
        and neg_anchor_row.minimal_extension_degree == expected_degree
        and anchor_row.root_degrees_up_to_c
        == tuple(range(expected_degree, c_axis + 1, expected_degree))
        and neg_anchor_row.root_degrees_up_to_c
        == tuple(range(expected_degree, c_axis + 1, expected_degree))
    ), expected_degree


def case_label(case: PullbackCase) -> str:
    return (
        f"{case.name}: "
        f"right_sources={[source.name for source in case.right_sources]} "
        f"c_source={case.c_source.name}"
    )


def summarize_support(support: set[int]) -> str:
    values = sorted(support)
    if len(values) <= 24:
        return str(values)
    return (
        f"count={len(values)} "
        f"first={values[:8]} "
        f"last={values[-8:]}"
    )


def audit_candidate(
    name: str,
    raw_y: list[int],
    case: PullbackCase,
    coordinates: list[tuple[int, int]],
    modulus: int,
) -> tuple[list[str], bool]:
    expected = carry_packet(case.c_axis, RIGHT_DEGREE, 1, modulus)
    quotient = quotient_sums(raw_y, coordinates, case, modulus)
    value_sets = block_value_sets(raw_y, coordinates, case)
    scale = quotient_scale(quotient, expected, modulus)

    source_coordinate_hits = sum(
        int(0 <= right < RIGHT_DEGREE and 0 <= c_index < case.c_axis)
        for right, c_index in coordinates
    )
    block_constancy_hits = sum(
        int(len(values) == 1 and len(values) <= case.b_trace)
        for values in value_sets.values()
    )
    residue_rectangle_constancy_hits = block_constancy_hits
    zero_rectangle_hits = 0
    carrying_rectangle_hits = 0
    quotient_scale_hits = 0
    raw_carry_one_positions = 0
    zone_carry_rectangles = {"zero": 0, "one_hot": 0, "two_hot": 0, "all_rows": 0}

    for right in range(RIGHT_DEGREE):
        for c_index in range(case.c_axis):
            index = right * case.c_axis + c_index
            expected_carry = int(expected[index] % modulus != 0)
            observed_carry = int(quotient[index] % modulus != 0)
            if expected_carry:
                carrying_rectangle_hits += int(observed_carry)
                zone_carry_rectangles[zone_name(case.c_axis, c_index)] += int(
                    observed_carry
                )
            else:
                zero_rectangle_hits += int(not observed_carry)
            if scale is not None:
                quotient_scale_hits += int(
                    quotient[index] == scale * expected[index] % modulus
                )

    for value, (right, c_index) in zip(raw_y, coordinates):
        expected_carry = template_bits(case.c_axis, c_index)[right]
        raw_carry_one_positions += int(expected_carry and value % modulus != 0)

    _matrix, _pure_c, mixed = decompose_arbitrary_packet(
        quotient, case.c_axis, modulus
    )
    _eigen_0, eigen_1, eigen_2 = right_eigenvectors(
        mixed, case.c_axis, modulus
    )
    eigen_rank = rank_mod([eigen_1, eigen_2], modulus)
    eigen_conjugacy = eigen_2 == negative_inversion(eigen_1, modulus)
    eigen_support = support_interval(eigen_1, modulus)
    powers = c_root_powers(case.c_axis, modulus)
    support_1 = c_fourier_support(eigen_1, powers, modulus)
    support_2 = c_fourier_support(eigen_2, powers, modulus)
    full_nontrivial_support = set(range(1, case.c_axis))
    c_fourier_ok = support_1 == full_nontrivial_support and support_2 == full_nontrivial_support

    defect = selected_defect(quotient, case.c_axis, modulus)
    selected_defect_ok = value_conditions_hold(defect, case.c_axis, modulus)
    raw_product_ok = raw_producer_conditions(quotient, case.c_axis, modulus)
    kummer_descent_ok, kummer_degree = anchor_kummer_ok(case.c_axis)
    square_residual_lines: list[str] = []
    square_residual_ok = True
    if case.c_axis == 169:
        square_residual_lines, square_residual_ok = square_axis_boundary_residual_audit(
            quotient, modulus
        )
    expected_zone_carry = expected_zone_carry_rectangles(case.c_axis)
    expected_carrying_rectangles = sum(expected_zone_carry.values())
    expected_zero_rectangles = RIGHT_DEGREE * case.c_axis - expected_carrying_rectangles
    expected_raw_carry_positions = case.b_trace * expected_carrying_rectangles
    expected_fourier_support = case.c_axis - 1
    expected_eigen_support = expected_support(case.c_axis)
    row_ok = (
        source_coordinate_hits == case.raw_order
        and block_constancy_hits == RIGHT_DEGREE * case.c_axis
        and residue_rectangle_constancy_hits == RIGHT_DEGREE * case.c_axis
        and scale is not None
        and quotient_scale_hits == RIGHT_DEGREE * case.c_axis
        and zero_rectangle_hits == expected_zero_rectangles
        and carrying_rectangle_hits == expected_carrying_rectangles
        and raw_carry_one_positions == expected_raw_carry_positions
        and zone_carry_rectangles == expected_zone_carry
        and eigen_rank == 2
        and eigen_conjugacy
        and eigen_support == expected_eigen_support
        and c_fourier_ok
        and selected_defect_ok
        and raw_product_ok
        and kummer_descent_ok
        and square_residual_ok
    )
    audit = CandidateAudit(
        name=name,
        modulus=modulus,
        scale=scale,
        source_coordinate_hits=source_coordinate_hits,
        block_constancy_hits=block_constancy_hits,
        residue_rectangle_constancy_hits=residue_rectangle_constancy_hits,
        quotient_scale_hits=quotient_scale_hits,
        zero_rectangle_hits=zero_rectangle_hits,
        carrying_rectangle_hits=carrying_rectangle_hits,
        raw_carry_one_positions=raw_carry_one_positions,
        zone_carry_rectangles=zone_carry_rectangles,
        eigen_rank=eigen_rank,
        eigen_conjugacy=eigen_conjugacy,
        eigen_support=eigen_support,
        c_fourier_support_size=len(support_1),
        selected_defect_ok=selected_defect_ok,
        raw_product_ok=raw_product_ok,
        expected_kummer_degree=kummer_degree,
        kummer_descent_ok=kummer_descent_ok,
        ok=row_ok,
    )
    lines = [
        (
            f"candidate {audit.name}: case={case.name} c={case.c_axis} B={case.b_trace} "
            f"raw_order={case.raw_order} modulus={audit.modulus} "
            f"scale={audit.scale} "
            f"source_coordinate_hits={audit.source_coordinate_hits}/{case.raw_order} "
            f"block_constancy_hits={audit.block_constancy_hits}/{RIGHT_DEGREE * case.c_axis} "
            f"residue_rectangle_constancy_hits={audit.residue_rectangle_constancy_hits}/{RIGHT_DEGREE * case.c_axis} "
            f"quotient_scale_hits={audit.quotient_scale_hits}/{RIGHT_DEGREE * case.c_axis} "
            f"zero_rectangle_hits={audit.zero_rectangle_hits}/{expected_zero_rectangles} "
            f"carrying_rectangle_hits={audit.carrying_rectangle_hits}/{expected_carrying_rectangles} "
            f"raw_carry_one_positions={audit.raw_carry_one_positions}/{expected_raw_carry_positions} "
            f"eigen_rank={audit.eigen_rank} "
            f"eigen_conjugacy={int(audit.eigen_conjugacy)} "
            f"eigen_support={audit.eigen_support} "
            f"expected_eigen_support={expected_eigen_support} "
            f"c_fourier_support_size={audit.c_fourier_support_size}/{expected_fourier_support} "
            f"selected_defect_ok={int(audit.selected_defect_ok)} "
            f"raw_product_ok={int(audit.raw_product_ok)} "
            f"expected_kummer_degree={audit.expected_kummer_degree} "
            f"kummer_descent_ok={int(audit.kummer_descent_ok)} "
            f"ok={int(audit.ok)}"
        ),
        f"  zone_carry_rectangles={audit.zone_carry_rectangles}",
        f"  expected_zone_carry_rectangles={expected_zone_carry}",
        *square_residual_lines,
        f"  c_fourier_support_1={summarize_support(support_1)}",
        f"  c_fourier_support_2={summarize_support(support_2)}",
    ]
    return lines, row_ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a p25 Lane B raw theta_3_1 producer candidate."
    )
    parser.add_argument(
        "--case",
        choices=[case.name for case in PULLBACK_CASES],
        default="tiny_C3xC13",
        help="Lane B pullback case to check; default is the tiny C_3 x C_13 lab",
    )
    parser.add_argument(
        "--raw-y",
        type=Path,
        help="optional raw candidate vector with length matching the selected case",
    )
    args = parser.parse_args()

    case = case_by_name(args.case)
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    coordinates = local_coordinates(case)
    if args.raw_y is None:
        candidate_name = f"synthetic_canonical_control_{case.name}"
        raw_y = synthetic_raw_y(case, coordinates, modulus)
    else:
        candidate_name = str(args.raw_y)
        raw_y = parse_raw_y(args.raw_y, case.raw_order, modulus)

    print("p25 Lane B ray-local theta_3_1 pullback falsifier gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(case_label(case))
    print("mode=synthetic_control" if args.raw_y is None else "mode=raw_candidate")
    lines, ok = audit_candidate(candidate_name, raw_y, case, coordinates, modulus)
    for line in lines:
        print(line)
    print(f"ray_local_theta31_pullback_rows={int(ok)}/1")
    print("interpretation")
    print("  raw_candidate_must_embed_on_the_selected_actual_local_source=1")
    print("  B_block_and_local_residue_rectangle_constancy_are_required=1")
    print("  quotient_packet_must_equal_canonical_theta_3_1_up_to_global_scale=1")
    print("  square_axis_candidates_must_obey_the_base_plus_boundary_residual_law=1")
    print("  square_axis_candidates_must_match_the_triangular_digit_no_borrow_quotient_shift_comb=1")
    print("  right_character_payload_must_be_rank2_full_C_axis_and_diamond_conjugate=1")
    print("  selected_case_anchor_must_have_recorded_kummer_descent=1")
    print("conclusion=reported_p25_laneB_ray_local_theta31_pullback_falsifier_gate")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
