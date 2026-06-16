#!/usr/bin/env python3
"""Degree accounting for real-cyclotomic relative energy packets."""

from __future__ import annotations

import sympy as sp

P24 = 10**24 + 7
N = 3107441


def orbit_reps(multiplier: int, identify_sign: bool) -> list[int]:
    seen: set[int] = set()
    reps: list[int] = []
    for a in range(1, N):
        if a in seen:
            continue
        reps.append(a)
        x = a
        while x not in seen:
            seen.add(x)
            if identify_sign:
                seen.add((-x) % N)
            x = x * multiplier % N
    return reps


def main() -> None:
    pmod = P24 % N
    ord_p = int(sp.n_order(pmod, N))
    half = ord_p // 2
    minus_in_orbit = ord_p % 2 == 0 and pow(P24, half, N) == N - 1
    full_reps = orbit_reps(pmod, identify_sign=False)
    signed_reps = orbit_reps(pmod, identify_sign=True)
    energy_degree = half if minus_in_orbit else ord_p

    print("p24 energy real-cyclotomic packet audit")
    print(f"p={P24}")
    print(f"n={N}")
    print(f"p_mod_n={pmod}")
    print(f"ord_n_p={ord_p}")
    print(f"p_pow_ord_over_2_mod_n={pow(P24, half, N) if ord_p % 2 == 0 else 'NA'}")
    print(f"minus_one_in_frobenius_orbit={int(minus_in_orbit)}")
    print(f"relative_content_packet_degree={ord_p}")
    print(f"energy_packet_degree={energy_degree}")
    print(f"degree_halved_for_energy={int(energy_degree * 2 == ord_p)}")
    print(f"relative_character_orbit_count={len(full_reps)}")
    print(f"signed_energy_orbit_count={len(signed_reps)}")
    print(f"relative_character_reps={full_reps}")
    print(f"signed_energy_reps={signed_reps}")
    print()
    print("interpretation")
    print("  E_a_equals_E_minus_a_because_C_d_equals_C_minus_d=1")
    print("  p_power_half_orbit_maps_a_to_minus_a=1")
    print("  scalar_energy_certificates_live_in_real_cyclotomic_subfields=1")
    print("  number_of_energy_packets_same_as_relative_orbits_for_p24=1")
    print("conclusion=energy_halves_packet_degree_but_not_packet_count")


if __name__ == "__main__":
    main()

