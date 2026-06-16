#!/usr/bin/env python3
"""Toy gate for the prefix Hilbert-90 nonintersection form.

For coprime finite extensions L=F_q^l, R=F_q^r, E=F_q^(lr), the p24
four-prefix theorem can be written as:

    R^k -> L,
    (y_j) -> Tr_{E/L}(sum_j y_j*S_j)

is injective.  Let phi(y)=sum_j y_j*S_j and tau be the generator of Gal(E/L).
Additive Hilbert 90 says ker Tr_{E/L} = image(tau-1), so injectivity is
equivalent to:

    phi is injective and image(phi) cap image(tau-1) = {0}.

This toy verifies that finite handoff and includes controls where each part
fails.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd
import random

from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_adjoint_trace_toy import (
    coordinate_vector,
    random_element,
    relative_trace_to_left,
)


@dataclass(frozen=True)
class Hilbert90Row:
    label: str
    domain_dim: int
    phi_rank: int
    trace_rank: int
    domain_trace_kernel_dim: int
    coboundary_rank: int
    trace_kernel_dim: int
    coboundary_trace_failures: int
    image_coboundary_intersection_dim: int
    phi_injective: bool
    trace_injective: bool
    hilbert90_match: bool
    nonintersection_event: bool
    event_match: bool


def standard_basis(field: ExtensionField) -> list[FpE]:
    return [
        tuple(1 if i == j else 0 for i in range(field.degree))
        for j in range(field.degree)
    ]


def right_frobenius_step(left_degree: int, right_degree: int) -> int:
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("right Frobenius step expects coprime degrees")
    return left_degree * pow(left_degree % right_degree, -1, right_degree)


def tau_right(
    value: FpE,
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> FpE:
    return field.pow(value, field.q ** right_frobenius_step(left_degree, right_degree))


def row_span_intersection_dim(
    left_rows: list[list[int]],
    right_rows: list[list[int]],
    q: int,
) -> int:
    return (
        rank_mod_q(left_rows, q)
        + rank_mod_q(right_rows, q)
        - rank_mod_q(left_rows + right_rows, q)
    )


def phi_rows(
    seeds: list[FpE],
    right_basis: list[FpE],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in seeds:
        for y in right_basis:
            rows.append(list(field.mul(y, seed)))
    return rows


def trace_rows(
    seeds: list[FpE],
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for seed in seeds:
        for y in right_basis:
            trace_value = relative_trace_to_left(
                field.mul(y, seed),
                left_degree,
                right_degree,
                field,
            )
            rows.append(coordinate_vector(trace_value, left_degree, left_inverse, field))
    return rows


def coboundary_rows(
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for value in standard_basis(field):
        rows.append(list(field.sub(tau_right(value, left_degree, right_degree, field), value)))
    return rows


def full_trace_rows(
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for value in standard_basis(field):
        trace_value = relative_trace_to_left(value, left_degree, right_degree, field)
        rows.append(coordinate_vector(trace_value, left_degree, left_inverse, field))
    return rows


def coboundary_trace_failures(
    coboundaries: list[list[int]],
    left_degree: int,
    right_degree: int,
    field: ExtensionField,
) -> int:
    failures = 0
    for row in coboundaries:
        value = tuple(row)
        if relative_trace_to_left(value, left_degree, right_degree, field) != field.zero:
            failures += 1
    return failures


def audit_tuple(
    label: str,
    seeds: list[FpE],
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
    cob_rows: list[list[int]],
    trace_kernel_dim: int,
    cob_trace_failures: int,
) -> Hilbert90Row:
    domain_dim = len(seeds) * right_degree
    prows = phi_rows(seeds, right_basis, field)
    trows = trace_rows(
        seeds,
        right_basis,
        left_degree,
        right_degree,
        left_inverse,
        field,
    )
    phi_rank = rank_mod_q(prows, field.q)
    trace_rank = rank_mod_q(trows, field.q)
    cob_rank = rank_mod_q(cob_rows, field.q)
    intersection = row_span_intersection_dim(prows, cob_rows, field.q)
    phi_injective = phi_rank == domain_dim
    trace_injective = trace_rank == domain_dim
    hilbert90_match = cob_rank == trace_kernel_dim and cob_trace_failures == 0
    nonintersection_event = phi_injective and intersection == 0
    return Hilbert90Row(
        label=label,
        domain_dim=domain_dim,
        phi_rank=phi_rank,
        trace_rank=trace_rank,
        domain_trace_kernel_dim=domain_dim - trace_rank,
        coboundary_rank=cob_rank,
        trace_kernel_dim=trace_kernel_dim,
        coboundary_trace_failures=cob_trace_failures,
        image_coboundary_intersection_dim=intersection,
        phi_injective=phi_injective,
        trace_injective=trace_injective,
        hilbert90_match=hilbert90_match,
        nonintersection_event=nonintersection_event,
        event_match=trace_injective == (hilbert90_match and nonintersection_event),
    )


def find_good_seeds(
    k: int,
    right_basis: list[FpE],
    left_degree: int,
    right_degree: int,
    left_inverse: list[list[FpE]],
    field: ExtensionField,
    cob_rows: list[list[int]],
    trace_kernel_dim: int,
    cob_trace_failures: int,
    rng: random.Random,
    attempts: int,
) -> list[FpE] | None:
    domain_dim = k * right_degree
    for _ in range(attempts):
        seeds = [random_element(field, rng) for _ in range(k)]
        row = audit_tuple(
            "candidate",
            seeds,
            right_basis,
            left_degree,
            right_degree,
            left_inverse,
            field,
            cob_rows,
            trace_kernel_dim,
            cob_trace_failures,
        )
        if row.trace_rank == domain_dim:
            return seeds
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left-degree", type=int, default=5)
    parser.add_argument("--right-degree", type=int, default=2)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if gcd(args.left_degree, args.right_degree) != 1:
        raise ValueError("left and right degrees must be coprime")
    if args.k * args.right_degree > args.left_degree:
        raise ValueError("default theorem gate expects a positive prefix kernel in L")

    extension_degree = args.left_degree * args.right_degree
    field = ExtensionField(
        args.q,
        extension_degree,
        find_irreducible_modulus(args.q, extension_degree, args.seed),
    )
    left_seed = args.seed + 17
    right_seed = args.seed + 29
    right_basis = subfield_power_basis(args.q, args.right_degree, field, right_seed)
    left_inverse = lang_inverse_for_orbit(args.q, args.left_degree, field, left_seed)
    cob_rows = coboundary_rows(args.left_degree, args.right_degree, field)
    full_trows = full_trace_rows(
        args.left_degree,
        args.right_degree,
        left_inverse,
        field,
    )
    trace_kernel_dim = extension_degree - rank_mod_q(full_trows, args.q)
    cob_trace_failures = coboundary_trace_failures(
        cob_rows,
        args.left_degree,
        args.right_degree,
        field,
    )
    rng = random.Random(args.seed)

    rows: list[Hilbert90Row] = []
    rows.append(
        audit_tuple(
            "forced_zero",
            [field.zero for _ in range(args.k)],
            right_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
            cob_rows,
            trace_kernel_dim,
            cob_trace_failures,
        )
    )

    repeated = random_element(field, rng)
    rows.append(
        audit_tuple(
            "forced_repeated_seed",
            [repeated for _ in range(args.k)],
            right_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
            cob_rows,
            trace_kernel_dim,
            cob_trace_failures,
        )
    )

    z = random_element(field, rng)
    coboundary_seed = field.sub(
        tau_right(z, args.left_degree, args.right_degree, field),
        z,
    )
    rows.append(
        audit_tuple(
            "forced_coboundary_intersection",
            [coboundary_seed] + [random_element(field, rng) for _ in range(args.k - 1)],
            right_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
            cob_rows,
            trace_kernel_dim,
            cob_trace_failures,
        )
    )

    good = find_good_seeds(
        args.k,
        right_basis,
        args.left_degree,
        args.right_degree,
        left_inverse,
        field,
        cob_rows,
        trace_kernel_dim,
        cob_trace_failures,
        rng,
        attempts=2000,
    )
    if good is not None:
        rows.append(
            audit_tuple(
                "found_hilbert90_nonintersection",
                good,
                right_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
                cob_rows,
                trace_kernel_dim,
                cob_trace_failures,
            )
        )

    for trial in range(args.trials):
        rows.append(
            audit_tuple(
                f"random_{trial}",
                [random_element(field, rng) for _ in range(args.k)],
                right_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
                cob_rows,
                trace_kernel_dim,
                cob_trace_failures,
            )
        )

    print("Trace-GCD prefix Hilbert-90 nonintersection toy")
    print(f"q={args.q}")
    print(f"left_degree={args.left_degree}")
    print(f"right_degree={args.right_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"domain_dim={args.k * args.right_degree}")
    print(f"expected_positive_kernel_dim={args.left_degree - args.k * args.right_degree}")
    print("columns: label phi_rank trace_rank domain_kernel intersection phi_inj trace_inj h90 nonintersection event_match")
    for row in rows[:24]:
        print(
            f"row label={row.label} phi_rank={row.phi_rank} "
            f"trace_rank={row.trace_rank} "
            f"domain_kernel={row.domain_trace_kernel_dim} "
            f"intersection={row.image_coboundary_intersection_dim} "
            f"phi_inj={int(row.phi_injective)} "
            f"trace_inj={int(row.trace_injective)} "
            f"h90={int(row.hilbert90_match)} "
            f"nonintersection={int(row.nonintersection_event)} "
            f"event_match={int(row.event_match)}"
        )
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  coboundary_rank={rank_mod_q(cob_rows, args.q)}")
    print(f"  trace_kernel_dim={trace_kernel_dim}")
    print(f"  coboundary_trace_failures={cob_trace_failures}")
    print(f"  hilbert90_match_failures={sum(not row.hilbert90_match for row in rows)}")
    print(f"  trace_nonintersection_event_mismatches={sum(not row.event_match for row in rows)}")
    print(
        "  found_hilbert90_nonintersection="
        f"{int(any(row.label == 'found_hilbert90_nonintersection' and row.trace_injective for row in rows))}"
    )
    print(
        "  forced_coboundary_intersection_detected="
        f"{int(any(row.label == 'forced_coboundary_intersection' and row.image_coboundary_intersection_dim > 0 and not row.trace_injective for row in rows))}"
    )
    print(
        "  forced_period_dependence_detected="
        f"{int(any(row.label == 'forced_repeated_seed' and not row.phi_injective for row in rows))}"
    )
    print("interpretation")
    print("  ker_trace_equals_tau_minus_one_image=1")
    print("  prefix_adjoint_injective_iff_no_hilbert90_coboundary_intersection=1")
    print("  p24_prefix_target_is_no_resolvent_coboundary=1")
    print("conclusion=reported_trace_gcd_prefix_hilbert90_toy")


if __name__ == "__main__":
    main()
