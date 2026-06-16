#!/usr/bin/env python3
"""Barrier for low-degree trace-shift correspondences from cheap p24 seeds.

The broad fast p24 certificates give tempting seed objects:

* a Pocklington certificate from p-1;
* the near-square D=-7 CM curve with trace +/-2*10^12.

Could a low-degree algebraic correspondence, twist, or small modular move turn
one of these cheap objects into a strict DANGER3 curve?  This script records
the arithmetic obstruction:

* F_p-isogenies preserve trace, so they cannot move the D=-7 trace to the
  strict target traces.
* for j != 0,1728, quadratic twisting only changes trace sign;
* exceptional j=0,1728 and all class-number-one CM cases have already been
  audited and miss the strict trace;
* a bounded-degree non-isogenous recipe is just a bounded-degree family over
  the j-line, which changes only constants in the target trace entropy.
"""

from __future__ import annotations

import math

from low_degree_family_entropy_audit import P24, expected_trials, target_class_estimates


N = 10**12
K = 40
M = 1 << K
NEAR_SQUARE_TRACE = 2 * N
TARGET_SIGNED_TRACES = (
    -1178414874616,
    -1020608380936,
    -78903246840,
    78903246840,
    1020608380936,
    1178414874616,
)


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def main() -> None:
    rows = target_class_estimates()
    total_h = sum(row[3] for row in rows)
    sqrt_p = math.sqrt(P24)

    print("p24 low-degree correspondence / trace-shift barrier")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"sqrt_p={sqrt_p:.6e}")
    print()

    print("near_square_D_minus_7_seed")
    for trace in (NEAR_SQUARE_TRACE, -NEAR_SQUARE_TRACE):
        order = P24 + 1 - trace
        twist_order = P24 + 1 + trace
        nearest = min(TARGET_SIGNED_TRACES, key=lambda t: abs(t - trace))
        print(
            f"  trace={trace} trace_mod_2^40={trace % M} "
            f"v2_order={v2(order)} v2_twist={v2(twist_order)} "
            f"nearest_strict_trace={nearest} distance={abs(trace-nearest)}"
        )
    print("  j=-3375 not_exceptional=True")
    print("  isogeny_trace_shift_possible=False")
    print("  quadratic_twist_traces_only=+/-2n")
    print()

    print("strict_target_class_entropy")
    print(f"  total_signed_j_classes_est={total_h:.6e}")
    print(f"  random_j_expected_trials={expected_trials(total_h, 1.0):.6e}")
    print("  bounded_degree_correspondence_model")
    print("  degree expected_trials expected_trials/sqrt_p")
    for degree in (2, 3, 4, 6, 8, 12, 16, 32, 64, 256, 4096, 65536, 1_000_000):
        trials = expected_trials(total_h, float(degree))
        print(f"  {degree:8d} {trials:18.6e} {trials / sqrt_p:22.6e}")
    print()

    print("degree_required_for_exponent_saving")
    print("  target_exponent required_degree")
    for alpha in (0.40, 0.35, 0.30, 0.25):
        target = P24 ** alpha
        degree = P24 / (total_h * target)
        print(f"  p^{alpha:.2f} {degree:.6e}")
    print()
    print(
        "conclusion=low_degree_correspondences_from_the_fast_seed_curves_only_change_constants; "
        "trace_shift_requires_either_a_growing_level_or_a_new_class_selector"
    )


if __name__ == "__main__":
    main()
