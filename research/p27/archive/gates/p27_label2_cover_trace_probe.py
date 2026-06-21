#!/usr/bin/env python3
"""Small-prime trace probe for the p27 label-2 second-gate cover.

This is not a replacement for a Sage/Magma zeta-function computation.  It is a
cheap local diagnostic: count the intermediate biquadratic cover C and the
second-gate double cover D over several small prime fields, then test whether
the new Prym trace looks like an obvious combination of the known C factors.
"""

from __future__ import annotations

from itertools import product


PRIMES = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
N_SERIES = 12


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def root_count(a: int, p: int) -> int:
    c = legendre(a, p)
    return 1 + c


def roots(a: int, p: int) -> list[int]:
    a %= p
    return [x for x in range(p) if x * x % p == a]


def f_scalar(x: int, p: int) -> int:
    return (x * x * x - x) % p


def g_scalar(x: int, p: int) -> int:
    x2 = x * x % p
    return x * (x2 + 1) * (x2 + 2 * x - 1) % p


def wt_squarefree_scalar(x: int, p: int) -> int:
    return (x - 1) * (x + 1) * (x * x + 1) * (x * x + 2 * x - 1) % p


def compact_parts_scalar(x: int, w: int, p: int) -> tuple[int, int]:
    x2 = x * x % p
    mt = (x + 1) * (2 * w * x + x**3 + x2 - x - 1) % p
    m0 = (x2 + 1) * (x2 + 2 * x - 1) * (w * x + w + 2 * x2) % p
    return mt, m0


def h_scalar(x: int, w: int, t: int, p: int) -> int:
    mt, m0 = compact_parts_scalar(x, w, p)
    return w * (x * x + 1) * (m0 + mt * t) * pow(x, p - 2, p) % p


def add(a: list[int], b: list[int], p: int) -> list[int]:
    return [(x + y) % p for x, y in zip(a, b)]


def sub(a: list[int], b: list[int], p: int) -> list[int]:
    return [(x - y) % p for x, y in zip(a, b)]


def scale(c: int, a: list[int], p: int) -> list[int]:
    return [(c * x) % p for x in a]


def mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * N_SERIES
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b[: N_SERIES - i]):
            if bj:
                out[i + j] = (out[i + j] + ai * bj) % p
    return out


def pow_series(a: list[int], e: int, p: int) -> list[int]:
    out = [0] * N_SERIES
    out[0] = 1
    base = a
    while e:
        if e & 1:
            out = mul(out, base, p)
        base = mul(base, base, p)
        e >>= 1
    return out


def const(c: int, p: int) -> list[int]:
    out = [0] * N_SERIES
    out[0] = c % p
    return out


def var() -> list[int]:
    out = [0] * N_SERIES
    out[1] = 1
    return out


def order(a: list[int]) -> int:
    for i, ai in enumerate(a):
        if ai:
            return i
    return N_SERIES


def f_series(x: list[int], p: int) -> list[int]:
    return sub(pow_series(x, 3, p), x, p)


def g_series(x: list[int], p: int) -> list[int]:
    x2 = mul(x, x, p)
    return mul(x, mul(add(x2, const(1, p), p), add(sub(x2, const(1, p), p), scale(2, x, p), p), p), p)


def solve_branch_x(a: int, p: int) -> list[int]:
    x = const(a, p)
    for k in range(1, N_SERIES):
        target = 1 if k == 2 else 0
        known = f_series(x, p)[k]
        trial = x[:]
        trial[k] = (trial[k] + 1) % p
        delta = (f_series(trial, p)[k] - known) % p
        if delta:
            x[k] = (x[k] + (target - known) * pow(delta, p - 2, p)) % p
    return x


def sqrt_ramified(rhs: list[int], y1: int, p: int) -> list[int]:
    y = [0] * N_SERIES
    y[1] = y1 % p
    for k in range(2, N_SERIES):
        if k + 1 >= N_SERIES:
            break
        known = mul(y, y, p)[k + 1]
        y[k] = ((rhs[k + 1] - known) * pow(2 * y1 % p, p - 2, p)) % p
    return y


def compact_parts_series(x: list[int], w: list[int], p: int) -> tuple[list[int], list[int]]:
    x2 = mul(x, x, p)
    mt = mul(
        add(x, const(1, p), p),
        add(scale(2, mul(w, x, p), p), sub(add(pow_series(x, 3, p), x2, p), add(x, const(1, p), p), p), p),
        p,
    )
    m0 = mul(
        add(x2, const(1, p), p),
        mul(add(sub(x2, const(1, p), p), scale(2, x, p), p), add(add(mul(w, x, p), w, p), scale(2, x2, p), p), p),
        p,
    )
    return mt, m0


