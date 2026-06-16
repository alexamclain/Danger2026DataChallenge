# Trace-GCD Metric Schur Refinement

Date: 2026-06-06

This note corrects the Gram bridge to use the intrinsic trace metric.

## Why The Ordinary Dot Gram Is Not Enough

The finite Schur identity was first written with the standard coordinate dot
product:

```text
det([A;B][A;B]^T) det(N^T N)
  = det(A A^T) det(BN)^2.
```

This is correct finite linear algebra for a chosen coordinate basis.  But in
the trace-GCD construction the rows of `A` and `B` are trace functionals:

```text
row_x(b_i) = Tr_{L/F_p}(x b_i)
```

for a chosen basis `b_i` of `L = F_p(mu_157)`.  The ordinary dot product on
these coordinate rows is not invariant under a change of basis.  Therefore
`det(A A^T)` is a useful plumbing check but not the natural arithmetic payload.

The finite-field toy:

```text
p24/metric_schur_identity_toy.py
```

reports, for example:

```text
q=101, r=5, s=3:
metric_mismatches=0
naive_basis_zero_mismatches=19
metric_basis_zero_mismatches=0
```

so lower-dimensional naive Gram nonzero-ness can change under basis change.

## Metric-Aware Identity

Let `G` be the primal trace-pairing matrix in the selected basis:

```text
G_ij = Tr_{L/F_p}(b_i b_j).
```

Then `G^{-1}` is the induced dual metric on row covectors.  If `N` is a basis
matrix for `ker A` in primal coordinates, the invariant Schur identity is:

```text
det([A;B] G^{-1} [A;B]^T) det(N^T G N)
  = det(A G^{-1} A^T) det(BN)^2.
```

This is just the ordinary Schur identity after an arbitrary metric
trivialization, but it is coordinate-invariant.  It is also the form that makes
the prefix Gram determinant equal to the restricted trace pairing on the actual
field elements corresponding to the trace rows.

## Correct Prefix Obstruction

With the metric-aware Gram, the prefix theorem is again intrinsic:

```text
P_t = det(A_t G^{-1} A_t^T) != 0
```

if and only if the prefix field-value subspace `U_t` is nondegenerate under:

```text
<x,y> = Tr_{L/F_p}(xy).
```

Equivalently:

```text
U_t cap U_t^perp = 0.
```

The kernel Gram determinant is:

```text
K_t = det(N_t^T G N_t),
```

so `P_t != 0` forces `K_t != 0` because `ker A_t = U_t^perp` for the
nondegenerate trace metric.

## Actual-CM Check

The actual-CM Schur falsifier now has:

```text
--metric-aware
```

which computes the trace metric `G` from the selected subfield power basis and
uses the invariant identity above.  A bounded nonzero-prefix run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 1 --max-cases 8 --max-abs-D 30000 \
  --q-stop 120000 --max-origin-shifts 40
```

found the same small actual-CM row as the coordinate-dot run:

```text
D=-2159 q=3923 h=60 m=20 n=3 pair=(4,4) left=L2
tail_zero=0
schur_fail=0
prefixGram0=0
fullGram0=0
kernelGram0=0
right_class_mismatches=0
orbitSchur=1
```

The orbit product values differ from the coordinate-dot version, as they
should, but the metric Schur identity is the arithmetic form worth pursuing.

A slightly broader bounded run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/orbitwise_schur_bridge_falsifier.py \
  --metric-aware --include-linear \
  --max-factor-degree 10 --max-extension-degree 10 \
  --min-left-orbit-len 2 --require-square-tail --min-prefix-len 1 \
  --max-rows 4 --max-cases 30 --max-abs-D 60000 \
  --q-stop 250000 --max-origin-shifts 60
```

again found no metric Schur failures, no prefix/full/kernel Gram zeros, and
no right-class mismatches across four actual small-CM rows.  The rows are
still tiny, but they keep the metric-Gram route alive as a falsifiable theorem
shape.

## Consequence

The 28-element Gram payload remains possible, but it must mean:

```text
P_O = prod_t det(A_t G^{-1} A_t^T),
L_O = prod_t det([A_t;B_t] G^{-1} [A_t;B_t]^T),
```

plus their inverses for the seven right Frobenius orbits.  The hard theorem is
still the prefix self-orthogonal exclusion.  The direct seven-orbit Fitting
payload remains smaller and cleaner unless the metric Gram products admit a
better Hermitian/autocorrelation p-unit proof.
