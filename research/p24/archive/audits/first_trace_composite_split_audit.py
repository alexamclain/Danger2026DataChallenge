#!/usr/bin/env python3
"""Composite split-ideal search for the first strict p24 trace.

The first trace has cyclic class group

    h = 2 * 19 * 7335098083,

and the split prime above 2 is a full generator.  Single-prime audits found:

    ell=19  index=19, recovery=2*7335098083;
    ell=107 index=38, recovery=7335098083.

This script searches signed products of small split primes to see whether the
index-38 class can be represented at smaller norm / X0 degree than the single
prime 107, or whether any other formal quotient/recovery tradeoff improves.
It is still only a formal cycle audit; it does not construct the embedded
period quotient.
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari
from sympy.ntheory.modular import crt


P = 10**24 + 7
D_K = -739589633190799177940983
H = 278733727154
GENERATOR_PRIME = 2
CLASS_FACTORS = (2, 19, 7335098083)
TARGET_INDICES = (19, 38, 2 * 19 * 7335098083)


@dataclass(frozen=True)
class PrimeLog:
    ell: int
    log: int
    index: int
    order: int


@dataclass(frozen=True)
class Hit:
    norm: int
    x0_index: int
    log: int
    index: int
    order: int
    signed_terms: tuple[int, ...]


def form_key(pari: Pari, form) -> str:
    return str(pari.qfbred(form))


def inverse_form(pari: Pari, form):
    return pari(f"Qfb({int(form[0])},{-int(form[1])},{int(form[2])})")


def compose(pari: Pari, a, b, nucomp_l: int):
    return pari.qfbred(pari.qfbnucomp(a, b, nucomp_l))


def pow_form(pari: Pari, form, exponent: int, nucomp_l: int):
    return pari.qfbred(pari.qfbnupow(form, int(exponent), nucomp_l))


def bsgs_prime_order_log(pari: Pari, base, target, order: int, nucomp_l: int) -> int:
    if order == 2:
        identity = pow_form(pari, base, 0, nucomp_l)
        return 0 if form_key(pari, target) == form_key(pari, identity) else 1
    m = math.isqrt(order) + 1
    table: dict[str, int] = {}
    cur = pow_form(pari, base, 0, nucomp_l)
    for j in range(m):
        table.setdefault(form_key(pari, cur), j)
        cur = compose(pari, cur, base, nucomp_l)
    step = inverse_form(pari, pow_form(pari, base, m, nucomp_l))
    gamma = target
    for i in range(m + 1):
        key = form_key(pari, gamma)
        if key in table:
            value = i * m + table[key]
            if value < order:
                return value
        gamma = compose(pari, gamma, step, nucomp_l)
    raise RuntimeError(f"log failed for order {order}")


def class_log(pari: Pari, generator, form, nucomp_l: int) -> int:
    residues: list[int] = []
    moduli: list[int] = []
    for q in CLASS_FACTORS:
        base_q = pow_form(pari, generator, H // q, nucomp_l)
        target_q = pow_form(pari, form, H // q, nucomp_l)
        residues.append(bsgs_prime_order_log(pari, base_q, target_q, q, nucomp_l))
        moduli.append(q)
    value, modulus = crt(moduli, residues)
    if int(modulus) != H:
        raise AssertionError((modulus, H))
    return int(value) % H


def gamma0_index_squarefree(norm: int) -> int:
    value = norm
    for prime in sp.factorint(norm):
        value *= prime + 1
        value //= prime
    return int(value)


def prime_logs(prime_bound: int) -> list[PrimeLog]:
    pari = Pari()
    pari.allocatemem(512 * 1024 * 1024)
    nucomp_l = int((abs(D_K) // 4) ** 0.25) + 1
    generator = pari.qfbprimeform(D_K, GENERATOR_PRIME)
    rows: list[PrimeLog] = []
    for ell in sp.primerange(2, prime_bound + 1):
        ell = int(ell)
        if abs(D_K) % ell == 0 or sp.kronecker_symbol(D_K, ell) != 1:
            continue
        form = pari.qfbprimeform(D_K, ell)
        log_value = 1 if ell == GENERATOR_PRIME else class_log(pari, generator, form, nucomp_l)
        index = math.gcd(H, log_value)
        rows.append(PrimeLog(ell, log_value, index, H // index))
    return rows


def search_products(rows: list[PrimeLog], max_factors: int, max_norm: int) -> list[Hit]:
    signed_rows = [(row.ell, row.log) for row in rows] + [(row.ell, (-row.log) % H) for row in rows]
    hits: list[Hit] = []
    seen: set[tuple[int, tuple[int, ...], int]] = set()
    for size in range(1, max_factors + 1):
        for combo in itertools.combinations(signed_rows, size):
            primes = tuple(ell for ell, _log in combo)
            if len(set(primes)) != len(primes):
                continue
            norm = math.prod(primes)
            if norm > max_norm:
                continue
            log_sum = sum(log for _ell, log in combo) % H
            index = math.gcd(H, log_sum)
            order = H // index
            signed_terms = []
            for ell, log_value in combo:
                original = next(row.log for row in rows if row.ell == ell)
                signed_terms.append(ell if log_value == original else -ell)
            signed_tuple = tuple(sorted(signed_terms, key=abs))
            key = (index, tuple(sorted(abs(x) for x in signed_tuple)), log_sum)
            if key in seen:
                continue
            seen.add(key)
            hits.append(
                Hit(
                    norm=norm,
                    x0_index=gamma0_index_squarefree(norm),
                    log=log_sum,
                    index=index,
                    order=order,
                    signed_terms=signed_tuple,
                )
            )
    return sorted(hits, key=lambda hit: (hit.index, hit.x0_index, hit.norm, len(hit.signed_terms)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=300)
    ap.add_argument("--max-factors", type=int, default=4)
    ap.add_argument("--max-norm", type=int, default=20000)
    ap.add_argument("--show", type=int, default=12)
    args = ap.parse_args()

    sqrt_p = math.isqrt(P)
    rows = prime_logs(args.prime_bound)
    hits = search_products(rows, args.max_factors, args.max_norm)

    print("first-trace composite split-ideal audit")
    print(f"p={P}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"D_K={D_K}")
    print(f"class_number={H}")
    print(f"class_number_factor={sp.factorint(H)}")
    print(f"generator_prime={GENERATOR_PRIME}")
    print(f"prime_bound={args.prime_bound}")
    print(f"split_primes={len(rows)}")
    print(f"max_factors={args.max_factors}")
    print(f"max_norm={args.max_norm}")
    print()

    print("single_prime_logs")
    print("  ell log index order x0_degree seeded_proxy_over_sqrt")
    for row in rows:
        if row.ell <= 300 and row.index in {1, 2, 19, 38}:
            print(
                f"  {row.ell:5d} {row.log:15d} {row.index:8d} {row.order:15d} "
                f"{row.ell + 1:9d} {(row.ell + 1) * row.order / sqrt_p:22.6e}"
            )
    print()

    for index in (19, 38):
        selected = [hit for hit in hits if hit.index == index]
        print(f"best_products_index_{index}")
        print("  norm x0_index order x0_index*order/sqrt signed_terms log")
        for hit in selected[: args.show]:
            print(
                f"  {hit.norm:8d} {hit.x0_index:8d} {hit.order:15d} "
                f"{hit.x0_index * hit.order / sqrt_p:22.6e} "
                f"{hit.signed_terms!s:24s} {hit.log}"
            )
        if not selected:
            print("  none")
        print()

    print("interpretation")
    print("  index_19_is_the_order19_theorem_toy=1")
    print("  index_38_halves_recovery_but_still_has_recovery_7335098083=1")
    print("  composite_products_may_reduce_correspondence_degree_constants=1")
    print("  embedded_period_projector_problem_remains=1")
    print("conclusion=reported_first_trace_composite_split_products")


if __name__ == "__main__":
    main()
