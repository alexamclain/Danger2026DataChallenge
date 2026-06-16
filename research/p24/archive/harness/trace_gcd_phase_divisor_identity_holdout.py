#!/usr/bin/env python3
"""Holdout for phase-divisor identities versus interpolation.

This combines two bounded checks on the pinned actual-CM trace-GCD row:

1. A small phase-unit dictionary test.  A real Borcherds/Fitting product
   should recognize the determinant-line phase vector before the unit
   dictionary spans the full ambient log space.  Full-rank containment is
   treated as interpolation.

2. A determinant-zero control.  Coordinatewise nonzero payloads, including
   coordinate Kummer-style powers, do not certify a determinant line.  The
   control uses the same matrix size as the actual row and builds a singular
   matrix with all entries nonzero.

The script is a theorem microscope, not a proof of the p24 p-unit theorem.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import random

import sympy as sp

from lang_trace_gcd_block_cycle_norm_audit import (
    class_representatives,
    det_mod,
    first_matrix_row,
)
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence
from trace_gcd_chow_phase_coordinate_scan import values_by_omitted
from trace_gcd_chow_phase_divisor_span_scan import (
    contains_mod_prime,
    discrete_log_table,
    first_containment_index,
    log_vector,
    ordered_dictionary,
    random_containment_rate,
    rank_mod_prime,
)
from trace_gcd_chow_plain_divisor_scan import first_row_with_cycle


def dense_control_matrix(size: int, q: int) -> tuple[tuple[int, ...], ...]:
    base = tuple((index + 2) % q for index in range(size))
    return tuple(
        tuple((scale * value) % q for value in base)
        for scale in range(1, size + 1)
    )


def all_entries_nonzero(matrix: tuple[tuple[int, ...], ...], q: int) -> bool:
    return all(value % q for row in matrix for value in row)


def coordinate_power_nonzero(
    matrix: tuple[tuple[int, ...], ...],
    q: int,
    exponent: int,
) -> bool:
    return all(pow(value % q, exponent, q) for row in matrix for value in row)


def determinant_control(args: argparse.Namespace) -> dict[str, int]:
    row = first_matrix_row(args)
    if row is None:
        raise SystemExit("no eligible actual-CM matrix row found")

    records_by_omitted: dict[int, list] = defaultdict(list)
    for record in row.records:
        records_by_omitted[record.omitted].append(record)

    chosen_omitted = sorted(records_by_omitted)[0]
    reps, det_mismatches = class_representatives(
        records_by_omitted[chosen_omitted], row.right
    )
    actual = next(record for record in reps if record.determinant)
    size = len(actual.matrix)
    control = dense_control_matrix(size, row.q)
    control_det = det_mod(control, row.q)

    return {
        "D": row.D,
        "q": row.q,
        "m": row.m,
        "left": row.left,
        "right": row.right,
        "omitted": chosen_omitted,
        "right_class_det_mismatches": det_mismatches,
        "block_size": size,
        "actual_det_nonzero": int(bool(actual.determinant)),
        "actual_entries_all_nonzero": int(all_entries_nonzero(actual.matrix, row.q)),
        "control_entries_all_nonzero": int(all_entries_nonzero(control, row.q)),
        "coordinate_power_nonzero": int(
            coordinate_power_nonzero(control, row.q, row.right)
        ),
        "control_det_zero": int(control_det == 0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=13463)
    parser.add_argument("--q-stop", type=int, default=13464)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=8)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int, default=140)
    parser.add_argument("--only-D", type=int, default=-13319)
    parser.add_argument("--only-q", type=int, default=13463)
    parser.add_argument("--only-m", type=int, default=28)
    parser.add_argument("--only-left", type=int, default=4)
    parser.add_argument("--only-right", type=int, default=7)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--all-omitted", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument(
        "--unit-family",
        nargs="+",
        choices=("right-binomial", "heegner-fiber"),
        default=["right-binomial", "heegner-fiber"],
    )
    parser.add_argument("--max-binomial-constant", type=int, default=8)
    parser.add_argument("--max-heegner-abs-D", type=int, default=500)
    parser.add_argument("--max-heegner-h", type=int, default=10)
    parser.add_argument("--random-controls", type=int, default=50)
    args = parser.parse_args()

    bundle = first_row_with_cycle(args)
    if bundle is None:
        raise SystemExit("no eligible phase-divisor holdout row found")
    row = bundle.row
    generator, logs = discrete_log_table(row.q)
    factors = sorted(int(prime) for prime in sp.factorint(row.q - 1))
    units = ordered_dictionary(args, bundle)
    unit_logs = [log_vector(unit.values, logs, row.q - 1) for unit in units]
    rng = random.Random(args.seed + 2024)

    print("trace-GCD phase-divisor identity holdout")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"log_generator={generator}")
    print(f"q_minus_1_prime_factors={factors}")
    print(f"unit_dictionary_size={len(units)}")
    print(f"unit_dictionary_names_prefix={[unit.name for unit in units[:8]]}")

    nonrandom_span_hits = 0
    full_rank_interpolation_hits = 0
    target_misses = 0
    failures = 0
    for omitted, records in values_by_omitted(bundle).items():
        if args.only_omitted is not None and omitted != args.only_omitted:
            continue
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        if any(value == 0 for value in seq):
            failures += 1
            print(f"omitted={omitted} skipped_zero_target=1")
            continue
        target_log = log_vector(seq, logs, row.q - 1)
        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  target_values={seq}")
        for prime in factors:
            rows_mod = [[value % prime for value in vector] for vector in unit_logs]
            target_mod = [value % prime for value in target_log]
            rank = rank_mod_prime(rows_mod, prime)
            contains = contains_mod_prime(rows_mod, target_mod, prime)
            first_index, first_rank = first_containment_index(
                rows_mod, target_mod, prime
            )
            random_rate = random_containment_rate(
                rows_mod, row.right, prime, args.random_controls, rng
            )
            nonrandom = contains and rank < row.right and random_rate < 0.25
            full_interp = contains and rank == row.right
            nonrandom_span_hits += int(nonrandom)
            full_rank_interpolation_hits += int(full_interp)
            target_misses += int(not contains)
            print(f"  mod_prime={prime}")
            print(f"    dictionary_rank={rank}/{row.right}")
            print(f"    target_in_span={int(contains)}")
            print(f"    first_containment_index={first_index}")
            print(f"    first_containment_rank={first_rank}")
            print(f"    random_containment_rate={random_rate:.6f}")
            print(f"    nonrandom_span_hit={int(nonrandom)}")
            print(f"    full_rank_interpolation_hit={int(full_interp)}")

    control = determinant_control(args)
    print("determinant_zero_control")
    for key, value in control.items():
        print(f"  {key}={value}")

    coordinate_control_failure = (
        control["control_entries_all_nonzero"]
        and control["coordinate_power_nonzero"]
        and control["control_det_zero"]
    )
    print("summary")
    print(f"  nonrandom_span_hits={nonrandom_span_hits}")
    print(f"  full_rank_interpolation_hits={full_rank_interpolation_hits}")
    print(f"  target_misses={target_misses}")
    print(f"  coordinate_payload_zero_detection_failure={int(coordinate_control_failure)}")
    print("interpretation")
    print("  nonrandom_span_hits>0 would suggest a real bounded product formula.")
    print("  full_rank_interpolation_hits are tautological dictionary span events.")
    print("  coordinate_payload_zero_detection_failure=1 rejects entrywise/Kummer-only payloads.")
    print("  a p24 proof still needs a phase-aware determinant-line divisor or direct Fitting p-unit.")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_phase_divisor_identity_holdout")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
