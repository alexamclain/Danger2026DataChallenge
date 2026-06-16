# Centered Marginal Difference-MDS Boundary

Date: 2026-06-06

This note tests a strengthening suggested by the cyclic-difference
formulation.

## Stronger Statement

Let

```text
Q_b = P_b - P_{b-1}
```

be the centered cyclic-difference columns.  The live theorem only needs the
cyclic consecutive minors:

```text
det(Q_{t+1}, ..., Q_{t+left-1}) != 0.
```

A stronger scalar-MDS theorem would say:

```text
every (left-1)-subset of the Q_b columns is independent.
```

For p24 this would mean the `156 x 211` difference matrix generates an
ordinary scalar MDS code with distance:

```text
211 - 156 + 1 = 56.
```

That distance would exclude every bad support of size at most `55`, including
the p24 plateau complements.

## Audit

Added:

```text
p24/centered_marginal_difference_mds_audit.py
```

Small actual-CM rows:

```text
D=-6719, q=6863, pair=(3,7):
  row_dim=2
  subset_count=21
  zero_subset_count=0
  cyclic_zero_count=0
  random_mds_count=199/200.

D=-13319, q=13463, pair=(4,7):
  row_dim=3
  subset_count=35
  zero_subset_count=0
  cyclic_zero_count=0
  random_mds_count=199/200.

D=-10919, q=11243, pair=(3,13):
  row_dim=2
  subset_count=78
  zero_subset_count=0
  cyclic_zero_count=0
  random_mds_count=197/200.

D=-5444, q=2657, pair=(3,4):
  row_dim=2
  subset_count=6
  zero_subset_count=0
  cyclic_zero_count=0
  random_mds_count=200/200.
```

## Consequence

The full scalar-MDS strengthening is consistent with the small actual-CM
rows, but it is not distinctive: random matrices of the same sizes are also
MDS almost always over these fields.

So this is not a product formula, a class-field identity, or evidence of a
special low-complexity structure.  It is a possible theorem shape only if a
future arithmetic argument identifies the actual p24 difference matrix with a
known MDS/MSRD object.

The current proof target should remain the smaller cyclic-consecutive
Fitting product:

```text
prod_{t mod 211} det(Q_{t+1}, ..., Q_{t+156}) != 0.
```

The full-MDS statement is too broad to be a small certificate surface unless
it comes for free from a stronger class-field or skew-polynomial theorem.

The visible GRS/rational-normal-curve strengthening was tested in:

```text
p24/centered_marginal_difference_geometry_boundary.md
p24/centered_marginal_difference_geometry_audit.py
```

No excess low-degree projective equations were found beyond zero-sum random
controls.
