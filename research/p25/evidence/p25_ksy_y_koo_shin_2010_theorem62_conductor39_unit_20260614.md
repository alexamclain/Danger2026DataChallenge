# P25 KSY-y: Koo-Shin 2010 Theorem 6.2 Conductor-39 Unit

Updated: 2026-06-14 12:19 PDT

## Purpose

The Koo-Shin full-paper screen classifies Theorem `6.2` as not being a direct
producer for the p25 75-atom product.  This note records the positive use that
remains: Theorem `6.2` certifies the compact conductor-39 source as an
`X_1(39)` one-axis product.

## Theorem 6.2 Check

At level `N=39`, use the primitive word:

```text
U_chi = -chi_39
```

and its scaled forms:

```text
V_bal = 3*U_chi
W     = 6*U_chi
```

All three satisfy the Theorem `6.2` congruences:

```text
sum_t m(t)       = 0 mod 12
sum_t m(t)*t^2   = 0 mod 39
support          = 24
```

By Koo-Shin Lemma `6.1`, each nonzero `t` expands to the full `n=0..38`
fiber, so each source word has:

```text
24 * 39 = 936 full-fiber Siegel cells
```

That is a legal one-axis source certificate, not the p25 finite product.

## Route Classifier

```text
primitive U_chi source:
  decision = source_certified_value_theorem_missing
  missing  = finite-field value/divisor theorem and Yang/Hilbert-90 descent

W followed by Yang 13-fiber lift:
  decision = period_norm_source_certified_theorem_missing
  missing  = theorem that evaluates or identifies Norm_156(Y_507)

Theorem 6.2 as exact 75-atom product:
  decision = reject_one_axis_full_fiber_not_mixed_product
  missing  = mixed C3 x C169 row graph, T edge, equal 75 atoms, and orientation

Theorem 6.2 as DANGER3 extraction:
  decision = reject_no_x16_surface_or_halving_payload
  missing  = A,xP16 surface plus x-chain, sqrt-witness chain, or vpp-verified x0
```

## Consequence

Koo-Shin 2010 Theorem `6.2` is a real positive source certificate for the
conductor-39 object.  It upgrades `U_chi`, `V_bal`, and `W` from formal words
to legal `X_1(39)` one-axis products.

It still does not close p25.  The remaining upgrade is:

```text
finite-field value/divisor theorem for the source
Yang/Hilbert-90 descent
cross-level X_1(16) surface
halving payload
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_gate.py
```

Marker:

```text
ksy_y_koo_shin_2010_theorem62_conductor39_unit_rows=1/1
```
