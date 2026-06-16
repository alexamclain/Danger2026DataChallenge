# Centered Marginal Plucker-Kummer Descent Boundary

Date: 2026-06-06

This note records the determinant-level Kummer/descent test for the centered
right determinant sequence.

## Question

The centered target is:

```text
Delta_C(t),     t mod right.
```

A determinant-level Kummer theorem might try to construct individual descended
values:

```text
Theta(t) = unit(t) * Delta_C(t)^e.
```

This would be useful only if a nontrivial exponent makes the determinant line
semi-invariant on right Frobenius orbits.  Otherwise the honest descended
payload is the orbit product:

```text
Pi_O = prod_{t in O} Delta_C(t).
```

## Audit

Added:

```text
p24/centered_marginal_plucker_kummer_descent_audit.py
```

For each small actual-CM row it computes the normalized right sequence, the
right Frobenius orbits, and the smallest multiplicative exponent that makes
each orbit constant.

Pinned rows:

```text
D=-6719, q=6863, pair=(3,7):
  raw_descended_nontrivial_orbits=0/1
  tested_small_power_descended_nontrivial_orbits=0/1
  orbit_product_nonzero_count=2/2.

D=-13319, q=13463, pair=(4,7):
  raw_descended_nontrivial_orbits=0/2
  tested_small_power_descended_nontrivial_orbits=0/2
  orbit_product_nonzero_count=3/3.

D=-10919, q=11243, pair=(3,13):
  raw_descended_nontrivial_orbits=0/1
  tested_small_power_descended_nontrivial_orbits=0/1
  orbit_product_nonzero_count=2/2.
```

In every nontrivial right Frobenius orbit, the smallest exponent that makes
the tested determinant values constant is the trivial exponent `q-1`.

## Consequence

The centered determinant behaves like the trace-GCD determinant in this
respect: individual values do not naturally descend on nontrivial right
Frobenius orbits.  Therefore the safe p24 payload remains:

```text
seven orbit products plus inverses,
or one full-origin norm plus inverse if a closed full-origin product formula
is proved.
```

An individual Plucker-Kummer payload is still logically possible, but only
after an additional arithmetic theorem:

```text
the chosen centered Plucker determinant line is semi-invariant under the
hidden right-phase action.
```

The small actual-CM rows say not to assume this theorem.  The current
phase-aware producer should target orbit norms/Fitting determinants directly.

This matches the centered crossed-product Fitting target:

```text
p24/centered_marginal_crossed_product_fitting_target.md
```
