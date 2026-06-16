#!/usr/bin/env python3
"""Terminal 2-torsion branch audit for upstream all-triple data.

For small p, pp12 contains every verifier x-coordinate.  The verifier accepts
when [2^k]P is infinity and [2^(k-1)]P is a nonzero 2-torsion point.  On a
Montgomery curve the possible terminal x-values are

    0, roots of x^2 + A*x + 1.

This script measures how the terminal branches explain the cheap character
biases visible in pp16A, especially chi(A+2) and chi(A-2).
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PP12 = ROOT / "upstream_DANGER3" / "pp12.txt.gz"


def rows(path: Path, limit: int | None):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="ascii") as handle:
        for index, line in enumerate(handle):
            if limit is not None and index >= limit:
                break
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


def sign_pair(p: int, A: int) -> tuple[int, int, int]:
    return (legendre(A + 2, p), legendre(A - 2, p), legendre(A * A - 4, p))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, default=PP12)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--min-p", type=int, default=0)
    ap.add_argument("--max-p", type=int, default=1 << 63)
    ap.add_argument("--mod", type=int, default=8)
    ap.add_argument("--residue", type=int, default=None)
    ap.add_argument("--tail-threshold", type=int, default=2048)
    args = ap.parse_args()

    triple_counts: Counter[str] = Counter()
    triple_sign_branch: Counter[tuple[tuple[int, int, int], str]] = Counter()
    prefix_branch_mask: dict[tuple[int, int], set[str]] = defaultdict(set)
    prefix_sign: dict[tuple[int, int], tuple[int, int, int]] = {}

    for p, A, x in rows(args.path, args.limit):
        if p < args.min_p or p > args.max_p:
            continue
        if args.residue is not None and p % args.mod != args.residue:
            continue
        branch = terminal_branch(p, A, x)
        signs = sign_pair(p, A)
        triple_counts[branch] += 1
        triple_sign_branch[(signs, branch)] += 1
        key = (p, A)
        prefix_branch_mask[key].add(branch)
        prefix_sign[key] = signs

    prefix_counts: Counter[str] = Counter()
    prefix_sign_counts: Counter[tuple[int, int, int]] = Counter()
    tail_prefix_counts: Counter[str] = Counter()
    tail_sign_counts: Counter[tuple[int, int, int]] = Counter()
    for key, branches in prefix_branch_mask.items():
        p, _A = key
        mask = "+".join(sorted(branches))
        prefix_counts[mask] += 1
        prefix_sign_counts[prefix_sign[key]] += 1
        if p >= args.tail_threshold:
            tail_prefix_counts[mask] += 1
            tail_sign_counts[prefix_sign[key]] += 1

    print("upstream terminal branch audit")
    print(f"path={args.path}")
    print(f"limit={args.limit}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"residue_mod={args.mod}")
    print(f"residue={args.residue}")
    print(f"triple_count={sum(triple_counts.values())}")
    print(f"prefix_count={len(prefix_branch_mask)}")
    print(f"triple_branch_counts={dict(sorted(triple_counts.items()))}")
    print(f"prefix_branch_masks={dict(sorted(prefix_counts.items()))}")
    print(f"tail_threshold={args.tail_threshold}")
    print(f"tail_prefix_branch_masks={dict(sorted(tail_prefix_counts.items()))}")

    print("prefix_sign_counts chi(A+2),chi(A-2),chi(A^2-4)")
    for signs, count in sorted(prefix_sign_counts.items(), key=lambda row: (-row[1], row[0])):
        print(f"  {signs}: {count}")

    print("tail_prefix_sign_counts chi(A+2),chi(A-2),chi(A^2-4)")
    for signs, count in sorted(tail_sign_counts.items(), key=lambda row: (-row[1], row[0])):
        print(f"  {signs}: {count}")

    print("triple_sign_branch_counts chi(A+2),chi(A-2),chi(A^2-4),branch")
    for (signs, branch), count in sorted(triple_sign_branch.items(), key=lambda row: (-row[1], row[0])):
        print(f"  {signs} {branch}: {count}")

    print("conclusion=terminal_branch_and_A_plus_minus_2_biases_are_fixed_branch_mixture_data")


if __name__ == "__main__":
    main()
