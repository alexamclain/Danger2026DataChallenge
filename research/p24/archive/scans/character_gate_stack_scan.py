#!/usr/bin/env python3
"""Greedy train/holdout scan for stacking cheap character gates.

The one-feature scan finds a stable A±2 gate, which is the first inverse
halving condition and gives only a constant-factor lift.  This script asks a
stronger question:

    Can a stack of cheap low-degree Legendre gates keep adding independent
    2-adic information across small p = n^2 + 7 fields?

It trains a greedy gate stack on the first half of exact small-field rows and
reports both train and holdout precision/lift after each selected atom.  A
genuine structural label should generalize; overfit gates should collapse on
the held-out rows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np

from low_degree_character_trace_scan import (
    exact_xonly_good_flags,
    features,
    prime_rows,
)
from near_square_formula_probe import legendre_table


@dataclass(frozen=True)
class Atom:
    feature_index: int
    sign: int
    label: str


@dataclass
class FieldData:
    n: int
    p: int
    good: np.ndarray
    nonsingular: np.ndarray
    atoms: list[np.ndarray]
    good_count: int
    total_count: int


def build_field_data(n: int, p: int, fs, atoms: list[Atom]) -> FieldData:
    chi = legendre_table(p)
    good, _stats = exact_xonly_good_flags(p, chi)
    A = np.arange(p, dtype=np.int64)
    A2 = A * A % p
    nonsingular = np.ones(p, dtype=np.bool_)
    nonsingular[[2, p - 2]] = False

    values_by_feature: list[np.ndarray] = []
    for feature in fs:
        c2, c1, c0 = feature.coeffs(n, p)
        values_by_feature.append(chi[(c2 * A2 + c1 * A + c0) % p])

    atom_masks = [
        nonsingular & (values_by_feature[atom.feature_index] == atom.sign)
        for atom in atoms
    ]
    return FieldData(
        n=n,
        p=p,
        good=good,
        nonsingular=nonsingular,
        atoms=atom_masks,
        good_count=int(np.count_nonzero(good & nonsingular)),
        total_count=int(np.count_nonzero(nonsingular)),
    )


def metrics(fields: list[FieldData], selected: list[np.ndarray]) -> tuple[int, int, int, int]:
    total = 0
    hits = 0
    base_total = 0
    base_hits = 0
    for idx, field in enumerate(fields):
        if selected:
            mask = field.nonsingular.copy()
            for atom_masks in selected:
                mask &= atom_masks[idx]
        else:
            mask = field.nonsingular
        total += int(np.count_nonzero(mask))
        hits += int(np.count_nonzero(mask & field.good))
        base_total += field.total_count
        base_hits += field.good_count
    return hits, total, base_hits, base_total


def fmt_metrics(fields: list[FieldData], selected: list[np.ndarray]) -> str:
    hits, total, base_hits, base_total = metrics(fields, selected)
    precision = hits / total if total else 0.0
    base = base_hits / base_total if base_total else 0.0
    lift = precision / base if base else 0.0
    capture = hits / base_hits if base_hits else 0.0
    coverage = total / base_total if base_total else 0.0
    return (
        f"hits={hits}/{total} precision={precision:.6f} lift={lift:.3f} "
        f"capture={capture:.3f} coverage={coverage:.3f}"
    )


def score(fields: list[FieldData], selected: list[np.ndarray]) -> tuple[float, float, float]:
    hits, total, base_hits, base_total = metrics(fields, selected)
    if not total or not base_hits or not base_total:
        return (0.0, 0.0, 0.0)
    precision = hits / total
    base = base_hits / base_total
    lift = precision / base if base else 0.0
    capture = hits / base_hits
    coverage = total / base_total
    # Balanced objective: prefer precision, but punish tiny slices.
    return (lift * (capture ** 0.5), lift, coverage)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-p", type=int, default=10_000)
    ap.add_argument("--max-p", type=int, default=220_000)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--coeff-bound", type=int, default=2)
    ap.add_argument("--constant-coeffs", action="store_true")
    ap.add_argument("--max-gates", type=int, default=6)
    ap.add_argument("--min-train-coverage", type=float, default=0.02)
    ap.add_argument("--n-modulus", type=int, default=8)
    ap.add_argument("--n-residue", type=int, default=0)
    args = ap.parse_args()

    rows = prime_rows(args.min_p, args.max_p, args.max_rows, args.n_modulus, args.n_residue)
    fs = features(args.coeff_bound, include_linear_n=not args.constant_coeffs)
    atoms: list[Atom] = []
    for idx, feature in enumerate(fs):
        for sign in (-1, 1):
            atoms.append(Atom(idx, sign, f"sign={sign:+d} feature={feature.label()}"))

    print("character gate stack scan")
    print("family=p=n^2+7")
    print(f"rows={len(rows)}")
    print(f"coeff_bound={args.coeff_bound}")
    print(f"constant_coeffs={args.constant_coeffs}")
    print(f"feature_count={len(fs)} atom_count={len(atoms)}")

    all_fields = [build_field_data(n, p, fs, atoms) for n, p in rows]
    split = max(1, len(all_fields) // 2)
    train = all_fields[:split]
    holdout = all_fields[split:]
    print("train_rows=" + ",".join(str(field.p) for field in train))
    print("holdout_rows=" + ",".join(str(field.p) for field in holdout))
    print("base_train " + fmt_metrics(train, []))
    print("base_holdout " + fmt_metrics(holdout, []))

    selected_atom_indices: list[int] = []
    selected_train_masks: list[np.ndarray] = []
    selected_holdout_masks: list[np.ndarray] = []

    for step in range(1, args.max_gates + 1):
        best = None
        for atom_index, atom in enumerate(atoms):
            if atom_index in selected_atom_indices:
                continue
            train_masks = selected_train_masks + [[field.atoms[atom_index] for field in train]]
            # Transpose list-of-per-field masks back into per-atom lists for metrics.
            candidate_selected = selected_train_masks + [
                [field.atoms[atom_index] for field in train]
            ]
            _hits, _total, _base_hits, base_total = metrics(train, candidate_selected)
            coverage = _total / base_total if base_total else 0.0
            if coverage < args.min_train_coverage:
                continue
            row = (score(train, candidate_selected), atom_index)
            if best is None or row > best:
                best = row

        if best is None:
            print(f"step={step} no_candidate_meets_min_train_coverage")
            break

        (_score, atom_index) = best
        atom = atoms[atom_index]
        selected_atom_indices.append(atom_index)
        selected_train_masks.append([field.atoms[atom_index] for field in train])
        selected_holdout_masks.append([field.atoms[atom_index] for field in holdout])
        print(f"step={step} selected {atom.label}")
        print("  train   " + fmt_metrics(train, selected_train_masks))
        print("  holdout " + fmt_metrics(holdout, selected_holdout_masks))

    print("selected_atoms")
    for atom_index in selected_atom_indices:
        print(f"  {atoms[atom_index].label}")
    print("conclusion=stacked_character_gates_are_holdout_checked_constant_filters")


if __name__ == "__main__":
    main()
