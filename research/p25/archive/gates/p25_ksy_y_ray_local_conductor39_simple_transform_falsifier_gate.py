#!/usr/bin/env python3
"""Cheap-transform falsifier from conductor-39 U_chi to theta31.

The alignment gate proves that U_chi=-chi_3*chi_13 is not the ray-local
theta31 payload.  This gate sharpens that into a first falsifier for common
"bridge by local massaging" claims: scalar/product-affine relabels,
row/column additive normalizations, and separated multiplicative gauges.

It deliberately does not reject genuine finite value/divisor theorems for
U_chi, W, Y_507, or H0.  Those remain source/value routes.  It only kills the
cheap claim that the conductor-39 source can be locally transformed into
theta31 without a real bridge or evaluation theorem.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import gcd

from p25_ksy_y_ray_local_conductor39_alignment_gate import (
    Matrix,
    profile_ray_local_conductor39_alignment,
    rank_over_q,
    support,
    theta31_matrix,
    theta_mixed_scaled_by_3,
    u_chi_matrix,
)


RIGHT_DEGREE = 3
C_AXIS = 13


@dataclass(frozen=True)
class ProductAffineSupportAudit:
    maps_checked: int
    exact_theta_support_matches: int
    exact_theta_mixed_support_matches: int
    max_theta_intersection: int
    max_theta_mixed_intersection: int
    theta_intersection_histogram: tuple[tuple[int, int], ...]
    theta_mixed_intersection_histogram: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class SeparatedAdditiveFit:
    target_name: str
    equation_count: int
    variable_count: int
    rank: int
    inconsistent_rows: int
    inconsistent_residuals: tuple[str, ...]
    solvable: bool


@dataclass(frozen=True)
class SimpleTransformFalsifierProfile:
    alignment_ok: bool
    theta31_support: int
    u_chi_support: int
    theta31_mixed_rank: int
    u_chi_rank: int
    combined_mixed_rank: int
    product_affine: ProductAffineSupportAudit
    raw_row_column_fit: SeparatedAdditiveFit
    mixed_row_column_fit: SeparatedAdditiveFit
    separated_multiplicative_rank_ceiling: int
    separated_multiplicative_reaches_theta31_mixed: bool
    killed_transform_classes: tuple[str, ...]
    live_route: str
    row_ok: bool


def units(modulus: int) -> tuple[int, ...]:
    return tuple(value for value in range(modulus) if gcd(value, modulus) == 1)


def product_affine_image(
    supp: set[tuple[int, int]], right_unit: int, right_shift: int, c_unit: int, c_shift: int
) -> set[tuple[int, int]]:
    return {
        ((right_unit * right + right_shift) % RIGHT_DEGREE, (c_unit * c_index + c_shift) % C_AXIS)
        for right, c_index in supp
    }


def product_affine_support_audit() -> ProductAffineSupportAudit:
    theta_supp = support(theta31_matrix())
    theta_mixed_supp = support(theta_mixed_scaled_by_3(theta31_matrix()))
    u_supp = support(u_chi_matrix())
    theta_hist: Counter[int] = Counter()
    theta_mixed_hist: Counter[int] = Counter()
    exact_theta = 0
    exact_theta_mixed = 0
    maps_checked = 0

    for right_unit in units(RIGHT_DEGREE):
        for right_shift in range(RIGHT_DEGREE):
            for c_unit in units(C_AXIS):
                for c_shift in range(C_AXIS):
                    image = product_affine_image(
                        u_supp, right_unit, right_shift, c_unit, c_shift
                    )
                    maps_checked += 1
                    if image == theta_supp:
                        exact_theta += 1
                    if image == theta_mixed_supp:
                        exact_theta_mixed += 1
                    theta_hist[len(image & theta_supp)] += 1
                    theta_mixed_hist[len(image & theta_mixed_supp)] += 1

    return ProductAffineSupportAudit(
        maps_checked=maps_checked,
        exact_theta_support_matches=exact_theta,
        exact_theta_mixed_support_matches=exact_theta_mixed,
        max_theta_intersection=max(theta_hist),
        max_theta_mixed_intersection=max(theta_mixed_hist),
        theta_intersection_histogram=tuple(sorted(theta_hist.items())),
        theta_mixed_intersection_histogram=tuple(sorted(theta_mixed_hist.items())),
    )


def separated_additive_fit(target_name: str, target: Matrix, source: Matrix) -> SeparatedAdditiveFit:
    """Solve target = a*source + row[right] + column[c] over Q.

    The row-plus-column gauge fixes row[0]=0, leaving variables:
    a, row[1], row[2], column[0], ..., column[12].
    """

    variable_count = 1 + (RIGHT_DEGREE - 1) + C_AXIS
    rows: list[list[Fraction]] = []
    for right in range(RIGHT_DEGREE):
        for c_index in range(C_AXIS):
            equation = [Fraction(0) for _ in range(variable_count)]
            equation[0] = Fraction(source[right][c_index])
            if right > 0:
                equation[right] = Fraction(1)
            equation[RIGHT_DEGREE + c_index] = Fraction(1)
            rows.append(equation + [Fraction(target[right][c_index])])

    rank = 0
    for column in range(variable_count):
        pivot = next(
            (row_index for row_index in range(rank, len(rows)) if rows[row_index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row_index in range(len(rows)):
            if row_index == rank or not rows[row_index][column]:
                continue
            factor = rows[row_index][column]
            rows[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(rows[row_index], rows[rank])
            ]
        rank += 1

    residuals = tuple(
        sorted(
            {
                str(row[variable_count])
                for row in rows
                if all(not row[column] for column in range(variable_count))
                and row[variable_count]
            }
        )
    )
    inconsistent_rows = sum(
        1
        for row in rows
        if all(not row[column] for column in range(variable_count)) and row[variable_count]
    )
    return SeparatedAdditiveFit(
        target_name=target_name,
        equation_count=RIGHT_DEGREE * C_AXIS,
        variable_count=variable_count,
        rank=rank,
        inconsistent_rows=inconsistent_rows,
        inconsistent_residuals=residuals,
        solvable=inconsistent_rows == 0,
    )


def profile_simple_transform_falsifier() -> SimpleTransformFalsifierProfile:
    alignment = profile_ray_local_conductor39_alignment()
    theta = theta31_matrix()
    theta_mixed = theta_mixed_scaled_by_3(theta)
    u_chi = u_chi_matrix()
    product_affine = product_affine_support_audit()
    raw_fit = separated_additive_fit("theta31_raw", theta, u_chi)
    mixed_fit = separated_additive_fit("theta31_mixed_scaled", theta_mixed, u_chi)
    killed = (
        "scalar_or_sign_multiple",
        "product_affine_relabel",
        "product_affine_plus_scalar",
        "row_column_additive_normalization",
        "separated_multiplicative_gauge",
    )
    separated_rank_ceiling = 1
    separated_reaches = rank_over_q(theta_mixed) <= separated_rank_ceiling
    row_ok = (
        alignment.row_ok
        and alignment.theta31_support == 18
        and alignment.u_chi_support == 24
        and rank_over_q(theta_mixed) == 2
        and rank_over_q(u_chi) == 1
        and rank_over_q(theta_mixed + u_chi) == 3
        and product_affine
        == ProductAffineSupportAudit(
            maps_checked=936,
            exact_theta_support_matches=0,
            exact_theta_mixed_support_matches=0,
            max_theta_intersection=12,
            max_theta_mixed_intersection=12,
            theta_intersection_histogram=((10, 288), (11, 288), (12, 360)),
            theta_mixed_intersection_histogram=((10, 432), (12, 504)),
        )
        and raw_fit
        == SeparatedAdditiveFit(
            target_name="theta31_raw",
            equation_count=39,
            variable_count=16,
            rank=16,
            inconsistent_rows=8,
            inconsistent_residuals=("-1", "1"),
            solvable=False,
        )
        and mixed_fit
        == SeparatedAdditiveFit(
            target_name="theta31_mixed_scaled",
            equation_count=39,
            variable_count=16,
            rank=16,
            inconsistent_rows=8,
            inconsistent_residuals=("-3", "3"),
            solvable=False,
        )
        and separated_rank_ceiling == 1
        and not separated_reaches
    )
    return SimpleTransformFalsifierProfile(
        alignment_ok=alignment.row_ok,
        theta31_support=alignment.theta31_support,
        u_chi_support=alignment.u_chi_support,
        theta31_mixed_rank=rank_over_q(theta_mixed),
        u_chi_rank=rank_over_q(u_chi),
        combined_mixed_rank=rank_over_q(theta_mixed + u_chi),
        product_affine=product_affine,
        raw_row_column_fit=raw_fit,
        mixed_row_column_fit=mixed_fit,
        separated_multiplicative_rank_ceiling=separated_rank_ceiling,
        separated_multiplicative_reaches_theta31_mixed=separated_reaches,
        killed_transform_classes=killed,
        live_route=(
            "genuine finite value/divisor theorem for U_chi, W, Y_507, or H0; "
            "not local theta31 conversion"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_simple_transform_falsifier()
    print("p25 KSY-y ray-local / conductor-39 simple-transform falsifier gate")
    print("alignment")
    print(f"  alignment_ok={int(profile.alignment_ok)}")
    print(f"  theta31_support={profile.theta31_support}")
    print(f"  u_chi_support={profile.u_chi_support}")
    print(f"  theta31_mixed_rank={profile.theta31_mixed_rank}")
    print(f"  u_chi_rank={profile.u_chi_rank}")
    print(f"  combined_mixed_rank={profile.combined_mixed_rank}")
    print("product_affine_support")
    print(f"  maps_checked={profile.product_affine.maps_checked}")
    print(f"  exact_theta_support_matches={profile.product_affine.exact_theta_support_matches}")
    print(
        "  exact_theta_mixed_support_matches="
        f"{profile.product_affine.exact_theta_mixed_support_matches}"
    )
    print(f"  max_theta_intersection={profile.product_affine.max_theta_intersection}")
    print(
        f"  max_theta_mixed_intersection={profile.product_affine.max_theta_mixed_intersection}"
    )
    print(
        "  theta_intersection_histogram="
        f"{profile.product_affine.theta_intersection_histogram}"
    )
    print(
        "  theta_mixed_intersection_histogram="
        f"{profile.product_affine.theta_mixed_intersection_histogram}"
    )
    print("row_column_additive_fit")
    print(f"  raw_fit={profile.raw_row_column_fit}")
    print(f"  mixed_fit={profile.mixed_row_column_fit}")
    print("separated_multiplicative_gauge")
    print(
        "  rank_ceiling="
        f"{profile.separated_multiplicative_rank_ceiling} "
        "reaches_theta31_mixed="
        f"{int(profile.separated_multiplicative_reaches_theta31_mixed)}"
    )
    print("interpretation")
    for killed in profile.killed_transform_classes:
        print(f"  killed_{killed}=1")
    print(f"  live_route={profile.live_route}")
    print("  require_explicit_bridge_or_value_theorem_beyond_simple_transform=1")
    print(
        "ksy_y_ray_local_conductor39_simple_transform_falsifier_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("ray-local / conductor-39 simple-transform falsifier failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
