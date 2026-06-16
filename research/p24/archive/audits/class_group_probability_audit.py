#!/usr/bin/env python3
"""Probability algorithms on the p24 target class groups.

The smooth third target makes generic group algorithms look tempting:

    h = 205880396014,  sqrt(h) ~= 4.5e5 << sqrt(p).

This script separates what random walks/birthday/Pollard methods can do from
what the DANGER certificate needs.  These algorithms can navigate or solve
hidden-shift/discrete-log problems once an embedded CM root set or class-action
oracle is available.  They do not create the first embedded root/oracle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)


@dataclass(frozen=True)
class Target:
    trace: int
    D_K: int
    h: int
    class_group: tuple[int, ...]


TARGETS = (
    Target(1020608380936, -739589633190799177940983, 278733727154, (278733727154,)),
    Target(-78903246840, -998443569409526507503607, 833035208344, (208258802086, 2, 2)),
    Target(-1178414874616, -652834595820939249713143, 205880396014, (205880396014,)),
)


def main() -> None:
    print("p24 class-group probability audit")
    print(f"p={P24}")
    print(f"sqrt_floor_p={SQRT_P}")
    print()
    print(
        "trace h h/sqrt_p sqrt_h sqrt_h/sqrt_p random_j_expected "
        "pollard_requires_embedded_oracle"
    )
    for target in TARGETS:
        sqrt_h = math.sqrt(target.h)
        random_j_expected = P24 / target.h
        print(
            f"{target.trace:15d} {target.h:12d} {target.h / SQRT_P:10.6f} "
            f"{sqrt_h:12.3f} {sqrt_h / SQRT_P:14.6e} "
            f"{random_j_expected:17.6e} yes"
        )
        print(f"  D_K={target.D_K}")
        print(f"  class_group={list(target.class_group)}")

    third = TARGETS[2]
    best_quotient = 66254
    best_recovery = 3107441
    print()
    print("third_target_conditional_costs")
    print(f"  h={third.h}")
    print(f"  sqrt_h={math.sqrt(third.h):.3f}")
    print(f"  best_decomposed_degrees={best_quotient}*{best_recovery}")
    print(f"  best_recovery_over_sqrt_h={best_recovery / math.sqrt(third.h):.6f}")
    print(f"  best_recovery_over_sqrt_p={best_recovery / SQRT_P:.6e}")
    print()
    print("oracle_separation")
    print("  seeded_embedded_root_available -> already have a CM j root; certificate tail is cheap")
    print("  embedded_class_action_oracle_available -> Pollard/hidden-shift costs about sqrt(h)")
    print("  abstract_class_group_only -> samples labels, not Fp j-values")
    print("  split_H_D_polynomial_available -> output/input size already degree h")
    print("  no_seed_no_embedded_invariant -> random walk has no Fp state space to walk")
    print()
    print("small_toy_analogy")
    print("  In the D=-5000,h=30 calibration all roots are Frobenius-fixed over q=1259.")
    print("  Any root can be called principal after rotating the abstract class label.")
    print("  Randomizing the abstract label does not identify an embedded root without an anchor.")
    print()
    print(
        "conclusion=class_group_probability_methods_are_subsqrt_only_after_the_"
        "missing_embedded_root_or_class_action_oracle_is_supplied"
    )


if __name__ == "__main__":
    main()
