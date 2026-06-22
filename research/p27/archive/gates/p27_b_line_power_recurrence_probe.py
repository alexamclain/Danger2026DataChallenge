#!/usr/bin/env python3
"""Power-map recurrence screen for the p27 B-line Kummer sequence.

The B-line coordinate is

    B = 8*X^2/(X^2 - 1)^2 = 8/(X - 1/X)^2.

This gives a small theorem-shaped family of self maps induced by X -> X^m.
Unlike another low-degree coefficient scan, these maps are forced by the
hidden X-line behind the B quotient.  The probe tests whether d4(B) is the
pullback of d3 along one of these maps, optionally conjugated by the visible
Belyi S3 symmetries of {0, -2, infinity}.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_b_line_branch_support_probe import core_b_values, legal_b_maps, parse_ints
from p27_b_line_belyi_orbit_probe import Transform, belyi_transforms
from p27_label2_alpha_branch_recurrence_probe import legendre


@dataclass(frozen=True)
class PowerMap:
    name: str
    fn: Callable[[int, int], int | None]


@dataclass(frozen=True)
class ScoredMap:
    name: str
    polarity: int
    covered: int
    matches: int
    domain_size: int
    legal_images: int
    core_images: int
    undefined: int


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def power_denominator_u(m: int, u: int, p: int) -> int:
    """Return D_m^2 as U * Q_m(U), where U=(X-X^-1)^2.

    Supported m are intentionally small.  They cover the nearest power maps
    without turning this into an unfocused correspondence search.
    """

    u %= p
    if m == 2:
        return u * (u + 4)
    if m == 3:
        return u * pow(u + 3, 2, p)
    if m == 4:
        return u * (u + 4) * pow(u + 2, 2, p)
    if m == 5:
        return u * pow((u * u + 5 * u + 5) % p, 2, p)
    if m == 6:
        return u * (u + 4) * pow((u * u + 4 * u + 3) % p, 2, p)
    raise ValueError(f"unsupported power map m={m}")


def x_power_map(m: int, b: int, p: int) -> int | None:
    binv = inv(b, p)
    if binv is None:
        return None
    u = 8 * binv % p
    den = power_denominator_u(m, u, p) % p
    den_inv = inv(den, p)
    if den_inv is None:
        return None
    return 8 * den_inv % p


def make_power_map(m: int) -> PowerMap:
    return PowerMap(f"X^{m}", lambda b, p, mm=m: x_power_map(mm, b, p))


def compose(
    left: Transform,
    middle: PowerMap,
    right: Transform,
    b: int,
    p: int,
) -> int | None:
    first = right.fn(b, p)
    if first is None:
        return None
    second = middle.fn(first, p)
    if second is None:
        return None
    return left.fn(second, p)


def score_relation(
    source: dict[int, int],
    target: dict[int, int],
    core: set[int],
    legal: set[int],
    q: int,
    name: str,
    fn: Callable[[int, int], int | None],
) -> list[ScoredMap]:
    base: Counter = Counter()
    polarity_stats = {1: Counter(), -1: Counter()}
    for b, target_sign in target.items():
        image = fn(b, q)
        if image is None:
            base["undefined"] += 1
            continue
        image %= q
        if image in core:
            base["core_images"] += 1
        if image in legal:
            base["legal_images"] += 1
        source_sign = source.get(image)
        if source_sign is None:
            continue
        base["covered"] += 1
        for polarity in (1, -1):
            if target_sign == polarity * source_sign:
                polarity_stats[polarity]["matches"] += 1

    out = []
    for polarity in (1, -1):
        out.append(
            ScoredMap(
                name=name,
                polarity=polarity,
                covered=base["covered"],
                matches=polarity_stats[polarity]["matches"],
                domain_size=len(target),
                legal_images=base["legal_images"],
                core_images=base["core_images"],
                undefined=base["undefined"],
            )
        )
    return out


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_best(prefix: str, hits: list[ScoredMap], keep_best: int) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
        return
    for hit in sorted(
        hits,
        key=lambda item: (item.matches == item.covered == item.domain_size, item.covered, item.matches),
        reverse=True,
    )[:keep_best]:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"core_images={hit.core_images} legal_images={hit.legal_images} "
            f"undefined={hit.undefined}"
        )


def run_field(q: int, powers: list[int], keep_best: int) -> None:
    d3, d4, setup = legal_b_maps(q)
    core = core_b_values(q)
    legal = set(d3)
    transforms = belyi_transforms()
    power_maps = [make_power_map(m) for m in powers]

    setup_stats = Counter({f"setup_{key}": value for key, value in setup.items()})
    setup_stats["q_mod_16"] = q % 16
    setup_stats["chi_minus_one"] = legendre(-1, q)
    setup_stats["chi_two"] = legendre(2, q)
    setup_stats["core_B"] = len(core)
    setup_stats["legal_B"] = len(legal)
    setup_stats["d3_B_rows"] = len(d3)
    setup_stats["d4_B_rows"] = len(d4)
    print_counter(f"q{q}_setup", setup_stats)

    forward_hits: list[ScoredMap] = []
    reverse_hits: list[ScoredMap] = []
    stats: Counter = Counter()
    for left in transforms:
        for middle in power_maps:
            for right in transforms:
                name = f"{left.name} o {middle.name} o {right.name}"
                fn = lambda b, p, ll=left, mm=middle, rr=right: compose(ll, mm, rr, b, p)
                stats["maps_tested"] += 1
                forward = score_relation(d3, d4, core, legal, q, name, fn)
                reverse = score_relation(d4, d3, core, legal, q, name, fn)
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
        stats["forward_best_match_x1000000"] = (
            best_forward.matches * 1_000_000 // best_forward.domain_size
            if best_forward.domain_size
            else 0
        )
        stats["forward_best_coverage_x1000000"] = (
            best_forward.covered * 1_000_000 // best_forward.domain_size
            if best_forward.domain_size
            else 0
        )
    if reverse_hits:
        best_reverse = max(reverse_hits, key=lambda hit: (hit.covered, hit.matches))
        stats["reverse_best_covered"] = best_reverse.covered
        stats["reverse_best_matches"] = best_reverse.matches
        stats["reverse_best_match_x1000000"] = (
            best_reverse.matches * 1_000_000 // best_reverse.domain_size
            if best_reverse.domain_size
            else 0
        )
        stats["reverse_best_coverage_x1000000"] = (
            best_reverse.covered * 1_000_000 // best_reverse.domain_size
            if best_reverse.domain_size
            else 0
        )

    print_counter(f"q{q}_power_recurrence_stats", stats)
    print_best(f"q{q}_forward_d4_eq_d3_power_best", forward_hits, keep_best)
    print_best(f"q{q}_reverse_d3_eq_d4_power_best", reverse_hits, keep_best)


def parse_powers(raw: str) -> list[int]:
    powers = [int(part) for part in raw.split(",") if part.strip()]
    unsupported = [power for power in powers if power not in {2, 3, 4, 5, 6}]
    if unsupported:
        raise ValueError(f"unsupported powers: {unsupported}")
    return powers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--powers", default="2,3,4,5,6")
    parser.add_argument("--keep-best", type=int, default=10)
    args = parser.parse_args()

    powers = parse_powers(args.powers)
    print("p27 B-line power recurrence probe")
    print("screen = d4(B) or d3(B) via Belyi-conjugated X -> X^m maps")
    print(f"powers = {','.join(str(power) for power in powers)}")
    for q in parse_ints(args.small_primes):
        run_field(q, powers, args.keep_best)
    print("p27_b_line_power_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
