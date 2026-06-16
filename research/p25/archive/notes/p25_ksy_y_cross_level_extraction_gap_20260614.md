# P25 KSY-y Cross-Level Extraction Gap

Updated: 2026-06-14 11:46 PDT

## Purpose

The current moonshot has a strong value-side object, but it is not yet an
extraction object.

The KSY/Yang/H90 side lives at odd level:

```text
conductor source = 39
odd modular-unit level = 507 = 3 * 13^2
live objects = U_507, Y_507, Norm_156(Y_507), canonical H0
```

The practical DANGER3 extractor lives at the 2-primary level:

```text
X_1(16) parameter y
model root x
Montgomery A
marked coordinate xP16
halving chain to x0
official vpp.py verification
```

These are coprime levels:

```text
gcd(16,507) = 1
lcm(16,507) = 8112
```

So an odd-level theorem on `X_1(507)` or conductor `39` is not automatically an
`X_1(16)` extraction theorem.

## Route Classifier

```text
Y_507 / H0 value identity only:
  decision = odd_level_value_not_x16_extraction
  missing  = cross-level relation to X_1(16), or direct (A,x0)

X_1(507) modular-unit provenance:
  decision = odd_level_unit_not_x16_extraction
  missing  = theorem selecting the p25 value and a 2-primary extraction map

X_1(8112) fiber-product theorem:
  decision = cross_level_target_identified_specialization_missing
  missing  = specialized p25 relation yielding y, A, xP16, or x0

specialized X_1(16) surface payload:
  decision = x16_surface_reached_halving_or_vpp_missing
  missing  = valid halving chain and official vpp.py verification

direct verified Pomerance triple:
  decision = submission_ready
```

## Consequence

The extraction gap is not a 75-atom enumeration problem.  The 75 atoms are
fixed factors in one KSY product.

The positive moonshot artifact must now be one of:

```text
1. a theorem on the X_1(16) x_j X_1(507) fiber product,
   specialized enough to emit y, A, xP16, or x0; or

2. a direct concrete (p,A,x0) triple verified by official vpp.py.
```

Anything that only evaluates `Y_507`, `H0`, or the conductor-`39` source is
still valuable theorem progress, but it remains upstream of extraction.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_cross_level_extraction_gap_gate.py
```

Marker:

```text
ksy_y_cross_level_extraction_gap_rows=1/1
```
