# Actual-CM Admissible Jacobi-Span Boundary

Date: 2026-06-07

## Point

The p24 Jacobi route now has a sharp positive theorem target:

```text
the selected weighted packet after Tr_{B/C}
lands in the rank-621 admissible C-axis Jacobi-carry span.
```

This boundary asks whether nearby ordinary actual-CM packets already have that
property.  If they did, the missing theorem might be a generic embedded-CM
fact.  They do not.

## Rows Checked

Two existing small CM rows were used:

```text
D=-5000,  q=3851,  h=30,  right quotient C_2, C-analogue C_5
D=-13319, q=13463, h=140, right quotient C_2, relative C_5
```

The first is the raw projector/internal-character row.  The second is the
pinned right-combo/product row already used for the fixed-frequency
right-obstruction boundaries.

For the pinned row, three profiles are tested:

```text
right_combo_resolvent:        right-combo evaluations R(a)
weighted_coefficients:        coefficient-side G_chi values c_k
selected_defect_coefficients: section-aware defects c_k - c_0
```

Both are quotient-level tests.  They do not enumerate p24 roots.

## Result

```text
projector row:
  admissible rank = 5
  broad rank      = 6
  no-forbidden projected origins = 0/30
  admissible-span origins        = 0/30
  broad-span origins             = 0/30

right-combo row:
  admissible rank = 5
  broad rank      = 6

  right_combo_resolvent:
    no-forbidden projected origins = 0/140
    admissible-span origins        = 0/140
    broad-span origins             = 0/140

  weighted_coefficients:
    no-forbidden projected origins = 0/140
    admissible-span origins        = 0/140
    broad-span origins             = 0/140

  selected_defect_coefficients:
    no-forbidden projected origins = 0/140
    admissible-span origins        = 0/140
    broad-span origins             = 0/140
```

So the admissible Jacobi-span condition is not an automatic consequence of:

```text
ordinary embedded CM;
nontrivial projector channel;
right-combo obstruction shape;
raw weighted coefficient shape;
selected-child defect subtraction;
global origin/section shift.
```

## Consequence

This does not refute the p24 branch.  It narrows what the branch must prove.

The next positive computation has to materialize the **selected weighted**
trace-GCD packet, or a faithful small analogue of it, and test admissible-span
membership there.  Testing unweighted projector packets or generic right-combo
packets is now mostly useful as a negative control.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary.py
```

Runtime on the local machine was about one minute, mostly PARI setup for the
small actual-CM cycles.
