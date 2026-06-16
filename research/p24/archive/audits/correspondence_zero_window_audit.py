#!/usr/bin/env python3
"""Search for a finite-field zero-lemma window in p24 split correspondences.

Conditional idea:

    If a weighted class-character trace along a class element beta of order n
    can be realized as a nonzero modular/correspondence function with pole
    degree at most n * delta, then harmful vanishing on every quotient fiber
    would force vanishing on all h CM points.  The finite-field zero lemma
    would rule this out when

        n * delta < h,

    equivalently delta < h/n = index(beta).

Here delta is optimistically approximated by the squarefree X0 index of the
rational norm used to represent beta.  Any real orientation cover only makes
delta larger, so this is a generous pass/fail screen.
"""

from __future__ import annotations

import argparse
import math

from cypari2 import Pari

from all_trace_composite_order_search import (
    P,
    TRACES,
    exact_targets,
    search_target,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=1000)
    ap.add_argument("--max-factors", type=int, default=4)
    ap.add_argument("--max-norm", type=int, default=250000)
    ap.add_argument("--trace", type=int, default=-1178414874616)
    ap.add_argument("--show", type=int, default=16)
    args = ap.parse_args()

    if args.trace not in TRACES:
        raise SystemExit(f"trace must be one of {TRACES}")

    pari = Pari()
    target = next(row for row in exact_targets(pari) if row.trace == args.trace)
    hits = search_target(
        target,
        prime_bound=args.prime_bound,
        max_factors=args.max_factors,
        max_norm=args.max_norm,
    )

    sqrt_p = math.isqrt(P)
    passing = [row for row in hits if row.x0_index < row.index]
    best = sorted(hits, key=lambda row: (row.x0_index / row.index, row.x0_index, row.norm))

    print("p24 correspondence zero-lemma window audit")
    print(f"p={P}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"trace={target.trace}")
    print(f"D_K={target.D_K}")
    print(f"h={target.h}")
    print(f"group={target.group}")
    print(f"prime_bound={args.prime_bound}")
    print(f"max_factors={args.max_factors}")
    print(f"max_norm={args.max_norm}")
    print(f"hits={len(hits)}")
    print(f"zero_lemma_window_hits={len(passing)}")
    print()

    print("criterion")
    print("  order = n")
    print("  index = h/n = m")
    print("  delta = optimistic squarefree X0 correspondence index")
    print("  zero lemma window requires delta < index")
    print()

    if passing:
        print("passing_rows")
        print("  ratio delta index order norm seeded/sqrt signed_terms")
        for row in sorted(passing, key=lambda r: (r.x0_index / r.index, r.x0_index * r.order))[
            : args.show
        ]:
            print(
                f"  {row.x0_index / row.index:9.6f} {row.x0_index:8d} "
                f"{row.index:10d} {row.order:15d} {row.norm:8d} "
                f"{row.x0_index * row.order / sqrt_p:11.6f} {row.signed_terms}"
            )
        print()

    print("best_ratio_rows")
    print("  ratio delta index order norm n_delta_over_h seeded/sqrt signed_terms")
    for row in best[: args.show]:
        ratio = row.x0_index / row.index
        print(
            f"  {ratio:9.6f} {row.x0_index:8d} {row.index:10d} "
            f"{row.order:15d} {row.norm:8d} {ratio:14.6f} "
            f"{row.x0_index * row.order / sqrt_p:11.6f} {row.signed_terms}"
        )

    print()
    print("interpretation")
    print("  zero_lemma_window_found=" + str(int(bool(passing))))
    print("  best_ratio_delta_over_index=" + (f"{best[0].x0_index / best[0].index:.6f}" if best else "nan"))
    print("  optimistic_orientation_cover_used=0")
    print("  real_oriented_correspondence_degree_can_only_be_larger=1")
    print(
        "conclusion=bounded_split_correspondence_zero_lemma_does_not_certify_"
        "the_p24_relative_packet_in_this_search_window"
    )


if __name__ == "__main__":
    main()
