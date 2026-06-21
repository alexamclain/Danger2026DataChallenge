#!/usr/bin/env python3
"""P27 label-2 alpha/T-deck and branch recurrence probe.

The order-4 lift makes compactD=-1 a meaningful second-gate stratum, but the
sqrt-beating question is whether that stratum gives any deterministic handle on
the next selected halving gate.  This probe samples p27 residual-E label-2 rows,
pairs the two T-deck roots, enumerates the two second-halving x-branches, and
measures the next d3 squareclass.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter


P = 1000000000000000000000000103
FEATURES = [
    "X",
    "W",
    "X-1",
    "X+1",
    "X2+1",
    "X2+2X-1",
    "X2-2X-1",
    "S",
    "S_conj",
    "mt_linear",
    "m0",
    "mt_coeff",
    "prefactor",
    "L",
]


def inv(a: int, p: int = P) -> int:
    return pow(a % p, p - 2, p)


def legendre(a: int, p: int = P) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def sqrt_mod(a: int, p: int = P) -> int | None:
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
        return None
    # p27 is 3 mod 4.
    r = pow(a, (p + 1) // 4, p)
    if r * r % p != a:
        return None
    return r


def x16_a_num(y: int, p: int = P) -> int:
    num = 1
    for coeff in [-8, 24, -32, 8, 32, -48, 32, -8]:
        num = (num * y + coeff) % p
    return num


def root_to_a_xp(root: int, y: int, p: int = P) -> tuple[int, int] | None:
    ym1 = (y - 1) % p
    den_a = 4 * pow(ym1, 4, p) % p
    den_x = (root - y) % p
    if den_a == 0 or den_x == 0:
        return None
    a = x16_a_num(y, p) * inv(den_a, p) % p
    xp = root * inv(den_x, p) % p
    if a <= 2 or a >= p - 2:
        return None
    return a, xp


def halve_known_d(x: int, sd: int, p: int = P) -> list[int]:
    out: list[int] = []
    inv2 = (p + 1) // 2
    for rd in [sd % p, (-sd) % p]:
        u = (2 * x + 2 * rd) % p
        w = (u * u - 4) % p
        sw = sqrt_mod(w, p)
        if sw is None:
            continue
        for cand in [((u + sw) * inv2) % p, ((u - sw) * inv2) % p]:
            if cand and cand not in out:
                out.append(cand)
    return out


def halve_all(a: int, x: int, p: int = P) -> tuple[int, list[int]]:
    d = (x * x + a * x + 1) % p
    sd = sqrt_mod(d, p)
    if sd is None:
        return legendre(d, p), []
    return 1, halve_known_d(x, sd, p)


def compact_class(x: int, w: int, t: int, p: int = P) -> int:
    x2 = x * x % p
    x3 = x2 * x % p
    x4 = x2 * x2 % p
    x5 = x4 * x % p
    x6 = x5 * x % p
    mt = (2 * w * x2 + 2 * w * x + x4 + 2 * x3 - 2 * x - 1) % p
    m0 = (
        w * x5
        + 3 * w * x4
        + 2 * w * x3
        + 2 * w * x2
        + w * x
        - w
        + 2 * x6
        + 4 * x5
        + 4 * x3
        - 2 * x2
    ) % p
    if x == 0:
        return 0
    v = w * (x2 + 1) * inv(x2, p) % p
    criterion = x * v % p
    criterion = criterion * ((m0 + mt * t) % p) % p
    c = legendre(criterion, p)
    return -c


def feature_values(x: int, w: int, p: int = P) -> dict[str, int]:
    x2 = x * x % p
    x3 = x2 * x % p
    s = (w * (x + 1) + 2 * x2) % p
    sm = (w * (x + 1) - 2 * x2) % p
    mtlin = (2 * w * x + x3 + x2 - x - 1) % p
    m0 = (x2 + 1) * (x2 + 2 * x - 1) * s % p
    mt = (x + 1) * mtlin % p
    pref = w * (x2 + 1) * inv(x, p) % p
    linear_l = (4 * w * x2 + 4 * w * x + x2 * x2 + 6 * x3 - 2 * x - 1) % p
    return {
        "X": x,
        "W": w,
        "X-1": x - 1,
        "X+1": x + 1,
        "X2+1": x2 + 1,
        "X2+2X-1": x2 + 2 * x - 1,
        "X2-2X-1": x2 - 2 * x - 1,
        "S": s,
        "S_conj": sm,
        "mt_linear": mtlin,
        "m0": m0,
        "mt_coeff": mt,
        "prefactor": pref,
        "L": linear_l,
    }


def bit_pm1(v: int) -> int:
    if v == 1:
        return 0
    if v == -1:
        return 1
    raise ValueError(v)


def popcount(n: int) -> int:
    return bin(n).count("1")


def combo_name(mask: int) -> str:
    names = [FEATURES[i] for i in range(len(FEATURES)) if (mask >> i) & 1]
    return " * ".join(names) if names else "1"


def find_exact_combo(rows: list[tuple[int, int]]) -> int | None:
    if not rows:
        return None
    for combo in range(1 << len(FEATURES)):
        if all((popcount(mask & combo) & 1) == target for mask, target in rows):
            return combo
    return None


def best_combos(rows: list[tuple[int, int]], limit: int = 8) -> list[tuple[int, int, int]]:
    scored = []
    for combo in range(1 << len(FEATURES)):
        good = 0
        for mask, target in rows:
            good += (popcount(mask & combo) & 1) == target
        scored.append((good, popcount(combo), combo))
    scored.sort(key=lambda item: (-item[0], item[1], item[2]))
    return scored[:limit]


def label2_candidate(x: int, w: int, t: int, root_index: int, p: int = P) -> tuple[str, dict[str, object] | None]:
    if x in (0, 1):
        return "degenerate", None
    y = 2 * x * inv(x - 1, p) % p
    y2 = y * y % p
    y3 = y2 * y % p
    nonsplit = (y2 - 2) * (y2 - 4 * y + 2) % p
    if legendre(nonsplit, p) != -1:
        return "not_nonsplit", None
    qa = (y2 - 2 * y) % p
    qb = (2 * y2 - y3) % p
    if qa == 0:
        return "degenerate", None
    sd = 4 * t % p
    sd = sd * inv(pow(x - 1, 3, p), p) % p
    root = ((sd if root_index == 0 else -sd) - qb) % p
    root = root * inv(2 * qa, p) % p
    ax = root_to_a_xp(root, y, p)
    if ax is None:
        return "degenerate", None
    a, xp = ax
    z = w * sd % p * inv(2 * x, p) % p
    den = 2 * (root - y) % p * pow(y - 1, 2, p) % p
    if den == 0:
        return "degenerate", None
    sd1 = y * z % p * inv(den, p) % p
    d1 = (xp * xp + a * xp + 1) % p
    if sd1 * sd1 % p != d1:
        return "d1_sqrt_mismatch", None
    x5s = halve_known_d(xp, sd1, p)
    if not x5s:
        return "d1_no_half", None
    x5 = x5s[0]
    d2_chi, x6s = halve_all(a, x5, p)
    d3_classes = [legendre(x6 * x6 + a * x6 + 1, p) for x6 in x6s]
    d4_groups = []
    for x6, d3_class in zip(x6s, d3_classes):
        if d3_class != 1:
            continue
        _, x7s = halve_all(a, x6, p)
        d4_groups.append([legendre(x7 * x7 + a * x7 + 1, p) for x7 in x7s])
    return "ok", {
        "A": a,
        "x5": x5,
        "d2_chi": d2_chi,
        "x6_count": len(x6s),
        "d3_classes": d3_classes,
        "d3_plus": sum(1 for c in d3_classes if c == 1),
        "d3_zero": sum(1 for c in d3_classes if c == 0),
        "d4_groups": d4_groups,
    }


def sample_rows(target: int, seed: int, max_draws: int, p: int = P) -> tuple[list[dict[str, object]], Counter]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    stats: Counter = Counter()
    while len(rows) < target and stats["x_draws"] < max_draws:
        stats["x_draws"] += 1
        x = rng.randrange(1, p)
        f = (x * x * x - x) % p
        w0 = sqrt_mod(f, p)
        if w0 is None:
            stats["no_w"] += 1
            continue
        t2 = x * (x * x + 1) % p * ((x * x + 2 * x - 1) % p) % p
        t0 = sqrt_mod(t2, p)
        if t0 is None:
            stats["no_t"] += 1
            continue
        for w in [w0, (-w0) % p] if w0 else [0]:
            comp = compact_class(x, w, t0, p)
            comp_neg = compact_class(x, w, (-t0) % p, p)
            if comp != comp_neg:
                stats["compact_t_mismatch"] += 1
                continue
            if comp != -1:
                stats["compact_not_target"] += 1
                continue
            pair = []
            for ri, t in enumerate([t0, (-t0) % p]):
                reason, cand = label2_candidate(x, w, t, ri, p)
                if cand is None:
                    stats[f"candidate_invalid_{reason}"] += 1
                    pair.append(None)
                else:
                    pair.append(cand)
            if pair[0] is None or pair[1] is None:
                stats["pair_incomplete"] += 1
                continue
            rows.append({"X": x, "W": w, "root0": pair[0], "root1": pair[1]})
            if len(rows) >= target:
                break
    return rows, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--max-draws", type=int, default=500000)
    args = parser.parse_args()

    rows, stats = sample_rows(args.target, args.seed, args.max_draws)
    branch_hist: Counter = Counter()
    pair_hist: Counter = Counter()
    feature_rows: list[tuple[int, int]] = []
    feature_zero_skips = 0
    d2_fail = 0
    total_roots = 0
    total_branches = 0
    d3_plus = 0
    d3_zero = 0
    d4_hist: Counter = Counter()
    d4_pair_hist: Counter = Counter()
    total_d3plus_x6 = 0
    total_x7_branches = 0
    d4_plus = 0
    d4_zero = 0
    any_plus_pair = 0
    all_plus_pair = 0
    root_plus = [0, 0]
    root_branches = [0, 0]

    for row in rows:
        pair_plus = 0
        pair_branches = 0
        pair_d4_plus = 0
        pair_d4_branches = 0
        root_counts = []
        for ri, key in enumerate(["root0", "root1"]):
            cand = row[key]
            assert isinstance(cand, dict)
            total_roots += 1
            if cand["d2_chi"] != 1:
                d2_fail += 1
            nbranches = int(cand["x6_count"])
            nplus = int(cand["d3_plus"])
            nzero = int(cand["d3_zero"])
            branch_hist[(nbranches, nplus, nzero)] += 1
            root_counts.append(nplus)
            root_branches[ri] += nbranches
            root_plus[ri] += nplus
            total_branches += nbranches
            d3_plus += nplus
            d3_zero += nzero
            pair_plus += nplus
            pair_branches += nbranches
            d4_groups = cand["d4_groups"]
            assert isinstance(d4_groups, list)
            for group in d4_groups:
                total_d3plus_x6 += 1
                n7 = len(group)
                n4plus = sum(1 for c in group if c == 1)
                n4zero = sum(1 for c in group if c == 0)
                d4_hist[(n7, n4plus, n4zero)] += 1
                total_x7_branches += n7
                d4_plus += n4plus
                d4_zero += n4zero
                pair_d4_plus += n4plus
                pair_d4_branches += n7
        pair_hist[tuple(root_counts)] += 1
        if pair_d4_branches:
            d4_pair_hist[(pair_d4_branches, pair_d4_plus)] += 1
        if root_counts in ([0, 0], [2, 2]):
            vals = feature_values(int(row["X"]), int(row["W"]))
            mask = 0
            skip = False
            for i, name in enumerate(FEATURES):
                c = legendre(vals[name])
                if c == 0:
                    skip = True
                    break
                mask |= bit_pm1(c) << i
            if skip:
                feature_zero_skips += 1
            else:
                feature_rows.append((mask, 0 if root_counts == [2, 2] else 1))
        if pair_plus:
            any_plus_pair += 1
        if pair_branches and pair_plus == pair_branches:
            all_plus_pair += 1

    print("p27 label2 alpha/T-deck branch recurrence probe")
    print(f"p = {P}")
    print(f"target_pairs = {args.target}")
    print(f"seed = {args.seed}")
    print(f"sampled_pairs = {len(rows)}")
    for key in sorted(stats):
        print(f"sample_stat {key} = {stats[key]}")
    print(f"total_roots = {total_roots}")
    print(f"d2_fail_after_compactDneg = {d2_fail}")
    print(f"total_x6_branches = {total_branches}")
    print(f"d3_plus_branches = {d3_plus}")
    print(f"d3_zero_branches = {d3_zero}")
    print(
        "d3_plus_branch_rate = "
        f"{(d3_plus / total_branches) if total_branches else 0.0:.9f}"
    )
    print(
        "root0_d3_plus_rate = "
        f"{(root_plus[0] / root_branches[0]) if root_branches[0] else 0.0:.9f}"
    )
    print(
        "root1_d3_plus_rate = "
        f"{(root_plus[1] / root_branches[1]) if root_branches[1] else 0.0:.9f}"
    )
    print(
        "paired_T_orbit_any_d3_plus_rate = "
        f"{(any_plus_pair / len(rows)) if rows else 0.0:.9f}"
    )
    print(
        "paired_T_orbit_all_d3_plus_rate = "
        f"{(all_plus_pair / len(rows)) if rows else 0.0:.9f}"
    )
    print("per_root_branch_hist nbranches n_d3_plus n_d3_zero count rate")
    for (nbranches, nplus, nzero), count in sorted(branch_hist.items()):
        print(
            f"  {nbranches} {nplus} {nzero} {count} "
            f"{(count / total_roots) if total_roots else 0.0:.9f}"
        )
    print("paired_T_root_d3_plus_hist root0_plus root1_plus count rate")
    for (r0, r1), count in sorted(pair_hist.items()):
        print(f"  {r0} {r1} {count} {(count / len(rows)) if rows else 0.0:.9f}")
    print(f"total_d3plus_x6 = {total_d3plus_x6}")
    print(f"total_x7_branches = {total_x7_branches}")
    print(f"d4_plus_branches = {d4_plus}")
    print(f"d4_zero_branches = {d4_zero}")
    print(
        "d4_plus_branch_rate_after_d3 = "
        f"{(d4_plus / total_x7_branches) if total_x7_branches else 0.0:.9f}"
    )
    print("per_d3plus_x6_d4_branch_hist nbranches n_d4_plus n_d4_zero count rate")
    for (nbranches, nplus, nzero), count in sorted(d4_hist.items()):
        print(
            f"  {nbranches} {nplus} {nzero} {count} "
            f"{(count / total_d3plus_x6) if total_d3plus_x6 else 0.0:.9f}"
        )
    print("paired_T_orbit_d4_plus_hist x7_branches d4_plus count rate")
    d4_pair_total = sum(d4_pair_hist.values())
    for (nbranches, nplus), count in sorted(d4_pair_hist.items()):
        print(f"  {nbranches} {nplus} {count} {(count / d4_pair_total) if d4_pair_total else 0.0:.9f}")
    exact = find_exact_combo(feature_rows)
    print("d3_visible_residual_E_character_screen:")
    print("  features = " + ", ".join(FEATURES))
    print(f"  rows = {len(feature_rows)}")
    print(f"  zero_feature_skips = {feature_zero_skips}")
    print(f"  exact_combo = {combo_name(exact) if exact is not None else 'none'}")
    print("  best_combos:")
    for good, weight, combo in best_combos(feature_rows):
        rate = good / len(feature_rows) if feature_rows else 0.0
        print(f"    good={good}/{len(feature_rows)} rate={rate:.9f} weight={weight} combo={combo_name(combo)}")
    print("p27_label2_alpha_branch_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
