#!/usr/bin/env python3
"""Square-axis graph-lift Fourier gate for p25 Lane B.

The boundary-residual gate shows that the C_169 target is a C_13 fiber
background plus an 18-point residual.  This gate refines the residual:

    residual(r, a + 13*b) = theta_13(r,a) on the graph b = 9 - 3*h,
    h = r - a mod 3.

The residual is therefore a skew graph lift of the C_13 trace-shadow mask into
three boundary fibers.  Surprisingly, each individual h-slice is already
Fourier-dense: even the 3-point h=0 slice has the full non-right character
support profile of the whole residual.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_divisor_footprint_gate import dft, primitive_root, rank_mod
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


BASE_C = 13
SQUARE_C = BASE_C * BASE_C
ODD_RANK_FIELD = 1_000_003


@dataclass(frozen=True)
class FourierProfile:
    nonzero: int
    scalar: int
    right_only: int
    pure_lift: int
    pure_nonlift: int
    mixed_lift: int
    mixed_nonlift: int
    by_right_frequency: tuple[int, int, int]


@dataclass(frozen=True)
class SliceProfile:
    h_value: int
    boundary_fiber: int
    coordinate_support: int
    row_sums: tuple[int, int, int]
    rank_f2: int
    rank_odd: int
    points: tuple[tuple[int, int, int], ...]
    fourier: FourierProfile


def residual_bit(right: int, c_index: int, h_filter: int | None = None) -> int:
    residue = c_index % BASE_C
    fiber = c_index // BASE_C
    h_value = (right - residue) % RIGHT_DEGREE
    if h_filter is not None and h_value != h_filter:
        return 0
    boundary = 9 - 3 * h_value
    return int(template_bits(BASE_C, residue)[right] and fiber == boundary)


def residual_vector(h_filter: int | None = None) -> list[int]:
    return [
        residual_bit(right, c_index, h_filter)
        for right in range(RIGHT_DEGREE)
        for c_index in range(SQUARE_C)
    ]


def graph_points(h_value: int) -> tuple[tuple[int, int, int], ...]:
    points: list[tuple[int, int, int]] = []
    for right in range(RIGHT_DEGREE):
        for residue in range(BASE_C):
            h_current = (right - residue) % RIGHT_DEGREE
            if h_current == h_value and template_bits(BASE_C, residue)[right]:
                points.append((right, residue, residue + BASE_C * (9 - 3 * h_value)))
    return tuple(points)


def fourier_profile(vector: list[int], modulus: int) -> FourierProfile:
    coefficients = dft(vector, SQUARE_C, modulus)
    nonzero = 0
    scalar = 0
    right_only = 0
    pure_lift = 0
    pure_nonlift = 0
    mixed_lift = 0
    mixed_nonlift = 0
    by_right_frequency = [0, 0, 0]
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(SQUARE_C):
            value = coefficients[right_frequency * SQUARE_C + c_frequency]
            if not value:
                continue
            nonzero += 1
            by_right_frequency[right_frequency] += 1
            if right_frequency == 0 and c_frequency == 0:
                scalar += 1
            elif right_frequency != 0 and c_frequency == 0:
                right_only += 1
            elif right_frequency == 0:
                if c_frequency % BASE_C == 0:
                    pure_lift += 1
                else:
                    pure_nonlift += 1
            else:
                if c_frequency % BASE_C == 0:
                    mixed_lift += 1
                else:
                    mixed_nonlift += 1
    return FourierProfile(
        nonzero=nonzero,
        scalar=scalar,
        right_only=right_only,
        pure_lift=pure_lift,
        pure_nonlift=pure_nonlift,
        mixed_lift=mixed_lift,
        mixed_nonlift=mixed_nonlift,
        by_right_frequency=tuple(by_right_frequency),
    )


def slice_profile(h_value: int, modulus: int) -> SliceProfile:
    vector = residual_vector(h_value)
    matrix = [
        vector[right * SQUARE_C : (right + 1) * SQUARE_C]
        for right in range(RIGHT_DEGREE)
    ]
    return SliceProfile(
        h_value=h_value,
        boundary_fiber=9 - 3 * h_value,
        coordinate_support=sum(vector),
        row_sums=tuple(sum(row) for row in matrix),  # type: ignore[arg-type]
        rank_f2=rank_mod(matrix, 2),
        rank_odd=rank_mod(matrix, ODD_RANK_FIELD),
        points=graph_points(h_value),
        fourier=fourier_profile(vector, modulus),
    )


def graph_formula_coefficients(modulus: int) -> list[int]:
    root = primitive_root(modulus)
    zeta_right = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zeta_c = pow(root, (modulus - 1) // SQUARE_C, modulus)
    coefficients: list[int] = []
    for right_frequency in range(RIGHT_DEGREE):
        for c_frequency in range(SQUARE_C):
            total = 0
            for right in range(RIGHT_DEGREE):
                right_factor = pow(zeta_right, right_frequency * right, modulus)
                for residue in range(BASE_C):
                    if not template_bits(BASE_C, residue)[right]:
                        continue
                    h_value = (right - residue) % RIGHT_DEGREE
                    boundary = 9 - 3 * h_value
                    c_index = residue + BASE_C * boundary
                    total += right_factor * pow(zeta_c, c_frequency * c_index, modulus)
            coefficients.append(total % modulus)
    return coefficients


def expected_fourier_profile() -> FourierProfile:
    return FourierProfile(
        nonzero=505,
        scalar=1,
        right_only=0,
        pure_lift=12,
        pure_nonlift=156,
        mixed_lift=24,
        mixed_nonlift=312,
        by_right_frequency=(169, 168, 168),
    )


def main() -> int:
    print("p25 Lane B square-axis graph-lift Fourier gate")
    print(f"right_degree={RIGHT_DEGREE}")
    print(f"base_c={BASE_C} square_c={SQUARE_C}")
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    print(f"modulus={modulus}")

    expected_profile = expected_fourier_profile()
    slices = [slice_profile(h_value, modulus) for h_value in range(RIGHT_DEGREE)]
    residual = residual_vector()
    residual_profile = fourier_profile(residual, modulus)
    residual_coefficients = dft(residual, SQUARE_C, modulus)
    graph_coefficients = graph_formula_coefficients(modulus)
    graph_formula_hits = sum(
        int(left == right)
        for left, right in zip(residual_coefficients, graph_coefficients)
    )

    slice_rows_ok = 0
    for current in slices:
        expected_support = RIGHT_DEGREE * (current.h_value + 1)
        expected_row_sums = (current.h_value + 1,) * RIGHT_DEGREE
        row_ok = (
            current.boundary_fiber == 9 - 3 * current.h_value
            and current.coordinate_support == expected_support
            and current.row_sums == expected_row_sums
            and current.rank_f2 == 3
            and current.rank_odd == 3
            and current.fourier == expected_profile
        )
        slice_rows_ok += int(row_ok)
        print(
            f"slice h={current.h_value}: "
            f"boundary_fiber={current.boundary_fiber} "
            f"coordinate_support={current.coordinate_support}/{expected_support} "
            f"row_sums={list(current.row_sums)} "
            f"rank_f2={current.rank_f2} "
            f"rank_odd={current.rank_odd} "
            f"fourier_nonzero={current.fourier.nonzero} "
            f"by_right_frequency={list(current.fourier.by_right_frequency)} "
            f"pure_lift={current.fourier.pure_lift} "
            f"pure_nonlift={current.fourier.pure_nonlift} "
            f"mixed_lift={current.fourier.mixed_lift} "
            f"mixed_nonlift={current.fourier.mixed_nonlift} "
            f"ok={int(row_ok)}"
        )
        print(f"  points={list(current.points)}")

    graph_row_ok = (
        graph_formula_hits == RIGHT_DEGREE * SQUARE_C
        and residual_profile == expected_profile
        and sum(residual) == 18
        and slice_rows_ok == RIGHT_DEGREE
    )
    print(
        f"graph_formula_hits={graph_formula_hits}/{RIGHT_DEGREE * SQUARE_C} "
        f"residual_support={sum(residual)}/18 "
        f"residual_fourier_nonzero={residual_profile.nonzero}/505 "
        f"slice_fourier_saturation_rows={slice_rows_ok}/{RIGHT_DEGREE} "
        f"ok={int(graph_row_ok)}"
    )
    print("graph_lift_law")
    print("  residual(r, a + 13*b) = theta_13(r,a) if b = 9 - 3*(r-a mod 3)")
    print("  each h-slice has full non-right C169 Fourier support")
    print(f"square_axis_graph_lift_fourier_rows={int(graph_row_ok)}/1")
    print("interpretation")
    print("  boundary_residual_is_a_skew_graph_lift_of_the_C13_trace_shadow=1")
    print("  every_single_boundary_slice_is_already_fourier_dense=1")
    print("  square_axis_producer_must_create_graph_lift_geometry_not_just_frequency_mass=1")
    print("conclusion=reported_p25_laneB_square_axis_graph_lift_fourier_gate")
    return 0 if graph_row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
