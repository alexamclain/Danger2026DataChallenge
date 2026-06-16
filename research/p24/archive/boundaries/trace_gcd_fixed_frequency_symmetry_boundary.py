#!/usr/bin/env python3
"""Boundary test for easy fixed-frequency symmetry explanations.

The six right Frobenius orbits modulo 211 are the type-6 Gaussian cosets for
the p24 right field.  The fixed-frequency no-defect theorem asks, after the
length-35 orbit DFT, for the orbit containing 1 to lie in the span of the
four selected orbits, at the seven frequencies fixed by p on Z/35Z.

This script checks a deliberately generous generic model:

* the right profile is centered, so the sum over nonzero right frequencies is
  zero;
* the profile is sign-symmetric, f(s)=f(-s), which is stronger than the
  formal pairing one would try to extract from Hermitian symmetry.

Even with those constraints, the orbit-1 DFT functional is forced by the four
selected orbit functionals only at the trivial fixed frequency a=0.  The six
nontrivial order-7 fixed frequencies need extra arithmetic from the actual
CM/Lang packet.
"""

from __future__ import annotations


P24 = 10**24 + 7
RIGHT = 211
Q = 29
SELECTED_ORBITS = (2, 3, 5, 6)


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


def rank_mod_q(rows: list[list[int]], q: int) -> int:
    matrix = [[value % q for value in row] for row in rows if any(value % q for value in row)]
    if not matrix:
        return 0
    row_count = len(matrix)
    col_count = len(matrix[0])
    rank = 0
    for col in range(col_count):
        pivot = next((row for row in range(rank, row_count) if matrix[row][col] % q), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col] % q, -1, q)
        matrix[rank] = [value * inv % q for value in matrix[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            scale = matrix[row][col] % q
            if scale:
                matrix[row] = [
                    (value - scale * pivot_value) % q
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def right_orbits() -> list[list[int]]:
    multiplier = P24 % RIGHT
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(1, RIGHT):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = value * multiplier % RIGHT
        orbits.append(orbit)
    return orbits


def sign_pair_index() -> dict[int, int]:
    pairs: dict[int, int] = {}
    for value in range(1, RIGHT):
        if value in pairs:
            continue
        index = len({pair for pair in pairs.values()})
        pairs[value] = index
        pairs[(-value) % RIGHT] = index
    return pairs


def fixed_frequency_functional(
    orbit_label: int,
    fixed_index: int,
    orbits: list[list[int]],
    pairs: dict[int, int],
    zeta7: int,
) -> list[int]:
    """Orbit DFT functional on centered/sign-symmetric right profiles."""

    row = [0] * ((RIGHT - 1) // 2)
    for orbit_position, value in enumerate(orbits[orbit_label - 1]):
        coeff = pow(zeta7, (-fixed_index * orbit_position) % 7, Q)
        row[pairs[value]] = (row[pairs[value]] + coeff) % Q
    return row


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {value: index + 1 for index, orbit in enumerate(orbits) for value in orbit}


def main() -> None:
    orbits = right_orbits()
    pairs = sign_pair_index()
    zeta7 = pow(primitive_root(Q), (Q - 1) // 7, Q)
    labels = orbit_label_map(orbits)
    gaussian_coset = []
    value = 1
    generator = pow(2, 35, RIGHT)
    for _ in range(6):
        gaussian_coset.append(value)
        value = value * generator % RIGHT

    center_constraint = [2 % Q] * ((RIGHT - 1) // 2)
    rows = []
    for fixed_index in range(7):
        selected = [
            fixed_frequency_functional(label, fixed_index, orbits, pairs, zeta7)
            for label in SELECTED_ORBITS
        ]
        target = fixed_frequency_functional(1, fixed_index, orbits, pairs, zeta7)
        rank_without_target = rank_mod_q(selected + [center_constraint], Q)
        rank_with_target = rank_mod_q(selected + [center_constraint, target], Q)
        rows.append((fixed_index, 5 * fixed_index % 35, rank_without_target, rank_with_target))

    print("Trace-GCD fixed-frequency symmetry boundary")
    print(f"q={Q}")
    print(f"p24_p_mod_211={P24 % RIGHT}")
    print(f"right_orbit_count={len(orbits)}")
    print(f"right_orbit_lengths={sorted({len(orbit) for orbit in orbits})}")
    print(f"gaussian_coset={gaussian_coset}")
    print(
        "gaussian_coset_orbit_labels="
        f"{[(value, labels[value]) for value in gaussian_coset]}"
    )
    print(
        "negation_orbit_labels="
        f"{[(label, labels[(-orbits[label - 1][0]) % RIGHT]) for label in range(1, 7)]}"
    )
    for fixed_index, frequency, rank_without, rank_with in rows:
        print(
            f"fixed_index={fixed_index} frequency={frequency} "
            f"forced_by_centering_and_sign_symmetry={int(rank_without == rank_with)} "
            f"rank_without_target={rank_without} rank_with_target={rank_with}"
        )
    nontrivial_forced = sum(
        1 for fixed_index, _frequency, rank_without, rank_with in rows[1:]
        if rank_without == rank_with
    )
    print("interpretation")
    print("  orbit_containing_minus_one_is_the_omitted_full_block=1")
    print("  centering_plus_sign_symmetry_forces_only_trivial_fixed_frequency=1")
    print("  nontrivial_order7_fixed_frequencies_need_extra_cm_lang_arithmetic=1")
    print("  easy_right_orbit_symmetry_is_not_the_missing_cyclic_syzygy=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_symmetry_boundary")

    if rows[0][2] != rows[0][3]:
        raise SystemExit("trivial fixed frequency should be forced")
    if nontrivial_forced != 0:
        raise SystemExit("nontrivial fixed frequencies should not be forced")


if __name__ == "__main__":
    main()
