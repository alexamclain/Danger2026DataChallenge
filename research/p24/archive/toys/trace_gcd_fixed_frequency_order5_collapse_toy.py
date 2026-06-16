#!/usr/bin/env python3
"""Order-5 collapse for p24 fixed right frequencies.

For p24 the right Frobenius orbit length is 35 and p acts on frequencies by
22 mod 35.  The fixed frequencies are a=5b.  At those frequencies the DFT
coefficient has period 7 along the orbit:

    zeta_35^(5b r) = zeta_7^(b r).

Therefore a fixed-frequency section only depends on the seven order-5 collapsed
sums

    Y_s = sum_{t=0..4} X_{s+7t},  s mod 7.

This is the finite reason a fixed-only audit can avoid adjoining a primitive
35th root: the 7th roots already lie in F_p because p=1 mod 7.  The same
collapse deliberately does not determine nonfixed frequencies.
"""

from __future__ import annotations

import random


Q = 71
RIGHT_LEN = 35
FIXED_COUNT = 7
ORDER5_COUNT = 5


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def dft35(values: list[int], frequency: int, zeta35: int) -> int:
    return sum(
        value * pow(zeta35, frequency * index % RIGHT_LEN, Q)
        for index, value in enumerate(values)
    ) % Q


def dft7(values: list[int], frequency: int, zeta7: int) -> int:
    return sum(
        value * pow(zeta7, frequency * index % FIXED_COUNT, Q)
        for index, value in enumerate(values)
    ) % Q


def collapse_order5(values: list[int]) -> list[int]:
    return [
        sum(values[s + FIXED_COUNT * t] for t in range(ORDER5_COUNT)) % Q
        for s in range(FIXED_COUNT)
    ]


def add_zero_collapse_perturbation(values: list[int]) -> list[int]:
    out = values[:]
    out[0] = (out[0] + 1) % Q
    out[FIXED_COUNT] = (out[FIXED_COUNT] - 1) % Q
    return out


def main() -> None:
    rng = random.Random(20260606)
    root = primitive_root(Q)
    zeta35 = pow(root, (Q - 1) // RIGHT_LEN, Q)
    zeta7 = pow(zeta35, ORDER5_COUNT, Q)
    values = [rng.randrange(Q) for _ in range(RIGHT_LEN)]
    collapsed = collapse_order5(values)
    fixed_mismatches = []
    for b in range(FIXED_COUNT):
        direct = dft35(values, 5 * b, zeta35)
        collapsed_value = dft7(collapsed, b, zeta7)
        if direct != collapsed_value:
            fixed_mismatches.append((b, direct, collapsed_value))

    perturbed = add_zero_collapse_perturbation(values)
    same_collapse = collapse_order5(values) == collapse_order5(perturbed)
    fixed_changed = any(
        dft35(values, 5 * b, zeta35) != dft35(perturbed, 5 * b, zeta35)
        for b in range(FIXED_COUNT)
    )
    nonfixed_changed = dft35(values, 1, zeta35) != dft35(perturbed, 1, zeta35)

    print("Trace-GCD fixed-frequency order-5 collapse toy")
    print(f"q={Q}")
    print(f"right_len={RIGHT_LEN}")
    print(f"fixed_frequency_count={FIXED_COUNT}")
    print(f"order5_collapse_length={ORDER5_COUNT}")
    print(f"fixed_frequency_mismatches={len(fixed_mismatches)}")
    print(f"same_order5_collapsed_sums_after_control={int(same_collapse)}")
    print(f"fixed_frequencies_changed_after_control={int(fixed_changed)}")
    print(f"nonfixed_frequency_changed_after_control={int(nonfixed_changed)}")
    print("interpretation")
    print("  fixed_frequency_sections_depend_only_on_order5_collapsed_sums=1")
    print("  fixed_only_audit_needs_7th_roots_not_35th_roots=1")
    print("  nonfixed_frequencies_are_not_determined_by_order5_collapse=1")
    print("  p24_fixed_relation_can_be_tested_in_the_7_part=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_order5_collapse_toy")

    if fixed_mismatches:
        raise SystemExit(1)
    if not same_collapse or fixed_changed or not nonfixed_changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
