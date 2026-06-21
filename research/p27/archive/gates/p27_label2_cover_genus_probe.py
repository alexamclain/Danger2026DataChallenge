#!/usr/bin/env python3
"""Genus/ramification probe for the p27 label-2 second-gate cover.

This is a lightweight substitute for the requested Sage/Magma pass.  It uses
the explicit tower equations and finite-field local expansions at a prime
where the visible branch factors split.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


P = 17
N = 16


def inv(a: int) -> int:
    return pow(a % P, P - 2, P)


def add(a: list[int], b: list[int]) -> list[int]:
    return [(x + y) % P for x, y in zip(a, b)]


def sub(a: list[int], b: list[int]) -> list[int]:
    return [(x - y) % P for x, y in zip(a, b)]


def scale(c: int, a: list[int]) -> list[int]:
    return [(c * x) % P for x in a]


def mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * N
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b[: N - i]):
            if bj:
                out[i + j] = (out[i + j] + ai * bj) % P
    return out


def pow_series(a: list[int], e: int) -> list[int]:
    out = [0] * N
    out[0] = 1
    base = a
    while e:
        if e & 1:
            out = mul(out, base)
        base = mul(base, base)
        e >>= 1
    return out


def const(c: int) -> list[int]:
    out = [0] * N
    out[0] = c % P
    return out


def var() -> list[int]:
    out = [0] * N
    out[1] = 1
    return out


def order(a: list[int]) -> int:
    for i, ai in enumerate(a):
        if ai % P:
            return i
    return N


def poly_eval(coeffs: list[int], x: list[int]) -> list[int]:
    out = [0] * N
    for c in reversed(coeffs):
        out = mul(out, x)
        out[0] = (out[0] + c) % P
    return out


def f_series(x: list[int]) -> list[int]:
    # x^3 - x
    return sub(pow_series(x, 3), x)


def g_series(x: list[int]) -> list[int]:
    # x*(x^2+1)*(x^2+2x-1)
    x2 = mul(x, x)
    return mul(x, mul(add(x2, const(1)), add(sub(x2, const(1)), scale(2, x))))


def solve_branch_x(a: int, poly_fn, target_order: int = 2) -> list[int]:
    """Return x(u)=a+... with poly_fn(x)=u^target_order."""
    x = const(a)
    for k in range(1, N):
        target = 1 if k == target_order else 0
        # coefficient is linear in c because the constant term is a simple root.
        base = poly_fn(x)
        known = base[k]
        trial = x[:]
        trial[k] = (trial[k] + 1) % P
        delta = (poly_fn(trial)[k] - known) % P
        if delta:
            c = ((target - known) * inv(delta)) % P
            x[k] = (x[k] + c) % P
    return x


def sqrt_unramified(rhs: list[int], y0: int) -> list[int]:
    y = const(y0)
    for k in range(1, N):
        known = mul(y, y)[k]
        delta = (2 * y0) % P
        c = ((rhs[k] - known) * inv(delta)) % P
        y[k] = c
    return y


def sqrt_ramified(rhs: list[int], y1: int) -> list[int]:
    y = [0] * N
    y[1] = y1 % P
    for k in range(2, N):
        known = mul(y, y)[k + 1] if k + 1 < N else 0
        delta = (2 * y1) % P
        if k + 1 < N:
            y[k] = ((rhs[k + 1] - known) * inv(delta)) % P
    return y


def compact_parts(x: list[int], w: list[int]) -> tuple[list[int], list[int], list[int]]:
    x2 = mul(x, x)
    xp1 = add(x, const(1))
    mt = mul(xp1, add(scale(2, mul(w, x)), sub(add(pow_series(x, 3), x2), add(x, const(1)))))
    m0 = mul(
        add(x2, const(1)),
        mul(add(sub(x2, const(1)), scale(2, x)), add(add(mul(w, x), w), scale(2, x2))),
    )
    return mt, m0, add(m0, const(0))


def h_series(x: list[int], w: list[int], t: list[int]) -> list[int]:
    x2 = mul(x, x)
    mt, m0, _ = compact_parts(x, w)
    mp = add(m0, mul(mt, t))
    numerator = mul(w, mul(add(x2, const(1)), mp))
    ox = order(x)
    if ox:
        # Divide by u^ox times the leading coefficient.  This is enough for
        # parity at the only finite pole x=0 in this probe.
        lead_inv = inv(x[ox])
        shifted = numerator[ox:] + [0] * ox
        return scale(lead_inv, shifted)
    return mul(numerator, const(inv(x[0])))


@dataclass
class LocalPoint:
    name: str
    x: list[int]
    w: list[int]
    t: list[int]


def roots_quad(a: int, b: int, c: int) -> list[int]:
    return [x for x in range(P) if (a * x * x + b * x + c) % P == 0]


def finite_points() -> list[LocalPoint]:
    pts: list[LocalPoint] = []
    u = var()

    # f-branch only: X = +/-1, local parameter W.
    for a in [1, P - 1]:
        x = solve_branch_x(a, f_series)
        gv = g_series(const(a))[0]
        for t0 in range(P):
            if t0 * t0 % P == gv:
                t = sqrt_unramified(g_series(x), t0)
                pts.append(LocalPoint(f"x={a if a != P-1 else -1}, W=0, T={t0}", x, u, t))

    # g-branch only: roots of X^2+1 and X^2+2X-1, local parameter T.
    for label, roots in [
        ("X2+1", roots_quad(1, 0, 1)),
        ("X2+2X-1", roots_quad(1, 2, -1)),
    ]:
        for a in roots:
            x = solve_branch_x(a, g_series)
            fv = f_series(const(a))[0]
            for w0 in range(P):
                if w0 * w0 % P == fv:
                    w = sqrt_unramified(f_series(x), w0)
                    pts.append(LocalPoint(f"{label} root X={a}, W={w0}, T=0", x, w, u))

    # common f/g branch at X=0, local parameter W.
    x = solve_branch_x(0, f_series)
    gx = g_series(x)
    # T/W has two possible leading ratios at X=0.
    for t1 in [1, P - 1]:
        t = sqrt_ramified(gx, t1)
        pts.append(LocalPoint(f"x=0 common branch, T/W={t1}", x, u, t))

    # Unramified points where the remaining W-linear norm factor has double
    # zeros: roots of X^2-2X-1.  Use X-a as parameter.
    for a in roots_quad(1, -2, -1):
        x = add(const(a), u)
        fv = f_series(const(a))[0]
        gv = g_series(const(a))[0]
        for w0 in range(P):
            if w0 * w0 % P != fv:
                continue
            # L=0 selects the relevant W sign.
            L0 = (4 * w0 * a * a + 4 * w0 * a + a**4 + 6 * a**3 - 2 * a - 1) % P
            if L0:
                continue
            w = sqrt_unramified(f_series(x), w0)
            for t0 in range(P):
                if t0 * t0 % P != gv:
                    continue
                mt, m0, _ = compact_parts(const(a), const(w0))
                if (m0[0] + mt[0] * t0) % P == 0:
                    t = sqrt_unramified(g_series(x), t0)
                    pts.append(LocalPoint(f"L double root X={a}, W={w0}, T={t0}", x, w, t))

    return pts


def genus_hyperelliptic_squarefree_degree(deg: int) -> int:
    return (deg - 1) // 2


def infinity_orders() -> list[int]:
    s = sp.symbols("s")
    x = s**-2
    wbar = sp.sqrt(1 - s**4).series(s, 0, 12).removeO()
    out = []
    for sign in [1, -1]:
        tbar = (
            sign
            * sp.sqrt((1 + s**4) * (1 + 2 * s**2 - s**4)).series(s, 0, 14).removeO()
        )
        w = wbar * s**-3
        t = tbar * s**-5
        mt = (x + 1) * (2 * w * x + x**3 + x**2 - x - 1)
        m0 = (x**2 + 1) * (x**2 + 2 * x - 1) * (w * x + w + 2 * x**2)
        h = sp.expand(w * (x**2 + 1) * (m0 + mt * t) / x)
        exps = [int(term.as_powers_dict().get(s, 0)) for term in sp.Add.make_args(h)]
        out.append(min(exps))
    return out


def main() -> int:
    # Biquadratic genus via the three quadratic quotients over P1.
    genus_w = genus_hyperelliptic_squarefree_degree(3)
    genus_t = genus_hyperelliptic_squarefree_degree(5)
    genus_wt = genus_hyperelliptic_squarefree_degree(6)
    genus_c = genus_w + genus_t + genus_wt

    odd = []
    print("p27 label2 cover genus/ramification probe")
    print(f"prime = {P}")
    print(f"genus_W = {genus_w}")
    print(f"genus_T = {genus_t}")
    print(f"genus_WT = {genus_wt}")
    print(f"genus_intermediate_C = {genus_c}")
    print("finite_local_orders:")
    for pt in finite_points():
        oh = order(h_series(pt.x, pt.w, pt.t))
        parity = oh % 2
        if parity:
            odd.append(pt.name)
        print(f"  {pt.name}: order={oh} parity={parity}")
    print(f"finite_odd_local_orders = {len(odd)}")
    for name in odd:
        print(f"  odd: {name}")
    inf_orders = infinity_orders()
    inf_odd = [o for o in inf_orders if o % 2]
    print("infinity_local_orders:")
    for idx, o in enumerate(inf_orders):
        print(f"  infinity_class={idx} order={o} parity={o % 2}")
    print(f"infinity_odd_local_orders = {len(inf_odd)}")
    ramification_points = len(odd) + len(inf_odd)
    genus_double_cover = 2 * genus_c - 1 + ramification_points // 2
    print(f"ramification_points_for_R_cover = {ramification_points}")
    print(f"genus_R_cover_if_smooth = {genus_double_cover}")
    print("p27_label2_cover_genus_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
