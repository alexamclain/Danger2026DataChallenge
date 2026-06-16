# Axis CRT Fourier Support Boundary

Date: 2026-06-05

This note refines the weighted Fourier/Cauchy-Binet boundary for the
selected-origin trace-frame Toeplitz minor.

The generic prime-cyclic model says selected Fourier minors have full
Cauchy-Binet coefficient support.  The p24 selected-origin axis is different:
its Fourier length is composite,

```text
m = 66254 = 2 * 157 * 211,
S_axis = {0} union nonzero characters on the 2-, 157-, and 211-axes,
|S_axis| = 368.
```

So the CRT axis can kill many Cauchy-Binet coefficients before any CM
arithmetic is used.

## Script

```text
p24/axis_crt_fourier_coefficient_support.py
```

For a `k = |S_axis|` subset `U subset Z/mZ`, the Cauchy-Binet coefficient is:

```text
det(F_{T,U}) * det(F^{-1}_{U,S_axis})
```

with `T = {0,...,k-1}`.  The first determinant is a Vandermonde and is
nonzero for every `U`, so coefficient support is exactly:

```text
rank(F_{U,S_axis}) = k.
```

## Incidence Interpretation

Write:

```text
m = c_1 * ... * c_r,       gcd(c_i,c_j)=1.
```

A row `u mod m` has CRT coordinates:

```text
(u mod c_1, ..., u mod c_r).
```

After invertible DFT changes inside each component, the row features
`F_{u,S_axis}` are equivalent to the incidence vector of the hyperedge:

```text
{u mod c_1, ..., u mod c_r}
```

in the complete `r`-partite `r`-uniform hypergraph with part sizes
`c_1,...,c_r`, modulo the usual per-part constant redundancies.

Thus full rank is the additive-model / incidence condition:

```text
the sampled hyperedges span the vertex-incidence space.
```

For exactly:

```text
k = 1 + sum_i (c_i - 1)
```

edges, this is the spanning-hypertree condition: the hyperedges cover the
component levels and have no additive incidence cycle.  In the two-component
case this reduces to ordinary spanning trees in `K_{c_1,c_2}`.

## Small Results

Exact runs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_crt_fourier_coefficient_support.py \
  --m 6 --max-subsets 1000

m=6, components=[2,3], axis_dim=4
subset_count=15
full_rank=12
zero_coeff=3
```

This matches the spanning-tree count for `K_{2,3}`:

```text
2^(3-1) * 3^(2-1) = 12.
```

Another exact two-component row:

```text
m=10, components=[2,5], axis_dim=6
subset_count=210
full_rank=80
zero_coeff=130
```

matching:

```text
2^(5-1) * 5^(2-1) = 80.
```

Sampled rows:

```text
m=15, components=[3,5], axis_dim=7
tested=1000, full_fraction=0.327

m=30, components=[2,3,5], axis_dim=8
tested=5000, full_fraction=0.253

m=42, components=[2,3,7], axis_dim=10
tested=20000, full_fraction=0.0956

m=66, components=[2,3,11], axis_dim=14
tested=20000, full_fraction=0.0106
```

The support restriction strengthens as one component grows, but surviving
coefficients are still numerous and structurally complicated.

## p24 Size Estimate

The script:

```text
p24/axis_crt_hypertree_support_estimate.py
```

uses no enumeration.  It reports a constructive lower bound and a
coverage-only upper bound for the actual p24 parts:

```text
parts = (2,157,211)
edge_count = 66254
axis_dim = 368

total 368-subsets log10 = 987.668848
lower support log10     = 826.291656
upper support log10     = 957.338867
```

The lower bound is explicit.  Take a spanning tree of the complete bipartite
graph `K_{157,211}`:

```text
tau(K_{157,211}) = 157^210 * 211^156.
```

Lift every tree edge with first coordinate `0`, then duplicate one tree edge
with first coordinate `1`.  This gives `368` tripartite hyperedges.  The
script checks the resulting incidence feature matrix has full rank:

```text
lower_rank_rows = 368
lower_rank_cols = 368
lower_rank_full = 1.
```

Thus the surviving support is definitely enormous:

```text
at least 10^826.29 terms.
```

The upper bound counts ordered edge sequences that hit every level in each
part and divides by `368!`.  It is deliberately loose, but it proves the CRT
support collapse is real:

```text
upper_support_log10 is 30.33 below total_k_subsets_log10.
```

## p24 Consequence

For p24, the Cauchy-Binet expansion is not fully generic.  Its support is
restricted to CRT-axis incidence hypertrees in the complete tripartite
hypergraph with parts:

```text
2, 157, 211.
```

This is a real structural improvement over the prime-cyclic toy:

```text
not every 368-subset U contributes.
```

But it does not yet give a sub-sqrt certificate:

```text
the surviving support is still a huge spanning-hypertree polynomial in the
CM spectral weights.
```

Quantitatively, even the explicit lower bound is far beyond any certificate
payload:

```text
support_lower_bound > 10^826 terms.
```

So the current theorem target becomes sharper:

```text
prove p-unit noncancellation of the CRT-axis spanning-hypertree polynomial
for the p24 CM weights.
```

This is equivalent to the full leading determinant-line p-unit theorem, but
with the support now identified combinatorially.  It may be useful for a
matrix-tree/Pfaffian/hypergraph determinant attack, but it is not itself the
certificate.

## Matrix-Tree Weight Boundary

The follow-up note:

```text
p24/axis_crt_matrix_tree_factorization_boundary.md
p24/axis_crt_matrix_tree_factorization_toy.py
```

tests whether the surviving CRT-axis coefficients can be turned into an
ordinary edge-weighted matrix-tree polynomial.  They cannot, already in exact
small analogues.

The test uses the pair-sum identity forced by any factorization:

```text
c(B) = C * prod_{e in B} a_e.
```

For `m=6,10,15`, and in a sampled `m=30` tripartite analogue, the actual
Cauchy-Binet coefficient

```text
det(F_{T,B}) det((F^{-1})_{B,S_axis})
```

violates this identity.  Thus the complete multipartite hypertree model
describes support, but the coefficients remain genuinely Plucker/exterior
weights.

The updated p24 target is therefore not an ordinary Laplacian determinant.
It is the Plucker-weighted CRT hypertree p-unit theorem, equivalently the
full leading determinant-line statement:

```text
delta_all in A_all^*.
```

## Boundary

This rules out two opposite oversimplifications:

```text
1. prime-cyclic full-support Chebotarev is too pessimistic for the CRT axis;
2. CRT support collapse is still not small enough to replace the p-unit
   determinant-line theorem.
```

The surviving route is still:

```text
full leading determinant-line norm / Fitting p-unitness,
now viewed as a weighted spanning-hypertree noncancellation theorem.
```
