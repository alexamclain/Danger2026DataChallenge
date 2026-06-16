# Actual-CM Left-Paired H-Coboundary Boundary

Date: 2026-06-06

## Result

The p24 H-coboundary target is a paired profile, not merely a raw right
resolvent:

```text
G_s = <A_1, B_s>.
```

A natural hope was that the pinned actual-CM right-axis obstruction disappears
after inserting a nontrivial left character.  It does not.

On the same actual-CM row used for the covariance boundary:

```text
D = -6719
q = 6863
h = 105
m = 21 = 3 * 7
n = 5
rho = Frob_q^2
```

`rho` fixes the left component and shifts the right quotient.  For all left
frequencies `u in {0,1,2}`, the internally traced profiles still have formal
covariance.  But the nontrivial left-paired profiles have:

```text
nontrivial_left_equal_H_coset_sums=0/4
nontrivial_left_anchor_descended=0/4
nontrivial_left_gauss_normalized_nonzero=8/8
nontrivial_left_gauss_normalized_fixed=8/8
```

So the Gauss-normalized quotient projections are `rho`-fixed and nonzero even
after nontrivial left pairing.

## Interpretation

This rules out the candidate theorem:

```text
right-axis covariance + nontrivial left character pairing
  => H-coboundary / equal H-coset sums.
```

The surviving p24 target must use the actual trace-GCD weighted product or
section structure, not just left pairing of ordinary CM additive resolvents.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_left_paired_h_boundary.py
```

Expected conclusion:

```text
conclusion=reported_trace_gcd_fixed_frequency_actual_cm_left_paired_h_boundary
```
