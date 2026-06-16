#!/usr/bin/env python3
"""Cost model for smooth-class torsor navigation versus first-root discovery.

The third p24 trace has an unusually smooth cyclic class group.  This is very
useful after one target CM root or one embedded quotient period is known: the
class action can be organized into small factors, and the best decomposed-CM
root degrees are tiny compared with sqrt(p).

This script separates that real benefit from two non-benefits:

* random fixed-trace discovery still has density Theta(1/sqrt(p));
* smooth class-group navigation does not create the first seed root or the
  embedded quotient equations.
"""

from __future__ import annotations

import math

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)

STRICT_ROWS = (
    ("first", 1020608380936, 278733727154, (2, 19, 7335098083)),
    ("middle", -78903246840, 833035208344, (8, 104129401043)),
    ("third", -1178414874616, 205880396014, (2, 157, 211, 3107441)),
)

THIRD_QUOTIENT = 2 * 157 * 211
THIRD_RECOVERY = 3107441


def main() -> None:
    total_h = sum(row[2] for row in STRICT_ROWS)
    doubled_total_h = 2 * total_h  # maximal + conductor-2 order upper proxy.
    bounded_montgomery_degree = 6

    print("p24 smooth torsor search tradeoff audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print()

    print("strict_trace_class_sizes")
    print("  label trace h h_over_sqrt factors random_j_trials_over_sqrt")
    for label, trace, h, factors in STRICT_ROWS:
        expected = P24 / h
        print(
            f"  {label:6s} {trace:15d} {h:12d} {h / SQRT_P:11.6f} "
            f"{factors!s:34s} {expected / SQRT_P:24.6f}"
        )
    print()

    print("aggregate_random_discovery_model")
    print(f"  sum_h_one_order_per_trace={total_h}")
    print(f"  sum_h_over_sqrt={total_h / SQRT_P:.6f}")
    print(f"  random_j_expected_trials_over_sqrt_using_sum_h={P24 / total_h / SQRT_P:.6f}")
    print(f"  two_order_upper_proxy_roots={doubled_total_h}")
    print(f"  two_order_proxy_expected_trials_over_sqrt={P24 / doubled_total_h / SQRT_P:.6f}")
    print(
        "  generous_montgomery_A_degree_bound_expected_trials_over_sqrt="
        f"{P24 / (bounded_montgomery_degree * doubled_total_h) / SQRT_P:.6f}"
    )
    print("  interpretation=bounded_degree_maps_and_extra_orders_change_constants_not_exponent")
    print()

    print("third_trace_smooth_structure")
    print(f"  h={STRICT_ROWS[2][2]}")
    print(f"  class_factors={STRICT_ROWS[2][3]}")
    print(f"  best_embedded_quotient_degree={THIRD_QUOTIENT}")
    print(f"  best_embedded_recovery_degree={THIRD_RECOVERY}")
    print(f"  quotient_plus_recovery={THIRD_QUOTIENT + THIRD_RECOVERY}")
    print(f"  recovery_over_sqrt={THIRD_RECOVERY / SQRT_P:.6e}")
    print()

    print("what_smoothness_buys")
    print("  after_seed_class_navigation=cheap")
    print("  after_embedded_quotient_root_recovery_degree=subsqrt")
    print("  quotient_tower_degrees=2,157,211,3107441")
    print("  pohlig_hellman_style_indexing_after_two_known_vertices=polylog_or_small")
    print()

    print("what_smoothness_does_not_buy")
    print("  first_target_trace_root_density=Theta(1/sqrt_p)")
    print("  random_trace_or_SEA_recognition_exponent=1/2")
    print("  class_action_walk_requires_seed_vertex=1")
    print("  decomposed_CM_equations_must_be_embedded_not_abstract=1")
    print("  known_embedded_equation_construction_uses_class_orbits_or_CRT_height=1")
    print()

    print(
        "conclusion=smooth_class_group_makes_the_third_trace_the_best_formal_"
        "route_but_does_not_by_itself_beat_sqrt_scaling_without_an_embedded_"
        "quotient_period_or_seed_selector"
    )


if __name__ == "__main__":
    main()
