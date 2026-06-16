#!/usr/bin/env python3
"""Streaming audit for Sutherland's larger one-witness DANGER3 files.

The upstream README links pp28/pp30/pp32, but pp30 and pp32 are large gzip
streams.  This audit avoids saving those archives locally.  It uses:

* HEAD metadata for all three URLs,
* bounded prefix reads for all three URLs,
* one sparse full pass over pp28, which is small enough to stream once.

The point is not to mine every row.  It is to test whether the larger
one-witness files expose a scalable predictive rule for A, x0, split class,
terminal branch, p residues, near-square primes, or witness selection.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import io
import math
import statistics
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_DANGER3"
LOCAL_PP24 = UPSTREAM / "pp24.txt.gz"

URLS = {
    "pp28": "https://math.mit.edu/~drew/pp28.txt.gz",
    "pp30": "https://math.mit.edu/~drew/pp30.txt.gz",
    "pp32": "https://math.mit.edu/~drew/pp32.txt.gz",
}


@dataclass(frozen=True)
class Row:
    p: int
    A: int
    x: int


@dataclass(frozen=True)
class Feature:
    p: int
    A: int
    x: int
    split: int
    terminal: str
    fx_char: int
    sign_pair: tuple[int, int, int]
    target_orders: int
    delta_square: int


def open_local_rows(path: Path) -> Iterator[Row]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="ascii") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            p, A, x = (int(part) for part in line.split(","))
            yield Row(p, A, x)


def open_url_rows(url: str, timeout: int = 60) -> Iterator[Row]:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-p24-audit/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        with gzip.GzipFile(fileobj=response) as gz:
            with io.TextIOWrapper(gz, encoding="ascii") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    p, A, x = (int(part) for part in line.split(","))
                    yield Row(p, A, x)


def take(rows: Iterable[Row], limit: int | None) -> Iterator[Row]:
    for index, row in enumerate(rows):
        if limit is not None and index >= limit:
            break
        yield row


def head_metadata(url: str, timeout: int = 30) -> dict[str, str]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "codex-p24-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return {key.lower(): value for key, value in response.headers.items()}


def verifier_k(p: int) -> int:
    q = math.isqrt(p)
    return (q + 1 + math.isqrt(4 * q)).bit_length()


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def double_xz(p: int, C: int, X: int, Z: int) -> tuple[int, int]:
    U = (X + Z) * (X + Z) % p
    V = (X - Z) * (X - Z) % p
    W = (U - V) % p
    return U * V % p, W * ((V + C * W) % p) % p


def terminal_branch(p: int, A: int, x: int) -> str:
    inv4 = pow(4, -1, p)
    C = (A + 2) * inv4 % p
    X, Z = x % p, 1
    prev = (X, Z)
    for _ in range(verifier_k(p)):
        prev = (X, Z)
        X, Z = double_xz(p, C, X, Z)
    if Z % p != 0 or math.gcd(prev[1], p) != 1:
        return "not_verified"
    xt = prev[0] * pow(prev[1], -1, p) % p
    if xt == 0:
        return "zero_root"
    if (xt * xt + A * xt + 1) % p == 0:
        return "quadratic_root"
    return "other_root"


def target_order_count(p: int) -> int:
    k = verifier_k(p)
    step = 1 << k
    q = math.isqrt(p)
    lo = p + 1 - 2 * q
    hi = p + 1 + 2 * q
    first = lo + ((step - lo) % step)
    if first > hi:
        return 0
    return 1 + (hi - first) // step


def feature(row: Row) -> Feature:
    p, A, x = row.p, row.A, row.x
    split = legendre(A * A - 4, p)
    fx = x * (x * x + A * x + 1) % p
    n = math.isqrt(p)
    return Feature(
        p=p,
        A=A,
        x=x,
        split=split,
        terminal=terminal_branch(p, A, x),
        fx_char=legendre(fx, p),
        sign_pair=(legendre(A + 2, p), legendre(A - 2, p), split),
        target_orders=target_order_count(p),
        delta_square=p - n * n,
    )


def quantiles(values: list[float], qs: tuple[float, ...]) -> list[float]:
    if not values:
        return [0.0 for _ in qs]
    ordered = sorted(values)
    out = []
    for q in qs:
        index = min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))
        out.append(ordered[index])
    return out


class FeatureSummary:
    def __init__(self, label: str) -> None:
        self.label = label
        self.rows = 0
        self.first_p: int | None = None
        self.last_p: int | None = None
        self.split = collections.Counter()
        self.terminal = collections.Counter()
        self.fx = collections.Counter()
        self.signs = collections.Counter()
        self.mod8_split = collections.Counter()
        self.mod16_split = collections.Counter()
        self.mod12_split = collections.Counter()
        self.target_orders = collections.Counter()
        self.delta = collections.Counter()
        self.a_over_p: list[float] = []
        self.x_over_p: list[float] = []
        self.min_a_over_p: list[float] = []
        self.min_x_over_p: list[float] = []

    def add(self, feat: Feature) -> None:
        p, A, x = feat.p, feat.A, feat.x
        if self.first_p is None:
            self.first_p = p
        self.last_p = p
        self.rows += 1
        self.split[feat.split] += 1
        self.terminal[feat.terminal] += 1
        self.fx[feat.fx_char] += 1
        self.signs[feat.sign_pair] += 1
        self.mod8_split[(p % 8, feat.split)] += 1
        self.mod16_split[(p % 16, feat.split)] += 1
        self.mod12_split[(p % 12, feat.split)] += 1
        self.target_orders[feat.target_orders] += 1
        if feat.delta_square <= 64:
            self.delta[feat.delta_square] += 1
        self.a_over_p.append(A / p)
        self.x_over_p.append(x / p)
        self.min_a_over_p.append(min(A, p - A) / p)
        self.min_x_over_p.append(min(x, p - x) / p)

    def emit(self) -> None:
        print(f"summary={self.label}")
        print(f"  rows={self.rows}")
        print(f"  first_p={self.first_p}")
        print(f"  last_p={self.last_p}")
        print(f"  split_counts={dict(sorted(self.split.items()))}")
        print(f"  terminal_counts={dict(sorted(self.terminal.items()))}")
        print(f"  fx_char_counts={dict(sorted(self.fx.items()))}")
        print(f"  target_order_count_hist={dict(sorted(self.target_orders.items()))}")
        print(f"  top_sign_pairs={self.signs.most_common(8)}")
        print(f"  mod8_split_counts={dict(sorted(self.mod8_split.items()))}")
        print(f"  mod16_split_counts={dict(sorted(self.mod16_split.items()))}")
        print(f"  mod12_split_counts={dict(sorted(self.mod12_split.items()))}")
        print(f"  small_square_delta_counts={dict(sorted(self.delta.items()))}")
        qs = (0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99)
        print(
            "  A_over_p_quantiles_1_10_25_50_75_90_99="
            + ",".join(f"{x:.6f}" for x in quantiles(self.a_over_p, qs))
        )
        print(
            "  x_over_p_quantiles_1_10_25_50_75_90_99="
            + ",".join(f"{x:.6f}" for x in quantiles(self.x_over_p, qs))
        )
        print(
            "  min_A_over_p_quantiles_1_10_25_50_75_90_99="
            + ",".join(f"{x:.6f}" for x in quantiles(self.min_a_over_p, qs))
        )
        print(
            "  min_x_over_p_quantiles_1_10_25_50_75_90_99="
            + ",".join(f"{x:.6f}" for x in quantiles(self.min_x_over_p, qs))
        )


def row_hash(rows: Iterable[Row], limit: int | None) -> tuple[int, int | None, str]:
    digest = hashlib.sha256()
    count = 0
    last_p: int | None = None
    for row in take(rows, limit):
        count += 1
        last_p = row.p
        digest.update(f"{row.p},{row.A},{row.x}\n".encode("ascii"))
    return count, last_p, digest.hexdigest()


def audit_prefixes(prefix_rows: int) -> None:
    print("larger_one_witness_prefix_audit")
    print(f"prefix_rows={prefix_rows}")
    local_count, local_last, local_digest = row_hash(open_local_rows(LOCAL_PP24), prefix_rows)
    print(
        f"local_pp24_prefix rows={local_count} last_p={local_last} "
        f"sha256={local_digest}"
    )

    digests: dict[str, str] = {}
    for label, url in URLS.items():
        count, last_p, digest = row_hash(open_url_rows(url), prefix_rows)
        digests[label] = digest
        print(f"{label}_prefix rows={count} last_p={last_p} sha256={digest}")
    print(f"remote_prefix_hashes_equal={len(set(digests.values())) == 1}")
    print(f"remote_prefix_equals_local={all(digest == local_digest for digest in digests.values())}")
    print()

    for label, url in URLS.items():
        summary = FeatureSummary(f"{label}_prefix_{prefix_rows}")
        for row in take(open_url_rows(url), prefix_rows):
            summary.add(feature(row))
        summary.emit()
        print()


def audit_heads() -> None:
    print("larger_one_witness_head_metadata")
    for label, url in URLS.items():
        meta = head_metadata(url)
        fields = {
            "content-length": meta.get("content-length", ""),
            "last-modified": meta.get("last-modified", ""),
            "etag": meta.get("etag", ""),
            "accept-ranges": meta.get("accept-ranges", ""),
            "content-type": meta.get("content-type", ""),
        }
        print(f"{label} url={url}")
        for key, value in fields.items():
            print(f"  {key}={value}")
    print()


def summarize_numeric(values: list[int]) -> str:
    if not values:
        return "none"
    return (
        f"count={len(values)} min={min(values)} max={max(values)} "
        f"mean={statistics.mean(values):.3f}"
    )


def audit_pp28_sparse(stride: int, tail_keep: int, near_delta: int) -> None:
    print("pp28_sparse_full_stream_audit")
    print(f"stride={stride}")
    print(f"tail_keep={tail_keep}")
    print(f"near_delta={near_delta}")

    rows_seen = 0
    first_p: int | None = None
    last_p: int | None = None
    bit_counts = collections.Counter()
    mod8_counts = collections.Counter()
    mod16_counts = collections.Counter()
    mod12_counts = collections.Counter()
    target_count_full = collections.Counter()
    delta7_rows: list[Row] = []
    near_rows: list[Row] = []
    stride_summary = FeatureSummary("pp28_stride_sample")
    by_bit: dict[int, FeatureSummary] = {}
    tail: collections.deque[Row] = collections.deque(maxlen=tail_keep)

    for index, row in enumerate(open_url_rows(URLS["pp28"]), start=1):
        rows_seen = index
        if first_p is None:
            first_p = row.p
        last_p = row.p
        bit_counts[row.p.bit_length()] += 1
        mod8_counts[row.p % 8] += 1
        mod16_counts[row.p % 16] += 1
        mod12_counts[row.p % 12] += 1
        target_count_full[target_order_count(row.p)] += 1
        tail.append(row)

        n = math.isqrt(row.p)
        delta = row.p - n * n
        if delta == 7:
            delta7_rows.append(row)
        if delta <= near_delta:
            near_rows.append(row)

        if (index - 1) % stride == 0:
            feat = feature(row)
            stride_summary.add(feat)
            band = row.p.bit_length()
            by_bit.setdefault(band, FeatureSummary(f"pp28_stride_bitlen_{band}")).add(feat)

    print(f"rows_seen={rows_seen}")
    print(f"first_p={first_p}")
    print(f"last_p={last_p}")
    print(f"bit_length_counts={dict(sorted(bit_counts.items()))}")
    print(f"p_mod8_counts={dict(sorted(mod8_counts.items()))}")
    print(f"p_mod16_counts={dict(sorted(mod16_counts.items()))}")
    print(f"p_mod12_counts={dict(sorted(mod12_counts.items()))}")
    print(f"target_order_count_full_hist={dict(sorted(target_count_full.items()))}")
    print(f"near_square_delta_7={summarize_numeric([row.p for row in delta7_rows])}")
    print(f"near_square_delta_le_{near_delta}={summarize_numeric([row.p for row in near_rows])}")
    print()

    stride_summary.emit()
    print()

    print("pp28_stride_sample_by_bit_length")
    for band in sorted(by_bit):
        by_bit[band].emit()
    print()

    tail_summary = FeatureSummary(f"pp28_tail_{len(tail)}")
    for row in tail:
        tail_summary.add(feature(row))
    tail_summary.emit()
    print()

    delta7_summary = FeatureSummary("pp28_near_square_delta_7")
    for row in delta7_rows:
        delta7_summary.add(feature(row))
    delta7_summary.emit()
    print()

    near_summary = FeatureSummary(f"pp28_near_square_delta_le_{near_delta}")
    for row in near_rows:
        near_summary.add(feature(row))
    near_summary.emit()
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--heads", action="store_true")
    parser.add_argument("--prefixes", action="store_true")
    parser.add_argument("--pp28-sparse", action="store_true")
    parser.add_argument("--prefix-rows", type=int, default=200_000)
    parser.add_argument("--stride", type=int, default=997)
    parser.add_argument("--tail-keep", type=int, default=20_000)
    parser.add_argument("--near-delta", type=int, default=32)
    args = parser.parse_args()

    if not (args.heads or args.prefixes or args.pp28_sparse):
        args.heads = True
        args.prefixes = True

    if args.heads:
        audit_heads()
    if args.prefixes:
        audit_prefixes(args.prefix_rows)
    if args.pp28_sparse:
        audit_pp28_sparse(args.stride, args.tail_keep, args.near_delta)


if __name__ == "__main__":
    main()
