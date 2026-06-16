#!/usr/bin/env python3
"""C-axis Fourier payload gate for p25 Lane B.

The right-eigenbasis gate turns the mixed module into two nontrivial right
character eigenvectors E_1 and E_2, each a vector on the C-axis.  This gate asks
how much C-axis character payload those vectors actually require.

For every admissible packet in the prime-axis labs, and representative packets
on C_169, each E_i has zero mean but nonzero projection to every nontrivial
C-axis Fourier character.  So the producer cannot be a one-component,
low-frequency, or orbit-sparse C-axis object; after the right-character split it
has to supply a full nontrivial C-character payload, twice.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_literal_jacobi_packet_model import (
    admissible_pairs,
    representative_pairs,
)
from p25_laneB_mixed_character_module_gate import decompose_packet
from p25_laneB_right_eigenbasis_gate import right_eigenvectors
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


P25 = 10**25 + 13


@dataclass(frozen=True)
class FourierCase:
    name: str
    c_axis: int
    exhaustive: bool


CASES = (
    FourierCase("tiny_C3xC13", 13, True),
    FourierCase("prime_axis_C3xC53", 53, True),
    FourierCase("square_axis_C3xC169", 169, False),
)


def c_root_powers(c_axis: int, modulus: int) -> list[list[int]]:
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // c_axis, modulus)
    if zeta == 1 or pow(zeta, c_axis, modulus) != 1:
        raise AssertionError("bad C-axis root")
    return [
        [pow(zeta, frequency * index, modulus) for index in range(c_axis)]
        for frequency in range(c_axis)
    ]


def c_fourier_support(
    vector: list[int], powers: list[list[int]], modulus: int
) -> set[int]:
    support: set[int] = set()
    for frequency, row in enumerate(powers):
        total = sum(value * root_power for value, root_power in zip(vector, row))
        if total % modulus:
            support.add(frequency)
    return support


def coordinate_support(vector: list[int], modulus: int) -> int:
    return sum(1 for value in vector if value % modulus)


def real_pair(value: int, c_axis: int) -> int:
    value %= c_axis
    return min(value, (-value) % c_axis)


def real_pairs_from_support(support: set[int], c_axis: int) -> set[int]:
    return {real_pair(value, c_axis) for value in support if value % c_axis}


def real_frobenius_orbits(c_axis: int) -> list[list[int]]:
    remaining = {real_pair(value, c_axis) for value in range(1, c_axis)}
    multiplier = P25 % c_axis
    orbits: list[list[int]] = []
    while remaining:
        start = min(remaining)
        current = start
        orbit: list[int] = []
        while current in remaining:
            remaining.remove(current)
            orbit.append(current)
            current = real_pair(current * multiplier, c_axis)
        orbits.append(orbit)
    return orbits


def covers_real_orbits(
    support: set[int], c_axis: int, orbits: list[list[int]]
) -> bool:
    real_support = real_pairs_from_support(support, c_axis)
    return all(set(orbit) <= real_support for orbit in orbits)


def audit_case(case: FourierCase) -> tuple[list[str], bool]:
    modulus = split_prime_for(RIGHT_DEGREE * case.c_axis)
    pairs = (
        admissible_pairs(case.c_axis)
        if case.exhaustive
        else representative_pairs(case.c_axis)
    )
    powers = c_root_powers(case.c_axis, modulus)
    full_nontrivial_support = set(range(1, case.c_axis))
    orbits = real_frobenius_orbits(case.c_axis)

    zero_mean_hits = 0
    full_support_hits = 0
    same_fourier_support_hits = 0
    real_pair_coverage_hits = 0
    frobenius_component_coverage_hits = 0
    coordinate_support_counts: dict[tuple[int, int], int] = {}
    c_fourier_support_counts: dict[tuple[int, int], int] = {}
    canonical_summary: str | None = None

    for u_value, v_value in pairs:
        _matrix, _pure_c, mixed = decompose_packet(
            case.c_axis, modulus, u_value, v_value
        )
        _eigen_0, eigen_1, eigen_2 = right_eigenvectors(
            mixed, case.c_axis, modulus
        )
        support_1 = c_fourier_support(eigen_1, powers, modulus)
        support_2 = c_fourier_support(eigen_2, powers, modulus)
        coordinate_pair = (
            coordinate_support(eigen_1, modulus),
            coordinate_support(eigen_2, modulus),
        )
        fourier_pair = (len(support_1), len(support_2))

        zero_mean_hits += int(0 not in support_1 and 0 not in support_2)
        full_support_hits += int(
            support_1 == full_nontrivial_support
            and support_2 == full_nontrivial_support
        )
        same_fourier_support_hits += int(support_1 == support_2)
        real_pair_coverage_hits += int(
            real_pairs_from_support(support_1, case.c_axis)
            == set(range(1, (case.c_axis + 1) // 2))
            and real_pairs_from_support(support_2, case.c_axis)
            == set(range(1, (case.c_axis + 1) // 2))
        )
        frobenius_component_coverage_hits += int(
            covers_real_orbits(support_1, case.c_axis, orbits)
            and covers_real_orbits(support_2, case.c_axis, orbits)
        )
        coordinate_support_counts[coordinate_pair] = (
            coordinate_support_counts.get(coordinate_pair, 0) + 1
        )
        c_fourier_support_counts[fourier_pair] = (
            c_fourier_support_counts.get(fourier_pair, 0) + 1
        )

        if u_value == RIGHT_DEGREE and v_value == 1:
            canonical_summary = (
                f"canonical_theta_3_1: coordinate_support_pair={coordinate_pair} "
                f"c_fourier_support_pair={fourier_pair} "
                f"real_component_count={len(orbits)} "
                f"real_orbit_lengths={[len(orbit) for orbit in orbits]}"
            )

    pair_count = len(pairs)
    row_ok = (
        zero_mean_hits == pair_count
        and full_support_hits == pair_count
        and same_fourier_support_hits == pair_count
        and real_pair_coverage_hits == pair_count
        and frobenius_component_coverage_hits == pair_count
        and canonical_summary is not None
    )

    lines = [
        (
            f"case {case.name}: c={case.c_axis} modulus={modulus} "
            f"pairs_checked={pair_count} exhaustive={int(case.exhaustive)} "
            f"zero_mean_hits={zero_mean_hits}/{pair_count} "
            f"full_nontrivial_c_fourier_hits={full_support_hits}/{pair_count} "
            f"same_fourier_support_hits={same_fourier_support_hits}/{pair_count} "
            f"real_pair_coverage_hits={real_pair_coverage_hits}/{pair_count} "
            f"frobenius_component_coverage_hits={frobenius_component_coverage_hits}/{pair_count} "
            f"real_component_count={len(orbits)} "
            f"real_orbit_lengths={[len(orbit) for orbit in orbits]} "
            f"ok={int(row_ok)}"
        ),
        f"  coordinate_support_counts={dict(sorted(coordinate_support_counts.items()))}",
        f"  c_fourier_support_counts={dict(sorted(c_fourier_support_counts.items()))}",
        f"  {canonical_summary}",
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B C-axis Fourier payload gate")
    print(f"p={P25}")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"c_axis_fourier_payload_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  right_eigenvectors_have_zero_C_mean=1")
    print("  each_right_eigenvector_uses_every_nontrivial_C_axis_character=1")
    print("  producer_cannot_be_low_frequency_or_single_real_component_on_C_axis=1")
    print("  producer_must_supply_full_nontrivial_C_character_payload_twice=1")
    print("conclusion=reported_p25_laneB_c_axis_fourier_payload_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
