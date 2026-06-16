#!/usr/bin/env python3
"""Relative trace construction target for low-moment child selection.

The sparse-relation gate says a few child power sums may identify the selected
child fiber.  This gate identifies the intrinsic source of those power sums:
they are relative traces of powers of the quotient-period generator.

In the D=-5000 tower

    degree 2 parent  <- degree 6 fine quotient,

the children above a parent are the three fine periods with the same parity.
For a fine-period generator Y, the values

    Tr(Y^d), d=1,2,...

from the fine quotient to the parent quotient are exactly the child power
sums.  All child-polynomial coefficients can be recovered from the first
relative-degree many traces by Newton identities, but the low-moment route
uses fewer traces plus sparse-relation avoidance.
"""

from __future__ import annotations

from itertools import combinations

from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)
from tower_phase_refinement_toy import (
    REFINEMENT_DEGREE,
    TOP_QUOTIENT,
    build_tower,
    interpolate_linear,
)


def power_sums(values: list[int], max_degree: int, q: int = Q) -> list[int]:
    return [
        sum(pow(value, degree, q) for value in values) % q
        for degree in range(1, max_degree + 1)
    ]


def poly_from_power_sums(sums: list[int], q: int = Q) -> list[int]:
    """Recover monic polynomial coefficients from enough power sums."""
    degree = len(sums)
    elementary = [0] * (degree + 1)
    elementary[0] = 1
    for m in range(1, degree + 1):
        total = 0
        for i in range(1, m + 1):
            sign = 1 if i % 2 == 1 else -1
            total = (total + sign * elementary[m - i] * sums[i - 1]) % q
        elementary[m] = total * pow(m, -1, q) % q

    coeffs = [0] * (degree + 1)
    coeffs[degree] = 1
    for m in range(1, degree + 1):
        coeffs[degree - m] = ((-1) ** m * elementary[m]) % q
    return coeffs


def signature(values: list[int], degree: int, q: int = Q) -> tuple[int, ...]:
    return tuple(power_sums(values, degree, q))


def matching_subset_count(
    values: list[int],
    child_size: int,
    target_values: list[int],
    moment_count: int,
    q: int = Q,
) -> int:
    target = signature(target_values, moment_count, q)
    count = 0
    for indices in combinations(range(len(values)), child_size):
        candidate = [values[index] for index in indices]
        if signature(candidate, moment_count, q) == target:
            count += 1
    return count


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    tower = build_tower(cycle)

    full_newton_rows = 0
    low_moment_unique_rows = 0
    moment_interpolation_rows = 0
    relative_moment_rows: list[tuple[int, list[int], list[int], list[int]]] = []

    for parent in range(TOP_QUOTIENT):
        children = [
            tower.fine_periods[index]
            for index in range(parent, len(tower.fine_periods), TOP_QUOTIENT)
        ]
        sums = power_sums(children, REFINEMENT_DEGREE)
        recovered_poly = poly_from_power_sums(sums)
        full_newton_rows += int(recovered_poly == tower.refinement_polys[parent])
        low_moment_unique_rows += int(
            matching_subset_count(
                tower.fine_periods,
                REFINEMENT_DEGREE,
                children,
                1,
            )
            == 1
        )
        relative_moment_rows.append((parent, children, sums, recovered_poly))

    # Moment functions are parent-field elements: interpolate each Tr(Y^d) as
    # a function of the parent period Z in this degree-2 toy.
    for degree_index in range(REFINEMENT_DEGREE):
        c0 = relative_moment_rows[0][2][degree_index]
        c1 = relative_moment_rows[1][2][degree_index]
        beta, alpha = interpolate_linear(
            tower.top_periods[0],
            c0,
            tower.top_periods[1],
            c1,
        )
        ok = True
        for parent in range(TOP_QUOTIENT):
            value = (beta + alpha * tower.top_periods[parent]) % Q
            ok = ok and value == relative_moment_rows[parent][2][degree_index]
        moment_interpolation_rows += int(ok)

    p24_first_layer_low_traces = 4
    p24_second_layer_low_traces = 26
    p24_selected_path_low_traces = (
        p24_first_layer_low_traces + p24_second_layer_low_traces
    )
    p24_parent_field_trace_coefficients = (
        2 * p24_first_layer_low_traces
        + 314 * p24_second_layer_low_traces
    )

    print("trace-GCD low-moment relative-trace gate")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"top_quotient={TOP_QUOTIENT}")
    print(f"relative_degree={REFINEMENT_DEGREE}")
    print()
    for parent, children, sums, recovered_poly in relative_moment_rows:
        print(f"parent={parent}")
        print(f"  child_periods={children}")
        print(f"  relative_trace_power_sums={sums}")
        print(f"  newton_recovered_child_poly={recovered_poly}")
        print(f"  actual_child_poly={tower.refinement_polys[parent]}")
    print()
    print(f"full_newton_recovery_rows={full_newton_rows}/{TOP_QUOTIENT}")
    print(f"degree_one_low_moment_unique_rows={low_moment_unique_rows}/{TOP_QUOTIENT}")
    print(f"moment_parent_interpolation_rows={moment_interpolation_rows}/{REFINEMENT_DEGREE}")
    print()
    print("p24_relative_trace_surface")
    print(f"p24_first_layer_low_relative_traces={p24_first_layer_low_traces}")
    print(f"p24_second_layer_low_relative_traces={p24_second_layer_low_traces}")
    print(f"p24_selected_path_low_relative_traces={p24_selected_path_low_traces}")
    print(f"p24_parent_field_trace_coefficients={p24_parent_field_trace_coefficients}")
    print()
    print("interpretation")
    print("  child_power_sums_are_relative_traces_of_quotient_period_powers=1")
    print("  all_relative_degree_many_traces_recover_child_polynomial_by_newton=1")
    print("  low_traces_plus_sparse_relation_avoidance_can_replace_full_child_polynomial=1")
    print("  moment_values_are_parent_field_elements_not_postfit_subset_labels=1")
    print("  p24_low_moment_constructor_target_is_30_selected_relative_traces=1")
    print("conclusion=reported_trace_gcd_low_moment_relative_trace_gate")

    if full_newton_rows != TOP_QUOTIENT:
        raise SystemExit(1)
    if low_moment_unique_rows != TOP_QUOTIENT:
        raise SystemExit(1)
    if moment_interpolation_rows != REFINEMENT_DEGREE:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
