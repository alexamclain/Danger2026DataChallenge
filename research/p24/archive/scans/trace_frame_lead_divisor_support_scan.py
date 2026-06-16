#!/usr/bin/env python3
"""Divisor-shape diagnostic for the leading trace-frame determinant.

This tests the easiest Borcherds/modular-unit hope for the new Xi_lead target:
as the CM origin moves around a small embedded cycle, does the norm of the
fixed leading Plucker determinant look like a low-complexity divisor in the
plain j coordinate, with numerator roots supported on target CM or small
Heegner reductions?

The test is intentionally small.  Generic roots do not disprove a genuinely
phase-aware divisor, but they rule out the naive "Xi_lead is already a simple
Heegner-supported function of j" explanation.
"""

from __future__ import annotations

import argparse

from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from phase_divisor_heegner_support_scan import (
    heegner_roots,
    interpolant_roots,
    root_hits,
)
from relative_moment_projection_scan import rotate, section_fiber_polynomials
from trace_frame_leading_residual_value_audit import target_value_rows


def minimal_period(values: list[int]) -> int:
    if not values:
        return 0
    n = len(values)
    for period in range(1, n + 1):
        if n % period == 0 and all(values[i] == values[i % period] for i in range(n)):
            return period
    return n


def fixed_cycle(D: int, q: int, ell: int) -> list[int]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), q)
    graph = isogeny_neighbors(roots, ell, q)
    return walk_cycle(graph)


def lead_norm_pairs(
    cycle: list[int],
    q: int,
    m: int,
    factor_index: int,
    subdegree: int,
    target: str,
    seed: int,
    max_top_count: int,
) -> tuple[list[tuple[int, int]], dict[str, int]]:
    n = len(cycle) // m
    factors = packet_factors(n, q)
    factor = factors[factor_index]
    pairs: list[tuple[int, int]] = []
    metadata: dict[str, int] = {
        "n": n,
        "factor_degree": factor.degree(),
        "missing_rows": 0,
        "zero_norm_values": 0,
        "raw_rank": -1,
        "tensor_factor_degree": -1,
        "top_count": -1,
    }
    for shift in range(len(cycle)):
        shifted = rotate(cycle, shift)
        residues = [
            fiber.rem(factor)
            for fiber in section_fiber_polynomials(shifted, q, m, "complement")
        ]
        residue_vectors = [
            coeff_vector(residue, factor.degree(), q)
            for residue in residues
        ]
        rows = [
            row for row in target_value_rows(
                D=0,
                q=q,
                ell=0,
                h=len(cycle),
                m=m,
                factor=factor,
                origin_shift=shift,
                residue_vectors=residue_vectors,
                target=target,
                seed=seed,
                max_top_count=max_top_count,
            )
            if row.subdegree == subdegree
        ]
        if len(rows) != 1 or rows[0].det_norm_base is None:
            metadata["missing_rows"] += 1
            continue
        row = rows[0]
        metadata["raw_rank"] = row.raw_rank
        metadata["tensor_factor_degree"] = row.tensor_factor_degree
        metadata["top_count"] = row.top_count
        value = row.det_norm_base % q
        if value == 0:
            metadata["zero_norm_values"] += 1
        pairs.append((cycle[shift] % q, value))
    return pairs, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--D", type=int, default=-10919)
    parser.add_argument("--q", type=int, default=11243)
    parser.add_argument("--ell", type=int, default=2)
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--factor-index", type=int, default=0)
    parser.add_argument("--subdegree", type=int, default=2)
    parser.add_argument("--target", default="axis")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--max-top-count", type=int, default=4)
    parser.add_argument("--max-heegner-abs-D", type=int, default=3000)
    parser.add_argument("--max-heegner-h", type=int, default=30)
    args = parser.parse_args()

    cycle = fixed_cycle(args.D, args.q, args.ell)
    pairs, metadata = lead_norm_pairs(
        cycle,
        args.q,
        args.m,
        args.factor_index,
        args.subdegree,
        args.target,
        args.seed,
        args.max_top_count,
    )
    if len(pairs) < 2:
        raise RuntimeError("not enough determinant values to interpolate")
    degree, num_roots, den_roots = interpolant_roots(pairs, args.q)
    cm_roots = {x for x, _ in pairs}
    heegner = heegner_roots(args.q, args.max_heegner_abs_D, args.max_heegner_h)
    hits = root_hits(num_roots, heegner)
    ordered_values = [y for _, y in pairs]
    distinct_values = set(ordered_values)
    period = minimal_period(ordered_values)

    print("trace-frame leading determinant divisor-support scan")
    print(f"D={args.D}")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"h={len(cycle)}")
    print(f"m={args.m}")
    print(f"n={metadata['n']}")
    print(f"target={args.target}")
    print(f"factor_index={args.factor_index}")
    print(f"factor_degree={metadata['factor_degree']}")
    print(f"tensor_factor_degree={metadata['tensor_factor_degree']}")
    print(f"subdegree={args.subdegree}")
    print(f"raw_rank={metadata['raw_rank']}")
    print(f"top_count={metadata['top_count']}")
    print(f"value_rows={len(pairs)}")
    print(f"missing_rows={metadata['missing_rows']}")
    print(f"zero_norm_values={metadata['zero_norm_values']}")
    print(f"distinct_norm_values={len(distinct_values)}")
    print(f"origin_value_period={period}")
    print(f"origin_value_orbit_size={len(pairs) // period if period else 0}")
    print(f"rational_degree={degree}")
    print(f"numerator_roots={num_roots}")
    print(f"denominator_roots={den_roots}")
    print(f"numerator_roots_in_target_cm={sorted(set(num_roots) & cm_roots)}")
    print(f"heegner_discriminants_tested={len(heegner)}")
    print(f"heegner_roots_total={sum(len(v) for v in heegner.values())}")
    print("numerator_root_heegner_hits")
    for hit in hits:
        print(f"  root={hit.root} discriminants={hit.discriminants}")
    print()
    print("interpretation")
    print(f"  determinant_norm_constant={int(len(distinct_values) == 1)}")
    print("  determinant_norm_has_nontrivial_origin_period=" + str(int(period < len(pairs))))
    print("  numerator_roots_outside_target_cm=" + str(int(not set(num_roots) <= cm_roots)))
    print("  numerator_roots_with_small_heegner_support=" + str(sum(bool(hit.discriminants) for hit in hits)))
    print("  tested_simple_j_divisor_for_Xi_lead=1")
    print("conclusion=reported_trace_frame_lead_divisor_support_scan")


if __name__ == "__main__":
    main()
