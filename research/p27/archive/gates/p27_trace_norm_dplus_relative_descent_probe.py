#!/usr/bin/env python3
"""Symbolic relative descent identity for the p27 trace/norm Dplus class.

The finite-field quotient probe found that Dplus is constant on the visible
fibers of

    a = t - 1/t,  g = w/t,  a^2 + g^2 = 4

after the domain-spin root z is present.  This script explains the exact
symbolic reason.  If u = -core = u0 + u1*z in the quadratic extension
z^2 = F, then

    Norm_z(u) = F * square

after imposing w^2 = -(t^2+2t-1)(t^2-2t-1).  Thus the z-flip fiber constancy
is conditional on the domain-spin squareclass F already being square.  The
Dplus class is a relative Kummer/Hilbert-90 class over the domain-spin cover,
not a standalone rational character on the quotient conic.
"""

from __future__ import annotations

import sympy as sp


def main() -> int:
    t, z, w, eh, ev = sp.symbols("t z w eh ev")
    B = t**2 + 1
    C = t**2 + 2 * t - 1
    R = t**2 - 2 * t - 1
    y = t + 1
    F = t * C * B
    K = -C * R

    hcore = C * B + eh * 2 * t * z
    vcore = 2 * C * t**2 + ev * z * w
    u = sp.expand(-((1 - t**2) * B * C * y * hcore * vcore))

    poly_z = sp.Poly(u, z)
    u0 = 0
    u1 = 0
    for (power,), coeff in poly_z.terms():
        if power % 2 == 0:
            u0 += coeff * F ** (power // 2)
        else:
            u1 += coeff * F ** ((power - 1) // 2)
    u0 = sp.factor(u0.subs({eh**2: 1, ev**2: 1}))
    u1 = sp.factor(u1.subs({eh**2: 1, ev**2: 1}))

    norm_z = sp.expand(u0**2 - u1**2 * F)
    poly_w = sp.Poly(norm_z, w)
    norm_reduced = 0
    for (power,), coeff in poly_w.terms():
        if power % 2 == 0:
            norm_reduced += coeff * K ** (power // 2)
        else:
            norm_reduced += coeff * w * K ** ((power - 1) // 2)
    norm_reduced = sp.factor(norm_reduced.subs({eh**2: 1, ev**2: 1}))

    square_part = (t - 1) ** 3 * (t + 1) ** 4 * B * C**2
    expected = sp.factor(F * square_part**2)
    quotient = sp.factor(norm_reduced / F)

    print("p27 trace/norm Dplus relative descent probe")
    print("variables:")
    print("  B=t^2+1")
    print("  C=t^2+2*t-1")
    print("  R=t^2-2*t-1")
    print("  F=t*C*B=z^2")
    print("  w^2=-C*R")
    print("  u=-core=u0+u1*z")
    print("u0_factor:")
    print(f"  {u0}")
    print("u1_factor:")
    print(f"  {u1}")
    print("norm_reduced:")
    print(f"  {norm_reduced}")
    print("square_part:")
    print(f"  {square_part}")
    print("norm_identity:")
    print("  Norm_z(u) = F * square_part^2")
    print(f"  exact = {int(sp.simplify(norm_reduced - expected) == 0)}")
    print("norm_over_F:")
    print(f"  {quotient}")
    print("interpretation:")
    print("  zflip constancy is conditional on F being square")
    print("  Dplus is a relative Kummer class over the domain-spin cover")
    print("  do not search for a standalone rational R(m) on a^2+g^2=4")
    print("p27_trace_norm_dplus_relative_descent_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
