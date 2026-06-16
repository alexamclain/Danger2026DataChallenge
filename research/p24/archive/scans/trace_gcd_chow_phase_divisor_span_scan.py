#!/usr/bin/env python3
"""Phase-aware unit-span scan for the trace-GCD Chow determinant.

This is a bounded recognition test for a possible product formula

    Chow right-phase sequence = product of simple phase-aware units.

It builds a small dictionary of unit-valued right-phase vectors, converts
them and the Chow determinant values to discrete-log vectors modulo the prime
factors of `q-1`, and asks whether the Chow vector lies in the span before
the dictionary becomes the whole ambient space.

The scan is intentionally small and falsification-oriented.  A sparse
non-random span would suggest a candidate `Psi_O`; a full-rank-only fit is
just interpolation in unit clothing.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import random

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence
from phase_divisor_heegner_support_scan import heegner_roots
from trace_gcd_chow_phase_coordinate_scan import values_by_omitted
from trace_gcd_chow_plain_divisor_scan import RowWithCycle, first_row_with_cycle


@dataclass(frozen=True)
class UnitVector:
    name: str
    values: tuple[int, ...]


def rank_mod_prime(rows: list[list[int]], prime: int) -> int:
    mat = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    if not mat:
        return 0
    row_count = len(mat)
    col_count = len(mat[0])
    rank = 0
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if mat[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % prime, -1, prime)
        mat[rank] = [(value * inv) % prime for value in mat[rank]]
        for row in range(row_count):
            if row == rank or not mat[row][col] % prime:
                continue
            scale = mat[row][col] % prime
            mat[row] = [
                (left - scale * right) % prime
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def contains_mod_prime(rows: list[list[int]], target: list[int], prime: int) -> bool:
    return rank_mod_prime(rows, prime) == rank_mod_prime(rows + [target], prime)


def discrete_log_table(q: int) -> tuple[int, dict[int, int]]:
    generator = int(sp.primitive_root(q))
    table: dict[int, int] = {}
    value = 1
    for exponent in range(q - 1):
        table[value] = exponent
        value = value * generator % q
    if len(table) != q - 1:
        raise RuntimeError("primitive root table did not cover F_q^*")
    return generator, table


def log_vector(values: tuple[int, ...] | list[int], table: dict[int, int], modulus: int) -> list[int]:
    out: list[int] = []
    for value in values:
        value %= modulus + 1
        if value == 0:
            raise ValueError("cannot take log of zero")
        out.append(table[value])
    return out


def ext_norm_to_base(field: ExtensionField, value: tuple[int, ...]) -> int | None:
    if any(coeff % field.q for coeff in value[1:]):
        return None
    return value[0] % field.q


def right_binomial_units(
    q: int,
    right: int,
    max_constant: int,
    seed: int,
) -> list[UnitVector]:
    order = int(sp.n_order(q % right, right))
    modulus = find_irreducible_modulus(q, order, seed)
    field = ExtensionField(q, order, modulus)
    zeta = primitive_root_of_order(field, right, seed)
    units: list[UnitVector] = []
    frob_powers = [pow(q, i, right) for i in range(order)]
    for c in range(2, min(q, max_constant + 1)):
        c_ext = field.embed(c)
        for k in range(1, right):
            values: list[int] = []
            ok = True
            for t in range(right):
                norm = field.one
                for power in frob_powers:
                    exponent = (k * t * power) % right
                    term = field.sub(field.one, field.mul(c_ext, field.pow(zeta, exponent)))
                    norm = field.mul(norm, term)
                base = ext_norm_to_base(field, norm)
                if base is None or base == 0:
                    ok = False
                    break
                values.append(base)
            if ok:
                units.append(UnitVector(f"right_binomial:c={c}:k={k}", tuple(values)))
    return units


def heegner_fiber_units(
    bundle: RowWithCycle,
    max_abs_D: int,
    max_h: int,
) -> list[UnitVector]:
    row = bundle.row
    heegner = heegner_roots(row.q, max_abs_D, max_h)
    roots = sorted({root for roots in heegner.values() for root in roots})
    records_by_right: dict[int, list] = defaultdict(list)
    for record in row.records:
        records_by_right[record.alpha % row.right].append(record)
    units: list[UnitVector] = []
    for root in roots:
        values: list[int] = []
        ok = True
        for t in range(row.right):
            product = 1
            for record in records_by_right[t]:
                factor = (bundle.cycle[record.shift] - root) % row.q
                if factor == 0:
                    ok = False
                    break
                product = product * factor % row.q
            if not ok:
                break
            values.append(product)
        if ok:
            units.append(UnitVector(f"heegner_fiber:root={root}", tuple(values)))
    return units


def ordered_dictionary(args: argparse.Namespace, bundle: RowWithCycle) -> list[UnitVector]:
    units: list[UnitVector] = []
    requested = set(args.unit_family)
    if "right-binomial" in requested:
        units.extend(
            right_binomial_units(
                bundle.row.q,
                bundle.row.right,
                args.max_binomial_constant,
                args.seed,
            )
        )
    if "heegner-fiber" in requested:
        units.extend(
            heegner_fiber_units(
                bundle,
                args.max_heegner_abs_D,
                args.max_heegner_h,
            )
        )
    # Preserve order while removing duplicate value vectors.
    seen: set[tuple[int, ...]] = set()
    unique: list[UnitVector] = []
    for unit in units:
        if unit.values in seen:
            continue
        seen.add(unit.values)
        unique.append(unit)
    return unique


def first_containment_index(
    rows: list[list[int]],
    target: list[int],
    prime: int,
) -> tuple[int | None, int]:
    current: list[list[int]] = []
    current_rank = 0
    for index, row in enumerate(rows, start=1):
        new_rank = rank_mod_prime(current + [row], prime)
        current.append(row)
        current_rank = new_rank
        if contains_mod_prime(current, target, prime):
            return index, current_rank
    return None, current_rank


def random_containment_rate(
    rows: list[list[int]],
    length: int,
    prime: int,
    trials: int,
    rng: random.Random,
) -> float:
    if trials <= 0:
        return float("nan")
    hits = 0
    for _ in range(trials):
        target = [rng.randrange(prime) for _ in range(length)]
        hits += int(contains_mod_prime(rows, target, prime))
    return hits / trials


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
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true", default=True)
    parser.add_argument("--require-square-tail", action="store_true", default=True)
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
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
    parser.add_argument("--max-heegner-abs-D", type=int, default=1000)
    parser.add_argument("--max-heegner-h", type=int, default=20)
    parser.add_argument("--random-controls", type=int, default=100)
    args = parser.parse_args()

    bundle = first_row_with_cycle(args)
    if bundle is None:
        raise SystemExit("no eligible phase-divisor span row found")
    row = bundle.row
    if row.q <= row.right:
        raise SystemExit("this bounded scan expects q > right")
    generator, logs = discrete_log_table(row.q)
    factors = sorted(int(prime) for prime in sp.factorint(row.q - 1))
    units = ordered_dictionary(args, bundle)
    unit_logs = [log_vector(unit.values, logs, row.q - 1) for unit in units]
    rng = random.Random(args.seed + 9001)

    print("trace-GCD Chow phase-divisor unit-span scan")
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
    print(f"unit_families={args.unit_family}")
    print(f"unit_dictionary_size={len(units)}")
    print(f"unit_dictionary_names_prefix={[unit.name for unit in units[:12]]}")

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
        print(f"  target_logs_mod_q_minus_1={target_log}")
        for prime in factors:
            rows_mod = [[value % prime for value in vector] for vector in unit_logs]
            target_mod = [value % prime for value in target_log]
            rank = rank_mod_prime(rows_mod, prime)
            contains = contains_mod_prime(rows_mod, target_mod, prime)
            first_index, first_rank = first_containment_index(rows_mod, target_mod, prime)
            random_rate = random_containment_rate(
                rows_mod,
                row.right,
                prime,
                args.random_controls,
                rng,
            )
            print(f"  mod_prime={prime}")
            print(f"    dictionary_rank={rank}/{row.right}")
            print(f"    target_in_span={int(contains)}")
            print(f"    first_containment_index={first_index}")
            print(f"    first_containment_rank={first_rank}")
            print(f"    random_containment_rate={random_rate:.6f}")

    print("interpretation")
    print("  target_in_span with rank < right and low random rate would suggest a product formula.")
    print("  target_in_span only at full rank is just interpolation in unit coordinates.")
    print("  target_not_in_span demotes this bounded phase-unit dictionary.")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_chow_phase_divisor_span_scan")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
