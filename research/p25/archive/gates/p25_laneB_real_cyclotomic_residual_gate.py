#!/usr/bin/env python3
"""Real-cyclotomic residual gate for the p25 Lane B anchor.

After the punctured Hasse-Davenport gate, a future producer still has to
certify the single reduced-anchor residual.  This gate ports the p24
cyclotomic-divisor / diamond-norm bookkeeping to the p25 prime C-axes.

For prime c, the denominator-cleared residual is

    D_c = sum_{k != 0} [zeta_c^k] - (c - 1)[1],

the diamond norm of the one-point divisor [zeta_c] - [1].  Over F_p the
real-cyclotomic quotient splits according to Frobenius orbits on
(Z/cZ)^*/{+-1}.  For p25 and c in {13,53}, this gives two small components.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


P25 = 10**25 + 13


@dataclass(frozen=True)
class ResidualCase:
    name: str
    c_axis: int


CASES = (
    ResidualCase("tiny_C3xC13", 13),
    ResidualCase("prime_axis_C3xC53", 53),
)


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(modulus: int) -> int:
    factors = factor_distinct(modulus - 1)
    for candidate in range(2, modulus):
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root")


def single_divisor(c_axis: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_axis)
    values[0] = (-1) % modulus
    values[1] = 1
    return values


def diamond_action(values: list[int], c_axis: int, multiplier: int) -> list[int]:
    out = [0] * len(values)
    for right in range(RIGHT_DEGREE):
        for c_index in range(c_axis):
            target = (multiplier * c_index) % c_axis
            out[right * c_axis + target] = values[right * c_axis + c_index]
    return out


def add(left: list[int], right: list[int], modulus: int) -> list[int]:
    return [(a + b) % modulus for a, b in zip(left, right)]


def diamond_norm_divisor(c_axis: int, modulus: int) -> list[int]:
    total = [0] * (RIGHT_DEGREE * c_axis)
    base = single_divisor(c_axis, modulus)
    for multiplier in range(1, c_axis):
        total = add(total, diamond_action(base, c_axis, multiplier), modulus)
    return total


def formal_residual_divisor(c_axis: int, modulus: int) -> list[int]:
    values = [0] * (RIGHT_DEGREE * c_axis)
    values[0] = (-(c_axis - 1)) % modulus
    for c_index in range(1, c_axis):
        values[c_index] = 1
    return values


def dft(values: list[int], c_axis: int, modulus: int) -> list[int]:
    root = primitive_root(modulus)
    zeta_r = pow(root, (modulus - 1) // RIGHT_DEGREE, modulus)
    zeta_c = pow(root, (modulus - 1) // c_axis, modulus)
    coeffs: list[int] = []
    for a_freq in range(RIGHT_DEGREE):
        for b_freq in range(c_axis):
            total = 0
            for right in range(RIGHT_DEGREE):
                for c_index in range(c_axis):
                    total += (
                        values[right * c_axis + c_index]
                        * pow(zeta_r, a_freq * right, modulus)
                        * pow(zeta_c, b_freq * c_index, modulus)
                    )
            coeffs.append(total % modulus)
    return coeffs


def fourier_profile(values: list[int], c_axis: int, modulus: int) -> dict[str, int]:
    coeffs = dft(values, c_axis, modulus)
    profile = {
        "nonzero": 0,
        "right_nontrivial_c_zero": 0,
        "right_zero_c_nonzero": 0,
        "mixed": 0,
    }
    for a_freq in range(RIGHT_DEGREE):
        for b_freq in range(c_axis):
            value = coeffs[a_freq * c_axis + b_freq]
            if value == 0:
                continue
            profile["nonzero"] += 1
            if a_freq != 0 and b_freq == 0:
                profile["right_nontrivial_c_zero"] += 1
            elif a_freq == 0 and b_freq != 0:
                profile["right_zero_c_nonzero"] += 1
            elif a_freq != 0 and b_freq != 0:
                profile["mixed"] += 1
    return profile


def real_pair(value: int, c_axis: int) -> int:
    value %= c_axis
    return min(value, (-value) % c_axis)


def real_frobenius_orbits(c_axis: int) -> list[list[int]]:
    remaining = {real_pair(value, c_axis) for value in range(1, c_axis)}
    multiplier = P25 % c_axis
    orbits: list[list[int]] = []
    while remaining:
        start = min(remaining)
        orbit: list[int] = []
        current = start
        while current in remaining:
            remaining.remove(current)
            orbit.append(current)
            current = real_pair(current * multiplier, c_axis)
        orbits.append(orbit)
    return orbits


def multiplicative_order(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise ValueError("value is not a unit")
    order = 1
    residue = value % modulus
    while residue != 1:
        residue = residue * value % modulus
        order += 1
    return order


def audit_case(case: ResidualCase) -> tuple[list[str], bool]:
    c_axis = case.c_axis
    modulus = split_prime_for(RIGHT_DEGREE * c_axis)
    norm_divisor = diamond_norm_divisor(c_axis, modulus)
    expected_divisor = formal_residual_divisor(c_axis, modulus)
    profile = fourier_profile(norm_divisor, c_axis, modulus)
    orbits = real_frobenius_orbits(c_axis)
    orbit_lengths = sorted(len(orbit) for orbit in orbits)
    real_degree = (c_axis - 1) // 2
    p_order_mod_c = multiplicative_order(P25 % c_axis, c_axis)
    p_order_mod_3c = multiplicative_order(P25 % (RIGHT_DEGREE * c_axis), RIGHT_DEGREE * c_axis)

    divisor_ok = norm_divisor == expected_divisor
    degree_zero_ok = sum(norm_divisor) % modulus == 0
    profile_ok = (
        profile["nonzero"] == RIGHT_DEGREE * (c_axis - 1)
        and profile["right_nontrivial_c_zero"] == 0
        and profile["right_zero_c_nonzero"] == c_axis - 1
        and profile["mixed"] == (RIGHT_DEGREE - 1) * (c_axis - 1)
    )
    real_orbit_ok = (
        len(orbits) == 2
        and sum(orbit_lengths) == real_degree
        and len(set(orbit_lengths)) == 1
    )
    no_mu_c_in_fp = gcd(c_axis, P25 - 1) == 1
    plain_frobenius_mismatch = p_order_mod_3c < RIGHT_DEGREE * c_axis
    ok = (
        divisor_ok
        and degree_zero_ok
        and profile_ok
        and real_orbit_ok
        and no_mu_c_in_fp
        and plain_frobenius_mismatch
    )
    lines = [
        (
            f"case {case.name}: c={c_axis} modulus={modulus} "
            f"diamond_orbit_size={c_axis - 1} "
            f"divisor_norm_ok={int(divisor_ok)} "
            f"degree_zero_ok={int(degree_zero_ok)} "
            f"fourier_profile={profile} "
            f"fourier_profile_ok={int(profile_ok)} "
            f"p_mod_c={P25 % c_axis} p_order_mod_c={p_order_mod_c} "
            f"p_order_mod_3c={p_order_mod_3c} "
            f"mu_c_in_Fp={int(not no_mu_c_in_fp)} "
            f"plain_cyclotomic_realizes_full_quotient={int(not plain_frobenius_mismatch)} "
            f"real_cyclotomic_degree={real_degree} "
            f"real_frobenius_orbit_lengths={orbit_lengths} "
            f"real_component_count={len(orbits)} "
            f"real_orbit_ok={int(real_orbit_ok)} "
            f"ok={int(ok)}"
        )
    ]
    return lines, ok


def main() -> int:
    print("p25 Lane B real-cyclotomic residual gate")
    print(f"p={P25}")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"real_cyclotomic_residual_rows={ok_rows}/{len(CASES)}")
    print("interpretation")
    print("  reduced_anchor_residual_is_diamond_norm_of_one_point_divisor=1")
    print("  residual_has_expected_degree_zero_fourier_profile=1")
    print("  p25_real_residual_splits_into_two_equal_frobenius_components=1")
    print("  post_producer_check_can_use_two_small_real_cyclotomic_resultants=1")
    print("  this_is_not_the_missing_cm_artin_pullback_producer=1")
    print("conclusion=reported_p25_laneB_real_cyclotomic_residual_gate")
    return 0 if ok_rows == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
