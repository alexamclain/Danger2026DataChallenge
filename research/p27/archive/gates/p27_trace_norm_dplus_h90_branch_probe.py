#!/usr/bin/env python3
"""Branch/Kummer extraction for the normalized Dplus H90 quartic.

For

    rho^4 - 2*U_eta*rho^2 + F*Sprime^2 = 0

over E_h90, the quadratic resolvent is controlled by

    Delta_eta = U_eta^2 - F*Sprime^2.

This probe verifies symbolically that

    Delta_eta = F * W_eta^2

after reducing by the elliptic equation w^2=-(t^2+2t-1)(t^2-2t-1).
Therefore the first quadratic layer is exactly the domain-spin cover z^2=F.
The hard class is the second layer

    rho^2 = U_eta + z*W_eta

over the genus-5 cover E_h90(z).
"""

from __future__ import annotations

import sympy as sp


def reduce_w(expr: sp.Expr, w: sp.Symbol, relation: sp.Expr) -> sp.Expr:
    poly = sp.Poly(sp.expand(expr), w)
    out = 0
    for (power,), coeff in poly.terms():
        if power % 2 == 0:
            out += coeff * relation ** (power // 2)
        else:
            out += coeff * w * relation ** ((power - 1) // 2)
    return sp.factor(out)


def reduce_square(expr: sp.Expr, var: sp.Symbol, relation: sp.Expr) -> sp.Expr:
    poly = sp.Poly(sp.expand(expr), var)
    out = 0
    for (power,), coeff in poly.terms():
        if power % 2 == 0:
            out += coeff * relation ** (power // 2)
        else:
            out += coeff * var * relation ** ((power - 1) // 2)
    return sp.factor(out)


def reduce_eta(expr: sp.Expr, eta: sp.Symbol) -> sp.Expr:
    poly = sp.Poly(sp.expand(expr), eta)
    out = 0
    for (power,), coeff in poly.terms():
        out += coeff * (eta if power % 2 else 1)
    return sp.factor(out)


def main() -> int:
    t, w, eta, rho, z = sp.symbols("t w eta rho z")
    B = t**2 + 1
    C = t**2 + 2 * t - 1
    R = t**2 - 2 * t - 1
    F = t * C * B
    K = -C * R
    Sprime = (t - 1) ** 3 * (t + 1) ** 2 * B
    Ueta = 2 * t**2 * (t - 1) * B**2 * (eta * w + C)
    Weta = (t - 1) * B * (4 * t**3 + eta * B * w)
    Delta = Ueta**2 - F * Sprime**2
    delta_reduced = reduce_eta(reduce_w(Delta - F * Weta**2, w, K), eta)
    quartic = rho**4 - 2 * Ueta * rho**2 + F * Sprime**2
    split_product = (rho**2 - (Ueta + z * Weta)) * (rho**2 - (Ueta - z * Weta))
    split_reduced = reduce_eta(reduce_w(reduce_square(split_product - quartic, z, F), w, K), eta)

    print("p27 trace/norm Dplus H90 branch probe")
    print("E_h90: w^2=-(t^2+2t-1)(t^2-2t-1)")
    print("quartic = rho^4 - 2*U_eta*rho^2 + F*Sprime^2")
    print("U_eta:")
    print(f"  {sp.factor(Ueta)}")
    print("W_eta:")
    print(f"  {sp.factor(Weta)}")
    print("Delta_identity:")
    print("  U_eta^2 - F*Sprime^2 = F*W_eta^2")
    print(f"  exact = {int(sp.simplify(delta_reduced) == 0)}")
    print("quartic_split_over_z2_F:")
    print("  quartic = (rho^2 - (U_eta + z*W_eta))*(rho^2 - (U_eta - z*W_eta))")
    print(f"  exact = {int(sp.simplify(split_reduced) == 0)}")
    print("second_layer:")
    print("  rho^2 = U_eta + z*W_eta over z^2=F")
    print("p27_trace_norm_dplus_h90_branch_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
