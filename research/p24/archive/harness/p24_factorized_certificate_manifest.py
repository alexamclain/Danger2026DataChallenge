#!/usr/bin/env python3
"""Print the explicit p24 factorized mixed certificate manifest.

This is deliberately arithmetic-light: it names the six right Frobenius
orbits, the four full prefix blocks, and the 16-coordinate tail block used in
the current B_j/T_j p-unit target.
"""

from __future__ import annotations


P = 10**24 + 7
LEFT = 157
RIGHT = 211
LEFT_DIM = 156
RIGHT_DIM = 35
PREFIX_BLOCKS = LEFT_DIM // RIGHT_DIM
TAIL_LEN = LEFT_DIM - PREFIX_BLOCKS * RIGHT_DIM


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


def orbit_labels(indices: tuple[int, ...] | list[int]) -> list[str]:
    return ["O" + str(index) for index in indices]


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {
        value: index
        for index, orbit in enumerate(orbits, start=1)
        for value in orbit
    }


def unit_permutation(unit: int, right_orbits: list[list[int]]) -> tuple[int, ...]:
    labels = orbit_label_map(right_orbits)
    return tuple(
        labels[(unit * orbit[0]) % RIGHT]
        for orbit in right_orbits
    )


def apply_permutation(perm: tuple[int, ...], index: int) -> int:
    return perm[index - 1]


def multiply_window(unit: int, window: list[int]) -> list[int]:
    return [(unit * value) % RIGHT for value in window]


def print_paired_certificate(
    name: str,
    pairs: list[tuple[int, int]],
    right_orbits: list[list[int]],
    negation_aligned_tails: bool = False,
) -> None:
    print(name)
    paired_prefixes: dict[tuple[int, ...], list[str]] = {}
    for left, right in pairs:
        prefix = tuple(
            index
            for index in range(1, len(right_orbits) + 1)
            if index not in (left, right)
        )
        if negation_aligned_tails:
            tail_windows = {
                left: right_orbits[left - 1][:TAIL_LEN],
                right: [(-value) % RIGHT for value in right_orbits[left - 1][:TAIL_LEN]],
            }
        else:
            tail_windows = {
                left: right_orbits[left - 1][:TAIL_LEN],
                right: right_orbits[right - 1][:TAIL_LEN],
            }
        for deleted, tail in ((left, right), (right, left)):
            paired_prefixes.setdefault(prefix, []).append(
                f"delete_O{deleted}_tail_O{tail}"
            )
            tail_freqs = tail_windows[tail]
            tail_positions = [
                right_orbits[tail - 1].index(value) for value in tail_freqs
            ]
            print(
                f"  deleted=O{deleted} "
                f"B_prefix={orbit_labels(prefix)} "
                f"T_tail=O{tail} "
                f"tail_window_{TAIL_LEN}={tail_freqs} "
                f"tail_positions_in_natural_order={tail_positions}"
            )
    print(f"{name}_distinct_B_prefix_count={len(paired_prefixes)}")
    print(f"{name}_tail_factor_count={len(right_orbits)}")


def print_equivariant_representative_certificate(
    right_orbits: list[list[int]],
) -> None:
    print("equivariant_1B1T_representative_certificate")
    unit = 2
    unit_perm = unit_permutation(unit, right_orbits)
    representative_deleted = 4
    representative_tail = 1
    representative_prefix = tuple(
        index
        for index in range(1, len(right_orbits) + 1)
        if index not in (1, 4)
    )
    representative_window = right_orbits[representative_tail - 1][:TAIL_LEN]
    print(
        f"  representative_deleted=O{representative_deleted} "
        f"representative_B_prefix={orbit_labels(representative_prefix)} "
        f"representative_T_tail=O{representative_tail} "
        f"representative_tail_window_{TAIL_LEN}={representative_window}"
    )
    print(
        "  representative_leading_punit="
        "L_rep=B_rep*T_rep=Moore_det(prefix_140_plus_tail_16)"
    )
    deleted = representative_deleted
    tail = representative_tail
    window = representative_window
    for step in range(len(right_orbits)):
        prefix_pair = tuple(sorted((deleted, tail)))
        prefix = tuple(
            index
            for index in range(1, len(right_orbits) + 1)
            if index not in prefix_pair
        )
        positions = [right_orbits[tail - 1].index(value) for value in window]
        print(
            f"  unit2_step={step} deleted=O{deleted} "
            f"B_prefix={orbit_labels(prefix)} T_tail=O{tail} "
            f"tail_window_{TAIL_LEN}={window} "
            f"tail_positions_in_natural_order={positions}"
        )
        deleted = apply_permutation(unit_perm, deleted)
        tail = apply_permutation(unit_perm, tail)
        window = multiply_window(unit, window)
    print("equivariant_1B1T_prefix_representative_count=1")
    print("equivariant_1B1T_tail_representative_count=1")
    print("equivariant_1L_leading_representative_count=1")
    print("equivariant_1B1T_unit=2")


