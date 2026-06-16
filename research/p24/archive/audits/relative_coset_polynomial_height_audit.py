#!/usr/bin/env python3
"""Height audit for the principal H-coset recovery-polynomial route.

The third p24 target has a formally attractive subgroup

    |H| = 3107441

for the oriented class 2 * 463 * 223^(-1).  A tempting positive route is to
skip the quotient selector and compute only the principal coset polynomial

    R_H(X) = product_{a in H} (X - j(a)).

Its degree is far below sqrt(p), and any root of R_H mod p would be a target
CM j-invariant.  There are two catches:

* phase: R_H is a relative polynomial whose coefficients live in the quotient
  field, not in Q; reducing it mod p requires choosing the embedded quotient
  root/prime above p;
* height: the principal conjugate is one of the roots and has log-size about
  pi*sqrt(|Delta|), so ordinary complex/CRT computation is height-scale.

This audit records the height scale.  The phase obstruction is illustrated in
`p24/relative_coset_phase_toy.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

P24 = 10**24 + 7
SQRT_P = math.isqrt(P24)
LOG_P = math.log(P24)


@dataclass(frozen=True)
class Target:
    label: str
    abs_trace: int
    subgroup_size: int
    quotient_size: int
    class_invariant_height_factor: float


TARGETS = (
    Target("first_trace_order19_principal_H", 1020608380936, 14670196166, 19, 1.0),
    Target("third_trace_composite_principal_H", 1178414874616, 3107441, 66254, 1.0),
    Target("third_trace_composite_height_1_over_28", 1178414874616, 3107441, 66254, 1 / 28),
)


def main() -> None:
    print("p24 relative coset polynomial height audit")
    print(f"p={P24}")
    print(f"sqrt_floor={SQRT_P}")
    print(f"log_p={LOG_P:.6f}")
    print()
    print(
        "label degree quotient degree_over_sqrt raw_log_principal "
        "scaled_log_principal scaled_over_log_p min_crt_bits_proxy"
    )
    for target in TARGETS:
        delta = target.abs_trace * target.abs_trace - 4 * P24
        raw_log = math.pi * math.sqrt(abs(delta))
        scaled = raw_log * target.class_invariant_height_factor
        print(
            f"{target.label:42s} {target.subgroup_size:12d} "
            f"{target.quotient_size:9d} {target.subgroup_size / SQRT_P:16.6e} "
            f"{raw_log:22.6f} {scaled:22.6f} "
            f"{scaled / LOG_P:18.6e} {scaled / math.log(2):22.6e}"
        )
    print()
    print("interpretation")
    print("  principal_H_coset_degree_can_be_subsqrt=1")
    print("  any_root_mod_p_would_be_a_target_CM_j=1")
    print("  coefficients_live_in_the_quotient_field_not_Q=1")
    print("  reducing_one_coset_requires_an_embedded_quotient_phase=1")
    print("  ordinary_complex_CM_needs_precision_comparable_to_coefficient_height=1")
    print("  CRT_mod_p_without_direct_mod_p_evaluation_needs_height_bound=1")
    print("  coefficient_height_proxy_is_astronomically_larger_than_log_p=1")
    print("  constant_factor_class_invariants_do_not_change_the_exponent_enough=1")
    print(
        "conclusion=relative_coset_polynomial_degree_is_attractive_but_"
        "ordinary_height_based_computation_does_not_give_a_subsqrt_selector"
    )


if __name__ == "__main__":
    main()
