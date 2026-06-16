#!/usr/bin/env python3
"""Phase sensitivity of the centered full-origin product.

The centered full-origin Borcherds route hopes to replace many local
determinants by a closed class-field product.  This gate checks what data such
a product can depend on in a pinned actual-CM row.

It preserves each quotient fiber

    {j_{r + m*k} : 0 <= k < n}

as an unordered set, but randomly shuffles the selected child order inside
the fibers.  The centered origin/right determinant product changes.  Thus
unordered relative fibers or trace/norm data do not determine the full-origin
Chow product; the p-unit theorem must retain embedded phase/order data or
construct the Chow/Fitting divisor directly.
"""

from __future__ import annotations

import argparse
import random

from relative_moment_projection_scan import rotate
from packetized_relative_content_scan import packet_factors
from centered_marginal_alpha_sequence_complexity import normalized_right_sequence
from centered_marginal_origin_product_audit import (
    OriginProductAudit,
    audit_case,
    leading_det_for_shift,
    product_mod,
    scan,
    translation_det_on_zero_sum,
)


PINNED_D = -13319
PINNED_Q = 13463
PINNED_M = 28
PINNED_LEFT = 4
PINNED_RIGHT = 7
TRIALS = 8
SEED = 20260606


def pinned_args() -> argparse.Namespace:
    return argparse.Namespace(
        max_cases=24,
        min_h=12,
        max_h=220,
        max_abs_D=80000,
        max_prime_quotients=12,
        max_composite_quotients=24,
        min_n=3,
        max_n=220,
        q_start=PINNED_Q,
        q_stop=PINNED_Q + 1,
        max_splitting_primes=1,
        max_m=120,
        max_factor_degree=12,
        include_linear=False,
        only_D=PINNED_D,
        only_m=PINNED_M,
        only_left=PINNED_LEFT,
        only_right=PINNED_RIGHT,
    )


def matching_factor(row: OriginProductAudit):
    for factor in packet_factors(row.n, row.q):
        if factor.degree() != row.factor_degree:
            continue
        candidate = audit_case(
            row.D,
            row.q,
            row.ell,
            list(row.cycle),
            row.m,
            factor,
            row.left,
            row.right,
        )
        if candidate is not None and candidate.alpha_values == row.alpha_values:
            return factor
    raise RuntimeError("could not recover the pinned packet factor")


def alpha_values_for_cycle(row: OriginProductAudit, factor, cycle: list[int]) -> list[int]:
    return [
        leading_det_for_shift(
            cycle,
            row.q,
            row.m,
            factor,
            row.left,
            row.right,
            (row.n * alpha) % row.h,
        )
        for alpha in range(row.m)
    ]


def normalized_right_classes(row: OriginProductAudit, values: list[int]) -> dict[int, set[int]]:
    classes: dict[int, set[int]] = {}
    for alpha, value in enumerate(values):
        sign = translation_det_on_zero_sum(row.left, alpha)
        normalized = value if sign == 1 else (-value) % row.q
        classes.setdefault(alpha % row.right, set()).add(normalized)
    return classes


def normalized_right_values(row: OriginProductAudit, values: list[int]) -> tuple[int, ...] | None:
    classes = normalized_right_classes(row, values)
    if any(len(bucket) != 1 for bucket in classes.values()):
        return None
    return tuple(next(iter(classes[index])) for index in range(row.right))


def fiber_multisets(row: OriginProductAudit, cycle: list[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sorted(cycle[r + row.m * k] for k in range(row.n)))
        for r in range(row.m)
    )


def shuffled_inside_recovery_fibers(row: OriginProductAudit, rng: random.Random) -> list[int]:
    cycle = list(row.cycle)
    for r in range(row.m):
        positions = [r + row.m * k for k in range(row.n)]
        values = [cycle[position] for position in positions]
        rng.shuffle(values)
        for position, value in zip(positions, values):
            cycle[position] = value
    return cycle


def main() -> None:
    row = scan(pinned_args())
    if row is None:
        raise SystemExit("pinned row not found")
    factor = matching_factor(row)
    rng = random.Random(SEED)

    original_alpha = list(row.alpha_values)
    original_product = product_mod(original_alpha, row.q)
    original_right = tuple(normalized_right_sequence(row))
    original_right_product = product_mod(list(original_right), row.q)
    original_fibers = fiber_multisets(row, list(row.cycle))

    shifted_product_preserved = 0
    for shift in [1, row.n, row.m, row.n + row.m]:
        shifted = rotate(list(row.cycle), shift)
        shifted_alpha = alpha_values_for_cycle(row, factor, shifted)
        shifted_product_preserved += int(product_mod(shifted_alpha, row.q) == original_product)

    fiber_preserved = 0
    product_changed = 0
    right_sequence_changed = 0
    right_factorization_failed = 0
    zero_products = 0
    for _trial in range(TRIALS):
        shuffled = shuffled_inside_recovery_fibers(row, rng)
        fiber_preserved += int(fiber_multisets(row, shuffled) == original_fibers)
        alpha = alpha_values_for_cycle(row, factor, shuffled)
        alpha_product = product_mod(alpha, row.q)
        right = normalized_right_values(row, alpha)
        product_changed += int(alpha_product != original_product)
        zero_products += int(alpha_product == 0)
        right_factorization_failed += int(right is None)
        right_sequence_changed += int(right != original_right)

    print("Centered marginal full-origin phase-sensitivity gate")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"original_alpha_product={original_product}")
    print(f"original_right_product={original_right_product}")
    print(f"original_right_values={list(original_right)}")
    print(f"cyclic_origin_shift_product_preserved={shifted_product_preserved}/4")
    print(f"fiber_multisets_preserved_by_shuffle={fiber_preserved}/{TRIALS}")
    print(f"fiber_shuffle_alpha_product_changed={product_changed}/{TRIALS}")
    print(f"fiber_shuffle_right_sequence_changed={right_sequence_changed}/{TRIALS}")
    print(f"fiber_shuffle_right_factorization_failed={right_factorization_failed}/{TRIALS}")
    print(f"fiber_shuffle_zero_products={zero_products}/{TRIALS}")
    print("interpretation")
    print("  cyclic_origin_shift_preserves_the_full_origin_product=1")
    print("  unordered_recovery_fibers_do_not_determine_centered_full_origin_product=1")
    print("  full_origin_borcherds_producer_must_be_phase_aware=1")
    print("  closed_divisor_formula_cannot_be_replaced_by_unordered_fiber_data=1")
    print("conclusion=reported_centered_marginal_full_origin_phase_sensitivity_gate")

    if (row.D, row.q, row.m, row.n, row.left, row.right) != (
        PINNED_D,
        PINNED_Q,
        PINNED_M,
        5,
        PINNED_LEFT,
        PINNED_RIGHT,
    ):
        raise SystemExit(1)
    if shifted_product_preserved != 4:
        raise SystemExit(1)
    if fiber_preserved != TRIALS:
        raise SystemExit(1)
    if product_changed != TRIALS:
        raise SystemExit(1)
    if right_sequence_changed != TRIALS:
        raise SystemExit(1)
    if zero_products != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
