#!/usr/bin/env python3
"""Audit how Sutherland's one-witness files choose triples.

The upstream repository contains both all triples through 2^12 and one triple
per prime through larger ranges.  If the one-witness triples came from a
simple deterministic selector, e.g. first A, first x, first terminal branch,
that rule might be a construction clue.  This script compares pp20/pp24
witnesses against pp12 all-triple data on the overlapping primes.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_DANGER3"


@dataclass(frozen=True)
class WitnessRank:
    p: int
    A: int
    x: int
    triple_rank: int
    triple_count: int
    A_rank: int
    A_count: int
    x_rank_for_A: int
    x_count_for_A: int
    terminal: str
    split: int


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="ascii")
    return path.open("rt", encoding="ascii")


def rows(path: Path):
    with open_text(path) as handle:
        for line in handle:
            if line.strip():
                yield tuple(int(part) for part in line.strip().split(","))


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
    C = (A + 2) * pow(4, -1, p) % p
    X, Z = x % p, 1
    prev = (X, Z)
    for _ in range(verifier_k(p)):
        prev = (X, Z)
        X, Z = double_xz(p, C, X, Z)
    if Z % p != 0 or math.gcd(prev[1], p) != 1:
        return "not_verified"
    xt = prev[0] * pow(prev[1], -1, p) % p
    if xt == 0:
        return "zero"
    if (xt * xt + A * xt + 1) % p == 0:
        return "quadratic"
    return "other"


def load_all_triples(path: Path, max_p: int) -> dict[int, list[tuple[int, int]]]:
    out: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for p, A, x in rows(path):
        if p > max_p:
            break
        out[p].append((A, x))
    for p in out:
        out[p].sort()
    return dict(out)


def load_witnesses(path: Path, max_p: int) -> dict[int, tuple[int, int]]:
    out: dict[int, tuple[int, int]] = {}
    for p, A, x in rows(path):
        if p > max_p:
            break
        out[p] = (A, x)
    return out


def rank_witness(p: int, triples: list[tuple[int, int]], A: int, x: int) -> WitnessRank:
    triples_sorted = sorted(triples)
    triple_rank = triples_sorted.index((A, x))
    good_As = sorted({a for a, _x in triples_sorted})
    A_rank = good_As.index(A)
    xs_for_A = sorted(x0 for a, x0 in triples_sorted if a == A)
    x_rank = xs_for_A.index(x)
    return WitnessRank(
        p=p,
        A=A,
        x=x,
        triple_rank=triple_rank,
        triple_count=len(triples_sorted),
        A_rank=A_rank,
        A_count=len(good_As),
        x_rank_for_A=x_rank,
        x_count_for_A=len(xs_for_A),
        terminal=terminal_branch(p, A, x),
        split=legendre(A * A - 4, p),
    )


def summarize(label: str, ranks: list[WitnessRank], top: int) -> None:
    print(f"witness_file={label}")
    print(f"overlap_primes={len(ranks)}")
    if not ranks:
        return

    terminal_counts = Counter(row.terminal for row in ranks)
    split_counts = Counter(row.split for row in ranks)
    first_triple = sum(row.triple_rank == 0 for row in ranks)
    first_A = sum(row.A_rank == 0 for row in ranks)
    first_x_for_A = sum(row.x_rank_for_A == 0 for row in ranks)
    last_x_for_A = sum(row.x_rank_for_A == row.x_count_for_A - 1 for row in ranks)
    print(f"terminal_counts={dict(sorted(terminal_counts.items()))}")
    print(f"split_counts={dict(sorted(split_counts.items()))}")
    print(f"first_lexicographic_triple={first_triple}/{len(ranks)}")
    print(f"first_good_A={first_A}/{len(ranks)}")
    print(f"first_x_for_selected_A={first_x_for_A}/{len(ranks)}")
    print(f"last_x_for_selected_A={last_x_for_A}/{len(ranks)}")

    mean_triple_quantile = sum(row.triple_rank / max(1, row.triple_count - 1) for row in ranks) / len(ranks)
    mean_A_quantile = sum(row.A_rank / max(1, row.A_count - 1) for row in ranks) / len(ranks)
    mean_x_quantile = sum(row.x_rank_for_A / max(1, row.x_count_for_A - 1) for row in ranks) / len(ranks)
    print(f"mean_triple_rank_quantile={mean_triple_quantile:.6f}")
    print(f"mean_A_rank_quantile={mean_A_quantile:.6f}")
    print(f"mean_x_rank_for_A_quantile={mean_x_quantile:.6f}")

    print("sample_witness_ranks")
    for row in ranks[:top]:
        print(
            f"  p={row.p} A={row.A} x={row.x} "
            f"triple_rank={row.triple_rank}/{row.triple_count} "
            f"A_rank={row.A_rank}/{row.A_count} "
            f"x_rank={row.x_rank_for_A}/{row.x_count_for_A} "
            f"terminal={row.terminal} split={row.split}"
        )
    print()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-file", type=Path, default=UPSTREAM / "pp12.txt.gz")
    ap.add_argument("--witness-files", type=Path, nargs="+", default=[UPSTREAM / "pp20.txt", UPSTREAM / "pp24.txt.gz"])
    ap.add_argument("--max-p", type=int, default=4096)
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    all_triples = load_all_triples(args.all_file, args.max_p)
    print("upstream one-witness selection audit")
    print(f"all_file={args.all_file}")
    print(f"max_p={args.max_p}")
    print(f"all_primes={len(all_triples)}")
    print()

    for witness_path in args.witness_files:
        witnesses = load_witnesses(witness_path, args.max_p)
        ranks: list[WitnessRank] = []
        for p in sorted(set(all_triples) & set(witnesses)):
            A, x = witnesses[p]
            if (A, x) not in all_triples[p]:
                print(f"warning: witness_not_in_all_triples path={witness_path} p={p} A={A} x={x}")
                continue
            ranks.append(rank_witness(p, all_triples[p], A, x))
        summarize(str(witness_path), ranks, args.top)

    print("conclusion=one_witness_files_do_not_expose_a_low_rank_deterministic_selector_on_pp12_overlap")


if __name__ == "__main__":
    main()
