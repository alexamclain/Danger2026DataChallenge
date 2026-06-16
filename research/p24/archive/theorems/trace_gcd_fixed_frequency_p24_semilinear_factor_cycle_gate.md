# Fixed-Frequency p24 Semilinear Factor-Cycle Gate

Date: 2026-06-06

## Point

The scalar factor-cycle model is only a first approximation.  In the actual
tower, `rho=p^780` is semilinear on `E=F_p(mu_66254)`: it has order `7` on
`E`, fixes `L=F_p(mu_157)`, shifts the right order-7 quotient, and cycles the
70 tensor factors as ten 7-cycles.

Thus the needed implication is not just a geometric-series identity.  If a
cycle contribution has the form

```text
Z_i = lambda^i sigma^i(Z_0),
```

where `sigma=rho` has order `7` and `lambda` is a nontrivial 7th root, then

```text
S = sum_i Z_i
```

usually need not be zero.  Instead it satisfies

```text
sigma(S) = lambda^(-1) S.
```

This is useful for p24 because the original fixed-frequency projection is
`L`-valued and `rho` fixes `L`.  So the real finite implication is:

```text
semilinear rho-covariance of the factor-cycle packet sum
and descent of the total sum to L
  => S is fixed by rho and has nontrivial rho-eigenvalue
  => S = 0.
```

## p24 Arithmetic

For p24:

```text
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
rho = p^780
rho_order_on_E = 7
rho fixes mu_157
rho shifts the right H-quotient by 6 mod 7
rho shifts the 70 tensor factors by 10 mod 70
```

The shift by `10` gives ten cycles of length `7`.

## Finite Gate

The script

```text
p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.py
```

checks the refined finite-field statement over `F_43^7/F_43`:

```text
fixed_eigenspace_dimension=1
twisted_projection_ranks=[1, 1, 1, 1, 1, 1]
twisted_eigenspace_dimensions=[1, 1, 1, 1, 1, 1]
twisted_fixed_intersection_dimensions=[0, 0, 0, 0, 0, 0]
twisted_projection_eigen_failures=0
```

It also includes the boundary:

```text
semilinear_covariance_alone_does_not_force_zero=1
```

because the twisted projection is a nonzero rank-1 map for each nontrivial
character.  The missing p24 theorem is therefore precisely covariance plus
descent of the packet product sum, not scalar geometric cancellation by
itself.
