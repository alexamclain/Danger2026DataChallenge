#!/usr/bin/env python3
"""Toy showing genus traces are only a low-frequency projection.

In the D=-5000 period-transform toy, quotient size is 10.  Full recovery of
the ten subgroup periods needs all ten quotient-character twisted traces.
If only the trivial character and the order-2/genus-like character are known,
Fourier inversion recovers only the average of the five even periods and the
average of the five odd periods.

This models the p24 third target, whose genus quotient has size 2 while the
useful split-cycle quotients have size 314 or 422.
"""

from __future__ import annotations

from character_period_transform_toy import Q, QUOTIENT_SIZE, dft, inverse_dft, primitive_root_of_order

# Copied from the verified D=-5000 / F_3851 transform toy output.  Keeping the
# list explicit avoids recomputing modular polynomials just to demonstrate the
# projection.
PERIOD_SUMS = [2984, 3011, 70, 1051, 221, 2203, 3026, 440, 3847, 1358]


def main() -> None:
    zeta = primitive_root_of_order(Q, QUOTIENT_SIZE)
    traces = dft(PERIOD_SUMS, zeta, Q)
    full = inverse_dft(traces, zeta, Q)

    # Keep only s=0 and s=m/2, the trivial and quadratic quotient characters.
    sparse_traces = [0] * QUOTIENT_SIZE
    sparse_traces[0] = traces[0]
    sparse_traces[QUOTIENT_SIZE // 2] = traces[QUOTIENT_SIZE // 2]
    projection = inverse_dft(sparse_traces, zeta, Q)

    even_average = sum(PERIOD_SUMS[0::2]) * pow(5, -1, Q) % Q
    odd_average = sum(PERIOD_SUMS[1::2]) * pow(5, -1, Q) % Q

    print("genus projection period toy")
    print(f"q={Q}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"period_sums={PERIOD_SUMS}")
    print(f"full_inverse_dft={full}")
    print(f"trivial_plus_quadratic_projection={projection}")
    print(f"even_period_average={even_average}")
    print(f"odd_period_average={odd_average}")
    print(f"projection_distinct_values={sorted(set(projection))}")
    print()
    print("p24_analogue")
    print("  ell_677_quotient_size=314 genus_projection_bucket_size=157")
    print("  ell_7349_quotient_size=422 genus_projection_bucket_size=211")
    print()
    print("interpretation")
    print("  genus_traces_recover_only_parity_averages=1")
    print("  high_order_characters_are_needed_for_individual_periods=1")
    print(
        "conclusion=known_genus_twisted_traces_are_information_theoretically_"
        "insufficient_for_the_p24_split_cycle_selector"
    )


if __name__ == "__main__":
    main()
