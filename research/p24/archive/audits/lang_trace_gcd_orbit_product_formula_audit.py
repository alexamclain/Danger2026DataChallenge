#!/usr/bin/env python3
"""Formula-shape audit for trace-GCD Frobenius orbit products.

The seven-orbit p24 payload is small already, but a proof might become easier
if the orbit products satisfy a visible relation: equality under a unit action,
small power relations, or a simple product collapse.

This script checks those patterns on a small actual-CM trace-GCD row.  It is
only a theorem-candidate filter; absence of a small relation is not a proof of
independence.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from math import gcd

import sympy as sp

from lang_trace_gcd_origin_action_audit import OriginDet, first_row
from lang_trace_gcd_sequence_complexity import nonnull_ints, reduced_right_sequence


def product_mod(values: list[int], modulus: int) -> int:
    out = 1
    for value in values:
        out = (out * (value % modulus)) % modulus
    return out


def primitive_root(modulus: int) -> int:
    factors = [int(factor) for factor in sp.factorint(modulus - 1)]
    for candidate in range(2, modulus):
        if gcd(candidate, modulus) != 1:
            continue
        if all(pow(candidate, (modulus - 1) // factor, modulus) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {modulus}")


def discrete_log_table(generator: int, modulus: int) -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(modulus - 1):
        table[value] = exponent
        value = (value * generator) % modulus
    return table


def frobenius_orbits(modulus: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * multiplier) % modulus
        out.append(orbit)
    return out


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {value: index for index, orbit in enumerate(orbits) for value in orbit}


def unit_permutation(unit: int, modulus: int, orbits: list[list[int]]) -> tuple[int, ...] | None:
    labels = orbit_label_map(orbits)
    image: list[int] = []
    for orbit in orbits:
        mapped = (unit * orbit[0]) % modulus
        if mapped not in labels:
            return None
        image.append(labels[mapped])
    return tuple(image)


def small_power_relations(
    logs: list[int],
    modulus: int,
    bound: int,
) -> list[tuple[int, int, int, int]]:
    """Return relations product_i^a = product_j^b for small nonzero a,b."""
    relations: list[tuple[int, int, int, int]] = []
    for i in range(len(logs)):
        for j in range(i + 1, len(logs)):
            for a in range(-bound, bound + 1):
                if a == 0:
                    continue
                for b in range(-bound, bound + 1):
                    if b == 0:
                        continue
                    if (a * logs[i] - b * logs[j]) % modulus == 0:
                        relations.append((i, a, j, b))
    return relations


def small_total_relations(
    logs: list[int],
    modulus: int,
    bound: int,
) -> list[tuple[int, ...]]:
    """Return primitive small product relations among all orbit products."""
    out: list[tuple[int, ...]] = []

    def search(prefix: list[int], index: int) -> None:
        if index == len(logs):
            if all(value == 0 for value in prefix):
                return
            if gcd(*[abs(value) for value in prefix if value != 0]) != 1:
                return
            total = sum(coeff * log for coeff, log in zip(prefix, logs)) % modulus
            if total == 0:
                out.append(tuple(prefix))
            return
        for coeff in range(-bound, bound + 1):
            search(prefix + [coeff], index + 1)

    search([], 0)
    return out


def values_by_omitted(records: tuple[OriginDet, ...]) -> dict[int, list[OriginDet]]:
    out: dict[int, list[OriginDet]] = defaultdict(list)
    for record in records:
        out[record.omitted].append(record)
    return dict(sorted(out.items()))


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
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--relation-bound", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_row(args)
    if row is None:
        raise SystemExit("no eligible origin-action row found")

    q_mod_right = row.q % row.right
    orbits = frobenius_orbits(row.right, q_mod_right)
    nontrivial_orbits = [orbit for orbit in orbits if any(value != 0 for value in orbit)]
    generator = primitive_root(row.q)
    log_table = discrete_log_table(generator, row.q)

    print("Lang trace-gcd orbit-product formula audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"pair=({row.left},{row.right})")
    print(f"right={row.right}")
    print(f"q_mod_right={q_mod_right}")
    print(f"frobenius_orbits={orbits}")
    print(f"primitive_root_mod_q={generator}")
    print(f"relation_bound={args.relation_bound}")

    candidate_units = [
        unit
        for unit in range(2, row.right)
        if gcd(unit, row.right) == 1
        and unit_permutation(unit, row.right, orbits) is not None
    ]
    print(
        "unit_permutations="
        f"{[(unit, unit_permutation(unit, row.right, orbits)) for unit in candidate_units]}"
    )

    failures = 0
    for omitted, records in values_by_omitted(row.records).items():
        right_values, mismatches = reduced_right_sequence(records, row.right)
        seq = nonnull_ints(right_values)
        if mismatches:
            failures += 1
        orbit_products = [product_mod([seq[index] for index in orbit], row.q) for orbit in orbits]
        nontrivial_products = [
            product_mod([seq[index] for index in orbit], row.q)
            for orbit in nontrivial_orbits
        ]
        logs = [log_table[value] for value in orbit_products if value != 0]
        nontrivial_logs = [log_table[value] for value in nontrivial_products if value != 0]
        pair_relations = small_power_relations(
            nontrivial_logs,
            row.q - 1,
            args.relation_bound,
        )
        total_relations = small_total_relations(
            logs,
            row.q - 1,
            args.relation_bound,
        )

        print(f"omitted={omitted}")
        print(f"  right_mismatches={mismatches}")
        print(f"  right_values={seq}")
        print(f"  orbit_products={orbit_products}")
        print(f"  orbit_product_logs={logs}")
        print(f"  nontrivial_orbit_products={nontrivial_products}")
        print(f"  nontrivial_orbit_product_logs={nontrivial_logs}")
        print(f"  orbit_products_distinct={len(set(orbit_products))}/{len(orbit_products)}")
        print(
            "  nontrivial_orbit_products_distinct="
            f"{len(set(nontrivial_products))}/{len(nontrivial_products)}"
        )
        for unit in candidate_units:
            perm = unit_permutation(unit, row.right, orbits)
            if perm is None:
                continue
            equal_edges = sum(
                1
                for index, product in enumerate(orbit_products)
                if product == orbit_products[perm[index]]
            )
            print(f"  unit={unit} permutation={perm} equal_edges={equal_edges}/{len(orbits)}")
        print(f"  small_pair_power_relations={pair_relations[:20]}")
        print(f"  small_total_relations_count={len(total_relations)}")
        print(f"  small_total_relations_sample={total_relations[:20]}")
        print(
            "  visible_compression_relation_found="
            f"{int(bool(pair_relations or total_relations))}"
        )

    print("interpretation")
    print("  no_visible_relation means no equality/small-power shortcut was found")
    print("  orbit products remain the honest small payload for this row")
    print(f"failures={failures}")
    print("conclusion=reported_lang_trace_gcd_orbit_product_formula_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
