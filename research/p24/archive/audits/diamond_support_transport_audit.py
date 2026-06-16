#!/usr/bin/env python3
"""p24 support transport audit for the unit-2 diamond action.

The diamond determinant-line theorem must transport the representative
trace-GCD row

    delete O4, tail O1, prefix O2,O3,O5,O6

around all six nonzero right Frobenius orbits.  This script checks the finite
support/window bookkeeping: the unit `2 mod 211` cycles deleted and tail
orbits, carries the four-block prefix to the corresponding four-block prefix,
and transports the 16-coordinate tail window as a Frobenius-contiguous window
inside the target orbit.
"""

from __future__ import annotations

import json


P = 10**24 + 7
RIGHT = 211
UNIT = 2
TAIL_LEN = 16
REPRESENTATIVE_DELETED = 4
REPRESENTATIVE_TAIL = 1


def frobenius_orbits(multiplier: int, modulus: int) -> list[list[int]]:
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
            value = value * multiplier % modulus
        out.append(orbit)
    return out


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {
        value: index
        for index, orbit in enumerate(orbits, start=1)
        for value in orbit
    }


def unit_permutation(unit: int, orbits: list[list[int]]) -> dict[int, int]:
    labels = orbit_label_map(orbits)
    return {
        index: labels[(unit * orbit[0]) % RIGHT]
        for index, orbit in enumerate(orbits, start=1)
    }


def multiply_window(unit: int, window: list[int]) -> list[int]:
    return [(unit * value) % RIGHT for value in window]


def cyclic_interval_positions(positions: list[int], modulus: int) -> tuple[bool, int | None]:
    if not positions:
        return True, None
    start = positions[0]
    expected = [(start + offset) % modulus for offset in range(len(positions))]
    return positions == expected, start


def main() -> None:
    q = P % RIGHT
    orbits = frobenius_orbits(q, RIGHT)
    perm = unit_permutation(UNIT, orbits)
    deleted = REPRESENTATIVE_DELETED
    tail = REPRESENTATIVE_TAIL
    window = orbits[tail - 1][:TAIL_LEN]
    rows = []

    for step in range(len(orbits)):
        prefix = [
            label
            for label in range(1, len(orbits) + 1)
            if label not in {deleted, tail}
        ]
        target_orbit = orbits[tail - 1]
        positions = [target_orbit.index(value) for value in window]
        contiguous, rotation_start = cyclic_interval_positions(
            positions,
            len(target_orbit),
        )
        rows.append(
            {
                "step": step,
                "deleted": f"O{deleted}",
                "tail": f"O{tail}",
                "prefix": [f"O{label}" for label in prefix],
                "tail_window": window,
                "tail_positions": positions,
                "tail_window_frobenius_contiguous": contiguous,
                "tail_window_rotation_start": rotation_start,
            }
        )
        deleted = perm[deleted]
        tail = perm[tail]
        window = multiply_window(UNIT, window)

    deleted_cycle = [row["deleted"] for row in rows]
    tail_cycle = [row["tail"] for row in rows]
    prefix_sets = [tuple(row["prefix"]) for row in rows]
    final_target_orbit = orbits[REPRESENTATIVE_TAIL - 1]
    final_positions = [final_target_orbit.index(value) for value in window]
    final_contiguous, final_rotation_start = cyclic_interval_positions(
        final_positions,
        len(final_target_orbit),
    )
    audit = {
        "name": "p24_diamond_support_transport_audit",
        "p": P,
        "right": RIGHT,
        "p_mod_right": q,
        "unit": UNIT,
        "right_orbits": {
            f"O{index}": orbit for index, orbit in enumerate(orbits, start=1)
        },
        "unit_permutation": {f"O{k}": f"O{v}" for k, v in perm.items()},
        "representative": {
            "deleted": f"O{REPRESENTATIVE_DELETED}",
            "tail": f"O{REPRESENTATIVE_TAIL}",
            "prefix": rows[0]["prefix"],
            "tail_len": TAIL_LEN,
        },
        "rows": rows,
        "deleted_cycle_covers_all_nonzero_orbits": sorted(deleted_cycle)
        == [f"O{i}" for i in range(1, len(orbits) + 1)],
        "tail_cycle_covers_all_nonzero_orbits": sorted(tail_cycle)
        == [f"O{i}" for i in range(1, len(orbits) + 1)],
        "all_prefixes_have_four_blocks": all(len(prefix) == 4 for prefix in prefix_sets),
        "all_tail_windows_frobenius_contiguous": all(
            row["tail_window_frobenius_contiguous"] for row in rows
        ),
        "final_deleted_returns_to_representative": deleted == REPRESENTATIVE_DELETED,
        "final_tail_returns_to_representative": tail == REPRESENTATIVE_TAIL,
        "final_tail_window": window,
        "final_tail_positions": final_positions,
        "final_window_returns_to_representative_orbit": all(
            value in set(final_target_orbit) for value in window
        ),
        "final_window_frobenius_contiguous": final_contiguous,
        "final_window_rotation_start": final_rotation_start,
        "interpretation": [
            "unit-2 cycles the representative support through all six deletion rows",
            "tail windows remain Frobenius-contiguous but may be internally rotated",
            "the producer must allow internal Frobenius rotations in target factors",
            "this is finite support bookkeeping, not p-unit nonvanishing",
        ],
    }
    print(json.dumps(audit, indent=2, sort_keys=True))

    required = [
        audit["deleted_cycle_covers_all_nonzero_orbits"],
        audit["tail_cycle_covers_all_nonzero_orbits"],
        audit["all_prefixes_have_four_blocks"],
        audit["all_tail_windows_frobenius_contiguous"],
        audit["final_deleted_returns_to_representative"],
        audit["final_tail_returns_to_representative"],
        audit["final_window_returns_to_representative_orbit"],
        audit["final_window_frobenius_contiguous"],
    ]
    if not all(required):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
