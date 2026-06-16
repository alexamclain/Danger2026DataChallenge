# P25 KSY-y H0 Translate Koo-Shin 6.2 Screen

Updated: 2026-06-14 15:25 PDT

## Purpose

This checkpoint tests whether the four exact legal H0 products pass the
Koo-Shin 2010 Theorem 6.2 modular-unit congruence screen at conductor `39`.
It answers a narrow question:

```text
Can Koo-Shin 6.2 certify the product words themselves?
```

It does not answer the missing value/divisor theorem.

## Screen

For each exact H0 product, use the conductor-39 source word with coefficient
`+6` on the positive residue set `P` and `-6` on the negative residue set `N`.
The screen checks:

```text
sum exponents mod 12 = 0
sum residue^2 * exponent mod 39 = 0
```

All four exact products pass.

```text
multiplier 1: exp_mod12=0, quad_mod39=0
multiplier 2: exp_mod12=0, quad_mod39=0
multiplier 4: exp_mod12=0, quad_mod39=0
multiplier 8: exp_mod12=0, quad_mod39=0
```

Each row has support `12`, coefficient counts `(-6,6),(6,6)`, and `468`
full-fiber cells under the Koo-Shin Lemma 6.1 style expansion.

## Interpretation

Positive:

```text
Koo-Shin 6.2 can certify all four exact H0 products as source-level modular-unit products.
```

Still missing:

```text
finite-field value identity with period-156 context, or
divisor/additive identity with the Hilbert-90 boundary
```

So this strengthens the theorem ask but does not close it.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_koo_shin62_screen_gate.py
```

Expected marker:

```text
ksy_y_h0_translate_koo_shin62_screen_rows=1/1
```
