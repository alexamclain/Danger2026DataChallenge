#!/usr/bin/env python3
"""Height audit for the easy finite-field-to-characteristic-zero lift.

The remaining no-go theorem would like a faithfulness/lifting lemma: a
bounded finite-field identity in local modular data that selects the p24
periods should lift to characteristic zero, where the group-algebra support
lemma applies.

The most naive proof would use norms.  If an algebraic integer residual R is
zero at every prime above p, then p^h divides Norm(R).  If every complex
conjugate of R had absolute value < p, this would force R=0.

For singular moduli this route fails immediately.  The dominant conjugate has
log-size about pi*sqrt(|Delta|), while log(p) is only about 55.  Even a linear
residual in j has archimedean size enormously larger than p, so p-divisibility
of its norm does not imply characteristic-zero vanishing.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

P24 = 10**24 + 7


@dataclass(frozen=True)
class Target:
    label: str
    abs_trace: int
    class_number: int


TARGETS = (
    Target("first_trace_order19_toy", 1020608380936, 278733727154),
    Target("middle_trace_genus_control", 78903246840, 833035208344),
    Target("third_trace_composite_target", 1178414874616, 205880396014),
)


def main() -> None:
    log_p = math.log(P24)
    print("p24 finite-field lifting height audit")
    print(f"p={P24}")
    print(f"log_p={log_p:.6f}")
    print()
    print("label class_number log_dominant_j log_j_over_log_p log_norm_bound_minus_hlogp")
    for target in TARGETS:
        delta = target.abs_trace * target.abs_trace - 4 * P24
        log_j = math.pi * math.sqrt(abs(delta))
        # If every conjugate had the dominant size, this is the rough log of a
        # degree-h norm bound for a linear expression in j.  The sign tells us
        # whether p^h divisibility could force zero by this crude method.
        log_norm_minus_hlogp = target.class_number * (log_j - log_p)
        print(
            f"{target.label:32s} {target.class_number:15d} "
            f"{log_j:22.6f} {log_j / log_p:18.6e} "
            f"{log_norm_minus_hlogp:28.6e}"
        )
    print()
    print("interpretation")
    print("  p_splits_completely_so_mod_p_identity_can_hold_at_many_CM_primes=1")
    print("  archimedean_singular_moduli_are_exponentially_larger_than_p=1")
    print("  norm_divisibility_by_p^h_does_not_force_zero_for_j_formulas=1")
    print("  easy_height_based_lifting_lemma_fails_for_p24=1")
    print(
        "conclusion=remaining_faithfulness_lifting_gap_needs_more_than_"
        "a_crude_norm_height_bound"
    )


if __name__ == "__main__":
    main()
