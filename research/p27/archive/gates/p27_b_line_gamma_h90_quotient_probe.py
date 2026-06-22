#!/usr/bin/env python3
"""Explicit H90 quotient probe for the p27 B-line gamma class.

The gamma norm screen showed that gamma^2=v+2 has square norm on each
materialized two-root pair over a fixed (B,u).  This probe builds the
corresponding norm-one quotient data:

    r = (v1+2)/(v2+2)
    h^2 = r

with the involution sending h to 1/h.  It then tests whether quotient
coordinates such as h+1/h or the Cayley parameter expose f4 or a low-degree
relation.  A positive would be a concrete H90 source lead; a negative says the
H90 route needs actual CAS divisor/class work rather than another visible
quotient-coordinate scan.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
from typing import Callable, Optional

from p27_b_line_transition_closure_probe import (
    DEFAULT_FIRST,
    collect_actual_edges,
    load_field,
    transition_roots,
)
from p27_conic_pair_invariant_relation_probe import relation_stats_for_system
from p27_kline_reverse_z_relation_probe import parse_ints
from p27_label2_alpha_branch_recurrence_probe import legendre


AtomFn = Callable[[dict[str, int], int], Optional[int]]


def inv(a: int, p: int) -> Optional[int]:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def sqrt_mod_square(a: int, p: int) -> Optional[int]:
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
        return None
    if p % 4 != 3:
        raise ValueError("sqrt helper expects p = 3 mod 4")
    root = pow(a, (p + 1) // 4, p)
    return root if root * root % p == a else None


def maybe_div(num: int, den: int, p: int) -> Optional[int]:
    iden = inv(den, p)
    if iden is None:
        return None
    return num % p * iden % p


def build_rows(q: int, first: dict) -> tuple[list[dict[str, int]], Counter]:
    first_field = load_field(first, q)
    actual_edges, _actual_by_b, edge_stats = collect_actual_edges(q)
    rows: list[dict[str, int]] = []
    stats: Counter = Counter(edge_stats)

    for fixture_row in first_field["rows"]:
        if str(fixture_row["sign"]) != "plus":
            continue
        B = int(fixture_row["B"]) % q
        A = (B * B - 2) % q
        for raw_u in fixture_row["u_roots"]:
            u = int(raw_u) % q
            actual = sorted(actual_edges.get((B, u), set()))
            generic = sorted(transition_roots(A, u, q))
            if len(actual) != 2 or len(generic) != 4:
                stats["bad_pair_shape"] += 1
                continue
            v0, v1 = actual
            g0 = (v0 + 2) % q
            g1 = (v1 + 2) % q
            r = maybe_div(g0, g1, q)
            if r is None:
                stats["zero_gamma_denominator"] += 1
                continue
            h = sqrt_mod_square(r, q)
            if h is None:
                stats["ratio_not_square"] += 1
                continue
            ih = inv(h, q)
            ir = inv(r, q)
            if ih is None or ir is None:
                stats["zero_h_or_r"] += 1
                continue
            h_sym = (h + ih) % q
            h_anti = (h - ih) % q
            h_sym2 = h_sym * h_sym % q
            h_anti2 = h_anti * h_anti % q
            r_sym = (r + ir) % q
            tau = maybe_div(h - 1, h + 1, q)
            if tau is None:
                stats["tau_denominator_zero"] += 1
                continue
            tau2 = tau * tau % q
            itau2 = inv(tau2, q)
            if itau2 is None:
                stats["tau2_zero"] += 1
                continue
            tau_sym = (tau2 + itau2) % q
            gamma_norm = g0 * g1 % q
            f4 = legendre(g0, q)
            if legendre(g1, q) != f4:
                stats["pair_f4_mismatch"] += 1
            rows.append(
                {
                    "B": B,
                    "A": A,
                    "u": u,
                    "v0": v0,
                    "v1": v1,
                    "v_sum": (v0 + v1) % q,
                    "v_prod": v0 * v1 % q,
                    "gamma_norm": gamma_norm,
                    "r": r,
                    "r_sym": r_sym,
                    "h": h,
                    "h_sym": h_sym,
                    "h_anti": h_anti,
                    "h_sym2": h_sym2,
                    "h_anti2": h_anti2,
                    "tau": tau,
                    "tau2": tau2,
                    "tau_sym": tau_sym,
                    "f4": f4,
                }
            )

    stats["h90_rows"] = len(rows)
    stats["f4_plus"] = sum(1 for row in rows if row["f4"] == 1)
    stats["f4_minus"] = sum(1 for row in rows if row["f4"] == -1)
    return rows, stats


def atoms() -> list[tuple[str, AtomFn]]:
    out: list[tuple[str, AtomFn]] = []

    def add(name: str, fn: AtomFn) -> None:
        out.append((name, fn))

    for key in (
        "B",
        "A",
        "u",
        "v_sum",
        "v_prod",
        "gamma_norm",
        "r",
        "r_sym",
        "h",
        "h_sym",
        "h_anti",
        "h_sym2",
        "h_anti2",
        "tau",
        "tau2",
        "tau_sym",
    ):
        add(key, lambda row, _p, kk=key: row[kk])

    for key in ("r", "h", "h_sym", "tau", "tau2", "tau_sym"):
        for c in (-4, -2, -1, 1, 2, 4):
            add(f"{key}{c:+d}", lambda row, p, kk=key, cc=c: (row[kk] + cc) % p)
    add("B2-4", lambda row, p: (row["B"] * row["B"] - 4) % p)
    add("u2-4", lambda row, p: (row["u"] * row["u"] - 4) % p)
    add("A-2", lambda row, p: (row["A"] - 2) % p)
    add("2-A", lambda row, p: (2 - row["A"]) % p)
    return out


def mask_from_signs(signs: list[int]) -> int:
    mask = 0
    for i, sign in enumerate(signs):
        if sign == -1:
            mask |= 1 << i
    return mask


def popcount(value: int) -> int:
    return bin(value).count("1")


def score_mask(mask: int, target: int, full: int) -> tuple[int, int]:
    matches = popcount(mask ^ target ^ full)
    opposite = popcount((mask ^ full) ^ target ^ full)
    return matches, opposite


def product_screen(rows: list[dict[str, int]], q: int, max_weight: int, keep_best: int) -> tuple[Counter, list[str]]:
    stats: Counter = Counter()
    notes: list[str] = []
    full = (1 << len(rows)) - 1
    target = mask_from_signs([row["f4"] for row in rows])
    atom_masks: list[tuple[str, int]] = []
    for name, fn in atoms():
        signs = []
        zeros = 0
        for row in rows:
            value = fn(row, q)
            if value is None:
                zeros += 1
                signs.append(0)
                continue
            chi = legendre(value, q)
            if chi == 0:
                zeros += 1
            signs.append(chi)
        if zeros:
            stats[f"atom_{name}_zero_or_undefined"] = zeros
            continue
        atom_masks.append((name, mask_from_signs(signs)))

    best: list[tuple[int, int, tuple[str, ...], int]] = []
    exact: list[tuple[int, int, tuple[str, ...], int]] = []
    for weight in range(1, max_weight + 1):
        for combo in combinations(atom_masks, weight):
            names = tuple(name for name, _mask in combo)
            mask = 0
            for _name, atom_mask in combo:
                mask ^= atom_mask
            matches, opposite = score_mask(mask, target, full)
            best_matches = max(matches, opposite)
            polarity = 1 if matches >= opposite else -1
            item = (best_matches, weight, names, polarity)
            best.append(item)
            if best_matches == len(rows):
                exact.append(item)
    best.sort(key=lambda item: (item[0], -item[1]), reverse=True)
    stats["h90_atoms_usable"] = len(atom_masks)
    stats["h90_products_tested"] = len(best)
    stats["h90_exact_products"] = len(exact)
    if best:
        stats["h90_best_matches"] = best[0][0]
        stats["h90_best_match_x1000000"] = best[0][0] * 1_000_000 // len(rows)
        stats["h90_best_weight"] = best[0][1]

    notes.append("  exact_h90_products:")
    if exact:
        for matches, weight, names, polarity in exact[:keep_best]:
            notes.append(f"    weight={weight} polarity={polarity} atoms={' * '.join(names)}")
    else:
        notes.append("    none")
    notes.append("  best_h90_products:")
    for matches, weight, names, polarity in best[:keep_best]:
        notes.append(
            f"    matches={matches}/{len(rows)} polarity={polarity} "
            f"weight={weight} atoms={' * '.join(names)}"
        )
    return stats, notes


def relation_screen(rows: list[dict[str, int]], q: int, degrees: list[int]) -> list[str]:
    systems = {
        "B_rsym": [(row["B"], row["r_sym"]) for row in rows],
        "u_rsym": [(row["u"], row["r_sym"]) for row in rows],
        "B_hsym2": [(row["B"], row["h_sym2"]) for row in rows],
        "u_hsym2": [(row["u"], row["h_sym2"]) for row in rows],
        "B_tau_sym": [(row["B"], row["tau_sym"]) for row in rows],
        "u_tau_sym": [(row["u"], row["tau_sym"]) for row in rows],
        "B_u_hsym2": [(row["B"], row["u"], row["h_sym2"]) for row in rows],
        "B_u_tau_sym": [(row["B"], row["u"], row["tau_sym"]) for row in rows],
    }
    out: list[str] = []
    for name, points in systems.items():
        unique = sorted(set(points))
        stats = relation_stats_for_system(unique, q, degrees)
        out.append(f"  relation_{name}:")
        out.append(f"    rows = {len(points)}")
        out.append(f"    unique = {len(unique)}")
        for degree in degrees:
            prefix = f"deg{degree}"
            out.append(
                "    "
                f"{prefix}: monomials={stats[f'{prefix}_monomials']} "
                f"rank={stats[f'{prefix}_rank']} "
                f"nullity={stats[f'{prefix}_nullity']} "
                f"forced={stats[f'{prefix}_forced_nullity']} "
                f"extra={stats[f'{prefix}_extra_nullity']}"
            )
    return out


def parse_degrees(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def run_field(q: int, first: dict, max_weight: int, keep_best: int, degrees: list[int]) -> None:
    rows, stats = build_rows(q, first)
    stats["h90_ratio_square_fail"] = 0
    stats["rsym_minus_u_identity_fail"] = 0
    stats["hsym2_identity_fail"] = 0
    stats["hsym2_minus_uplus2_identity_fail"] = 0
    stats["hanti2_identity_fail"] = 0
    stats["tau_sym_formula_denominator_zero"] = 0
    stats["tau_sym_formula_fail"] = 0
    for row in rows:
        ih = inv(row["h"], q)
        if ih is None or row["h"] * ih % q != 1:
            stats["h90_inverse_fail"] += 1
        if (row["r_sym"] - row["u"]) % q:
            stats["rsym_minus_u_identity_fail"] += 1
        if (row["h_sym2"] - (row["r_sym"] + 2)) % q:
            stats["hsym2_identity_fail"] += 1
        if (row["h_sym2"] - (row["u"] + 2)) % q:
            stats["hsym2_minus_uplus2_identity_fail"] += 1
        if (row["h_anti2"] - (row["r_sym"] - 2)) % q:
            stats["hanti2_identity_fail"] += 1
        denom = (row["u"] - 2) % q
        if denom == 0:
            stats["tau_sym_formula_denominator_zero"] += 1
        else:
            expected_tau_sym = (2 * (row["u"] + 6) * pow(denom, q - 2, q)) % q
            if (row["tau_sym"] - expected_tau_sym) % q:
                stats["tau_sym_formula_fail"] += 1
    product_stats, product_notes = product_screen(rows, q, max_weight, keep_best)
    stats.update(product_stats)

    print(f"q={q}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")
    for note in product_notes:
        print(note)
    for note in relation_screen(rows, q, degrees):
        print(note)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--first-fixture", type=Path, default=DEFAULT_FIRST)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--keep-best", type=int, default=12)
    parser.add_argument("--degrees", default="2,4,6,8,10")
    args = parser.parse_args()

    first = json.loads(args.first_fixture.read_text())
    degrees = parse_degrees(args.degrees)
    print("p27 B-line gamma H90 quotient probe")
    print("question = do explicit norm-one quotient coordinates expose f4 or a low-degree source?")
    print(f"first_fixture = {args.first_fixture}")
    print(f"max_weight = {args.max_weight}")
    print(f"relation_degrees = {args.degrees}")
    for q in parse_ints(args.small_primes):
        run_field(q, first, args.max_weight, args.keep_best, degrees)
    print("p27_b_line_gamma_h90_quotient_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
