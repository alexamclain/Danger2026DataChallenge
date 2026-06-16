# Kernel-Tail Schur Identity Boundary

Date: 2026-06-05

This note records a finite determinant identity for the current trace-gcd
certificate.

## Setup

Let `A` be the prefix trace matrix and `B` the selected tail trace matrix:

```text
A : L -> F_p^140,
B : L -> F_p^16.
```

In the p24 representative row:

```text
rank A = 140,
K = ker A has dimension 16,
B|_K is the selected tail-on-kernel map.
```

The trace-gcd p-unit is:

```text
det(B|_K) != 0.
```

## Pluecker Quotient Identity

For a finite `r+s=d` model, choose pivot columns `X` for `A` and complementary
columns `Y`.  In ordered coordinates `X,Y`, a kernel basis is:

```text
N = [ -A_X^(-1) A_Y ; I_s ].
```

Then:

```text
det([A;B]_{X,Y}) = det(A_X) * det(BN).
```

Thus the tail-on-kernel determinant is literally the quotient:

```text
det(B|_K) = det(leading) / det(prefix-pivot).
```

This is exact and useful for checking conventions, but it is not a new proof
by itself: it repackages the same leading Moore/Pluecker p-unit.

## Gram Schur Identity

If the prefix row space is nondegenerate for the chosen dot pairing, then a
Schur-complement identity gives:

```text
det([A;B][A;B]^T) * det(N^T N)
  = det(A A^T) * det(BN)^2.
```

So a possible stronger arithmetic route is:

```text
prefix Gram p-unit
+ full leading Gram p-unit
+ kernel Gram p-unit
=> tail-on-kernel p-unit.
```

The caution is important: over finite fields, full row rank does not imply
nondegenerate restricted trace form.  This route is strictly stronger than
the trace-gcd determinant route.

## Toy

Added:

```text
p24/kernel_tail_schur_identity_toy.py
```

Runs:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/kernel_tail_schur_identity_toy.py \
  --q 101 --r 5 --s 3 --trials 1000
```

reported:

```text
full_prefix=1000
full_leading=992
tail_det_nonzero=992
pluecker_mismatches=0
prefix_rank_gram_singular=7
gram_checked=993
gram_mismatches=0.
```

Small-field controls:

```text
q=3, r=8, s=4:
  full_prefix=995
  full_leading=528
  tail_det_nonzero=528
  prefix_rank_gram_singular=368
  prefix_kernel_gram_zero_mismatches=0
  gram_checked=627
  gram_mismatches=0.

q=2, r=8, s=4:
  full_prefix=953
  full_leading=278
  tail_det_nonzero=278
  prefix_rank_gram_singular=547
  gram_checked=406
  gram_mismatches=0.
```

The identities hold exactly.  The Gram route is often unavailable because the
prefix rank can be full while the prefix Gram is singular.

For the arithmetic trace pairing, the invariant version replaces the ordinary
dot Gram by the metric-aware identity:

```text
det([A;B] G^{-1} [A;B]^T) det(N^T G N)
  = det(A G^{-1} A^T) det(BN)^2.
```

This correction is recorded in:

```text
p24/trace_gcd_metric_schur_refinement.md
p24/metric_schur_identity_toy.py
```

The toy now also checks the determinant-line refinement:

```text
prefix_kernel_gram_zero_mismatches=0
```

For a nondegenerate ambient trace pairing, `ker A` is the orthogonal
complement of the prefix row space.  Thus prefix Gram nonzero implies kernel
Gram nonzero.  The more natural finite payload is therefore:

```text
prefix Gram p-unit
+ full leading Gram p-unit
=> kernel Gram p-unit
=> tail-on-kernel p-unit.
```

This avoids treating the kernel Gram determinant as an independent
basis-dependent arithmetic object.

## Actual-CM Orbit Falsifier

The finite identity is now also checked on actual small-CM trace-GCD rows by:

```text
p24/orbitwise_schur_bridge_falsifier.py
p24/orbitwise_schur_bridge_falsifier.md
```

On the pinned `D=-13319, q=13463, m=28, pair=(4,7)` row it reports, for both
omitted right blocks:

```text
tail_zero=0
schur_fail=0
prefixGram0=0
fullGram0=0
kernelGram0=0
right_class_mismatches=0
orbitSchur=1 on every Frobenius orbit of Z/7Z
```

This pinned row is tail-only (`prefix_len=0`), so it verifies the orbit
plumbing rather than a hard prefix-Gram theorem.  A bounded nonzero-prefix
search found only tiny `L=2` rows before larger-left calibration became row
discovery.  The lesson is that the Schur bridge is finite-algebraically sound
but remains a stronger p-unit route.

The refined p24 payload discussion is:

```text
p24/trace_gcd_prefix_full_gram_payload_refinement.md
p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md
p24/trace_gcd_metric_schur_refinement.md
```

The self-orthogonal obstruction guardrail is:

```text
p24/prefix_gram_obstruction_toy.py
```

## Consequence

For p24, this gives two proof surfaces:

```text
direct route:
  prove det(B|_K) is a p-unit;

stronger Gram route:
  prove the relevant prefix and full trace-Gram determinants are p-units
  and use the Schur identity.
```

The direct route remains the smallest theorem.  The Gram route might be more
natural for p-adic local-lattice or Borcherds methods, but it is a stronger
selected-prime theorem and cannot be inferred from rank alone.
