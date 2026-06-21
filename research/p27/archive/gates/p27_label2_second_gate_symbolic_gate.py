#!/usr/bin/env python3
"""Symbolic label-2 second-gate screen for the p27 X1(16) tower.

This is target-independent algebra, but it is recorded in p27 because the
p27 sign of the compact-D selector is the one currently under test.
"""

from __future__ import annotations

import sympy as sp


def reduce_w(expr: sp.Expr, x: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    poly = sp.Poly(sp.together(expr).as_numer_denom()[0], w)
    return sp.factor(poly.rem(sp.Poly(w**2 - (x**3 - x), w)).as_expr())


def main() -> int:
    x, w, t = sp.symbols("X W T")

    # Label 2 from the residual first-lift elliptic cover E: W^2 = X^3-X.
    y = 2 * x / (x - 1)
    d16 = sp.factor(y * (y - 2) * (y**2 - 2) * (y**2 - 2 * y + 2))
    t2 = sp.factor(d16 * (x - 1) ** 6 / 16)
    expected_t2 = x * (x**2 + 1) * (x**2 + 2 * x - 1)
    assert sp.factor(t2 - expected_t2) == 0

    # Compact-D criterion copied from label2_compact_d_class128.
    mt_coeff = sp.factor(
        2 * w * x**2 + 2 * w * x + x**4 + 2 * x**3 - 2 * x - 1
    )
    m0 = sp.factor(
        w * x**5
        + 3 * w * x**4
        + 2 * w * x**3
        + 2 * w * x**2
        + w * x
        - w
        + 2 * x**6
        + 4 * x**5
        + 4 * x**3
        - 2 * x**2
    )
    v = w * (x**2 + 1) / x**2
    criterion = sp.factor(x * v * (m0 + mt_coeff * t))

    # Norm from T to the residual elliptic field.
    norm_t = sp.factor(x**2 * v**2 * (m0**2 - mt_coeff**2 * expected_t2))
    norm_t_num = reduce_w(norm_t, x, w)
    norm_t_den = sp.together(norm_t).as_numer_denom()[1]
    expected_norm_t_num = sp.factor(
        4
        * x**3
        * (x - 1)
        * (x + 1)
        * (x**2 + 1) ** 3
        * (x**2 + 2 * x - 1)
        * (4 * w * x**2 + 4 * w * x + x**4 + 6 * x**3 - 2 * x - 1)
    )
    assert sp.factor(norm_t_num - expected_norm_t_num) == 0
    assert sp.factor(norm_t_den - x**2) == 0

    # The remaining W-linear factor has square norm to the X-line.
    linear = 4 * w * x**2 + 4 * w * x + x**4 + 6 * x**3 - 2 * x - 1
    norm_tw_linear = reduce_w(linear * linear.subs(w, -w), x, w)
    expected_norm_tw_linear = (x**2 + 1) ** 2 * (x**2 - 2 * x - 1) ** 2
    assert sp.factor(norm_tw_linear - expected_norm_tw_linear) == 0

    print("p27 label2 second-gate symbolic screen")
    print(f"label2_y = {sp.factor(y)}")
    print(f"T2 = {expected_t2}")
    print(f"mt_coeff = {mt_coeff}")
    print(f"m0 = {m0}")
    print(f"compactD_criterion = {criterion}")
    print(f"norm_T_num = {norm_t_num}")
    print(f"norm_T_den = {norm_t_den}")
    print(f"norm_T_remaining_linear = {linear}")
    print(f"norm_TW_remaining_linear = {norm_tw_linear}")
    print("x_line_quadratic_character_gate = 0")
    print("second_gate_lives_on_mixed_X_W_T_cover = 1")
    print("p27_label2_second_gate_symbolic_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
