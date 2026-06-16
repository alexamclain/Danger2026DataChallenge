#!/usr/bin/env python3
"""Static accounting for intermediate subfields of the p24 tensor factor.

The current one-factor target works in a finite field B/E of degree 5549.
Since 5549 = 31 * 179, B has exactly two nontrivial intermediate fields over E.
This script records the dimension constraints those subfields impose on any
attempt to split the one-factor Moore determinant.
"""

from __future__ import annotations

import math

P = 10**24 + 7
M = 66254
N = 3107441
ORD_N = 388430
ORD_M = 5460
COMPONENTS = (2, 157, 211)


def divisors(value: int) -> list[int]:
    out: list[int] = []
    for candidate in range(1, math.isqrt(value) + 1):
        if value % candidate:
            continue
        out.append(candidate)
        if candidate * candidate != value:
            out.append(value // candidate)
    return sorted(out)


def main() -> None:
    tensor_factor_count = math.gcd(ORD_N, ORD_M)
    factor_degree = ORD_N // tensor_factor_count
    factorization = " * ".join(
        f"{prime}^{exp}" if exp > 1 else str(prime)
        for prime, exp in [(31, 1), (179, 1)]
    )
    axis_counts = {
        "constant": 1,
        "2": 1,
        "157": 156,
        "211": 210,
    }
    proper_subdegrees = [
        degree for degree in divisors(factor_degree)
        if degree not in (1, factor_degree)
    ]
    total_proper_trace_capacity = sum(proper_subdegrees)
    degree_179 = 179
    axis_dim = sum(axis_counts.values())
    twists_for_axis_to_179 = math.ceil(axis_dim / degree_179)
    twists_for_211_to_179 = math.ceil(axis_counts["211"] / degree_179)

    print("p24 tensor factor intermediate-field accounting")
    print(f"p={P}")
    print(f"m={M}")
    print(f"n={N}")
    print(f"components={COMPONENTS}")
    print(f"ord_n(p)={ORD_N}")
    print(f"ord_m(p)={ORD_M}")
    print(f"tensor_factor_count_over_E={tensor_factor_count}")
    print(f"tensor_factor_degree_over_E={factor_degree}")
    print(f"tensor_factor_degree_factorization={factorization}")
    print()
    print("intermediate_subfields_over_E")
    print("  subdegree=1 name=E")
    for degree in proper_subdegrees:
        print(f"  subdegree={degree} relative_index={factor_degree // degree}")
    print(f"  subdegree={factor_degree} name=B")
    print()
    print("axis_block_dimensions")
    for name, count in axis_counts.items():
        print(f"  {name}: {count}")
    print(f"  axis_total={sum(axis_counts.values())}")
    print()
    print("dimension_observations")
    print("  block_157_plus_constant_plus_2_dim=158")
    print("  block_157_plus_constant_plus_2_fits_in_subdegree_179=1")
    print("  block_211_dim=210")
    print("  block_211_equals_31_plus_179=1")
    print(f"  all_proper_subfield_trace_capacity={total_proper_trace_capacity}")
    print("  full_axis_dim_exceeds_all_proper_subfield_trace_capacity=1")
    print()
    print("candidate_split")
    print("  prove internal normality for constant+2+157 by trace_to_degree_179")
    print("  prove internal normality for 211 by joint traces_to_degrees_31_and_179")
    print("  still need cross-block directness in the full degree-5549 factor")
    print()
    print("twisted_trace_frame_capacity")
    print(f"  degree_179_subfield_capacity={degree_179}")
    print(f"  twists_needed_for_211_block={twists_for_211_to_179}")
    print(f"  twists_needed_for_full_axis={twists_for_axis_to_179}")
    print(f"  full_axis_twisted_trace_capacity={twists_for_axis_to_179 * degree_179}")
    print("  relative_degree_B_over_degree_179_subfield=31")
    print("  proposed_full_axis_frame=T_3_to_degree_179")
    print("conclusion=reported_tensor_factor_intermediate_accounting")


if __name__ == "__main__":
    main()
