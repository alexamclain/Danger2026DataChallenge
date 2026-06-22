#!/usr/bin/env python3
"""Branch support screen on the p27 B-line.

The B-source descent probe shows that the d3 and d4 bits descend to Bplus on
the legal source.  This probe asks whether those descended bits are low-degree
Kummer characters on P1_B.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations

from p27_b_source_descent_probe import row_core_ok, source_b_plus
from p27_kline_base_param_sampler_probe import enumerate_param_rows
from p27_kline_reverse_z_relation_probe import dedupe_candidates, parse_ints
from p27_label2_alpha_branch_recurrence_probe import halve_all, legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import candidate_bits, normalize


def popcount(x: int) -> int:
    return bin(x).count("1")


def legal_b_maps(q: int) -> tuple[dict[int, int], dict[int, int], Counter]:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    by_b: defaultdict[int, list[object]] = defaultdict(list)
    stats: Counter = Counter({f"enum_{key}": value for key, value in enum_stats.items()})
    for cand in dedupe_candidates(candidates):
        A = int(cand["A"]) % q
        x5 = int(cand["x5"]) % q
        d2, _ = halve_all(A, x5, q)
        if d2 != 1:
            stats["d2_minus"] += 1
            continue
        B = source_b_plus(int(cand["X"]) % q, q)
        if B is None:
            stats["b_degenerate"] += 1
            continue
        by_b[B].append(candidate_bits(cand, q))

    d3: dict[int, int] = {}
    d4: dict[int, int] = {}
    for B, bits in by_b.items():
        d3_value = normalize(bit.d3 for bit in bits)
        if d3_value in (-1, 1):
            d3[B] = d3_value
        elif d3_value == 0:
            stats["d3_mixed_on_B"] += 1
        if d3_value == 1:
            d4_value = normalize(bit.d4 for bit in bits)
            if d4_value in (-1, 1):
                d4[B] = d4_value
            elif d4_value == 0:
                stats["d4_mixed_on_B"] += 1

    stats["legal_B"] = len(by_b)
    stats["d3_labeled_B"] = len(d3)
    stats["d4_labeled_B"] = len(d4)
    return d3, d4, stats


def core_b_values(q: int) -> set[int]:
    out: set[int] = set()
    for row in enumerate_param_rows(q):
        if row.branch == 1 and row_core_ok(row, q):
            out.add(row.B)
    return out


def mask_for_rows(rows: list[tuple[int, int]]) -> int:
    mask = 0
    for index, (_B, bit) in enumerate(rows):
        if bit:
            mask |= 1 << index
    return mask


def factor_columns(q: int, rows: list[tuple[int, int]]) -> list[tuple[int, int]]:
    domain = {B for B, _bit in rows}
    cols: list[tuple[int, int]] = []
    for a in range(q):
        if a in domain:
            continue
        mask = 0
        for index, (B, _bit) in enumerate(rows):
            chi = legendre(B - a, q)
            if chi == -1:
                mask |= 1 << index
        cols.append((a, mask))
    return cols


def exact_linear_factor_search(q: int, rows: list[tuple[int, int]], max_weight: int) -> tuple[Counter, tuple[int, tuple[int, ...], int] | None]:
    stats: Counter = Counter()
    n = len(rows)
    target = mask_for_rows(rows)
    full = (1 << n) - 1
    stats["rows"] = n
    stats["plus_rows"] = sum(1 for _B, bit in rows if bit == 0)
    stats["minus_rows"] = sum(1 for _B, bit in rows if bit == 1)
    stats["target_weight"] = popcount(target)
    cols = factor_columns(q, rows)
    stats["candidate_linear_factors"] = len(cols)

    for a, mask in cols:
        if mask == target:
            return stats, (1, (a,), 1)
        if (mask ^ full) == target:
            return stats, (1, (a,), -1)
    if max_weight <= 1:
        return stats, None

    pair: dict[int, tuple[int, int]] = {}
    for i, (a, mask_a) in enumerate(cols):
        for b, mask_b in cols[i + 1 :]:
            value = mask_a ^ mask_b
            pair.setdefault(value, (a, b))
    stats["pair_xors"] = len(pair)

    for value, factors in pair.items():
        if value == target:
            return stats, (2, factors, 1)
        if (value ^ full) == target:
            return stats, (2, factors, -1)
    if max_weight <= 2:
        return stats, None

    for a, mask in cols:
        need = mask ^ target
        if need in pair:
            return stats, (3, (a, *pair[need]), 1)
        need = mask ^ (target ^ full)
        if need in pair:
            return stats, (3, (a, *pair[need]), -1)
    if max_weight <= 3:
        return stats, None

    for value, factors in pair.items():
        need = value ^ target
        if need in pair:
            return stats, (4, (*factors, *pair[need]), 1)
        need = value ^ (target ^ full)
        if need in pair:
            return stats, (4, (*factors, *pair[need]), -1)
    return stats, None


def irreducible_quadratic_plus_linear_search(
    q: int, rows: list[tuple[int, int]], max_linear: int
) -> tuple[Counter, tuple[int, int, tuple[int, ...], int] | None]:
    """Search q(B) times up to max_linear rational factors.

    q(B) ranges over monic irreducible quadratics B^2 + uB + v.  This tests
    branch support of total degree up to 2 + max_linear without enumerating
    pairs of irreducible quadratics.
    """

    stats: Counter = Counter()
    n = len(rows)
    target = mask_for_rows(rows)
    full = (1 << n) - 1
    domain = [B for B, _bit in rows]
    lin = factor_columns(q, rows)
    lin_map = {mask: (a,) for a, mask in lin}
    stats["linear_factors"] = len(lin)

    pair: dict[int, tuple[int, int]] = {}
    if max_linear >= 2:
        for i, (a, mask_a) in enumerate(lin):
            for b, mask_b in lin[i + 1 :]:
                pair.setdefault(mask_a ^ mask_b, (a, b))
        stats["linear_pair_xors"] = len(pair)

    for u in range(q):
        for v in range(q):
            disc = (u * u - 4 * v) % q
            if legendre(disc, q) != -1:
                continue
            mask = 0
            for index, B in enumerate(domain):
                value = (B * B + u * B + v) % q
                if value == 0:
                    stats["quadratic_zero_skip"] += 1
                    break
                if legendre(value, q) == -1:
                    mask |= 1 << index
            else:
                stats["irreducible_quadratics_tested"] += 1
                for polarity, desired in [(1, target), (-1, target ^ full)]:
                    if mask == desired:
                        return stats, (u, v, (), polarity)
                    if max_linear >= 1:
                        need = mask ^ desired
                        if need in lin_map:
                            return stats, (u, v, lin_map[need], polarity)
                    if max_linear >= 2:
                        need = mask ^ desired
                        if need in pair:
                            return stats, (u, v, pair[need], polarity)
    return stats, None


def squareclass_table(q: int) -> list[int]:
    chars = [-1] * q
    chars[0] = 0
    for a in range(1, q):
        chars[a * a % q] = 1
    return chars


def irreducible_quadratic_pair_search(
    q: int, rows: list[tuple[int, int]]
) -> tuple[Counter, tuple[tuple[int, int], tuple[int, int], int] | None]:
    """Search products of two monic irreducible quadratics on P1_B.

    This is the missing structured degree-4 Kummer-class test after rational
    factors and one-quadratic-plus-linears.  It is a meet-in-the-middle over
    character vectors on the legal B rows, not an unrestricted coefficient fit.
    """

    stats: Counter = Counter()
    n = len(rows)
    target = mask_for_rows(rows)
    full = (1 << n) - 1
    domain = [B for B, _bit in rows]
    chars = squareclass_table(q)
    seen: dict[int, tuple[int, int]] = {}
    stats["rows"] = n
    stats["plus_rows"] = sum(1 for _B, bit in rows if bit == 0)
    stats["minus_rows"] = sum(1 for _B, bit in rows if bit == 1)
    stats["target_weight"] = popcount(target)

    for u in range(q):
        for v in range(q):
            disc = (u * u - 4 * v) % q
            if chars[disc] != -1:
                continue
            mask = 0
            for index, B in enumerate(domain):
                value = (B * B + u * B + v) % q
                if chars[value] == -1:
                    mask |= 1 << index
            stats["irreducible_quadratics_tested"] += 1

            if mask == target:
                return stats, ((u, v), (-1, -1), 1)
            if (mask ^ full) == target:
                return stats, ((u, v), (-1, -1), -1)

            need = mask ^ target
            if need in seen:
                stats["unique_quadratic_masks_before_hit"] = len(seen)
                return stats, ((u, v), seen[need], 1)
            need = mask ^ (target ^ full)
            if need in seen:
                stats["unique_quadratic_masks_before_hit"] = len(seen)
                return stats, ((u, v), seen[need], -1)
            seen.setdefault(mask, (u, v))

    stats["unique_quadratic_masks"] = len(seen)
    return stats, None


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int, max_weight: int, quadratic_d3: bool, quadratic_pair_d3: bool) -> None:
    d3, d4, stats = legal_b_maps(q)
    core = core_b_values(q)
    stats["core_B"] = len(core)
    stats["legal_B_in_core"] = len(set(d3) & core)
    stats["legal_B_missing_core"] = len(set(d3) - core)
    print_counter(f"q{q}_b_line_domain_stats", stats)

    screens = {
        "d2legal_on_coreB": [(B, 0 if B in d3 else 1) for B in sorted(core)],
        "d3_on_legalB": [(B, 0 if value == 1 else 1) for B, value in sorted(d3.items())],
        "d4_on_d3plusB": [(B, 0 if value == 1 else 1) for B, value in sorted(d4.items())],
    }
    for name, rows in screens.items():
        search_stats, solution = exact_linear_factor_search(q, rows, max_weight)
        print_counter(f"q{q}_{name}_linear_support_stats", search_stats)
        if solution is None:
            print(f"q{q}_{name}_linear_support_result: none_weight_le_{max_weight}")
        else:
            weight, factors, polarity = solution
            print(
                f"q{q}_{name}_linear_support_result: "
                f"weight={weight} polarity={polarity} factors={','.join(str(f) for f in factors)}"
            )

        if quadratic_d3 and name == "d3_on_legalB":
            quad_stats, quad_solution = irreducible_quadratic_plus_linear_search(q, rows, 2)
            print_counter(f"q{q}_{name}_quad_plus_linear_support_stats", quad_stats)
            if quad_solution is None:
                print(f"q{q}_{name}_quad_plus_linear_support_result: none_quad_plus_le_2_linear")
            else:
                u, v, factors, polarity = quad_solution
                print(
                    f"q{q}_{name}_quad_plus_linear_support_result: "
                    f"quadratic=B^2+{u}B+{v} polarity={polarity} "
                    f"linear_factors={','.join(str(f) for f in factors) if factors else 'none'}"
                )

        if quadratic_pair_d3 and name == "d3_on_legalB":
            pair_stats, pair_solution = irreducible_quadratic_pair_search(q, rows)
            print_counter(f"q{q}_{name}_two_quadratic_support_stats", pair_stats)
            if pair_solution is None:
                print(f"q{q}_{name}_two_quadratic_support_result: none_two_irreducible_quadratics")
            else:
                q0, q1, polarity = pair_solution
                q0_label = "single" if q1 == (-1, -1) else f"B^2+{q1[0]}B+{q1[1]}"
                print(
                    f"q{q}_{name}_two_quadratic_support_result: "
                    f"polarity={polarity} "
                    f"quadratic0=B^2+{q0[0]}B+{q0[1]} "
                    f"quadratic1={q0_label}"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="607,1607,1847,2087")
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--quadratic-d3", action="store_true")
    parser.add_argument("--quadratic-pair-d3", action="store_true")
    args = parser.parse_args()

    print("p27 B-line branch-support probe")
    print("screens = d2 legal on core B, d3 on legal B, d4 after d3 on legal B")
    print("factor families = rational linears; optional irreducible quadratic tests")
    print(f"max_weight = {args.max_weight}")
    print(f"quadratic_d3 = {args.quadratic_d3}")
    print(f"quadratic_pair_d3 = {args.quadratic_pair_d3}")
    for q in parse_ints(args.small_primes):
        run_field(q, args.max_weight, args.quadratic_d3, args.quadratic_pair_d3)
    print("p27_b_line_branch_support_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
