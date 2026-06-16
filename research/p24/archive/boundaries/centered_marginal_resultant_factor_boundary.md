# Centered Marginal Resultant-Factor Boundary

Date: 2026-06-05

This note corrects the cyclic-resultant packaging for the reduced
right-translation product.

## Point

For a base-valued sequence

```text
F(t), t mod right,
```

one can interpolate a polynomial over `F_q(mu_right)` satisfying

```text
f(omega^t)=F(t).
```

But this interpolant has coefficients in the base field only if:

```text
F(q*t)=F(t)
```

for all `t`.  The actual small-CM determinant sequences fail this Frobenius
compatibility.

Thus the product still splits into Frobenius-orbit products of base values,
but these factors should not be called norms of a base-coefficient
interpolating polynomial without additional structure.

## Audit

Added:

```text
p24/centered_marginal_resultant_factor_audit.py
```

Small rows:

```text
D=-6719, q=6863, pair=(3,7):
  right=7
  ord_right_q=6
  sequence_distinct_values=7
  frobenius_compatibility_mismatches=5
  dft_support_size=7/7.

D=-13319, q=13463, pair=(4,7):
  right=7
  ord_right_q=3
  sequence_distinct_values=7
  frobenius_compatibility_mismatches=4
  dft_support_size=7/7.

D=-10919, q=11243, pair=(3,13):
  right=13
  ord_right_q=12
  sequence_distinct_values=13
  frobenius_compatibility_mismatches=11
  dft_support_size=13/13.
```

The DFT support is full in these rows, so there is no small spectral-support
shortcut either.

## p24 Form

For p24, `ord_211(p)=35`, so the right translations split into:

```text
{0} plus six nonzero Frobenius orbits of size 35.
```

The corrected seven-factor product is:

```text
Pi_C,right =
  F(0) * prod_{j=1}^6 prod_{t in O_j} F(t).
```

Each factor is base-field valued because the values `F(t)` are in `F_p`.
This is still a seven-factor certificate surface, but it is an **orbit-product
certificate**, not presently a norm of a base-coefficient cyclic interpolant.

The missing theorem remains:

```text
none of these seven orbit products vanishes modulo p=10^24+7.
```
