#!/usr/bin/env python3
"""Materialization-oriented phase-word screen for the p27 B-line V4 phases.

The first phase-word probe used a local square root of H^2 = u + 2.  Since
alpha and beta both flip under H -> -H, a real telescoping law might require a
sheet convention carried by the selected x-coordinate.  On a selected row,

    H^2 = x + 2 + 1/x = (x + 1)^2 / x.

This probe orients H as

    H = (x + 1) / sqrt(x)

using the same deterministic square-root routine used by the local CPU
probes.  It then reruns the same pre-registered phase-word source screen with
raw-source denominators.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from p27_b_line_alpha_beta_phase_sequence_probe import (
    Phase,
    candidate_start,
    next_square_children,
    p27_oriented_candidates,
)
from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, inv, legendre, sqrt_mod
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates


@dataclass(frozen=True)
class PhasePath:
    phases: tuple[Phase, ...]


@dataclass(frozen=True)
class Observable:
    name: str
    last_gate: int
    value: Callable[[tuple[Phase, ...]], int | None]


def oriented_phase_record(B: int, x: int, p: int, gate: int) -> tuple[Phase | None, Counter]:
    stats: Counter = Counter()
    x %= p
    if x == 0:
        stats["x_zero"] += 1
        return None, stats
    sx = sqrt_mod(x, p)
    if sx is None:
        stats["x_sqrt_missing"] += 1
        return None, stats
    u = (x + inv(x, p)) % p
    H2 = (u + 2) % p
    H = (x + 1) * inv(sx, p) % p
    if H * H % p != H2:
        stats["H_orientation_fail"] += 1
        return None, stats

    R = sqrt_mod(H2 - 4, p)
    S = sqrt_mod(B * B + H2 - 4, p)
    if R is None:
        stats["R_missing"] += 1
        return None, stats
    if S is None:
        stats["S_missing"] += 1
        return None, stats
    alpha = legendre(H + R, p)
    beta = legendre(H + S, p)
    product = alpha * beta
    if product not in (-1, 1):
        stats["product_zero"] += 1
    return Phase(gate=gate, x=x, u=u, alpha=alpha, beta=beta, product=product), stats


def phase_at(phases: tuple[Phase, ...], gate: int) -> Phase | None:
    index = gate - 3
    if index < 0 or index >= len(phases):
        return None
    phase = phases[index]
    return phase if phase.gate == gate else None


def single_value(kind: str, gate: int) -> Callable[[tuple[Phase, ...]], int | None]:
    def value(phases: tuple[Phase, ...]) -> int | None:
        phase = phase_at(phases, gate)
        return None if phase is None else int(getattr(phase, kind))

    return value


def link_value(left: str, gate: int, right: str) -> Callable[[tuple[Phase, ...]], int | None]:
    def value(phases: tuple[Phase, ...]) -> int | None:
        p0 = phase_at(phases, gate)
        p1 = phase_at(phases, gate + 1)
        if p0 is None or p1 is None:
            return None
        return int(getattr(p0, left)) * int(getattr(p1, right))

    return value


def cumulative_value(kind: str, last_gate: int) -> Callable[[tuple[Phase, ...]], int | None]:
    def value(phases: tuple[Phase, ...]) -> int | None:
        out = 1
        for gate in range(3, last_gate + 1):
            phase = phase_at(phases, gate)
            if phase is None:
                return None
            out *= int(getattr(phase, kind))
        return out

    return value


def observables(max_gate: int) -> list[Observable]:
    out: list[Observable] = []
    for gate in range(3, max_gate + 1):
        out.append(Observable(f"oa{gate}", gate, single_value("alpha", gate)))
        out.append(Observable(f"ob{gate}", gate, single_value("beta", gate)))
    for gate in range(3, max_gate):
        out.append(Observable(f"oaa{gate}_{gate + 1}", gate + 1, link_value("alpha", gate, "alpha")))
        out.append(Observable(f"oab{gate}_{gate + 1}", gate + 1, link_value("alpha", gate, "beta")))
        out.append(Observable(f"oba{gate}_{gate + 1}", gate + 1, link_value("beta", gate, "alpha")))
        out.append(Observable(f"obb{gate}_{gate + 1}", gate + 1, link_value("beta", gate, "beta")))
    for gate in range(4, max_gate + 1):
        out.append(Observable(f"ocuma3_{gate}", gate, cumulative_value("alpha", gate)))
        out.append(Observable(f"ocumb3_{gate}", gate, cumulative_value("beta", gate)))
    return out


def collect_phase_paths(candidates: list[dict[str, int]], p: int, max_gate: int) -> tuple[list[PhasePath], Counter]:
    stats: Counter = Counter()
    paths: list[PhasePath] = []
    seen: set[tuple[int, int, int]] = set()

    for cand in dedupe_candidates(candidates):
        A = int(cand["A"]) % p
        x5 = int(cand["x5"]) % p
        B = source_b_plus(int(cand["X"]) % p, p)
        if B is None:
            stats["B_degenerate"] += 1
            continue
        key = (A, x5, B)
        if key in seen:
            stats["duplicate_A_x5_B"] += 1
            continue
        seen.add(key)

        starts, start_stats = candidate_start(A, x5, p)
        stats.update(start_stats)
        active: list[tuple[int, tuple[Phase, ...]]] = [(x, ()) for x in starts]
        for gate in range(3, max_gate + 1):
            if not active:
                break
            next_active: list[tuple[int, tuple[Phase, ...]]] = []
            for x, prior in active:
                phase, phase_stats = oriented_phase_record(B, x, p, gate)
                stats.update(phase_stats)
                if phase is None:
                    stats["phase_missing"] += 1
                    paths.append(PhasePath(prior))
                    continue
                phases = (*prior, phase)
                stats[f"gate{gate}_records"] += 1
                stats[f"gate{gate}_alpha_{phase.alpha}"] += 1
                stats[f"gate{gate}_beta_{phase.beta}"] += 1
                stats[f"gate{gate}_product_{phase.product}"] += 1
                if phase.alpha != 1:
                    stats[f"gate{gate}_alpha_not_plus"] += 1
                if phase.beta != phase.product:
                    stats[f"gate{gate}_beta_product_mismatch"] += 1
                children, child_stats = next_square_children(A, x, p)
                stats.update({f"gate{gate}_{key}": value for key, value in child_stats.items()})
                if phase.product == 1 and children:
                    for child in children:
                        next_active.append((child, phases))
                else:
                    if phase.product == 1 and not children:
                        stats[f"gate{gate}_product_plus_no_child"] += 1
                    if phase.product == -1 and children:
                        stats[f"gate{gate}_product_minus_has_child"] += len(children)
                    paths.append(PhasePath(phases))
            active = next_active
        for _x, phases in active:
            paths.append(PhasePath(phases))

    stats["unique_A_x5_B"] = len(seen)
    stats["phase_paths"] = len(paths)
    for path in paths:
        stats[f"path_len_{len(path.phases)}"] += 1
    return paths, stats


def survives_target(phases: tuple[Phase, ...], target_gate: int) -> bool:
    target_len = target_gate - 2
    return len(phases) >= target_len and all(phase.product == 1 for phase in phases[:target_len])


def score_observable(paths: list[PhasePath], obs: Observable, sign: int, target_gate: int, source_draws: int) -> Counter:
    stats: Counter = Counter()
    for path in paths:
        value = obs.value(path.phases)
        if value not in (-1, 1):
            continue
        target = survives_target(path.phases, target_gate)
        stats["domain"] += 1
        stats["domain_target"] += int(target)
        if value == sign:
            stats["selected"] += 1
            stats["selected_target"] += int(target)

    if stats["domain"]:
        stats["selected_rate_x1000000"] = stats["selected"] * 1_000_000 // stats["domain"]
        stats["baseline_target_rate_x1000000"] = stats["domain_target"] * 1_000_000 // stats["domain"]
    if stats["selected"]:
        stats["selected_target_rate_x1000000"] = stats["selected_target"] * 1_000_000 // stats["selected"]
    if source_draws:
        stats["baseline_target_per_source_x1000000000"] = stats["domain_target"] * 1_000_000_000 // source_draws
        stats["selected_target_per_source_x1000000000"] = stats["selected_target"] * 1_000_000_000 // source_draws
        stats["selected_per_source_x1000000000"] = stats["selected"] * 1_000_000_000 // source_draws
    baseline = stats["baseline_target_rate_x1000000"]
    selected_rate = stats["selected_target_rate_x1000000"]
    if baseline:
        stats["conditional_lift_x1000"] = selected_rate * 1000 // baseline
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def screen_label(
    label: str,
    candidates: list[dict[str, int]],
    p: int,
    max_gate: int,
    target_gate: int,
    source_draws: int,
    min_selected: int,
) -> None:
    paths, path_stats = collect_phase_paths(candidates, p, max_gate)
    print_counter(f"{label}_path_stats", path_stats)
    print(f"{label}_oriented_phase_word_table:")
    print(
        "  name sign domain selected domain_target selected_target "
        "baseline_rate selected_rate conditional_lift "
        "baseline_target_per_source selected_target_per_source selected_per_source"
    )
    rows: list[tuple[int, int, str, int, Counter]] = []
    for obs in observables(target_gate - 1):
        for sign in (-1, 1):
            stats = score_observable(paths, obs, sign, target_gate, source_draws)
            if stats["selected"] < min_selected or stats["domain_target"] == 0:
                continue
            rows.append((stats["conditional_lift_x1000"], stats["selected"], obs.name, sign, stats))

    for _lift, _selected, name, sign, stats in sorted(rows, reverse=True):
        print(
            f"  {name} {sign} "
            f"{stats['domain']} {stats['selected']} "
            f"{stats['domain_target']} {stats['selected_target']} "
            f"{stats['baseline_target_rate_x1000000'] / 1_000_000:.9f} "
            f"{stats['selected_target_rate_x1000000'] / 1_000_000:.9f} "
            f"{stats['conditional_lift_x1000'] / 1000:.3f} "
            f"{stats['baseline_target_per_source_x1000000000'] / 1_000_000_000:.9f} "
            f"{stats['selected_target_per_source_x1000000000'] / 1_000_000_000:.9f} "
            f"{stats['selected_per_source_x1000000000'] / 1_000_000_000:.9f}"
        )


def run_p27(label: str, target: int, seed: int, max_draws: int, max_gate: int, target_gate: int, min_selected: int) -> None:
    candidates, sample_stats = p27_oriented_candidates(target, seed, max_draws)
    print_counter(f"{label}_sample_stats", sample_stats)
    screen_label(label, candidates, P, max_gate, target_gate, sample_stats["sample_x_draws"], min_selected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p27-target", type=int, default=6000)
    parser.add_argument("--p27-heldout-target", type=int, default=6000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=2000000)
    parser.add_argument("--max-gate", type=int, default=9)
    parser.add_argument("--target-gate", type=int, default=8)
    parser.add_argument("--min-selected", type=int, default=500)
    parser.add_argument("--small-primes", default="")
    args = parser.parse_args()

    print("p27 B-line materialization-oriented phase-word probe")
    print("orientation = H = (x + 1) / sqrt(x)")
    print(f"max_gate = {args.max_gate}")
    print(f"target_gate = {args.target_gate}")
    print(f"min_selected = {args.min_selected}")

    if args.p27_target:
        run_p27("p27_train", args.p27_target, args.seed, args.max_draws, args.max_gate, args.target_gate, args.min_selected)
    if args.p27_heldout_target:
        run_p27(
            "p27_heldout",
            args.p27_heldout_target,
            args.heldout_seed,
            args.max_draws,
            args.max_gate,
            args.target_gate,
            args.min_selected,
        )
    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print_counter(f"q{q}_enum_stats", Counter({f"enum_{key}": value for key, value in enum_stats.items()}))
        screen_label(f"q{q}", candidates, q, args.max_gate, args.target_gate, 0, args.min_selected)

    print("p27_b_line_oriented_phase_word_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
