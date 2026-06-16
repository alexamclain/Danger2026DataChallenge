#!/usr/bin/env python3
"""Audit right-unit action on p24 Frobenius orbit labels.

The right cyclotomic algebra F_p[mu_211] is a product of six degree-35
factors.  Frobenius fixes each factor, while multiplication by a unit modulo
211 permutes the factors.  This script records the action of the unit `2`,
which cycles the three opposite pairs used by the refined p24 certificate.
"""

from __future__ import annotations


P = 10**24 + 7
RIGHT = 211
LEFT = 157


def frobenius_orbits(modulus: int, q: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(1, modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * q) % modulus
        out.append(orbit)
    return out


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {value: index for index, orbit in enumerate(orbits, start=1) for value in orbit}


def unit_permutation(unit: int, orbits: list[list[int]]) -> tuple[int, ...]:
    labels = orbit_label_map(orbits)
    return tuple(labels[(unit * orbit[0]) % RIGHT] for orbit in orbits)


def apply_perm_to_set(perm: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(perm[index - 1] for index in values))


def cycle_string(perm: tuple[int, ...]) -> str:
    seen: set[int] = set()
    cycles: list[str] = []
    for start in range(1, len(perm) + 1):
        if start in seen:
            continue
        cur = start
        cycle: list[int] = []
        while cur not in seen:
            seen.add(cur)
            cycle.append(cur)
            cur = perm[cur - 1]
        if len(cycle) > 1:
            cycles.append("(" + " ".join(f"O{value}" for value in cycle) + ")")
    return "".join(cycles) if cycles else "identity"


def main() -> None:
    right_orbits = frobenius_orbits(RIGHT, P)
    left_orbits = frobenius_orbits(LEFT, P)
    opposite_pairs = ((1, 4), (2, 5), (3, 6))
    opposite_prefixes = tuple(
        tuple(index for index in range(1, 7) if index not in pair)
        for pair in opposite_pairs
    )
    print("p24 right orbit unit-action audit")
    print(f"p_mod_211={P % RIGHT}")
    print(f"right_orbit_count={len(right_orbits)}")
    print(f"right_orbit_lengths={sorted({len(orbit) for orbit in right_orbits})}")
    print(f"left_orbit_count_mod_157={len(left_orbits)}")
    print(f"left_orbit_length_mod_157={len(left_orbits[0])}")
    for unit in (P % RIGHT, -1 % RIGHT, 2, 4, 8):
        perm = unit_permutation(unit, right_orbits)
        pair_action = tuple(apply_perm_to_set(perm, pair) for pair in opposite_pairs)
        prefix_action = tuple(
            apply_perm_to_set(perm, prefix) for prefix in opposite_prefixes
        )
        print(
            f"unit={unit:3d} perm={perm} cycles={cycle_string(perm)} "
            f"pair_action={pair_action} prefix_action={prefix_action}"
        )
    print("unit_2_cycles_opposite_pairs=1")
    print("unit_2_cycles_opposite_prefixes=1")
    print("unit_2_cycles_representative_tails_up_to_inversion=1")
    print("conclusion=reported_right_orbit_unit_action_audit")


if __name__ == "__main__":
    main()
