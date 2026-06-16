#!/usr/bin/env python3
"""Constant-factor class-invariant heights do not prove lifting.

Some CM class invariants have class polynomials much smaller than the Hilbert
class polynomial for j.  This is crucial in ordinary CM implementations, but
for the p24 lifting problem a constant height factor is not enough.

Even using a very optimistic 1/28 height factor, mentioned in the Enge-style
class-invariant literature for certain eta-quotient invariants, the dominant
archimedean log-size is still about 1e11, while log(p) is about 55.  Therefore
the naive "p^h divides the norm and every conjugate is <p" lifting proof still
cannot work for ordinary class-invariant formulas.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

P24 = 10**24 + 7
HEIGHT_FACTORS = (1.0, 1 / 28, 1 / 1000)


@dataclass(frozen=True)
class Target:
    label: str
    abs_trace: int


TARGETS = (
    Target("first_trace_order19_toy", 1020608380936),
    Target("middle_trace_genus_control", 78903246840),
    Target("third_trace_composite_target", 1178414874616),
)


def main() -> None:
    log_p = math.log(P24)
    print("p24 class-invariant lifting height audit")
    print(f"p={P24}")
    print(f"log_p={log_p:.6f}")
    print("height_factors=" + ",".join(f"{factor:.8g}" for factor in HEIGHT_FACTORS))
    print()
    print("label raw_log_j factor scaled_log scaled_over_log_p below_p")
    for target in TARGETS:
        delta = target.abs_trace * target.abs_trace - 4 * P24
        raw = math.pi * math.sqrt(abs(delta))
        for factor in HEIGHT_FACTORS:
            scaled = factor * raw
            print(
                f"{target.label:32s} {raw:22.6f} {factor:10.8f} "
                f"{scaled:18.6f} {scaled / log_p:18.6e} {int(scaled < log_p):7d}"
            )
    print()
    print("interpretation")
    print("  constant_factor_height_reductions_help_CM_coefficient_size=1")
    print("  constant_factor_height_reductions_do_not_make_conjugates_smaller_than_p=1")
    print("  naive_norm_lifting_still_fails_for_known_class_invariant_scale=1")
    print("conclusion=smaller_class_invariants_are_not_a_faithfulness_lifting_theorem")


if __name__ == "__main__":
    main()
