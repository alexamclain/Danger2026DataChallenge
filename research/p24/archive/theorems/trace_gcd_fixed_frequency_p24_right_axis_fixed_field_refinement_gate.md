# p24 Right-Axis Fixed-Field Refinement

The seven-coset theorem only needs an anchor H-coset sum to be fixed by
`rho=p^780`.  It does not need that anchor to descend all the way to
`L=F_p(mu_157)`.

This distinction matters.  On the right `211`-cyclotomic layer, `rho` has
order `7`, so the `rho`-fixed right-period subfield has degree `5`.  In the
full `E=F_p(mu_66254)` layer:

```text
[F_p(mu_157):F_p] = 156
right rho-fixed degree = 5
[E^rho:F_p] = 780
```

Thus the exact finite target is:

```text
Y_{c+6} = rho(Y_c)
Y_0 in E^rho
```

Descent to `F_p(mu_157)` would be sufficient, but it is stronger than needed.

The executable gate also checks a negative control: the pure right
`H=<2^7>` Gaussian periods are covariant under `rho`, but the anchor period is
not `rho`-fixed and all six nontrivial order-7 projections leak.  Therefore
the actual CM/Lang `G_chi` coefficients must cancel the nonfixed right-period
part; pure cyclotomic H-period bookkeeping is not enough.
