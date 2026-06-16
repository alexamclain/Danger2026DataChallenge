# Axis CRT Matrix-Tree Factorization Boundary

Date: 2026-06-05

This note tests whether the CRT-axis Cauchy-Binet support collapse can be
upgraded into an ordinary matrix-tree compression.

## Question

The selected-origin trace-frame minor has Cauchy-Binet coefficients

```text
c(U) = det(F_{T,U}) det((F^{-1})_{U,S_axis})
```

for `|U| = |S_axis|`.  The CRT-axis support note shows that the nonzero
subsets `U` are incidence hypertrees in the complete multipartite model.

The stronger hope was:

```text
c(U) = C * prod_{u in U} a_u
```

on the surviving hypertrees, after a harmless change of edge variables.  If
true, an ordinary graph/hypergraph matrix-tree determinant could compress the
weighted polynomial.

## Pair-Sum Test

The script:

```text
p24/axis_crt_matrix_tree_factorization_toy.py
```

uses a necessary identity for every ordinary edge-weight factorization.  If

```text
c(B) = C * prod_{e in B} a_e,
```

then any two pairs of bases with the same edge-count vector must satisfy:

```text
c(B1)c(B2) = c(B3)c(B4)

whenever

1_B1 + 1_B2 = 1_B3 + 1_B4.
```

A single violation rules out per-edge matrix-tree weights for that coefficient
family.

The finite implication is Lean-checked in:

```text
p24/lean/MatrixTreeFactorizationObstructionGate.lean
```

Lean does not certify the finite-field determinant arithmetic; the Python toy
does that.  Lean checks the logical gate: an edge-factorized coefficient
family must satisfy the pair-sum product relation, so one unequal-product
witness disproves that factorization type.

## Results

Exact small two-component rows:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_crt_matrix_tree_factorization_toy.py \
  --m 6 --m 10 --m 15 --max-subsets 10000 --max-pairs 500000
```

found violations for the actual full Cauchy-Binet coefficient:

```text
m=6, q=13:
  full_coeff pair_sum_status=violated
  product_a=12, product_b=10

m=10, q=31:
  full_coeff pair_sum_status=violated
  product_a=12, product_b=10

m=15, q=31:
  full_coeff pair_sum_status=violated
  product_a=28, product_b=8
```

The separate factors also violate:

```text
axis_det pair_sum_status=violated
prefix_det pair_sum_status=violated
```

The same obstruction appears in a sampled tripartite analogue:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_crt_matrix_tree_factorization_toy.py \
  --m 30 --max-subsets 20000 --max-pairs 500000

m=30, q=61:
  full_coeff pair_sum_status=violated
  product_a=54, product_b=9
```

## Consequence

The complete multipartite hypertree model is still the correct support
language:

```text
nonzero Cauchy-Binet terms = CRT-axis spanning hypertrees.
```

But the actual coefficients are not those of an ordinary edge-weighted
matrix-tree polynomial.  The prefix Vandermonde/Plucker determinant and the
axis Fourier determinant carry global basis interactions that cannot be
absorbed into one scalar weight per edge.

So the matrix-tree route is now bounded:

```text
ordinary per-edge Laplacian determinant compression is ruled out;
mixed Plucker / exterior determinant identities remain possible;
any successful proof must use the CM weights or a p-unit theorem, not only
the support matroid.
```

## Updated Theorem Target

The surviving p24 proof target is the Plucker-weighted CRT hypertree
p-unit statement:

```text
sum_{CRT hypertrees H}
  det(F_{T,H}) det((F^{-1})_{H,S_axis}) prod_{h in H} lambda_h

is a p-unit at the p24 CM spectral point lambda = Lambda_CM.
```

Equivalently, this is still the full leading determinant-line theorem:

```text
delta_all in A_all^*
Fitt_0(coker T_lead,all) = A_all
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }
  = {0}.
```

The full-top-three condition `W_axis cap F_27={0}` is a necessary consequence
but not a sufficient replacement for the selected leading minor.

Probability, statistics, and CS theory remain useful only when lifted to a
pointwise deterministic form:

```text
p-unit PIT for the weighted exterior polynomial;
rank-condenser / MSRD theorem after arithmetic coordinate changes;
classification and exclusion of structured CM trace annihilators.
```

They do not provide certificate evidence as average-case or generic
statements for the fixed prime `p = 10^24 + 7`.
