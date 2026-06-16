# Centered Marginal Full-Arc Boundary

Date: 2026-06-05

This note tests whether the current cyclic consecutive affine-arc theorem can
be strengthened to a full affine-arc theorem.

## Stronger Theorem

The live p24 theorem asks only that the 211 centered-marginal point columns
have every cyclic consecutive block of 157 affinely independent points.

A stronger statement would be:

```text
every 157-subset of the 211 points is affinely independent.
```

This is a full affine-arc/MDS-type condition.

## Audit

Added:

```text
p24/centered_marginal_full_arc_audit.py
```

Small actual-CM rows where all subsets are enumerable:

```text
D=-6719, q=6863, pair=(3,7):
  subset_size=3
  subset_count=35
  zero_subset_count=0
  consecutive_zero_count=0.

D=-13319, q=13463, pair=(4,7):
  subset_size=4
  subset_count=35
  zero_subset_count=0
  consecutive_zero_count=0.

D=-10919, q=11243, pair=(3,13):
  subset_size=3
  subset_count=286
  zero_subset_count=0
  consecutive_zero_count=0.
```

The random baseline is also almost always full in these large finite fields:

```text
D=-6719 analogue:  random_full_arc_count=200/200.
D=-13319 analogue: random_full_arc_count=200/200.
D=-10919 analogue: random_full_arc_count=194/200.
```

## Consequence

The full-arc strengthening is consistent with small actual-CM rows, but it
looks random-generic at these field sizes.  It does not reveal a special CM
identity.

The natural-coordinate projective geometry also looks random-like rather than
moment-curve-like; see:

```text
p24/centered_marginal_projective_geometry_boundary.md
p24/centered_marginal_projective_geometry_audit.py
```

The live p24 certificate should remain the smaller cyclic-consecutive product:

```text
prod_{t mod 211} F(t) != 0,
```

unless a proof of the full affine-arc property appears naturally from the
class-field construction.
