#!/usr/bin/env python3
"""Exhaust low-degree Kummer semiconjugacies over small finite fields.

In the Kummer coordinate s=x+1/x, Montgomery doubling is a rational map R_A(s).
If there were a low-degree rational S(u), with u=z+z^-1, satisfying

    R_A(S(u)) = S(u^2 - 2),

then a depth-k DANGER condition could reduce to a power-map/root-extraction
problem.  The LFT case is checked in kummer_semiconjugacy_probe.py; this file
exhausts all projective rational maps of degree <= 2 over small fields.

This is evidence, not a proof over Q or F_p24.
"""

from __future__ import annotations

from itertools import product


INF = None


def canonical_projective_vectors(p: int, length: int):
    for coeffs in product(range(p), repeat=length):
        if all(c == 0 for c in coeffs):
            continue
        first = next(c for c in coeffs if c != 0)
        if first != 1:
            continue
        yield coeffs


def proportional(a: tuple[int, ...], b: tuple[int, ...], p: int) -> bool:
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if (a[i] * b[j] - a[j] * b[i]) % p != 0:
                return False
    return True


def eval_quad(coeffs: tuple[int, int, int], u: int | None, p: int) -> int:
    c0, c1, c2 = coeffs
    if u is INF:
        return c2 % p
    return (c0 + c1 * u + c2 * u * u) % p


def eval_S(
    num: tuple[int, int, int],
    den: tuple[int, int, int],
    u: int | None,
    p: int,
) -> tuple[int, int]:
    n = eval_quad(num, u, p)
    d = eval_quad(den, u, p)
    return n, d


def R_projective(A: int, point: tuple[int, int], p: int) -> tuple[int, int]:
    n, d = point
    if d % p == 0:
        return 1, 0

    s = n * pow(d, p - 2, p) % p
    s2m4 = (s * s - 4) % p
    spA = (s + A) % p
    rn = (s2m4 * s2m4 + 16 * spA * spA) % p
    rd = (4 * spA * s2m4) % p
    return rn, rd


def same_projective(p1: tuple[int, int], p2: tuple[int, int], p: int) -> bool:
    return (p1[0] * p2[1] - p1[1] * p2[0]) % p == 0


def identity_holds(
    p: int,
    A: int,
    num: tuple[int, int, int],
    den: tuple[int, int, int],
) -> bool:
    for u in list(range(p)) + [INF]:
        left = R_projective(A, eval_S(num, den, u, p), p)
        u2 = INF if u is INF else (u * u - 2) % p
        right = eval_S(num, den, u2, p)
        if not same_projective(left, right, p):
            return False
    return True


def run_prime(p: int) -> None:
    solutions: list[tuple[int, tuple[int, ...]]] = []
    maps_checked = 0
    for coeffs in canonical_projective_vectors(p, 6):
        num = coeffs[:3]
        den = coeffs[3:]
        if den == (0, 0, 0):
            continue
        if proportional(num, den, p):
            continue
        maps_checked += 1
        for A in range(p):
            if (A * A - 4) % p == 0:
                continue
            if identity_holds(p, A, num, den):
                solutions.append((A, coeffs))
                if len(solutions) <= 5:
                    print(f"  solution A={A} coeffs={coeffs}")
    print(
        f"p={p:2d} maps_checked={maps_checked} "
        f"nonconstant_nonsingular_degree_le_2_solutions={len(solutions)}"
    )


def main() -> None:
    print("degree_le_2_kummer_semiconjugacy_probe")
    for p in (5, 7, 11, 13):
        run_prime(p)


if __name__ == "__main__":
    main()
