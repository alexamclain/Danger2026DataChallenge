#!/usr/bin/env python3
"""Compute the split 2-adic branch valuations for the p24 strict traces."""

from __future__ import annotations

P = 10**24 + 7
TRACES = [1020608380936, -78903246840, -1178414874616]


def v2(n: int) -> int:
    n = abs(n)
    out = 0
    while n and n % 2 == 0:
        out += 1
        n //= 2
    return out if n else 10**9


def sqrt_mod_power_two_roots(a: int, exponent: int) -> list[int]:
    modulus = 8
    roots = [r for r in range(8) if (r * r - a) % 8 == 0]
    while modulus < (1 << exponent):
        lifted: list[int] = []
        for root in roots:
            for candidate in (root, root + modulus):
                if (candidate * candidate - a) % (2 * modulus) == 0:
                    lifted.append(candidate % (2 * modulus))
        roots = sorted(set(lifted))
        modulus *= 2
    return roots


def main() -> None:
    print("p24 split 2-adic branch audit")
    print(f"p={P}")
    print("trace D_mod_8 v2_order split_valuation_pairs split_exponent_v2")
    for trace in TRACES:
        D = (trace * trace - 4 * P) // 4
        pairs = set()
        for root in sqrt_mod_power_two_roots(D, 80):
            plus = trace // 2 - 1 + root
            minus = trace // 2 - 1 - root
            pairs.add(tuple(sorted((v2(plus), v2(minus)))))
        exponent_v2 = max(max(pair) for pair in pairs)
        print(
            f"{trace} {D % 8} {v2(P + 1 - trace)} "
            f"{sorted(pairs)} {exponent_v2}"
        )
    print("conclusion=reported_p24_split_2adic_branch_audit")


if __name__ == "__main__":
    main()
