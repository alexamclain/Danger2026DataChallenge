# Trace-GCD Orbit Exterior Schubert Expansion

Date: 2026-06-06

This note records the orbit-level exterior expansion for the current
trace-GCD determinant.  It is the sharper Cauchy-Binet form of the selected
Schubert p-unit theorem.

## Orbit Module

Fix one nonzero right Frobenius orbit

```text
O subset (Z/211Z)^*,        |O| = 35.
```

After adjoining the 211st roots of unity, the corresponding right factor
`B_O` splits into the 35 character lines indexed by `O`.  The trace-GCD tail
determinant for that orbit is:

```text
Delta_O(t) = det(P V_t W),
```

where:

```text
W subset B_O             is the transported 16-plane,
P : B_O -> F_p^16        is the selected Lang-head projection,
V_t                      is multiplication by zeta_211^t.
```

In the split character basis:

```text
V_t = diag(zeta_211^{u t})_{u in O}.
```

## Cauchy-Binet Expansion

Let `F_O` be the orbit Fourier/Vandermonde change of basis.  For every
`t mod 211`,

```text
Delta_O(t)
  = sum_{U subset O, |U|=16}
      det((P F_O^{-1})_{*,U})
      det((F_O W)_{U,*})
      zeta_211^{t * sum_{u in U} u}.
```

The first determinant is the fixed Schubert/Vandermonde coefficient, and the
second is a Plucker coordinate of the actual CM 16-plane `W`.

For the selected first-16 Lang coordinates, the fixed determinant is, up to
p-unit Fourier normalization, the consecutive-row Vandermonde

```text
det(zeta_211^(r u_j))_{0<=r<16, u_j in U}.
```

Thus every fixed coefficient is nonzero for every 16-subset `U`, because the
`u_j` are distinct modulo the prime `211`.  Since `211` is prime to
`p=10^24+7`, the Fourier normalization denominators are p-units.  This is
recorded in:

```text
p24/trace_gcd_fourier_minor_unit_theorem.md
p24/fourier_head_minor_unit_audit.py
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

Therefore a zero of `Delta_O(t)` is not a support failure on the fixed
projection side.  It is cancellation among the actual CM Plucker coordinates,
or equivalently failure of the corresponding Fitting/orbit norm to be a
p-unit.

The number of exterior terms per nonzero orbit is:

```text
binom(35,16) = binom(35,19) = 4059928950.
```

This is far smaller than the full 210-frequency exterior count
`binom(210,54)`, but still too large for direct expansion as a producer.
The exponent support is also not sparse.  The audit

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_crossed_weight_spectral_audit.py
```

reports for p24:

```text
distinct_subset_sum_size_k1=35
distinct_subset_sum_size_k2=210
distinct_subset_sum_size_k3=211
distinct_subset_sum_size_k16=211
full_support_by_k3=1
```

Thus the character polynomial has all 211 right frequencies available long
before the actual tail size `16`.

## Norm Form

The seven-orbit certificate needs:

```text
Pi_O = prod_{t in O} Delta_O(t) != 0.
```

In the split exterior form this is the norm of the character polynomial
`Delta_O(t)` along the Frobenius action on `O`.  Thus the p-unit theorem can
be restated as:

```text
for every right orbit O, the exterior Schubert character polynomial attached
to the actual CM 16-plane W has no zero on the p24 Frobenius orbit.
```

Equivalently:

```text
the CM Plucker vector of W avoids the orbit product hypersurface cut out by
the 16-plane Schubert translate family.
```

## Consequence

This expansion rules out one more vague shortcut:

```text
nonzero Fourier/Vandermonde coefficients
+ nonzero CM Plucker coordinates
=> Delta_O(t) nonzero.
```

The first hypothesis is now proved for the selected Lang head at p24; the
shortcut still fails because the Cauchy-Binet sum can cancel.

That implication is false in the weighted-Fourier toy:

```text
p24/weighted_fourier_cauchy_binet_toy.py
```

where every Cauchy-Binet coefficient is nonzero and the spectral weights are
nonzero, but the selected weighted minor still vanishes by cancellation.

The orbit-level version is exercised directly by:

```text
p24/orbit_exterior_schubert_toy.py
```

Default run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/orbit_exterior_schubert_toy.py
```

uses the small Frobenius orbit

```text
right=7, multiplier=2, orbit=[1,2,4], rank=2, field_q=29.
```

It found:

```text
terms_subset_fixed_plucker =
  [((0,1), 23,16), ((0,2), 5,25), ((1,2), 3,8)]

direct_delta_on_orbit   = [15,0,25]
expanded_delta_on_orbit = [15,0,25]
```

Thus every fixed coefficient and every Plucker coordinate is nonzero, the
Cauchy-Binet expansion matches exactly, and nevertheless one orbit translate
vanishes by cancellation.  The orbit product is therefore zero.

So the surviving theorem is genuinely arithmetic:

```text
prove p-adic noncancellation of this specific CM Plucker/exterior polynomial,
or identify the orbit product with a class-field/Borcherds/Fitting p-unit.
```

This is the same selected Schubert p-unit theorem as:

```text
p24/trace_gcd_selected_schubert_punit_frontier.md
```

but expressed at the exact exterior polynomial where cancellation can occur.
