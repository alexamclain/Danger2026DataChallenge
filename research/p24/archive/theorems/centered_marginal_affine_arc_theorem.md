# Centered Marginal Affine-Arc Theorem Candidate

Date: 2026-06-05

This note records the finite-geometry form of the current right-product
certificate.

## Point Set

Let

```text
P_b in F_p^156,       b mod 211,
```

be the columns of the centered `157 x 211` Hermitian marginal after dropping
the left zero row and setting `P_0=0`.  The right-translation factor is:

```text
F(t)=det(P_{t+1}-P_t, ..., P_{t+156}-P_t).
```

Thus:

```text
F(t) != 0
```

if and only if

```text
P_t, P_{t+1}, ..., P_{t+156}
```

are affinely independent.

The p24 `Pi_C,right` theorem is therefore:

```text
the 211 ordered centered-marginal points form a cyclic consecutive
157-arc in A^156(F_p).
```

This is weaker than being a full `211`-point affine arc, since only the 211
cyclic consecutive blocks of length `157` are required.

The stronger full-arc condition is audited separately in:

```text
p24/centered_marginal_full_arc_boundary.md
p24/centered_marginal_full_arc_audit.py
```

Small actual-CM rows satisfy the full-arc condition, but so do random
baselines at similar field sizes.  The live p24 certificate therefore remains
the cyclic consecutive product unless a full-arc proof emerges naturally.

## Dual Plateau Form

The dual statement is:

```text
no nonzero affine functional is constant on 157 consecutive points.
```

This is the plateau formulation from:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
```

## Symmetry Audit

Added:

```text
p24/centered_marginal_plateau_intersection_audit.py
```

It tests:

```text
1. all plateau intersections are zero;
2. whether the row span is stable under cyclic shifts;
3. whether the row span is stable under Frobenius multiplier b -> q*b.
```

Small actual-CM rows:

```text
D=-6719, q=6863, pair=(3,7):
  code_rank=2
  cyclic_shift_span_rank=4
  frobenius_multiplier_span_rank=4
  zero_plateau_intersections=7/7.

D=-13319, q=13463, pair=(4,7):
  code_rank=3
  cyclic_shift_span_rank=6
  frobenius_multiplier_span_rank=6
  zero_plateau_intersections=7/7.

D=-10919, q=11243, pair=(3,13):
  code_rank=2
  cyclic_shift_span_rank=4
  frobenius_multiplier_span_rank=4
  zero_plateau_intersections=13/13.
```

## Consequence

The finite-geometry theorem is exact and compact:

```text
prove the p24 centered-marginal points are a cyclic consecutive 157-arc.
```

But the small rows show that this is not explained by ordinary cyclic-code
stability or Frobenius-multiplier stability of the row span.  The required
proof is still arithmetic: it must use the CM/exterior trace-form origin of
the point set, not just an abstract affine-arc theorem.
