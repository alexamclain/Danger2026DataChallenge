#!/usr/bin/env python3
"""Probe the squareclass of rational roots of the Montgomery 3-division quartic.

For p == 1 mod 3 and E_A: y^2 = x^3 + A*x^2 + x, the p23 ell=3
trace filter rejects trace class 1 and accepts classes 0 and 2.  The
3-division x-polynomial is:

    psi_3(z) = 3*z^4 + 4*A*z^3 + 6*z^2 - 1.

For a root z of psi_3, the curve/twist bit is chi(f(z)) = chi(z), because

    f(z) = z^3 + A*z^2 + z = (z - 1)^2 * (z + 1)^2 / (4*z).

This sidecar samples X1(16) Montgomery A-values over calibration primes,
factors psi_3 over Fp, and records whether rational roots have uniform
squareclass by trace residue.  It is a research artifact, not a production
benchmark.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter

import sympy as sp

import x16_trace_residue_calibration as cal
from ell3_trace_filter_validate import trace_mod3_filter


P23_MODULUS_DEFAULT = 8 * 3 * 5 * 7 * 11


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    value = pow(a, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def psi3_roots(A: int, p: int, z: sp.Symbol) -> list[int]:
    poly = sp.Poly(3 * z**4 + 4 * A * z**3 + 6 * z**2 - 1, z, modulus=p)
    roots: list[int] = []
    for root, multiplicity in poly.ground_roots().items():
        roots.extend([int(root) % p] * multiplicity)
    return sorted(roots)


def run_prime(p: int, samples: int, seed: int) -> None:
    rng = random.Random(seed)
    As = cal.x16_montgomery_A_values(p, rng, samples)
    z = sp.symbols("z")

    pattern_counts: Counter[tuple[int, int, int, int]] = Counter()
    mismatched_classifier = 0
    nonuniform_squareclass = 0
    examples: list[tuple[int, int, tuple[int, ...], int, list[int]]] = []

    for A in As:
        tm3 = trace_mod3_filter(A, p)
        roots = psi3_roots(A, p, z)
        signs = tuple(legendre(root, p) for root in roots)
        pattern_counts[(tm3, len(roots), signs.count(1), signs.count(-1))] += 1

        shortcut_reject = bool(roots and signs.count(-1))
        if shortcut_reject != (tm3 == 1):
            mismatched_classifier += 1
        if signs and len(set(signs)) > 1:
            nonuniform_squareclass += 1
        if len(examples) < 8 and roots:
            examples.append((tm3, len(roots), signs, A, roots[:4]))

    print(f"p={p}")
    print(f"samples={len(As)} seed={seed}")
    print(f"mismatched_classifier={mismatched_classifier}")
    print(f"nonuniform_root_squareclass={nonuniform_squareclass}")
    print("pattern tm3 rational_roots square_roots nonsquare_roots count")
    for (tm3, nroots, nsq, nns), count in sorted(pattern_counts.items()):
        print(f"{tm3} {nroots} {nsq} {nns} {count}")
    print("examples tm3,nroots,signs,A,roots")
    for row in examples:
        print(",".join(str(x) for x in row))
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=160)
    parser.add_argument("--starts", type=int, nargs="+", default=[100_000, 200_000, 400_000])
    parser.add_argument("--seed", type=int, default=20260606)
    parser.add_argument("--modulus", type=int, default=P23_MODULUS_DEFAULT)
    args = parser.parse_args()

    if args.modulus % 3 != 0:
        raise SystemExit("--modulus should include 3 so calibration primes match p23 mod 3")

    print("Ell=3 rational-root squareclass probe")
    print(f"p23_mod_modulus={cal.P23 % args.modulus} modulus={args.modulus}")
    print()
    for start in args.starts:
        p = cal.find_calibration_prime(start, args.modulus, cal.P23 % args.modulus)
        if p % 3 != 1:
            print(f"skipping p={p}: p mod 3 != 1", file=sys.stderr)
            continue
        run_prime(p, args.samples, args.seed)


if __name__ == "__main__":
    main()
