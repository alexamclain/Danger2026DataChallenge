#!/usr/bin/env python3
"""Finite-field check of the Dplus relative H90 automorphism.

For u=-core=u0+u1*z and Norm_z(u)=z^2*S^2, the z-conjugation lifts to the
relative Dplus cover by

    alpha(t,z,w,s) = (t,-z,w,z*S/s).

Then alpha^2 is the s-deck involution and alpha^4 is the identity.  Since
alpha fixes t,w, the quotient should be the elliptic curve

    w^2 = -(t^2+2t-1)(t^2-2t-1).

This probe validates the automorphism and orbit sizes on small p27-compatible
fields; it is not a production search path.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import importlib.util
from pathlib import Path
import sys


def load_symmetry_module():
    path = Path(__file__).with_name("p27_trace_norm_dplus_symmetry_probe.py")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sym = load_symmetry_module()


def inv(a: int, q: int) -> int | None:
    a %= q
    if a == 0:
        return None
    return pow(a, q - 2, q)


def square_part(t: int, q: int) -> int:
    t %= q
    b = (t * t + 1) % q
    c = (t * t + 2 * t - 1) % q
    return pow(t - 1, 3, q) * pow(t + 1, 4, q) % q * b % q * (c * c % q) % q


def u_value(t: int, z: int, w: int, eh: int, ev: int, q: int) -> int | None:
    pack = sym.core_and_signs(t, z, w, q)
    if pack is None:
        return None
    core, _dplus, _eh, _ev = pack
    # Recompute with requested fixed eh/ev, not Legendre-derived labels, so
    # all four orientation components can be checked uniformly.
    t %= q
    z %= q
    w %= q
    y, b, c, _r, _k = sym.parts(t, q)
    hcore = (c * b + eh * 2 * t * z) % q
    vcore = (2 * c * t * t + ev * z * w) % q
    core = (1 - t * t) % q
    core = core * b % q
    core = core * c % q
    core = core * y % q
    core = core * vcore % q
    core = core * hcore % q
    return (-core) % q


def alpha(point: tuple[int, int, int, int], eh: int, ev: int, q: int) -> tuple[int, int, int, int] | None:
    t, z, w, s = point
    inv_s = inv(s, q)
    if inv_s is None:
        return None
    return (t % q, (-z) % q, w % q, z * square_part(t, q) % q * inv_s % q)


def valid_point(point: tuple[int, int, int, int], eh: int, ev: int, q: int) -> bool:
    t, z, w, s = point
    y, b, c, _r, k = sym.parts(t, q)
    f = t * c % q * b % q
    if z * z % q != f:
        return False
    if w * w % q != k:
        return False
    u = u_value(t, z, w, eh, ev, q)
    if u is None:
        return False
    return s * s % q == u


def collect_component(q: int, eh: int, ev: int) -> list[tuple[int, int, int, int]]:
    points: list[tuple[int, int, int, int]] = []
    for t in range(q):
        y, b, c, _r, k = sym.parts(t, q)
        f = t * c % q * b % q
        if t == 0 or y == 0 or b == 0 or c == 0 or k == 0 or f == 0:
            continue
        for z in sym.roots2(f, q):
            for w in sym.roots2(k, q):
                u = u_value(t, z, w, eh, ev, q)
                if u is None:
                    continue
                for s in sym.roots2(u, q):
                    points.append((t, z, w, s))
    return points


def orbit_size(point: tuple[int, int, int, int], eh: int, ev: int, q: int) -> int | None:
    seen: set[tuple[int, int, int, int]] = set()
    cur: tuple[int, int, int, int] | None = point
    for _ in range(8):
        if cur is None:
            return None
        if cur in seen:
            return len(seen)
        seen.add(cur)
        cur = alpha(cur, eh, ev, q)
    return None


def run_component(q: int, eh: int, ev: int) -> Counter[str]:
    points = collect_component(q, eh, ev)
    point_set = set(points)
    stats: Counter[str] = Counter()
    stats["points"] = len(points)
    base_tw: set[tuple[int, int]] = set()
    for point in points:
        t, _z, w, s = point
        base_tw.add((t, w))
        image1 = alpha(point, eh, ev, q)
        image2 = alpha(image1, eh, ev, q) if image1 is not None else None
        image4 = image2
        if image4 is not None:
            image3 = alpha(image2, eh, ev, q)
            image4 = alpha(image3, eh, ev, q) if image3 is not None else None
        if image1 is None:
            stats["alpha_undefined"] += 1
            continue
        if image1 not in point_set or not valid_point(image1, eh, ev, q):
            stats["alpha_invalid"] += 1
        if image2 != (t, point[1], w, (-s) % q):
            stats["alpha2_not_sdeck"] += 1
        if image4 != point:
            stats["alpha4_not_identity"] += 1
        size = orbit_size(point, eh, ev, q)
        stats[f"orbit_size_{size}"] += 1
    stats["base_tw_points"] = len(base_tw)
    if stats["base_tw_points"]:
        stats["degree_scaled_x1000000"] = stats["points"] * 1_000_000 // stats["base_tw_points"]
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qs", default="607,1607,1847,2087")
    args = parser.parse_args()

    qs = [int(part) for part in args.qs.split(",") if part]
    print("p27 trace/norm Dplus H90 automorphism probe")
    print("alpha = (t,z,w,s) -> (t,-z,w,z*S/s)")
    print("S = (t-1)^3*(t+1)^4*(t^2+1)*(t^2+2t-1)^2")
    print("quotient candidate = w^2=-(t^2+2t-1)(t^2-2t-1)")
    for q in qs:
        for eh, ev in product((1, -1), (1, -1)):
            stats = run_component(q, eh, ev)
            print(f"q{q}_eh{eh}_ev{ev}:")
            for key in sorted(stats):
                print(f"  {key} = {stats[key]}")
    print("p27_trace_norm_dplus_h90_automorphism_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
