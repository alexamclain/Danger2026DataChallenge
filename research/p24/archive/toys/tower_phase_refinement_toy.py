#!/usr/bin/env python3
"""Toy calibration for embedded class-field tower phase.

The third p24 target has

    h = 2 * 157 * 211 * 3107441

and the attractive formal route is to separate the quotient
`2*157*211` from the recovery subgroup of size `3107441`.  This toy uses the
small cyclic CM torsor

    D=-5000, h=30=2*3*5

over F_1259.  We take the recovery subgroup H=<g^6> of size 5 and decompose
the quotient G/H of size 6 through a tower 2 then 3:

    H=<g^6> <= K=<g^2> <= G.

The script builds the embedded period data from the actual CM cycle and then
records exactly what the tower needs:

* a top degree-2 period polynomial for K-cosets;
* two relative degree-3 refinement polynomials, one above each top root;
* a bivariate relation F(Z,Y) interpolating those refinements.

This is a positive shape theorem for towers, but it also shows the phase
obstruction: the relative refinements are not determined by the abstract
factorization 30=2*3*5 or by the top polynomial alone.  In the toy they are
constructed from the embedded j-cycle; in p24 that is the missing primitive.
"""

from __future__ import annotations

from dataclasses import dataclass

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    monic_poly_from_roots,
    pari_linear_roots,
    walk_cycle,
)

RECOVERY_SIZE = 5
FINE_QUOTIENT = H // RECOVERY_SIZE
TOP_SUBGROUP_STEP = 2
TOP_QUOTIENT = TOP_SUBGROUP_STEP
REFINEMENT_DEGREE = FINE_QUOTIENT // TOP_QUOTIENT


@dataclass(frozen=True)
class TowerData:
    cycle: list[int]
    fine_periods: list[int]
    top_periods: list[int]
    fine_poly: list[int]
    top_poly: list[int]
    refinement_polys: list[list[int]]
    interpolation_coeffs: list[tuple[int, int]]
    cross_zero_count: int


def period(values: list[int]) -> int:
    return sum(values) % Q


def interpolate_linear(z0: int, c0: int, z1: int, c1: int) -> tuple[int, int]:
    """Return beta, alpha such that beta + alpha*z_i = c_i over F_Q."""
    alpha = (c1 - c0) * pow((z1 - z0) % Q, -1, Q)
    alpha %= Q
    beta = (c0 - alpha * z0) % Q
    return beta, alpha


def eval_poly(poly: list[int], x: int) -> int:
    out = 0
    for coeff in reversed(poly):
        out = (out * x + coeff) % Q
    return out


def eval_interpolated(interpolation: list[tuple[int, int]], z: int, y: int) -> int:
    coeffs = [(beta + alpha * z) % Q for beta, alpha in interpolation]
    return eval_poly(coeffs, y)


def build_tower(cycle: list[int]) -> TowerData:
    # Fine H-cosets: r mod 6, each of size 5.
    fine_cosets = [
        [cycle[(r + FINE_QUOTIENT * k) % H] for k in range(RECOVERY_SIZE)]
        for r in range(FINE_QUOTIENT)
    ]
    fine_periods = [period(coset) for coset in fine_cosets]
    fine_poly = monic_poly_from_roots(fine_periods, Q)

    # Top K-cosets: parity r mod 2, each is union of three fine H-cosets.
    top_cosets = [
        [cycle[(r + TOP_QUOTIENT * k) % H] for k in range(H // TOP_QUOTIENT)]
        for r in range(TOP_QUOTIENT)
    ]
    top_periods = [period(coset) for coset in top_cosets]
    top_poly = monic_poly_from_roots(top_periods, Q)

    # Refinement above each top coset: the fine periods with the matching
    # parity.  Each polynomial has degree 3 in this toy.
    refinement_polys: list[list[int]] = []
    for parent in range(TOP_QUOTIENT):
        child_periods = [
            fine_periods[r]
            for r in range(parent, FINE_QUOTIENT, TOP_QUOTIENT)
        ]
        refinement_polys.append(monic_poly_from_roots(child_periods, Q))

    interpolation_coeffs = [
        interpolate_linear(
            top_periods[0],
            refinement_polys[0][i],
            top_periods[1],
            refinement_polys[1][i],
        )
        for i in range(REFINEMENT_DEGREE + 1)
    ]

    cross_zero_count = 0
    for parent, z in enumerate(top_periods):
        wrong = 1 - parent
        for r in range(wrong, FINE_QUOTIENT, TOP_QUOTIENT):
            if eval_interpolated(interpolation_coeffs, z, fine_periods[r]) == 0:
                cross_zero_count += 1

    return TowerData(
        cycle=cycle,
        fine_periods=fine_periods,
        top_periods=top_periods,
        fine_poly=fine_poly,
        top_poly=top_poly,
        refinement_polys=refinement_polys,
        interpolation_coeffs=interpolation_coeffs,
        cross_zero_count=cross_zero_count,
    )


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    tower = build_tower(cycle)

    print("tower phase refinement toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"recovery_subgroup_size={RECOVERY_SIZE}")
    print(f"fine_quotient_size={FINE_QUOTIENT}")
    print(f"tower_factorization={TOP_QUOTIENT}*{REFINEMENT_DEGREE}")
    print()
    print("period_polynomials")
    print(f"  top_periods={tower.top_periods}")
    print(f"  top_polynomial_degree={len(tower.top_poly) - 1}")
    print(f"  top_polynomial_coeffs_ascending={tower.top_poly}")
    print(f"  fine_periods={tower.fine_periods}")
    print(f"  fine_polynomial_degree={len(tower.fine_poly) - 1}")
    print(f"  fine_polynomial_coeffs_ascending={tower.fine_poly}")
    print()
    print("relative_refinement")
    for idx, poly in enumerate(tower.refinement_polys):
        print(
            f"  parent={idx} top_value={tower.top_periods[idx]} "
            f"child_polynomial_coeffs_ascending={poly}"
        )
    print("  bivariate_relation_coeffs_for_Y^i_as_beta_plus_alpha_Z=")
    for i, pair in enumerate(tower.interpolation_coeffs):
        print(f"    i={i}: beta={pair[0]} alpha={pair[1]}")
    print(f"  wrong_parent_cross_zeros={tower.cross_zero_count}")
    print()
    print("interpretation")
    print("  tower_decomposes_degree_6_quotient_into_degrees_2_and_3=1")
    print("  selected_top_root_plus_relative_polynomial_gives_three_children=1")
    print("  symmetrized_fine_polynomial_loses_parent_phase=1")
    print("  relative_polynomial_was_built_from_embedded_j_cycle=1")
    print(
        "conclusion=class_field_towers_reduce_root_degrees_only_after_the_"
        "embedded_relative_phase_data_has_been_constructed"
    )


if __name__ == "__main__":
    main()
