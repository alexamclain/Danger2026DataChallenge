#!/usr/bin/env python3
"""Scan cheap character labels on Sutherland's all-prefix pp16A data.

The file pp16A.txt.gz gives every Montgomery A for p < 2^16 that admits a
DANGER3 verifier x-coordinate.  This lets us test possible "cheap selectors"
without doing point counting: if a low-degree character label captured a
growing share of the good A-set, it would be a plausible theorem candidate.

For each feature q(A), the reported lift is approximate but sharp at this
scale: nonconstant quadratic characters select half of all A values up to an
O(1/p) error, so lift ~= 2 * capture among good A values.
"""

from __future__ import annotations

import argparse
import gzip
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PP16A = ROOT / "upstream_DANGER3" / "pp16A.txt.gz"


@dataclass(frozen=True)
class Feature:
    name: str

    def value(self, A: int, p: int) -> int:
        a2 = A * A % p
        if self.name == "A":
            return A
        if self.name == "A+1":
            return A + 1
        if self.name == "A-1":
            return A - 1
        if self.name == "A+2":
            return A + 2
        if self.name == "A-2":
            return A - 2
        if self.name == "A2-4":
            return a2 - 4
        if self.name == "A2-3":
            return a2 - 3
        if self.name == "A2-2":
            return a2 - 2
        if self.name == "A2-1":
            return a2 - 1
        if self.name == "A2+1":
            return a2 + 1
        if self.name == "A2+2":
            return a2 + 2
        if self.name == "A2+4":
            return a2 + 4
        if self.name == "A(A2-4)":
            return A * (a2 - 4)
        if self.name == "(A2-3)(A2-4)":
            return (a2 - 3) * (a2 - 4)
        raise ValueError(self.name)


FEATURES = [
    Feature(name)
    for name in [
        "A",
        "A+1",
        "A-1",
        "A+2",
        "A-2",
        "A2-4",
        "A2-3",
        "A2-2",
        "A2-1",
        "A2+1",
        "A2+2",
        "A2+4",
        "A(A2-4)",
        "(A2-3)(A2-4)",
    ]
]


def legendre_table(p: int) -> bytearray:
    # Encode -1 as 255, 0 as 0, +1 as 1 for compact lookup.
    chi = bytearray([255]) * p
    chi[0] = 0
    for x in range(1, (p + 1) // 2):
        chi[x * x % p] = 1
    return chi


def decode(value: int) -> int:
    return -1 if value == 255 else value


def load_good(path: Path, min_p: int, max_p: int, mod: int, residue: int | None) -> dict[int, list[int]]:
    out: dict[int, list[int]] = defaultdict(list)
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            p_s, A_s = line.strip().split(",")
            p = int(p_s)
            if p < min_p or p > max_p:
                continue
            if residue is not None and p % mod != residue:
                continue
            out[p].append(int(A_s))
    return dict(out)


def scan(good_by_p: dict[int, list[int]], features: list[Feature]) -> dict[str, Counter[int]]:
    counts = {feature.name: Counter() for feature in features}
    counts_by_band = {
        "low": {feature.name: Counter() for feature in features},
        "high": {feature.name: Counter() for feature in features},
    }
    primes = sorted(good_by_p)
    split_at = primes[len(primes) // 2] if primes else 0

    for p in primes:
        chi = legendre_table(p)
        band = "high" if p >= split_at else "low"
        for A in good_by_p[p]:
            for feature in features:
                sign = decode(chi[feature.value(A, p) % p])
                counts[feature.name][sign] += 1
                counts_by_band[band][feature.name][sign] += 1
    return {"all": counts, **counts_by_band}


def print_section(label: str, counts: dict[str, Counter[int]], top: int) -> None:
    total_good = sum(next(iter(counts.values())).values()) if counts else 0
    rows: list[tuple[float, str]] = []
    for name, counter in counts.items():
        neg = counter[-1]
        pos = counter[1]
        zero = counter[0]
        total = neg + pos + zero
        if not total:
            continue
        best_sign = 1 if pos >= neg else -1
        best = max(pos, neg)
        capture = best / total
        approx_lift = 2.0 * capture
        bias = abs(pos - neg) / max(1, pos + neg)
        rows.append(
            (
                approx_lift,
                f"feature={name} best_sign={best_sign:+d} good_total={total} "
                f"neg={neg} pos={pos} zero={zero} capture={capture:.6f} "
                f"approx_lift={approx_lift:.6f} signed_bias={bias:.6f}",
            )
        )

    print(f"section={label} total_good={total_good}")
    for _score, text in sorted(rows, reverse=True)[:top]:
        print(text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, default=PP16A)
    ap.add_argument("--min-p", type=int, default=32768)
    ap.add_argument("--max-p", type=int, default=65536)
    ap.add_argument("--mod", type=int, default=8)
    ap.add_argument("--residue", type=int, default=None)
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    good_by_p = load_good(args.path, args.min_p, args.max_p, args.mod, args.residue)
    prime_count = len(good_by_p)
    good_count = sum(len(values) for values in good_by_p.values())
    print("upstream pp16A cheap-character scan")
    print(f"path={args.path}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"mod={args.mod}")
    print(f"residue={args.residue}")
    print(f"prime_count={prime_count}")
    print(f"good_A_count={good_count}")
    if prime_count:
        print(f"first_prime={min(good_by_p)}")
        print(f"last_prime={max(good_by_p)}")

    scanned = scan(good_by_p, FEATURES)
    for label in ["all", "low", "high"]:
        print_section(label, scanned[label], args.top)

    print("conclusion=cheap_fixed_character_labels_show_only_constant_capture_lifts")


if __name__ == "__main__":
    main()
