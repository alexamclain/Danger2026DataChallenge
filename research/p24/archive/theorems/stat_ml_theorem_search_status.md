# Statistics / ML Theorem-Search Status

This note records what statistics or ML can productively contribute after the
current p24 reductions.

## High-Value Search: Stable Plucker Norm Identity

Hypothesis:

```text
one or a small family of Plucker coordinates for
Omega_1, Omega_211, Omega_3
has an origin-stable product equal to a class-field norm/resultant.
```

Evidence and boundary:

```text
p24/tensor_factor_marginal_origin_product.md
p24/tensor_factor_crt_marginal_rank.md
```

support the origin-stable product surface.  But:

```text
p24/tensor_factor_beta_support_boundary.md
p24/tensor_factor_marginal_random_support.md
p24/tensor_factor_trace_coordinate_support.md
```

rule out "small support by generic recurrence" as the explanation.

Cheap useful audit:

```text
across small CM rows, enumerate or sample Plucker minors;
rank them by stable nonzero origin products and unusually low-height or
factorable norm values;
compare against random tensor-factor controls.
```

This has high p-unit plausibility if a product matches a norm identity.

The first version of this audit is now recorded in:

```text
p24/tensor_factor_plucker_norm_miner.py
p24/tensor_factor_plucker_norm_miner.md
```

It is negative for ordinary trace-coordinate minors.  On the pinned
`D=-10919, m=12` row, the square full-axis determinant and rectangular
component Plucker products are all nonzero, but their beta products have full
coefficient-field degree and random-looking base norms.  Random tensor-factor
controls often have smaller best norm height.  Therefore the remaining
Plucker-norm route needs an intrinsic exterior norm, a CM-adapted coordinate
change, or a full-support p-unit identity rather than a visibly small natural
coordinate product.

## New High-Value Search: Subspace-Polynomial Residual Mining

The live rank-metric theorem is now:

```text
A_C(X)=X^(p^156)-X
```

for the `210` trace-dual mixed coordinates `C`.  The subspace-polynomial
recursion adjoins a coordinate `c` by recording the residual

```text
y = A_U(c)
```

before updating `A_U`.  The pivot residuals are Moore-minor witnesses in
disguise, and their norm products are the right objects for exact
class-field/resultant matching.

I extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

to emit:

```text
pivot_count
pivot_prefix
pivot_norm_product_base
zero_residual_norms
```

Pinned `D=-10919` output includes examples such as:

```text
pivotprefix[0, 1]:pivotnorm6471
pivotprefix[0]:pivotnorm50
```

and the summary:

```text
zero_residual_norms=0
missing_pivot_norm_products=0
max_pivot_count=2
```

The current rows are still too small (`max_left_orbit_len=2`) to reveal the
p24 pattern, but the mining target is now explicit:

```text
find a stable 156-pivot pattern or residual norm product across
dimension-eligible CM rows, origins, and Frobenius rotations.
```

Success would produce a concrete Moore-minor p-unit/norm candidate.  Failure
would be useful too: it would rule out coordinate-order residual mining and
push the proof back to the dual trace-intersection theorem.

## Useful Failure Clustering: Exact Content / Hermitian Scalars

Hypothesis:

```text
exact packet content or Hermitian packet scalars vanish only on an explicit
arithmetic divisor, while coordinate/product failures are unrelated cyclic-code
artifacts.
```

Evidence:

```text
p24/packetized_relative_content_scan.md
p24/relative_resultant_selected_prime_scan.md
p24/hermitian_axis_packet_norm_scan.py
```

The exact packet content scans remain clean in prime-`n` windows, while
stronger coordinate nonvanishing statements have known failures.

Cheap useful audit:

```text
make a compact table of zero and near-zero events with features
(D,q,m,n,factor_degree, conductor, genus data, origin);
use sparse rules or decision trees only to propose exact divisibility
conditions.
```

This is plausible because the target is already a content/norm p-unit
statement.

## Medium-Value Search: Hidden Block-Moore Normality

Hypothesis:

```text
after the right trace-frame or normal-basis change, the marginal vectors have
a Moore/Gabidulin determinant interpretation.
```

The coordinate-free theorem candidate is recorded in:

```text
p24/marginal_block_moore_theorem_candidate.md
```

The direct Toeplitz/Hankel/Cauchy-style version is now disfavored by:

```text
p24/tensor_factor_marginal_cs_structure_audit.py
p24/cs_rank_condenser_theorem_status.md
```

Cheap useful audit:

```text
search toy marginal matrices for low-degree q-linearized annihilators or a
coordinate transform that makes stable minors Moore-determinantal;
compare against shuffled/random controls.
```

This has moderate-to-high p-unit plausibility if it becomes a Moore norm.

## Low-Value But Useful Falsifier: Montgomery Invariant Selector

Hypothesis:

```text
any direct Montgomery-space selector must respect reciprocal, negA_negx, and
orbit symmetries and compress all-good prefixes below Theta(sqrt(p)).
```

Existing upstream data mostly rules out natural versions:

```text
p24/upstream_dataset_experiment_audit.md
p24/upstream_near_square_dataset_boundary.md
p24/full_small_triple_pp12_p7_tail_audit.txt
p24/quotient_period_low_degree_feature_audit.md
```

Cheap useful audit:

```text
bounded symbolic search over low-degree invariant rational functions on
pp12/pp16A holdouts after branch conditioning.
```

This has low p-unit plausibility, but it is a good sanity check for any
claimed direct Montgomery selector.

The order-19 quotient analogue now gives the same lesson inside the CM period
problem: degree `<= 3` local `Phi_ell` feature formulas fail on `ell=index`
examples, and the first success at degree `4` is full-rank interpolation.  So
statistics should be used to mine exact norm/Fitting identities or falsify
candidate formulas, not as standalone certificate evidence.

## Summary

Statistics and ML are useful only as theorem search:

```text
mine small data for a stable norm identity,
cluster true arithmetic failures,
or suggest a Moore normality transform.
```

They should not be used as evidence that p24 is certified.  Any successful
pattern must graduate to an exact finite-field identity or selected-prime
p-unit theorem.
