#!/usr/bin/env python3
"""Audit the tempting large-odd-cofactor route for p24.

The strict target orders have sizable odd cofactors, for example

    p + 1 - (-1178414874616) = 2^41 * 454747350887.

It is natural to ask whether one can first construct a curve with the odd
cofactor in its group order, then finish the 2^40 DANGER condition cheaply.

This script records the orientation bookkeeping.  For an odd divisor m, an
X0(m) condition supplies a Frobenius-stable cyclic subgroup.  It does not say
that Frobenius acts as 1 on that subgroup.  The condition m | #E(F_p) is the
odd analogue of X1 orientation: among the roughly phi(m)/2 x-only orientations
on the X0 subgroup, only the lambda=1 or dual lambda=p branch gives the trace
residue t == p+1 mod m.

Thus the apparent residual trace search after imposing m, about sqrt(p)/m,
is multiplied back by the odd orientation cover.  Large odd cofactors are
pleasant after the target isogeny class is known, but they do not give a
sub-sqrt strict sampler by themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

import sympy as sp

P24 = 10**24 + 7
K = 40
M = 1 << K
TARGET_TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class OddChoice:
    trace: int
    m: int
    factors: dict[int, int]
    hasse_trace_count: int
    target_trace_count: int
    residual_trace_trials: float
    orientation_cover: int
    x0_then_orientation_trials: float
    gamma0_index: int
    gamma1_index: int


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def gamma0_index(n: int) -> int:
    value = Fraction(n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell + 1, ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def gamma1_index(n: int) -> int:
    value = Fraction(n * n, 1)
    for ell in sp.factorint(n):
        value *= Fraction(ell * ell - 1, ell * ell)
    if value.denominator != 1:
        raise AssertionError((n, value))
    return value.numerator


def phi(n: int) -> int:
    out = n
    for ell in sp.factorint(n):
        out = out // ell * (ell - 1)
    return out


def hasse_trace_count_divisible_by(m: int) -> int:
    bound = math.isqrt(4 * P24)
    residue = (P24 + 1) % m
    first = -bound + ((residue + bound) % m)
    if first > bound:
        return 0
    return (bound - first) // m + 1


def odd_divisors_of_target_orders() -> list[tuple[int, int]]:
    rows: set[tuple[int, int]] = set()
    for trace in TARGET_TRACES:
        order = P24 + 1 - trace
        odd = order >> v2(order)
        for d in sp.divisors(odd):
            if d > 1:
                rows.add((trace, int(d)))
    return sorted(rows, key=lambda row: (row[1], row[0]))


def audit_choice(trace: int, m: int) -> OddChoice:
    hasse_count = hasse_trace_count_divisible_by(m)
    target_count = sum(1 for t in TARGET_TRACES if (P24 + 1 - t) % m == 0)
    if target_count == 0:
        raise AssertionError((trace, m))
    residual = hasse_count / target_count
    # For odd m > 2, x-only orientation identifies P and -P.
    orient = max(1, phi(m) // 2)
    return OddChoice(
        trace=trace,
        m=m,
        factors={int(q): int(e) for q, e in sp.factorint(m).items()},
        hasse_trace_count=hasse_count,
        target_trace_count=target_count,
        residual_trace_trials=residual,
        orientation_cover=orient,
        x0_then_orientation_trials=orient * residual,
        gamma0_index=gamma0_index(m),
        gamma1_index=gamma1_index(m),
    )


def main() -> None:
    sqrt_p = math.isqrt(P24)
    print("p24 odd-cofactor orientation tradeoff audit")
    print(f"p={P24}")
    print(f"k={K}")
    print(f"2^k={M}")
    print(f"sqrt_floor={sqrt_p}")
    print()

    rows = [audit_choice(trace, m) for trace, m in odd_divisors_of_target_orders()]
    interesting = [
        row
        for row in rows
        if row.m in {
            3,
            7,
            21,
            29,
            71,
            29 * 71,
            110429177,
            43309271513,
            454747350887,
            227373675443,
            909494701773,
        }
    ]

    print("selected_odd_divisors")
    print(
        "  trace m factors hasse_traces target_traces residual "
        "orient_cover orient*residual/sqrt gamma0/sqrt gamma1/sqrt"
    )
    for row in interesting:
        print(
            f"  {row.trace:15d} {row.m:12d} {row.factors!s:34s} "
            f"{row.hasse_trace_count:12d} {row.target_trace_count:13d} "
            f"{row.residual_trace_trials:10.3f} {row.orientation_cover:12d} "
            f"{row.x0_then_orientation_trials / sqrt_p:21.6f} "
            f"{row.gamma0_index / sqrt_p:12.6e} "
            f"{row.gamma1_index / sqrt_p:12.6e}"
        )

    print()
    print("best_by_x0_then_orientation_proxy")
    for row in sorted(rows, key=lambda r: r.x0_then_orientation_trials)[:12]:
        print(
            f"  trace={row.trace:15d} m={row.m:12d} factors={row.factors} "
            f"hasse={row.hasse_trace_count:8d} targets={row.target_trace_count} "
            f"orientation={row.orientation_cover:12d} "
            f"proxy_over_sqrt={row.x0_then_orientation_trials / sqrt_p:.6f}"
        )

    print()
    print("best_by_gamma1_level")
    for row in sorted(rows, key=lambda r: r.gamma1_index)[:12]:
        print(
            f"  trace={row.trace:15d} m={row.m:12d} factors={row.factors} "
            f"gamma1_over_sqrt={row.gamma1_index / sqrt_p:.6e} "
            f"residual={row.residual_trace_trials:.3f}"
        )

    print()
    print("interpretation")
    print("  X0_m_can_have_subsqrt_index_for_large_odd_cofactors=1")
    print("  X0_m_does_not_force_lambda_equal_1=1")
    print("  odd_orientation_cover_times_residual_trace_count_stays_sqrt_scale=1")
    print("  generic_X1_m_level_is_gamma1_and_is_large_for_the_large_cofactors=1")
    print(
        "conclusion=large_odd_cofactors_help_after_trace_selection_but_do_not_"
        "give_a_subsqrt_strict_sampler"
    )


if __name__ == "__main__":
    main()
