#!/usr/bin/env python3
"""Elliptic-coset audit for the p27 trace/norm quotient line.

The p27 transfer gate reduced the active trace/norm structure to two balanced
bits on the quotient

    C: b^2 = 16 - a^4.

This gate maps C to the j=1728 elliptic curve

    E: v^2 = u^3 - u
    u = 4/a^2
    v = 2b/a^3

and tests whether the domain bit or T_line bit is explained by small torsion
or quotient-coset data on E(F_p).  Since p27 is 3 mod 4, E is expected to be
supersingular with #E(F_p)=p+1; this makes small torsion projections a natural
first structural falsifier before asking for heavier theta/divisor machinery.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import importlib.util
from pathlib import Path
import sys
from typing import Optional


def load_gate(name: str):
    path = Path(__file__).with_name(name)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


transfer = load_gate("p27_trace_norm_transfer_gate.py")
P = transfer.P
GROUP_ORDER = P + 1
GROUP_EXPONENT_CANDIDATE = GROUP_ORDER // 2
EC_A = P - 1  # y^2 = x^3 - x

Affine = Optional[tuple[int, int]]
Jacobian = tuple[int, int, int]
Record = tuple[Affine, int]


def inv(value: int) -> int:
    return pow(value % P, P - 2, P)


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def parse_range(raw: str) -> list[int]:
    return transfer.parse_range(raw)


def affine_from_ab(a: int, b: int) -> Affine:
    a %= P
    b %= P
    if a == 0:
        return None
    a2 = a * a % P
    u = 4 * inv(a2) % P
    v = 2 * b % P * inv(a2 * a % P) % P
    if (v * v - (u * u % P * u - u)) % P != 0:
        raise RuntimeError("bad C -> E map")
    return u, v


def jac_from_affine(point: Affine) -> Jacobian:
    if point is None:
        return (0, 1, 0)
    x, y = point
    return (x % P, y % P, 1)


def jac_is_inf(point: Jacobian) -> bool:
    return point[2] % P == 0


def jac_double(point: Jacobian) -> Jacobian:
    x1, y1, z1 = point
    if z1 == 0 or y1 == 0:
        return (0, 1, 0)
    xx = x1 * x1 % P
    yy = y1 * y1 % P
    yyyy = yy * yy % P
    zz = z1 * z1 % P
    s = 2 * (((x1 + yy) * (x1 + yy) - xx - yyyy) % P) % P
    m = (3 * xx + EC_A * zz % P * zz) % P
    x3 = (m * m - 2 * s) % P
    y3 = (m * (s - x3) - 8 * yyyy) % P
    z3 = ((y1 + z1) * (y1 + z1) - yy - zz) % P
    return x3, y3, z3


def jac_add(p1: Jacobian, p2: Jacobian) -> Jacobian:
    if jac_is_inf(p1):
        return p2
    if jac_is_inf(p2):
        return p1
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    z1z1 = z1 * z1 % P
    z2z2 = z2 * z2 % P
    u1 = x1 * z2z2 % P
    u2 = x2 * z1z1 % P
    s1 = y1 * z2 % P * z2z2 % P
    s2 = y2 * z1 % P * z1z1 % P
    h = (u2 - u1) % P
    r = (s2 - s1) % P
    if h == 0:
        if r == 0:
            return jac_double(p1)
        return (0, 1, 0)
    hh = h * h % P
    hhh = h * hh % P
    v = u1 * hh % P
    x3 = (r * r - hhh - 2 * v) % P
    y3 = (r * (v - x3) - s1 * hhh) % P
    z3 = h * z1 % P * z2 % P
    return x3, y3, z3


def jac_mul(point: Affine, scalar: int) -> Jacobian:
    result = (0, 1, 0)
    addend = jac_from_affine(point)
    n = scalar
    while n:
        if n & 1:
            result = jac_add(result, addend)
        addend = jac_double(addend)
        n >>= 1
    return result


def affine_from_jac(point: Jacobian) -> Affine:
    x, y, z = point
    if z == 0:
        return None
    zinv = inv(z)
    z2 = zinv * zinv % P
    z3 = z2 * zinv % P
    return x * z2 % P, y * z3 % P


def canonical_point_key(point: Affine) -> tuple[str, int, int]:
    if point is None:
        return ("O", 0, 0)
    x, y = point
    y_canon = min(y, (-y) % P)
    return ("P", x, y_canon)


def collect_records(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
    max_records: int,
) -> tuple[list[Record], list[Record], Counter[str]]:
    points, collect_stats = transfer.collect_k_points(seeds, chunks, tids, draws_per_thread)
    stats: Counter[str] = Counter(collect_stats)

    domain_by_a: dict[int, tuple[Affine, int]] = {}
    for y, w in points:
        coords = transfer.quotient_coordinates(y, w)
        if coords is None:
            stats["domain_quotient_undefined"] += 1
            continue
        a, b = coords
        if (b * b - (16 - pow(a, 4, P))) % P != 0:
            stats["domain_quotient_relation_fail"] += 1
            continue
        target = transfer.chi(transfer.f_value(y))
        if target == 0:
            stats["domain_target_zero"] += 1
            continue
        point = affine_from_ab(a, b)
        if point is None:
            stats["domain_a_zero_skipped"] += 1
            continue
        old = domain_by_a.get(a)
        if old is None:
            domain_by_a[a] = (point, target)
        elif old[1] != target:
            stats["domain_inconsistent"] += 1
    domain_records = list(domain_by_a.values())

    quotient_rows, quotient_stats = transfer.collect_quotient_rows(points)
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    target_by_a: dict[int, tuple[Affine, int]] = {}
    for a, b, target in quotient_rows:
        line_target = transfer.normalized_line_target(a, b, target, "p26_Tline")
        if line_target is None or line_target == 0:
            stats["target_line_unusable"] += 1
            continue
        point = affine_from_ab(a, b)
        if point is None:
            stats["target_a_zero_skipped"] += 1
            continue
        old = target_by_a.get(a)
        if old is None:
            target_by_a[a] = (point, line_target)
        elif old[1] != line_target:
            stats["target_line_inconsistent"] += 1
    target_records = list(target_by_a.values())

    if max_records:
        domain_records = domain_records[:max_records]
        target_records = target_records[:max_records]
    stats["domain_records"] = len(domain_records)
    stats["target_records"] = len(target_records)
    return domain_records, target_records, stats


def score_projection(records: list[Record], modulus: int) -> Counter[str]:
    cofactor = GROUP_EXPONENT_CANDIDATE // modulus
    by_class: dict[tuple[str, int, int], Counter[int]] = defaultdict(Counter)
    stats: Counter[str] = Counter()
    for point, target in records:
        projected = affine_from_jac(jac_mul(point, cofactor))
        key = canonical_point_key(projected)
        by_class[key][target] += 1
        stats["rows"] += 1
        stats[f"target_{sign_name(target)}"] += 1
    majority = 0
    mixed = 0
    singleton = 0
    largest = 0
    for counts in by_class.values():
        total = counts[1] + counts[-1]
        largest = max(largest, total)
        majority += max(counts[1], counts[-1])
        if counts[1] and counts[-1]:
            mixed += 1
        if total == 1:
            singleton += 1
    stats["classes"] = len(by_class)
    stats["mixed_classes"] = mixed
    stats["singleton_classes"] = singleton
    stats["largest_class"] = largest
    stats["majority"] = majority
    if stats["rows"]:
        plus = stats["target_+1"]
        stats["baseline_majority"] = max(plus, stats["rows"] - plus)
    return stats


def print_projection_scores(label: str, records: list[Record], moduli: list[int]) -> None:
    print(f"{label}_projection_scores:")
    for modulus in moduli:
        if GROUP_EXPONENT_CANDIDATE % modulus != 0:
            continue
        stats = score_projection(records, modulus)
        rows = stats["rows"]
        majority_score = stats["majority"] / rows if rows else 0.0
        baseline_score = stats["baseline_majority"] / rows if rows else 0.0
        lift = majority_score / baseline_score if baseline_score else 0.0
        exact = int(rows > 0 and stats["mixed_classes"] == 0 and stats["singleton_classes"] < stats["classes"])
        print(
            "  "
            f"m={modulus} rows={rows} classes={stats['classes']} "
            f"mixed_classes={stats['mixed_classes']} singleton_classes={stats['singleton_classes']} "
            f"largest_class={stats['largest_class']} target_+1={stats['target_+1']} "
            f"target_-1={stats['target_-1']} majority_score={majority_score:.9f} "
            f"baseline_score={baseline_score:.9f} class_lift={lift:.9f} exact_nontrivial={exact}"
        )


def print_order_checks(label: str, records: list[Record], limit: int) -> None:
    stats: Counter[str] = Counter()
    for point, _target in records[:limit]:
        stats["checked"] += 1
        if jac_is_inf(jac_mul(point, GROUP_ORDER)):
            stats["p_plus_1_zero"] += 1
        if jac_is_inf(jac_mul(point, GROUP_ORDER // 2)):
            stats["half_order_zero"] += 1
    print(f"{label}_order_check:")
    for key in ("checked", "p_plus_1_zero", "half_order_zero"):
        print(f"  {key}={stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:32")
    parser.add_argument("--draws-per-thread", type=int, default=256)
    parser.add_argument("--max-records", type=int, default=4096)
    parser.add_argument("--moduli", default="2,3,4,6,12")
    parser.add_argument("--order-check-limit", type=int, default=128)
    args = parser.parse_args()

    moduli = [int(x) for x in args.moduli.split(",") if x]
    domain_records, target_records, stats = collect_records(
        seeds=parse_range(args.seeds),
        chunks=parse_range(args.chunks),
        tids=parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
        max_records=args.max_records,
    )

    print("p27_trace_norm_elliptic_coset_gate")
    print(f"p={P}")
    print("curve:")
    print("  C: b^2=16-a^4")
    print("  E: v^2=u^3-u")
    print("  map: u=4/a^2, v=2b/a^3")
    print(f"  expected_order=p+1={GROUP_ORDER}")
    print(f"  observed_exponent_candidate=(p+1)/2={GROUP_EXPONENT_CANDIDATE}")
    print("sample:")
    for key in (
        "raw_draws",
        "nonsplit_y",
        "k_points",
        "domain_records",
        "target_records",
        "domain_inconsistent",
        "target_line_inconsistent",
        "domain_a_zero_skipped",
        "target_a_zero_skipped",
    ):
        print(f"  {key}={stats[key]}")
    print_order_checks("domain", domain_records, args.order_check_limit)
    print_order_checks("target", target_records, args.order_check_limit)
    print_projection_scores("domain", domain_records, moduli)
    print_projection_scores("target_line", target_records, moduli)
    print("p27_trace_norm_elliptic_coset_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
