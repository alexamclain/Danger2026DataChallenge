# Centered Marginal Difference-Geometry Boundary

Date: 2026-06-06

This note tests whether the centered difference columns show visible
generalized Reed-Solomon / rational-normal-curve structure.

## Question

The difference-MDS audit showed that the columns

```text
Q_b = P_b - P_{b-1}
```

are full scalar-MDS in small actual-CM rows, but random controls are also MDS
almost always.  A more structured theorem would identify the projective
columns `[1:Q_b]` with a rational-normal-curve or GRS model after p-unit row
and column transformations.

In small dimensions this should create excess low-degree projective equations.
For example, the `left=4` rows have `Q_b in A^3`, so `[1:Q_b]` lie in `P^3`;
a twisted-cubic/GRS explanation would be visible through special quadratic
relations beyond the random baseline.

## Audit

Added:

```text
p24/centered_marginal_difference_geometry_audit.py
```

The random controls use zero-sum coordinate rows, matching the automatic
condition:

```text
sum_b Q_b = 0.
```

Pinned rows:

```text
D=-13319, q=13463, pair=(4,7):
  row_dim=3
  homogeneous_degree=2
  monomial_count=10
  form_rank=7
  form_nullity=3
  random_nullity_histogram={3: 200}
  coordinate_complexities=[6,6,6]
  random_coordinate_complexity_min=6
  random_coordinate_complexity_max=6.

D=-6719, q=6863, pair=(3,7):
  row_dim=2
  homogeneous_degree=2
  monomial_count=6
  form_rank=6
  form_nullity=0
  random_nullity_histogram={0: 200}
  coordinate_complexities=[6,6]
  random_coordinate_complexity_min=6
  random_coordinate_complexity_max=6.

D=-10919, q=11243, pair=(3,13):
  row_dim=2
  homogeneous_degree=2
  monomial_count=6
  form_rank=6
  form_nullity=0
  random_nullity_histogram={0: 200}
  coordinate_complexities=[12,12]
  random_coordinate_complexity_min=12
  random_coordinate_complexity_max=12.
```

## Consequence

There is no visible excess low-degree projective geometry in these actual-CM
difference columns.  The `left=4,right=7` row has three quadratic relations,
but so do all zero-sum random controls: seven points in `P^3` impose seven
conditions on ten quadrics.

Thus the centered difference matrix is not presently recognized as a
GRS/rational-normal-curve object.  A future MDS/MSRD proof would need a more
specific p-unit equivalence theorem, not just the observed full-MDS behavior
in small fields.

The live proof surface remains:

```text
prove the 211 cyclic consecutive difference minors are p-units,
or prove the equivalent centered Schubert/Fitting orbit product is a p-unit.
```
