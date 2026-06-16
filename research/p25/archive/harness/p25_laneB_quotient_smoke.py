#!/usr/bin/env python3
"""Deterministic p25 Lane B quotient smoke checks.

This validates the formal Frobenius quotient skeletons identified for the
negative p25 trace.  It does not construct a selected packet and therefore is
not a certificate producer.
"""

from __future__ import annotations

from dataclasses import dataclass


P25 = 10**25 + 13


@dataclass(frozen=True)
class QuotientCase:
    name: str
    recovery_n: int
    rho_exp: int
    right: int
    c_axis: int
    b_trace: int
    expected_order: int
    expected_equations: int
    expected_dimension: int


CASES = (
    QuotientCase(
        name="tiny_C3xC13",
        recovery_n=2453448,
        rho_exp=2,
        right=3,
        c_axis=13,
        b_trace=325,
        expected_order=12675,
        expected_equations=21,
        expected_dimension=18,
    ),
    QuotientCase(
        name="prime_axis_C3xC53",
        recovery_n=11536098,
        rho_exp=16,
        right=3,
        c_axis=53,
        b_trace=25,
        expected_order=3975,
        expected_equations=81,
        expected_dimension=78,
    ),
)


def factor(n: int) -> str:
    parts: list[str] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            parts.append(f"{d}^{e}" if e > 1 else str(d))
        d += 1 if d == 2 else 2
    if n > 1:
        parts.append(str(n))
    return " * ".join(parts)


def order_mod(a: int, modulus: int, limit: int) -> int:
    value = 1
    for order in range(1, limit + 1):
        value = value * a % modulus
        if value == 1:
            return order
    raise ValueError(f"order exceeds limit={limit}")


def subgroup(gen: int, order: int, modulus: int) -> set[int]:
    out: set[int] = set()
    value = 1
    for _ in range(order):
        out.add(value)
        value = value * gen % modulus
    if value != 1 or len(out) != order:
        raise AssertionError("subgroup generator has unexpected order")
    return out


def coset_key(value: int, subgroup_values: set[int], modulus: int) -> int:
    return min(value * h % modulus for h in subgroup_values)


def check_case(case: QuotientCase) -> str:
    rho = pow(P25, case.rho_exp, case.recovery_n)
    raw_order = order_mod(rho, case.recovery_n, case.expected_order)
    if raw_order != case.expected_order:
        raise AssertionError((case.name, raw_order, case.expected_order))

    internal = pow(rho, case.right, case.recovery_n)
    trace_subgroup = subgroup(
        pow(internal, case.c_axis, case.recovery_n),
        case.b_trace,
        case.recovery_n,
    )

    qcosets = {
        coset_key(pow(rho, e, case.recovery_n), trace_subgroup, case.recovery_n)
        for e in range(raw_order)
    }
    product_cosets = {
        coset_key(
            pow(rho, case.c_axis * r, case.recovery_n)
            * pow(internal, c, case.recovery_n)
            % case.recovery_n,
            trace_subgroup,
            case.recovery_n,
        )
        for r in range(case.right)
        for c in range(case.c_axis)
    }
    if qcosets != product_cosets:
        raise AssertionError(f"{case.name}: product cosets do not cover quotient")

    quotient_size = case.right * case.c_axis
    equations = (
        (case.right - 1)
        + case.right * (case.c_axis - 1) // 2
        + (case.right - 1) // 2
    )
    dimension = quotient_size - equations
    if equations != case.expected_equations:
        raise AssertionError((case.name, equations, case.expected_equations))
    if dimension != case.expected_dimension:
        raise AssertionError((case.name, dimension, case.expected_dimension))

    return (
        f"{case.name}: n={case.recovery_n} rho=p^{case.rho_exp} "
        f"ord={raw_order}={factor(raw_order)} quotient=C_{case.right}xC_{case.c_axis} "
        f"size={quotient_size} equations={equations} dimension={dimension} "
        "cover=yes"
    )


def main() -> int:
    print("p25 Lane B quotient smoke")
    print(f"p={P25}")
    for case in CASES:
        print(check_case(case))
    print("verdict=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
