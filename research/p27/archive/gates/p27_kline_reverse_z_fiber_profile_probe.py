#!/usr/bin/env python3
"""Fiber profiles for the p27 K/S reverse-root cover.

The extension-count probe showed fixed aggregate fibers over K and Sroot.  This
probe records per-fiber histograms.  It is a cheap branch proxy: rational
branch/support structure would often show up first as anomalous K or Sroot
fibers before a full normalization is available.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Callable

from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)
from p27_kline_reverse_z_extension_count_probe import ks_coordinates, parse_ints


def empty_fiber() -> dict[str, object]:
    return {
        "rows": 0,
        "A": set(),
        "Ax": set(),
        "x6": set(),
        "z": set(),
        "r": set(),
        "zsum": set(),
        "zdiff": set(),
    }


def record_fiber(
    fiber: dict[str, object],
    F: GF,
    A: int,
    x5: int,
    x6: int,
    z: int,
) -> None:
    fiber["rows"] = int(fiber["rows"]) + 1
    for name, value in [
        ("A", A),
        ("Ax", (A, x5)),
        ("x6", x6),
        ("z", z),
    ]:
        values = fiber[name]
        assert isinstance(values, set)
        values.add(value)

    if x6 != 0:
        values = fiber["r"]
        assert isinstance(values, set)
        values.add(F.add(x6, F.inv(x6)))
    if z != 0:
        iz = F.inv(z)
        for name, value in [
            ("zsum", F.add(z, iz)),
            ("zdiff", F.sub(z, iz)),
        ]:
            values = fiber[name]
            assert isinstance(values, set)
            values.add(value)


def set_size(fiber: dict[str, object], name: str) -> int:
    values = fiber[name]
    assert isinstance(values, set)
    return len(values)


def collect_field(q: int, n: int) -> tuple[Counter, dict[str, dict[int, dict[str, object]]]]:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    stats: Counter = Counter()
    stats["field_size"] = F.size
    fibers: dict[str, defaultdict[int, dict[str, object]]] = {
        "K": defaultdict(empty_fiber),
        "S": defaultdict(empty_fiber),
    }
    k_to_s: defaultdict[int, set[int]] = defaultdict(set)
    s_to_k: dict[int, int] = {}
    seen_candidates: set[tuple[int, int, int, int, int]] = set()

    for x in range(F.size):
        if x in (0, F.one):
            stats["skip_x_degenerate"] += 1
            continue
        x2 = F.sqr(x)
        w2 = F.sub(F.mul(x2, x), x)
        t2 = F.mul(F.mul(x, F.add(x2, F.one)), F.add(F.add(x2, F.mul(F.two, x)), F.neg(F.one)))
        for w in F.roots(w2):
            ks = ks_coordinates(F, x, w)
            if ks is None:
                stats["ks_degenerate"] += 1
                continue
            k, s = ks
            for t in F.roots(t2):
                if compact_class(F, x, w, t) != -1:
                    stats["compact_not_target"] += 1
                    continue
                stats["source_rows"] += 1
                for root_index in (0, 1):
                    reason, cand = label2_candidate(F, x, w, t, root_index)
                    if cand is None:
                        stats[f"candidate_invalid_{reason}"] += 1
                        continue
                    A, x5 = cand
                    key = (x, w, t, A, x5)
                    if key in seen_candidates:
                        stats["duplicate_candidate"] += 1
                        continue
                    seen_candidates.add(key)
                    stats["candidates"] += 1
                    d2, x6s = halve_all(F, A, x5)
                    if d2 != 1:
                        stats["d2_minus"] += 1
                        continue
                    stats["d2_plus_candidates"] += 1
                    for x6 in x6s:
                        stats["x6_branches"] += 1
                        zroots = F.roots(x6)
                        if not zroots:
                            stats["x6_nonsquare"] += 1
                            continue
                        stats["x6_square_branches"] += 1
                        for z in zroots:
                            stats["z_rows"] += 1
                            k_to_s[k].add(s)
                            prior_k = s_to_k.get(s)
                            if prior_k is not None and prior_k != k:
                                stats["S_to_mixed_K"] += 1
                            s_to_k[s] = k
                            record_fiber(fibers["K"][k], F, A, x5, x6, z)
                            record_fiber(fibers["S"][s], F, A, x5, x6, z)

    stats["unique_K"] = len(fibers["K"])
    stats["unique_S"] = len(fibers["S"])
    stats["K_to_S_values"] = len(k_to_s)
    stats["unique_S_all_seen"] = len(s_to_k)
    stats["K_to_S_size_hist_keys"] = len(Counter(len(v) for v in k_to_s.values()))
    stats["S_to_mixed_K"] += 0
    # Cast defaultdicts to ordinary dicts before returning.
    return stats, {"K": dict(fibers["K"]), "S": dict(fibers["S"])}


def histogram_for(fibers: dict[int, dict[str, object]], measure: Callable[[dict[str, object]], int]) -> Counter:
    return Counter(measure(fiber) for fiber in fibers.values())


def print_hist(prefix: str, hist: Counter) -> None:
    if not hist:
        print(f"  {prefix}: empty")
        return
    parts = " ".join(f"{value}:{hist[value]}" for value in sorted(hist))
    print(f"  {prefix}: {parts}")


def print_coord_profile(label: str, coord: str, fibers: dict[int, dict[str, object]]) -> None:
    print(f"{label}_{coord}_fiber_profile:")
    print(f"  fibers = {len(fibers)}")
    measures: list[tuple[str, Callable[[dict[str, object]], int]]] = [
        ("rows", lambda f: int(f["rows"])),
        ("unique_A", lambda f: set_size(f, "A")),
        ("unique_Ax", lambda f: set_size(f, "Ax")),
        ("unique_x6", lambda f: set_size(f, "x6")),
        ("unique_z", lambda f: set_size(f, "z")),
        ("unique_r", lambda f: set_size(f, "r")),
        ("unique_zsum", lambda f: set_size(f, "zsum")),
        ("unique_zdiff", lambda f: set_size(f, "zdiff")),
    ]
    for name, measure in measures:
        hist = histogram_for(fibers, measure)
        print_hist(name, hist)
        if hist:
            modal_value, modal_count = hist.most_common(1)[0]
            anomalies = len(fibers) - modal_count
            print(f"  {name}_modal = {modal_value}")
            print(f"  {name}_anomalous_fibers = {anomalies}")


def print_field(q: int, n: int, stats: Counter, fibers: dict[str, dict[int, dict[str, object]]]) -> None:
    N = stats["field_size"]
    label = f"GF({q}^{n})"
    print(f"{label} N={N}:")
    for key in [
        "source_rows",
        "candidates",
        "d2_plus_candidates",
        "d2_minus",
        "x6_branches",
        "x6_square_branches",
        "x6_nonsquare",
        "z_rows",
        "unique_K",
        "unique_S",
        "K_to_S_values",
        "unique_S_all_seen",
        "K_to_S_size_hist_keys",
        "S_to_mixed_K",
        "candidate_invalid_degenerate",
        "candidate_invalid_degenerate_A",
        "candidate_invalid_not_nonsplit",
        "ks_degenerate",
        "compact_not_target",
    ]:
        if key in stats:
            print(f"  {key} = {stats[key]}")
    print(f"  unique_K/N = {stats.get('unique_K', 0) / N:.9f}")
    print(f"  unique_S/N = {stats.get('unique_S', 0) / N:.9f}")
    print_coord_profile(label.replace("^", "_"), "K", fibers["K"])
    print_coord_profile(label.replace("^", "_"), "S", fibers["S"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=1607)
    parser.add_argument("--degrees", default="1")
    args = parser.parse_args()

    print("p27 K-line reverse-z fiber-profile probe")
    print("source = residual E/T + compactD=-1 + label-2 candidate map")
    print("reverse source = d2 square and d3 all-plus with x6=z^2")
    print("branch proxy = rational K/Sroot fiber histograms")
    for n in parse_ints(args.degrees):
        stats, fibers = collect_field(args.q, n)
        print_field(args.q, n, stats, fibers)
    print("p27_kline_reverse_z_fiber_profile_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
