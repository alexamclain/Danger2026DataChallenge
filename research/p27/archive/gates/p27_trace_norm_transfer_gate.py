#!/usr/bin/env python3
"""P27 trace/norm transfer gate from the p26 post-hit structure.

This is a bounded diagnostic, not a production search.  It asks whether the
p26 trace/norm structure survives for

    p = 10^27 + 103,  p mod 8 = 7.

The p26 structure was:

    F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
    K = -(y^2 - 2)(y^2 - 4y + 2)
    E_K: w^2 = K
    t = y - 1
    a = t - 1/t
    b = w(t^2 + 1)/t^2
    b^2 = 16 - a^4

and, on the F-square domain, the D orientation normalized by chi(y) descended
to the quotient.  Since p27 flips chi(2) relative to p26, every identity is
rechecked here before it is promoted as a source/filter candidate.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Callable, Optional


P = 1000000000000000000000000103
MASK64 = (1 << 64) - 1
GPU_CHUNK_CONST = 0xD1342543DE82EF95
GPU_TID_CONST = 0x9E3779B97F4A7C15
GPU_SEED_CONST = 0x7364529176530163


Point = tuple[int, int]
Transform = Callable[[int, int], Optional[Point]]


@dataclass
class Rng:
    s0: int
    s1: int

    def next64(self) -> int:
        s1 = self.s0
        s0 = self.s1
        self.s0 = s0
        s1 ^= (s1 << 23) & MASK64
        self.s1 = (s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)) & MASK64
        return (self.s1 + s0) & MASK64


def splitmix64_next(state: int) -> tuple[int, int]:
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    return state, (z ^ (z >> 31)) & MASK64


def cuda_rng(seed_offset: int, chunk_nonce: int, tid: int) -> Rng:
    seed = (
        seed_offset
        ^ ((chunk_nonce * GPU_CHUNK_CONST) & MASK64)
        ^ ((tid * GPU_TID_CONST) & MASK64)
        ^ GPU_SEED_CONST
    ) & MASK64
    seed, s0 = splitmix64_next(seed)
    seed, s1 = splitmix64_next(seed)
    if (s0 | s1) == 0:
        s1 = 1442695040888963407
    rng = Rng(s0, s1)
    for _ in range(200):
        rng.next64()
    return rng


def rand_below96(rng: Rng, p: int, mask: int) -> int:
    while True:
        a = rng.next64()
        b = rng.next64()
        value = (a | ((b & 0xFFFFFFFF) << 64)) & mask
        if value < p:
            return value


def inv(value: int) -> int:
    return pow(value % P, P - 2, P)


def chi(value: int | None) -> int:
    if value is None:
        return 0
    value %= P
    if value == 0:
        return 0
    r = pow(value, (P - 1) // 2, P)
    return 1 if r == 1 else -1


def sqrt_mod(value: int) -> int | None:
    value %= P
    if value == 0:
        return 0
    if chi(value) != 1:
        return None
    if P % 4 == 3:
        return pow(value, (P + 1) // 4, P)
    q = P - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while chi(z) != -1:
        z += 1
    m = s
    c = pow(z, q, P)
    t = pow(value, q, P)
    r = pow(value, (q + 1) // 2, P)
    while t != 1:
        i = 1
        tt = t * t % P
        while tt != 1:
            tt = tt * tt % P
            i += 1
            if i >= m:
                return None
        b = pow(c, 1 << (m - i - 1), P)
        m = i
        c = b * b % P
        t = t * c % P
        r = r * b % P
    return r


def sign_name(sign: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}.get(sign, "?")


def parse_range(raw: str) -> list[int]:
    if ":" in raw:
        lo, hi = raw.split(":", 1)
        return list(range(int(lo), int(hi)))
    if "," in raw:
        return [int(x) for x in raw.split(",") if x]
    return [int(raw)]


def parse_coeffs(raw: str) -> tuple[int, ...]:
    return tuple(int(x) for x in raw.split(",") if x)


def f_value(y: int) -> int:
    y %= P
    y2 = y * y % P
    return (y - 1) * (y2 - 2) % P * (y2 - 2 * y + 2) % P


def k_value(y: int) -> int:
    y %= P
    y2 = y * y % P
    return (-(y2 - 2) * (y2 - 4 * y + 2)) % P


def x16_y_predicts_nonsplit(y: int) -> bool:
    y %= P
    y2 = y * y % P
    f = (y2 - 2) * (y2 - 4 * y + 2) % P
    return f != 0 and chi(f) != 1


def branch_d_values(y: int, z: int, w: int) -> tuple[int, int, int, int]:
    y %= P
    y2 = y * y % P
    ym1 = (y - 1) % P
    ym2 = (y - 2) % P
    b_quad = (y2 - 2 * y + 2) % P
    c_quad = (y2 - 2) % P

    ch = 4 * c_quad % P * b_quad % P
    av = 8 * y % P * pow(ym1, 2, P) % P

    nh_scale = 8 * ym1 % P
    nh_scale_chi = chi(nh_scale)
    nv_scale_chi = chi(y * c_quad)
    chi_c = chi(c_quad)
    chi_2b = chi(2 * b_quad)
    x_pref = chi((-y * ym2) % P)
    if 0 in (nh_scale_chi, nv_scale_chi, chi_c, chi_2b, x_pref):
        return (0, 0, 0, 0)

    out: list[int] = []
    for z_sign, w_sign in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        sqrt_nh = nh_scale * z % P
        if nh_scale_chi * z_sign < 0:
            sqrt_nh = (-sqrt_nh) % P
        h = chi(2 * (ch + sqrt_nh))

        sqrt_nv_num = 4 * y % P * z % P * w % P
        if nv_scale_chi * z_sign * w_sign < 0:
            sqrt_nv_num = (-sqrt_nv_num) % P
        v_arg_num = (c_quad * av + sqrt_nv_num) % P
        vq = chi_2b * chi(2 * v_arg_num) * chi_c
        if h == 0 or vq == 0:
            out.append(0)
        else:
            out.append(-x_pref * vq * h)
    return tuple(out)  # type: ignore[return-value]


def d_on_k_point(y: int, w: int, stats: Counter[str] | None = None) -> int | None:
    f = f_value(y)
    if chi(f) != 1:
        return None
    z = sqrt_mod(f)
    if z is None:
        if stats is not None:
            stats["unexpected_f_sqrt_fail"] += 1
        return None
    dpp, dmp, _dpm, _dmm = branch_d_values(y, z, w % P)
    if dpp != dmp and stats is not None:
        stats["target_z_not_invariant"] += 1
    if dpp == 0 and stats is not None:
        stats["target_D_zero"] += 1
    return dpp


def collect_k_points(
    seeds: list[int],
    chunks: list[int],
    tids: list[int],
    draws_per_thread: int,
) -> tuple[list[Point], Counter[str]]:
    pbits = P.bit_length()
    mask = (1 << pbits) - 1
    seen_y: set[int] = set()
    points: list[Point] = []
    stats: Counter[str] = Counter()
    for seed in seeds:
        for chunk in chunks:
            for tid in tids:
                rng = cuda_rng(seed, chunk, tid)
                for _ in range(draws_per_thread):
                    y = rand_below96(rng, P, mask)
                    stats["raw_draws"] += 1
                    if y in seen_y:
                        stats["duplicate_y"] += 1
                        continue
                    seen_y.add(y)
                    if y == 0:
                        stats["zero_y"] += 1
                        continue
                    if not x16_y_predicts_nonsplit(y):
                        continue
                    stats["nonsplit_y"] += 1

                    k = k_value(y)
                    k_chi = chi(k)
                    stats[f"K_chi_{sign_name(k_chi)}"] += 1
                    if k_chi != 1:
                        continue
                    w0 = sqrt_mod(k)
                    if w0 is None:
                        stats["unexpected_k_sqrt_fail"] += 1
                        continue
                    f_chi = chi(f_value(y))
                    stats[f"F_chi_{sign_name(f_chi)}"] += 2
                    points.append((y % P, w0))
                    points.append((y % P, (-w0) % P))
    stats["k_points"] = len(points)
    return points, stats


def transform_neg_t(y: int, w: int) -> Point:
    return ((2 - y) % P, w % P)


def transform_inv_t(y: int, w: int) -> Point | None:
    t = (y - 1) % P
    if t == 0:
        return None
    t_inv = inv(t)
    return ((1 + t_inv) % P, w * t_inv % P * t_inv % P)


def transform_neg_inv_t(y: int, w: int) -> Point | None:
    t = (y - 1) % P
    if t == 0:
        return None
    t_inv = inv(t)
    return ((1 - t_inv) % P, w * t_inv % P * t_inv % P)


TRANSFORMS: tuple[tuple[str, Transform], ...] = (
    ("neg_t", transform_neg_t),
    ("inv_t", transform_inv_t),
    ("neg_inv_t", transform_neg_inv_t),
)


def audit_ek_transforms(points: list[Point]) -> dict[str, Counter[str]]:
    out: dict[str, Counter[str]] = {}
    for name, transform in TRANSFORMS:
        stats: Counter[str] = Counter()
        for y, w in points:
            stats["source_points"] += 1
            f_source = chi(f_value(y))
            stats[f"source_F_{sign_name(f_source)}"] += 1
            d_source = d_on_k_point(y, w, stats) if f_source == 1 else None
            if d_source is not None:
                stats["source_D_domain"] += 1
                stats[f"source_D_{sign_name(d_source)}"] += 1

            image = transform(y, w)
            if image is None:
                stats["undefined"] += 1
                continue
            stats["defined"] += 1
            y2, w2 = image
            if (w2 * w2 - k_value(y2)) % P != 0:
                stats["K_not_preserved"] += 1
                continue
            stats["K_preserved"] += 1

            f_image = chi(f_value(y2))
            stats[f"image_F_{sign_name(f_image)}"] += 1
            if f_source == f_image:
                stats["F_chi_equal"] += 1
            if f_source == -f_image:
                stats["F_chi_flipped"] += 1
            if f_source == 1 and f_image == 1:
                stats["domain_to_domain"] += 1
            elif f_source == 1:
                stats["domain_to_not_domain"] += 1

            d_image = d_on_k_point(y2, w2, stats) if f_image == 1 else None
            if d_source is None or d_image is None:
                continue
            stats["compare_rows"] += 1
            ratio = d_image * d_source
            if d_image == d_source:
                stats["D_invariant"] += 1
            elif d_image == -d_source:
                stats["D_anti_invariant"] += 1

            if name == "neg_inv_t":
                expected = chi((y - 1) * y % P * (y - 2))
                y_ratio = chi(y2 * inv(y) % P) if y % P else 0
                stats[f"neg_inv_ratio_{sign_name(ratio)}"] += 1
                if ratio == expected:
                    stats["neg_inv_ratio_matches_chi_t_y_ym2"] += 1
                if ratio == -expected:
                    stats["neg_inv_ratio_anti_chi_t_y_ym2"] += 1
                if ratio == y_ratio:
                    stats["neg_inv_ratio_matches_chi_image_y_over_y"] += 1
                if ratio == -y_ratio:
                    stats["neg_inv_ratio_anti_chi_image_y_over_y"] += 1
        out[name] = stats
    return out


def quotient_coordinates(y: int, w: int) -> tuple[int, int] | None:
    t = (y - 1) % P
    if t == 0:
        return None
    t_inv = inv(t)
    a = (t - t_inv) % P
    b = w % P * ((t * t + 1) % P) % P * inv(t * t) % P
    return a, b


def collect_quotient_rows(points: list[Point]) -> tuple[list[tuple[int, int, int]], Counter[str]]:
    rows: list[tuple[int, int, int]] = []
    stats: Counter[str] = Counter()
    seen: set[tuple[int, int, int]] = set()
    for y, w in points:
        if chi(f_value(y)) != 1:
            continue
        d = d_on_k_point(y, w, stats)
        y_chi = chi(y)
        if d is None or d == 0 or y_chi == 0:
            stats["target_unusable"] += 1
            continue
        coords = quotient_coordinates(y, w)
        if coords is None:
            stats["quotient_undefined"] += 1
            continue
        a, b = coords
        if (b * b - (16 - pow(a, 4, P))) % P != 0:
            stats["quotient_relation_fail"] += 1
            continue
        target = d * y_chi
        rows.append((a, b, target))
        seen.add((a, b, target))
        stats[f"target_{sign_name(target)}"] += 1
    stats["quotient_rows"] = len(rows)
    stats["quotient_unique_rows"] = len(seen)
    return rows, stats


def collect_domain_line_rows(points: list[Point]) -> tuple[list[tuple[int, int]], Counter[str]]:
    by_a: dict[int, int] = {}
    stats: Counter[str] = Counter()
    for y, w in points:
        coords = quotient_coordinates(y, w)
        if coords is None:
            stats["quotient_undefined"] += 1
            continue
        a, b = coords
        if (b * b - (16 - pow(a, 4, P))) % P != 0:
            stats["quotient_relation_fail"] += 1
            continue
        target = chi(f_value(y))
        stats[f"F_line_raw_{sign_name(target)}"] += 1
        if target == 0:
            stats["F_line_zero"] += 1
            continue
        old = by_a.get(a)
        if old is None:
            by_a[a] = target
        elif old != target:
            stats["F_line_inconsistent"] += 1
    rows = sorted(by_a.items())
    stats["domain_line_rows"] = len(rows)
    stats["domain_line_+1"] = sum(1 for _a, target in rows if target == 1)
    stats["domain_line_-1"] = sum(1 for _a, target in rows if target == -1)
    return rows, stats


def normalized_line_target(a: int, b: int, target: int, mode: str) -> int | None:
    a_chi = chi(a)
    b_chi = chi(b)
    if mode == "p26_Tline":
        if a_chi == 0 or b_chi == 0:
            return None
        return target if a_chi == 1 else target * b_chi
    if mode == "T":
        return target
    if mode == "T_b":
        return None if b_chi == 0 else target * b_chi
    if mode == "T_a":
        return None if a_chi == 0 else target * a_chi
    if mode == "T_ab":
        return None if a_chi == 0 or b_chi == 0 else target * a_chi * b_chi
    raise ValueError(mode)


def collect_target_line_rows(
    quotient_rows: list[tuple[int, int, int]],
    mode: str,
) -> tuple[list[tuple[int, int]], Counter[str]]:
    by_a: dict[int, int] = {}
    stats: Counter[str] = Counter()
    for a, b, target in quotient_rows:
        a_chi = chi(a)
        b_chi = chi(b)
        stats[f"a_chi_{sign_name(a_chi)}"] += 1
        stats[f"b_chi_{sign_name(b_chi)}"] += 1
        line_target = normalized_line_target(a, b, target, mode)
        if line_target is None or line_target == 0:
            stats["line_unusable"] += 1
            continue
        stats[f"line_target_raw_{sign_name(line_target)}"] += 1
        old = by_a.get(a)
        if old is None:
            by_a[a] = line_target
        elif old != line_target:
            stats["line_inconsistent"] += 1
    rows = sorted(by_a.items())
    stats["line_rows"] = len(rows)
    stats["line_target_+1"] = sum(1 for _a, target in rows if target == 1)
    stats["line_target_-1"] = sum(1 for _a, target in rows if target == -1)
    return rows, stats


def audit_b_flip(quotient_rows: list[tuple[int, int, int]]) -> Counter[str]:
    by_a: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for a, b, target in quotient_rows:
        by_a[a].append((b, target))
    stats: Counter[str] = Counter()
    for a, rows in by_a.items():
        seen: dict[int, int] = {}
        for b, target in rows:
            seen[b] = target
        for b, target in list(seen.items()):
            b2 = (-b) % P
            if b2 not in seen or b > b2:
                continue
            target2 = seen[b2]
            ratio = target2 * target
            a_chi = chi(a)
            b_chi = chi(b)
            stats["b_flip_pairs"] += 1
            stats[f"b_flip_ratio_{sign_name(ratio)}"] += 1
            if ratio == a_chi:
                stats["b_flip_ratio_matches_chi_a"] += 1
            if ratio == -a_chi:
                stats["b_flip_ratio_anti_chi_a"] += 1
            if ratio == b_chi:
                stats["b_flip_ratio_matches_chi_b"] += 1
            if ratio == -b_chi:
                stats["b_flip_ratio_anti_chi_b"] += 1
    return stats


def eval_poly(coeffs: tuple[int, ...], x: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x + coeff) % P
    return value


def trim_coeffs(coeffs: tuple[int, ...]) -> tuple[int, ...]:
    coeffs = tuple(c % P for c in coeffs)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs = coeffs[:-1]
    return coeffs


def pad_coeffs(coeffs: tuple[int, ...], degree: int) -> tuple[int, ...]:
    return coeffs + (0,) * (degree + 1 - len(coeffs))


def small_coeff_label(coeffs: tuple[int, ...]) -> str:
    vals: list[str] = []
    for coeff in coeffs:
        c = coeff
        if c > P // 2:
            c -= P
        vals.append(str(c))
    return "[" + ",".join(vals) + "]"


def score_poly(rows: list[tuple[int, int]], coeffs: tuple[int, ...]) -> tuple[int, int, int, int, int, float]:
    signs: list[int] = []
    targets: list[int] = []
    for a, target in rows:
        signs.append(chi(eval_poly(coeffs, a)))
        targets.append(target)
    zero = signs.count(0)
    exact_plus = int(zero == 0 and all(sign == target for sign, target in zip(signs, targets)))
    exact_minus = int(zero == 0 and all(-sign == target for sign, target in zip(signs, targets)))
    target_plus = sum(1 for target in targets if target == 1)
    baseline = target_plus / len(targets) if targets else 0.0
    best_good = best_total = 0
    best_lift = 0.0
    for orient in (1, -1):
        selected = [target for sign, target in zip(signs, targets) if sign and orient * sign == 1]
        if not selected or baseline == 0.0:
            continue
        good = sum(1 for target in selected if target == 1)
        lift = (good / len(selected)) / baseline
        if lift > best_lift:
            best_lift = lift
            best_good = good
            best_total = len(selected)
    return exact_plus, exact_minus, zero, best_good, best_total, best_lift


def search_polys(
    rows: list[tuple[int, int]],
    degree: int,
    coeff_values: tuple[int, ...],
    prefix_size: int,
    top: int,
) -> tuple[list[tuple[float, int, int, int, tuple[int, ...]]], Counter[str]]:
    stats: Counter[str] = Counter()
    prefix = rows[: min(prefix_size, len(rows))]
    stats["prefix_rows"] = len(prefix)
    prefix_survivors: list[tuple[int, ...]] = []
    for coeffs in product(coeff_values, repeat=degree + 1):
        if all(c == 0 for c in coeffs):
            continue
        coeffs_mod = tuple(c % P for c in coeffs)
        stats["candidate_count"] += 1
        exact_plus, exact_minus, zero, _good, _total, _lift = score_poly(prefix, coeffs_mod)
        if exact_plus or exact_minus:
            prefix_survivors.append(trim_coeffs(coeffs_mod))
        elif zero == 0:
            stats["prefix_nonzero_nonexact"] += 1
    stats["prefix_exact_survivors"] = len(prefix_survivors)

    top_rows: list[tuple[float, int, int, int, tuple[int, ...]]] = []
    exact_count = 0
    for coeffs in prefix_survivors:
        coeffs_full = pad_coeffs(coeffs, degree)
        exact_plus, exact_minus, zero, good, total, lift = score_poly(rows, coeffs_full)
        if exact_plus or exact_minus:
            exact_count += 1
        top_rows.append((lift, good, total, zero, trim_coeffs(coeffs_full)))
    stats["full_exact_count"] = exact_count
    top_rows.sort(reverse=True, key=lambda row: (row[0], row[1], -row[3]))
    return top_rows[:top], stats


def basis_scan(rows: list[tuple[int, int]], top: int) -> list[tuple[float, int, int, int, str]]:
    def basis(a: int) -> list[tuple[str, int]]:
        a %= P
        a2 = a * a % P
        return [
            ("a", chi(a)),
            ("a_minus_2", chi(a - 2)),
            ("a_plus_2", chi(a + 2)),
            ("a2_minus_4", chi(a2 - 4)),
            ("a2_plus_4", chi(a2 + 4)),
        ]

    signed_rows = [(basis(a), target) for a, target in rows]
    if not signed_rows:
        return []
    n_basis = len(signed_rows[0][0])
    scored: list[tuple[float, int, int, int, str]] = []
    for mask in range(1 << n_basis):
        agree = anti = zero = 0
        labels: list[str] = []
        for i in range(n_basis):
            if mask & (1 << i):
                labels.append(signed_rows[0][0][i][0])
        label = "*".join(labels) if labels else "1"
        for chars, target in signed_rows:
            value = 1
            for i, (_name, sign) in enumerate(chars):
                if mask & (1 << i):
                    if sign == 0:
                        value = 0
                        break
                    value *= sign
            if value == 0:
                zero += 1
            elif value == target:
                agree += 1
            elif value == -target:
                anti += 1
        best = max(agree, anti)
        score = best / len(rows)
        if anti > agree:
            label = "-" + label
        scored.append((score, agree, anti, zero, label))
    scored.sort(reverse=True, key=lambda row: (row[0], -row[3], max(row[1], row[2])))
    return scored[:top]


def print_counter_section(title: str, stats: Counter[str], keys: tuple[str, ...]) -> None:
    print(title)
    for key in keys:
        print(f"  {key}={stats[key]}")


def print_basis_and_poly(
    label: str,
    rows: list[tuple[int, int]],
    degree: int,
    coeffs: tuple[int, ...],
    prefix_size: int,
    top: int,
) -> Counter[str]:
    print(f"{label}_basis_character_scan:")
    for score, agree, anti, zero, basis_label in basis_scan(rows, top):
        print(f"  label={basis_label} score={score:.9f} agree={agree} anti={anti} zero={zero}")
    top_polys, stats = search_polys(rows, degree, coeffs, prefix_size, top)
    print(f"{label}_polynomial_search:")
    for key in ("candidate_count", "prefix_rows", "prefix_exact_survivors", "full_exact_count"):
        print(f"  {key}={stats[key]}")
    for rank, (lift, good, total, zero, poly_coeffs) in enumerate(top_polys, 1):
        print(
            "  top "
            f"rank={rank} lift={lift:.9f} good={good} total={total} zero={zero} "
            f"coeffs={small_coeff_label(poly_coeffs)}"
        )
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="121")
    parser.add_argument("--chunks", default="0,1")
    parser.add_argument("--tids", default="0:64")
    parser.add_argument("--draws-per-thread", type=int, default=128)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--coeffs", default="-1,0,1")
    parser.add_argument("--prefix-size", type=int, default=4096)
    parser.add_argument("--top", type=int, default=8)
    args = parser.parse_args()

    points, collect_stats = collect_k_points(
        seeds=parse_range(args.seeds),
        chunks=parse_range(args.chunks),
        tids=parse_range(args.tids),
        draws_per_thread=args.draws_per_thread,
    )
    ek_stats = audit_ek_transforms(points)
    quotient_rows, quotient_stats = collect_quotient_rows(points)
    b_flip_stats = audit_b_flip(quotient_rows)
    domain_rows, domain_stats = collect_domain_line_rows(points)

    line_modes = ("p26_Tline", "T", "T_b", "T_a", "T_ab")
    line_results: dict[str, tuple[list[tuple[int, int]], Counter[str]]] = {}
    for mode in line_modes:
        line_results[mode] = collect_target_line_rows(quotient_rows, mode)
    target_rows, target_stats = line_results["p26_Tline"]

    print("p27_trace_norm_transfer_gate")
    print(f"p={P}")
    print("normal_form:")
    print("  F=(y-1)*(y^2-2)*(y^2-2y+2)")
    print("  K=-(y^2-2)*(y^2-4y+2)")
    print("  t=y-1")
    print("  E_K: w^2=-t^4+6*t^2-1")
    print("  quotient_coords: a=t-1/t, b=w*(t^2+1)/t^2")
    print("  quotient_curve: b^2=16-a^4")
    print("sample:")
    for key in (
        "raw_draws",
        "duplicate_y",
        "zero_y",
        "nonsplit_y",
        "K_chi_+1",
        "K_chi_-1",
        "F_chi_+1",
        "F_chi_-1",
        "F_chi_0",
        "k_points",
    ):
        print(f"  {key}={collect_stats[key]}")

    print("ek_automorphisms:")
    for name in ("neg_t", "inv_t", "neg_inv_t"):
        stats = ek_stats[name]
        print(f"  transform={name}")
        for key in (
            "source_points",
            "defined",
            "K_preserved",
            "K_not_preserved",
            "source_D_domain",
            "domain_to_domain",
            "domain_to_not_domain",
            "compare_rows",
            "D_invariant",
            "D_anti_invariant",
            "neg_inv_ratio_matches_chi_t_y_ym2",
            "neg_inv_ratio_anti_chi_t_y_ym2",
            "neg_inv_ratio_matches_chi_image_y_over_y",
            "neg_inv_ratio_anti_chi_image_y_over_y",
        ):
            if key.startswith("neg_inv") and name != "neg_inv_t":
                continue
            print(f"    {key}={stats[key]}")

    print_counter_section(
        "quotient:",
        quotient_stats,
        (
            "quotient_rows",
            "quotient_unique_rows",
            "quotient_undefined",
            "quotient_relation_fail",
            "target_+1",
            "target_-1",
        ),
    )
    print_counter_section(
        "b_flip_cocycle:",
        b_flip_stats,
        (
            "b_flip_pairs",
            "b_flip_ratio_+1",
            "b_flip_ratio_-1",
            "b_flip_ratio_matches_chi_a",
            "b_flip_ratio_anti_chi_a",
            "b_flip_ratio_matches_chi_b",
            "b_flip_ratio_anti_chi_b",
        ),
    )

    print_counter_section(
        "domain_line:",
        domain_stats,
        (
            "quotient_undefined",
            "quotient_relation_fail",
            "F_line_raw_+1",
            "F_line_raw_-1",
            "F_line_raw_0",
            "domain_line_rows",
            "F_line_inconsistent",
            "domain_line_+1",
            "domain_line_-1",
        ),
    )
    domain_poly_stats = print_basis_and_poly(
        "domain_line",
        domain_rows,
        args.degree,
        parse_coeffs(args.coeffs),
        args.prefix_size,
        args.top,
    )

    print("target_line_modes:")
    for mode in line_modes:
        _rows, stats = line_results[mode]
        print(
            "  "
            f"mode={mode} line_rows={stats['line_rows']} "
            f"line_inconsistent={stats['line_inconsistent']} "
            f"line_unusable={stats['line_unusable']} "
            f"line_target_+1={stats['line_target_+1']} "
            f"line_target_-1={stats['line_target_-1']}"
        )
    print_counter_section(
        "target_line_p26_Tline:",
        target_stats,
        (
            "a_chi_+1",
            "a_chi_-1",
            "b_chi_+1",
            "b_chi_-1",
            "line_rows",
            "line_inconsistent",
            "line_unusable",
            "line_target_+1",
            "line_target_-1",
        ),
    )
    target_poly_stats = print_basis_and_poly(
        "target_line",
        target_rows,
        args.degree,
        parse_coeffs(args.coeffs),
        args.prefix_size,
        args.top,
    )

    domain_consistent = int(domain_stats["F_line_inconsistent"] == 0)
    target_consistent = int(target_stats["line_inconsistent"] == 0)
    neg_inv_cocycle = int(
        ek_stats["neg_inv_t"]["compare_rows"] > 0
        and ek_stats["neg_inv_t"]["neg_inv_ratio_matches_chi_t_y_ym2"]
        == ek_stats["neg_inv_t"]["compare_rows"]
    )
    b_flip_cocycle = int(
        b_flip_stats["b_flip_pairs"] > 0
        and b_flip_stats["b_flip_ratio_matches_chi_a"] == b_flip_stats["b_flip_pairs"]
    )
    print("verdict:")
    print(f"  neg_inv_cocycle_exact={neg_inv_cocycle}")
    print(f"  quotient_relation_exact={int(quotient_stats['quotient_relation_fail'] == 0)}")
    print(f"  b_flip_cocycle_exact={b_flip_cocycle}")
    print(f"  domain_line_consistent={domain_consistent}")
    print(f"  target_line_p26_Tline_consistent={target_consistent}")
    print(f"  domain_line_polynomial_exact_found={int(domain_poly_stats['full_exact_count'] > 0)}")
    print(f"  target_line_polynomial_exact_found={int(target_poly_stats['full_exact_count'] > 0)}")
    print("p27_trace_norm_transfer_gate_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

