#!/usr/bin/env python3
"""Scan A-level cubic characters as possible shortcuts for the ell=3 filter.

The Montgomery 3-division quartic

    psi_3(z) = 3*z^4 + 4*A*z^3 + 6*z^2 - 1

has square discriminant for p23-congruence fields, so a natural hope is that a
cubic resolvent character in A, or in a low-degree polynomial in A, can cheaply
classify trace mod 3. This sidecar scans full three-valued cubic characters of
low-degree A-polynomials and pair products against the exact ell=3 classifier.

This is research-only and does not touch the production run.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations

import x16_trace_feature_scan as feature_scan
import x16_trace_residue_calibration as cal
from ell3_trace_filter_validate import trace_mod3_filter


@dataclass(frozen=True)
class Row:
    A: int
    trace_mod3: int


def primitive_cube_root_unity(p: int) -> int:
    for g in range(2, p):
        omega = pow(g, (p - 1) // 3, p)
        if omega != 1:
            return omega
    raise ValueError("no primitive cube root of unity found")


def cubic_class(a: int, p: int, omega: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 3, p)
    if value == 1:
        return 1
    if value == omega:
        return 2
    if value == omega * omega % p:
        return 3
    raise ValueError("unexpected cubic character value")


def feature_values(A: int, p: int) -> dict[str, int]:
    A %= p
    A2 = A * A % p
    A3 = A2 * A % p
    inv27 = pow(27, p - 2, p)
    return {
        "A": A,
        "A-1": A - 1,
        "A+1": A + 1,
        "A-2": A - 2,
        "A+2": A + 2,
        "A^2-4": A2 - 4,
        "A^2-3": A2 - 3,
        "A^2+3": A2 + 3,
        "A^2+A+1": A2 + A + 1,
        "A^2-A+1": A2 - A + 1,
        "A^2+4A+1": A2 + 4 * A + 1,
        "A^2-4A+1": A2 - 4 * A + 1,
        "A^3-3A+1": A3 - 3 * A + 1,
        "A^3+3A+1": A3 + 3 * A + 1,
        "(A-2)*(A+1)": (A - 2) * (A + 1),
        "(A+2)*(A-1)": (A + 2) * (A - 1),
        "Cardano_C=16*(A^2-4)/27": 16 * (A2 - 4) * inv27,
    }


def summarize_partition(labels: list[int], rows: list[Row], label: str) -> tuple[float, str]:
    buckets: dict[int, Counter[int]] = defaultdict(Counter)
    for cls, row in zip(labels, rows):
        buckets[cls][row.trace_mod3] += 1
    majority_accuracy = sum(max(counter.values()) for counter in buckets.values()) / len(rows)

    reject_total = sum(1 for row in rows if row.trace_mod3 == 1)
    best_reject_score = 0.0
    best_reject = ""
    for cls, counter in buckets.items():
        selected = sum(counter.values())
        hits = counter[1]
        if not selected:
            continue
        precision = hits / selected
        capture = hits / reject_total if reject_total else 0.0
        base = reject_total / len(rows)
        lift = precision / base if base else 0.0
        score = precision * capture
        if score > best_reject_score:
            best_reject_score = score
            best_reject = (
                f"best_reject_bucket={cls} selected={selected} hits={hits} "
                f"precision={precision:.4f} capture={capture:.4f} lift={lift:.3f}"
            )

    return majority_accuracy, f"{label} majority_accuracy={majority_accuracy:.4f} {best_reject}"


def scan_prime(p: int, samples: int, seed: int, top: int, pair_top: int) -> None:
    rng = random.Random(seed)
    pairs = feature_scan.x16_samples_with_y(p, rng, samples)
    rows = [Row(A=A, trace_mod3=trace_mod3_filter(A, p)) for _y, A in pairs]
    omega = primitive_cube_root_unity(p)
    print(f"p={p}")
    print(f"samples={len(rows)} seed={seed}")
    print(f"primitive_cube_root_unity={omega}")
    print(f"trace_mod3_counts={dict(sorted(Counter(row.trace_mod3 for row in rows).items()))}")

    names = sorted(feature_values(rows[0].A, p)) if rows else []
    class_vectors: dict[tuple[str, int], list[int]] = {}
    single_rows: list[tuple[float, str]] = []
    for name in names:
        values = [feature_values(row.A, p)[name] for row in rows]
        for exp in (1, 2):
            labels = [cubic_class(pow(value % p, exp, p), p, omega) for value in values]
            acc, text = summarize_partition(labels, rows, f"feature={name}^{exp}")
            single_rows.append((acc, text))
            class_vectors[(name, exp)] = labels

    print("top_single")
    for _acc, text in sorted(single_rows, reverse=True)[:top]:
        print(text)

    if pair_top:
        pair_rows: list[tuple[float, str]] = []
        atoms = list(class_vectors)
        for (name1, exp1), (name2, exp2) in combinations(atoms, 2):
            if name1 == name2:
                continue
            labels = []
            for row in rows:
                vals = feature_values(row.A, p)
                value = pow(vals[name1] % p, exp1, p) * pow(vals[name2] % p, exp2, p)
                labels.append(cubic_class(value, p, omega))
            acc, text = summarize_partition(
                labels,
                rows,
                f"pair=({name1}^{exp1})*({name2}^{exp2})",
            )
            pair_rows.append((acc, text))

        print("top_pairs")
        for _acc, text in sorted(pair_rows, reverse=True)[:pair_top]:
            print(text)
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=600)
    parser.add_argument("--starts", type=int, nargs="+", default=[100_000, 200_000, 400_000])
    parser.add_argument("--seed", type=int, default=20260608)
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("--pair-top", type=int, default=8)
    args = parser.parse_args()

    modulus = 8 * 3 * 5 * 7 * 11
    print("Ell=3 A-level cubic-resolvent scan")
    print(f"p23_mod_modulus={cal.P23 % modulus} modulus={modulus}")
    print()
    for start in args.starts:
        p = cal.find_calibration_prime(start, modulus, cal.P23 % modulus)
        scan_prime(p, args.samples, args.seed, args.top, args.pair_top)


if __name__ == "__main__":
    main()
