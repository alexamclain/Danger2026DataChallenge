# Fixed-Frequency p24 Gauss-Normalization Boundary

Date: 2026-06-06

## Point

The idempotent covariance theorem must be stated for the Gauss-normalized
`L`-valued projection.  Formal Frobenius covariance of the unnormalized
additive resolvent is not enough.

For a right profile `G_s in L`, define

```text
H_v = sum_s zeta_211^(v*s) G_s
U_chi = sum_v chi(v) H_v
P_chi = sum_s chi(s)^(-1) G_s
```

Then

```text
U_chi = tau(chi) * P_chi.
```

Under `rho=p^780`, the unnormalized object satisfies

```text
rho(U_chi) = chi(rho^(-1)) U_chi,
```

but the Gauss sum has the same eigenvalue:

```text
rho(tau(chi)) = chi(rho^(-1)) tau(chi).
```

So the normalized projection `P_chi` is fixed by `rho` and can be nonzero.

## Boundary Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_p24_gauss_normalization_boundary.py
```

It verifies:

```text
additive_resolvent_eigen_mismatches=0
gauss_sum_eigen_mismatches=0
additive_equals_gauss_times_projection_mismatches=0
normalized_projection_fixed_mismatches=0
random_normalized_projection_nonzero=96/96
ordinary_centered_normalized_projection_nonzero=96/96
```

## Consequence

The formal root-of-unity Frobenius calculation only recovers the Gauss-sum
eigenvalue.  The remaining p24 theorem must prove an extra identity:

```text
Gauss-normalized complete 70-idempotent covariance
```

for the actual CM/Lang packet contribution.  Otherwise we have only reproved
the old Frobenius mirage.
