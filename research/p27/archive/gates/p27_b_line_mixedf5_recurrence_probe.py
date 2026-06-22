#!/usr/bin/env python3
"""Fixture-based recurrence screen for the mixed-f5 B-line fields.

The mixed-f5 guard shows that chi(W+2)=f5(B) exactly on selected f4-plus B
rows.  This probe asks whether that repeated class is already a visible
recurrence from the previous conditional class:

    f5(B) = +/- f4(phi(B)).

It tests two targeted map families:
  * all full-coverage PGL2 maps P1_B -> P1_B,
  * Belyi-conjugated hidden-X power maps X -> X^m, m=2..6.

The input is the frozen mixed-f5 Kummer fixture, so this is a reproducible
class-comparison falsifier rather than a fresh enumeration.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Any

from p27_b_line_belyi_orbit_probe import belyi_transforms
from p27_b_line_pgl2_recurrence_probe import PGL2Hit, eval_pgl2, pgl2_from_three
from p27_b_line_power_recurrence_probe import ScoredMap, compose, make_power_map, parse_powers, score_relation
from p27_kline_reverse_z_relation_probe import parse_ints


DEFAULT_KUMMER = Path("research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_mixedf5_20260622.json")


def sign_to_int(label: str) -> int:
    if label == "plus":
        return 1
    if label == "minus":
        return -1
    raise ValueError(label)


def load_field(packet: dict[str, Any], q: int) -> dict[str, Any]:
    for fixture in packet["fixtures"]:
        if int(fixture["field"]) == q:
            return fixture
    raise KeyError(q)


def family_signs(field: dict[str, Any], name: str) -> dict[int, int]:
    for family in field["families"]:
        if family["name"] == name:
            out: dict[int, int] = {}
            for row in family["rows"]:
                label = str(row["sign"])
                if label in ("plus", "minus"):
                    out[int(row["B"])] = sign_to_int(label)
            return out
    raise KeyError(name)


def score_pgl2(
    q: int,
    source: dict[int, int],
    target: dict[int, int],
    phi,
    polarity: int,
) -> tuple[int, int, int]:
    covered = 0
    matches = 0
    poles = 0
    for b, target_sign in target.items():
        image = eval_pgl2(phi, b, q)
        if image is None:
            poles += 1
            continue
        source_sign = source.get(image)
        if source_sign is None:
            continue
        covered += 1
        if target_sign == polarity * source_sign:
            matches += 1
    return covered, matches, poles


def find_pgl2(q: int, source: dict[int, int], target: dict[int, int], keep_best: int) -> tuple[Counter, list[PGL2Hit], list[PGL2Hit]]:
    stats: Counter = Counter()
    stats["source_rows"] = len(source)
    stats["target_rows"] = len(target)
    if len(source) < 3 or len(target) < 3:
        return stats, [], []

    xs = tuple(sorted(target)[:3])
    source_values = tuple(sorted(source))
    seen = set()
    exact: list[PGL2Hit] = []
    best: list[PGL2Hit] = []

    for ys in permutations(source_values, 3):
        phi = pgl2_from_three(xs, ys, q)
        if phi is None or phi in seen:
            continue
        seen.add(phi)
        stats["pgl2_maps_tested"] += 1
        for polarity in (1, -1):
            covered, matches, poles = score_pgl2(q, source, target, phi, polarity)
            stats["candidate_poles"] += poles
            hit = PGL2Hit(phi=phi, polarity=polarity, covered=covered, matches=matches)
            if covered == len(target) and matches == len(target):
                exact.append(hit)
            best.append(hit)

    best.sort(key=lambda hit: (hit.matches == hit.covered == len(target), hit.covered, hit.matches), reverse=True)
    stats["distinct_pgl2_maps"] = len(seen)
    stats["exact_pgl2_recurrences"] = len(exact)
    if best:
        stats["best_covered"] = best[0].covered
        stats["best_matches"] = best[0].matches
        stats["best_match_x1000000"] = best[0].matches * 1_000_000 // len(target)
        stats["best_coverage_x1000000"] = best[0].covered * 1_000_000 // len(target)
    return stats, exact[:keep_best], best[:keep_best]


def find_power_maps(
    q: int,
    source: dict[int, int],
    target: dict[int, int],
    powers: list[int],
    keep_best: int,
) -> tuple[Counter, list[ScoredMap], list[ScoredMap]]:
    transforms = belyi_transforms()
    power_maps = [make_power_map(m) for m in powers]
    stats: Counter = Counter()
    forward_hits: list[ScoredMap] = []
    reverse_hits: list[ScoredMap] = []
    source_domain = set(source)
    target_domain = set(target)
    both_domain = source_domain | target_domain

    for left in transforms:
        for middle in power_maps:
            for right in transforms:
                name = f"{left.name} o {middle.name} o {right.name}"
                fn = lambda b, p, ll=left, mm=middle, rr=right: compose(ll, mm, rr, b, p)
                stats["maps_tested"] += 1
                forward = score_relation(source, target, both_domain, source_domain, q, name, fn)
                reverse = score_relation(target, source, both_domain, target_domain, q, name, fn)
                forward_hits.extend(forward)
                reverse_hits.extend(reverse)
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in forward):
                    stats["forward_exact"] += 1
                if any(hit.covered == hit.domain_size and hit.matches == hit.domain_size for hit in reverse):
                    stats["reverse_exact"] += 1

    forward_hits.sort(
        key=lambda hit: (hit.matches == hit.covered == hit.domain_size, hit.covered, hit.matches),
        reverse=True,
    )
    reverse_hits.sort(
        key=lambda hit: (hit.matches == hit.covered == hit.domain_size, hit.covered, hit.matches),
        reverse=True,
    )
    if forward_hits:
        hit = forward_hits[0]
        stats["forward_best_covered"] = hit.covered
        stats["forward_best_matches"] = hit.matches
        stats["forward_best_coverage_x1000000"] = hit.covered * 1_000_000 // hit.domain_size
        stats["forward_best_match_x1000000"] = hit.matches * 1_000_000 // hit.domain_size
    if reverse_hits:
        hit = reverse_hits[0]
        stats["reverse_best_covered"] = hit.covered
        stats["reverse_best_matches"] = hit.matches
        stats["reverse_best_coverage_x1000000"] = hit.covered * 1_000_000 // hit.domain_size
        stats["reverse_best_match_x1000000"] = hit.matches * 1_000_000 // hit.domain_size
    return stats, forward_hits[:keep_best], reverse_hits[:keep_best]


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_pgl2_hits(prefix: str, hits: list[PGL2Hit]) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
        return
    for hit in hits:
        phi = hit.phi
        print(
            "  "
            f"phi=({phi.a}*B+{phi.b})/({phi.c}*B+{phi.d}) "
            f"polarity={hit.polarity} covered={hit.covered} matches={hit.matches}"
        )


def print_power_hits(prefix: str, hits: list[ScoredMap]) -> None:
    print(f"{prefix}:")
    if not hits:
        print("  none")
        return
    for hit in hits:
        print(
            "  "
            f"{hit.name} polarity={hit.polarity} "
            f"covered={hit.covered}/{hit.domain_size} matches={hit.matches} "
            f"core_images={hit.core_images} legal_images={hit.legal_images} "
            f"undefined={hit.undefined}"
        )


def run_field(packet: dict[str, Any], q: int, powers: list[int], keep_best: int) -> None:
    field = load_field(packet, q)
    f4 = family_signs(field, "f4_conditional")
    f5 = family_signs(field, "f5_conditional")
    setup: Counter = Counter()
    setup["f4_rows"] = len(f4)
    setup["f4_plus"] = sum(1 for value in f4.values() if value == 1)
    setup["f4_minus"] = sum(1 for value in f4.values() if value == -1)
    setup["f5_rows"] = len(f5)
    setup["f5_plus"] = sum(1 for value in f5.values() if value == 1)
    setup["f5_minus"] = sum(1 for value in f5.values() if value == -1)
    print_counter(f"q{q}_setup", setup)

    pgl2_stats, exact, best = find_pgl2(q, f4, f5, keep_best)
    print_counter(f"q{q}_f4_to_f5_pgl2_stats", pgl2_stats)
    print_pgl2_hits(f"q{q}_f4_to_f5_exact_pgl2", exact)
    print_pgl2_hits(f"q{q}_f4_to_f5_best_pgl2", best)

    power_stats, forward, reverse = find_power_maps(q, f4, f5, powers, keep_best)
    print_counter(f"q{q}_f4_f5_power_stats", power_stats)
    print_power_hits(f"q{q}_forward_f5_eq_f4_power_best", forward)
    print_power_hits(f"q{q}_reverse_f4_eq_f5_power_best", reverse)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="4999,5783,6007,6247")
    parser.add_argument("--kummer-fixture", type=Path, default=DEFAULT_KUMMER)
    parser.add_argument("--powers", default="2,3,4,5,6")
    parser.add_argument("--keep-best", type=int, default=8)
    args = parser.parse_args()

    packet = json.loads(args.kummer_fixture.read_text())
    powers = parse_powers(args.powers)
    print("p27 B-line mixed-f5 recurrence probe")
    print("screen = f5(B) = +/- f4(phi(B)) on mixed-f5 guard fields")
    print("families = full-coverage PGL2; Belyi-conjugated hidden-X power maps")
    print(f"kummer_fixture = {args.kummer_fixture}")
    print(f"powers = {','.join(str(power) for power in powers)}")
    for q in parse_ints(args.small_primes):
        run_field(packet, q, powers, args.keep_best)
    print("p27_b_line_mixedf5_recurrence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
