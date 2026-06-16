# Lang Projective-Relation Boundary

Date: 2026-06-05

This note tests whether the small actual-CM Lang full arcs have visibly
Reed-Solomon-like projective geometry.

## Tool

Added:

```text
p24/lang_projective_relation_audit.py
```

It builds the actual CM Lang-transformed columns, chooses an `F_q` basis for
their span, and tests homogeneous projective relations of a requested degree.

For the dimension-3 row, the RS/GRS-like test is conic containment:

```text
six points in P^2 lie on a degree-2 homogeneous curve.
```

A random full arc in `P^2(F_q)` almost never satisfies this.

## Result

Pinned actual-CM row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_projective_relation_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 7 --only-right 7 --include-linear \
  --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 3 --degree 2 --random-trials 200
```

reported:

```text
left_orbit_len=3
coordinate_count=6
coordinate_rank=3
relation_degree=2
monomial_count=6
relation_rank=6
relation_nullity=0
random_nullity_range=0..0
random_positive_nullity_count=0
```

## Consequence

The row is a full ordinary Moore arc, but it is not on a conic in its natural
Lang coordinates.  Thus the simplest GRS/Reed-Solomon projective explanation
is not visible.

This does not kill the sum-rank LRS/MSRD route, because that route may require
blockwise semilinear coordinate changes and skew-evaluation structure rather
than ordinary projective conics.  It does rule out the cheapest explanation:

```text
natural Lang columns look like a low-degree rational normal curve.
```

The remaining LRS/MSRD theorem must identify a less visible block-equivalence,
or the proof should return to the selected p-unit `L_rep != 0`.
