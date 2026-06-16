# Trace-Frame Weighted Fourier Expansion

Date: 2026-06-05

This note records the exact Cauchy-Binet expansion behind the
CM-weighted Chebotarev theorem.

## Abstract Minor

Let `n` be prime, let `F` be the `n x n` Fourier matrix, and let

```text
Lambda = diag(lambda_0,...,lambda_{n-1}).
```

For two `k`-subsets `T,S subset Z/nZ`, define the weighted Fourier minor:

```text
D_{T,S}(lambda) =
  det( (F * Lambda * F^{-1})_{T,S} ).
```

Cauchy-Binet gives:

```text
D_{T,S}(lambda)
  = sum_{U subset Z/nZ, |U|=k}
      det(F_{T,U}) * det((F^{-1})_{U,S}) * prod_{u in U} lambda_u.
```

For prime `n`, Chebotarev's theorem says every square minor of `F` is
nonzero.  Hence every coefficient in this multilinear expansion is nonzero:

```text
det(F_{T,U}) * det((F^{-1})_{U,S}) != 0.
```

So a zero of `D_{T,S}` with all `lambda_u != 0` is not a support failure.  It
is cancellation in a full-support exterior polynomial.

## Toy Check

I added:

```text
p24/weighted_fourier_cauchy_binet_toy.py
```

The toy uses `n=5`, `q=11`, `k=2`, and the nonconstant nonzero spectral twist:

```text
lambda = [1,1,1,1,2].
```

It verifies:

```text
cauchy_binet_subset_count=10
expected_subset_count=10
zero_coefficient_count=0
nonzero_term_count=10
actual_minor=0
expanded_minor=0
expansion_matches=1
```

Thus the weighted-minor failure from:

```text
p24/trace_frame_twisted_chebotarev_boundary.md
p24/trace_frame_toeplitz_schur_boundary.md
```

is a full-support cancellation among nonzero Cauchy-Binet terms.

## Actual-CM Sanity Check

The pinned trace-frame Fourier audit on the small `D=-10919` row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_top_coefficient_fourier_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1
```

reported:

```text
dft_failures=0
full_frequency_support_counts=[12,12,12]
axis_frequency_support_counts=[6,6,6]
```

So in actual small CM trace-frame rows, the Fourier identity is exact and the
coordinate functions are dense.  This supports treating p24 as a weighted
noncancellation theorem rather than a sparse-support theorem.

## p24 Interpretation

The trace-frame leading determinant can be viewed as a relative/crossed-product
version of this weighted Fourier minor:

```text
F_T * diag(Lambda_CM) * F^{-1}_S.
```

Here:

```text
S = selected smooth-axis character set, |S|=368;
T = selected Schubert/relative-coefficient coordinate set, |T|=368;
Lambda_CM = singular-moduli class-character resolvent weights.
```

An untwisted Fourier support proof would only see that:

```text
368 + 28*179 << 3107441.
```

The expansion says why that is insufficient.  The determinant is a
full-support exterior polynomial in `Lambda_CM`.  The desired theorem is:

```text
D_{T,S}(Lambda_CM) is a p-unit
```

for every beta-orbit algebra, equivalently:

```text
R_lead,Omega is a p-unit.
```

## Consequence

This closes another tempting shortcut:

```text
Chebotarev nonzero coefficients + nonzero CM Fourier weights
  => weighted determinant nonzero.
```

The implication is false by the toy.  To finish p24 by this route, one needs
one of:

```text
1. a hidden basis/block change turning the CM twist into row/column scalings;
2. a Schur/exterior identity that collapses the full-support sum for the
   actual singular-moduli weights;
3. a direct class-field/divisor/p-adic p-unit theorem for the weighted minor.
```

This is the same theorem as the determinant-line local-unit criterion, but
now stated at the exact Cauchy-Binet cancellation point.

The equivalent cyclic Toeplitz/skew-Schur form is recorded in:

```text
p24/trace_frame_toeplitz_schur_boundary.md
p24/trace_frame_translate_minor_form.md
p24/axis_crt_fourier_support_boundary.md
```

It rewrites `F * diag(lambda) * F^-1` as the cyclic Toeplitz matrix
`c_{r-s}` where `c` is the inverse DFT of `lambda`.  The same toy shows all
symbol coefficients can be nonzero while the selected minor vanishes, so the
Toeplitz form is a useful standard language, not a free p-unit proof.
The translate-minor note adds that when `lambda` is the class-character
resolvent vector, `c` is the original CM torsor sequence; the desired
determinant is therefore a selected translate-matrix minor, not the full
Dedekind group determinant.

The CRT-axis support note refines this for the selected-origin `m=66254`
axis.  Because `m` is composite and the columns are the smooth CRT-axis
characters, many Cauchy-Binet coefficients vanish for incidence reasons.
The surviving terms are spanning-hypertree terms for the complete tripartite
hypergraph with parts `2,157,211`.  This is real structure, but it leaves a
large weighted noncancellation theorem rather than a small support
certificate.

The matrix-tree factorization follow-up:

```text
p24/axis_crt_matrix_tree_factorization_toy.py
p24/axis_crt_matrix_tree_factorization_boundary.md
```

shows that the surviving coefficients are not ordinary per-edge tree weights.
They violate the pair-sum identities forced by `c(B)=C*prod_{e in B}a_e` in
exact `m=6,10,15` analogues.  Thus the weighted polynomial is genuinely
Plucker/exterior, not a standard Laplacian tree polynomial in disguised edge
variables.
