#!/usr/bin/env python3
"""p24 defect-support accounting for the RS-tail frequency-resultant route.

The cyclic-section descent gate says a base selector must have Frobenius-stable
support.  For p24 the frequency set is Z/35Z and Frobenius acts by

    a |-> 22*a mod 35.

This audit records the exact stable support possibilities of size 16.  It
also corrects an easy overstatement: descent alone does not force four
length-4 orbits.  A stable 16-set can also contain four fixed frequencies and
three length-4 orbits.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


P = 10**24 + 7
MODULUS = 35
TAIL_DIM = 16
FROBENIUS = P % MODULUS


@dataclass(frozen=True)
class SupportAccounting:
    modulus: int
    frobenius: int
    tail_dim: int
    fixed_orbits: tuple[tuple[int, ...], ...]
    length4_orbits: tuple[tuple[int, ...], ...]
    pure_length4_supports: int
    mixed_fixed_length4_supports: int
    total_stable_supports: int
    nonstable_size16_supports: int


def frobenius_orbits(modulus: int, multiplier: int) -> list[tuple[int, ...]]:
    seen: set[int] = set()
    out: list[tuple[int, ...]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = multiplier * current % modulus
        out.append(tuple(orbit))
    return out


def stable_supports_of_size(
    orbits: list[tuple[int, ...]],
    size: int,
) -> list[tuple[tuple[int, ...], ...]]:
    out: list[tuple[tuple[int, ...], ...]] = []

    def rec(index: int, chosen: list[tuple[int, ...]], total: int) -> None:
        if total == size:
            out.append(tuple(chosen))
            return
        if total > size or index == len(orbits):
            return
        rec(index + 1, chosen, total)
        chosen.append(orbits[index])
        rec(index + 1, chosen, total + len(orbits[index]))
        chosen.pop()

    rec(0, [], 0)
    return out


def n_choose_k(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    out = 1
    for i in range(1, k + 1):
        out = out * (n - i + 1) // i
    return out


def support_accounting() -> SupportAccounting:
    orbits = frobenius_orbits(MODULUS, FROBENIUS)
    fixed = tuple(orbit for orbit in orbits if len(orbit) == 1)
    length4 = tuple(orbit for orbit in orbits if len(orbit) == 4)
    stable = stable_supports_of_size(orbits, TAIL_DIM)
    pure = sum(1 for support in stable if all(len(orbit) == 4 for orbit in support))
    mixed = len(stable) - pure
    all_size16 = n_choose_k(MODULUS, TAIL_DIM)
    return SupportAccounting(
        modulus=MODULUS,
        frobenius=FROBENIUS,
        tail_dim=TAIL_DIM,
        fixed_orbits=fixed,
        length4_orbits=length4,
        pure_length4_supports=pure,
        mixed_fixed_length4_supports=mixed,
        total_stable_supports=len(stable),
        nonstable_size16_supports=all_size16 - len(stable),
    )


def support_type_counts(
    fixed_count: int,
    length4_count: int,
    size: int,
) -> list[tuple[int, int, int]]:
    rows: list[tuple[int, int, int]] = []
    for fixed_used in range(fixed_count + 1):
        remaining = size - fixed_used
        if remaining < 0 or remaining % 4:
            continue
        length4_used = remaining // 4
        if length4_used > length4_count:
            continue
        rows.append(
            (
                fixed_used,
                length4_used,
                n_choose_k(fixed_count, fixed_used)
                * n_choose_k(length4_count, length4_used),
            )
        )
    return rows


def main() -> None:
    row = support_accounting()
    type_rows = support_type_counts(
        len(row.fixed_orbits),
        len(row.length4_orbits),
        row.tail_dim,
    )
    print("Trace-GCD RS-tail p24 defect-support accounting")
    print(f"p={P}")
    print(f"modulus={row.modulus}")
    print(f"frobenius_mod_35={row.frobenius}")
    print(f"tail_dim={row.tail_dim}")
    print(f"fixed_orbit_count={len(row.fixed_orbits)}")
    print(f"length4_orbit_count={len(row.length4_orbits)}")
    print(f"fixed_orbits={list(map(list, row.fixed_orbits))}")
    print(f"length4_orbits={list(map(list, row.length4_orbits))}")
    print("stable_support_type_counts")
    for fixed_used, length4_used, count in type_rows:
        print(
            f"  fixed_singletons={fixed_used} "
            f"length4_orbits={length4_used} count={count}"
        )
    print(f"pure_length4_supports={row.pure_length4_supports}")
    print(f"mixed_fixed_length4_supports={row.mixed_fixed_length4_supports}")
    print(f"total_stable_supports={row.total_stable_supports}")
    print(f"nonstable_size16_supports={row.nonstable_size16_supports}")
    print("interpretation")
    print("  p24_frobenius_stable_16_supports_are_exactly_two_types=1")
    print("  four_length4_orbits_is_not_forced_by_descent_alone=1")
    print("  no_fixed_defect_theorem_would_reduce_supports_from_1260_to_35=1")
    print("  mixed_supports_require_four_fixed_frequencies_plus_three_length4_orbits=1")
    print("  p24_defect_selector_still_needs_arithmetic_support_identification=1")
    print("conclusion=reported_trace_gcd_rs_tail_defect_support_accounting")

    expected_type_rows = [(0, 4, 35), (4, 3, 1225)]
    if (
        row.frobenius != 22
        or len(row.fixed_orbits) != 7
        or len(row.length4_orbits) != 7
        or type_rows != expected_type_rows
        or row.pure_length4_supports != 35
        or row.mixed_fixed_length4_supports != 1225
        or row.total_stable_supports != 1260
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
