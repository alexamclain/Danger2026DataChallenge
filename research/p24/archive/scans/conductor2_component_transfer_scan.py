#!/usr/bin/env python3
"""Bounded scan for conductor-2 component transfer.

This generalizes `conductor2_component_transfer_toy.py`.  It searches small
ordinary rows with `t^2-4p=4D`, `D == 1 mod 8`, and compares odd-prime
horizontal components on the maximal and conductor-2 root sets.

The test is not a proof of the p24 theorem.  It checks whether the
conductor-2/nonsplit branch creates a new quotient collapse.  The expected
answer is no: the descending 2-isogeny should transfer components
equivariantly, preserving quotient degree while changing the embedded period
values.
"""

from __future__ import annotations

import argparse
from math import isqrt

from cypari2 import Pari

from conductor2_nonsplit_gate_scan import is_prime, is_squarefree
from conductor2_component_transfer_toy import components, phi_neighbors_between
from embedded_decomposition_calibration import isogeny_neighbors
from fixed_trace_cm_root_toy import pari_linear_roots


def component_lookup(comps: list[list[int]]) -> dict[int, int]:
    out: dict[int, int] = {}
    for idx, comp in enumerate(comps):
        for root in comp:
            out[root] = idx
    return out


def scan_case(pari: Pari, p: int, t: int, D: int, ell: int) -> dict[str, object] | None:
    max_roots = pari_linear_roots(pari.polclass(D), p)
    c2_roots = pari_linear_roots(pari.polclass(4 * D), p)
    if len(max_roots) != len(c2_roots) or len(max_roots) < 4:
        return None

    max_graph = isogeny_neighbors(max_roots, ell, p)
    c2_graph = isogeny_neighbors(c2_roots, ell, p)
    max_degrees = sorted({len(v) for v in max_graph.values()})
    c2_degrees = sorted({len(v) for v in c2_graph.values()})
    if max_degrees != [2] or c2_degrees != [2]:
        return None

    max_comps = components(max_graph)
    c2_comps = components(c2_graph)
    if len(max_comps) < 2:
        return None
    down = phi_neighbors_between(max_roots, c2_roots, 2, p)
    down_degrees = sorted({len(v) for v in down.values()})
    if down_degrees != [1]:
        return None

    c2_index = component_lookup(c2_comps)
    image_index_sets = []
    for comp in max_comps:
        image_index_sets.append(tuple(sorted({c2_index[down[root][0]] for root in comp})))
    equivariant = all(len(s) == 1 for s in image_index_sets)

    max_sums = sorted(sum(comp) % p for comp in max_comps)
    c2_sums = sorted(sum(comp) % p for comp in c2_comps)
    return {
        "p": p,
        "t": t,
        "D": D,
        "h": len(max_roots),
        "ell": ell,
        "component_count": len(max_comps),
        "component_sizes": sorted({len(c) for c in max_comps}),
        "equivariant": equivariant,
        "sum_sets_equal": max_sums == c2_sums,
        "max_sums": max_sums,
        "c2_sums": c2_sums,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-p", type=int, default=700)
    parser.add_argument("--max-h", type=int, default=30)
    parser.add_argument("--max-ell", type=int, default=17)
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()

    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[dict[str, object]] = []
    for p in range(7, args.max_p + 1):
        if p % 8 != 7 or not is_prime(p):
            continue
        for t in range(8, 2 * isqrt(p) + 1, 8):
            D4 = t * t - 4 * p
            if D4 >= 0 or D4 % 4 != 0:
                continue
            D = D4 // 4
            if D % 8 != 1 or not is_squarefree(abs(D)):
                continue
            h = int(pari.poldegree(pari.polclass(D)))
            h2 = int(pari.poldegree(pari.polclass(4 * D)))
            if h > args.max_h or h2 > args.max_h:
                continue
            for ell in range(3, args.max_ell + 1, 2):
                if not is_prime(ell) or ell == p:
                    continue
                row = scan_case(pari, p, t, D, ell)
                if row is None:
                    continue
                rows.append(row)
                print(
                    "p={p} t={t} D={D} h={h} ell={ell} comps={component_count} "
                    "sizes={component_sizes} equivariant={equivariant} "
                    "sum_sets_equal={sum_sets_equal}".format(**row)
                )
                if len(rows) >= args.max_rows:
                    break
            if len(rows) >= args.max_rows:
                break
        if len(rows) >= args.max_rows:
            break

    print()
    print(f"rows={len(rows)}")
    print(f"all_equivariant={int(all(bool(row['equivariant']) for row in rows)) if rows else 0}")
    print(f"rows_with_same_sum_set={sum(1 for row in rows if row['sum_sets_equal'])}")
    print("conclusion=reported_conductor2_component_transfer_scan")


if __name__ == "__main__":
    main()
