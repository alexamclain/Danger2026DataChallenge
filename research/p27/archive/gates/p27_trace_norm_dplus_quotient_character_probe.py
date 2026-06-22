#!/usr/bin/env python3
"""Character screen on the natural Dplus quotient conic.

The symmetry probe shows that Dplus is invariant under z -> -z and under

    tau: t -> -1/t, z -> +/- z/t^3, w -> -w/t^2.

The visible tau quotient has coordinates

    a = t - 1/t
    g = w/t
    a^2 + g^2 = 4.

This probe checks two things:
  1. Dplus is constant on the finite-field fibers of (a,g).
  2. The descended class is or is not a tiny product of natural characters on
     the conic/its rational parameter.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import importlib.util
from pathlib import Path
import sys


def load_symmetry_module():
    path = Path(__file__).with_name("p27_trace_norm_dplus_symmetry_probe.py")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sym = load_symmetry_module()


def inv(a: int, q: int) -> int | None:
    a %= q
    if a == 0:
        return None
    return pow(a, q - 2, q)


def balanced(v: int, q: int) -> int:
    v %= q
    if v > q // 2:
        return v - q
    return v


def quotient_key(row: sym.Row, q: int) -> tuple[int, int] | None:
    inv_t = inv(row.t, q)
    if inv_t is None:
        return None
    a = (row.t - inv_t) % q
    g = row.w * inv_t % q
    if (a * a + g * g - 4) % q != 0:
        raise RuntimeError("quotient conic relation failed")
    return a, g


def quotient_rows(q: int) -> tuple[list[dict[str, int]], Counter[str]]:
    groups: defaultdict[tuple[int, int], Counter[int]] = defaultdict(Counter)
    source_rows = sym.collect_rows(q)
    stats: Counter[str] = Counter()
    for row in source_rows:
        key = quotient_key(row, q)
        if key is None:
            stats["missing_key"] += 1
            continue
        groups[key][row.dplus] += 1
    out: list[dict[str, int]] = []
    for (a, g), signs in groups.items():
        total = sum(signs.values())
        stats["quotient_points"] += 1
        stats[f"fiber_size_{total}"] += 1
        if len(signs) != 1:
            stats["fiber_conflicts"] += 1
            continue
        dplus = next(iter(signs))
        m = None
        denom = (a - 2) % q
        if denom != 0:
            m = g * pow(denom, q - 2, q) % q
        out.append({"a": a, "g": g, "m": -1 if m is None else m, "dplus": dplus})
    stats["source_rows"] = len(source_rows)
    stats["usable_quotient_rows"] = len(out)
    stats["dplus_+1"] = sum(1 for row in out if row["dplus"] == 1)
    stats["dplus_-1"] = sum(1 for row in out if row["dplus"] == -1)
    return out, stats


def atom_values(row: dict[str, int], q: int) -> dict[str, int]:
    a = row["a"]
    g = row["g"]
    m_raw = row["m"]
    values: dict[str, int] = {
        "a": a,
        "g": g,
        "a+1": a + 1,
        "a-1": a - 1,
        "a+2": a + 2,
        "a-2": a - 2,
        "g+1": g + 1,
        "g-1": g - 1,
        "g+2": g + 2,
        "g-2": g - 2,
        "a+g": a + g,
        "a-g": a - g,
        "a+g+1": a + g + 1,
        "a+g-1": a + g - 1,
        "a-g+1": a - g + 1,
        "a-g-1": a - g - 1,
        "a2+1": a * a + 1,
        "a2-1": a * a - 1,
        "g2+1": g * g + 1,
        "g2-1": g * g - 1,
        "ag+1": a * g + 1,
        "ag-1": a * g - 1,
    }
    if m_raw != -1:
        m = m_raw
        values.update(
            {
                "m": m,
                "m+1": m + 1,
                "m-1": m - 1,
                "m+2": m + 2,
                "m-2": m - 2,
                "m2+1": m * m + 1,
                "m2-1": m * m - 1,
                "m2+2": m * m + 2,
                "m2-2": m * m - 2,
                "m2+m+1": m * m + m + 1,
                "m2-m+1": m * m - m + 1,
            }
        )
    return {name: value % q for name, value in values.items()}


def eval_combo(row: dict[str, int], q: int, combo: tuple[str, ...]) -> int:
    values = atom_values(row, q)
    sign = 1
    for name in combo:
        value = values.get(name)
        if value is None:
            return 0
        chi = sym.leg(value, q)
        if chi == 0:
            return 0
        sign *= chi
    return sign


def score_combo(rows: list[dict[str, int]], q: int, combo: tuple[str, ...]) -> tuple[int, int, int, int]:
    covered = 0
    plus_match = 0
    minus_match = 0
    for row in rows:
        sign = eval_combo(row, q, combo)
        if sign == 0:
            continue
        covered += 1
        if sign == row["dplus"]:
            plus_match += 1
        if -sign == row["dplus"]:
            minus_match += 1
    best = max(plus_match, minus_match)
    polarity = 1 if plus_match >= minus_match else -1
    return covered, best, polarity, plus_match - minus_match


def all_atom_names(rows: list[dict[str, int]], q: int) -> list[str]:
    names: set[str] = set()
    for row in rows:
        names.update(atom_values(row, q))
    return sorted(names)


def run_field(q: int, max_weight: int, min_coverage: float) -> tuple[list[dict[str, int]], Counter[str], list[tuple]]:
    rows, stats = quotient_rows(q)
    atoms = all_atom_names(rows, q)
    stats["atom_count"] = len(atoms)
    scored: list[tuple] = []
    for weight in range(1, max_weight + 1):
        for combo in combinations(atoms, weight):
            covered, best, polarity, delta = score_combo(rows, q, combo)
            if not rows or covered / len(rows) < min_coverage:
                continue
            scored.append((best / covered if covered else 0.0, covered, weight, polarity, combo, delta))
    scored.sort(reverse=True, key=lambda item: (item[0], item[1], -item[2], item[4]))
    return rows, stats, scored


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qs", default="607,1607,1847,2087")
    parser.add_argument("--max-weight", type=int, default=3)
    parser.add_argument("--min-coverage", type=float, default=0.98)
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args()

    qs = [int(part) for part in args.qs.split(",") if part]
    print("p27 trace/norm Dplus quotient character probe")
    print("quotient = a=t-1/t, g=w/t, a^2+g^2=4")
    print(f"max_weight = {args.max_weight}")
    print(f"min_coverage = {args.min_coverage}")

    field_results: dict[int, tuple[list[dict[str, int]], Counter[str], list[tuple]]] = {}
    for q in qs:
        rows, stats, scored = run_field(q, args.max_weight, args.min_coverage)
        field_results[q] = (rows, stats, scored)
        print(f"q{q}_sample:")
        for key in sorted(stats):
            print(f"  {key} = {stats[key]}")
        print(f"q{q}_top:")
        for rank, (score, covered, weight, polarity, combo, delta) in enumerate(scored[: args.top], start=1):
            print(
                "  "
                f"rank={rank} score={score:.9f} covered={covered} "
                f"weight={weight} polarity={polarity:+d} delta={delta} combo={','.join(combo)}"
            )

    if len(qs) >= 2:
        train_q = qs[0]
        heldout_qs = qs[1:]
        _train_rows, _train_stats, train_scored = field_results[train_q]
        print(f"train_q = {train_q}")
        print("heldout_scores:")
        for rank, (score, _covered, weight, polarity, combo, _delta) in enumerate(train_scored[: args.top], start=1):
            combo_scores = []
            for q in heldout_qs:
                rows, _stats, _scored = field_results[q]
                covered, best, _pol, delta = score_combo(rows, q, combo)
                # Keep the train polarity, not the heldout-best polarity.
                fixed_match = 0
                for row in rows:
                    sign = eval_combo(row, q, combo)
                    if sign != 0 and polarity * sign == row["dplus"]:
                        fixed_match += 1
                fixed_score = fixed_match / covered if covered else 0.0
                combo_scores.append(f"q{q}:fixed={fixed_score:.9f}:best={best / covered if covered else 0.0:.9f}:covered={covered}:delta={delta}")
            print(
                "  "
                f"rank={rank} train_score={score:.9f} weight={weight} "
                f"polarity={polarity:+d} combo={','.join(combo)} {' '.join(combo_scores)}"
            )

    print("p27_trace_norm_dplus_quotient_character_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
