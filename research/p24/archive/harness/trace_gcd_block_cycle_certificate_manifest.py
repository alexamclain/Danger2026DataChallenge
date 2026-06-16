#!/usr/bin/env python3
"""Print the fixed p24 block-cycle certificate manifest.

This is not a certificate producer.  It records the verifier-side constants
for the current trace-GCD block-cycle route and the payload sizes of the
candidate finite certificates.
"""

from __future__ import annotations

import json


P = 10**24 + 7
RIGHT = 211
BLOCK_SIZE = 16


def multiplicative_order(a: int, mod: int) -> int:
    x = 1
    for k in range(1, mod + 1):
        x = (x * a) % mod
        if x == 1:
            return k
    raise ValueError(f"{a} has no multiplicative order modulo {mod}")


def frobenius_orbits(q: int, mod: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(mod):
        if start in seen:
            continue
        orbit: list[int] = []
        x = start
        while x not in seen:
            seen.add(x)
            orbit.append(x)
            x = (x * q) % mod
        orbits.append(orbit)
    return orbits


def main() -> None:
    q = P % RIGHT
    orbits = frobenius_orbits(q, RIGHT)
    nonzero_orbits = [orbit for orbit in orbits if orbit != [0]]
    nonzero_orbit_len = len(nonzero_orbits[0])
    block_cycle_dim = BLOCK_SIZE * nonzero_orbit_len
    fixed_orbit_dim = BLOCK_SIZE
    explicit_block_entries = (
        fixed_orbit_dim * fixed_orbit_dim
        + len(nonzero_orbits) * block_cycle_dim * block_cycle_dim
    )

    manifest = {
        "p": P,
        "sqrt_p_floor": 10**12,
        "right": RIGHT,
        "frobenius_multiplier_q": q,
        "ord_q_mod_right": multiplicative_order(q, RIGHT),
        "orbits": [
            {"id": f"O{i}", "length": len(orbit), "members": orbit}
            for i, orbit in enumerate(orbits)
        ],
        "block_size": BLOCK_SIZE,
        "nonzero_block_cycle_dim": block_cycle_dim,
        "fixed_orbit_block_cycle_dim": fixed_orbit_dim,
        "nonzero_block_cycle_sign_positive": (BLOCK_SIZE * (nonzero_orbit_len - 1)) % 2 == 0,
        "payload_field_elements": {
            "global_operator_norm_plus_inverse": 2,
            "unit2_fixed_plus_representative_norms_plus_inverses": 4,
            "seven_orbit_norms_plus_inverses": 2 * len(orbits),
            "pointwise_values_plus_inverses": 2 * RIGHT,
            "explicit_block_matrices": explicit_block_entries,
            "explicit_block_matrices_plus_inverse_matrices": 2 * explicit_block_entries,
        },
        "payload_ratio_to_sqrt_p": {
            "global_operator_norm_plus_inverse": 2 / 10**12,
            "unit2_fixed_plus_representative_norms_plus_inverses": 4 / 10**12,
            "seven_orbit_norms_plus_inverses": (2 * len(orbits)) / 10**12,
            "pointwise_values_plus_inverses": (2 * RIGHT) / 10**12,
            "explicit_block_matrices_plus_inverse_matrices": (2 * explicit_block_entries) / 10**12,
        },
        "conditional_payload_assumptions": {
            "unit2_fixed_plus_representative_norms_plus_inverses": [
                "producer proves O0 and O1 values are honest Fitting orbit norms",
                "producer proves unit-2 diamond determinant-line equivariance up to p-units",
            ],
        },
    }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
