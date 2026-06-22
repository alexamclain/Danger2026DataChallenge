#!/usr/bin/env python3
"""Obvious sign-quotient screen for the p27 conic tower.

The repeated conic selector is exact, but a sqrt-beating source needs a
quotient/sampler for the legal tower.  This probe asks the first cheap
quotient question: if we forget the natural square-root and reciprocal signs,
is the next selector still well-defined?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable

from p27_conic_pair_d4_recurrence_probe import conic_lifts_modsqrt, roots_mod
from p27_conic_pair_d5_tower_probe import transition_lifts_modsqrt
from p27_conic_pair_two_step_kummer_probe import selector_data, two_step_rows
from p27_label2_alpha_branch_recurrence_probe import P, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row


SYSTEMS: dict[str, tuple[str, ...]] = {
    "base_A": ("A",),
    "base_Ax": ("A", "x0"),
    "first_signed": ("A", "x0", "c", "r0", "R0", "L0"),
    "first_unsigned": ("A", "x0", "c2", "u0", "w0", "m0"),
    "first_square": ("A", "x0", "c2", "R0sq", "L0sq", "a0sq"),
    "two_signed": ("A", "x0", "c", "r0", "R0", "L0", "R1", "L1"),
    "two_drop_L1_sign": ("A", "x0", "c", "r0", "R0", "L0", "R1", "L1sq", "w1"),
    "two_square": ("A", "x0", "c2", "R0sq", "L0sq", "R1sq", "L1sq", "a1sq", "w1"),
    "two_reciprocal": ("A", "x0", "c2", "u0", "w0", "m0", "u1", "w1", "m1"),
    "two_selector_signless": ("A", "x0", "c2", "u0", "w0", "S0", "u1", "w1"),
    "z0_signless": ("A", "x0", "c2", "u0", "w0", "Z0sq", "u1", "w1", "m1"),
}


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def maybe_div(a: int, b: int, p: int) -> int | None:
    ib = inv(b, p)
    if ib is None:
        return None
    return a * ib % p


def add_derived(row: dict[str, int | None], p: int) -> dict[str, int | None]:
    out = dict(row)
    for name in ["c", "r0", "R0", "L0", "R1", "L1", "a0", "a1", "Z0"]:
        value = out.get(name)
        if value is not None:
            out[f"{name}sq"] = value * value % p
    if out.get("c") is not None:
        out["c2"] = int(out["c"]) * int(out["c"]) % p

    for prefix in ["0", "1"]:
        R = out.get(f"R{prefix}")
        L = out.get(f"L{prefix}")
        a = out.get(f"a{prefix}")
        if R is not None:
            iR = inv(R, p)
            if iR is not None:
                out[f"u{prefix}"] = (R + iR) % p
                out[f"v{prefix}"] = (R - iR) % p
        if L is not None and a is not None:
            ia = a * a % p
            out[f"a{prefix}sq"] = ia
            out[f"w{prefix}"] = (L * L - ia) % p
            il = inv(L, p)
            if il is not None:
                out[f"m{prefix}"] = (L + ia * il) % p
                out[f"n{prefix}"] = (L - ia * il) % p

    z0 = out.get("Z0")
    if z0 is not None:
        out["Z0sq"] = z0 * z0 % p
    return out


def p27_selector_rows(target: int, seed: int, max_draws: int) -> tuple[list[dict[str, int | None]], Counter]:
    rows, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in rows:
        candidates.extend(all_oriented_candidates_from_row(row, P))

    by_ax: dict[tuple[int, int], dict[str, int]] = {}
    for cand in candidates:
        by_ax.setdefault((int(cand["A"]), int(cand["x5"])), cand)

    out: list[dict[str, int | None]] = []
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sample_rows"] = len(rows)
    stats["oriented_candidates"] = len(candidates)
    stats["unique_ax"] = len(by_ax)

    for A, x5 in by_ax:
        first_lifts = conic_lifts_modsqrt(A, x5, P)
        stats["first_lifts"] += len(first_lifts)
        for first in first_lifts:
            d0 = selector_data(first, P)
            if d0 is None or d0["selector"] == 0:
                stats["first_degenerate_selector"] += 1
                continue
            z0_roots = roots_mod(d0["selector"], P)
            if not z0_roots:
                stats["d4_minus_first_lifts"] += 1
                continue
            stats["d4_plus_first_lifts"] += 1
            second_lifts = transition_lifts_modsqrt(first.c, first.R, P)
            stats["second_lifts_after_d4plus"] += len(second_lifts)
            for second in second_lifts:
                d1 = selector_data(second, P)
                if d1 is None or d1["selector"] == 0:
                    stats["second_degenerate_selector"] += 1
                    continue
                target_chi = legendre(d1["selector"], P)
                if target_chi not in (-1, 1):
                    stats["second_zero_selector"] += 1
                    continue
                if target_chi == 1:
                    stats["d5_plus_second_lifts"] += 1
                else:
                    stats["d5_minus_second_lifts"] += 1
                base = {
                    "A": A,
                    "x0": x5,
                    "c": first.c,
                    "r0": first.r,
                    "R0": first.R,
                    "R1": second.R,
                    "a0": d0["a"],
                    "a1": d1["a"],
                    "L0": d0["L"],
                    "L1": d1["L"],
                    "w0": d0["w"],
                    "w1": d1["w"],
                    "S0": d0["selector"],
                    "S1": d1["selector"],
                    "target": target_chi,
                }
                for z0 in z0_roots:
                    row = dict(base)
                    row["Z0"] = z0
                    out.append(row)
    stats["selector_rows"] = len(out)
    return out, stats


def field_selector_rows(q: int) -> tuple[list[dict[str, int | None]], Counter]:
    selector_rows, _root_rows, stats = two_step_rows(q)
    out: list[dict[str, int | None]] = []
    for row in selector_rows:
        s1 = row.get("S1")
        if s1 is None:
            continue
        target = legendre(int(s1), q)
        if target not in (-1, 1):
            continue
        rrow = dict(row)
        rrow["target"] = target
        out.append(rrow)
    stats = Counter(stats)
    stats["selector_rows_for_quotient"] = len(out)
    return out, stats


def key_for(values: dict[str, int | None], system: tuple[str, ...], p: int) -> tuple[int, ...] | None:
    key: list[int] = []
    for name in system:
        value = values.get(name)
        if value is None:
            return None
        key.append(int(value) % p)
    return tuple(key)


def screen_rows(label: str, rows: list[dict[str, int | None]], p: int) -> list[tuple[str, Counter]]:
    out: list[tuple[str, Counter]] = []
    derived_rows = [add_derived(row, p) for row in rows]
    for name, system in SYSTEMS.items():
        groups: defaultdict[tuple[int, ...], Counter] = defaultdict(Counter)
        stats: Counter = Counter()
        for row in derived_rows:
            key = key_for(row, system, p)
            if key is None:
                stats["degenerate_rows"] += 1
                continue
            target = row.get("target")
            if target not in (-1, 1):
                stats["bad_target_rows"] += 1
                continue
            groups[key][int(target)] += 1
        stats["label_" + label] = 1
        stats["rows"] = sum(sum(counter.values()) for counter in groups.values())
        stats["groups"] = len(groups)
        stats["target_plus_rows"] = sum(counter[1] for counter in groups.values())
        stats["target_minus_rows"] = sum(counter[-1] for counter in groups.values())
        for counter in groups.values():
            size = sum(counter.values())
            stats[f"group_size_{size}"] += 1
            if counter[1] and counter[-1]:
                stats["mixed_groups"] += 1
                stats["mixed_rows"] += size
            elif counter[1]:
                stats["plus_groups"] += 1
            elif counter[-1]:
                stats["minus_groups"] += 1
        if stats["groups"]:
            stats["max_group_size"] = max(sum(counter.values()) for counter in groups.values())
            stats["collapse_x1000000"] = (stats["rows"] * 1_000_000) // stats["groups"]
            stats["mixed_group_rate_x1000000"] = (stats["mixed_groups"] * 1_000_000) // stats["groups"]
            stats["mixed_row_rate_x1000000"] = (stats["mixed_rows"] * 1_000_000) // stats["rows"]
        out.append((name, stats))
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=600)
    parser.add_argument("--p27-heldout-target", type=int, default=600)
    parser.add_argument("--p27-seed", type=int, default=20260621)
    parser.add_argument("--p27-heldout-seed", type=int, default=20260622)
    parser.add_argument("--p27-max-draws", type=int, default=1000000)
    parser.add_argument("--skip-p27", action="store_true")
    args = parser.parse_args()

    print("p27 conic tower sign-quotient probe")
    print("question = does d5 descend after forgetting obvious signs?")
    for q in parse_ints(args.small_primes):
        rows, stats = field_selector_rows(q)
        print_counter(f"q{q}_base", stats)
        for name, qstats in screen_rows(f"q{q}", rows, q):
            print_counter(f"q{q}_{name}", qstats)

    if not args.skip_p27:
        for label, rows, stats in [
            ("p27_train", *p27_selector_rows(args.p27_target, args.p27_seed, args.p27_max_draws)),
            (
                "p27_heldout",
                *p27_selector_rows(args.p27_heldout_target, args.p27_heldout_seed, args.p27_max_draws),
            ),
        ]:
            print_counter(f"{label}_base", stats)
            for name, qstats in screen_rows(label, rows, P):
                print_counter(f"{label}_{name}", qstats)

    print("p27_conic_tower_sign_quotient_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
