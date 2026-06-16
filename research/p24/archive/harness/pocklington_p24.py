#!/usr/bin/env python3
"""Pocklington certificate for p = 10^24 + 7.

This is a primality certificate, not a DANGER3 Montgomery x-only triple.  It
uses the large prime factor of p-1 to beat sqrt(p) scaling outright for this
specific p.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

P24 = 10**24 + 7
OUT = Path(__file__).with_name("pocklington_p24_certificate.json")


@dataclass
class Cert:
    n: int
    factors: dict[int, int]
    bases: dict[int, int]
    children: dict[int, "Cert"]

    def to_jsonable(self):
        return {
            "n": str(self.n),
            "n_minus_1_factorization": {str(k): v for k, v in sorted(self.factors.items())},
            "bases_by_prime_factor": {str(k): v for k, v in sorted(self.bases.items())},
            "children": {str(k): v.to_jsonable() for k, v in sorted(self.children.items())},
        }


def trial_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = math.isqrt(n)
    d = 3
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True


def find_base(n: int, q: int) -> int:
    for a in range(2, 10_000):
        if math.gcd(a, n) != 1:
            continue
        if pow(a, n - 1, n) != 1:
            continue
        if math.gcd(pow(a, (n - 1) // q, n) - 1, n) == 1:
            return a
    raise RuntimeError(f"no Pocklington base found for n={n} q={q}")


def build_cert(n: int, small_limit: int = 10_000) -> Cert:
    if n <= small_limit:
        if not trial_prime(n):
            raise ValueError(f"small leaf is not prime: {n}")
        return Cert(n=n, factors={}, bases={}, children={})

    factors = {int(k): int(v) for k, v in sp.factorint(n - 1).items()}
    children: dict[int, Cert] = {}
    bases: dict[int, int] = {}
    for q in factors:
        if q > small_limit:
            children[q] = build_cert(q, small_limit=small_limit)
        elif not trial_prime(q):
            raise ValueError(f"small factor is not prime: {q}")
        bases[q] = find_base(n, q)
    return Cert(n=n, factors=factors, bases=bases, children=children)


def verify_cert(cert: Cert, small_limit: int = 10_000) -> None:
    n = cert.n
    if n <= small_limit:
        if not trial_prime(n):
            raise AssertionError(f"small leaf is not prime: {n}")
        return

    product = 1
    for q, e in cert.factors.items():
        if q in cert.children:
            verify_cert(cert.children[q], small_limit=small_limit)
        elif not trial_prime(q):
            raise AssertionError(f"uncertified composite factor {q} of {n}-1")
        product *= q**e
    if product != n - 1:
        raise AssertionError(f"bad factorization for {n}-1")
    if product <= math.isqrt(n):
        raise AssertionError(f"certified factor product is not > sqrt({n})")

    for q in cert.factors:
        a = cert.bases[q]
        if pow(a, n - 1, n) != 1:
            raise AssertionError(f"base {a} fails Fermat for n={n}")
        if math.gcd(pow(a, (n - 1) // q, n) - 1, n) != 1:
            raise AssertionError(f"base {a} fails q={q} Pocklington gcd for n={n}")


def from_jsonable(obj) -> Cert:
    return Cert(
        n=int(obj["n"]),
        factors={int(k): int(v) for k, v in obj["n_minus_1_factorization"].items()},
        bases={int(k): int(v) for k, v in obj["bases_by_prime_factor"].items()},
        children={int(k): from_jsonable(v) for k, v in obj["children"].items()},
    )


def main() -> None:
    cert = build_cert(P24)
    verify_cert(cert)
    OUT.write_text(json.dumps(cert.to_jsonable(), indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(f"p={P24}")
    print(f"sqrt_floor={math.isqrt(P24)}")
    big = max(cert.factors)
    print(f"largest_factor_p_minus_1={big}")
    print(f"largest_factor_gt_sqrt={big > math.isqrt(P24)}")

    roundtrip = from_jsonable(json.loads(OUT.read_text()))
    verify_cert(roundtrip)
    print("verification=PASS")


if __name__ == "__main__":
    main()
