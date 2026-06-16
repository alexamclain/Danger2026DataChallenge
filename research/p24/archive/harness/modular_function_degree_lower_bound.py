#!/usr/bin/env python3
"""Degree lower bound for single modular-function H-invariants.

Suppose a modular function f on a modular curve X_Gamma is used as a local CM
class invariant: for each CM j-root one chooses a point P above it and records
f(P).  If f has degree d as a map to P^1, then any value of f has at most d
preimages on X_Gamma, hence can contain at most d distinct j-values.

Therefore a single modular-function value that is constant on an H-coset of
size n must have degree at least n.  This rules out constant-level class
invariants as the p24 selector.  It does not rule out a growing-level object
with degree comparable to the recovery degree; it says such an object has
already paid the projector-sized degree.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)


@dataclass(frozen=True)
class Target:
    label: str
    quotient: int
    recovery: int
    current_correspondence_proxy: int


TARGETS = (
    Target("first_trace_order19", 19, 14670196166, 20),
    Target("first_trace_ell107", 38, 7335098083, 108),
    Target("third_trace_ell677", 314, 655670051, 678),
    Target("third_trace_composite_2_463_223inv", 66254, 3107441, 311808),
)


def main() -> None:
    print("p24 modular-function degree lower bound")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print()
    print(
        "label quotient recovery min_degree_for_single_value "
        "min_degree_over_sqrt correspondence_proxy proxy_vs_min_degree"
    )
    for target in TARGETS:
        min_degree = target.recovery
        print(
            f"{target.label:38s} {target.quotient:9d} {target.recovery:12d} "
            f"{min_degree:27d} {min_degree / SQRT_P:20.6e} "
            f"{target.current_correspondence_proxy:20d} "
            f"{target.current_correspondence_proxy / min_degree:19.6e}"
        )
    print()
    print("interpretation")
    print("  fixed_level_modular_functions_have_bounded_degree=1")
    print("  bounded_degree_values_can_merge_only_bounded_many_j_roots=1")
    print("  H_coset_selector_value_requires_degree_at_least_recovery_size=1")
    print("  third_composite_degree_lower_bound_is_subsqrt_but_not_constructive=1")
    print("  current_low_degree_correspondence_proxy_is_not_an_H_invariant_value=1")
    print(
        "conclusion=constant_level_class_invariants_cannot_select_the_p24_"
        "H_period;_a_positive_route_needs_a_growing_degree_or_period_trace"
    )


if __name__ == "__main__":
    main()
