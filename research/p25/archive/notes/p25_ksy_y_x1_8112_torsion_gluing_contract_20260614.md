# P25 KSY-y X1(8112) Torsion-Gluing Contract

Updated: 2026-06-14 12:00 PDT

## Purpose

The bridge-theorem intake says a useful theorem must glue the odd
KSY/Yang/H90 target to the practical `X_1(16)` extractor over the same
`j`-line.

This note records the constructive torsion arithmetic behind that gluing.

## Coprime Levels

```text
16 * 507 = 8112
gcd(16,507) = 1
```

If `R` has exact order `8112` on an elliptic curve, then:

```text
[507]R has exact order 16
[16]R  has exact order 507
```

For normalized projections that recombine back to `R`:

```text
507^-1 mod 16 = 3
16^-1 mod 507 = 412

P16  = [3*507]R  = [1521]R
Q507 = [412*16]R = [6592]R

P16 + Q507 = R
```

The gate verifies the order and recombination arithmetic:

```text
ord([1521]R) = 16
ord([6592]R) = 507
1521 + 6592 = 8113 = 1 mod 8112
```

Conversely, if a theorem supplies an exact `16`-torsion point and an exact
`507`-torsion point on the same curve, their sum has exact order `8112`.

## Route Classifier

```text
odd-level value only:
  decision = odd_component_not_extraction
  missing  = same-curve X_1(16) component or order-8112 generator

generic X_1(16) surface only:
  decision = x16_component_not_ksy_bridge
  missing  = exact odd KSY/Yang/H90 component on the same curve

independent level-16 and level-507 data:
  decision = reject_unglued_components
  missing  = same j-invariant or same elliptic curve

same-curve P16 and Q507:
  decision = construct_order_8112_generator_then_specialize_x16
  missing  = practical y, model root, A, and xP16 extraction data

order-8112 generator R:
  decision = project_R_to_P16_and_Q507_then_specialize
  missing  = practical X_1(16) y, model root, A, and xP16

order-8112 bridge with X_1(16) surface:
  decision = x16_surface_reached_halving_or_vpp_missing
  missing  = valid halving chain from xP16 to x0
```

## Consequence

The constructive bridge target can now be stated in either of two equivalent
forms:

```text
1. same-curve exact P16 and Q507 tied to the p25 odd target; or
2. an exact order-8112 point R tied to the p25 odd target.
```

But this is still only the gluing layer.  It does not replace the practical
Montgomery extraction surface:

```text
X_1(16) y
model root x
A = N(y)/(4*(y-1)^4)
xP16 = x/(x-y)
halving chain to x0
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_torsion_gluing_contract_gate.py
```

Marker:

```text
ksy_y_x1_8112_torsion_gluing_contract_rows=1/1
```
