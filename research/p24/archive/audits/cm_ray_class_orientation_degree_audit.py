#!/usr/bin/env python3
"""Degree audit for combining CM root selection with strict 2^40 orientation.

The ring-class CM route and the X1/ray-orientation route are individually
tempting.  This script records what happens when they are combined honestly.

For a target CM order with class number h, adjoining an x-coordinate of a
single oriented 2^k ray above a prime q|2 has degree

    h * phi(2^k) / 2 = h * 2^(k-2)

over the CM base in the x-only quotient (P and -P are identified).  This is
the class-field version of the verifier's missing orientation data.  The
condition pi == 1 mod q^k says that p splits completely in this ray class
field; it does not select one root above p.

Thus:

* ring-class j alone is smaller but unmarked: root torsor problem;
* j plus x/ray orientation is marked but has degree far above sqrt(p).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

P24 = 10**24 + 7
K = 40
SQRT_P = math.isqrt(P24)


@dataclass(frozen=True)
class Target:
    trace: int
    class_number: int
    group_shape: str


TARGETS = (
    Target(1020608380936, 278733727154, "cyclic 2*19*7335098083"),
    Target(-78903246840, 833035208344, "[208258802086,2,2]"),
    Target(-1178414874616, 205880396014, "cyclic 2*157*211*3107441"),
)


def main() -> None:
    orientation_cover = 1 << (K - 2)  # phi(2^K)/2 for x-only P ~ -P.
    print("p24 CM ray-class orientation degree audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"sqrt_floor_p={SQRT_P}")
    print(f"x_only_orientation_cover=2^(k-2)={orientation_cover}")
    print()
    print("target_trace class_number h_over_sqrt ray_degree ray_degree_over_sqrt class_group")
    for target in TARGETS:
        ray_degree = target.class_number * orientation_cover
        print(
            f"{target.trace:15d} {target.class_number:15d} "
            f"{target.class_number / SQRT_P:11.6f} "
            f"{ray_degree:26d} {ray_degree / SQRT_P:22.6e} "
            f"{target.group_shape}"
        )
    print()

    smooth_h = 205880396014
    quotient_degree = 66254
    recovery_degree = 3107441
    dream_marked_quotient_degree = quotient_degree * orientation_cover
    print("smooth_third_target_dream_quotient")
    print(f"  h={smooth_h}=66254*3107441")
    print(f"  unmarked_quotient_degree={quotient_degree}")
    print(f"  unmarked_recovery_degree={recovery_degree}")
    print(f"  marked_quotient_degree={dream_marked_quotient_degree}")
    print(f"  marked_quotient_degree_over_sqrt={dream_marked_quotient_degree / SQRT_P:.6e}")
    print()
    print("interpretation")
    print("  ring_class_j_degree_below_sqrt_for_fixed_p24_rows=1")
    print("  ring_class_j_selects_root_over_completely_split_p=0")
    print("  torsion_or_ray_invariant_marks_x_orientation=1")
    print("  torsion_or_ray_degree_far_above_sqrt=1")
    print(
        "conclusion=combining_CM_with_the_strict_2^40_ray_restores_the_"
        "orientation_cover_and_does_not_beat_sqrt"
    )


if __name__ == "__main__":
    main()
