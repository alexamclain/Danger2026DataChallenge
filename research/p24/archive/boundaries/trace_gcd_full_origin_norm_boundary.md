# Trace-GCD Full-Origin Norm Boundary

Date: 2026-06-05

This note separates two superficially similar ideas:

```text
good:
  use a closed modular/Fitting/Borcherds product formula for the full-origin
  determinant norm, then descend to the 211-term right norm;

bad:
  compute the full-origin norm by expanding over the whole CM torsor or by
  constructing the full Hilbert class polynomial.
```

The origin-norm power theorem shows that the first idea would land on the
correct finite certificate.  The second idea is only class enumeration in a
cleaner suit.

## Accounting

The p24 numbers are:

```text
p = 10^24 + 7
sqrt(p) = 10^12
h = 205880396014
m = 66254 = 2 * 157 * 211
n = 3107441
right = 211
m/right = 314
n*m/right = 975736474
```

The finite trace-GCD payloads are tiny:

```text
211 values plus inverses: 422 base-field elements
7 orbit products plus inverses: 14 base-field elements
one norm plus inverse: 2 base-field elements
```

But a naive full-origin product over the class torsor has degree:

```text
h = 205880396014 = 0.205880396014 * sqrt(p).
```

That is below `sqrt(p)` for this fixed number, but it is still class-number
scale and does not give the desired asymptotic improvement.  The selected
tower and factorized routes remain the real sub-sqrt degree surfaces:

```text
2 + 157 + 211 + 3107441 = 3107811
66254 + 3107441 = 3173695
```

Both are about `3.1e-6 * sqrt(p)` for p24.

The accounting script is:

```text
p24/full_origin_norm_vs_class_enumeration_accounting.py
```

## What Full-Origin Symmetry Gives

The new origin-norm power audit shows, in the pinned actual-CM row, that
larger origin products are powers of the reduced right product:

```text
prod_{all origins} Delta_origin
  = unit * Pi_right^(n*m/right).
```

Thus a closed formula proving the full-origin product is a p-unit would prove
`Pi_right` is a p-unit.  The finite implication is recorded in:

```text
p24/lean/OriginNormPowerGate.lean
p24/lean/TraceGcdFullOriginBorcherdsGate.lean
p24/trace_gcd_full_origin_borcherds_gate.md
```

This is a useful bridge because known CM product formulas usually see global
CM norms more naturally than a selected right-origin product.

## Why the Naive Global Norm Is Not Enough

The full-origin product is symmetric under cycling the embedded torsor.  In
principle, any symmetric polynomial in all `h` CM roots can be written in the
Hilbert class polynomial coefficients.  But producing those coefficients is
the original class-set-scale work.  It does not beat sqrt asymptotically.

So the product-formula route must do more:

```text
construct the determinant section as a recognized modular/Borcherds/Fitting
object whose CM norm is computable without first listing the class set.
```

The existing divisor diagnostics caution against the easy versions:

```text
p24/packet_scalar_divisor_shape_boundary.md
p24/phase_divisor_heegner_support_boundary.md
p24/packet_scalar_edge_shape_boundary.md
```

Plain `j`, one-edge, and small-Heegner-supported explanations look generic in
small non-genus rows.  A successful divisor theorem would therefore have to
retain the non-genus phase, not just recognize a low-degree function of the
selected `j`.

## Current Theorem Target

The full-origin route is viable only in this form:

```text
Construct a phase-aware automorphic/Fitting determinant section Psi_trace
whose CM norm equals unit * prod_all_origins Delta_origin, and prove that
CM norm is a p-unit at p = 10^24 + 7.
```

Then:

```text
Psi_trace norm p-unit
  => full-origin determinant product p-unit
  => Pi_right p-unit
  => all 211 trace-GCD determinants nonzero
  => representative Schubert/support gate
  => mixed p24 certificate.
```

The finite version of this implication is now checked as
`selected_good_from_full_origin_borcherds` in:

```text
p24/lean/TraceGcdFullOriginBorcherdsGate.lean
```

Without such a closed formula, the right-norm route should stay focused on
constructing `f_trace` directly in:

```text
O_F[Y]/(Y^211 - 1),
```

using embedded relative class-character or Kummer data for the `157` and
`211` tower layers.
