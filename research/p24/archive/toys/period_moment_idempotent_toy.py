#!/usr/bin/env python3
"""Toy audit: period moments still contain the high-order idempotent.

The split-cycle selector might try to avoid individual twisted traces by
computing the quotient polynomial

    V(Y) = prod_r (Y - y_r)

directly from its power sums P_d=sum_r y_r^d.  This script checks the exact
Fourier identity in the D=-5000 quotient-size-10 toy:

    P_d = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}.

Thus direct moments are not automatically a new primitive; they are the same
subgroup idempotent after convolution.  If the available trace formulas only
see the trivial and quadratic/genus characters, the "moment polynomial" is the
coarser polynomial with repeated parity averages, not the true period
polynomial.
"""

from __future__ import annotations

from character_period_transform_toy import Q, QUOTIENT_SIZE, dft, monic_poly_from_roots, primitive_root_of_order

PERIOD_SUMS = [2984, 3011, 70, 1051, 221, 2203, 3026, 440, 3847, 1358]


def power_sums(values: list[int], q: int) -> list[int]:
    return [sum(pow(value, d, q) for value in values) % q for d in range(1, len(values) + 1)]


def convolution_power_sum(traces: list[int], d: int, q: int) -> int:
    """Compute m^(1-d) sum_{s_1+...+s_d=0} prod T_s by cyclic convolution."""
    m = len(traces)
    coeffs = [1] + [0] * (m - 1)
    for _ in range(d):
        nxt = [0] * m
        for a, ca in enumerate(coeffs):
            if ca == 0:
                continue
            for b, tb in enumerate(traces):
                nxt[(a + b) % m] = (nxt[(a + b) % m] + ca * tb) % q
        coeffs = nxt
    return coeffs[0] * pow(m, 1 - d, q) % q


def newton_from_power_sums(powers: list[int], q: int) -> list[int]:
    """Return ascending coefficients of monic polynomial from power sums."""
    m = len(powers)
    elementary = [1]
    for k in range(1, m + 1):
        total = 0
        for i in range(1, k + 1):
            total = (total + (-1) ** (i - 1) * elementary[k - i] * powers[i - 1]) % q
        elementary.append(total * pow(k, -1, q) % q)
    coeffs = [0] * (m + 1)
    for k in range(m + 1):
        coeffs[m - k] = ((-1) ** k * elementary[k]) % q
    return coeffs


def main() -> None:
    zeta = primitive_root_of_order(Q, QUOTIENT_SIZE)
    traces = dft(PERIOD_SUMS, zeta, Q)
    powers = power_sums(PERIOD_SUMS, Q)
    convolution_powers = [convolution_power_sum(traces, d, Q) for d in range(1, QUOTIENT_SIZE + 1)]
    true_poly = monic_poly_from_roots(PERIOD_SUMS, Q)
    reconstructed_poly = newton_from_power_sums(powers, Q)

    even_average = sum(PERIOD_SUMS[0::2]) * pow(5, -1, Q) % Q
    odd_average = sum(PERIOD_SUMS[1::2]) * pow(5, -1, Q) % Q
    genus_periods = [even_average, odd_average] * (QUOTIENT_SIZE // 2)
    genus_poly = monic_poly_from_roots(genus_periods, Q)
    genus_powers = power_sums(genus_periods, Q)

    print("period moment idempotent toy")
    print(f"q={Q}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"period_sums={PERIOD_SUMS}")
    print(f"twisted_traces={traces}")
    print()
    print(f"power_sums={powers}")
    print(f"convolution_formula_power_sums={convolution_powers}")
    print(f"convolution_formula_matches={int(powers == convolution_powers)}")
    print(f"newton_reconstructs_true_period_polynomial={int(reconstructed_poly == true_poly)}")
    print(f"true_period_polynomial_coeffs_ascending_mod_q={true_poly}")
    print()
    print("genus_only_projection")
    print(f"  even_average={even_average}")
    print(f"  odd_average={odd_average}")
    print(f"  genus_projected_periods={genus_periods}")
    print(f"  genus_power_sums={genus_powers}")
    print(f"  genus_projected_polynomial_coeffs_ascending_mod_q={genus_poly}")
    print(f"  genus_polynomial_equals_true={int(genus_poly == true_poly)}")
    print()
    print("interpretation")
    print("  quotient_power_sums_are_high_order_character_convolutions=1")
    print("  direct_moment_route_still_needs_the_subgroup_indicator=1")
    print("  genus_only_moments_reconstruct_a_coarser_repeated_average_polynomial=1")
    print(
        "conclusion=period_moments_do_not_remove_the_need_for_order_"
        "157_or_211_information_in_the_p24_split_cycle_quotients"
    )


if __name__ == "__main__":
    main()
