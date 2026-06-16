# Trace-Frame Beta-Product Resultant Boundary

Date: 2026-06-05

This note packages the residual-tail beta product as a cyclic resultant and
records the first small CM audit.

## Product As Resultant

For a fixed alpha origin, write the beta-shifted determinant as:

```text
D_beta = D(theta^(-beta)),       beta mod n.
```

Here `D` can mean either:

```text
full leading determinant,
residual-tail determinant on ker(prefix blocks).
```

Let `B/E` be the tensor factor containing `theta`, and interpolate a cyclic
polynomial:

```text
f(Y) in B[Y] / (Y^n - 1)
f(theta^(-beta)) = D_beta.
```

Then:

```text
prod_{beta mod n} D_beta
  = det(multiplication by f on B[Y]/(Y^n - 1)).
```

Equivalently:

```text
prod_beta D_beta = Res_Y(Y^n - 1, f(Y)).
```

This is the exact algebraic package behind the beta-product theorem.  The
hard p24 task is not this finite identity; it is constructing/proving a
p-unit for `f` or its resultant from the class-field tower without explicitly
testing every beta translate.

## Audit

I added:

```text
p24/trace_frame_beta_product_resultant_audit.py
```

It:

1. computes the beta determinant sequence on small actual-CM tensor rows;
2. interpolates `f` using the tensor-factor root `theta`;
3. computes the cyclic resultant as the determinant of multiplication by `f`
   in `B[Y]/(Y^n-1)`;
4. verifies that this equals the direct product over beta;
5. records support and subfield descent of the interpolant;
6. verifies the orbit-trace expansion and normality rank of coefficient
   seeds.

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_beta_product_resultant_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

reported eight rows, all with:

```text
resultant_match=1
resultant_in_E=1
resultant_zero=0
```

The proper residual-tail rows were:

```text
target=constant_plus_3, subdegree=2, tail:
  raw=3, top=2, residual_dim=1
  beta=13, distinct=13, zeros=0
  product_norm=1842
  support=13, E_coeffs=1, subfield_hist=[1:1,6:12]
  coeff_orbit_support=3/3, coeff_semilin_fail=0
  trace_recon_fail=0, seed_rank_hist=[1:1,6:2]
  value_orbit_constants=1/3
  orbit_count=3, orbit_lengths=[1:1,6:2], orbit_zero_products=0

target=constant_plus_4, subdegree=3, tail:
  raw=4, top=2, residual_dim=1
  beta=13, distinct=13, zeros=0
  product_norm=456
  support=13, E_coeffs=1, subfield_hist=[1:1,6:12]
  coeff_orbit_support=3/3, coeff_semilin_fail=0
  trace_recon_fail=0, seed_rank_hist=[1:1,6:2]
  value_orbit_constants=1/3
  orbit_count=3, orbit_lengths=[1:1,6:2], orbit_zero_products=0
```

Thus the exact resultant package exists, but the p24-shaped tail interpolant
has full beta support in this toy and almost all coefficients have full
tensor-factor degree.  It does not descend to `E[Y]`, and it is not sparse in
the visible beta coordinate.

The new semilinear diagnostic is important.  Since each determinant value
`D_beta` lies in `E`, the interpolating coefficients satisfy:

```text
c_l = c_{l / Q}^Q,       Q = |E|.
```

Equivalently:

```text
f(Y) = sigma_E(f)(Y^Q).
```

The audit reported:

```text
coeff_semilin_fail=0
```

in every row.  So the interpolant is not a random dense element of
`B[Y]/(Y^n-1)`: it is a Frobenius-twisted orbit object.  However the value
sequence is not constant on nonzero `Q`-orbits:

```text
value_orbit_constants=1/3
```

only the beta-zero orbit is constant.  Therefore the orbit factors are not
ordinary norms of an `E[Y]` polynomial.  They are twisted/crossed-product
resultants controlled by one coefficient seed per exponent orbit.

2026-06-08 base-field descent probe: on the pinned `D=-10919, m=12` rows with
`axis`, `constant_plus_4`, and `constant_plus_3`, the direct full beta product
was not fixed by base Frobenius:

