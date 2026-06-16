# Centered Orbit-Fitting Block-Cycle Audit

Date: 2026-06-06

## Question

Does the centered crossed-product/Fitting determinant have the expected finite
determinant-line plumbing on an actual-CM row?

For a right Frobenius orbit `O`, the target identity is:

```text
det(block_cycle(phi_t : t in O))
  = sign * prod_{t in O} Delta_C(t).
```

This is the finite bridge that lets a future phase-aware producer certify an
orbit product as one crossed-product/Fitting determinant.

## Actual-CM Test

Pinned row:

```text
D=-13319
q=13463
h=140
m=28
n=5
factor_degree=4
pair=(4,7)
right=7
q mod right=2
```

The centered Schubert window determinants are:

```text
[554, 5943, 7703, 361, 3117, 10521, 13172]
```

The right Frobenius orbits are:

```text
[0]
[1, 2, 4]
[3, 6, 5]
```

For every orbit:

```text
direct_sum_det = orbit_product
block_cycle_det = sign * orbit_product
block_cycle_full_rank iff every local determinant is nonzero
```

Singular controls, made by replacing one window matrix by a singular matrix,
always force the block-cycle determinant to zero.

## Result

```text
determinant_mismatches=0
direct_sum_mismatches=0
zero_detection_failures=0
full_rank_iff_failures=0
singular_control_failures=0
```

## Consequence

The centered orbit product is exactly the determinant of the expected
crossed-product/Fitting block-cycle operator in this actual-CM calibration.
So the determinant-line assembly is not the missing theorem.

The remaining arithmetic statement is still:

```text
prove the phase-aware centered orbit-Fitting determinant is a p-unit at the
selected ordinary p24 prime, without enumerating the class set.
```

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_marginal_orbit_fitting_block_cycle_audit.py
```

Key markers:

```text
actual_centered_orbit_product_equals_direct_sum_fitting_det=1
actual_centered_orbit_product_equals_signed_block_cycle_fitting_det=1
block_cycle_zero_detects_orbit_schubert_zero=1
crossed_product_fitting_plumbing_is_not_the_missing_arithmetic=1
conclusion=reported_centered_marginal_orbit_fitting_block_cycle_audit
```
