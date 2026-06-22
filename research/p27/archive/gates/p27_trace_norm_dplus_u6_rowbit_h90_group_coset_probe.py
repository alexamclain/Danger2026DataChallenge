#!/usr/bin/env python3
"""Group-coset screen for the H90-soluble Dplus U6 row bit.

The solubility-boundary probe shows that the row bit is uniform exactly on
H90-soluble t-fibers.  This asks the next cheap structural question:

    is the soluble-side plus/minus sign a small elliptic group quotient class?

Using the known maps

    E_h90: w^2 = -t^4 + 6*t^2 - 1
    a = t - 1/t
    b = w*(t^2+1)/t^2
    C: b^2 = 16 - a^4
    E: v^2 = u^3 - u,  u = 4/a^2,  v = 2b/a^3

the probe projects H90-soluble row-bit records to small quotients of
E(F_q).  Pure quotient classes would be a concrete source/coset candidate.
Mixed classes kill that small group-character explanation.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from typing import Optional

from p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe import (
    chi,
    h90_values,
    inv,
    parse_fields,
    roots_square,
    row_signs_for_t,
    sign_name,
)


Affine = Optional[tuple[int, int]]
Jacobian = tuple[int, int, int]
Record = tuple[Affine, int]


def normalize_signs(values: list[int]) -> int | None:
    signs = {value for value in values if value in (-1, 1)}
    if not signs:
        return None
    if len(signs) == 1:
        return signs.pop()
    return 0


def affine_from_h90(t: int, w: int, q: int) -> Affine:
    t %= q
    w %= q
    if t == 0:
        return None
    t2 = t * t % q
    a = (t - inv(t, q)) % q
    if a == 0:
        return None
    b = w * (t2 + 1) % q * inv(t2, q) % q
    if (b * b - (16 - pow(a, 4, q))) % q != 0:
        raise RuntimeError("bad H90 -> C map")
    a2 = a * a % q
    u = 4 * inv(a2, q) % q
    v = 2 * b % q * inv(a2 * a % q, q) % q
    if (v * v - (u * u % q * u - u)) % q != 0:
        raise RuntimeError("bad C -> E map")
    return u, v


def jac_from_affine(point: Affine, q: int) -> Jacobian:
    if point is None:
        return (0, 1, 0)
    x, y = point
    return (x % q, y % q, 1)


def jac_is_inf(point: Jacobian, q: int) -> bool:
    return point[2] % q == 0


def jac_double(point: Jacobian, q: int) -> Jacobian:
    x1, y1, z1 = point
    if z1 == 0 or y1 == 0:
        return (0, 1, 0)
    ec_a = q - 1
    xx = x1 * x1 % q
    yy = y1 * y1 % q
    yyyy = yy * yy % q
    zz = z1 * z1 % q
    s = 2 * (((x1 + yy) * (x1 + yy) - xx - yyyy) % q) % q
    m = (3 * xx + ec_a * zz % q * zz) % q
    x3 = (m * m - 2 * s) % q
    y3 = (m * (s - x3) - 8 * yyyy) % q
    z3 = ((y1 + z1) * (y1 + z1) - yy - zz) % q
    return x3, y3, z3


def jac_add(p1: Jacobian, p2: Jacobian, q: int) -> Jacobian:
    if jac_is_inf(p1, q):
        return p2
    if jac_is_inf(p2, q):
        return p1
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    z1z1 = z1 * z1 % q
    z2z2 = z2 * z2 % q
    u1 = x1 * z2z2 % q
    u2 = x2 * z1z1 % q
    s1 = y1 * z2 % q * z2z2 % q
    s2 = y2 * z1 % q * z1z1 % q
    h = (u2 - u1) % q
    r = (s2 - s1) % q
    if h == 0:
        if r == 0:
            return jac_double(p1, q)
        return (0, 1, 0)
    hh = h * h % q
    hhh = h * hh % q
    v = u1 * hh % q
    x3 = (r * r - hhh - 2 * v) % q
    y3 = (r * (v - x3) - s1 * hhh) % q
    z3 = h * z1 % q * z2 % q
    return x3, y3, z3


def jac_mul(point: Affine, scalar: int, q: int) -> Jacobian:
    result = (0, 1, 0)
    addend = jac_from_affine(point, q)
    n = scalar
    while n:
        if n & 1:
            result = jac_add(result, addend, q)
        addend = jac_double(addend, q)
        n >>= 1
    return result


def affine_from_jac(point: Jacobian, q: int) -> Affine:
    x, y, z = point
    if z == 0:
        return None
    zinv = inv(z, q)
    z2 = zinv * zinv % q
    z3 = z2 * zinv % q
    return x * z2 % q, y * z3 % q


def canonical_point_key(point: Affine, q: int) -> tuple[str, int, int]:
    if point is None:
        return ("O", 0, 0)
    x, y = point
    return ("P", x, min(y, (-y) % q))


def elliptic_order(q: int) -> int:
    total = 1
    for x in range(q):
        rhs = (x * x % q * x - x) % q
        c = chi(rhs, q)
        total += 1 if c == 0 else 2 if c == 1 else 0
    return total


def collect_records(q: int, materialization_filters: bool) -> tuple[list[Record], Counter[str]]:
    records: list[Record] = []
    stats: Counter[str] = Counter()
    by_point: dict[tuple[str, int, int], int] = {}
    for t in range(1, q):
        signs = row_signs_for_t(t, q, materialization_filters)
        target = normalize_signs(signs)
        if target is None:
            stats["empty_t"] += 1
            continue
        if target == 0:
            stats["mixed_t_skipped"] += 1
            continue
        _B, _C, _Fspin, Ktrace = h90_values(t, q)
        w_roots = roots_square(Ktrace, q)
        if not w_roots:
            stats["uniform_t_without_h90_point"] += 1
            continue
        stats["uniform_t_with_h90_point"] += 1
        stats[f"target_{sign_name(target)}"] += 1
        for w in w_roots:
            point = affine_from_h90(t, w, q)
            if point is None:
                stats["h90_point_at_infinity_or_undefined"] += 1
                continue
            key = canonical_point_key(point, q)
            old = by_point.get(key)
            if old is not None and old != target:
                stats["point_target_inconsistent"] += 1
                continue
            by_point[key] = target
    for key, target in by_point.items():
        if key[0] == "O":
            point = None
        else:
            point = (key[1], key[2])
        records.append((point, target))
    stats["records"] = len(records)
    return records, stats


def score_projection(records: list[Record], q: int, order: int, modulus: int) -> Counter[str]:
    stats: Counter[str] = Counter()
    if order % modulus != 0:
        stats["skipped_order_not_divisible"] = 1
        return stats
    cofactor = order // modulus
    by_class: dict[tuple[str, int, int], Counter[int]] = defaultdict(Counter)
    for point, target in records:
        projected = affine_from_jac(jac_mul(point, cofactor, q), q)
        by_class[canonical_point_key(projected, q)][target] += 1
        stats["rows"] += 1
        stats[f"target_{sign_name(target)}"] += 1
    for counts in by_class.values():
        total = counts[1] + counts[-1]
        stats["classes"] += 1
        stats["largest_class"] = max(stats["largest_class"], total)
        stats["majority"] += max(counts[1], counts[-1])
        if counts[1] and counts[-1]:
            stats["mixed_classes"] += 1
        if total == 1:
            stats["singleton_classes"] += 1
    plus = stats["target_plus"]
    minus = stats["target_minus"]
    stats["baseline_majority"] = max(plus, minus)
    if stats["rows"]:
        stats["majority_x1000000"] = stats["majority"] * 1_000_000 // stats["rows"]
        stats["baseline_x1000000"] = stats["baseline_majority"] * 1_000_000 // stats["rows"]
    stats["both_signs_present"] = int(plus > 0 and minus > 0)
    stats["exact_nontrivial"] = int(
        stats["both_signs_present"]
        and stats["mixed_classes"] == 0
        and stats["singleton_classes"] < stats["classes"]
    )
    return stats


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, moduli: list[int], materialization_filters: bool) -> Counter[str]:
    order = elliptic_order(q)
    records, stats = collect_records(q, materialization_filters)
    stats["elliptic_order"] = order
    stats["q_plus_1"] = q + 1
    print_counter(f"q{q}", stats)
    aggregate = Counter(stats)
    for modulus in moduli:
        pstats = score_projection(records, q, order, modulus)
        if pstats["skipped_order_not_divisible"]:
            continue
        print_counter(f"q{q}_projection_m{modulus}", pstats)
        aggregate[f"m{modulus}_mixed_classes"] += pstats["mixed_classes"]
        aggregate[f"m{modulus}_exact_nontrivial"] += pstats["exact_nontrivial"]
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="263,607,1607,1847,2087")
    parser.add_argument("--moduli", default="2,3,4,6,8,12,16,24")
    parser.add_argument("--include-bare", action="store_true")
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    moduli = [int(part) for part in args.moduli.replace(",", " ").split() if part.strip()]
    print("p27 trace/norm Dplus U6 row-bit H90 group-coset probe")
    print("question = is the H90-soluble row bit a small quotient class on E: v^2=u^3-u?")
    print(f"fields = {','.join(str(q) for q in fields)}")
    print(f"moduli = {','.join(str(m) for m in moduli)}")

    exact_total = 0
    for materialization_filters in ([True, False] if args.include_bare else [True]):
        print(f"materialization_filters = {int(materialization_filters)}")
        for q in fields:
            aggregate = run_field(q, moduli, materialization_filters)
            exact_total += sum(value for key, value in aggregate.items() if key.endswith("_exact_nontrivial"))

    print("verdict:")
    print("  exact nontrivial quotient classes promote an elliptic-coset source candidate")
    print("  mixed projected classes kill the tested small group quotient explanation")
    print(f"exact_nontrivial_projection_total = {exact_total}")
    print("p27_trace_norm_dplus_u6_rowbit_h90_group_coset_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