def h_series_at_x0(t_sign: int, p: int) -> list[int]:
    x = solve_branch_x(0, p)
    w = var()
    t = sqrt_ramified(g_series(x, p), t_sign % p, p)
    x2 = mul(x, x, p)
    mt, m0 = compact_parts_series(x, w, p)
    numerator = mul(w, mul(add(x2, const(1, p), p), add(m0, mul(mt, t, p), p), p), p)
    ox = order(x)
    shifted = numerator[ox:] + [0] * ox
    return scale(pow(x[ox], p - 2, p), shifted, p)


def normalized_cover_count_from_series(h: list[int], p: int) -> int:
    o = order(h)
    c = h[o] if o < N_SERIES else 0
    if o % 2:
        return 1
    return 2 if legendre(c, p) == 1 else 0


def x0_d_count(p: int) -> int:
    total = 0
    for sign in [1, p - 1]:
        total += normalized_cover_count_from_series(h_series_at_x0(sign, p), p)
    return total


def infinity_d_count(p: int) -> int:
    # Laurent check in p27_label2_cover_genus_probe.py gives two infinity
    # classes with even orders -18 and -12 and leading coefficient 2.
    return 2 * (2 if legendre(2, p) == 1 else 0)


def count_w_curve(p: int) -> int:
    return sum(root_count(f_scalar(x, p), p) for x in range(p)) + 1


def count_t_curve(p: int) -> int:
    return sum(root_count(g_scalar(x, p), p) for x in range(p)) + 1


def count_wt_curve(p: int) -> int:
    return sum(root_count(wt_squarefree_scalar(x, p), p) for x in range(p)) + 2


def count_c(p: int) -> int:
    affine = 0
    for x in range(p):
        affine += root_count(f_scalar(x, p), p) * root_count(g_scalar(x, p), p)
    return affine + 2


def count_d(p: int) -> int:
    total = 0
    for x in range(1, p):
        for w, t in product(roots(f_scalar(x, p), p), roots(g_scalar(x, p), p)):
            total += root_count(h_scalar(x, w, t, p), p)
    total += x0_d_count(p)
    total += infinity_d_count(p)
    return total


def find_small_combo(rows: list[dict[str, int]], keys: list[str], target: str, bound: int = 8) -> tuple[int, ...] | None:
    for coeffs in product(range(-bound, bound + 1), repeat=len(keys)):
        if all(c == 0 for c in coeffs):
            continue
        if all(sum(c * row[k] for c, k in zip(coeffs, keys)) == row[target] for row in rows):
            return coeffs
    return None


def main() -> int:
    rows = []
    print("p27 label2 cover trace probe")
    print("p #W aW #T aT #WT aWT aWT_common_branch_adj #C aC #D aD aPrym")
    for p in PRIMES:
        n_w = count_w_curve(p)
        n_t = count_t_curve(p)
        n_wt = count_wt_curve(p)
        n_c = count_c(p)
        n_d = count_d(p)
        a_w = p + 1 - n_w
        a_t = p + 1 - n_t
        a_wt = p + 1 - n_wt
        # The V4 cover has common branch at X=0.  The smooth squarefree
        # third quotient trace needs this +1 correction to match C.
        a_wt_adj = a_wt + 1
        a_c = p + 1 - n_c
        a_d = p + 1 - n_d
        a_prym = a_d - a_c
        rows.append(
            {
                "p": p,
                "aW": a_w,
                "aT": a_t,
                "aWT": a_wt,
                "aWTadj": a_wt_adj,
                "aC": a_c,
                "aD": a_d,
                "aPrym": a_prym,
            }
        )
        print(
            f"{p} {n_w} {a_w} {n_t} {a_t} {n_wt} {a_wt} {a_wt_adj} "
            f"{n_c} {a_c} {n_d} {a_d} {a_prym}"
        )

    raw_offsets = [row["aC"] - (row["aW"] + row["aT"] + row["aWT"]) for row in rows]
    c_ok = all(row["aC"] == row["aW"] + row["aT"] + row["aWTadj"] for row in rows)
    print(f"intermediate_raw_common_branch_offsets = {raw_offsets}")
    print(f"intermediate_trace_decomposition_common_branch_adjusted_ok = {int(c_ok)}")
    combo = find_small_combo(rows, ["aW", "aT", "aWTadj"], "aPrym", bound=8)
    print(f"prym_trace_small_combo_known_factors = {combo if combo is not None else 'none_bound_8'}")
    print("p27_label2_cover_trace_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
