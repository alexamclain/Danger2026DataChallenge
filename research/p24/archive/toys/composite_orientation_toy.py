#!/usr/bin/env python3
"""Toy model for composite-correspondence orientation loss.

For D=-5000 the norm-3 ideal generates the class group of order 30.  The split
prime logs include

    log(3) = 1,  log(17) = 7.

The oriented product 3 * 17^(-1) has log -6 = 24, hence index 6 and order 5.
But an unoriented X0(3*17) correspondence sees all sign choices

    +/-log(3) +/-log(17) = {8, 24, 6, 22}.

Those moves generate the index-2 subgroup, not the desired index-6 subgroup.
Thus forgetting orientation replaces six 5-cycles by two 15-vertex components.

This is the small analogue of the p24 composite target
2 * 463 * 223^(-1), where the desired index is 66254 but the unoriented
X0(206498) sign choices generate only index 2.
"""

from __future__ import annotations

import itertools
import math

H = 30
LOGS = {3: 1, 17: 7}
DESIRED = {3: 1, 17: -1}


def subgroup_index(moves: list[int]) -> int:
    g = H
    for move in moves:
        g = math.gcd(g, move)
    return g


def orbit(start: int, moves: list[int]) -> set[int]:
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for move in moves:
            nxt = (current + move) % H
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def orbit_partition(moves: list[int]) -> list[set[int]]:
    remaining = set(range(H))
    out: list[set[int]] = []
    while remaining:
        start = min(remaining)
        comp = orbit(start, moves)
        out.append(comp)
        remaining -= comp
    return out


def main() -> None:
    sign_rows = []
    for signs in itertools.product((1, -1), repeat=len(LOGS)):
        signed = dict(zip(LOGS, signs))
        move = sum(signed[ell] * LOGS[ell] for ell in LOGS) % H
        index = math.gcd(H, move)
        order = H // index
        signed_factors = tuple(signed[ell] * ell for ell in LOGS)
        sign_rows.append((signed_factors, move, index, order))

    desired_tuple = tuple(DESIRED[ell] * ell for ell in LOGS)
    desired_move = next(row[1] for row in sign_rows if row[0] == desired_tuple)
    all_moves = [row[1] for row in sign_rows]
    oriented_components = orbit_partition([desired_move])
    unoriented_components = orbit_partition(all_moves)

    print("composite orientation toy")
    print("D=-5000")
    print(f"class_number={H}")
    print(f"logs={LOGS}")
    print(f"desired_signed_factors={desired_tuple}")
    print()
    print("sign_choices")
    print("  signed_factors move index order")
    for signed_factors, move, index, order in sorted(sign_rows, key=lambda row: (row[2], row[0])):
        marker = " desired" if signed_factors == desired_tuple else ""
        print(f"  {signed_factors!s:10s} {move:4d} {index:5d} {order:5d}{marker}")
    print()
    print("components")
    print(f"  oriented_move={desired_move}")
    print(f"  oriented_component_count={len(oriented_components)}")
    print(f"  oriented_component_sizes={sorted({len(c) for c in oriented_components})}")
    print(f"  unoriented_subgroup_index={subgroup_index(all_moves)}")
    print(f"  unoriented_component_count={len(unoriented_components)}")
    print(f"  unoriented_component_sizes={sorted({len(c) for c in unoriented_components})}")
    print()
    print("interpretation")
    print("  oriented_composite_cycle_has_desired_index=1")
    print("  plain_unoriented_X0_product_merges_desired_cycles=1")
    print("  orientation_selector_is_still_required=1")
    print("conclusion=composite_norm_savings_do_not_bypass_orientation_or_period_selection")


if __name__ == "__main__":
    main()
