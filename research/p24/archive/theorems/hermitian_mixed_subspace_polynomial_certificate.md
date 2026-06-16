# Hermitian Mixed Subspace-Polynomial Certificate

This note sharpens the Lang/trace-dual theorem into a standard
rank-metric object.

## Setup

After the p24 mixed Schur reductions, the target coordinates are

```text
w_{j,i} = Tr_{E/L}(delta_i * S_j) in L = F_p(mu_157),
1 <= j <= 6, 1 <= i <= 35.
```

There are `210` such coordinates and

```text
[L:F_p] = 156.
```

The current theorem is:

```text
dim_Fp span{w_{j,i}} = 156.
```

## Subspace Polynomial

For any finite tuple `C` in `F_{q^ell}`, let `A_C(X)` be the monic
`q`-linearized annihilator polynomial of its `F_q`-span:

```text
A_C(X) = sum_{r=0}^d a_r X^{q^r},
A_C(c) = 0 for all c in C,
a_d = 1,
```

with minimal `q`-degree.  Equivalently, `A_C` is the subspace polynomial of
`span_Fq(C)`.

Standard finite-field linearized-polynomial theory gives:

```text
qdeg A_C = dim_Fq span(C).
```

Therefore the p24 mixed theorem is equivalent to the exact identity

```text
A_C(X) = X^(p^156) - X.
```

Equivalently:

```text
there is no nonzero p-linearized polynomial of p-degree < 156
that kills all 210 trace-dual mixed coordinates.
```

This is the cleanest CS/rank-metric import so far.  It replaces the raw
`156 x 210` rank test by a canonical linearized annihilator object.

Terminology caveat: this is not a standard length-`210` Gabidulin MRD code,
since ordinary Gabidulin length is bounded by the extension degree.  The more
accurate phrase is:

```text
interleaved rank-support / full Moore-rank condition.
```

## Certificate Shape

A strict certificate could now be phrased as a p-unit theorem for the
subspace polynomial:

```text
The subspace polynomial of the six mixed class-field period packets is
X^(p^156)-X.
```

Or, in determinant language:

```text
some 156-coordinate Moore minor of the 210 coordinates is a p-unit.
```

The subspace-polynomial form is better for theorem hunting because it is
coordinate-free under `F_p`-basis changes in `L`.  It also exposes the exact
failure divisor: a failure means the six period packets lie in a proper
`F_p`-subspace of `L`, so their subspace polynomial has degree `<156`.

## Delete-One Moore Certificate

The Delsarte right-orbit strengthening gives a sharper certificate target.
Order the six right Frobenius orbits as `O_1,...,O_6`, and let

```text
C^{(j)} = {w_{k,i} : k != j, 1 <= i <= 35}
```

be the `175` Lang/trace-dual coordinates left after deleting orbit `j`.
The support-`>=2` theorem is equivalent to:

```text
span_Fp C^{(j)} = L       for every j=1,...,6.
```

Thus a strict p24 certificate can be packaged as six subspace-polynomial
identities:

```text
A_{C^{(j)}}(X) = X^(p^156) - X.
```

The small actual-CM stress row suggests an even more concrete version.  In the
full delete-one cases, the incremental annihilator pivots are the leading
coordinates of each kept packet.  The p24 theorem candidate is therefore:

```text
for every deleted orbit j,
the leading 156 coordinates of C^{(j)} have nonzero Moore determinant.
```

Equivalently, if `P_{j,a}` is the incremental annihilator after the first `a`
leading kept coordinates, the residual product

```text
R_j = product_{a=0}^{155} Norm_{L/F_p}(P_{j,a}(c_{j,a+1}))
```

is nonzero.  This gives six explicit p-unit candidates rather than an
unstructured search over `binom(175,156)` minors.

The actual-CM audit now tests this prefix statement directly with:

```text
delete_one_leading_min_rank
delete_one_leading_full_count
delete_one_leading_full_field_annihilator_count
delete_one_leading_norm_products_base
```

The same candidate is restated as a six-erasure incidence theorem in:

```text
p24/hermitian_mixed_leading_erasure_theorem.md
```

The trace-GCD bridge back to the current four-field payload is recorded in:

```text
p24/trace_gcd_trace_pairing_subspace_bridge.md
p24/trace_gcd_trace_pairing_subspace_bridge_audit.py
```

It checks on actual-CM rows that the trace-pairing determinant used by the
bad-lambda/Fitting map is nonzero exactly when the selected leading
coordinates have full `F_q`-span, exactly when the incremental residual norm
product is nonzero.  This identifies the Moore residual product with the same
determinant line as the trace-GCD resultant, up to p-unit basis factors.

The random six-orbit toy is a useful negative control: delete-one rank held in
`80/80` tests, but leading delete-one prefix rank held only in `10/80`.  Thus
the leading-prefix p-unit is not forced by the Delsarte/Moore formalism alone;
it is an additional CM arithmetic target.

For p24 the leading window splits as `140+16`: four full right blocks and
sixteen coordinates of the fifth kept block.  This gives a nested certificate:

