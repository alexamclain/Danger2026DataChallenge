#!/usr/bin/env python3
"""Toy audit for the Kummer phase in prime-index CM quotients.

This tests small analogues of the first p24 order-19 target:

    index(<ell>) = ell,
    q == -1 mod ell,
    zeta_ell lives in F_{q^2}.

For such examples, Kummer/Fourier coordinates exist over a quadratic
extension.  The test asks whether this selects the embedded quotient from the
unordered split-cycle periods.  It does not: different cyclic orderings of the
same period set produce different Kummer constants T_1^ell.  The true one is
defined only after an oriented class-action generator on the quotient has
been supplied.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots
from norm_equals_index_local_phi_toy import Candidate, components


@dataclass(frozen=True)
class ToyCase:
    D: int
    h: int
    ell: int
    order: int


CASES = (
    ToyCase(D=-743, h=21, ell=3, order=7),
    ToyCase(D=-2239, h=35, ell=5, order=7),
)


def nonsquare(q: int) -> int:
    for d in range(2, q):
        if sp.legendre_symbol(d, q) == -1:
            return d
    raise ValueError("no nonsquare found")


def fadd(a: tuple[int, int], b: tuple[int, int], q: int) -> tuple[int, int]:
    return ((a[0] + b[0]) % q, (a[1] + b[1]) % q)


def fmul(a: tuple[int, int], b: tuple[int, int], q: int, d: int) -> tuple[int, int]:
    return ((a[0] * b[0] + a[1] * b[1] * d) % q, (a[0] * b[1] + a[1] * b[0]) % q)


def fpow(a: tuple[int, int], exponent: int, q: int, d: int) -> tuple[int, int]:
    out = (1, 0)
    base = a
    n = exponent
    while n:
        if n & 1:
            out = fmul(out, base, q, d)
        base = fmul(base, base, q, d)
        n >>= 1
    return out


def fscale(c: int, a: tuple[int, int], q: int) -> tuple[int, int]:
    return (c * a[0] % q, c * a[1] % q)


def primitive_root_in_quadratic(q: int, order: int) -> tuple[int, int, int]:
    d = nonsquare(q)
    exponent = (q * q - 1) // order
    for b in range(1, q):
        for a in range(q):
            candidate = fpow((a, b), exponent, q, d)
            if candidate == (1, 0):
                continue
            if fpow(candidate, order, q, d) != (1, 0):
                continue
            if all(fpow(candidate, order // prime, q, d) != (1, 0) for prime in sp.factorint(order)):
                return candidate[0], candidate[1], d
    raise ValueError("no primitive root found")


def find_splitting_prime(pari: Pari, D: int, h: int, ell: int, max_q: int = 80_000) -> tuple[int, list[int]]:
    hilbert = pari.polclass(D)
    for q in sp.primerange(max(101, h + 2), max_q):
        if q % ell != ell - 1 or abs(D) % q == 0:
            continue
        try:
            roots = pari_linear_roots(hilbert, int(q))
        except ValueError:
            continue
        if len(roots) == h:
            return int(q), roots
    raise ValueError(f"no split q == -1 mod {ell} found")


def component_periods(roots: list[int], ell: int, q: int) -> tuple[list[list[int]], list[int]]:
    graph = isogeny_neighbors(roots, ell, q)
    comps = components(graph)
    periods = [sum(comp) % q for comp in comps]
    return comps, periods


def component_mover_order(
    pari: Pari,
    roots: list[int],
    comps: list[list[int]],
    D: int,
    forbidden_ell: int,
    q: int,
    max_prime: int = 43,
) -> tuple[int | None, list[int] | None]:
    root_to_comp: dict[int, int] = {}
    for idx, comp in enumerate(comps):
        for root in comp:
            root_to_comp[root] = idx

    for prime in sp.primerange(2, max_prime + 1):
        prime = int(prime)
        if prime == forbidden_ell or abs(D) % prime == 0:
            continue
        if sp.kronecker_symbol(D, prime) != 1:
            continue
        graph = isogeny_neighbors(roots, prime, q)
        comp_graph = {idx: set() for idx in range(len(comps))}
        for root, neighs in graph.items():
            src = root_to_comp[root]
            for neigh in neighs:
                dst = root_to_comp[neigh]
                if dst != src:
                    comp_graph[src].add(dst)
                    comp_graph[dst].add(src)
        if sorted(len(v) for v in comp_graph.values()) != [2] * len(comps):
            continue
        order = [0]
        prev = None
        current = 0
        while True:
            candidates = sorted(v for v in comp_graph[current] if v != prev)
            if not candidates:
                break
            nxt = candidates[0]
            if nxt == 0:
                return prime, order
            prev, current = current, nxt
            order.append(current)
            if len(order) > len(comps):
                break
        if len(order) == len(comps):
            return prime, order
    return None, None


def twisted_trace(periods: list[int], zeta: tuple[int, int], q: int, d: int) -> tuple[int, int]:
    total = (0, 0)
    for r, value in enumerate(periods):
        total = fadd(total, fscale(value, fpow(zeta, r, q, d), q), q)
    return total


def kummer_constant(periods: list[int], zeta: tuple[int, int], q: int, d: int) -> tuple[int, int]:
    return fpow(twisted_trace(periods, zeta, q, d), len(periods), q, d)


def conjugacy_orbit_count(values: set[tuple[int, int]], q: int) -> int:
    seen: set[tuple[int, int]] = set()
    count = 0
    for value in values:
        if value in seen:
            continue
        conj = (value[0], (-value[1]) % q)
        seen.add(value)
        seen.add(conj)
        count += 1
    return count


def audit_case(case: ToyCase) -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    q, roots = find_splitting_prime(pari, case.D, case.h, case.ell)
    comps, unordered_periods = component_periods(roots, case.ell, q)
    mover_prime, comp_order = component_mover_order(pari, roots, comps, case.D, case.ell, q)
    if comp_order is None:
        ordered_periods = unordered_periods
    else:
        ordered_periods = [unordered_periods[i] for i in comp_order]

    z0, z1, d = primitive_root_in_quadratic(q, case.ell)
    zeta = (z0, z1)
    true_constant = kummer_constant(ordered_periods, zeta, q, d)

    constants: set[tuple[int, int]] = set()
    first = unordered_periods[0]
    rest = unordered_periods[1:]
    for perm in itertools.permutations(rest):
        constants.add(kummer_constant([first, *perm], zeta, q, d))

    print("toy_case")
    print(f"  D={case.D}")
    print(f"  h={case.h}")
    print(f"  ell=index={case.ell}")
    print(f"  subgroup_order={case.order}")
    print(f"  q={q}")
    print(f"  q_mod_ell={q % case.ell}")
    print(f"  zeta_field=F_q2")
    print(f"  quadratic_nonsquare={d}")
    print(f"  zeta_pair={zeta}")
    print(f"  component_count={len(comps)}")
    print(f"  component_sizes={sorted({len(comp) for comp in comps})}")
    print(f"  unordered_periods={unordered_periods}")
    print(f"  component_mover_prime={mover_prime}")
    print(f"  component_order={comp_order}")
    print(f"  true_ordered_periods={ordered_periods}")
    print(f"  true_T1_power_ell={true_constant}")
    print(f"  true_T1_power_in_Fq={int(true_constant[1] == 0)}")
    print(f"  kummer_constants_from_unordered_periods={len(constants)}")
    print(f"  kummer_constants_up_to_frobenius={conjugacy_orbit_count(constants, q)}")
    print(f"  true_constant_is_one_of_unordered_possibilities={int(true_constant in constants)}")
    print()


def main() -> None:
    print("order-l Kummer phase toy")
    print("interpretation_preface")
    print("  q == -1 mod ell makes the Fourier/Kummer layer quadratic")
    print("  T_1^ell is invariant under cyclic rotation of an ordered quotient")
    print("  but the unordered embedded quotient has many possible cyclic orders")
    print()
    for case in CASES:
        audit_case(case)
    print("interpretation")
    print("  quadratic_cyclotomic_descent_exists_in_toys=1")
    print("  unordered_period_set_does_not_select_kummer_constant=1")
    print("  selecting_the_true_constant_requires_oriented_quotient_action=1")
    print(
        "conclusion=zeta_in_degree_2_is_a_normal_form_for_an_already_"
        "oriented_period_vector_not_a_seedless_embedded_selector"
    )


if __name__ == "__main__":
    main()
