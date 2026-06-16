#!/usr/bin/env python3
"""Audit the p24 unit-2 action on right Frobenius orbits.

This is finite bookkeeping for a possible producer-theorem compression.  The
arithmetic theorem would still have to prove that multiplication by 2 carries
the actual trace-GCD determinant-line/Fitting section to the corresponding
deleted-row section up to p-units.
"""

from __future__ import annotations


P = 10**24 + 7
RIGHT = 211
UNIT = 2


def frobenius_orbits(multiplier: int, modulus: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = value * multiplier % modulus
        out.append(orbit)
    return out


def orbit_index_of(value: int, orbits: list[list[int]]) -> int:
    for index, orbit in enumerate(orbits):
        if value in orbit:
            return index
    raise ValueError(value)


def cycle_from_mapping(mapping: dict[int, int], start: int) -> list[int]:
    out: list[int] = []
    value = start
    while value not in out:
        out.append(value)
        value = mapping[value]
    return out


def main() -> None:
    multiplier = P % RIGHT
    orbits = frobenius_orbits(multiplier, RIGHT)
    mapping = {
        index: orbit_index_of((UNIT * orbit[0]) % RIGHT, orbits)
        for index, orbit in enumerate(orbits)
    }
    nonzero_cycle = cycle_from_mapping(mapping, 1)
    fixed_zero = mapping[0] == 0
    covers_nonzero = sorted(nonzero_cycle) == list(range(1, len(orbits)))

    print("trace-GCD p24 unit-2 orbit-compression audit")
    print(f"p={P}")
    print(f"right={RIGHT}")
    print(f"frobenius_multiplier={multiplier}")
    print(f"unit={UNIT}")
    print(f"orbit_count={len(orbits)}")
    print(f"orbit_lengths={[len(orbit) for orbit in orbits]}")
    print(f"unit_action_mapping={mapping}")
    print(f"zero_orbit_fixed={int(fixed_zero)}")
    print(f"nonzero_cycle={nonzero_cycle}")
    print(f"nonzero_cycle_length={len(nonzero_cycle)}")
    print(f"nonzero_cycle_covers_all_nonzero_orbits={int(covers_nonzero)}")
    print("conditional_compression")
    print("  if determinant-line sections are unit-2 equivariant up to p-units,")
    print("  one nonzero representative orbit norm plus the fixed orbit norm")
    print("  propagates to all six nonzero deletion/orbit rows.")
    print("  without that arithmetic equivariance theorem, check all seven orbit norms.")
    print("conclusion=reported_trace_gcd_unit2_orbit_compression")


if __name__ == "__main__":
    main()
