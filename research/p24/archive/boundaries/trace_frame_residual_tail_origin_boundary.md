# Trace-Frame Residual-Tail Origin Boundary

Date: 2026-06-05

This note records the origin-action audit for the refined residual-tail
determinant.

## Script

I added:

```text
p24/trace_frame_residual_tail_origin_action_audit.py
```

It computes, over a full small CM origin orbit:

```text
full leading determinant:
  det(first raw_rank coordinates of Top_k)

residual-tail determinant:
  det(first residual_dim tail coordinates on ker(prefix blocks))
```

The residual-tail determinant uses the deterministic right-kernel basis from
`trace_frame_residual_tail_audit.py`.  Its exact value is basis-dependent; its
zero/nonzero status is not.  Norms are taken down to the base field of the
small split prime.

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_residual_tail_origin_action_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3 \
  --first-case-only
```

## Pinned Result

The run used:

```text
D=-10919, q=11243, h=156, m=12, n=13.
```

It produced four target/subdegree groups.  The two p24-shaped proper
residual-tail groups were:

```text
target=constant_plus_3, subdegree=2:
  raw_rank=3, top_count=2, residual_dim=1
  full_det_all       count=156 distinct=13 zeros=0
  full_norm_all      count=156 distinct=13 zeros=0
  tail_det_all       count=156 distinct=39 zeros=0
  tail_norm_all      count=156 distinct=13 zeros=0
  pure_alpha_beta0_full_norm distinct=1
  pure_alpha_beta0_tail_norm distinct=1
  pure_beta_alpha0_full_norm distinct=13
  pure_beta_alpha0_tail_norm distinct=13
  beta_orbit_tail_det_distinct min=13 max=13
  tail_product_over_beta_zero_by_alpha zero_products=0
  tail_norm_product_over_beta_by_alpha distinct=1 zeros=0

target=constant_plus_4, subdegree=3:
  raw_rank=4, top_count=2, residual_dim=1
  full_det_all       count=156 distinct=26 zeros=0
  full_norm_all      count=156 distinct=13 zeros=0
  tail_det_all       count=156 distinct=52 zeros=0
  tail_norm_all      count=156 distinct=13 zeros=0
  pure_alpha_beta0_full_norm distinct=1
  pure_alpha_beta0_tail_norm distinct=1
  pure_beta_alpha0_full_norm distinct=13
  pure_beta_alpha0_tail_norm distinct=13
  beta_orbit_tail_det_distinct min=13 max=13
  tail_product_over_beta_zero_by_alpha zero_products=0
  tail_norm_product_over_beta_by_alpha distinct=1 zeros=0
```

The non-proper groups showed the same origin pattern, but their residual image
filled the selected subfield block and are less p24-shaped.

## Interpretation

This reinforces the origin covariance split:

```text
alpha direction:
  base norms are constant.

beta direction:
  individual determinant norms move through all n=13 values.

beta product:
  product over all beta shifts is nonzero and alpha-constant in this toy.
```

So a pointwise beta-invariance theorem is false in the shape that matters.
The selected-origin theorem remains a genuine selected p-unit:

```text
Norm_{E/F_p}(D_tail(beta_0)) != 0.
```

But the stronger beta-product theorem is now a concrete live target rather
than only a formal escape hatch:

```text
prod_{beta mod n} Norm_{E/F_p}(D_tail(beta)) != 0.
```

This would imply the selected-origin statement for every beta translate and
would avoid naming the embedded beta origin.  The price is that it must be
proved by a class-field norm/resultant identity, not by enumerating the
`n=3107441` beta values in p24.

## Theorem Frontier

The clean finite-field form is:

```text
U_beta = b_28(K_2(beta)) subset C,
T      = span_E{nu_10,...,nu_178}.
```

Selected-origin version:

```text
U_beta0 cap T = {0}.
```

Product version:

```text
for every beta in the H-direction,
  U_beta cap T = {0}.
```

Equivalently:

```text
prod_beta det(pi_10 | U_beta) != 0,
```

or in annihilator language:

```text
prod_beta det(A_T(u_{beta,j})^(Q^i)) != 0.
```

The audit says the beta orbit is genuinely moving, so any proof of the product
must package the full beta orbit as a norm/resultant in the packet algebra.
That is still sub-sqrt if the product is evaluated symbolically through the
tower, but it is not available from the current finite reduction alone.

I then checked the exact cyclic-resultant package in:

```text
p24/trace_frame_beta_product_resultant_audit.py
p24/trace_frame_beta_product_resultant_boundary.md
```

For the proper residual-tail toy rows, the cyclic resultant identity holds
exactly and the resultant lands back in `E`, but the interpolating polynomial
has full beta support and almost all coefficients have full tensor-factor
degree.  Its coefficients satisfy Frobenius-twisted covariance, while the
values are not constant on nonzero beta orbits.  Thus the product theorem
should not be pursued as a sparse beta interpolant or ordinary `E[Y]` norm.
The live arithmetic statement is a twisted packet-norm p-unit theorem for the
Frobenius-orbit trace-sum resultants.  In the pinned proper residual-tail toy
rows, the nonzero orbit seeds are full-normal over the tensor factor, so the
trace-sum view does not collapse to a proper subfield statement.

## Lean Gate

I extended:

```text
p24/lean/TraceFrameResidualTailGate.lean
```

with the direct selected-tail operator implication and the abstract
annihilator implication:

```text
selected-tail operator p-unit
=> residual-tail avoidance

ker(A_T) = T
+ A_T has trivial kernel on U
=> U cap T = {0}
=> residual-tail avoidance.
```

The direct operator form is now the safest live theorem because it proves
`K_sel=0` without separately assuming full residual-image rank.  The
`U cap T`/linearized-resultant form is still valid once that rank hypothesis is
included.  Neither Lean gate proves the arithmetic nonvanishing; they keep the
finite reduction honest while the p-unit theorem is attacked.
