#!/usr/bin/env python3
"""Phase-sequence screen for the p27 B-line V4 gamma factorization.

The V4 factorization writes the next selected bit as

    f_{j+1} = alpha_j * beta_j
    alpha_j = chi(H_j + R_j),  R_j^2 = H_j^2 - 4
    beta_j  = chi(H_j + S_j),  S_j^2 = B^2 + H_j^2 - 4

where H_j^2 = u_j + 2 and u_j=x_j+1/x_j.  Since alpha and beta both flip
under H -> -H, neither is a canonical bucket alone.  This probe asks the next
question: do the phases recur or telescope across successive selected gates?
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Optional

from p27_b_source_descent_probe import source_b_plus
from p27_kline_reverse_z_relation_probe import dedupe_candidates, p27_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import P, halve_all, inv, legendre, sqrt_mod
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates


@dataclass(frozen=True)
class Phase:
    gate: int
    x: int
    u: int
    alpha: int
    beta: int
    product: int


@dataclass(frozen=True)
class PathState:
    x: int
    last_phase: Optional[Phase]
    length: int


def phase_record(B: int, x: int, p: int, gate: int) -> tuple[Optional[Phase], Counter]:
    stats: Counter = Counter()
    if x % p == 0:
        stats["x_zero"] += 1
        return None, stats
    u = (x + inv(x, p)) % p
    H2 = (u + 2) % p
    H = sqrt_mod(H2, p)
    R = sqrt_mod(H2 - 4, p)
    S = sqrt_mod(B * B + H2 - 4, p)
    if H is None:
        stats["H_missing"] += 1
        return None, stats
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
    return Phase(gate=gate, x=x % p, u=u, alpha=alpha, beta=beta, product=product), stats


def next_square_children(A: int, x: int, p: int) -> tuple[list[int], Counter]:
    stats: Counter = Counter()
    d, branches = halve_all(A, x, p)
    stats[f"next_d_{d}"] += 1
    children = sorted({branch % p for branch in branches if legendre(branch, p) == 1})
    stats[f"square_children_{len(children)}"] += 1
    return children, stats


def candidate_start(A: int, x5: int, p: int) -> tuple[list[int], Counter]:
    stats: Counter = Counter()
    d2, x6s = halve_all(A, x5, p)
    stats[f"d2_{d2}"] += 1
    if d2 != 1:
        return [], stats
    starts = sorted({x6 % p for x6 in x6s if legendre(x6, p) == 1})
    stats[f"start_square_x6_{len(starts)}"] += 1
    return starts, stats


def walk_candidate(A: int, B: int, x5: int, p: int, max_gate: int) -> tuple[list[Phase], list[tuple[Phase, Phase]], Counter]:
    stats: Counter = Counter()
    starts, start_stats = candidate_start(A, x5, p)
    stats.update(start_stats)
    active = [PathState(x=x, last_phase=None, length=0) for x in starts]
    phases_out: list[Phase] = []
    links_out: list[tuple[Phase, Phase]] = []

    for gate in range(3, max_gate):
        if not active:
            break
        next_active: list[PathState] = []
        for state in active:
            phase, phase_stats = phase_record(B, state.x, p, gate)
            stats.update(phase_stats)
            if phase is None:
                stats["phase_missing"] += 1
                stats[f"path_len_{state.length}"] += 1
                continue
            phases_out.append(phase)
            if state.last_phase is not None:
                links_out.append((state.last_phase, phase))
            length = state.length + 1
            stats[f"gate{gate}_phase_records"] += 1
            stats[f"gate{gate}_product_{phase.product}"] += 1
            children, child_stats = next_square_children(A, state.x, p)
            stats.update({f"gate{gate}_{key}": value for key, value in child_stats.items()})
            if phase.product == 1:
                if not children:
                    stats[f"gate{gate}_product_plus_no_child"] += 1
                    stats[f"path_len_{length}"] += 1
                for child in children:
                    next_active.append(PathState(x=child, last_phase=phase, length=length))
            else:
                if children:
                    stats[f"gate{gate}_product_minus_has_child"] += len(children)
                stats[f"path_len_{length}"] += 1
        active = next_active

    for state in active:
        stats[f"path_len_{state.length}"] += 1
    return phases_out, links_out, stats


def candidates_to_phase_paths(
    candidates: list[dict[str, int]],
    p: int,
    max_gate: int,
) -> tuple[list[Phase], list[tuple[Phase, Phase]], Counter]:
    stats: Counter = Counter()
    phases: list[Phase] = []
    links: list[tuple[Phase, Phase]] = []
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
        cand_phases, cand_links, cand_stats = walk_candidate(A, B, x5, p, max_gate)
        stats.update(cand_stats)
        phases.extend(cand_phases)
        links.extend(cand_links)
    stats["unique_A_x5_B"] = len(seen)
    stats["phase_records"] = len(phases)
    stats["phase_links"] = len(links)
    return phases, links, stats


def p27_oriented_candidates(target: int, seed: int, max_draws: int) -> tuple[list[dict[str, int]], Counter]:
    return p27_candidates(target, seed, max_draws)


def phase_summary(phases: list[Phase], links: list[tuple[Phase, Phase]], walk_stats: Counter, max_gate: int) -> Counter:
    stats: Counter = Counter()
    stats["phase_records"] = len(phases)
    stats["phase_links"] = len(links)
    for key, value in walk_stats.items():
        if str(key).startswith("path_len_"):
            stats[key] = value
    for phase in phases:
        stats[f"gate{phase.gate}_alpha_{phase.alpha}"] += 1
        stats[f"gate{phase.gate}_beta_{phase.beta}"] += 1
        stats[f"gate{phase.gate}_product_{phase.product}"] += 1
    for prev, curr in links:
        key = f"gate{prev.gate}_to_{curr.gate}"
        state = prev.alpha  # On a continued path prev.product=+1, so alpha=beta.
        stats[f"{key}_pairs"] += 1
        stats[f"{key}_state_{state}_target_{curr.product}"] += 1
        stats[f"{key}_aa_{prev.alpha * curr.alpha}"] += 1
        stats[f"{key}_ab_{prev.alpha * curr.beta}"] += 1
        stats[f"{key}_ba_{prev.beta * curr.alpha}"] += 1
        stats[f"{key}_bb_{prev.beta * curr.beta}"] += 1

    for gate in range(3, max_gate):
        plus = stats[f"gate{gate}_product_1"]
        minus = stats[f"gate{gate}_product_-1"]
        total = plus + minus
        if total:
            stats[f"gate{gate}_product_plus_rate_x1000000"] = plus * 1_000_000 // total
    for gate in range(3, max_gate - 1):
        key = f"gate{gate}_to_{gate + 1}"
        for state in (-1, 1):
            plus = stats[f"{key}_state_{state}_target_1"]
            minus = stats[f"{key}_state_{state}_target_-1"]
            total = plus + minus
            if total:
                stats[f"{key}_state_{state}_next_plus_rate_x1000000"] = plus * 1_000_000 // total
        pairs = stats[f"{key}_pairs"]
        if pairs:
            for label in ("aa", "ab", "ba", "bb"):
                plus = stats[f"{key}_{label}_1"]
                stats[f"{key}_{label}_plus_rate_x1000000"] = plus * 1_000_000 // pairs
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_transition_table(prefix: str, stats: Counter, max_gate: int) -> None:
    print(f"{prefix}_transition_table:")
    print("  from_gate state_minus_next_plus state_plus_next_plus aa_plus ab_plus ba_plus bb_plus pairs")
    for gate in range(3, max_gate - 1):
        key = f"gate{gate}_to_{gate + 1}"
        pairs = stats[f"{key}_pairs"]
        if not pairs:
            continue
        print(
            f"  {gate} "
            f"{stats.get(f'{key}_state_-1_next_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{stats.get(f'{key}_state_1_next_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{stats.get(f'{key}_aa_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{stats.get(f'{key}_ab_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{stats.get(f'{key}_ba_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{stats.get(f'{key}_bb_plus_rate_x1000000', 0) / 1_000_000:.9f} "
            f"{pairs}"
        )


def run_label(label: str, candidates: list[dict[str, int]], p: int, max_gate: int, source_draws: int = 0) -> None:
    phases, links, walk_stats = candidates_to_phase_paths(candidates, p, max_gate)
    summary = phase_summary(phases, links, walk_stats, max_gate)
    if source_draws:
        summary["source_draws"] = source_draws
        for gate in range(3, max_gate):
            total = summary[f"gate{gate}_product_1"] + summary[f"gate{gate}_product_-1"]
            if total:
                summary[f"gate{gate}_phase_records_per_source_x1000000"] = total * 1_000_000 // source_draws
    print_counter(f"{label}_walk_stats", walk_stats)
    print_counter(f"{label}_phase_stats", summary)
    print_transition_table(label, summary, max_gate)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--p27-target", type=int, default=3000)
    parser.add_argument("--p27-heldout-target", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260621)
    parser.add_argument("--heldout-seed", type=int, default=20260622)
    parser.add_argument("--max-draws", type=int, default=1000000)
    parser.add_argument("--max-gate", type=int, default=8)
    args = parser.parse_args()

    print("p27 B-line alpha/beta phase sequence probe")
    print("question = do V4 phases recur or telescope across selected gates?")
    print(f"max_gate = {args.max_gate}")

    if args.p27_target:
        candidates, sample_stats = p27_oriented_candidates(args.p27_target, args.seed, args.max_draws)
        print_counter("p27_train_sample_stats", sample_stats)
        run_label("p27_train", candidates, P, args.max_gate, sample_stats["sample_x_draws"])

    if args.p27_heldout_target:
        candidates, sample_stats = p27_oriented_candidates(args.p27_heldout_target, args.heldout_seed, args.max_draws)
        print_counter("p27_heldout_sample_stats", sample_stats)
        run_label("p27_heldout", candidates, P, args.max_gate, sample_stats["sample_x_draws"])

    for q in parse_ints(args.small_primes):
        candidates, enum_stats = enumerate_small_prime_candidates(q)
        print_counter(f"q{q}_enum_stats", Counter({f"enum_{key}": value for key, value in enum_stats.items()}))
        run_label(f"q{q}", candidates, q, args.max_gate)

    print("p27_b_line_alpha_beta_phase_sequence_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
