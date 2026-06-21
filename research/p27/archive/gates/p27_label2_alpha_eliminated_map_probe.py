#!/usr/bin/env python3
"""Explicit alpha map on the eliminated label-2 cyclic quartic.

The order-4 lift was originally written on the (X,W,T,R) cover:

    T -> -T
    R -> R*(m0 - mt*T)/(2*T*S)

The eliminated cyclic-quartic model over E=(X,W) has only R:

    R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*S^2 = 0.

Using R^2 = pref*(m0 + mt*T), the alpha action becomes the rational map

    R -> R*mt*(2*pref*m0 - R^2)/(2*S*(R^2 - pref*m0)).

This probe validates that map over p27-signature finite fields.  The point is
to turn "ask CAS for the alpha quotient" into an explicit quotient-map input.
"""

from __future__ import annotations

import argparse
from collections import Counter


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, q: int) -> int:
    return pow(a % q, q - 2, q)


def roots_table(q: int) -> list[list[int]]:
    out: list[list[int]] = [[] for _ in range(q)]
    for x in range(q):
        out[x * x % q].append(x)
    return out


def e_rhs(x: int, q: int) -> int:
    return (x * x % q * x - x) % q


def pieces(x: int, w: int, q: int) -> dict[str, int] | None:
    if x % q == 0:
        return None
    x2 = x * x % q
    x3 = x2 * x % q
    t2 = x * (x2 + 1) % q * ((x2 + 2 * x - 1) % q) % q
    mt = (x + 1) * (2 * w * x + x3 + x2 - x - 1) % q
    m0 = (x2 + 1) * (x2 + 2 * x - 1) % q
    m0 = m0 * ((w * x + w + 2 * x2) % q) % q
    salpha = (w * (x + 1) + 2 * x2) % q
    pref = w * (x2 + 1) % q * inv(x, q) % q
    return {"T2": t2, "mt": mt, "m0": m0, "S": salpha, "pref": pref}


def quartic_value(x: int, w: int, r: int, q: int) -> int | None:
    data = pieces(x, w, q)
    if data is None:
        return None
    r2 = r * r % q
    return (
        r2 * r2
        - 2 * data["pref"] * data["m0"] * r2
        + 4 * data["pref"] * data["pref"] * data["T2"] * data["S"] * data["S"]
    ) % q


def alpha_r(x: int, w: int, r: int, q: int) -> int | None:
    data = pieces(x, w, q)
    if data is None:
        return None
    r2 = r * r % q
    pref_m0 = data["pref"] * data["m0"] % q
    den = 2 * data["S"] % q * ((r2 - pref_m0) % q) % q
    if den == 0:
        return None
    num = r * data["mt"] % q * ((2 * pref_m0 - r2) % q) % q
    return num * inv(den, q) % q


def quartic_roots_for_e_point(x: int, w: int, q: int, roots: list[list[int]]) -> list[int]:
    data = pieces(x, w, q)
    if data is None:
        return []
    # Solve in U=R^2, then take square roots of U.
    a = 1
    b = (-2 * data["pref"] * data["m0"]) % q
    c = 4 * data["pref"] * data["pref"] % q
    c = c * data["T2"] % q * data["S"] % q * data["S"] % q
    disc = (b * b - 4 * a * c) % q
    out: list[int] = []
    for sd in roots[disc]:
        u = (-b + sd) * inv(2 * a, q) % q
        for r in roots[u]:
            if r not in out:
                out.append(r)
    return out


def analyze_field(q: int) -> Counter:
    roots = roots_table(q)
    stats: Counter = Counter()
    for x in range(q):
        for w in roots[e_rhs(x, q)]:
            stats["e_affine_points"] += 1
            rs = quartic_roots_for_e_point(x, w, q, roots)
            stats[f"quartic_fiber_{len(rs)}"] += 1
            for r in rs:
                stats["quartic_affine_points"] += 1
                if quartic_value(x, w, r, q) != 0:
                    stats["quartic_root_mismatch"] += 1
                ar = alpha_r(x, w, r, q)
                if ar is None:
                    stats["alpha_undefined"] += 1
                    continue
                stats["alpha_defined"] += 1
                if quartic_value(x, w, ar, q) != 0:
                    stats["alpha_image_not_on_curve"] += 1
                if ar == r:
                    stats["alpha_fixed_affine"] += 1
                ar2 = alpha_r(x, w, ar, q)
                if ar2 is None:
                    stats["alpha2_undefined"] += 1
                    continue
                if ar2 != (-r) % q:
                    stats["alpha2_not_rdeck"] += 1
                ar3 = alpha_r(x, w, ar2, q)
                ar4 = alpha_r(x, w, ar3, q) if ar3 is not None else None
                if ar4 != r:
                    stats["alpha4_not_identity"] += 1
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 label2 alpha eliminated-map probe")
    print("alpha_R = R*mt*(2*pref*m0 - R^2)/(2*S*(R^2 - pref*m0))")
    print("promotion = explicit order-4 map for CAS quotient/Prym extraction")
    for q in parse_ints(args.small_primes):
        stats = analyze_field(q)
        print(f"q={q}:")
        print(f"  q_mod16 = {q % 16}")
        print_counter("  stats", stats)
    print("p27_label2_alpha_eliminated_map_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
