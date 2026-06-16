# Fixed-Frequency p24 Idempotent Covariance Circularity Boundary

Date: 2026-06-06

## Point

Once the complete 70-factor recombination has already descended to the
`rho=p^780` fixed field `L=F_p(mu_157)`, its idempotent components have the
trivial factor covariance:

```text
Z_{delta+10} = rho(Z_delta).
```

The desired nontrivial covariance

```text
Z_{delta+10} = lambda_chi * rho(Z_delta),   lambda_chi != 1
```

then forces every component to be zero.  So after descent, nontrivial
idempotent covariance is equivalent to the target vanishing.

This means the covariance theorem is only useful if it is proved directly from
the CM trace-resolvent terms before complete recombination, not inferred from
formal scalar-extension idempotent action.

## Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary.py
```

It verifies:

```text
descended_eigenvalue1_failures=0
random_descended_nonzero=24/24
random_descended_fail_nontrivial_covariance=24/24
zero_components_satisfy_both_covariances=24/24
```

## Consequence

The remaining theorem must be stated as a noncircular trace-term identity:

```text
before using S_chi = sum_delta Z_delta(chi) in L,
prove the Gauss-normalized trace-resolvent terms transform with
lambda_chi along delta -> delta+10.
```

Only after that should complete recombination and descent be used to force
`S_chi=0`.
