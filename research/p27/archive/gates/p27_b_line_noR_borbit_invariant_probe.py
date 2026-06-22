#!/usr/bin/env python3
"""Trace/norm invariant screen for the no-R B-orbit mechanism.

The no-R coordinate-degree profile split the cover into quadratic fixed-B
fiber mechanisms and cubic/quadratic B-orbit mechanisms.  The fixed-B side now
has named norm classes; this probe asks the matching B-orbit question:

  * are gamma signs uniform on Frobenius B-orbits?
  * do orbit invariants such as Tr(B), Norm(B), or the orbit discriminant
    visibly carry gamma?
  * is there a cheap base-field character law worth turning into a sampler?

This is a finite-field falsifier for visible orbit-coordinate laws, not a
substitute for normalizing the no-R cover.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations

from p27_b_line_gamma_extension_count_probe import GF, parse_field_specs
from p27_b_line_noR_coordinate_degree_probe import element_degree, enumerate_points, lcm
from p27_b_line_noR_fixedB_character_screen import base_value, legendre_base
from p27_b_line_noR_quadratic_subcover_classifier import classify


def frobenius_orbit(field: GF, value: int) -> tuple[int, ...]:
    orbit: list[int] = []
    cur = value
    while cur not in orbit:
        orbit.append(cur)
        cur = field.pow(cur, field.p)
    return tuple(sorted(orbit))


def base_int(field: GF, value: int) -> int:
    out = base_value(field, value)
    if out is None:
        raise ValueError(f"value is not in GF({field.p})")
    return out


def add_many(field: GF, values: list[int]) -> int:
    out = 0
    for value in values:
        out = field.add(out, value)
    return out


def mul_many(field: GF, values: tuple[int, ...]) -> int:
    out = 1
    for value in values:
        out = field.mul(out, value)
    return out


def elementary_symmetric(field: GF, orbit: tuple[int, ...]) -> tuple[int, ...]:
    values = list(orbit)
    out: list[int] = []
    for degree in range(1, len(values) + 1):
        terms = [mul_many(field, tuple(combo)) for combo in combinations(values, degree)]
        out.append(base_int(field, add_many(field, terms)))
    return tuple(out)


def cubic_discriminant(e1: int, e2: int, e3: int, p: int) -> int:
    # Discriminant of z^3 - e1*z^2 + e2*z - e3.
    a = (-e1) % p
    b = e2 % p
    c = (-e3) % p
    return (a * a * b * b - 4 * b**3 - 4 * a**3 * c - 27 * c * c + 18 * a * b * c) % p


def orbit_rows(field: GF) -> list[dict[str, object]]:
    by_orbit: defaultdict[tuple[int, ...], Counter] = defaultdict(Counter)
    b_signatures: defaultdict[tuple[int, ...], dict[int, Counter]] = defaultdict(lambda: defaultdict(Counter))
    norm_chi_by_orbit: defaultdict[tuple[int, ...], Counter] = defaultdict(Counter)

    for x, w, t, beta, bline, x5, unext, selector in enumerate_points(field):
        degrees = {
            "X": element_degree(field, x),
            "W": element_degree(field, w),
            "T": element_degree(field, t),
            "beta": element_degree(field, beta),
            "B": element_degree(field, bline),
            "x5": element_degree(field, x5),
            "U": element_degree(field, unext),
            "selector": element_degree(field, selector),
        }
        point_degree = lcm(list(degrees.values()))
        gamma_chi = field.legendre(selector)
        cls = classify(degrees, point_degree, gamma_chi)
        if cls != "B_orbit":
            continue

        orbit = frobenius_orbit(field, bline)
        by_orbit[orbit]["points"] += 1
        by_orbit[orbit][f"gamma_{gamma_chi}"] += 1
        b_signatures[orbit][bline][f"gamma_{gamma_chi}"] += 1
        b_signatures[orbit][bline]["points"] += 1

        norm_selector = field.pow(selector, (field.q - 1) // (field.p - 1)) if selector else 0
        norm_selector_base = base_value(field, norm_selector)
        if norm_selector_base is None:
            by_orbit[orbit]["nonbase_norm_selector"] += 1
        else:
            norm_chi = legendre_base(norm_selector_base, field.p)
            norm_chi_by_orbit[orbit][f"norm_chi_{norm_chi}"] += 1
            if norm_chi != gamma_chi:
                by_orbit[orbit]["gamma_norm_mismatch"] += 1

    rows: list[dict[str, object]] = []
    for orbit, counts in sorted(by_orbit.items()):
        invariants = elementary_symmetric(field, orbit)
        if len(invariants) == 2:
            e1, e2 = invariants
            discr = (e1 * e1 - 4 * e2) % field.p
        elif len(invariants) == 3:
            discr = cubic_discriminant(invariants[0], invariants[1], invariants[2], field.p)
        else:
            discr = 0
        signature_set = {
            tuple(sorted(row.items()))
            for row in b_signatures[orbit].values()
        }
        rows.append(
            {
                "orbit": orbit,
                "degree": len(orbit),
                "invariants": invariants,
                "discriminant": discr,
                "points": counts["points"],
                "gamma_minus": counts["gamma_-1"],
                "gamma_zero": counts["gamma_0"],
                "gamma_plus": counts["gamma_1"],
                "gamma_norm_mismatch": counts["gamma_norm_mismatch"],
                "norm_conflicts": max(0, len([k for k in norm_chi_by_orbit[orbit] if k.startswith("norm_chi_")]) - 1),
                "b_signature_count": len(signature_set),
            }
        )
    return rows


def target_mask(rows: list[dict[str, object]], mode: str) -> int:
    mask = 0
    for idx, row in enumerate(rows):
        plus = int(row["gamma_plus"])
        minus = int(row["gamma_minus"])
        points = int(row["points"])
        if mode == "gamma_presence":
            active = plus > 0
        elif mode == "gamma_full":
            active = plus == points and points > 0
        elif mode == "gamma_majority":
            active = plus > minus
        else:
            raise ValueError(mode)
        if active:
            mask |= 1 << idx
    return mask


def mask_from_values(rows: list[dict[str, object]], p: int, values: list[int]) -> int | None:
    mask = 0
    for idx, value in enumerate(values):
        chi = legendre_base(value, p)
        if chi == 0:
            return None
        if chi == 1:
            mask |= 1 << idx
    return mask


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def popcount(a: int) -> int:
    return bin(a).count("1")


def screen_atoms(rows: list[dict[str, object]], p: int, target: int) -> tuple[Counter, tuple[str, int] | None]:
    stats: Counter = Counter()
    best: tuple[str, int] | None = None

    def consider(label: str, values: list[int]) -> None:
        nonlocal best
        mask = mask_from_values(rows, p, values)
        if mask is None:
            stats["zero_skip"] += 1
            return
        stats["tested"] += 1
        all_mask = (1 << len(rows)) - 1
        for candidate_label, candidate in ((label, mask), (f"-{label}", mask ^ all_mask)):
            dist = hamming(candidate, target)
            if best is None or dist < best[1]:
                best = (candidate_label, dist)

    max_degree = max(int(row["degree"]) for row in rows) if rows else 0
    for idx in range(max_degree):
        consider(f"e{idx + 1}", [int(row["invariants"][idx]) for row in rows])
        consider(f"e{idx + 1}+1", [(int(row["invariants"][idx]) + 1) % p for row in rows])
        consider(f"e{idx + 1}-1", [(int(row["invariants"][idx]) - 1) % p for row in rows])
        consider(f"e{idx + 1}+2", [(int(row["invariants"][idx]) + 2) % p for row in rows])
        consider(f"e{idx + 1}-2", [(int(row["invariants"][idx]) - 2) % p for row in rows])
    consider("disc", [int(row["discriminant"]) for row in rows])
    return stats, best


def screen_linear(rows: list[dict[str, object]], p: int, target: int, max_rows: int = 400) -> tuple[Counter, tuple[str, int] | None]:
    stats: Counter = Counter()
    best: tuple[str, int] | None = None
    if not rows or len(rows) > max_rows:
        stats["skipped_row_count"] = len(rows)
        return stats, best

    dim = max(int(row["degree"]) for row in rows)
    vectors = [tuple(int(v) for v in row["invariants"]) for row in rows]
    all_mask = (1 << len(rows)) - 1

    # Normalize by taking the first nonzero coefficient as 1 to avoid
    # rechecking scalar multiples of the same character.
    coeffs: list[tuple[int, ...]] = []
    for pivot in range(dim + 1):
        prefix = [0] * pivot
        if pivot == dim:
            coeffs.append(tuple(prefix + [1]))
            continue
        suffix_len = dim - pivot
        for tail in range(p**suffix_len):
            raw = []
            x = tail
            for _ in range(suffix_len):
                raw.append(x % p)
                x //= p
            coeffs.append(tuple(prefix + [1] + raw))

    for coeff in coeffs:
        values = []
        for vector in vectors:
            value = coeff[-1]
            for c, v in zip(coeff[:-1], vector):
                value += c * v
            values.append(value % p)
        mask = mask_from_values(rows, p, values)
        if mask is None:
            stats["zero_skip"] += 1
            continue
        stats["tested"] += 1
        label = "linear(" + ",".join(str(c) for c in coeff) + ")"
        for candidate_label, candidate in ((label, mask), (f"-{label}", mask ^ all_mask)):
            dist = hamming(candidate, target)
            if best is None or dist < best[1]:
                best = (candidate_label, dist)
    return stats, best


def run_field(p: int, n: int) -> None:
    field = GF(p, n)
    rows = orbit_rows(field)
    by_degree: defaultdict[int, list[dict[str, object]]] = defaultdict(list)
    stats: Counter = Counter()
    summary: Counter = Counter()
    invariant_chi_summary: Counter = Counter()

    for row in rows:
        degree = int(row["degree"])
        invariants = tuple(int(v) for v in row["invariants"])
        invariant_chis = tuple(legendre_base(v, p) for v in invariants)
        disc_chi = legendre_base(int(row["discriminant"]), p)
        by_degree[degree].append(row)
        stats["orbits"] += 1
        stats[f"degree_{degree}_orbits"] += 1
        stats["points"] += int(row["points"])
        stats["gamma_norm_mismatch"] += int(row["gamma_norm_mismatch"])
        stats["norm_conflict_orbits"] += int(int(row["norm_conflicts"]) > 0)
        stats["b_signature_mismatch_orbits"] += int(int(row["b_signature_count"]) > 1)
        summary[(degree, int(row["points"]), int(row["gamma_minus"]), int(row["gamma_zero"]), int(row["gamma_plus"]))] += 1
        invariant_chi_summary[(degree, invariant_chis, disc_chi)] += 1

    print(f"GF({p}^{n}) q={field.q}")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    print("  orbit_summary_top:")
    print("    columns = degree points gamma- gamma0 gamma+")
    for vector, count in summary.most_common(16):
        print(f"    {vector} = {count}")
    print("  invariant_chi_summary_top:")
    print("    columns = degree chi(e1..ed) chi(discriminant)")
    for vector, count in invariant_chi_summary.most_common(16):
        print(f"    {vector} = {count}")

    for degree in sorted(by_degree):
        degree_rows = by_degree[degree]
        print(f"  degree_{degree}_screens:")
        for mode in ("gamma_presence", "gamma_full", "gamma_majority"):
            target = target_mask(degree_rows, mode)
            active = popcount(target)
            print(f"    target {mode}: active={active}/{len(degree_rows)}")
            if active in (0, len(degree_rows)):
                print("      trivial_target = true")
                continue
            atom_stats, atom_best = screen_atoms(degree_rows, p, target)
            linear_stats, linear_best = screen_linear(degree_rows, p, target)
            atom_label = atom_best[0] if atom_best else "none"
            atom_dist = atom_best[1] if atom_best else -1
            linear_label = linear_best[0] if linear_best else "none"
            linear_dist = linear_best[1] if linear_best else -1
            print(
                f"      atoms: tested={atom_stats['tested']} zero_skip={atom_stats['zero_skip']} "
                f"best={atom_label} dist={atom_dist}"
            )
            if linear_stats["skipped_row_count"]:
                print(f"      linear: skipped_row_count={linear_stats['skipped_row_count']}")
            else:
                print(
                    f"      linear: tested={linear_stats['tested']} zero_skip={linear_stats['zero_skip']} "
                    f"best={linear_label} dist={linear_dist}"
                )
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fields", default="23^2,71^2,103^2,7^3,23^3")
    args = parser.parse_args()

    print("p27 B-line no-R B-orbit invariant probe")
    print("question = do trace/norm/discriminant orbit characters carry gamma?")
    print(f"fields = {args.fields}")
    print()
    for p, n in parse_field_specs(args.fields):
        run_field(p, n)
    print("p27_b_line_noR_borbit_invariant_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
