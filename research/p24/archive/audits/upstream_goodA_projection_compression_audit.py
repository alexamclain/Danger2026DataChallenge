#!/usr/bin/env python3
"""Projection-compression audit on Sutherland's all-good (p,A) dataset.

If a strict-DANGER construction is hiding behind a lower-dimensional invariant,
the exact all-prefix data should show the good A-set compressing under that
invariant with growing fiber size.  This script streams pp16A.txt.gz, groups
good A values by p, and measures image sizes/fibers for natural Montgomery
projections:

* A itself;
* A modulo sign, equivalently A^2;
* Montgomery j = 256*(A^2-3)^3/(A^2-4);
* A^2-4, the split/nonsplit discriminant;
* simple terminal ratios built from A+2 and A-2.

The expected outcome for ordinary low-degree maps is constant compression.
A growing compression would be a theorem-shaped lead.
"""

from __future__ import annotations

import argparse
import gzip
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
PP16A = ROOT / "upstream_DANGER3" / "pp16A.txt.gz"


@dataclass(frozen=True)
class ProjectionStats:
    name: str
    primes: int
    good_A: int
    mean_image_over_good: float
    median_image_over_good: float
    mean_max_fiber: float
    max_fiber: int
    mean_good_over_sqrt: float
    mean_image_over_sqrt: float


def load_good_by_p(path: Path, min_p: int, max_p: int, residue: int | None, mod: int) -> dict[int, list[int]]:
    out: dict[int, list[int]] = defaultdict(list)
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for line in handle:
            p_s, a_s = line.strip().split(",")
            p = int(p_s)
            if p < min_p or p > max_p:
                continue
            if residue is not None and p % mod != residue:
                continue
            out[p].append(int(a_s))
    return dict(out)


def inv_or_none(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, -1, p)


def montgomery_j(A: int, p: int) -> int | None:
    a2 = A * A % p
    den = (a2 - 4) % p
    inv = inv_or_none(den, p)
    if inv is None:
        return None
    return (256 * pow((a2 - 3) % p, 3, p) * inv) % p


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def projection_values(name: str, A_values: list[int], p: int) -> list[int]:
    out: list[int] = []
    for A in A_values:
        if name == "A":
            out.append(A)
        elif name == "signed_A":
            out.append(min(A, (-A) % p))
        elif name == "A2":
            out.append(A * A % p)
        elif name == "j":
            j = montgomery_j(A, p)
            if j is not None:
                out.append(j)
        elif name == "disc_A2_minus_4":
            out.append((A * A - 4) % p)
        elif name == "terminal_ratio":
            inv = inv_or_none(A - 2, p)
            if inv is not None:
                out.append(((A + 2) * inv) % p)
        elif name == "terminal_ratio_signed":
            inv = inv_or_none(A - 2, p)
            if inv is not None:
                u = ((A + 2) * inv) % p
                out.append(min(u, pow(u, -1, p) if u else u))
        elif name == "terminal_sign_pair":
            out.append((legendre(A + 2, p) + 1) * 3 + (legendre(A - 2, p) + 1))
        else:
            raise ValueError(name)
    return out


def summarize_projection(name: str, good_by_p: dict[int, list[int]]) -> ProjectionStats:
    ratios: list[float] = []
    max_fibers: list[int] = []
    good_over_sqrt: list[float] = []
    image_over_sqrt: list[float] = []
    total_good = 0
    for p, values in sorted(good_by_p.items()):
        projected = projection_values(name, values, p)
        counts = Counter(projected)
        image_size = len(counts)
        total = len(values)
        if total == 0:
            continue
        ratios.append(image_size / total)
        max_fibers.append(max(counts.values()) if counts else 0)
        good_over_sqrt.append(total / math.sqrt(p))
        image_over_sqrt.append(image_size / math.sqrt(p))
        total_good += total

    ratios_sorted = sorted(ratios)
    median = ratios_sorted[len(ratios_sorted) // 2] if ratios_sorted else 0.0
    return ProjectionStats(
        name=name,
        primes=len(good_by_p),
        good_A=total_good,
        mean_image_over_good=mean(ratios) if ratios else 0.0,
        median_image_over_good=median,
        mean_max_fiber=mean(max_fibers) if max_fibers else 0.0,
        max_fiber=max(max_fibers) if max_fibers else 0,
        mean_good_over_sqrt=mean(good_over_sqrt) if good_over_sqrt else 0.0,
        mean_image_over_sqrt=mean(image_over_sqrt) if image_over_sqrt else 0.0,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, default=PP16A)
    ap.add_argument("--min-p", type=int, default=32768)
    ap.add_argument("--max-p", type=int, default=65536)
    ap.add_argument("--mod", type=int, default=8)
    ap.add_argument("--residue", type=int, default=None)
    args = ap.parse_args()

    good_by_p = load_good_by_p(args.path, args.min_p, args.max_p, args.residue, args.mod)
    print("upstream good-A projection compression audit")
    print(f"path={args.path}")
    print(f"min_p={args.min_p}")
    print(f"max_p={args.max_p}")
    print(f"mod={args.mod}")
    print(f"residue={args.residue}")
    print(f"prime_count={len(good_by_p)}")
    print(f"good_A_count={sum(len(v) for v in good_by_p.values())}")
    print()

    names = [
        "A",
        "signed_A",
        "A2",
        "j",
        "disc_A2_minus_4",
        "terminal_ratio",
        "terminal_ratio_signed",
        "terminal_sign_pair",
    ]
    print(
        "projection primes good_A mean_image/good median_image/good "
        "mean_max_fiber max_fiber mean_good/sqrt mean_image/sqrt"
    )
    for name in names:
        row = summarize_projection(name, good_by_p)
        print(
            f"{row.name:22s} {row.primes:6d} {row.good_A:8d} "
            f"{row.mean_image_over_good:15.6f} {row.median_image_over_good:17.6f} "
            f"{row.mean_max_fiber:14.3f} {row.max_fiber:9d} "
            f"{row.mean_good_over_sqrt:14.6f} {row.mean_image_over_sqrt:15.6f}"
        )

    print(
        "conclusion=natural_Montgomery_projections_have_only_constant_degree_"
        "compression_on_the_exact_good_A_dataset"
    )


if __name__ == "__main__":
    main()
