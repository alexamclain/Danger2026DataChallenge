#!/usr/bin/env python3
"""Audit the X0(2^a) versus X1(2^a) orientation gap for p24.

For a curve with a rational cyclic 2^a-isogeny, Frobenius has odd eigenvalues
lambda and p/lambda modulo 2^a, so the trace lies in

    lambda + p/lambda mod 2^a.

For a DANGER/Pomerance certificate we need the much stronger condition that
one eigenvalue is 1 (or -1 on the twist), i.e. rational 2^a torsion.  This
script counts the trace residues allowed by X0(2^a) and the number of
orientations giving the DANGER residue.
"""

from __future__ import annotations

P24 = 10**24 + 7


def main() -> None:
    print("p24 X0(2^a) orientation audit")
    print(f"p={P24}")
    print(f"p_mod_16={P24 % 16}")
    print("a modulus x0_trace_residues fraction target_orientations source")
    for a in range(4, 21):
        modulus = 1 << a
        target = (P24 + 1) % modulus
        residues: set[int] = set()
        target_orientations = 0
        for lam in range(1, modulus, 2):
            tr = (lam + P24 * pow(lam, -1, modulus)) % modulus
            residues.add(tr)
            if tr == target:
                target_orientations += 1
        print(
            f"{a:2d} {modulus:13d} {len(residues):13d} "
            f"{len(residues) / modulus:.6f} {target_orientations:5d} enumerated"
        )

    # The enumerated rows stabilize immediately for p == 7 mod 16:
    # the X0 trace-residue image has size 2^(a-3), while the DANGER
    # residue has four odd-eigenvalue preimages.
    for a in (24, 28, 32, 36, 40):
        modulus = 1 << a
        residues = 1 << (a - 3)
        print(f"{a:2d} {modulus:13d} {residues:13d} {residues / modulus:.6f} {4:5d} pattern")


if __name__ == "__main__":
    main()
