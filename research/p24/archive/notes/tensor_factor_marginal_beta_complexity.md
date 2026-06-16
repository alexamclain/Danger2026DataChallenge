# Tensor Factor Marginal Beta Complexity

This note measures recurrence/Frobenius compression for the beta-shifted
marginal Plucker values:

```text
a_beta = P(Omega_beta).
```

The script is:

```text
p24/tensor_factor_marginal_beta_complexity.py
```

## Pinned Toy Row

For `D=-10919, m=12, n=13`, the full two-window target is square because
`coords=6` equals the full tensor-factor degree.  It reports:

```text
distinct_values=1
additive_period=1
bm_complexity=1
Q_invariance_matches=13/13
```

This is a full-space determinant artifact: multiplying all coordinates by
`theta^(-beta)` only changes the determinant by a norm-type unit, so the
chosen value is beta-constant.

The more p24-like projected component determinants are different.  For the
one-window `4` component:

```text
distinct_values=13
zero_count=0
additive_period=13
bm_complexity=7
q_frobenius_matches=0/13
Q_invariance_matches=1/13
```

For the one-window `constant+3` component:

```text
distinct_values=13
zero_count=0
additive_period=13
bm_complexity=7
q_frobenius_matches=0/13
Q_invariance_matches=1/13
```

Thus projected marginal Plucker coordinates keep genuine beta phase.  They do
not descend to a simple base-field or tensor-Frobenius norm orbit in this toy
row.

## p24 Meaning

For p24, the relevant maps are also proper projections:

```text
Omega_1:    158 rows into 179 coordinates,
Omega_211:  210 rows into 358 coordinates,
Omega_3:    368 rows into 537 coordinates,
```

inside a tensor factor of degree `5549`.  The full-space determinant artifact
does not apply.

The companion support audit:

```text
p24/tensor_factor_beta_support_audit.py
p24/tensor_factor_beta_support_boundary.md
```

shows that the p24 tensor-factor orbit has full threefold additive support.
So recurrence compression is not ruled out for a specially chosen coordinate,
but it is not forced by small character support or Frobenius descent.
