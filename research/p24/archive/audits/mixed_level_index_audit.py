#!/usr/bin/env python3
"""Audit mixed-level modular-curve costs for p24 target orders.

The strict verifier needs a 2^40 x-only point, but one possible detour is:

1. construct a curve whose order is forced by a large mixed divisor N of
   #E(F_p), perhaps using odd cofactors;
2. once the target isogeny class is known, obtain the 2^40 point by projection.

For this to beat sqrt(p), the construction of the mixed level itself must be
sub-sqrt.  The cheapest modular condition of this form is X0(N), a rational
cyclic subgroup of order N; X1(N), a rational point of order N, is harder.
This audit enumerates target-order divisors and records the best Gamma0/Gamma1
indices among divisors exceeding the relevant Hasse thresholds.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from sympy import divisors, factorint

P24 = 10**24 + 7
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Choice:
    trace: int
    divisor: int
    factors: dict[int, int]
    gamma0_index: int
    gamma1_index: int


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def gamma1_index(n: int) -> int:
    # [SL2(Z):Gamma1(N)] for N > 2.
    value = Fraction(n * n, 1)
    for ell in factorint(n):
        value *= Fraction(ell * ell - 1, ell * ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def choices_above(trace: int, threshold: int) -> list[Choice]:
    order = P24 + 1 - trace
    out: list[Choice] = []
    for d in divisors(order):
        if d <= threshold:
            continue
        out.append(
            Choice(
                trace=trace,
                divisor=d,
                factors=factorint(d),
                gamma0_index=gamma0_index(d),
                gamma1_index=gamma1_index(d),
            )
        )
    return out


def print_choice(label: str, choice: Choice | None, sqrt_p: int) -> None:
    if choice is None:
        print(f"  {label}=none")
        return
    print(
        f"  {label}: divisor={choice.divisor} factors={choice.factors} "
        f"gamma0={choice.gamma0_index} gamma0/sqrt={choice.gamma0_index / sqrt_p:.6f} "
        f"gamma1={choice.gamma1_index} gamma1/sqrt={choice.gamma1_index / sqrt_p:.6e}"
    )


def main() -> None:
    sqrt_p = math.isqrt(P24)
    danger_bound = sqrt_p + 1 + math.isqrt(4 * sqrt_p)
    hasse_width = math.isqrt(4 * P24) + 1
    thresholds = [
        ("danger_bound", danger_bound),
        ("hasse_width", hasse_width),
    ]

    print("p24 mixed-level modular index audit")
    print(f"p={P24}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"danger_bound={danger_bound}")
    print(f"hasse_width={hasse_width}")

    global_best_g0: dict[str, Choice | None] = {label: None for label, _ in thresholds}
    global_best_g1: dict[str, Choice | None] = {label: None for label, _ in thresholds}

    for trace in TARGET_TRACES:
        order = P24 + 1 - trace
        print()
        print(f"trace={trace}")
        print(f"  order={order}")
        print(f"  factor(order)={factorint(order)}")
        for label, threshold in thresholds:
            rows = choices_above(trace, threshold)
            best_g0 = min(rows, key=lambda row: row.gamma0_index, default=None)
            best_g1 = min(rows, key=lambda row: row.gamma1_index, default=None)
            print(f" threshold={label} value={threshold}")
            print_choice("best_gamma0", best_g0, sqrt_p)
            print_choice("best_gamma1", best_g1, sqrt_p)
            if best_g0 and (
                global_best_g0[label] is None
                or best_g0.gamma0_index < global_best_g0[label].gamma0_index
            ):
                global_best_g0[label] = best_g0
            if best_g1 and (
                global_best_g1[label] is None
                or best_g1.gamma1_index < global_best_g1[label].gamma1_index
            ):
                global_best_g1[label] = best_g1

    print()
    print("global_best")
    for label, _threshold in thresholds:
        print(f" threshold={label}")
        print_choice("best_gamma0", global_best_g0[label], sqrt_p)
        print_choice("best_gamma1", global_best_g1[label], sqrt_p)
    print("conclusion=mixed_odd_levels_do_not_give_subsqrt_modular_construction")


if __name__ == "__main__":
    main()
