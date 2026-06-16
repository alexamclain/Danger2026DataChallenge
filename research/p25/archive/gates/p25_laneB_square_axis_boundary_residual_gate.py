#!/usr/bin/env python3
"""Square-axis boundary-residual gate for p25 Lane B.

The fiber-placement law writes the C_169 target as a deterministic C_13 fiber
background plus one boundary injection on each carrying C_13 trace slot.  This
gate makes that decomposition explicit.

Write a C_169 coordinate as

    j = a + 13*b.

For row r, set h = r - a mod 3.  The base component is the C_13 half-arc row
h evaluated at b.  The residual is zero except at b = 9 - 3*h, where it is the
C_13 trace-shadow bit at (r,a).  Thus the 507-point C_169 mask splits into a
234-point deterministic fiber background plus an 18-point boundary residual.

The residual is sparse in coordinates but not low-frequency: its Fourier
support already uses every non-right character needed by the full square-axis
mask.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import dft, rank_mod
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


BASE_C = 13
SQUARE_C = BASE_C * BASE_C
ODD_RANK_FIELD = 1_000_003


@dataclass(frozen=True)
class ComponentProfile:
    name: str
    coordinate_support: int
    row_sums: tuple[int, int, int]
    rank_f2: int
    rank_odd: int
    fourier_nonzero: int
    scalar_support: int
    right_only_support: int
    pure_lift_support: int
    pure_nonlift_support: int
    mixed_lift_support: int
    mixed_nonlift_support: int


@dataclass(frozen=True)
class BoundaryResidualProfile:
    residual_prediction_hits: int
    residual_prediction_total: int
    decomposition_hits: int
    decomposition_total: int
    residual_ones: int
    residual_by_row: tuple[int, int, int]
    residual_by_h: tuple[int, int, int]
    residual_by_fiber: tuple[int, ...]
    boundary_positive_hits: int
    boundary_positive_total: int
    boundary_zero_hits: int
    boundary_zero_total: int
    nonboundary_zero_hits: int
    nonboundary_zero_total: int
    base_trace_hits: int
    residual_trace_hits: int
    square_trace_hits: int
    trace_total: int
    base_component: ComponentProfile
    residual_component: ComponentProfile
    square_component: ComponentProfile


def decompose_cell(right: int, c_index: int) -> tuple[int, int, int, int, int, int]:
    residue = c_index % BASE_C
    fiber = c_index // BASE_C
    h_value = (right - residue) % RIGHT_DEGREE
    trace_bit = template_bits(BASE_C, residue)[right]
    boundary = 9 - 3 * h_value
    base_bit = template_bits(BASE_C, fiber)[h_value]
    square_bit = template_bits(SQUARE_C, c_index)[right]
    predicted_residual = int(trace_bit == 1 and fiber == boundary)
    return base_bit, square_bit - base_bit, predicted_residual, trace_bit, h_value, boundary


def component_vector(which: str) -> list[int]:
    out: list[int] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(SQUARE_C):
            base_bit, residual_bit, _predicted, _trace_bit, _h_value, _boundary = decompose_cell(
                right, c_index
            )
            if which == "base":
                out.append(base_bit)
            elif which == "residual":
                out.append(residual_bit)
            elif which == "square":
                out.append(base_bit + residual_bit)
            else:
                raise AssertionError(f"unknown component {which}")
    return out


def component_profile(name: str, vector: list[int]) -> ComponentProfile:
    matrix = [
        vector[right * SQUARE_C : (right + 1) * SQUARE_C]
        for right in range(RIGHT_DEGREE)
    ]
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    coefficients = dft(vector, SQUARE_C, modulus)

    scalar_support = 0
    right_only_support = 0
    pure_lift_support = 0
    pure_nonlift_support = 0
    mixed_lift_support = 0
    mixed_nonlift_support = 0
    fourier_nonzero = 0
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(SQUARE_C):
            value = coefficients[right_frequency * SQUARE_C + c_frequency]
            if not value:
                continue
            fourier_nonzero += 1
            if right_frequency == 0 and c_frequency == 0:
                scalar_support += 1
            elif right_frequency != 0 and c_frequency == 0:
                right_only_support += 1
            elif right_frequency == 0:
                if c_frequency % BASE_C == 0:
                    pure_lift_support += 1
                else:
                    pure_nonlift_support += 1
            else:
                if c_frequency % BASE_C == 0:
                    mixed_lift_support += 1
                else:
                    mixed_nonlift_support += 1

    return ComponentProfile(
        name=name,
        coordinate_support=sum(1 for value in vector if value),
        row_sums=tuple(sum(row) for row in matrix),  # type: ignore[arg-type]
        rank_f2=rank_mod(matrix, 2),
        rank_odd=rank_mod(matrix, ODD_RANK_FIELD),
        fourier_nonzero=fourier_nonzero,
        scalar_support=scalar_support,
        right_only_support=right_only_support,
        pure_lift_support=pure_lift_support,
        pure_nonlift_support=pure_nonlift_support,
        mixed_lift_support=mixed_lift_support,
        mixed_nonlift_support=mixed_nonlift_support,
    )


def profile() -> BoundaryResidualProfile:
    residual_prediction_hits = 0
    decomposition_hits = 0
    residual_ones = 0
    residual_by_row = [0, 0, 0]
    residual_by_h = [0, 0, 0]
    residual_by_fiber = [0 for _ in range(BASE_C)]
    boundary_positive_hits = 0
    boundary_positive_total = 0
    boundary_zero_hits = 0
    boundary_zero_total = 0
    nonboundary_zero_hits = 0
    nonboundary_zero_total = 0
    base_trace_hits = 0
    residual_trace_hits = 0
    square_trace_hits = 0

    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            trace_bit = template_bits(BASE_C, residue)[right]
            base_trace = 0
            residual_trace = 0
            square_trace = 0
            for fiber in range(BASE_C):
                c_index = residue + BASE_C * fiber
                base_bit, residual_bit, predicted, _trace_bit, h_value, boundary = decompose_cell(
                    right, c_index
                )
                square_bit = template_bits(SQUARE_C, c_index)[right]
                residual_prediction_hits += int(residual_bit == predicted)
                decomposition_hits += int(square_bit == base_bit + residual_bit)
                residual_ones += int(residual_bit == 1)
                if residual_bit:
                    residual_by_row[right] += 1
                    residual_by_h[h_value] += 1
                    residual_by_fiber[fiber] += 1
                if fiber == boundary and trace_bit:
                    boundary_positive_total += 1
                    boundary_positive_hits += int(residual_bit == 1)
                elif fiber == boundary:
                    boundary_zero_total += 1
                    boundary_zero_hits += int(residual_bit == 0)
                else:
                    nonboundary_zero_total += 1
                    nonboundary_zero_hits += int(residual_bit == 0)
                base_trace += base_bit
                residual_trace += residual_bit
                square_trace += square_bit
            base_trace_hits += int(base_trace == 6)
            residual_trace_hits += int(residual_trace == trace_bit)
            square_trace_hits += int(square_trace == 6 + trace_bit)

    base_vector = component_vector("base")
    residual_vector = component_vector("residual")
    square_vector = component_vector("square")
    return BoundaryResidualProfile(
        residual_prediction_hits=residual_prediction_hits,
        residual_prediction_total=RIGHT_DEGREE * SQUARE_C,
        decomposition_hits=decomposition_hits,
        decomposition_total=RIGHT_DEGREE * SQUARE_C,
        residual_ones=residual_ones,
        residual_by_row=tuple(residual_by_row),
        residual_by_h=tuple(residual_by_h),
        residual_by_fiber=tuple(residual_by_fiber),
        boundary_positive_hits=boundary_positive_hits,
        boundary_positive_total=boundary_positive_total,
        boundary_zero_hits=boundary_zero_hits,
        boundary_zero_total=boundary_zero_total,
        nonboundary_zero_hits=nonboundary_zero_hits,
        nonboundary_zero_total=nonboundary_zero_total,
        base_trace_hits=base_trace_hits,
        residual_trace_hits=residual_trace_hits,
        square_trace_hits=square_trace_hits,
        trace_total=RIGHT_DEGREE * BASE_C,
        base_component=component_profile("base", base_vector),
        residual_component=component_profile("residual", residual_vector),
        square_component=component_profile("square", square_vector),
    )


def component_ok(component: ComponentProfile, expected: ComponentProfile) -> bool:
    return component == expected


def print_component(component: ComponentProfile) -> None:
    print(
        f"component {component.name}: "
        f"coordinate_support={component.coordinate_support} "
        f"row_sums={list(component.row_sums)} "
        f"rank_f2={component.rank_f2} "
        f"rank_odd={component.rank_odd} "
        f"fourier_nonzero={component.fourier_nonzero} "
        f"scalar_support={component.scalar_support} "
        f"right_only_support={component.right_only_support} "
        f"pure_lift_support={component.pure_lift_support} "
        f"pure_nonlift_support={component.pure_nonlift_support} "
        f"mixed_lift_support={component.mixed_lift_support} "
        f"mixed_nonlift_support={component.mixed_nonlift_support}"
    )


def main() -> int:
    print("p25 Lane B square-axis boundary-residual gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C}")
    current = profile()
    expected_base = ComponentProfile(
        name="base",
        coordinate_support=234,
        row_sums=(78, 78, 78),
        rank_f2=3,
        rank_odd=3,
        fourier_nonzero=469,
        scalar_support=1,
        right_only_support=0,
        pure_lift_support=0,
        pure_nonlift_support=156,
        mixed_lift_support=0,
        mixed_nonlift_support=312,
    )
    expected_residual = ComponentProfile(
        name="residual",
        coordinate_support=18,
        row_sums=(6, 6, 6),
        rank_f2=3,
        rank_odd=3,
        fourier_nonzero=505,
        scalar_support=1,
        right_only_support=0,
        pure_lift_support=12,
        pure_nonlift_support=156,
        mixed_lift_support=24,
        mixed_nonlift_support=312,
    )
    expected_square = ComponentProfile(
        name="square",
        coordinate_support=252,
        row_sums=(84, 84, 84),
        rank_f2=3,
        rank_odd=3,
        fourier_nonzero=505,
        scalar_support=1,
        right_only_support=0,
        pure_lift_support=12,
        pure_nonlift_support=156,
        mixed_lift_support=24,
        mixed_nonlift_support=312,
    )
    row_ok = (
        current.residual_prediction_hits == current.residual_prediction_total == 507
        and current.decomposition_hits == current.decomposition_total == 507
        and current.residual_ones == 18
        and current.residual_by_row == (6, 6, 6)
        and current.residual_by_h == (3, 6, 9)
        and current.residual_by_fiber == (0, 0, 0, 9, 0, 0, 6, 0, 0, 3, 0, 0, 0)
        and current.boundary_positive_hits == current.boundary_positive_total == 18
        and current.boundary_zero_hits == current.boundary_zero_total == 21
        and current.nonboundary_zero_hits == current.nonboundary_zero_total == 468
        and current.base_trace_hits == current.trace_total == 39
        and current.residual_trace_hits == current.trace_total == 39
        and current.square_trace_hits == current.trace_total == 39
        and component_ok(current.base_component, expected_base)
        and component_ok(current.residual_component, expected_residual)
        and component_ok(current.square_component, expected_square)
    )
    print(
        f"case square_axis_C3xC169: "
        f"residual_prediction_hits={current.residual_prediction_hits}/{current.residual_prediction_total} "
        f"decomposition_hits={current.decomposition_hits}/{current.decomposition_total} "
        f"residual_ones={current.residual_ones}/18 "
        f"residual_by_row={list(current.residual_by_row)} "
        f"residual_by_h={list(current.residual_by_h)} "
        f"residual_by_fiber={list(current.residual_by_fiber)} "
        f"boundary_positive_hits={current.boundary_positive_hits}/{current.boundary_positive_total} "
        f"boundary_zero_hits={current.boundary_zero_hits}/{current.boundary_zero_total} "
        f"nonboundary_zero_hits={current.nonboundary_zero_hits}/{current.nonboundary_zero_total} "
        f"base_trace_hits={current.base_trace_hits}/{current.trace_total} "
        f"residual_trace_hits={current.residual_trace_hits}/{current.trace_total} "
        f"square_trace_hits={current.square_trace_hits}/{current.trace_total} "
        f"ok={int(row_ok)}"
    )
    print_component(current.base_component)
    print_component(current.residual_component)
    print_component(current.square_component)
    print("boundary_residual_law")
    print("  j = a + 13*b")
    print("  h = right - a mod 3")
    print("  base = C13_half_arc_row[h][b]")
    print("  residual = C13_trace_bit(right,a) if b = 9 - 3*h else 0")
    print(f"square_axis_boundary_residual_rows={int(row_ok)}/1")
    print("interpretation")
    print("  C169_mask_splits_as_base_fiber_background_plus_18_point_boundary_residual=1")
    print("  residual_traces_down_exactly_to_the_C13_trace_shadow=1")
    print("  base_background_traces_down_to_constant_six_in_every_residue_slot=1")
    print("  sparse_residual_already_has_full_nonright_Fourier_support=1")
    print("conclusion=reported_p25_laneB_square_axis_boundary_residual_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
