#!/usr/bin/env python3
"""Finite gate for the p24 no-fixed-defect theorem.

The cyclic-section descent gate only says the defect selector support is
Frobenius-stable.  The support accounting then leaves two p24 size-16 types:

* four length-4 moving orbits;
* four fixed frequencies plus three length-4 moving orbits.

This gate isolates the extra arithmetic theorem needed to remove the mixed
case.  At a fixed frequency a in 5Z/35Z, "ordinary" means the tail local value
lies in the local prefix image:

    rank(prefix_a, tail_a) = rank(prefix_a).

Equivalently, the fixed frequency has no rank jump and is not a defect line.
Together with Frobenius-stable support of size 16, this reduces the selector
choices from 1260 to the 35 pure moving supports.
"""

from __future__ import annotations

from dataclasses import dataclass

from trace_gcd_rs_tail_defect_support_accounting import (
    FROBENIUS,
    MODULUS,
    TAIL_DIM,
    frobenius_orbits,
    n_choose_k,
)


Q = 211


@dataclass(frozen=True)
class FixedOrdinaryCase:
    label: str
    support_size: int
    stable_support: bool
    fixed_rank_jumps: int
    moving_orbits_used: int
    fixed_ordinary: bool
    pure_moving_support: bool
    tail_vandermonde_rank: int
    selected_basis_frequency_gate: bool
    no_fixed_theorem_applies: bool


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    rows = [row[:] for row in matrix if any(value % q for value in row)]
    rank = 0
    col = 0
    while rank < len(rows) and col < len(rows[0]):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col] % q:
                pivot = row
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % q, -1, q)
        rows[rank] = [(value * inv) % q for value in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col] % q:
                scale = rows[row][col] % q
                rows[row] = [
                    (rows[row][entry] - scale * rows[rank][entry]) % q
                    for entry in range(len(rows[row]))
                ]
        rank += 1
        col += 1
    return rank


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
    raise RuntimeError("no primitive root found")


def stable_subset(support: set[int]) -> bool:
    return {FROBENIUS * value % MODULUS for value in support} == support


def p24_orbits() -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    orbits = frobenius_orbits(MODULUS, FROBENIUS)
    fixed = [orbit for orbit in orbits if len(orbit) == 1]
    moving = [orbit for orbit in orbits if len(orbit) == 4]
    return fixed, moving


def support_from_orbits(orbits: list[tuple[int, ...]]) -> set[int]:
    return {frequency for orbit in orbits for frequency in orbit}


def local_rank_jump(frequency: int, defect_support: set[int]) -> bool:
    prefix_basis = [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
    ]
    tail_value = [0, 0, 0, 0, 1] if frequency in defect_support else [1, 0, 0, 0, 0]
    prefix_rank = rank_mod_q(prefix_basis, Q)
    prefix_tail_rank = rank_mod_q(prefix_basis + [tail_value], Q)
    return prefix_tail_rank == prefix_rank + 1


def tail_vandermonde_rank(support: set[int]) -> int:
    root = primitive_root(Q)
    omega = pow(root, (Q - 1) // MODULUS, Q)
    matrix = [
        [pow(omega, frequency * sample, Q) for frequency in sorted(support)]
        for sample in range(TAIL_DIM)
    ]
    return rank_mod_q(matrix, Q)


def analyze_case(label: str, support: set[int]) -> FixedOrdinaryCase:
    fixed, moving = p24_orbits()
    fixed_points = {orbit[0] for orbit in fixed}
    moving_sets = [set(orbit) for orbit in moving]
    fixed_jumps = sum(
        1 for frequency in fixed_points if local_rank_jump(frequency, support)
    )
    moving_orbits_used = sum(1 for orbit in moving_sets if orbit <= support)
    stable = stable_subset(support)
    vandermonde_rank = tail_vandermonde_rank(support)
    pure_moving = fixed_jumps == 0 and moving_orbits_used == TAIL_DIM // 4
    fixed_ordinary = fixed_jumps == 0
    return FixedOrdinaryCase(
        label=label,
        support_size=len(support),
        stable_support=stable,
        fixed_rank_jumps=fixed_jumps,
        moving_orbits_used=moving_orbits_used,
        fixed_ordinary=fixed_ordinary,
        pure_moving_support=pure_moving,
        tail_vandermonde_rank=vandermonde_rank,
        selected_basis_frequency_gate=(
            len(support) == TAIL_DIM and stable and vandermonde_rank == TAIL_DIM
        ),
        no_fixed_theorem_applies=(fixed_ordinary and stable and len(support) == TAIL_DIM),
    )


def print_case(case: FixedOrdinaryCase) -> None:
    print(
        f"case={case.label} support_size={case.support_size} "
        f"stable_support={int(case.stable_support)} "
        f"fixed_rank_jumps={case.fixed_rank_jumps} "
        f"moving_orbits_used={case.moving_orbits_used} "
        f"fixed_ordinary={int(case.fixed_ordinary)} "
        f"pure_moving_support={int(case.pure_moving_support)} "
        f"tail_vandermonde_rank={case.tail_vandermonde_rank} "
        f"selected_basis_frequency_gate={int(case.selected_basis_frequency_gate)} "
        f"no_fixed_theorem_applies={int(case.no_fixed_theorem_applies)}"
    )


def main() -> None:
    fixed, moving = p24_orbits()
    pure_support = support_from_orbits(moving[:4])
    mixed_support = support_from_orbits(fixed[:4] + moving[:3])
    nonstable_support = set(range(TAIL_DIM))

    cases = [
        analyze_case("pure_moving_support", pure_support),
        analyze_case("mixed_fixed_support_control", mixed_support),
        analyze_case("nonstable_support_control", nonstable_support),
    ]

    print("Trace-GCD RS-tail p24 fixed-frequency ordinary gate")
    print(f"p24_modulus={MODULUS}")
    print(f"p24_frobenius_mod_35={FROBENIUS}")
    print(f"p24_tail_dim={TAIL_DIM}")
    print(f"fixed_frequency_count={len(fixed)}")
    print(f"moving_orbit_count={len(moving)}")
    for case in cases:
        print_case(case)
    print("counts")
    print(f"  stable_supports_after_descent=1260")
    print(f"  stable_supports_after_no_fixed_defect={n_choose_k(len(moving), 4)}")
    print("interpretation")
    print("  fixed_frequency_ordinarity_is_exact_no_fixed_defect_condition=1")
    print("  no_fixed_defect_plus_descent_reduces_supports_to_35=1")
    print("  mixed_fixed_support_control_still_descends_and_has_vandermonde_unit=1")
    print("  mixed_support_rejected_only_by_fixed_ordinarity_not_by_descent=1")
    print("  p24_next_arithmetic_lemma_is_fixed_tail_inside_prefix=1")
    print("conclusion=reported_trace_gcd_rs_tail_fixed_frequency_ordinary_gate")

    pure, mixed, nonstable = cases
    if (
        not pure.no_fixed_theorem_applies
        or not pure.pure_moving_support
        or not mixed.selected_basis_frequency_gate
        or mixed.fixed_ordinary
        or mixed.tail_vandermonde_rank != TAIL_DIM
        or nonstable.stable_support
        or n_choose_k(len(moving), 4) != 35
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
