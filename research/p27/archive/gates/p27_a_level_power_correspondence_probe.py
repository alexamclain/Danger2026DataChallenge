#!/usr/bin/env python3
"""A-level projection of the hidden-X power correspondence screen.

The B-line power-map screen tests recurrences on the signed quotient

    B = 8X^2/(X^2 - 1)^2.

Since the selected tower also descends to A and A = B^2 - 2, this companion
probe asks whether the same hidden-X maps become useful only after forgetting
the sign of B.  A multivalued branch is accepted only when all source images
that land in the relevant domain have the same selected sign.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_a_level_prefix_descent_probe import collect_field_ax, parse_ints
from p27_a_line_character_support_probe import target_rows
from p27_b_line_belyi_orbit_probe import belyi_transforms
from p27_b_line_power_recurrence_probe import compose, make_power_map
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import roots_mod


@dataclass(frozen=True)
class ScoredCorrespondence:
    name: str
    polarity: int
    covered: int
    matches: int
    mixed: int
    domain_size: int
    branch_hits: int
    undefined_branches: int


def rows_to_signs(rows: list[tuple[int, int]]) -> dict[int, int]:
    # target_rows convention: 0 = +1, 1 = -1.
    return {A: (1 if bit == 0 else -1) for A, bit in rows}


def a_to_b_roots(A: int, q: int) -> list[int]:
    return roots_mod((A + 2) % q, q)


def score_correspondence(
    source: dict[int, int],
    target: dict[int, int],
    q: int,
    name: str,
    fn: Callable[[int, int], int | None],
) -> list[ScoredCorrespondence]:
    base: Counter = Counter()
    polarity_matches = Counter()
    for A, target_sign in target.items():
        signs: set[int] = set()
        roots = a_to_b_roots(A, q)
        if not roots:
            base["no_B_roots"] += 1
            continue
        for B in roots:
            image_B = fn(B, q)
            if image_B is None:
                base["undefined_branches"] += 1
                continue
            image_A = (image_B * image_B - 2) % q
            source_sign = source.get(image_A)
            if source_sign is None:
                continue
            base["branch_hits"] += 1
            signs.add(source_sign)
        if not signs:
            continue
        if len(signs) > 1:
            base["mixed"] += 1
            continue
        source_sign = next(iter(signs))
        base["covered"] += 1
        for polarity in (1, -1):
            if target_sign == polarity * source_sign:
                polarity_matches[polarity] += 1

    return [
        ScoredCorrespondence(
            name=name,
            polarity=polarity,
            covered=base["covered"],
            matches=polarity_matches[polarity],
            mixed=base["mixed"],
            domain_size=len(target),
            branch_hits=base["branch_hits"],
            undefined_branches=base["undefined_branches"],
        )
        for polarity in (1, -1)
    ]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_best(prefix: str, hits: list[ScoredCorrespondence], keep_best: int) -> None:
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
            -item.mixed,
        ),
        reverse=True,
    )[:keep_best]:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"mixed={hit.mixed} branch_hits={hit.branch_hits} "
            f"undefined_branches={hit.undefined_branches}"
        )


def run_field(q: int, powers: list[int], keep_best: int) -> None:
    ax_points, base = collect_field_ax(q)
    d3_rows, d3_stats = target_rows(ax_points, q, 3, 8)
    d4_rows, d4_stats = target_rows(ax_points, q, 4, 8)
    d3 = rows_to_signs(d3_rows)
    d4 = rows_to_signs(d4_rows)

    setup = Counter({f"base_{key}": value for key, value in base.items()})
    setup["q_mod_16"] = q % 16
    setup["chi_minus_one"] = legendre(-1, q)
    setup["chi_two"] = legendre(2, q)
    setup["d3_A_rows"] = len(d3)
    setup["d3_plus"] = d3_stats["plus_A"]
    setup["d3_minus"] = d3_stats["minus_A"]
    setup["d4_A_rows"] = len(d4)
    setup["d4_plus"] = d4_stats["plus_A"]
    setup["d4_minus"] = d4_stats["minus_A"]
    print_counter(f"q{q}_setup", setup)

    transforms = belyi_transforms()
    power_maps = [make_power_map(power) for power in powers]
    forward_hits: list[ScoredCorrespondence] = []
    reverse_hits: list[ScoredCorrespondence] = []
    stats: Counter = Counter()
    for left in transforms:
        for middle in power_maps:
            for right in transforms:
                name = f"{left.name} o {middle.name} o {right.name}"
                fn = lambda b, p, ll=left, mm=middle, rr=right: compose(ll, mm, rr, b, p)
                stats["correspondences_tested"] += 1
                forward = score_correspondence(d3, d4, q, name, fn)
                reverse = score_correspondence(d4, d3, q, name, fn)
                forward_hits.extend(forward)
                reverse_hits.extend(reverse)
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in forward):
                    stats["forward_exact"] += 1
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in reverse):
                    stats["reverse_exact"] += 1

    if forward_hits:
        best_forward = max(forward_hits, key=lambda hit: (hit.covered, hit.matches, -hit.mixed))
        stats["forward_best_covered"] = best_forward.covered
        stats["forward_best_matches"] = best_forward.matches
        stats["forward_best_mixed"] = best_forward.mixed
        stats["forward_best_coverage_x1000000"] = best_forward.covered * 1_000_000 // best_forward.domain_size
        stats["forward_best_match_x1000000"] = best_forward.matches * 1_000_000 // best_forward.domain_size
    if reverse_hits:
        best_reverse = max(reverse_hits, key=lambda hit: (hit.covered, hit.matches, -hit.mixed))
        stats["reverse_best_covered"] = best_reverse.covered
        stats["reverse_best_matches"] = best_reverse.matches
        stats["reverse_best_mixed"] = best_reverse.mixed
        stats["reverse_best_coverage_x1000000"] = best_reverse.covered * 1_000_000 // best_reverse.domain_size
        stats["reverse_best_match_x1000000"] = best_reverse.matches * 1_000_000 // best_reverse.domain_size

    print_counter(f"q{q}_a_power_correspondence_stats", stats)
    print_best(f"q{q}_forward_d4_eq_d3_a_power_best", forward_hits, keep_best)
    print_best(f"q{q}_reverse_d3_eq_d4_a_power_best", reverse_hits, keep_best)


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
    parser.add_argument("--keep-best", type=int, default=12)
    args = parser.parse_args()

    powers = parse_powers(args.powers)
    print("p27 A-level hidden-X power correspondence probe")
    print("screen = d4(A) or d3(A) via A=B^2-2 projection of Belyi-conjugated X -> X^m")
    print(f"powers = {','.join(str(power) for power in powers)}")
    for q in parse_ints(args.small_primes):
        run_field(q, powers, args.keep_best)
    print("p27_a_level_power_correspondence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
