#!/usr/bin/env python3
"""Extension-field counts for the p27 K/S reverse-root cover.

The plane-relation screen for the d3 reverse-source root kept the actual
variable z with x6=z^2 and found no low-degree shortcut over K or Sroot.  This
probe asks a different, coarser question over GF(q^n): do the K/S projections
of the legal reverse-root cover look source-sized or do they collapse to a
smaller object that could justify a direct sampler?
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_extension_prefix_count_probe import (
    GF,
    compact_class,
    find_irreducible,
    halve_all,
    label2_candidate,
)


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def ks_coordinates(F: GF, x: int, w: int) -> tuple[int, int] | None:
    """Return K=x([2]P) and Sroot for the 2-isogenous E' quotient."""
    if x == 0:
        return None
    x2 = F.sqr(x)
    u = F.sub(x, F.inv(x))
    v = F.mul(w, F.mul(F.add(x2, F.one), F.inv(x2)))
    if F.sqr(v) != F.add(F.mul(F.sqr(u), u), F.mul(F.c(4), u)):
        raise ValueError("2-isogeny quotient equation mismatch")

    u2 = F.sqr(u)
    den_k = F.mul(F.mul(F.c(4), u), F.add(u2, F.c(4)))
    den_s = F.mul(F.c(2), v)
    if den_k == 0 or den_s == 0:
        return None
    num = F.sub(u2, F.c(4))
    k = F.div(F.sqr(num), den_k)
    s = F.div(num, den_s)
    if F.sqr(s) != k:
        raise ValueError("Sroot square did not match K")
    return k, s


def add_projection_sets(
    sets: dict[str, set[int | tuple[int, int]]],
    k: int,
    s: int,
    x6: int,
    z: int,
    F: GF,
) -> None:
    sets["K"].add(k)
    sets["S"].add(s)
    sets["x6"].add(x6)
    sets["z"].add(z)
    sets["K_x6"].add((k, x6))
    sets["S_x6"].add((s, x6))
    sets["K_z"].add((k, z))
    sets["S_z"].add((s, z))

    if x6 != 0:
        r = F.add(x6, F.inv(x6))
        sets["r"].add(r)
        sets["K_r"].add((k, r))
        sets["S_r"].add((s, r))
    if z != 0:
        iz = F.inv(z)
        zsum = F.add(z, iz)
        zdiff = F.sub(z, iz)
        sets["zsum"].add(zsum)
        sets["zdiff"].add(zdiff)
        sets["K_zsum"].add((k, zsum))
        sets["S_zsum"].add((s, zsum))
        sets["K_zdiff"].add((k, zdiff))
        sets["S_zdiff"].add((s, zdiff))


def count_field(q: int, n: int) -> Counter:
    F = GF(q=q, n=n, modulus=find_irreducible(q, n))
    stats: Counter = Counter()
    stats["field_size"] = F.size
    stats["modulus_degree"] = n

    sets: dict[str, set[int | tuple[int, int]]] = {
        name: set()
        for name in [
            "A",
            "Ax",
            "K",
            "S",
            "x6",
            "z",
            "r",
            "zsum",
            "zdiff",
            "K_x6",
            "S_x6",
            "K_z",
            "S_z",
            "K_r",
            "S_r",
            "K_zsum",
            "S_zsum",
            "K_zdiff",
            "S_zdiff",
        ]
    }
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
                comp = compact_class(F, x, w, t)
                if comp != -1:
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
                    sets["A"].add(A)
                    sets["Ax"].add((A, x5))

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
                            add_projection_sets(sets, k, s, x6, z, F)

    for name, values in sets.items():
        stats[f"unique_{name}"] = len(values)
    return stats


def print_stats(q: int, n: int, stats: Counter) -> None:
    N = stats["field_size"]
    print(f"GF({q}^{n}) N={N}:")
    for key in [
        "source_rows",
        "candidates",
        "duplicate_candidate",
        "d2_plus_candidates",
        "d2_minus",
        "x6_branches",
        "x6_square_branches",
        "x6_nonsquare",
        "z_rows",
        "unique_Ax",
        "unique_A",
        "unique_K",
        "unique_S",
        "unique_x6",
        "unique_z",
        "unique_r",
        "unique_zsum",
        "unique_zdiff",
        "unique_K_x6",
        "unique_S_x6",
        "unique_K_z",
        "unique_S_z",
        "unique_K_r",
        "unique_S_r",
        "unique_K_zsum",
        "unique_S_zsum",
        "unique_K_zdiff",
        "unique_S_zdiff",
        "candidate_invalid_degenerate",
        "candidate_invalid_degenerate_A",
        "candidate_invalid_not_nonsplit",
        "candidate_invalid_d1_sqrt_mismatch",
        "candidate_invalid_d1_no_half",
        "ks_degenerate",
        "compact_not_target",
    ]:
        if key in stats:
            print(f"  {key} = {stats[key]}")

    for key in [
        "source_rows",
        "candidates",
        "z_rows",
        "unique_Ax",
        "unique_A",
        "unique_K",
        "unique_S",
        "unique_K_z",
        "unique_S_z",
        "unique_K_r",
        "unique_S_r",
    ]:
        value = stats.get(key, 0)
        print(f"  {key}/N = {value / N:.9f}")

    for numerator, denominator in [
        ("z_rows", "unique_K"),
        ("z_rows", "unique_S"),
        ("unique_K_z", "unique_K"),
        ("unique_S_z", "unique_S"),
        ("unique_K_r", "unique_K"),
        ("unique_S_r", "unique_S"),
        ("unique_Ax", "unique_A"),
    ]:
        den = stats.get(denominator, 0)
        value = stats.get(numerator, 0) / den if den else 0.0
        print(f"  {numerator}/{denominator} = {value:.9f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=7)
    parser.add_argument("--degrees", default="1,2,3,4")
    args = parser.parse_args()

    print("p27 K-line reverse-z extension-count probe")
    print("source = residual E/T + compactD=-1 + label-2 candidate map")
    print("reverse source = d2 square and d3 all-plus with x6=z^2")
    print("coordinates = K=x([2]P) on E', Sroot^2=K")
    for n in parse_ints(args.degrees):
        print_stats(args.q, n, count_field(args.q, n))
    print("p27_kline_reverse_z_extension_count_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
