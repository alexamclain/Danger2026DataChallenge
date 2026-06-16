#!/usr/bin/env python3
"""Finite verifier for the p24 trace-GCD orbit-norm payload.

This verifier checks only the finite p24 payload:

    Pi_O * Pi_O_inv = 1 mod p

for the seven Frobenius orbits on Z/211Z.  It does not prove producer
honesty.  A complete certificate must also prove that the supplied `Pi_O`
are the actual phase-aware block-cycle/Fitting orbit norms attached to the
p24 trace-GCD determinant section.

With `--unit2-schema` or `--unit2`, it checks the conditional compressed
payload consisting of the fixed orbit and one nonzero representative orbit.
That mode additionally requires a producer theorem proving diamond/unit-2
determinant-line equivariance up to p-unit transition factors.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


P24 = 10**24 + 7
RIGHT = 211
BLOCK_SIZE = 16


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


def orbit_manifest() -> list[dict[str, Any]]:
    return [
        {"id": f"O{index}", "members": orbit, "length": len(orbit)}
        for index, orbit in enumerate(frobenius_orbits(P24 % RIGHT, RIGHT))
    ]


def schema() -> dict[str, Any]:
    return {
        "p": P24,
        "right": RIGHT,
        "frobenius_multiplier": P24 % RIGHT,
        "block_size": BLOCK_SIZE,
        "orbits": orbit_manifest(),
        "orbit_norms": [
            {
                "id": orbit["id"],
                "value": "Pi_O in F_p",
                "inverse": "Pi_O^{-1} in F_p",
            }
            for orbit in orbit_manifest()
        ],
        "producer_honesty_required": (
            "Each value must be proved to equal the actual phase-aware "
            "block-cycle/Fitting orbit norm for this orbit."
        ),
    }


def unit2_schema() -> dict[str, Any]:
    return {
        "p": P24,
        "right": RIGHT,
        "frobenius_multiplier": P24 % RIGHT,
        "unit": 2,
        "block_size": BLOCK_SIZE,
        "orbits": orbit_manifest(),
        "unit_action_mapping": {
            "O0": "O0",
            "O1": "O2",
            "O2": "O3",
            "O3": "O4",
            "O4": "O5",
            "O5": "O6",
            "O6": "O1",
        },
        "unit2_orbit_norms": [
            {
                "id": "O0",
                "role": "fixed orbit",
                "value": "Pi_O0 in F_p",
                "inverse": "Pi_O0^{-1} in F_p",
            },
            {
                "id": "O1",
                "role": "one nonzero representative orbit",
                "value": "Pi_O1 in F_p",
                "inverse": "Pi_O1^{-1} in F_p",
            },
        ],
        "producer_honesty_required": (
            "The supplied values must be proved to equal the actual "
            "phase-aware block-cycle/Fitting orbit norms for O0 and O1."
        ),
        "diamond_equivariance_required": (
            "The producer must prove unit-2/diamond determinant-line "
            "equivariance up to p-unit transition factors around O1..O6."
        ),
    }


def require_int(name: str, value: Any) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def verify_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True

    p = require_int("p", payload.get("p", P24))
    if p != P24:
        ok = False
        messages.append(f"unexpected_p={p}")

    right = require_int("right", payload.get("right", RIGHT))
    if right != RIGHT:
        ok = False
        messages.append(f"unexpected_right={right}")

    orbit_rows = payload.get("orbit_norms")
    if not isinstance(orbit_rows, list):
        raise ValueError("orbit_norms must be a list")

    expected = {row["id"]: row for row in orbit_manifest()}
    seen: set[str] = set()
    for row in orbit_rows:
        if not isinstance(row, dict):
            raise ValueError("each orbit_norms entry must be an object")
        orbit_id = row.get("id")
        if orbit_id not in expected:
            ok = False
            messages.append(f"unexpected_orbit_id={orbit_id}")
            continue
        if orbit_id in seen:
            ok = False
            messages.append(f"duplicate_orbit_id={orbit_id}")
            continue
        seen.add(orbit_id)

        value = require_int(f"{orbit_id}.value", row.get("value"))
        inverse = require_int(f"{orbit_id}.inverse", row.get("inverse"))
        if not (0 <= value < p):
            ok = False
            messages.append(f"{orbit_id}.value_out_of_range=1")
        if not (0 <= inverse < p):
            ok = False
            messages.append(f"{orbit_id}.inverse_out_of_range=1")
        unit_ok = (value * inverse) % p == 1
        messages.append(f"{orbit_id}.unit_check={int(unit_ok)}")
        if not unit_ok:
            ok = False

    missing = sorted(set(expected) - seen)
    if missing:
        ok = False
        messages.append(f"missing_orbits={missing}")

    field_elements = 2 * len(expected)
    messages.append(f"orbit_count={len(expected)}")
    messages.append(f"payload_field_elements={field_elements}")
    messages.append(f"payload_over_sqrt_floor={field_elements / 10**12:.12g}")
    messages.append("producer_honesty_required=1")
    return ok, messages


def verify_unit2_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True

    p = require_int("p", payload.get("p", P24))
    if p != P24:
        ok = False
        messages.append(f"unexpected_p={p}")

    right = require_int("right", payload.get("right", RIGHT))
    if right != RIGHT:
        ok = False
        messages.append(f"unexpected_right={right}")

    orbit_rows = payload.get("unit2_orbit_norms")
    if not isinstance(orbit_rows, list):
        raise ValueError("unit2_orbit_norms must be a list")

    expected = {"O0", "O1"}
    seen: set[str] = set()
    for row in orbit_rows:
        if not isinstance(row, dict):
            raise ValueError("each unit2_orbit_norms entry must be an object")
        orbit_id = row.get("id")
        if orbit_id not in expected:
            ok = False
            messages.append(f"unexpected_orbit_id={orbit_id}")
            continue
        if orbit_id in seen:
            ok = False
            messages.append(f"duplicate_orbit_id={orbit_id}")
            continue
        seen.add(orbit_id)

        value = require_int(f"{orbit_id}.value", row.get("value"))
        inverse = require_int(f"{orbit_id}.inverse", row.get("inverse"))
        if not (0 <= value < p):
            ok = False
            messages.append(f"{orbit_id}.value_out_of_range=1")
        if not (0 <= inverse < p):
            ok = False
            messages.append(f"{orbit_id}.inverse_out_of_range=1")
        unit_ok = (value * inverse) % p == 1
        messages.append(f"{orbit_id}.unit_check={int(unit_ok)}")
        if not unit_ok:
            ok = False

    missing = sorted(expected - seen)
    if missing:
        ok = False
        messages.append(f"missing_orbits={missing}")

    field_elements = 2 * len(expected)
    messages.append("checked_orbits=['O0', 'O1']")
    messages.append(f"payload_field_elements={field_elements}")
    messages.append(f"payload_over_sqrt_floor={field_elements / 10**12:.12g}")
    messages.append("producer_honesty_required=1")
    messages.append("diamond_equivariance_required=1")
    return ok, messages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?")
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--unit2-schema", action="store_true")
    parser.add_argument("--unit2", action="store_true")
    args = parser.parse_args()

    if args.unit2_schema:
        print(json.dumps(unit2_schema(), indent=2))
        print("expected_payload_field_elements=4")
        print("expected_payload_over_sqrt_floor=4e-12")
        print("producer_honesty_required=1")
        print("diamond_equivariance_required=1")
        return

    if args.schema or args.certificate is None:
        print(json.dumps(schema(), indent=2))
        print("expected_payload_field_elements=14")
        print("expected_payload_over_sqrt_floor=1.4e-11")
        if args.certificate is None:
            return

    payload = json.loads(Path(args.certificate).read_text())
    ok, messages = (
        verify_unit2_payload(payload) if args.unit2 else verify_payload(payload)
    )
    print(f"trace_gcd_orbit_norm_certificate_verify={int(ok)}")
    for message in messages:
        print(message)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
