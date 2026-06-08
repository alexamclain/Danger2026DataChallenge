# p24 Admissible Jacobi-Carry Span Boundary

Date: 2026-06-07

## Point

The Jacobi-carry C-centering gate gave a positive support pattern for a narrow
subfamily:

```text
admissible C-axis Jacobi carries kill
  C_7^nontrivial x {C/E trivial}
```

Here admissible means one input is right-trivial and `C/E`-nontrivial, while
the partner and the sum both keep nontrivial `C/E` component.  The pure-right
partner and `C/E`-cancelling cases individually leak in the forbidden slots.

This note records the next guardrail.  The admissible C-axis Jacobi carries do
**not** span the whole no-forbidden-bidegree space.  Therefore the proof cannot
stop after showing that the weighted packet has no forbidden bidegree; it must
construct an actual decomposition into the much smaller admissible
Jacobi-carry span.

## Exact Small Ranks

For exact models `C_7 x C_c`, the gate computes the full span of carries

```text
theta_{u,v}(t) = [ut] + [vt] - [(u+v)t],
u in C-axis,
v and u+v nontrivial on the C-axis.
```

The observed exact rank is:

```text
admissible rank = 7*(c-1)/2 - 2.
```

Checked rows:

```text
c=5   admissible rank=12   origin-normalized no-forbidden dim=28
c=11  admissible rank=33   origin-normalized no-forbidden dim=70
c=13  admissible rank=40   origin-normalized no-forbidden dim=84
c=17  admissible rank=54   origin-normalized no-forbidden dim=112
c=19  admissible rank=61   origin-normalized no-forbidden dim=126
```

Thus the C-axis carry span is a strict arithmetic subspace even after origin
normalization.

## p24 Projection

For p24, `c=179`, so the same formula gives:

```text
admissible C-axis carry rank:       621
broad C-axis carry rank:            625
no-forbidden bidegree dimension:    1247
origin-normalized no-forbidden dim: 1246
```

The broader rank `625` matches the earlier slow exploratory p24 rank probe,
but that family includes four leaky directions coming from pure-right partners
and `C/E`-cancelling carries.  A theorem may still use the broader family only
if it separately proves cancellation of those leaks.  The cleaner termwise
route is the rank-`621` admissible span.

## Consequence

The positive Jacobi theorem is now sharper:

```text
The weighted trace-GCD obstruction after Tr_{B/C} lands in the rank-621
admissible C-axis Jacobi-carry span.
```

This is stronger than:

```text
the six forbidden bidegrees vanish.
```

So a proof must construct a specific Jacobi-carry decomposition, or an
equivalent arithmetic reason for membership in that span.  Support
vanishing alone is not enough.

Equivalently, a broader `625`-rank decomposition must also prove that the
four leaky directions cancel.  That is a valid but less clean theorem target.

## Check

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary.py
```

The check uses only small exact finite models and does not enumerate CM roots.
