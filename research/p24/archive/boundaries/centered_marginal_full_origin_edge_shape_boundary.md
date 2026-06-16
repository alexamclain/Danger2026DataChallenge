# Centered Full-Origin Oriented-Edge Shape Boundary

Date: 2026-06-06

## Question

Could the centered full-origin p-unit be the norm of a bounded local function
on one oriented split-prime edge?

In the pinned actual-CM row, this would mean:

```text
Delta_origin(i) = R(j_i, j_{i+1})
```

for a low-bidegree polynomial or rational function `R`.

## Actual-CM Test

Pinned row:

```text
D=-13319
q=13463
h=140
m=28
n=5
pair=(4,7)
```

The test uses all `140` origins.  The determinant value repeats in the beta
direction as predicted by the centered origin theorem, while the oriented
edge `(j_i,j_{i+1})` moves through `140` distinct edge pairs.

No low-bidegree expression was found:

```text
first_polynomial_bidegree_leq_4=None
first_rational_bidegree_leq_4=None
```

Random controls preserving the same repeated-alpha shape also had no hits:

```text
random_repeated_alpha_polynomial_hits=0/8
random_repeated_alpha_rational_hits=0/8
```

## Consequence

The centered full-origin product is not explained by a bounded one-edge
modular-correspondence function in the first actual-CM calibration.  The
surviving centered p-unit theorem still needs a phase-aware Fitting/Chow
divisor, a longer/path-level phase construction, or a local-intersection
formula.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_full_origin_edge_shape_boundary.py
```

Key markers:

```text
sample_count=140
distinct_edge_pairs=140
determinant_distinct_values=14
first_polynomial_bidegree_leq_4=None
first_rational_bidegree_leq_4=None
random_repeated_alpha_polynomial_hits=0/8
random_repeated_alpha_rational_hits=0/8
centered_full_origin_product_is_not_bounded_oriented_edge_function=1
bounded_local_correspondence_norm_needs_more_than_one_edge=1
phase_aware_fitting_divisor_still_required=1
```
