#!/usr/bin/env python3
"""Toy gate for relative trace period normality.

In the p24 decimated trace frame, B/E has degree 5549=31*179 and C/E is the
fixed field of the order-31 subgroup.  If theta is normal in B/E, then

    eta = Tr_{B/C}(theta)

has conjugates that form a normal basis of C/E.  This is a formal Galois
coset-sum fact: a quotient relation among the eta conjugates would lift to a
coset-constant relation among the theta conjugates.

The toy verifies the positive implication and keeps a nonnormal control so we
do not accidentally treat relative trace normality as automatic.
"""

from __future__ import annotations

from dataclasses import dataclass

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q


P24_P = 10**24 + 7
P24_M = 66254
P24_N = 3107441
P24_E_DEGREE_OVER_FP = 5460
P24_B_OVER_E = 5549
P24_C_OVER_E = 179
P24_B_OVER_C = 31


@dataclass(frozen=True)
class Case:
    label: str
    q: int
    ell: int
    subgroup_order: int
    quotient_degree: int


def conjugate_rank(
    field: ExtensionField,
    value: tuple[int, ...],
    q: int,
    count: int,
) -> int:
    return rank_mod_q([list(field.pow(value, q**i)) for i in range(count)], q)


def relative_trace(
    field: ExtensionField,
    theta: tuple[int, ...],
    q: int,
    subgroup_order: int,
    quotient_degree: int,
) -> tuple[int, ...]:
    total = field.zero
    for j in range(subgroup_order):
        total = field.add(total, field.pow(theta, q ** (quotient_degree * j)))
    return total


def run_case(case: Case) -> tuple[int, int, tuple[int, ...]]:
    degree = case.subgroup_order * case.quotient_degree
    field = ExtensionField(
        case.q,
        degree,
        find_irreducible_modulus(case.q, degree, 20260606),
    )
    theta = primitive_root_of_order(field, case.ell, 20260606)
    eta = relative_trace(
        field,
        theta,
        case.q,
        case.subgroup_order,
        case.quotient_degree,
    )
    theta_rank = conjugate_rank(field, theta, case.q, degree)
    eta_rank = conjugate_rank(field, eta, case.q, case.quotient_degree)
    return theta_rank, eta_rank, eta


def main() -> None:
    cases = [
        Case("normal_degree6_order2_trace", 3, 7, 2, 3),
        Case("normal_degree12_order2_trace", 2, 13, 2, 6),
        Case("nonnormal_degree8_order2_trace_control", 2, 17, 2, 4),
        Case("nonnormal_degree8_order4_trace_control", 2, 17, 4, 2),
    ]

    print("trace-frame relative trace normal-basis toy")
    positive_failures = 0
    nonnormal_controls = 0
    for case in cases:
        theta_rank, eta_rank, eta = run_case(case)
        degree = case.subgroup_order * case.quotient_degree
        theta_normal = theta_rank == degree
        eta_normal = eta_rank == case.quotient_degree
        if theta_normal and not eta_normal:
            positive_failures += 1
        if not theta_normal and not eta_normal:
            nonnormal_controls += 1
        print(
            f"case={case.label} q={case.q} ell={case.ell} "
            f"B_over_E={degree} B_over_C={case.subgroup_order} "
            f"C_over_E={case.quotient_degree} theta_rank={theta_rank} "
            f"theta_normal={int(theta_normal)} eta_rank={eta_rank} "
            f"eta_normal={int(eta_normal)} eta={eta}"
        )

    print("p24")
    print(f"  p24_E_degree_over_Fp={P24_E_DEGREE_OVER_FP}")
    print(f"  p24_B_over_E={P24_B_OVER_E}")
    print(f"  p24_B_over_C={P24_B_OVER_C}")
    print(f"  p24_C_over_E={P24_C_OVER_E}")
    print(f"  p24_trace_periods_are_relative_traces_of_order31_cosets=1")
    print(f"positive_implication_failures={positive_failures}")
    print(f"nonnormal_controls={nonnormal_controls}")
    print("normal_theta_implies_relative_trace_period_normal_basis=1")
    print("relative_trace_normality_is_not_automatic=1")
    print("conclusion=reported_trace_frame_relative_trace_normal_basis_toy")


if __name__ == "__main__":
    main()