def main() -> None:
    left_orbits = frobenius_orbits(LEFT, P)
    right_orbits = frobenius_orbits(RIGHT, P)
    print("p24 factorized mixed certificate manifest")
    print(f"p={P}")
    print(f"p_mod_157={P % LEFT}")
    print(f"p_mod_211={P % RIGHT}")
    print(f"left_orbit_count={len(left_orbits)}")
    print(f"left_orbit_length={len(left_orbits[0]) if left_orbits else 0}")
    print(f"right_orbit_count={len(right_orbits)}")
    print(f"right_orbit_lengths={sorted({len(orbit) for orbit in right_orbits})}")
    print(f"prefix_blocks={PREFIX_BLOCKS}")
    print(f"tail_len={TAIL_LEN}")
    print(f"prefix_dim={PREFIX_BLOCKS * RIGHT_DIM}")
    print(f"leading_dim={LEFT_DIM}")
    print()
    print("right_orbits")
    for index, orbit in enumerate(right_orbits, start=1):
        print(
            f"  O{index}: rep={orbit[0]} length={len(orbit)} "
            f"freqs={orbit}"
        )
    print()
    print("factorized_certificate_rows")
    prefix_rows: dict[tuple[int, ...], list[int]] = {}
    for deleted_index in range(1, len(right_orbits) + 1):
        kept = [index for index in range(1, len(right_orbits) + 1) if index != deleted_index]
        prefix = kept[:PREFIX_BLOCKS]
        tail = kept[PREFIX_BLOCKS]
        prefix_rows.setdefault(tuple(prefix), []).append(deleted_index)
        tail_freqs = right_orbits[tail - 1][:TAIL_LEN]
        erased_tail = right_orbits[tail - 1][TAIL_LEN:]
        print(
            f"  deleted=O{deleted_index} "
            f"B_prefix={orbit_labels(prefix)} "
            f"T_tail=O{tail} "
            f"tail_first_{TAIL_LEN}={tail_freqs} "
            f"erased_tail_{RIGHT_DIM - TAIL_LEN}={erased_tail} "
            f"B_dim={PREFIX_BLOCKS * RIGHT_DIM} T_dim={TAIL_LEN}"
        )
    print()
    print("shared_prefix_factors")
    for prefix, deleted_rows in prefix_rows.items():
        print(
            f"  B_prefix={orbit_labels(prefix)} "
            f"used_by_deleted={orbit_labels(deleted_rows)}"
        )
    print(f"distinct_B_prefix_count={len(prefix_rows)}")
    print(f"tail_factor_count={len(right_orbits)}")
    print()
    print("certificate_target")
    print("  For each deleted row j:")
    print("    B_j != 0 proves the four full prefix blocks have rank 140.")
    print("    T_j != 0 proves the first 16 tail coordinates add rank 16.")
    print("    B_j*T_j != 0 proves the leading 156-coordinate Moore minor.")
    print()
    print_paired_certificate(
        "paired_minimal_B_certificate",
        [(1, 2), (3, 4), (5, 6)],
        right_orbits,
    )
    print("paired_B_lower_bound=ceil(6/2)=3")
    print()
    negation_partner = {
        index: next(
            other_index
            for other_index, orbit in enumerate(right_orbits, start=1)
            if (-right_orbits[index - 1][0]) % RIGHT in orbit
        )
        for index in range(1, len(right_orbits) + 1)
    }
    print("right_orbit_negation_partners")
    for index in range(1, len(right_orbits) + 1):
        print(f"  -O{index}=O{negation_partner[index]}")
    opposite_pairs = []
    used: set[int] = set()
    for index in range(1, len(right_orbits) + 1):
        if index in used:
            continue
        partner = negation_partner[index]
        opposite_pairs.append((index, partner))
        used.add(index)
        used.add(partner)
    print_paired_certificate(
        "opposite_symmetry_paired_certificate",
        opposite_pairs,
        right_orbits,
        negation_aligned_tails=True,
    )
    print("opposite_pairing_note=prefixes_are_stable_under_v_to_minus_v")
    print("opposite_tail_windows=Lang_coordinate_windows_stable_under_v_to_minus_v")
    print("opposite_conjugation_tail_orbit_count=3_if_CM_periods_intertwine")
    print()
    print_equivariant_representative_certificate(right_orbits)
    print("conclusion=reported_p24_factorized_certificate_manifest")


if __name__ == "__main__":
    main()
