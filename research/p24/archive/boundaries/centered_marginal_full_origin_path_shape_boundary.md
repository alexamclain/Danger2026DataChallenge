# Centered Full-Origin Short-Path Shape Boundary

Date: 2026-06-06

## Question

After the one-edge model failed, could the centered full-origin p-unit be a
bounded local function of a short oriented path?

The tested shape is:

```text
Delta_origin(i) = R(j_i, j_{i+1}, ..., j_{i+s})
```

for low total-degree polynomial or rational `R`.

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

The test uses all `140` origins.  The determinant sequence has the expected
`14` distinct values, repeated along the beta direction.  The path coordinates
are all distinct in both tested cases.

Two-edge path, three vertices:

```text
path_vertices=3
sample_count=140
distinct_path_points=140
max_poly_total_degree=7
poly_monomials_at_cap=120
first_polynomial_total_degree=None
max_rat_total_degree=5
rat_monomials_at_cap=56
first_rational_total_degree=None
random_repeated_alpha_polynomial_hits=0/8
random_repeated_alpha_rational_hits=0/8
```

Three-edge path, four vertices:

```text
path_vertices=4
sample_count=140
distinct_path_points=140
max_poly_total_degree=5
poly_monomials_at_cap=126
first_polynomial_total_degree=None
max_rat_total_degree=3
rat_monomials_at_cap=35
first_rational_total_degree=None
random_repeated_alpha_polynomial_hits=0/8
random_repeated_alpha_rational_hits=0/8
```

The degree caps stay below generic interpolation:

```text
C(3+7,7)=120 < 140
2*C(3+5,5)=112 < 140
C(4+5,5)=126 < 140
2*C(4+3,3)=70 < 140
```

## Consequence

The centered full-origin product is not explained by a bounded low-degree
function of one, two, or three adjacent oriented edges in this actual-CM
calibration.  The surviving local theorem must use richer embedded phase
coordinates, a longer nonlocal path with a real divisor explanation, or a
direct phase-aware Chow/Fitting construction.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_full_origin_path_shape_boundary.py
```

Key markers:

```text
short_oriented_paths_have_no_subgeneric_low_degree_formula=1
local_correspondence_norm_must_use_richer_phase_or_direct_fitting_divisor=1
conclusion=reported_centered_marginal_full_origin_path_shape_boundary
```
