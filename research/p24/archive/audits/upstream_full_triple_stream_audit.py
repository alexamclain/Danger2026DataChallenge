#!/usr/bin/env python3
"""Bounded stream audit for upstream full-triple archives pp14/pp16.

The full-triple files contain every verifier x-coordinate, not just one
representative per prime.  This script streams a bounded window or stride
sample and measures x0/terminal/sign features without saving the archives.

Use it to extend local pp12 observations into pp14-sized primes while avoiding
large CPU-bound verifier replays over every row.
"""

from __future__ import annotations

import argparse
import gzip
import io
import math
import urllib.request
from collections import Counter, deque
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

from upstream_dataset_feature_audit import legendre, quantiles, terminal_branch, verifier_k


ROOT = Path(__file__).resolve().parent
PP12 = ROOT / "upstream_DANGER3" / "pp12.txt.gz"
PP14_URL = "https://math.mit.edu/~drew/pp14.txt.gz"
PP16_URL = "https://math.mit.edu/~drew/pp16.txt.gz"


@contextmanager
def open_stream(source: str) -> Iterator[TextIO]:
    if source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": "codex-p24-full-triple-audit/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            with gzip.GzipFile(fileobj=response) as gz:
                with io.TextIOWrapper(gz, encoding="ascii") as handle:
                    yield handle
        return
    path = Path(source)
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="ascii") as handle:
            yield handle
    else:
        with path.open("rt", encoding="ascii") as handle:
            yield handle


def parse_rows(source: str, skip: int, limit: int | None, stride: int) -> Iterator[tuple[int, int, int, int]]:
    kept = 0
    with open_stream(source) as handle:
        for index, line in enumerate(handle):
            if index < skip:
                continue
            if stride > 1 and (index - skip) % stride:
                continue
            if limit is not None and kept >= limit:
                break
            p_s, a_s, x_s = line.strip().split(",")
            kept += 1
            yield index, int(p_s), int(a_s), int(x_s)


def bin_unit(value: int, modulus: int, bins: int) -> int:
    return min(bins - 1, (value * bins) // modulus)


def summarize(label: str, triples: list[tuple[int, int, int]], max_terminal: int, bins: int) -> None:
    split = Counter()
    signs = Counter()
    terminal = Counter()
    pmod8_split = Counter()
    min_a = []
    min_x = []
    a_bins = Counter()
    x_bins = Counter()
    k_hist = Counter()
    prefixes: set[tuple[int, int]] = set()
    terminal_seen = 0

    for p, A, x in triples:
        s = legendre(A * A - 4, p)
        sign_pair = (legendre(A + 2, p), legendre(A - 2, p), s)
        split[s] += 1
        signs[sign_pair] += 1
        pmod8_split[(p % 8, s)] += 1
        min_a.append(min(A, p - A) / p)
        min_x.append(min(x, p - x) / p)
        a_bins[bin_unit(A, p, bins)] += 1
        x_bins[bin_unit(x, p, bins)] += 1
        k_hist[verifier_k(p)] += 1
        prefixes.add((p, A))
        if terminal_seen < max_terminal:
            terminal[terminal_branch(p, A, x, verifier_k(p))] += 1
            terminal_seen += 1

    print(f"{label}_rows={len(triples)}")
    if not triples:
        return
    print(f"{label}_first_p={triples[0][0]}")
    print(f"{label}_last_p={triples[-1][0]}")
    print(f"{label}_distinct_prefixes={len(prefixes)}")
    print(f"{label}_x_per_prefix={len(triples) / len(prefixes):.6f}")
    print(f"{label}_verifier_k_hist={dict(sorted(k_hist.items()))}")
    print(f"{label}_split_counts={dict(sorted(split.items()))}")
    print(f"{label}_terminal_rows={terminal_seen}")
    print(f"{label}_terminal_counts={dict(sorted(terminal.items()))}")
    print(f"{label}_top_sign_pairs={signs.most_common(8)}")
    print(f"{label}_pmod8_split_counts={dict(sorted(pmod8_split.items()))}")
    print(f"{label}_A_over_p_bins=" + ",".join(f"{i}:{a_bins[i]}" for i in range(bins)))
    print(f"{label}_x_over_p_bins=" + ",".join(f"{i}:{x_bins[i]}" for i in range(bins)))
    qs = (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99)
    print(f"{label}_min_A_over_p_quantiles=" + ",".join(f"{v:.6f}" for v in quantiles(min_a, qs)))
    print(f"{label}_min_x_over_p_quantiles=" + ",".join(f"{v:.6f}" for v in quantiles(min_x, qs)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", default=str(PP12))
    ap.add_argument("--pp14-url", action="store_true")
    ap.add_argument("--pp16-url", action="store_true")
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--limit", type=int, default=200000)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--tail-keep", type=int, default=0)
    ap.add_argument("--max-terminal", type=int, default=20000)
    ap.add_argument("--bins", type=int, default=16)
    args = ap.parse_args()

    source = args.source
    if args.pp14_url:
        source = PP14_URL
    if args.pp16_url:
        source = PP16_URL

    rows: list[tuple[int, int, int]] = []
    tail: deque[tuple[int, int, int]] = deque(maxlen=args.tail_keep)
    seen = 0
    first_index = None
    last_index = None
    for index, p, A, x in parse_rows(source, args.skip, args.limit, args.stride):
        if first_index is None:
            first_index = index
        last_index = index
        rows.append((p, A, x))
        if args.tail_keep:
            tail.append((p, A, x))
        seen += 1

    print("upstream full-triple stream audit")
    print(f"source={source}")
    print(f"skip={args.skip}")
    print(f"limit={args.limit}")
    print(f"stride={args.stride}")
    print(f"sample_rows={seen}")
    print(f"first_source_index={first_index}")
    print(f"last_source_index={last_index}")
    summarize("sample", rows, args.max_terminal, args.bins)
    if args.tail_keep:
        print()
        summarize("tail", list(tail), args.max_terminal, args.bins)
    print("conclusion=bounded_full_triple_stream_shows_x0_distribution_and_terminal_branch_structure")


if __name__ == "__main__":
    main()
