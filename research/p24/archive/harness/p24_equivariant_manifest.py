#!/usr/bin/env python3
"""Machine-readable equivariant manifest for the compressed p24 certificate."""

from __future__ import annotations

import json


P = 10**24 + 7
LEFT = 157
RIGHT = 211
LEFT_DIM = 156
RIGHT_DIM = 35
PREFIX_BLOCKS = LEFT_DIM // RIGHT_DIM
TAIL_LEN = LEFT_DIM - PREFIX_BLOCKS * RIGHT_DIM
UNIT = 2


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


def representative_orbit(right_orbits: list[list[int]]) -> list[dict[str, object]]:
    unit_perm = unit_permutation(UNIT, right_orbits)
    deleted = 4
    tail = 1
    window = right_orbits[tail - 1][:TAIL_LEN]
    rows: list[dict[str, object]] = []
    for step in range(len(right_orbits)):
        prefix = [
            index
            for index in range(1, len(right_orbits) + 1)
            if index not in (deleted, tail)
        ]
        rows.append(
            {
                "unit2_step": step,
                "deleted": deleted,
                "prefix": prefix,
                "tail": tail,
                "tail_window": window,
                "tail_positions_in_natural_order": [
                    right_orbits[tail - 1].index(value) for value in window
                ],
            }
        )
        deleted = apply_permutation(unit_perm, deleted)
        tail = apply_permutation(unit_perm, tail)
        window = multiply_window(UNIT, window)
    return rows


def manifest() -> dict[str, object]:
    left_orbits = frobenius_orbits(LEFT, P)
    right_orbits = frobenius_orbits(RIGHT, P)
    negation_perm = unit_permutation(-1 % RIGHT, right_orbits)
    unit2_perm = unit_permutation(UNIT, right_orbits)
    rows = representative_orbit(right_orbits)
    return {
        "name": "p24_equivariant_mixed_certificate_manifest",
        "p": P,
        "left_modulus": LEFT,
        "right_modulus": RIGHT,
        "left_orbit_count": len(left_orbits),
        "left_orbit_length": len(left_orbits[0]),
        "right_orbit_count": len(right_orbits),
        "right_orbit_length": len(right_orbits[0]),
        "right_orbits": {
            f"O{index}": orbit for index, orbit in enumerate(right_orbits, start=1)
        },
        "prefix_blocks": PREFIX_BLOCKS,
        "tail_len": TAIL_LEN,
        "leading_dim": LEFT_DIM,
        "negation_permutation": negation_perm,
        "unit2_permutation": unit2_perm,
        "representative_scalar": {
            "name": "L_rep",
            "meaning": "representative leading 156-coordinate Moore determinant",
            "factorization": "B_rep*T_rep",
            "required_status": "nonzero_mod_p",
        },
        "representative_row": rows[0],
        "representative_dual_obstruction": {
            "source": "L=F_p(mu_157)",
            "full_zero_blocks": [2, 3, 5, 6],
            "tail_zero_block": 1,
            "tail_zero_coordinates": list(range(TAIL_LEN)),
            "deleted_block": 4,
            "bad_event": (
                "nonzero lambda with a_2=a_3=a_5=a_6=0 and "
                "first 16 Lang coordinates of a_1 equal to zero"
            ),
        },
        "unit2_orbit_rows": rows,
        "finite_gates": [
            "p24/lean/RepresentativeOnePUnitGate.lean",
            "p24/lean/TraceGcdOperatorRepresentativeGate.lean",
            "p24/lean/UnitOrbitGate.lean",
            "p24/lean/ConjugateTailGate.lean",
            "p24/lean/RepresentativeDualObstructionGate.lean",
            "p24/lean/MixedSubspacePolynomialGate.lean",
            "p24/lean/MixedRightOrbitSupportGate.lean",
            "p24/lean/MixedTraceIntersectionGate.lean",
        ],
        "trace_gcd_operator_surface": {
            "name": "Norm_trace",
            "meaning": (
                "global operator norm det(m_f on F_p[Y]/(Y^211-1)) "
                "for the actual trace-GCD determinant sequence Delta(t)"
            ),
            "payload_with_inverse": 2,
            "required_honesty": (
                "any zero of the actual Delta(t) sequence forces Norm_trace=0"
            ),
        },
        "trace_gcd_two_resultant_surface": {
            "name": "Xi_O0_and_Xi_O1",
            "manifest": "p24/trace_gcd_two_resultant_theorem_manifest.py",
            "payload_with_inverses": 4,
            "values": ["Xi_O0", "Xi_O0_inverse", "Xi_O1", "Xi_O1_inverse"],
            "meaning": (
                "fixed p-linearized trace-GCD resultant plus one nonzero "
                "Frobenius/crossed norm of p-linearized resultants"
            ),
            "required_honesty": [
                "Xi_O0 is the actual fixed-orbit resultant Res_p-lin(P_K0,T_0)",
                "Xi_O1 is the actual reduced norm over one nonzero right Frobenius orbit",
                "unit-2 diamond determinant-line transport scales the other nonzero orbit norms by p-units",
            ],
        },
        "missing_arithmetic_theorem": (
            "prove the two-resultant p-unit theorem for the actual embedded "
            "p24 mixed Hermitian periods, including p-unit determinant-line "
            "transport around the unit-2 right-orbit cycle; the older L_rep "
            "or global Norm_trace surfaces remain sufficient fallbacks but "
            "are no longer the sharpest current target"
        ),
    }


def main() -> None:
    print(json.dumps(manifest(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
