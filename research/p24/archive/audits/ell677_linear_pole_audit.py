#!/usr/bin/env python3
"""Cusp-pole audit for linear endpoint functions on X0(ell).

The Atkin-Lehner zero-window scan used the optimistic proxy

    ceil([SL2:Gamma0(ell)] / 2) = (ell+1)/2

for prime ell.  That is a quotient-degree lower proxy, not the pole degree of
the linear endpoint functions whose character traces are forced to vanish by
relative-content collapse.

For X0(ell), write

    x = j(tau),       y = j(ell*tau).

At the two cusps, the pole orders are:

    cusp infinity:  x has order 1,   y has order ell
    cusp 0:         x has order ell, y has order 1

Thus any nonzero linear endpoint function has pole degree at least ell+1 on
X0(ell), except the symmetric combination x+y descends to X0(ell)^+ with pole
degree ell after the two cusps are identified.  Both are far above the p24
index 314 for ell=677.
"""

from __future__ import annotations

import argparse


def audit_prime_ell(ell: int, index: int) -> None:
    gamma0_degree = ell + 1
    atkin_proxy = (ell + 1) // 2
    endpoint_linear_degree = ell + 1
    symmetric_descended_degree = ell

    print("prime X0(ell) linear endpoint pole audit")
    print(f"ell={ell}")
    print(f"target_index={index}")
    print()
    print("cusp_pole_orders_on_X0_ell")
    print("  function cusp_infinity cusp_0 total_pole_degree_if_single_endpoint")
    print(f"  x=j(tau)       1 {ell:5d} {endpoint_linear_degree:5d}")
    print(f"  y=j(ell*tau) {ell:5d}     1 {endpoint_linear_degree:5d}")
    print()
    print("linear_combinations")
    print(f"  generic_a_x_plus_b_y_degree_on_X0={2 * ell}")
    print(f"  single_endpoint_degree_on_X0={endpoint_linear_degree}")
    print(f"  symmetric_x_plus_y_degree_on_X0_plus={symmetric_descended_degree}")
    print()
    print("zero_window_comparison")
    print(f"  optimistic_atkin_proxy=(ell+1)/2={atkin_proxy}")
    print(f"  optimistic_proxy_over_index={atkin_proxy / index:.6f}")
    print(f"  best_forced_linear_degree={symmetric_descended_degree}")
    print(f"  best_forced_linear_degree_over_index={symmetric_descended_degree / index:.6f}")
    print(f"  single_endpoint_degree_over_index={endpoint_linear_degree / index:.6f}")
    print()
    print("interpretation")
    print("  relative_content_collapse_forces_linear_endpoint_character_traces=1")
    print("  arbitrary_low_degree_functions_on_X0_plus_are_not_forced_to_vanish=1")
    print("  atkin_proxy_339_is_not_a_usable_linear_pole_degree=1" if ell == 677 else "  atkin_proxy_is_not_a_usable_linear_pole_degree=1")
    print("  ell677_zero_lemma_window_closed_for_linear_content=1" if ell == 677 else "  zero_lemma_window_closed_if_best_linear_degree_ge_index=1")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ell", type=int, default=677)
    parser.add_argument("--index", type=int, default=314)
    args = parser.parse_args()
    audit_prime_ell(args.ell, args.index)


if __name__ == "__main__":
    main()
