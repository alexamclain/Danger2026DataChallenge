#!/usr/bin/env python3
"""Tiny fixed-trace construction toy.

This distinguishes existence/classification theorems from a constructive
selector.  For p=103 and the maximal CM discriminant D_K=-87, the trace

    t = 8

satisfies

    t^2 - 4p = -348 = 4*D_K.

Thus the ordinary isogeny class with trace +/-8 is the small analogue of the
p24 strict traces, whose Frobenius discriminants are 4 times a large
fundamental discriminant.  The full fixed-trace isogeny class contains the
maximal-order crater and the conductor-2 floor, so it is the union of the
roots of H_{D_K} and H_{4D_K} modulo p.

The script enumerates all nonsingular short Weierstrass curves over F_103,
collects the j-invariants with trace +/-8, and compares them to the roots of
H_D mod p.  The point is not that enumeration is hard here; it is that naming
one fixed-trace curve is equivalent to choosing one embedded CM root.
"""

from __future__ import annotations

from cypari2 import Pari

P = 103
MAXIMAL_D = -87
FROBENIUS_D = 4 * MAXIMAL_D
TRACE = 8


def legendre(a: int, p: int = P) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def curve_order(a: int, b: int, p: int = P) -> int:
    total = 1
    for x in range(p):
        rhs = (x * x % p * x + a * x + b) % p
        chi = legendre(rhs, p)
        total += 1 if chi == 0 else 2 if chi == 1 else 0
    return total


def j_invariant(a: int, b: int, p: int = P) -> int | None:
    disc = (-16 * (4 * a * a % p * a + 27 * b * b)) % p
    if disc == 0:
        return None
    numerator = 1728 * (4 * a * a % p * a) % p
    denominator = (4 * a * a % p * a + 27 * b * b) % p
    return numerator * pow(denominator, -1, p) % p


def pari_linear_roots(poly, q: int) -> list[int]:
    pari = Pari()
    fac = pari(f"factor(Mod(1,{q})*({poly}))")
    roots: list[int] = []
    for i in range(len(fac[0])):
        factor = fac[0][i]
        exp = int(fac[1][i])
        if exp != 1:
            raise ValueError(f"non-simple factor {factor}^{exp}")
        degree = int(pari.poldegree(factor))
        if degree != 1:
            raise ValueError(f"nonlinear factor {factor}")
        leading = int(pari.polcoef(factor, 1))
        constant = int(pari.polcoef(factor, 0))
        roots.append((-constant * pow(leading, -1, q)) % q)
    return sorted(roots)


def main() -> None:
    pari = Pari()
    pari.allocatemem(128 * 1024 * 1024)
    maximal_hilbert = pari.polclass(MAXIMAL_D)
    frobenius_hilbert = pari.polclass(FROBENIUS_D)
    maximal_roots = pari_linear_roots(maximal_hilbert, P)
    frobenius_roots = pari_linear_roots(frobenius_hilbert, P)
    cm_roots = sorted(set(maximal_roots) | set(frobenius_roots))

    trace_j: set[int] = set()
    trace_counts: dict[int, int] = {}
    for a in range(P):
        for b in range(P):
            j = j_invariant(a, b)
            if j is None:
                continue
            trace = P + 1 - curve_order(a, b)
            if abs(trace) == TRACE:
                trace_j.add(j)
                trace_counts[trace] = trace_counts.get(trace, 0) + 1

    print("fixed-trace CM-root toy")
    print(f"p={P}")
    print(f"maximal_D={MAXIMAL_D}")
    print(f"frobenius_order_D={FROBENIUS_D}")
    print(f"target_abs_trace={TRACE}")
    print(f"trace_discriminant={TRACE * TRACE - 4 * P}")
    print(f"trace_discriminant_over_maximal_D={(TRACE * TRACE - 4 * P) // MAXIMAL_D}")
    print(f"H_maximal_D_degree={int(pari.poldegree(maximal_hilbert))}")
    print(f"H_frobenius_D_degree={int(pari.poldegree(frobenius_hilbert))}")
    print(f"H_maximal_D_roots_mod_p={maximal_roots}")
    print(f"H_frobenius_D_roots_mod_p={frobenius_roots}")
    print(f"union_CM_roots_mod_p={cm_roots}")
    print(f"enumerated_trace_j_values={sorted(trace_j)}")
    print(f"sets_equal={int(sorted(trace_j) == cm_roots)}")
    print(f"curve_model_counts_by_trace={dict(sorted(trace_counts.items()))}")
    print()
    print("interpretation")
    print("  Waterhouse_existence_or_trace_classification_names_an_isogeny_class=1")
    print("  fixed_trace_class_is_union_of_allowed_CM_orders=1")
    print("  constructing_one_curve_requires_choosing_one_embedded_CM_j_root=1")
    print(
        "conclusion=fixed_trace_construction_over_a_fixed_prime_is_CM_root_"
        "selection_not_a_separate_selector"
    )


if __name__ == "__main__":
    main()
