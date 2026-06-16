#!/usr/bin/env python3
"""Toy obstruction for inverse-SEA/oriented split-prime relations.

For the D=-5000 calibration, the norm-3 ideal generates the cyclic class group
of order 30.  Once a CM root is labeled as position i in this torsor, every
oriented split prime acts as a translation i -> i + log(ell).

This models inverse SEA data: knowing the Frobenius eigenvalue modulo many
Elkies primes tells us the oriented split-prime direction, but it does not
choose an origin in the CM torsor.  Any relation word with total log 0 closes
at every CM root, not at a distinguished root.
"""

from __future__ import annotations

import itertools
import math

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import D, ELL, H, Q, isogeny_neighbors, pari_linear_roots, walk_cycle


def qfb_key(pari: Pari, form) -> str:
    return str(pari.qfbred(form))


def class_logs(pari: Pari, primes: list[int]) -> dict[int, int]:
    nucomp_l = int((abs(D) // 4) ** 0.25) + 1
    generator = pari.qfbprimeform(D, ELL)
    powers = {
        qfb_key(pari, pari.qfbnupow(generator, exponent, nucomp_l)): exponent
        for exponent in range(H)
    }
    out: dict[int, int] = {}
    for ell in primes:
        form = pari.qfbprimeform(D, int(ell))
        out[ell] = powers[qfb_key(pari, form)]
    return out


def relation_shift(logs: dict[int, int], word: tuple[int, ...]) -> int:
    total = 0
    for term in word:
        sign = 1 if term > 0 else -1
        total += sign * logs[abs(term)]
    return total % H


def apply_word(index: int, logs: dict[int, int], word: tuple[int, ...]) -> int:
    return (index + relation_shift(logs, word)) % H


def find_small_relation(logs: dict[int, int]) -> tuple[int, ...]:
    items = sorted(logs)
    for size in range(2, 5):
        for combo in itertools.combinations(items, size):
            for signs in itertools.product((1, -1), repeat=size):
                word = tuple(sign * ell for sign, ell in zip(signs, combo))
                if relation_shift(logs, word) == 0:
                    return word
    raise RuntimeError("no small relation")


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    split_primes = [
        int(ell)
        for ell in sp.primerange(2, 80)
        if D % ell != 0 and sp.kronecker_symbol(D, int(ell)) == 1
    ]
    logs = class_logs(pari, split_primes)
    relation = find_small_relation(logs)
    relation_norm = math.prod(abs(term) for term in relation)
    fixed_indices = [i for i in range(H) if apply_word(i, logs, relation) == i]

    cycle_word = (11, 11, 11)
    cycle_fixed = [i for i in range(H) if apply_word(i, logs, cycle_word) == i]
    quotient_orbits = {}
    step = logs[11] % H
    for i in range(H):
        orbit = tuple(sorted({(i + k * step) % H for k in range(3)}))
        quotient_orbits.setdefault(orbit, []).append(i)

    print("oriented relation torsor toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"embedded_cycle_length={len(cycle)}")
    print()
    print("oriented_split_prime_logs_mod_h")
    for ell in split_primes:
        print(f"  ell={ell:2d} log={logs[ell]:2d} order={H // math.gcd(H, logs[ell]):2d}")
    print()
    print("relation_word")
    print(f"  word={relation}")
    print(f"  norm_product={relation_norm}")
    print(f"  total_log_mod_h={relation_shift(logs, relation)}")
    print(f"  fixed_indices_count={len(fixed_indices)}")
    print(f"  fixes_every_cm_root={int(len(fixed_indices) == H)}")
    print()
    print("single_prime_cycle_relation")
    print(f"  word={cycle_word}")
    print(f"  total_log_mod_h={relation_shift(logs, cycle_word)}")
    print(f"  fixed_indices_count={len(cycle_fixed)}")
    print(f"  quotient_orbit_count_for_ell_11={len(quotient_orbits)}")
    print(f"  quotient_orbit_sizes={sorted({len(orbit) for orbit in quotient_orbits})}")
    print()
    print("interpretation")
    print("  oriented_elkies_data_acts_by_translations_on_the_cm_torsor=1")
    print("  relation_words_close_at_every_root_not_one_root=1")
    print("  quotient_cycles_exist_but_need_an_origin_or_period_selector=1")
    print(
        "conclusion=inverse_sea_or_split_prime_relations_are_equivariant_"
        "constraints_and_do_not_break_the_cm_root_torsor_symmetry"
    )


if __name__ == "__main__":
    main()
