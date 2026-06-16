# Actual-CM Right-Axis Covariance Boundary

Date: 2026-06-06

## Point

The p24 right-axis theorem has a tempting proof shape:

```text
formal Frobenius covariance
  + Gauss normalization
  => quotient projection descends
  => quotient projection vanishes.
```

The middle implication is false.  A small actual-CM row with the same
right-axis geometry shows that additive covariance and Gauss-normalized
fixedness can both hold while the normalized quotient projections remain
nonzero.

## Actual-CM Row

The boundary uses:

```text
D = -6719
q = 6863
h = 105
m = 21 = 3 * 7
n = 5
left = 3
right = 7
```

Here:

```text
rho = Frob_q^2
rho fixes the left component:      q^2 = 1 mod 3
rho moves the right quotient:      q^2 = 2 mod 7
right quotient order:              3
internal generator:                q^6 = 1 mod 7, q^6 = 4 mod 5
internal relative subgroup:        [1, 4]
```

So this row clones the relevant finite shape:

```text
rho moves right H-cosets;
rho^3 fixes the right axis;
the internal relative trace does not average the right quotient.
```

## Result

The executable boundary is:

```text
p24/trace_gcd_fixed_frequency_actual_cm_right_axis_covariance_boundary.py
```

Key output:

```text
additive_resolvent_covariance_failures=0
anchor_coset_descended=0/2
equal_H_coset_sums=0/2
gauss_normalized_nonzero_projections=4/4
gauss_normalized_projection_rho_fixed=4/4
```

Thus the formal additive resolvent covariance is real, and the Gauss-normalized
quotient projections are fixed by `rho`, but they are all nonzero.  The anchor
coset sums do not descend, and the H-coset sums are not equal.

## Consequence

For p24, the remaining theorem cannot be only:

```text
rho covariance of additive right resolvents;
Gauss normalization;
complete internal trace bookkeeping.
```

Those are finite-algebra facts.  The arithmetic theorem must additionally
prove the section-aware anchor descent/equal-H-coset identity for the actual
weighted `G_chi` CM/Lang packet:

```text
rho(Y_0) = Y_0
```

under the already-known right-coset covariance, equivalently all nontrivial
right quotient-character projections vanish after internal tracing.
