#!/usr/bin/env python3
"""Exact quotient-to-packet contract for p25 Lane B.

The quotient smoke proves that the negative trace has small formal quotients.
This script records the exact post-B/C packet coordinates a selected producer
must fill.

For a raw cyclic value Y[e] indexed by powers of rho, the post-B trace packet is

    g(r, c) = sum_{j=0}^{B-1} Y[c_axis*r + right*c + right*c_axis*j].

The selected defect tested by p25_selected_defect_value_gate.py is then

    f(r, c) = g(r, c) - g(r, 0).
"""

from __future__ import annotations

from dataclasses import dataclass


P25 = 10**25 + 13


@dataclass(frozen=True)
class ContractCase:
    name: str
    recovery_n: int
    rho_exp: int
    right: int
    c_axis: int
    b_trace: int
    expected_order: int


CASES = (
    ContractCase("tiny_C3xC13", 2453448, 2, 3, 13, 325, 12675),
    ContractCase("prime_axis_C3xC53", 11536098, 16, 3, 53, 25, 3975),
    ContractCase("square_axis_C3xC169", 2453448, 2, 3, 169, 25, 12675),
)


def factor(n: int) -> str:
    parts: list[str] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            exp = 0
            while n % divisor == 0:
                n //= divisor
                exp += 1
            parts.append(f"{divisor}^{exp}" if exp > 1 else str(divisor))
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        parts.append(str(n))
    return " * ".join(parts)


def order_mod(value: int, modulus: int, limit: int) -> int:
    acc = 1
    for order in range(1, limit + 1):
        acc = acc * value % modulus
        if acc == 1:
            return order
    raise AssertionError(f"order exceeds limit={limit}")


def block_exponents(case: ContractCase, r: int, c: int) -> list[int]:
    step = case.right * case.c_axis
    start = case.c_axis * r + case.right * c
    return [(start + step * j) % case.expected_order for j in range(case.b_trace)]


def axis_decomposition(case: ContractCase) -> tuple[int, int]:
    quotient_order = case.right * case.c_axis
    for right_power in range(case.right):
        for c_power in range(case.c_axis):
            exponent = case.c_axis * right_power + case.right * c_power
            if exponent % quotient_order == 1:
                return right_power, c_power
    raise AssertionError("rho does not decompose in quotient axes")


def check_case(case: ContractCase) -> list[str]:
    rho = pow(P25, case.rho_exp, case.recovery_n)
    raw_order = order_mod(rho, case.recovery_n, case.expected_order)
    if raw_order != case.expected_order:
        raise AssertionError((case.name, raw_order, case.expected_order))
    if raw_order != case.right * case.c_axis * case.b_trace:
        raise AssertionError("raw order does not factor as right*c*B")

    all_blocks: dict[tuple[int, int], tuple[int, ...]] = {}
    seen: set[int] = set()
    for r in range(case.right):
        for c in range(case.c_axis):
            exponents = tuple(block_exponents(case, r, c))
            if len(set(exponents)) != case.b_trace:
                raise AssertionError("B-trace block has duplicates")
            overlap = seen.intersection(exponents)
            if overlap:
                raise AssertionError(f"overlapping B-trace blocks: {sorted(overlap)[:3]}")
            seen.update(exponents)
            all_blocks[(r, c)] = exponents
    if len(seen) != raw_order:
        raise AssertionError("B-trace blocks do not partition raw cycle")

    quotient_size = case.right * case.c_axis
    condition_count = (
        (case.right - 1)
        + case.right * ((case.c_axis - 1) // 2)
        + ((case.right - 1) // 2)
    )
    dimension = quotient_size - condition_count
    right_power, c_power = axis_decomposition(case)

    lines = [
        (
            f"{case.name}: n={case.recovery_n} rho=p^{case.rho_exp} "
            f"raw_order={raw_order}={factor(raw_order)} "
            f"right={case.right} c={case.c_axis} B={case.b_trace} "
            f"quotient_size={quotient_size} value_equations={condition_count} "
            f"admissible_dimension={dimension} partition=yes"
        ),
        (
            "  axis_decomposition: "
            f"rho = (rho^{case.c_axis})^{right_power} * "
            f"(rho^{case.right})^{c_power} mod B "
            f"(exponent {case.c_axis * right_power + case.right * c_power} "
            f"= 1 mod {quotient_size})"
        ),
        (
            "  packet_contract: "
            f"g(r,c)=sum_{{j=0}}^{case.b_trace - 1} "
            f"Y[{case.c_axis}*r + {case.right}*c + "
            f"{case.right * case.c_axis}*j mod {raw_order}]"
        ),
        (
            "  first_blocks: "
            f"g(0,0)={list(all_blocks[(0, 0)][:min(8, case.b_trace)])}; "
            f"g(1,0)={list(all_blocks[(1, 0)][:min(8, case.b_trace)])}; "
            f"g(0,1)={list(all_blocks[(0, 1)][:min(8, case.b_trace)])}"
        ),
    ]
    return lines


def main() -> int:
    print("p25 Lane B packet contract")
    print(f"p={P25}")
    for case in CASES:
        for line in check_case(case):
            print(line)
    print("verdict=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
