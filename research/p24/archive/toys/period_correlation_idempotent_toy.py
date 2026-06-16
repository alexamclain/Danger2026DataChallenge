#!/usr/bin/env python3
"""Toy audit: period correlations are the same high-order character data.

A possible escape from explicit class-character traces is to compute moments of
the subgroup periods through global correlations:

    C(d) = sum_i j_i * j_{i+d}.

For periods

    y_r = sum_{h in H} j_{r+h},

the second power sum satisfies

    sum_r y_r^2 = sum_{d in H} C(d).

This is useful bookkeeping, but it has not removed the subgroup projector.
The cyclic autocorrelation of the period sequence diagonalizes to

    DFT(A)(s) = T_s * T_{-s},

where T_s are the same quotient-character traces.  If all spectral components
are nonzero, correlation/moment data still contains the full high-order phase.
"""

from __future__ import annotations

from cypari2 import Pari

from character_period_transform_toy import (
    Q,
    QUOTIENT_SIZE,
    dft,
    primitive_root_of_order,
)
from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)

SUBGROUP_SIZE = H // QUOTIENT_SIZE


def cyclic_autocorrelation(values: list[int], q: int) -> list[int]:
    n = len(values)
    return [
        sum(values[i] * values[(i + shift) % n] for i in range(n)) % q
        for shift in range(n)
    ]


def period_sums(cycle: list[int], q: int) -> list[int]:
    return [
        sum(cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)) % q
        for r in range(QUOTIENT_SIZE)
    ]


def bm_linear_complexity(sequence: list[int], q: int) -> int:
    c = [1]
    b = [1]
    linear_complexity = 0
    m = 1
    last_discrepancy = 1
    for idx, value in enumerate(sequence):
        discrepancy = value
        for j in range(1, linear_complexity + 1):
            discrepancy = (discrepancy + c[j] * sequence[idx - j]) % q
        if discrepancy == 0:
            m += 1
            continue
        old_c = c[:]
        scale = discrepancy * pow(last_discrepancy, -1, q) % q
        if len(c) < len(b) + m:
            c.extend([0] * (len(b) + m - len(c)))
        for j, coeff in enumerate(b):
            c[j + m] = (c[j + m] - scale * coeff) % q
        if 2 * linear_complexity <= idx:
            linear_complexity = idx + 1 - linear_complexity
            b = old_c
            last_discrepancy = discrepancy
            m = 1
        else:
            m += 1
    return linear_complexity


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    periods = period_sums(cycle, Q)
    full_corr = cyclic_autocorrelation(cycle, Q)
    period_corr = cyclic_autocorrelation(periods, Q)
    subgroup_offsets = [k * QUOTIENT_SIZE for k in range(SUBGROUP_SIZE)]
    projected_corr_sum = sum(full_corr[d] for d in subgroup_offsets) % Q
    period_square_sum = sum(y * y for y in periods) % Q

    zeta = primitive_root_of_order(Q, QUOTIENT_SIZE)
    traces = dft(periods, zeta, Q)
    corr_spectrum = dft(period_corr, zeta, Q)
    trace_products = [traces[s] * traces[(-s) % QUOTIENT_SIZE] % Q for s in range(QUOTIENT_SIZE)]

    print("period correlation idempotent toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"generator_ell={ELL}")
    print(f"class_number={H}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print()
    print(f"periods={periods}")
    print(f"subgroup_offsets={subgroup_offsets}")
    print(f"period_square_sum={period_square_sum}")
    print(f"projected_full_autocorrelation_sum={projected_corr_sum}")
    print(f"square_sum_equals_projected_autocorrelation={int(period_square_sum == projected_corr_sum)}")
    print()
    print(f"period_autocorrelation={period_corr}")
    print(f"period_autocorrelation_bm_complexity={bm_linear_complexity(period_corr * 2, Q)}")
    print(f"quotient_character_traces={traces}")
    print(f"autocorrelation_dft={corr_spectrum}")
    print(f"trace_product_spectrum={trace_products}")
    print(f"autocorrelation_spectrum_matches_trace_products={int(corr_spectrum == trace_products)}")
    print(f"nonzero_spectral_components={sum(1 for value in corr_spectrum if value)}")
    print()
    print("interpretation")
    print("  second_moment_is_a_subgroup_projection_of_global_autocorrelations=1")
    print("  autocorrelation_diagonalizes_to_products_of_the_same_character_traces=1")
    print("  full_spectrum_means_correlation_data_has_not_collapsed_the_high_order_phase=1")
    print(
        "conclusion=correlation_or_hecke_trace_bookkeeping_rephrases_the_"
        "relative_period_problem_unless_a_new_way_to_project_to_H_is_supplied"
    )


if __name__ == "__main__":
    main()
