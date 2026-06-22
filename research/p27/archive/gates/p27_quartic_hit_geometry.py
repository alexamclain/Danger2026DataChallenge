#!/usr/bin/env python3
"""Verify and classify a p27 B/K quartic GPU hit.

The full quartic GPU suite can return a polynomial

    X^4 + a*X^3 + b*X^2 + c*X + d

for either the B-line or K-line target rows.  This analyzer verifies the hit
against the frozen packet and then records the immediate geometry of
z^2=f(X): squarefree degree, factor degrees, genus of the normalization, and
finite-field point count.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

import sympy as sp

import p27_b_line_quartic_verify as b_verify
import p27_kline_quartic_verify as k_verify


@dataclass(frozen=True)
class CoordinateOps:
    name: str
    packet: str
    load_packet: Any
    target_entry: Any
    verify: Any


COORDINATES = {
    "B": CoordinateOps(
        name="B",
        packet=b_verify.DEFAULT_PACKET,
        load_packet=b_verify.load_packet,
        target_entry=b_verify.target_entry,
        verify=b_verify.verify,
    ),
    "K": CoordinateOps(
        name="K",
        packet=k_verify.DEFAULT_PACKET,
        load_packet=k_verify.load_packet,
        target_entry=k_verify.target_entry,
        verify=k_verify.verify,
    ),
}


def parse_coeffs(raw: str) -> tuple[int, int, int, int]:
    parts = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--coeffs must be four comma-separated integers")
    return tuple(parts)  # type: ignore[return-value]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for value in range(1, p):
        table[value] = 1 if pow(value, (p - 1) // 2, p) == 1 else -1
    return table


def quartic_value(x_value: int, coeffs: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = coeffs
    x = x_value % p
    return (pow(x, 4, p) + a * pow(x, 3, p) + b * x * x + c * x + d) % p


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_degree(poly: list[int]) -> int:
    return len(trim(poly[:])) - 1


def poly_eval(poly: list[int], x_value: int, p: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x_value + coeff) % p
    return value


def divide_linear(poly: list[int], root: int, p: int) -> list[int]:
    """Divide a polynomial by x-root.  Caller guarantees root is a root."""

    coeffs_high = list(reversed(trim(poly[:])))
    quotient_high = [coeffs_high[0]]
    for coeff in coeffs_high[1:-1]:
        quotient_high.append((coeff + quotient_high[-1] * root) % p)
    return trim(list(reversed(quotient_high)))


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    size = max(len(a), len(b))
    out = [0] * size
    for i in range(size):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    size = max(len(a), len(b))
    out = [0] * size
    for i in range(size):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def poly_mod(poly: list[int], modulus: list[int], p: int) -> list[int]:
    out = trim(poly[:])
    modulus = trim(modulus[:])
    if modulus == [0]:
        raise ZeroDivisionError("polynomial modulus is zero")
    inv_lead = pow(modulus[-1], p - 2, p)
    while len(out) >= len(modulus) and out != [0]:
        scale = out[-1] * inv_lead % p
        shift = len(out) - len(modulus)
        for i, coeff in enumerate(modulus):
            out[i + shift] = (out[i + shift] - scale * coeff) % p
        trim(out)
    return out


def poly_pow_mod(base: list[int], exponent: int, modulus: list[int], p: int) -> list[int]:
    result = [1]
    base = poly_mod(base, modulus, p)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, base, p), modulus, p)
        base = poly_mod(poly_mul(base, base, p), modulus, p)
        exponent >>= 1
    return result


def factor_degrees_small(poly: list[int], p: int) -> list[tuple[int, int]]:
    """Return factor degrees/exponents for a degree <=4 polynomial over F_p."""

    remaining = trim(poly[:])
    factors: list[tuple[int, int]] = []
    for root in range(p):
        multiplicity = 0
        while poly_degree(remaining) > 0 and poly_eval(remaining, root, p) == 0:
            remaining = divide_linear(remaining, root, p)
            multiplicity += 1
        if multiplicity:
            factors.append((1, multiplicity))
    degree = poly_degree(remaining)
    if degree <= 0:
        return factors
    if degree in (2, 3):
        factors.append((degree, 1))
        return factors
    if degree == 4:
        x_poly = [0, 1]
        x_q2_minus_x = poly_sub(poly_pow_mod(x_poly, p * p, remaining, p), x_poly, p)
        x = sp.symbols("x")
        rem_poly = sp.Poly.from_list(list(reversed(remaining)), gens=x, modulus=p)
        probe_poly = sp.Poly.from_list(list(reversed(x_q2_minus_x)), gens=x, modulus=p)
        gcd_degree = sp.gcd(rem_poly, probe_poly).degree()
        repeated_degree = sp.gcd(rem_poly, rem_poly.diff()).degree()
        if gcd_degree == 0:
            factors.append((4, 1))
        elif repeated_degree == 2:
            factors.append((2, 2))
        else:
            factors.append((2, 1))
            factors.append((2, 1))
        return factors
    factors.append((degree, 1))
    return factors


def poly_data(coeffs: tuple[int, int, int, int], p: int) -> dict[str, Any]:
    x = sp.symbols("x")
    a, b, c, d = [value % p for value in coeffs]
    poly = sp.Poly(x**4 + a * x**3 + b * x**2 + c * x + d, x, modulus=p)
    derivative = poly.diff()
    repeated = sp.gcd(poly, derivative)
    squarefree = poly.quo(repeated)
    discriminant = int(sp.discriminant(poly.as_expr(), x)) % p
    squarefree_degree = squarefree.degree()
    normalization_genus = max(0, (squarefree_degree - 1) // 2)
    low_coeffs = [d, c, b, a, 1]
    squarefree_coeffs = [int(coeff) % p for coeff in reversed(squarefree.all_coeffs())]
    return {
        "degree": poly.degree(),
        "discriminant_mod_q": discriminant,
        "repeated_gcd_degree": repeated.degree(),
        "squarefree_degree": squarefree_degree,
        "normalization_genus": normalization_genus,
        "factor_degrees": factor_degrees_small(low_coeffs, p),
        "squarefree_factor_degrees": factor_degrees_small(squarefree_coeffs, p),
    }


def point_count(coeffs: tuple[int, int, int, int], p: int, squarefree_degree: int) -> dict[str, int]:
    chi = legendre_table(p)
    affine = 0
    zeros = 0
    square_values = 0
    nonsquare_values = 0
    for x_value in range(p):
        value = quartic_value(x_value, coeffs, p)
        sign = chi[value]
        if value == 0:
            affine += 1
            zeros += 1
        elif sign == 1:
            affine += 2
            square_values += 1
        else:
            nonsquare_values += 1
    if squarefree_degree == 4:
        infinity_points = 2
    elif squarefree_degree % 2 == 1:
        infinity_points = 1
    elif squarefree_degree > 0:
        infinity_points = 2
    else:
        infinity_points = 0
    return {
        "affine_points": affine,
        "infinity_points_model": infinity_points,
        "projective_points_model": affine + infinity_points,
        "zero_x_values": zeros,
        "square_x_values": square_values,
        "nonsquare_x_values": nonsquare_values,
    }


def print_mapping(title: str, mapping: dict[str, Any]) -> None:
    print(f"{title}:")
    for key in sorted(mapping):
        print(f"  {key} = {mapping[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coordinate", choices=sorted(COORDINATES), required=True)
    parser.add_argument("--packet")
    parser.add_argument("--field", type=int, required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--coeffs", type=parse_coeffs, required=True)
    parser.add_argument("--polarity", type=int, choices=(-1, 1), required=True)
    args = parser.parse_args()

    ops = COORDINATES[args.coordinate]
    packet_path = args.packet or ops.packet
    packet = ops.load_packet(packet_path)
    target = ops.target_entry(packet, args.field, args.family)
    verify_stats = ops.verify(target, args.coeffs, args.polarity)
    pass_hit = int(verify_stats["mismatches"] == 0 and verify_stats["zeros"] == 0)
    geometry = poly_data(args.coeffs, args.field)
    points = point_count(args.coeffs, args.field, int(geometry["squarefree_degree"]))

    print("p27 quartic hit geometry analyzer")
    print(f"coordinate = {args.coordinate}")
    print(f"packet = {packet_path}")
    print(f"field = {args.field}")
    print(f"family = {args.family}")
    print(f"coeffs = {','.join(str(c % args.field) for c in args.coeffs)}")
    print(f"polarity = {args.polarity}")
    print_mapping("verify_stats", verify_stats)
    print(f"verifier_pass = {pass_hit}")
    print_mapping("geometry", geometry)
    print_mapping("point_count", points)
    print("promotion_read:")
    if not pass_hit:
        print("  status = not_a_verified_hit")
    elif geometry["normalization_genus"] <= 1 and geometry["squarefree_degree"] >= 3:
        print("  status = low_genus_source_candidate")
    elif geometry["normalization_genus"] == 0:
        print("  status = degenerate_or_rational_candidate")
    else:
        print("  status = higher_genus_or_singular_candidate")
    print("p27_quartic_hit_geometry_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