```text
rows=12
product_in_base=0 in every row
product_frob_fixed=0 in every row
```

So the full product/resultant naturally lands in `E`, not in the base field.
The scalar p-unit payload is still tiny, but it costs `E`-entries; there is no
observed descent to two base-field scalars.

There is an even more explicit trace form.  For an exponent orbit `O` with
representative `ell` and seed coefficient `c_ell`, the contribution to the
beta value is:

```text
sum_{i=0}^{|O|-1} (c_ell * theta^(-beta*ell))^(Q^i).
```

For nonzero p24 orbits, `|O|=5549=[B:E]`, so this is the relative trace:

```text
Tr_{B/E}(c_ell * theta^(-beta*ell)).
```

The audit checked this reconstruction directly:

```text
trace_recon_fail=0.
```

In the proper residual-tail toy rows the seed ranks were:

```text
seed_rank_hist=[1:1,6:2].
```

Thus the scalar beta-zero seed has rank `1`, and both nonzero orbit seeds are
normal over `E` in the degree-6 tensor factor.  This rules out a proper-subfield
seed collapse in the p24-shaped rows.

Some non-proper/full-space rows had smaller support `7` for `n=13`; those rows
are less relevant because the residual image fills the selected block or the
rank is dimension-forced.

## p24 Shape

For p24:

```text
n = 3107441 is prime
Q = p^[E:F_p] = p^5460 mod n
ord_n(Q) = 5549
(n-1)/5549 = 560.
```

So over `E = F_p(mu_m)`, the nonzero beta powers split into `560`
Frobenius orbits of length `5549`, plus beta `0`.

The semilinear coefficient description therefore says that a p24 interpolant
is controlled by at most:

```text
561 coefficient seeds in B,
```

one for beta `0` and one for each nonzero orbit.  In the proper residual-tail
toy all coefficient orbits were nonzero, so there is no evidence for
orbit-sparsity either.  The trace reconstruction suggests the p24 beta values
should be viewed as:

```text
D_beta = c_0 + sum_{j=1}^{560}
  Tr_{B/E}(c_j * theta^(-beta*ell_j)).
```

Small-data seed ranks suggest the nonzero `c_j` should be treated as
full-normal elements of `B/E`, not as elements of a smaller subfield.

The naive cyclic resultant has degree `n`, so it is not a good computational
object by itself.  But the orbit split gives the correct class-field target:

```text
one beta=0 factor
+ 560 Frobenius-orbit norm/resultant factors of degree 5549.
```

For the selected p24 H-packet, these orbit factors must further be related to
the 70 tensor factors inside that H-packet.  This is exactly where the
missing embedded class-field theorem must enter.

## Consequence

The beta-product route is now sharply separated into two layers:

```text
finite algebra layer:
  product over beta = cyclic resultant in B[Y]/(Y^n-1).

missing arithmetic layer:
  prove the resultant/nonzero orbit factors are p-units for the actual
  embedded p24 CM packet.
```

The audit rules out two easy hopes in the residual-tail shape:

```text
small beta support,
coefficient descent to E[Y].
```

So the next useful theorem is not a sparse-interpolant theorem and not an
ordinary norm theorem.  It should be a twisted packet-norm theorem: identify
the 5549-degree orbit resultants with norms in the semilinear/crossed-product
class-field algebra and prove those trace-sum resultant elements are p-units.

The sharper block/crossed-product form is now recorded in:

```text
p24/trace_frame_trace_sum_crossed_product_boundary.md
p24/trace_frame_trace_sum_crossed_product_audit.py
```

There the finite orbit factor is checked in two equivalent forms:

```text
det_B(mul_f on B[Y]/phi_Omega) = prod_{beta in Omega} D_beta,
det(weighted cyclic shift by D_beta) = (-1)^(|Omega|-1) prod_{beta in Omega} D_beta.
```

The same proper residual-tail toy rows have `ordinary_power_match=0` on every
nonzero orbit, so this is a crossed-product reduced-norm target, not an
ordinary-norm collapse.
