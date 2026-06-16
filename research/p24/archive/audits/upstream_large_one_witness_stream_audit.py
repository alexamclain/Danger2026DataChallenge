#!/usr/bin/env python3
"""Streaming audit for Sutherland's larger one-witness DANGER3 datasets.

The upstream README links pp28/pp30/pp32, which contain one Pomerance triple
per prime.  These files are too biased to estimate the true solution density,
but they can test whether the published witness selection exposes a liftable
statistical rule for A, x0, or the near-square subfamily p = n^2 + 7.

This script streams local paths or HTTPS URLs.  It keeps cheap whole-file
statistics, a deterministic reservoir sample for expensive verifier features,
and exact retained buckets for near-square rows.
"""

from __future__ import annotations

import argparse
import gzip
import math
import random
import sys
import urllib.request
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

from upstream_dataset_feature_audit import (
    legendre,
    quantiles,
    target_order_count,
    terminal_branch,
    verifier_k,
)


PP28_URL = "https://math.mit.edu/~drew/pp28.txt.gz"
PP30_URL = "https://math.mit.edu/~drew/pp30.txt.gz"
PP32_URL = "https://math.mit.edu/~drew/pp32.txt.gz"


@contextmanager
def open_stream(source: str) -> Iterator[TextIO]:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=60) as response:
            if source.endswith(".gz"):
                with gzip.GzipFile(fileobj=response) as gz:
                    text = (line.decode("ascii") for line in gz)
                    yield text  # type: ignore[misc]
            else:
                text = (line.decode("ascii") for line in response)
                yield text  # type: ignore[misc]
        return

    path = Path(source)
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="ascii") as handle:
            yield handle
    else:
        with path.open("rt", encoding="ascii") as handle:
            yield handle


def parse_rows(source: str, limit: int | None = None) -> Iterator[tuple[int, int, int]]:
    with open_stream(source) as handle:
        for index, line in enumerate(handle):
            if limit is not None and index >= limit:
                break
            line = line.strip()
            if not line:
                continue
            p_s, a_s, x_s = line.split(",")
            yield int(p_s), int(a_s), int(x_s)


