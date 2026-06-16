# Centered Marginal Projective-Geometry Boundary

Date: 2026-06-05

This note checks whether the centered-marginal affine arcs visibly come from a
special low-degree projective curve such as a rational normal/moment curve.

## Audit

Added:

```text
p24/centered_marginal_projective_geometry_audit.py
```

For the projective points `[1:P_b]`, it computes:

```text
1. the nullity of homogeneous forms of a chosen degree through all points;
2. Berlekamp-Massey complexities of the coordinate sequences b -> P_b(a);
3. the same quantities for random point sets of the same shape.
```

## Results

Degree-2 checks:

```text
D=-6719, pair=(3,7):
  monomial_count=6
  form_nullity=0
  random_nullity_histogram={0:200}
  coordinate_complexities=[7,7].

D=-13319, pair=(4,7):
  monomial_count=10
  form_nullity=3
  random_nullity_histogram={3:200}
  coordinate_complexities=[7,7,7].

D=-10919, pair=(3,13):
  monomial_count=6
  form_nullity=0
  random_nullity_histogram={0:200}
  coordinate_complexities=[13,13].
```

Degree-3 checks on the first two rows were also exactly random-like:

```text
D=-6719:  form_nullity=3,  random_nullity_histogram={3:100}.
D=-13319: form_nullity=13, random_nullity_histogram={13:100}.
```

## Consequence

The full-arc behavior in small CM rows does not appear to come from an obvious
low-degree curve or moment-curve parameterization in the natural coordinates.

This does not rule out a hidden CM-adapted projective transformation.  It does
rule out the easy explanation:

```text
the centered-marginal points visibly lie on a low-degree rational normal
curve, so MDS/arc theorems apply.
```

The live proof target remains the exterior trace-form / cyclic consecutive
arc p-unit, not a known projective-curve MDS certificate.
