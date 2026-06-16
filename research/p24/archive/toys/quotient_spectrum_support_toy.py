#!/usr/bin/env python3
"""Toy checks for the quotient-spectrum support refinement.

The exact p24 support question is:

    min weight in e_H + Ann(J) >= |H|.

Full reduced normality implies this immediately.  This toy checks the weaker
case where only quotient characters are protected: artificial annihilators are
inserted away from the quotient spectrum, and the script brute-forces whether
they reduce the H-projector support in small cyclic groups.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools

import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_factor

T = sp.symbols("T")


@dataclass(frozen=True)
class Row:
    h: int
    q: int
    m: int
    n: int
    factor_degree: int
    quotient_factor: bool
    projector_weight: int
    best_weight: int
    reduced: bool


def poly_coeffs(poly: sp.Poly, h: int, q: int) -> list[int]:
    out = [0] * h
    for (power,), coeff in poly.as_dict().items():
        out[power % h] = (out[power % h] + int(coeff)) % q
    return out


def weight(vec: list[int], q: int) -> int:
    return sum(1 for x in vec if x % q)


def shift(vec: list[int], amount: int) -> list[int]:
    h = len(vec)
    out = [0] * h
    for i, value in enumerate(vec):
        out[(i + amount) % h] = value
    return out


def projector(h: int, m: int) -> list[int]:
    n = h // m
    out = [0] * h
    for k in range(n):
        out[(m * k) % h] = 1
    return out


def factor_is_quotient_spectrum(factor: sp.Poly, h: int, m: int, q: int) -> bool:
    """Return whether this factor divides the quotient-spectrum polynomial."""
    n = h // m
    quotient_poly = sp.Poly(T**m - 1, T, modulus=q)
    # Characters trivial on H are zeta^{n*r}; their minimal polynomials are
    # represented by T^m-1 after the quotient variable substitution.
    # For this toy we detect them by checking whether factor(T) divides T^m-1
    # after using small h where quotient factors embed visibly.
    return sp.gcd(factor, quotient_poly).degree() > 0 if factor.degree() <= m else False


def best_weight_with_factor(
    base: list[int],
    generator: list[int],
    q: int,
    degree: int,
    max_q_degree2: int,
) -> int | None:
    if degree == 1:
        best = len(base) + 1
        for a in range(q):
            candidate = [(x + a * y) % q for x, y in zip(base, generator)]
            best = min(best, weight(candidate, q))
        return best
    if degree == 2 and q <= max_q_degree2:
        basis = [generator, shift(generator, 1)]
        best = len(base) + 1
        for a, b in itertools.product(range(q), repeat=2):
            candidate = [
                (x + a * y + b * z) % q
                for x, y, z in zip(base, basis[0], basis[1])
            ]
            best = min(best, weight(candidate, q))
        return best
    return None


def rows(max_h: int, max_q: int, max_q_degree2: int) -> list[Row]:
    out: list[Row] = []
    for h in range(6, max_h + 1):
        for q in sp.primerange(3, max_q + 1):
            if (q - 1) % h:
                continue
            torsion = sp.Poly(T**h - 1, T, modulus=q)
            coeffs = [1] + [0] * (h - 1) + [-1]
            _unit, raw_factors = gf_factor(coeffs, int(q), ZZ)
            factors = [
                (
                    sp.Poly.from_list(
                        [int(c) % int(q) for c in factor_coeffs],
                        gens=T,
                        modulus=int(q),
                    ),
                    multiplicity,
                )
                for factor_coeffs, multiplicity in raw_factors
            ]
            for m in sp.divisors(h):
                m = int(m)
                if not (2 <= m < h and h % m == 0):
                    continue
                base = projector(h, m)
                for factor, multiplicity in factors:
                    if multiplicity != 1 or factor.degree() not in (1, 2):
                        continue
                    quotient, rem = torsion.div(factor)
                    if not rem.is_zero:
                        continue
                    generator = poly_coeffs(quotient, h, q)
                    best = best_weight_with_factor(
                        base,
                        generator,
                        q,
                        factor.degree(),
                        max_q_degree2=max_q_degree2,
                    )
                    if best is None:
                        continue
                    out.append(
                        Row(
                            h=h,
                            q=int(q),
                            m=m,
                            n=h // m,
                            factor_degree=factor.degree(),
                            quotient_factor=factor_is_quotient_spectrum(
                                factor, h, m, int(q)
                            ),
                            projector_weight=weight(base, int(q)),
                            best_weight=best,
                            reduced=best < weight(base, int(q)),
                        )
                    )
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-h", type=int, default=24)
    ap.add_argument("--max-q", type=int, default=250)
    ap.add_argument("--max-q-degree2", type=int, default=101)
    args = ap.parse_args()

    data = rows(
        max_h=args.max_h,
        max_q=args.max_q,
        max_q_degree2=args.max_q_degree2,
    )
    nonquotient = [row for row in data if not row.quotient_factor]
    quotient = [row for row in data if row.quotient_factor]
    reduced_nonquotient = [row for row in nonquotient if row.reduced]
    reduced_quotient = [row for row in quotient if row.reduced]

    print("quotient-spectrum support toy")
    print(f"max_h={args.max_h}")
    print(f"max_q={args.max_q}")
    print(f"rows={len(data)}")
    print()
    print("summary")
    print(f"  nonquotient_factor_rows={len(nonquotient)}")
    print(f"  nonquotient_reduced_rows={len(reduced_nonquotient)}")
    print(f"  quotient_factor_rows={len(quotient)}")
    print(f"  quotient_reduced_rows={len(reduced_quotient)}")
    print()
    print("sample rows: h q m n deg quotient_factor projector best reduced")
    for row in data[:30]:
        print(
            f"{row.h:2d} {row.q:3d} {row.m:2d} {row.n:2d} "
            f"{row.factor_degree:1d} {int(row.quotient_factor):1d} "
            f"{row.projector_weight:2d} {row.best_weight:2d} {int(row.reduced):1d}"
        )
    if reduced_nonquotient[:5]:
        print()
        print("nonquotient reductions")
        for row in reduced_nonquotient[:5]:
            print(row)
    if reduced_quotient[:5]:
        print()
        print("quotient reductions")
        for row in reduced_quotient[:5]:
            print(row)
    print()
    print("interpretation")
    print("  quotient_factor=0 models vanished non-H characters only")
    print("  quotient_factor=1 models a vanished character needed by e_H")
    print("  no nonquotient reductions supports the quotient-spectrum refinement")
    print("conclusion=reported_quotient_spectrum_support_toy")


if __name__ == "__main__":
    main()
