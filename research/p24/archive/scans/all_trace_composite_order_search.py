#!/usr/bin/env python3
"""Composite split-ideal order search for all strict p24 CM targets.

This is a sign/product search that does not assume the class group is cyclic.
For each strict trace it collects small split prime forms, composes signed
squarefree products, computes the class order of the product, and reports the
best quotient/recovery tradeoffs.

The goal is to catch formal split-cycle targets missed by single-prime scans,
especially for the middle noncyclic target.
"""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari


P = 10**24 + 7
TRACES = (1020608380936, -78903246840, -1178414874616)


@dataclass(frozen=True)
class Target:
    trace: int
    D_K: int
    h: int
    group: tuple[int, ...]


@dataclass(frozen=True)
class SplitForm:
    ell: int
    form: object
    inv_form: object


@dataclass(frozen=True)
class Hit:
    trace: int
    D_K: int
    h: int
    group: tuple[int, ...]
    norm: int
    x0_index: int
    order: int
    index: int
    signed_terms: tuple[int, ...]


def squarefree_part(n: int) -> int:
    out = 1
    for q, e in sp.factorint(abs(n)).items():
        if e & 1:
            out *= int(q)
    return out


def fundamental_discriminant_from_trace(trace: int) -> int:
    delta = trace * trace - 4 * P
    sf = squarefree_part(delta)
    d = -sf
    return d if d % 4 == 1 else 4 * d


def exact_targets(pari: Pari) -> list[Target]:
    out: list[Target] = []
    for trace in TRACES:
        D_K = fundamental_discriminant_from_trace(trace)
        data = pari.quadclassunit(D_K)
        out.append(Target(trace, D_K, int(data[0]), tuple(int(x) for x in list(data[1]))))
    return out


def form_key(pari: Pari, form) -> str:
    return str(pari.qfbred(form))


def inverse_form(pari: Pari, form):
    return pari(f"Qfb({int(form[0])},{-int(form[1])},{int(form[2])})")


def compose(pari: Pari, a, b, nucomp_l: int):
    return pari.qfbred(pari.qfbnucomp(a, b, nucomp_l))


def pow_form(pari: Pari, form, exponent: int, nucomp_l: int):
    return pari.qfbred(pari.qfbnupow(form, int(exponent), nucomp_l))


def principal_form(pari: Pari, D_K: int):
    if D_K % 4 == 1:
        return pari.qfbred(pari(f"Qfb(1,1,{(1 - D_K) // 4})"))
    return pari.qfbred(pari(f"Qfb(1,0,{(-D_K) // 4})"))


def form_order(pari: Pari, form, h: int, factors: dict[int, int], principal_text: str, nucomp_l: int) -> int:
    order = h
    for q, e in factors.items():
        for _ in range(e):
            candidate = order // q
            if form_key(pari, pow_form(pari, form, candidate, nucomp_l)) == principal_text:
                order = candidate
            else:
                break
    return order


def gamma0_index_squarefree(norm: int) -> int:
    value = norm
    for prime in sp.factorint(norm):
        value *= prime + 1
        value //= prime
    return int(value)


def split_forms(pari: Pari, D_K: int, prime_bound: int) -> list[SplitForm]:
    out: list[SplitForm] = []
    for ell in sp.primerange(2, prime_bound + 1):
        ell = int(ell)
        if abs(D_K) % ell == 0 or sp.kronecker_symbol(D_K, ell) != 1:
            continue
        form = pari.qfbprimeform(D_K, ell)
        out.append(SplitForm(ell, form, inverse_form(pari, form)))
    return out


