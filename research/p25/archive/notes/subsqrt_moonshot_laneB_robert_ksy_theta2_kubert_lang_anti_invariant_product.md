# P25 Lane B: Robert KSY Kubert-Lang Anti-Invariant Product

Updated: 2026-06-13 17:05 PDT

## Purpose

The raw K-trace reflection gate shows that the KSY `T`-edge product can be
viewed as an anti-invariant product after the full `K` trace.

This gate turns that into an accepted finite theorem-output interface.

## Accepted Interface

A theorem hit may emit:

```text
C = (47,28)
K = (57,0)
D = (22,3)
orientation = forward or reverse
```

The source centers are:

```text
A = C + jD + kK,  j in {-1,0,1}, k in {0,...,24}
```

Forward product:

```text
prod_A y(A) / y(-A)
```

emits exact `theta2^-1` and the finite resolvent recovers `-bridge`.

Reverse product:

```text
prod_A y(-A) / y(A)
```

emits exact `theta2` and the finite resolvent recovers `bridge`.

## Budgets

```text
compact parameter cells       = 3
center support                = 75
theta2 payload support        = 300
bridge support after resolvent = 150
support-resolvent term budget = 46800
support-resolvent union       = 11700
```

## Controls

All fail:

```text
missing K trace
collapsed K trace
truncated D segment
wrong D
shifted center
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_anti_invariant_product_rows=1/1
```

## Interpretation

This is the cleanest finite KL/KSY interface so far: a theorem source no longer
needs to emit a separate `T` edge.  It can emit a raw anti-invariant normalized-y
product over the symmetric `D` segment and full `K` trace.

The remaining moonshot debt is arithmetic legality: prove that this
anti-invariant normalized-y product is a challenge-legal modular/Siegel/Robert
unit identity.
