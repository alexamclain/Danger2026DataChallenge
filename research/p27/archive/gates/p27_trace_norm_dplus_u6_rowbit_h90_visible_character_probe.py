#!/usr/bin/env python3
"""Visible H90-character screen for the Dplus U6 row bit.

The H90 point-fiber probe shows that the row bit is uniform over rational
E_h90, domain-spin, and A_eta point fibers in small fields.  This probe asks
the next cheap question: is that uniform sign a visible character of the
available H90 coordinates?

It tests product characters on four levels:

    E_h90:       (t,w)
    Z:           (t,w,z), z^2 = Fspin
    Aeta_plus:   (t,w,z,rho), rho^2 = A_eta for eta=+1
    Aeta_minus:  (t,w,z,rho), rho^2 = A_eta for eta=-1

An exact product would be a concrete source handle.  A negative result keeps
the row bit in the non-visible Prym/theta/CAS lane.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import combinations

from p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_probe import (
    a_from_t,
    chi,
    h90_values,
    parse_fields,
    roots_square,
    row_signs_for_t,
    sign_name,
    x_from_t,
)


LEVELS = ("E", "Z", "Aeta_plus", "Aeta_minus")


@dataclass(frozen=True)
class ComboScore:
    level: str
    combo: tuple[str, ...]
    polarity: int
    matches: int
    total: int
    per_field: tuple[tuple[int, int, int], ...]


def normalize_sign(values: list[int]) -> int | None:
    signs = {value for value in values if value in (-1, 1)}
    if len(signs) == 1:
        return signs.pop()
    return None


def feature_values(q: int, t: int, w: int | None = None, z: int | None = None, rho: int | None = None) -> dict[str, int]:
    B, C, Fspin, Ktrace = h90_values(t, q)
    R = (t * t - 2 * t - 1) % q
    A = a_from_t(t, q)
    X = x_from_t(t, q)
    raw: dict[str, int] = {
        "t": t,
        "t_minus_1": t - 1,
        "t_plus_1": t + 1,
        "t2_minus_1": t * t - 1,
        "B": B,
        "C": C,
        "R": R,
        "B*C": B * C,
        "B*R": B * R,
        "C*R": C * R,
        "Fspin": Fspin,
        "Ktrace": Ktrace,
        "A": A,
        "A_minus_2": A - 2,
        "A_plus_2": A + 2,
        "X": X,
        "X_minus_2": X - 2,
        "X_plus_2": X + 2,
    }
    if w is not None:
        raw.update(
            {
                "w": w,
                "w_plus_t": w + t,
                "w_minus_t": w - t,
                "w_plus_B": w + B,
                "w_minus_B": w - B,
                "w_plus_C": w + C,
                "w_minus_C": w - C,
                "w_plus_R": w + R,
                "w_minus_R": w - R,
            }
        )
    if z is not None:
        raw.update(
            {
                "z": z,
                "z_plus_t": z + t,
                "z_minus_t": z - t,
                "z_plus_w": z + (w or 0),
                "z_minus_w": z - (w or 0),
                "z_plus_B": z + B,
                "z_minus_B": z - B,
                "z_plus_C": z + C,
                "z_minus_C": z - C,
                "z_plus_R": z + R,
                "z_minus_R": z - R,
            }
        )
    if rho is not None:
        raw.update(
            {
                "rho": rho,
                "rho_plus_t": rho + t,
                "rho_minus_t": rho - t,
                "rho_plus_w": rho + (w or 0),
                "rho_minus_w": rho - (w or 0),
                "rho_plus_z": rho + (z or 0),
                "rho_minus_z": rho - (z or 0),
                "rho_plus_B": rho + B,
                "rho_minus_B": rho - B,
                "rho_plus_C": rho + C,
                "rho_minus_C": rho - C,
                "rho_plus_R": rho + R,
                "rho_minus_R": rho - R,
            }
        )
    return {name: chi(value, q) for name, value in raw.items()}


def add_row(rows: dict[str, list[dict[str, int]]], level: str, q: int, target: int, features: dict[str, int]) -> None:
    row = {"q": q, "target": target}
    row.update(features)
    rows[level].append(row)


def collect_rows(fields: list[int], materialization_filters: bool) -> tuple[dict[str, list[dict[str, int]]], Counter[str]]:
    rows = {level: [] for level in LEVELS}
    stats: Counter[str] = Counter()
    for q in fields:
        for t in range(1, q):
            signs = row_signs_for_t(t, q, materialization_filters)
            target = normalize_sign(signs)
            if target is None:
                stats[f"q{q}_mixed_or_empty_t"] += 1
                continue
            B, C, Fspin, Ktrace = h90_values(t, q)
            w_roots = roots_square(Ktrace, q)
            if not w_roots:
                stats[f"q{q}_uniform_t_without_E"] += 1
                continue
            for w in w_roots:
                add_row(rows, "E", q, target, feature_values(q, t, w=w))
                z_roots = roots_square(Fspin, q)
                if not z_roots:
                    stats[f"q{q}_E_without_Z"] += 1
                    continue
                for z in z_roots:
                    add_row(rows, "Z", q, target, feature_values(q, t, w=w, z=z))
                    for eta, level in ((1, "Aeta_plus"), (-1, "Aeta_minus")):
                        Ueta = 2 * t % q * t % q * (t - 1) % q * B % q * B % q * ((eta * w + C) % q) % q
                        Weta = (t - 1) % q * B % q * ((4 * t % q * t % q * t + eta * B % q * w) % q) % q
                        Aeta = (Ueta + z * Weta) % q
                        rho_roots = roots_square(Aeta, q)
                        if not rho_roots:
                            stats[f"q{q}_{level}_missing_rho"] += 1
                            continue
                        for rho in rho_roots:
                            add_row(rows, level, q, target, feature_values(q, t, w=w, z=z, rho=rho))
    for level, level_rows in rows.items():
        stats[f"{level}_rows"] = len(level_rows)
    return rows, stats


def active_features(rows: list[dict[str, int]]) -> tuple[list[str], Counter[str]]:
    stats: Counter[str] = Counter()
    if not rows:
        return [], stats
    names = sorted(name for name in rows[0] if name not in ("q", "target"))
    active = []
    for name in names:
        counts = Counter(row[name] for row in rows)
        for value, count in counts.items():
            stats[f"{name}_{sign_name(value)}"] = count
        if counts.get(0, 0):
            stats["features_with_zero"] += 1
            continue
        if len(counts) <= 1:
            stats["constant_features"] += 1
            continue
        active.append(name)
    stats["active_features"] = len(active)
    return active, stats


def iter_combos(features: list[str], max_weight: int):
    for weight in range(1, min(max_weight, len(features)) + 1):
        yield from combinations(features, weight)


def score_combo(level: str, rows: list[dict[str, int]], combo: tuple[str, ...], polarity: int) -> ComboScore:
    matches = 0
    per_field_counts: dict[int, list[int]] = {}
    for row in rows:
        value = polarity
        for name in combo:
            value *= row[name]
        ok = int(value == row["target"])
        matches += ok
        bucket = per_field_counts.setdefault(row["q"], [0, 0])
        bucket[0] += ok
        bucket[1] += 1
    return ComboScore(
        level=level,
        combo=combo,
        polarity=polarity,
        matches=matches,
        total=len(rows),
        per_field=tuple((q, counts[0], counts[1]) for q, counts in sorted(per_field_counts.items())),
    )


def combo_label(score: ComboScore) -> str:
    return ("" if score.polarity == 1 else "-") + "*".join(score.combo)


def screen_level(level: str, rows: list[dict[str, int]], max_weight: int) -> tuple[Counter[str], list[ComboScore], list[ComboScore]]:
    features, profile = active_features(rows)
    scores: list[ComboScore] = []
    exact: list[ComboScore] = []
    for combo in iter_combos(features, max_weight):
        for polarity in (1, -1):
            score = score_combo(level, rows, combo, polarity)
            scores.append(score)
            if score.matches == score.total:
                exact.append(score)
    scores.sort(key=lambda score: (score.matches, -len(score.combo)), reverse=True)
    profile["features_screened"] = len(features)
    profile["combos_screened"] = len(scores)
    profile["exact_combos"] = len(exact)
    if scores:
        profile["best_matches"] = scores[0].matches
        profile["best_total"] = scores[0].total
        profile["best_match_x1000000"] = scores[0].matches * 1_000_000 // scores[0].total
    return profile, exact, scores


def print_counter(label: str, stats: Counter[str]) -> None:
    print(f"{label}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def print_scores(label: str, scores: list[ComboScore], keep: int) -> None:
    print(f"{label}:")
    if not scores:
        print("  none")
        return
    for score in scores[:keep]:
        fields = ", ".join(f"q{q}:{hit}/{total}" for q, hit, total in score.per_field)
        print(
            "  "
            f"combo={combo_label(score)} matches={score.matches}/{score.total} "
            f"fields=[{fields}]"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="71,167,199,263,607")
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--include-bare", action="store_true")
    args = parser.parse_args()

    fields = parse_fields(args.fields)
    print("p27 trace/norm Dplus U6 row-bit H90 visible-character probe")
    print("question = is the H90 point-fiber row bit a visible character on E/Z/Aeta coordinates?")
    print(f"fields = {','.join(str(q) for q in fields)}")
    print(f"max_weight = {args.max_weight}")

    for materialization_filters in ([True, False] if args.include_bare else [True]):
        print(f"materialization_filters = {int(materialization_filters)}")
        rows, collect_stats = collect_rows(fields, materialization_filters)
        print_counter("collection", collect_stats)
        for level in LEVELS:
            profile, exact, scores = screen_level(level, rows[level], args.max_weight)
            print_counter(f"{level}_profile", profile)
            print_scores(f"{level}_exact_combos", exact, args.top)
            print_scores(f"{level}_best_combos", scores, args.top)

    print("verdict:")
    print("  exact visible character promotes a source candidate")
    print("  no exact character keeps the row bit in Prym/theta/CAS territory")
    print("p27_trace_norm_dplus_u6_rowbit_h90_visible_character_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