def search_target(target: Target, prime_bound: int, max_factors: int, max_norm: int) -> list[Hit]:
    pari = Pari()
    pari.allocatemem(512 * 1024 * 1024)
    nucomp_l = int((abs(target.D_K) // 4) ** 0.25) + 1
    principal_text = form_key(pari, principal_form(pari, target.D_K))
    factors = {int(q): int(e) for q, e in sp.factorint(target.h).items()}
    identity = pow_form(pari, principal_form(pari, target.D_K), 0, nucomp_l)

    forms = split_forms(pari, target.D_K, prime_bound)
    signed = [(row.ell, row.form) for row in forms] + [(-row.ell, row.inv_form) for row in forms]
    hits: list[Hit] = []
    seen: set[tuple[tuple[int, ...], int]] = set()

    for size in range(1, max_factors + 1):
        for combo in itertools.combinations(signed, size):
            abs_terms = tuple(sorted(abs(ell) for ell, _form in combo))
            if len(set(abs_terms)) != len(abs_terms):
                continue
            norm = math.prod(abs_terms)
            if norm > max_norm:
                continue
            product = identity
            for _ell, form in combo:
                product = compose(pari, product, form, nucomp_l)
            key = (tuple(ell for ell, _form in combo), hash(form_key(pari, product)))
            if key in seen:
                continue
            seen.add(key)
            order = form_order(pari, product, target.h, factors, principal_text, nucomp_l)
            index = target.h // order
            hits.append(
                Hit(
                    trace=target.trace,
                    D_K=target.D_K,
                    h=target.h,
                    group=target.group,
                    norm=norm,
                    x0_index=gamma0_index_squarefree(norm),
                    order=order,
                    index=index,
                    signed_terms=tuple(ell for ell, _form in combo),
                )
            )
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime-bound", type=int, default=200)
    ap.add_argument("--max-factors", type=int, default=3)
    ap.add_argument("--max-norm", type=int, default=100000)
    ap.add_argument("--show", type=int, default=15)
    args = ap.parse_args()

    pari = Pari()
    targets = exact_targets(pari)
    sqrt_p = math.isqrt(P)
    print("all-trace composite split-ideal order search")
    print(f"p={P}")
    print(f"sqrt_floor={sqrt_p}")
    print(f"prime_bound={args.prime_bound}")
    print(f"max_factors={args.max_factors}")
    print(f"max_norm={args.max_norm}")
    print()

    all_hits: list[Hit] = []
    for target in targets:
        hits = search_target(target, args.prime_bound, args.max_factors, args.max_norm)
        all_hits.extend(hits)
        print(f"trace={target.trace}")
        print(f"  D_K={target.D_K}")
        print(f"  h={target.h}")
        print(f"  group={target.group}")
        print(f"  h_factor={sp.factorint(target.h)}")
        print(f"  hits={len(hits)}")
        print("  best_by_max_degree")
        print("    norm x0_index index order max/sqrt seeded/sqrt signed_terms")
        for hit in sorted(hits, key=lambda r: (max(r.index, r.order), r.x0_index, r.norm))[: args.show]:
            print(
                f"    {hit.norm:8d} {hit.x0_index:8d} {hit.index:10d} {hit.order:15d} "
                f"{max(hit.index, hit.order) / sqrt_p:9.3e} "
                f"{hit.x0_index * hit.order / sqrt_p:11.3e} {hit.signed_terms}"
            )
        print("  best_by_seeded_proxy")
        for hit in sorted(hits, key=lambda r: (r.x0_index * r.order, max(r.index, r.order), r.norm))[: args.show]:
            print(
                f"    {hit.norm:8d} {hit.x0_index:8d} {hit.index:10d} {hit.order:15d} "
                f"{max(hit.index, hit.order) / sqrt_p:9.3e} "
                f"{hit.x0_index * hit.order / sqrt_p:11.3e} {hit.signed_terms}"
            )
        print()

    print("global_best_by_max_degree")
    for hit in sorted(all_hits, key=lambda r: (max(r.index, r.order), r.x0_index, r.norm))[: args.show]:
        print(
            f"  trace={hit.trace:15d} norm={hit.norm:8d} x0_index={hit.x0_index:8d} "
            f"index={hit.index:10d} order={hit.order:15d} "
            f"max/sqrt={max(hit.index, hit.order) / sqrt_p:.3e} "
            f"seeded/sqrt={hit.x0_index * hit.order / sqrt_p:.3e} terms={hit.signed_terms}"
        )
    print()
    print("interpretation")
    print("  composite_products_can_rebalance_formal_quotient_and_recovery_degrees=1")
    print("  seeded_proxy_assumes_a_seed_root_or_embedded_quotient=1")
    print("  search_does_not_construct_CM_roots=1")
    print("conclusion=reported_all_trace_composite_split_order_search")


if __name__ == "__main__":
    main()
