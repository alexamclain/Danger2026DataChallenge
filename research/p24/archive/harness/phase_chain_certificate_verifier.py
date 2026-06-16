#!/usr/bin/env python3
"""Verifier for the p24 selected-chain certificate surface.

This is a finite verifier, not a producer.  A successful p24 selected-chain
certificate supplies a degree-2 top root, selected degree-157 and degree-211
child roots, a selected degree-3107441 recovery j-root, and optionally a
Montgomery A and x0 accepted by the DANGER3 verifier.

Dense coefficient count excluding monic leading coefficients:

    2 + 157 + 211 + 3107441 = 3107811 << sqrt(10^24+7).
"""

from __future__ import annotations

import argparse
import json
from math import gcd, isqrt
from pathlib import Path
from typing import Any


P24 = 10**24 + 7
EXPECTED_CHILD_DEGREES = [157, 211]
EXPECTED_RECOVERY_DEGREE = 3_107_441


def eval_poly_mod(coeffs: list[int], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x + coeff) % p
    return value


def degree(coeffs: list[int]) -> int:
    for idx in range(len(coeffs) - 1, -1, -1):
        if coeffs[idx]:
            return idx
    return -1


def monic_slots(coeffs: list[int], p: int) -> int:
    if coeffs and coeffs[-1] % p == 1:
        return len(coeffs) - 1
    return len(coeffs)


def montgomery_j_from_A(A: int, p: int) -> int:
    a2 = A * A % p
    numerator = 256 * pow((a2 - 3) % p, 3, p) % p
    denominator = (a2 - 4) % p
    return numerator * pow(denominator, -1, p) % p


def pp_verify(p: int, A: int, x0: int) -> bool:
    if p < 5 or p % 2 == 0:
        return False
    q = isqrt(p)
    k = (q + 1 + isqrt(4 * q)).bit_length()
    if gcd(A * A - 4, p) != 1:
        return False
    X, Z = x0 % p, 1
    Zprev = None
    inv4 = (p + 1) // 4 if p % 4 == 3 else (3 * p + 1) // 4
    C = ((A + 2) * inv4) % p
    for _ in range(k):
        Zprev = Z
        U = (X + Z) * (X + Z) % p
        V = (X - Z) * (X - Z) % p
        W = (U - V) % p
        X, Z = U * V % p, W * ((V + C * W) % p) % p
    return Z % p == 0 and gcd(Zprev, p) == 1


def require_int_list(name: str, data: Any) -> list[int]:
    if not isinstance(data, list) or not all(isinstance(value, int) for value in data):
        raise ValueError(f"{name} must be a list of integers")
    return data


def schema() -> dict[str, Any]:
    return {
        "p": P24,
        "top_poly": ["c0", "c1", "c2=1"],
        "child_polys": [
            ["degree-157 selected child polynomial coeffs ascending"],
            ["degree-211 selected child polynomial coeffs ascending"],
        ],
        "recovery_poly": [
            "degree-3107441 selected recovery polynomial coeffs ascending"
        ],
        "chain_values": ["Z0", "Y0", "W0"],
        "j": "selected conductor-2 CM j-root",
        "A": "optional Montgomery parameter",
        "x0": "optional DANGER3 x-coordinate",
    }


def verify_payload(payload: dict[str, Any], strict_degrees: bool) -> tuple[bool, list[str]]:
    messages: list[str] = []
    ok = True
    p = int(payload.get("p", P24))
    if p != P24:
        ok = False
        messages.append(f"unexpected p={p}")

    top_poly = require_int_list("top_poly", payload.get("top_poly"))
    child_polys_raw = payload.get("child_polys")
    if not isinstance(child_polys_raw, list) or len(child_polys_raw) != 2:
        raise ValueError("child_polys must contain exactly two polynomials")
    child_polys = [
        require_int_list(f"child_polys[{idx}]", poly)
        for idx, poly in enumerate(child_polys_raw)
    ]
    recovery_poly = require_int_list("recovery_poly", payload.get("recovery_poly"))
    chain_values = require_int_list("chain_values", payload.get("chain_values"))
    if len(chain_values) != 3:
        raise ValueError("chain_values must be [Z0,Y0,W0]")
    j = int(payload["j"])

    expected_degrees = [2] + EXPECTED_CHILD_DEGREES + [EXPECTED_RECOVERY_DEGREE]
    actual_degrees = [
        degree(top_poly),
        degree(child_polys[0]),
        degree(child_polys[1]),
        degree(recovery_poly),
    ]
    if strict_degrees and actual_degrees != expected_degrees:
        ok = False
        messages.append(
            f"degree mismatch actual={actual_degrees} expected={expected_degrees}"
        )

    if eval_poly_mod(top_poly, chain_values[0], p) != 0:
        ok = False
        messages.append("top root failed")
    if eval_poly_mod(child_polys[0], chain_values[1], p) != 0:
        ok = False
        messages.append("degree-157 child root failed")
    if eval_poly_mod(child_polys[1], chain_values[2], p) != 0:
        ok = False
        messages.append("degree-211 child root failed")
    if eval_poly_mod(recovery_poly, j, p) != 0:
        ok = False
        messages.append("selected recovery j-root failed")

    if "A" in payload:
        A = int(payload["A"])
        if gcd(A * A - 4, p) != 1:
            ok = False
            messages.append("Montgomery A is singular")
        elif montgomery_j_from_A(A, p) != j % p:
            ok = False
            messages.append("Montgomery j(A) mismatch")
        if "x0" in payload and not pp_verify(p, A, int(payload["x0"])):
            ok = False
            messages.append("DANGER3 x-only replay failed")

    slots = (
        monic_slots(top_poly, p)
        + monic_slots(child_polys[0], p)
        + monic_slots(child_polys[1], p)
        + monic_slots(recovery_poly, p)
    )
    messages.append(f"coefficient_slots_excluding_monic_if_present={slots}")
    messages.append(f"slots_over_sqrt_floor={slots / 10**12:.12g}")
    return ok, messages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?")
    parser.add_argument("--schema", action="store_true")
    parser.add_argument("--no-strict-degrees", action="store_true")
    args = parser.parse_args()

    if args.schema or args.certificate is None:
        print(json.dumps(schema(), indent=2))
        print("expected_selected_chain_slots=3107811")
        print("expected_selected_chain_slots_over_sqrt=3.107811e-6")
        if args.certificate is None:
            return

    payload = json.loads(Path(args.certificate).read_text())
    ok, messages = verify_payload(payload, strict_degrees=not args.no_strict_degrees)
    print(f"phase_chain_certificate_verify={int(ok)}")
    for message in messages:
        print(message)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
