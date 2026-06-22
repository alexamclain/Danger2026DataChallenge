#!/usr/bin/env python3
"""Normalized quartic model for the Dplus H90 quotient.

After quotienting by the order-4 H90 lift, the relative Dplus cover is a
degree-4 cover over E_h90:

    E_h90: w^2 = -(t^2+2t-1)(t^2-2t-1).

Scale s by D=(t+1)(t^2+2t-1).  The eliminated quartic for rho=s/D depends on
the orientation signs only through eta=eh*ev:

    rho^4 - 2*U_eta*rho^2 + F*S_eta^2 = 0

where

    U_eta = 2*t^2*(t-1)*(t^2+1)^2*(eta*w + t^2+2t-1)
    F = t*(t^2+2t-1)*(t^2+1)
    S_eta = (t-1)^3*(t+1)^2*(t^2+1).

This script verifies that identity symbolically.
"""

from __future__ import annotations

import sympy as sp


def main() -> int:
    t, w, z, eh, ev, rho = sp.symbols("t w z eh ev rho")
    eta = sp.symbols("eta")
    B = t**2 + 1
    C = t**2 + 2 * t - 1
    R = t**2 - 2 * t - 1
    F = t * C * B
    K = -C * R
    D = (t + 1) * C
    Sprime = (t - 1) ** 3 * (t + 1) ** 2 * B

    hcore = C * B + eh * 2 * t * z
    vcore = 2 * C * t**2 + ev * z * w
    u = sp.expand(-((1 - t**2) * B * C * (t + 1) * hcore * vcore))
    u_scaled = sp.factor(u / D**2)

    poly_z = sp.Poly(u_scaled, z)
    u0 = 0
    u1 = 0
    for (power,), coeff in poly_z.terms():
        if power % 2 == 0:
            u0 += coeff * F ** (power // 2)
        else:
            u1 += coeff * F ** ((power - 1) // 2)
    u0 = sp.factor(u0.subs({eh**2: 1, ev**2: 1}))
    u1 = sp.factor(u1.subs({eh**2: 1, ev**2: 1}))

    U_eta = 2 * t**2 * (t - 1) * B**2 * (eta * w + C)
    U_sub = sp.factor(U_eta.subs(eta, eh * ev))
    norm_scaled = sp.factor(u0**2 - u1**2 * F)
    norm_reduced = sp.Poly(sp.expand(norm_scaled), w)
    norm_w = 0
    for (power,), coeff in norm_reduced.terms():
        if power % 2 == 0:
            norm_w += coeff * K ** (power // 2)
        else:
            norm_w += coeff * w * K ** ((power - 1) // 2)
    norm_w = sp.factor(norm_w.subs({eh**2: 1, ev**2: 1}))

    expected_norm = sp.factor(F * Sprime**2)
    quartic = rho**4 - 2 * U_eta * rho**2 + F * Sprime**2

    print("p27 trace/norm Dplus H90 quartic model probe")
    print("E_h90: w^2=-(t^2+2t-1)(t^2-2t-1)")
    print("rho = s/((t+1)(t^2+2t-1))")
    print("eta = eh*ev")
    print("U_eta:")
    print(f"  {sp.factor(U_eta)}")
    print("Sprime:")
    print(f"  {sp.factor(Sprime)}")
    print("quartic:")
    print(f"  {sp.factor(quartic)}")
    print("u0_scaled:")
    print(f"  {u0}")
    print("u1_scaled:")
    print(f"  {u1}")
    print("u0_matches_U_eta:")
    print(f"  {int(sp.simplify(u0 - U_sub) == 0)}")
    print("norm_scaled_reduced:")
    print(f"  {norm_w}")
    print("norm_matches_F_Sprime_square:")
    print(f"  {int(sp.simplify(norm_w - expected_norm) == 0)}")
    print("sign_collapse:")
    print("  quartic depends on eh,ev only through eta=eh*ev")
    print("p27_trace_norm_dplus_h90_quartic_model_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
