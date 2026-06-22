#!/usr/bin/env python3
"""Monomial Belyi recurrence screen on the p27 lambda line.

The K-line Belyi coordinate is lambda = -K^2/4, whose branch set is
{0,1,infinity}.  Although lambda is not a rational p27 source quotient by
itself, a recurrence or coboundary visible on this normalized line would be a
serious clue for K-level branch-class extraction.

This probe tests fixed maps only:

    phi = left_S3 o (lambda -> lambda^m) o right_S3

for d4(lambda) = +/- d3(phi(lambda)) and the reverse direction.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_lambda_branch_divisor_probe import LambdaRow, collect_rows, parse_ints


@dataclass(frozen=True)
class Transform:
    name: str
    fn: Callable[[int, int], int | None]


@dataclass(frozen=True)
class LambdaHit:
    name: str
    polarity: int
    covered: int
    matches: int
    domain_size: int
    undefined: int


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def s3_transforms() -> list[Transform]:
    return [
        Transform("u", lambda u, p: u % p),
        Transform("1-u", lambda u, p: (1 - u) % p),
        Transform("1/u", lambda u, p: inv(u, p)),
        Transform("1/(1-u)", lambda u, p: inv(1 - u, p)),
        Transform("u/(u-1)", lambda u, p: None if inv(u - 1, p) is None else u * inv(u - 1, p) % p),
        Transform("(u-1)/u", lambda u, p: None if inv(u, p) is None else (u - 1) * inv(u, p) % p),
    ]


def compose(left: Transform, degree: int, right: Transform, u: int, p: int) -> int | None:
    first = right.fn(u, p)
    if first is None:
        return None
    middle = pow(first, degree, p)
    return left.fn(middle, p)


def row_map(rows: list[LambdaRow]) -> dict[int, int]:
    return {row.lam: row.target for row in rows}


def score_map(
    source: dict[int, int],
    target: dict[int, int],
    q: int,
    name: str,
    fn: Callable[[int, int], int | None],
) -> list[LambdaHit]:
    base: Counter = Counter()
    polarity_matches = Counter()
    for value, target_sign in target.items():
        image = fn(value, q)
        if image is None:
            base["undefined"] += 1
            continue
        image %= q
        source_sign = source.get(image)
        if source_sign is None:
            continue
        base["covered"] += 1
        for polarity in (1, -1):
            if target_sign == polarity * source_sign:
                polarity_matches[polarity] += 1

    return [
        LambdaHit(
            name=name,
            polarity=polarity,
            covered=base["covered"],
            matches=polarity_matches[polarity],
            domain_size=len(target),
            undefined=base["undefined"],
        )
        for polarity in (1, -1)
    ]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_hits(prefix: str, hits: list[LambdaHit], keep_best: int) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
        return
    for hit in sorted(
        hits,
        key=lambda item: (
            item.matches == item.covered == item.domain_size,
            item.covered,
            item.matches,
        ),
        reverse=True,
    )[:keep_best]:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"undefined={hit.undefined}"
        )


def run_field(q: int, degrees: list[int], keep_best: int) -> None:
    d3_rows, d4_rows, setup = collect_rows(q)
    d3 = row_map(d3_rows)
    d4 = row_map(d4_rows)
    transforms = s3_transforms()

    setup_stats = Counter({f"setup_{key}": value for key, value in setup.items()})
    setup_stats["q_mod_16"] = q % 16
    setup_stats["chi_minus_one"] = legendre(-1, q)
    setup_stats["chi_two"] = legendre(2, q)
    setup_stats["d3_lambda_rows"] = len(d3)
    setup_stats["d4_lambda_rows"] = len(d4)
    print_counter(f"q{q}_setup", setup_stats)

    stats: Counter = Counter()
    forward_hits: list[LambdaHit] = []
    reverse_hits: list[LambdaHit] = []
    for left in transforms:
        for degree in degrees:
            for right in transforms:
                name = f"{left.name} o u^{degree} o {right.name}"
                fn = lambda u, p, ll=left, dd=degree, rr=right: compose(ll, dd, rr, u, p)
                stats["maps_tested"] += 1
                forward = score_map(d3, d4, q, name, fn)
                reverse = score_map(d4, d3, q, name, fn)
                forward_hits.extend(forward)
                reverse_hits.extend(reverse)
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in forward):
                    stats["forward_exact"] += 1
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in reverse):
                    stats["reverse_exact"] += 1

    if forward_hits:
        best_forward = max(forward_hits, key=lambda hit: (hit.covered, hit.matches))
        stats["forward_best_covered"] = best_forward.covered
        stats["forward_best_matches"] = best_forward.matches
        stats["forward_best_coverage_x1000000"] = best_forward.covered * 1_000_000 // best_forward.domain_size
        stats["forward_best_match_x1000000"] = best_forward.matches * 1_000_000 // best_forward.domain_size
    if reverse_hits:
        best_reverse = max(reverse_hits, key=lambda hit: (hit.covered, hit.matches))
        stats["reverse_best_covered"] = best_reverse.covered
        stats["reverse_best_matches"] = best_reverse.matches
        stats["reverse_best_coverage_x1000000"] = best_reverse.covered * 1_000_000 // best_reverse.domain_size
        stats["reverse_best_match_x1000000"] = best_reverse.matches * 1_000_000 // best_reverse.domain_size

    print_counter(f"q{q}_lambda_monomial_recurrence_stats", stats)
    print_hits(f"q{q}_forward_d4_eq_d3_lambda_monomial_best", forward_hits, keep_best)
    print_hits(f"q{q}_reverse_d3_eq_d4_lambda_monomial_best", reverse_hits, keep_best)


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--degrees", default="2,3,4,5,6,7,8,9,10,11,12")
    parser.add_argument("--keep-best", type=int, default=10)
    args = parser.parse_args()

    degrees = parse_degrees(args.degrees)
    print("p27 lambda monomial Belyi recurrence probe")
    print("screen = d4(lambda) or d3(lambda) via S3-conjugated lambda -> lambda^m")
    print(f"degrees = {','.join(str(degree) for degree in degrees)}")
    for q in parse_ints(args.small_primes):
        run_field(q, degrees, args.keep_best)
    print("p27_lambda_monomial_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
