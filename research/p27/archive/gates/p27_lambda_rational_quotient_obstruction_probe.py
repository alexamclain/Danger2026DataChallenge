#!/usr/bin/env python3
"""Rational obstruction to using lambda = -K^2/4 as a p27 source quotient.

The K-line Belyi coordinate lambda identifies K and -K.  Over the algebraic
closure that is a clean normalization, but p27-compatible fields have
chi(-1)=-1.  Since

    K = x([2]P) = ((U^2 - 4)/(2V))^2 on E': V^2 = U^3 + 4U,

every rational doubled K is a square.  Therefore -K is a nonsquare and is not
in the same rational doubled stratum.  This probe records the symbolic identity
and verifies the square-stratum obstruction over the p27 guard fields.
"""

from __future__ import annotations

import argparse
from collections import Counter

import sympy as sp

from p27_eprime_double_kummer_line_probe import kummer_double_x, to_krows
from p27_equotient_2isogeny_line_probe import quotient_rows
from p27_label2_alpha_branch_recurrence_probe import legendre
from p27_reverse_doubling_source_probe import enumerate_small_prime_candidates
from p27_reverse_source_d4_recurrence_probe import quotient_bit_rows_from_candidates


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def roots2(a: int, p: int) -> list[int]:
    a %= p
    if a == 0:
        return [0]
    if legendre(a, p) != 1:
        return []
    r = pow(a, (p + 1) // 4, p) if p % 4 == 3 else None
    if r is None or r * r % p != a:
        for cand in range(p):
            if cand * cand % p == a:
                r = cand
                break
    assert r is not None
    return sorted({r, (-r) % p})


def symbolic_identity() -> dict[str, sp.Expr]:
    u, v = sp.symbols("U V")
    k = (u**2 - 4) ** 2 / (4 * u * (u**2 + 4))
    square_form = ((u**2 - 4) / (2 * v)) ** 2
    diff = sp.factor(sp.together((k - square_form).subs(v**2, u * (u**2 + 4))))
    return {
        "K": sp.factor(sp.together(k)),
        "square_form": sp.factor(sp.together(square_form)),
        "difference_after_Eprime_relation": diff,
    }


def doubled_image_stats(q: int) -> Counter:
    stats: Counter = Counter()
    image: set[int] = set()
    for u in range(q):
        rhs = (u * (u * u + 4)) % q
        for v in roots2(rhs, q):
            if v == 0:
                stats["v_zero_skip"] += 1
                continue
            k = kummer_double_x(u, q)
            if k is None:
                stats["k_undefined_skip"] += 1
                continue
            image.add(k)
            k_chi = legendre(k, q)
            k2p4_chi = legendre((k * k + 4) % q, q)
            if k_chi == 0:
                stats["k_zero"] += 1
            elif k_chi != 1:
                stats["k_square_fail"] += 1
            if k2p4_chi == 0:
                stats["k2p4_zero"] += 1
            elif k2p4_chi != 1:
                stats["k2p4_square_fail"] += 1
    stats["doubled_k_values"] = len(image)
    stats["nonzero_doubled_k_values"] = sum(1 for k in image if k != 0)
    stats["neg_nonzero_k_also_doubled"] = sum(1 for k in image if k != 0 and (-k) % q in image)
    return stats


def selected_row_stats(q: int) -> Counter:
    candidates, enum_stats = enumerate_small_prime_candidates(q)
    d3_rows, d4_rows, quotient_stats = quotient_bit_rows_from_candidates(candidates, q)
    qd3, d3_iso_stats = quotient_rows(d3_rows, q)
    qd4, d4_iso_stats = quotient_rows(d4_rows, q)
    kd3, d3_k_stats = to_krows(qd3, q)
    kd4, d4_k_stats = to_krows(qd4, q)
    stats: Counter = Counter()
    stats.update({f"enum_{key}": value for key, value in enum_stats.items()})
    stats.update({f"quotient_{key}": value for key, value in quotient_stats.items()})
    stats.update({f"d3_eprime_{key}": value for key, value in d3_iso_stats.items()})
    stats.update({f"d4_eprime_{key}": value for key, value in d4_iso_stats.items()})
    stats.update({f"d3_k_{key}": value for key, value in d3_k_stats.items()})
    stats.update({f"d4_k_{key}": value for key, value in d4_k_stats.items()})
    for label, rows in [("d3", kd3), ("d4", kd4)]:
        kset = {row.k for row in rows}
        stats[f"{label}_k_plus"] = sum(1 for row in rows if legendre(row.k, q) == 1)
        stats[f"{label}_k_minus"] = sum(1 for row in rows if legendre(row.k, q) == -1)
        stats[f"{label}_k_zero"] = sum(1 for row in rows if legendre(row.k, q) == 0)
        stats[f"{label}_k2p4_plus"] = sum(1 for row in rows if legendre((row.k * row.k + 4) % q, q) == 1)
        stats[f"{label}_neg_k_present"] = sum(1 for row in rows if (-row.k) % q in kset)
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--small-primes",
        default="607,863,991,1471,1607,1847,1951,1999,2039,2063,2087,2111,2143,2207,2239",
    )
    args = parser.parse_args()

    print("p27 lambda rational quotient obstruction probe")
    data = symbolic_identity()
    print(f"K = {data['K']}")
    print(f"K_square_form = {data['square_form']}")
    print(f"difference_after_Eprime_relation = {data['difference_after_Eprime_relation']}")
    print("consequence = rational doubles on E' have square K")
    print()

    for q in parse_ints(args.small_primes):
        print(f"q={q}:")
        print(f"  q_mod_8 = {q % 8}")
        print(f"  chi_minus_one = {legendre(-1, q)}")
        print(f"  chi_two = {legendre(2, q)}")
        print_counter("  doubled_image_stats", doubled_image_stats(q))
        print_counter("  selected_row_stats", selected_row_stats(q))
    print("p27_lambda_rational_quotient_obstruction_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
