#!/usr/bin/env python3
"""D6 sign-quotient continuation screen for the p27 conic tower.

The d5 screen showed that the next selector descends through the obvious
finite sign quotients.  This probe asks the next natural question: after
conditioning on d4-plus and d5-plus, does d6 still descend to the same small
quotients, or does it become a fresh half-cover?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from p27_conic_chain_source_probe import sqrt_table
from p27_conic_pair_d4_recurrence_probe import conic_lifts_modsqrt, inv, roots_mod
from p27_conic_pair_d5_tower_probe import transition_lifts_modsqrt, transition_lifts_table
from p27_conic_pair_two_step_kummer_probe import selector_data, two_step_rows
from p27_label2_alpha_branch_recurrence_probe import P, legendre, sample_rows
from p27_reverse_doubling_source_probe import all_oriented_candidates_from_row


SYSTEMS: dict[str, tuple[str, ...]] = {
    "base_A": ("A",),
    "base_Ax": ("A", "x0"),
    "first_unsigned": ("A", "x0", "c2", "u0", "w0", "m0"),
    "two_signed": ("A", "x0", "c", "r0", "R0", "L0", "R1", "L1"),
    "two_square": ("A", "x0", "c2", "R0sq", "L0sq", "R1sq", "L1sq", "a1sq", "w1"),
    "two_reciprocal": ("A", "x0", "c2", "u0", "w0", "m0", "u1", "w1", "m1"),
    "two_selector_signless": ("A", "x0", "c2", "u0", "w0", "S0", "u1", "w1", "S1"),
    "z01_signless": ("A", "x0", "c2", "u0", "w0", "Z0sq", "u1", "w1", "Z1sq"),
    "three_signed": ("A", "x0", "c", "r0", "R0", "L0", "R1", "L1", "R2", "L2"),
    "three_drop_L2_sign": ("A", "x0", "c", "r0", "R0", "L0", "R1", "L1", "R2", "L2sq", "w2"),
    "three_square": (
        "A",
        "x0",
        "c2",
        "R0sq",
        "L0sq",
        "R1sq",
        "L1sq",
        "R2sq",
        "L2sq",
        "a2sq",
        "w2",
    ),
    "three_reciprocal": ("A", "x0", "c2", "u0", "w0", "m0", "u1", "w1", "m1", "u2", "w2", "m2"),
}


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def maybe_inv(a: int | None, p: int) -> int | None:
    if a is None:
        return None
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def add_derived(row: dict[str, int | None], p: int) -> dict[str, int | None]:
    out = dict(row)
    c = out.get("c")
    if c is not None:
        out["c2"] = int(c) * int(c) % p

    for name in ["r0", "R0", "L0", "R1", "L1", "R2", "L2", "a0", "a1", "a2", "Z0", "Z1"]:
        value = out.get(name)
        if value is not None:
            out[f"{name}sq"] = int(value) * int(value) % p

    for prefix in ["0", "1", "2"]:
        R = out.get(f"R{prefix}")
        L = out.get(f"L{prefix}")
        a = out.get(f"a{prefix}")
        if R is not None:
            iR = maybe_inv(R, p)
            if iR is not None:
                out[f"u{prefix}"] = (int(R) + iR) % p
                out[f"v{prefix}"] = (int(R) - iR) % p
        if L is not None and a is not None:
            asq = int(a) * int(a) % p
            out[f"a{prefix}sq"] = asq
            out[f"w{prefix}"] = (int(L) * int(L) - asq) % p
            iL = maybe_inv(L, p)
            if iL is not None:
                out[f"m{prefix}"] = (int(L) + asq * iL) % p
                out[f"n{prefix}"] = (int(L) - asq * iL) % p
    return out


def d6_rows_from_prefix(
    base: dict[str, int | None],
    p: int,
    third_lift_fn,
) -> tuple[list[dict[str, int | None]], Counter]:
    stats: Counter = Counter()
    rows: list[dict[str, int | None]] = []
    c = base.get("c")
    r1 = base.get("R1")
    if c is None or r1 is None:
        stats["missing_third_source"] += 1
        return rows, stats

    third_lifts = third_lift_fn(int(c), int(r1))
    stats["third_lifts_after_d5plus"] += len(third_lifts)
    for third in third_lifts:
        d2 = selector_data(third, p)
        if d2 is None or d2["selector"] == 0:
            stats["third_degenerate_selector"] += 1
            continue
        target = legendre(int(d2["selector"]), p)
        if target not in (-1, 1):
            stats["third_zero_selector"] += 1
            continue
        if target == 1:
            stats["d6_plus_third_lifts"] += 1
        else:
            stats["d6_minus_third_lifts"] += 1
        row = dict(base)
        row.update(
            {
                "R2": third.R,
                "a2": d2["a"],
                "L2": d2["L"],
                "w2": d2["w"],
                "S2": d2["selector"],
                "target": target,
            }
        )
        rows.append(row)
    return rows, stats


def p27_selector_rows(target: int, seed: int, max_draws: int) -> tuple[list[dict[str, int | None]], Counter]:
    sampled, sample_stats = sample_rows(target, seed, max_draws, P)
    candidates: list[dict[str, int]] = []
    for row in sampled:
        candidates.extend(all_oriented_candidates_from_row(row, P))

    by_ax: dict[tuple[int, int], dict[str, int]] = {}
    for cand in candidates:
        by_ax.setdefault((int(cand["A"]), int(cand["x5"])), cand)

    out: list[dict[str, int | None]] = []
    stats: Counter = Counter({f"sample_{key}": value for key, value in sample_stats.items()})
    stats["sample_rows"] = len(sampled)
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
                z1_roots = roots_mod(d1["selector"], P)
                if not z1_roots:
                    stats["d5_minus_second_lifts"] += 1
                    continue
                stats["d5_plus_second_lifts"] += 1
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
                }
                for z0 in z0_roots:
                    for z1 in z1_roots:
                        prefix = dict(base)
                        prefix["Z0"] = z0
                        prefix["Z1"] = z1
                        rows, row_stats = d6_rows_from_prefix(
                            prefix,
                            P,
                            lambda c, r: transition_lifts_modsqrt(c, r, P),
                        )
                        stats.update(row_stats)
                        out.extend(rows)
    stats["selector_rows"] = len(out)
    return out, stats


def field_selector_rows(q: int) -> tuple[list[dict[str, int | None]], Counter]:
    roots = sqrt_table(q)
    _selector_rows, root_rows, stats = two_step_rows(q)
    out: list[dict[str, int | None]] = []
    stats = Counter(stats)
    for row in root_rows:
        rows, row_stats = d6_rows_from_prefix(
            row,
            q,
            lambda c, r: transition_lifts_table(c, r, q, roots),
        )
        stats.update(row_stats)
        out.extend(rows)
    stats["selector_rows_for_d6_quotient"] = len(out)
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

    print("p27 conic tower d6 sign-quotient probe")
    print("question = after d4-plus and d5-plus, does d6 descend through obvious quotients?")
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

    print("p27_conic_tower_d6_quotient_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
