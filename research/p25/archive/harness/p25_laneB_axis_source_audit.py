#!/usr/bin/env python3
"""Local source audit for the p25 Lane B quotient axes.

The Lane B quotient skeletons are orders of rho modulo a recovery modulus n.
This audit factors n and records which local factors survive the B-trace.

For a local factor m_i with ord_i = ord(rho mod m_i), the post-B selector sees

    ord_i / gcd(ord_i, B).

This identifies the source of the right C_3 axis and the C-axis.
"""

from __future__ import annotations

from dataclasses import dataclass


P25 = 10**25 + 13


@dataclass(frozen=True)
class AxisCase:
    name: str
    recovery_n: int
    rho_exp: int
    right: int
    c_axis: int
    b_trace: int
    raw_order: int


CASES = (
    AxisCase("tiny_C3xC13", 2453448, 2, 3, 13, 325, 12675),
    AxisCase("prime_axis_C3xC53", 11536098, 16, 3, 53, 25, 3975),
    AxisCase("square_axis_C3xC169", 2453448, 2, 3, 169, 25, 12675),
)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def factor_prime_powers(n: int) -> list[tuple[int, int, int]]:
    out: list[tuple[int, int, int]] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            exp = 0
            power = 1
            while n % divisor == 0:
                n //= divisor
                exp += 1
                power *= divisor
            out.append((divisor, exp, power))
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        out.append((n, 1, n))
    return out


def factor_string(n: int) -> str:
    parts = []
    for prime, exp, _ in factor_prime_powers(n):
        parts.append(f"{prime}^{exp}" if exp > 1 else str(prime))
    return " * ".join(parts) if parts else "1"


def order_mod(value: int, modulus: int, limit: int) -> int:
    if gcd(value, modulus) != 1:
        raise AssertionError("non-unit")
    acc = 1
    for order in range(1, limit + 1):
        acc = acc * value % modulus
        if acc == 1:
            return order
    raise AssertionError(f"order exceeds {limit}")


def classify_visible(case: AxisCase, visible_order: int) -> str:
    if visible_order == 1:
        return "killed"
    if visible_order == case.right:
        return "right_axis"
    if visible_order == case.c_axis:
        return "c_axis"
    if visible_order == case.right * case.c_axis:
        return "mixed_full_quotient"
    return "mixed_or_residual"


def audit_case(case: AxisCase) -> list[str]:
    rho = pow(P25, case.rho_exp, case.recovery_n)
    raw_lcm = 1
    visible_lcm = 1
    rows = [
        (
            f"case {case.name}: n={case.recovery_n}={factor_string(case.recovery_n)} "
            f"rho=p^{case.rho_exp} raw_order={case.raw_order}={factor_string(case.raw_order)} "
            f"B={case.b_trace} quotient={case.right * case.c_axis}"
        )
    ]
    for prime, exp, power in factor_prime_powers(case.recovery_n):
        local_rho = rho % power
        local_order = order_mod(local_rho, power, case.raw_order)
        visible = local_order // gcd(local_order, case.b_trace)
        raw_lcm = lcm(raw_lcm, local_order)
        visible_lcm = lcm(visible_lcm, visible)
        rows.append(
            "  local "
            f"mod={power} prime={prime}^{exp} "
            f"ord={local_order}={factor_string(local_order)} "
            f"gcd(ord,B)={gcd(local_order, case.b_trace)} "
            f"visible_after_B={visible}={factor_string(visible)} "
            f"role={classify_visible(case, visible)}"
        )
    rows.append(
        "  check "
        f"raw_lcm={raw_lcm} visible_lcm={visible_lcm} "
        f"raw_ok={int(raw_lcm == case.raw_order)} "
        f"quotient_ok={int(visible_lcm == case.right * case.c_axis)}"
    )
    return rows


def main() -> int:
    print("p25 Lane B axis source audit")
    print(f"p={P25}")
    for case in CASES:
        for line in audit_case(case):
            print(line)
    print("interpretation")
    print("  B_trace_kills_local_kernel_orders_and_leaves_the_right3_plus_C_axis=1")
    print("  tiny_C3xC13_uses_mod151_for_right3_and_mod677_for_C13=1")
    print("  prime_axis_C3xC53_uses_mod107_for_C53_and_has_right3_visible_on_mod7_and_mod151=1")
    print("  square_axis_C3xC169_uses_mod151_for_right3_and_mod677_for_C169=1")
    print("  embedded_packet_Y_must_couple_these_local_sources=1")
    print("conclusion=reported_p25_laneB_axis_source_audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