```text
first four kept blocks have rank 140;
their span plus the first 16 coordinates of the fifth kept block has rank 156.
```

Equivalently, four right traces leave a `16`-dimensional residual kernel, and
the fifth block's first `16` coordinates are nonsingular on that kernel.
The audit now records the corresponding quotient residual products by
starting the linearized-polynomial update from the annihilator of the four
full blocks:

```text
delete_one_prefix_full_block_norm_products_base
delete_one_prefix_tail_norm_products_base
delete_one_prefix_full_block_zero_residual_norms
delete_one_prefix_tail_zero_residual_norms
```

Thus each p24 leading minor is represented as a pair of p-units: a `140`
prefix product and a `16` quotient-tail product.
The exact six-row/five-prefix manifest is generated by:

```text
p24/p24_factorized_certificate_manifest.py
```

The same script also prints a paired certificate using only three distinct
four-block prefix factors, which is the combinatorial lower bound for this
certificate shape.  The paired certificate still has six row-specific
quotient-tail factors.

The independence of those paired tail factors is tested by:

```text
p24/paired_tail_independence_toy.py
```

## Iterative Formula

If `P_U` annihilates a subspace `U` and `x` has `y=P_U(x) != 0`, then the
annihilator of `U + F_q*x` is

```text
P_new(X) = P_U(X)^q - y^(q-1) P_U(X).
```

Starting from `P_0(X)=X`, this constructs `A_C` from the 210 coordinates.
For p24, proving that the final polynomial is `X^(p^156)-X` is exactly the
missing finite-field identity.

## Toy Audit

Added:

```text
p24/hermitian_mixed_subspace_polynomial_toy.py
```

Six-right-orbit miniature:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_subspace_polynomial_toy.py \
  --q 2 --left 7 --right 31 --trials 20 --summary-only
```

reported:

```text
subspace_tests=40
degree_rank_mismatches=0
vanish_failures=0
full_span_tests=40
full_field_annihilator_tests=40
forced_low_rank_degree_mismatches=0
max_coordinate_rank=3
max_annihilator_q_degree=3
```

One-right-orbit control:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_subspace_polynomial_toy.py \
  --q 2 --left 7 --right 5 --trials 20 --summary-only
```

reported:

```text
subspace_tests=40
degree_rank_mismatches=0
vanish_failures=0
full_span_tests=29
full_field_annihilator_tests=29
forced_low_rank_degree_mismatches=0
max_coordinate_rank=3
max_annihilator_q_degree=3
```

These tests do not prove p24.  They verify the exact algebraic certificate
shape and catch the low-rank controls correctly.

## Actual-CM Audit

I also extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

so actual small-CM rows now report:

```text
annihilator_q_degree
annihilator_degree_matches_rank
annihilator_vanish_failures
full_field_annihilator
pivot_count
pivot_prefix
pivot_norm_product_base
zero_residual_norms
```

Pinned rows:

```text
D=-10919:
  rows=2
  tests=12
  left_subfield_failures=0
  annihilator_degree_mismatches=0
  annihilator_vanish_failures=0
  zero_residual_norms=0
  missing_pivot_norm_products=0
  full_left_span_tests=12
  full_field_annihilator_tests=12
  max_annihilator_q_degree=2
  max_pivot_count=2

D=-8711:
  rows=2
  tests=12
  left_subfield_failures=0
  annihilator_degree_mismatches=0
  annihilator_vanish_failures=0
  zero_residual_norms=0
  missing_pivot_norm_products=0
  full_left_span_tests=12
  full_field_annihilator_tests=12
  max_annihilator_q_degree=2
  max_pivot_count=2
```

Bounded broader window:

```text
rows=3
tests=18
left_subfield_failures=0
annihilator_degree_mismatches=0
annihilator_vanish_failures=0
zero_residual_norms=0
missing_pivot_norm_products=0
full_left_span_tests=18
full_field_annihilator_tests=18
max_annihilator_q_degree=2
max_pivot_count=2
```

These rows only reach left orbit length `2`, so they are convention checks,
not evidence of the p24 degree-`156` theorem.  They verify that the canonical
annihilator object agrees with rank on real CM mixed periods.

The residual fields are the first productive statistics/ML hook: in a larger
dimension-eligible row, a stable `pivot_prefix` or stable norm product across
origins/Frobenius rotations would identify an explicit Moore-minor p-unit
candidate.

## New Missing Theorem

Let

```text
S_j = H_{157,211}(1,v_j) = <A_1,B_{v_j}>,
C = { Tr_{E/L}(delta_i*S_j) : 1 <= i <= 35, 1 <= j <= 6 }.
```

The remaining p24 theorem is:

```text
A_C(X) = X^(p^156) - X.
```

This is equivalent to the trace-intersection theorem

```text
F_p(mu_157) ∩ span_R{S_j}^perp = {0},
```

but it may be a more productive proof target because it packages all `210`
relative traces into one canonical `p`-linearized polynomial.