def bin_unit(value: int, modulus: int, bins: int) -> int:
    return min(bins - 1, (value * bins) // modulus)


def p24_analog(p: int, near_c: int) -> tuple[int, int] | None:
    n = math.isqrt(p)
    c = p - n * n
    if 0 < c <= near_c:
        return n, c
    return None


def update_reservoir(
    rng: random.Random,
    reservoir: list[tuple[int, int, int]],
    row_index: int,
    row: tuple[int, int, int],
    capacity: int,
) -> None:
    if capacity <= 0:
        return
    if len(reservoir) < capacity:
        reservoir.append(row)
        return
    j = rng.randrange(row_index + 1)
    if j < capacity:
        reservoir[j] = row


def summarize_triples(label: str, triples: list[tuple[int, int, int]], max_terminal: int) -> None:
    split_counts: Counter[int] = Counter()
    terminal_counts: Counter[str] = Counter()
    fx_counts: Counter[int] = Counter()
    gate_counts: Counter[tuple[int, int, int]] = Counter()
    pmod8_split: Counter[tuple[int, int]] = Counter()
    target_counts: Counter[int] = Counter()
    min_a: list[float] = []
    min_x: list[float] = []
    terminal_seen = 0

    for p, A, x in triples:
        split = legendre(A * A - 4, p)
        fx = x * (x * x + A * x + 1) % p
        fx_char = legendre(fx, p)
        split_counts[split] += 1
        fx_counts[fx_char] += 1
        pmod8_split[(p % 8, split)] += 1
        target_counts[target_order_count(p)] += 1
        gate_counts[(legendre(A + 2, p), legendre(A - 2, p), split)] += 1
        min_a.append(min(A, p - A) / p)
        min_x.append(min(x, p - x) / p)
        if terminal_seen < max_terminal:
            terminal_counts[terminal_branch(p, A, x, verifier_k(p))] += 1
            terminal_seen += 1

    print(f"{label}_rows={len(triples)}")
    if not triples:
        return
    print(f"{label}_split_counts={dict(sorted(split_counts.items()))}")
    print(f"{label}_fx_char_counts={dict(sorted(fx_counts.items()))}")
    print(f"{label}_terminal_rows={terminal_seen}")
    print(f"{label}_terminal_counts={dict(sorted(terminal_counts.items()))}")
    print(f"{label}_target_order_count_hist={dict(sorted(target_counts.items()))}")
    print(
        f"{label}_pmod8_split_counts="
        + ",".join(f"{key}:{value}" for key, value in sorted(pmod8_split.items()))
    )
    print(
        f"{label}_gate_counts="
        + ",".join(f"{key}:{value}" for key, value in sorted(gate_counts.items()))
    )
    qs = (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99)
    print(f"{label}_min_A_over_p_quantiles=" + ",".join(f"{x:.6f}" for x in quantiles(min_a, qs)))
    print(f"{label}_min_x_over_p_quantiles=" + ",".join(f"{x:.6f}" for x in quantiles(min_x, qs)))


def audit_source(args: argparse.Namespace, source: str) -> None:
    rng = random.Random(args.seed)
    reservoir: list[tuple[int, int, int]] = []
    near_rows: list[tuple[int, int, int]] = []
    analog_rows: list[tuple[int, int, int]] = []
    by_c: Counter[int] = Counter()
    by_c_nmod8: Counter[tuple[int, int]] = Counter()
    pmod8: Counter[int] = Counter()
    pmod16: Counter[int] = Counter()
    target_hist: Counter[int] = Counter()
    a_bins: Counter[int] = Counter()
    x_bins: Counter[int] = Counter()
    min_a_bins: Counter[int] = Counter()
    min_x_bins: Counter[int] = Counter()

    rows_seen = 0
    max_p = 0
    for row_index, (p, A, x) in enumerate(parse_rows(source, args.limit)):
        rows_seen += 1
        max_p = p
        pmod8[p % 8] += 1
        pmod16[p % 16] += 1
        target_hist[target_order_count(p)] += 1
        a_bins[bin_unit(A, p, args.bins)] += 1
        x_bins[bin_unit(x, p, args.bins)] += 1
        min_a_bins[bin_unit(min(A, p - A), p, args.bins)] += 1
        min_x_bins[bin_unit(min(x, p - x), p, args.bins)] += 1

        analog = p24_analog(p, args.near_c)
        if analog is not None:
            n, c = analog
            by_c[c] += 1
            by_c_nmod8[(c, n % 8)] += 1
            if len(near_rows) < args.keep_near:
                near_rows.append((p, A, x))
            if c == 7 and n % 8 == 0 and len(analog_rows) < args.keep_near:
                analog_rows.append((p, A, x))

        update_reservoir(rng, reservoir, row_index, (p, A, x), args.sample_size)
        if args.progress and rows_seen % args.progress == 0:
            print(f"progress source={source} rows={rows_seen} max_p={max_p}", file=sys.stderr)

    print(f"source={source}")
    print(f"rows={rows_seen}")
    print(f"max_p={max_p}")
    print(f"max_bitlen={max_p.bit_length() if max_p else 0}")
    print(f"pmod8_counts={dict(sorted(pmod8.items()))}")
    print(f"pmod16_counts={dict(sorted(pmod16.items()))}")
    print(f"target_order_count_hist={dict(sorted(target_hist.items()))}")
    print("A_over_p_bins=" + ",".join(f"{i}:{a_bins[i]}" for i in range(args.bins)))
    print("x_over_p_bins=" + ",".join(f"{i}:{x_bins[i]}" for i in range(args.bins)))
    print("min_A_over_p_bins=" + ",".join(f"{i}:{min_a_bins[i]}" for i in range(args.bins)))
    print("min_x_over_p_bins=" + ",".join(f"{i}:{min_x_bins[i]}" for i in range(args.bins)))
    print(f"near_square_c_le_{args.near_c}_counts={dict(sorted(by_c.items()))}")
    print(
        f"near_square_c_nmod8_counts="
        + ",".join(f"{key}:{value}" for key, value in sorted(by_c_nmod8.items()))
    )
    summarize_triples("reservoir", reservoir, args.max_terminal)
    summarize_triples("near_square_retained", near_rows, args.max_terminal)
    summarize_triples("p24_analog_c7_n0mod8", analog_rows, args.max_terminal)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="*", default=[str(Path(__file__).resolve().parent / "upstream_DANGER3" / "pp24.txt.gz")])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--sample-size", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--near-c", type=int, default=255)
    ap.add_argument("--keep-near", type=int, default=50000)
    ap.add_argument("--max-terminal", type=int, default=50000)
    ap.add_argument("--bins", type=int, default=16)
    ap.add_argument("--progress", type=int, default=0)
    ap.add_argument("--pp28-url", action="store_true")
    ap.add_argument("--pp30-url", action="store_true")
    ap.add_argument("--pp32-url", action="store_true")
    args = ap.parse_args()

    sources = list(args.sources)
    if args.pp28_url:
        sources.append(PP28_URL)
    if args.pp30_url:
        sources.append(PP30_URL)
    if args.pp32_url:
        sources.append(PP32_URL)

    print("upstream large one-witness stream audit")
    for index, source in enumerate(sources):
        if index:
            print()
        audit_source(args, source)


if __name__ == "__main__":
    main()
