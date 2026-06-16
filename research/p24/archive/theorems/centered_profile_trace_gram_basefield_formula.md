# Centered Profile Trace-Gram Base-Field Formula

Date: 2026-06-05

This note records the base-field formula behind the centered-profile
trace-Gram certificate.

## Root Trace

For p24, `p` is primitive modulo `157`, so:

```text
L = F_p(mu_157),       [L:F_p] = 156.
```

For `zeta = mu_157`, the trace values are:

```text
Tr_{L/F_p}(1) = 156,
Tr_{L/F_p}(zeta^a) = -1       for a != 0 mod 157.
```

Equivalently:

```text
Tr(zeta^a) = -1 + 157*[a=0].
```

## Centered Formula

Let `a=(a_r)` and `b=(b_r)` be centered coefficient vectors on
`Z/157Z`:

```text
sum_r a_r = 0,
sum_r b_r = 0.
```

Set:

```text
A = sum_r a_r zeta^r,
B = sum_r b_r zeta^r.
```

Then:

```text
Tr_{L/F_p}(A*B) = 157 * sum_r a_r b_{-r}.
```

The `-sum a * sum b` term cancels exactly because the coefficient vectors are
centered.

## p24 Profile Gram

Write the centered right profile as:

```text
G_s^0 = sum_r a_{r,s} zeta^r,
sum_r a_{r,s}=0.
```

For the leading profile window `s=0,...,155`, let `A_lead` be the
`157 x 156` base-field coefficient matrix with columns `a_{*,s}`, and let
`J_inv` be the permutation matrix for:

```text
r -> -r mod 157.
```

Then the trace-Gram matrix is:

```text
Gamma_profile_leading = 157 * A_lead^T * J_inv * A_lead.
```

Therefore:

```text
det(Gamma_profile_leading)
  = 157^156 * det(A_lead^T * J_inv * A_lead).
```

Since `157` is a p-unit for `p=10^24+7`, this gives a completely base-field
determinant target equivalent to the centered-profile Moore p-unit:

```text
det(A_lead^T * J_inv * A_lead) != 0 mod p.
```

## Dropped-Row Minor Form

The columns of `A_lead` are centered:

```text
sum_r a_{r,s}=0.
```

Use coordinates on the zero-sum hyperplane by dropping row `r=0`.  If
`D_profile_leading` is the determinant of the resulting `156 x 156` matrix,
then the inversion pairing on these coordinates has matrix:

```text
P_inv + 1*1^T,
```

where `P_inv` permutes the nonzero residues by `r -> -r`.  Its determinant is:

```text
det(P_inv + 1*1^T) = (-1)^78 * 157 = 157.
```

Therefore:

```text
det(A_lead^T * J_inv * A_lead)
  = 157 * D_profile_leading^2.
```

Combining with the trace factor gives:

```text
Gamma_profile_leading
  = 157^157 * D_profile_leading^2.
```

Since `157` is not divisible by `p`, the centered-profile certificate is
equivalent to the ordinary base-field minor:

```text
D_profile_leading != 0 mod p.
```

Dropping a different left residue row changes `D_profile_leading` only by a
unit sign, because all columns lie in the zero-sum hyperplane.

## Relation To Moore

The same trace-Gram determinant also satisfies:

```text
Gamma_profile_leading = M_profile_leading^2,
```

where `M_profile_leading` is the Moore determinant of the first `156`
centered profile values.  Thus the following are equivalent p-unit targets:

```text
M_profile_leading != 0,
det(Gamma_profile_leading) != 0,
det(A_lead^T * J_inv * A_lead) != 0,
D_profile_leading != 0.
```

The last form is attractive because it avoids adjoining `mu_157` and
`mu_211`: it is a base-field determinant of the centered Hermitian marginal
coefficients with the explicit inversion pairing on the left index.

## Toy Verification

Added:

```text
p24/centered_profile_trace_formula_toy.py
p24/centered_profile_moore_trace_gram_identity_toy.py
p24/centered_profile_base_minor_identity_toy.py
```

The trace formula toy:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_profile_trace_formula_toy.py --q 3 --ell 7 --trials 200
```

reports:

```text
trace_formula_mismatches=0
noncentered_formula_mismatches=100
centered_trace_equals_ell_times_inversion_dot=1
centering_hypothesis_is_used=1
```

The Moore/Gram identity toy reports:

```text
identity_mismatches=0
trace_gram_equals_moore_square=1
trace_gram_punit_iff_moore_punit=1
```

The dropped-row minor toy reports:

```text
pairing_det_matches_formula=1
gram_identity_mismatches=0
base_gram_equals_unit_times_minor_square=1
base_minor_punit_iff_base_gram_punit=1
```

## Current Arithmetic Target

The centered-profile certificate can now be stated without extension-field
coordinates:

```text
For the actual p24 centered Hermitian marginal coefficient matrix A_lead,
the dropped-row determinant D_profile_leading is nonzero modulo p.
```

This would prove:

```text
rank_Fp C_{157,211}=156,
```

and hence the mixed Schur correction needed by the p24 certificate.  It does
not by itself prove the stronger delete-one/right-support statement supplied
by `L_rep`.
