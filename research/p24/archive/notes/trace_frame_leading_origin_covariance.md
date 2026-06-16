# Trace-Frame Leading Origin Covariance

Date: 2026-06-05

This note separates the harmless origin direction from the genuinely hard one
for the leading trace-frame Plucker coordinate.

## Origin Action

For `h=m*n` and an origin shift `u`, write:

```text
u == n*alpha + m*beta mod h.
```

On one H-packet tensor factor, the K-character row of frequency `s` transforms
as:

```text
R_s  |->  zeta_m^(-s*alpha) * theta^(-beta) * R_s.
```

Therefore any full-axis Plucker coordinate transforms under the alpha part by
the scalar:

```text
zeta_m^(-alpha * Sum(S_axis)).
```

For p24:

```text
m = 66254 = 2 * 157 * 211
S_axis = {0}
       union {j*m/2   : 1 <= j < 2}
       union {j*m/157 : 1 <= j < 157}
       union {j*m/211 : 1 <= j < 211}.
```

The sum of the odd-prime component frequencies is a multiple of `m`, while
the order-2 component contributes `m/2`.  Thus:

```text
Sum(S_axis) == m/2 mod m.
```

So alpha translation multiplies the full-axis determinant by:

```text
(-1)^alpha.
```

Since:

```text
[E:F_p] = ord_m(p) = 5460
```

is even, this sign has norm `1` from `E` to `F_p`.  Hence alpha shifts preserve
the base norm and, in particular, the zero/nonzero status of:

```text
Norm_{E/F_p}(delta_lead).
```

## Hard Direction

The beta part sends:

```text
delta_lead -> det(P_lead * Top_3 * theta^(-beta) | W_axis).
```

When the selected rows span the whole tensor factor, this can become
dimension-forced: multiplication by `theta^(-beta)` has a determinant and the
top-frame coordinate map is an isomorphism.  This explains the stable norm in
the tiny `D=-10919, m=12` full-axis toy, where:

```text
raw_rank = tensor_factor_degree = 6.
```

But p24 is not in that regime:

```text
raw_rank = 368
tensor_factor_degree = 5549.
```

Lower-rank analogues in the same toy row confirm that beta/origin movement is
real:

```text
m=4, raw_rank=4 < 6: distinct determinant norms across tested origins = 24
m=3, raw_rank=3 < 6: distinct determinant norms across tested origins = 24
```

Thus the selected-origin theorem is not automatically origin-stable.  The live
p24 statements are:

```text
Selected-origin theorem:
  Norm_{E/F_p}(delta_lead(beta_0)) != 0
  for the embedded beta_0 attached to the constructed CM origin.

Origin-stable strengthening:
  prod_{beta mod n} Norm_{E/F_p}(delta_lead(beta)) != 0.
```

The second statement avoids selecting the beta origin, but it is stronger and
retains the full H-phase.  It should only be pursued if a class-field norm
identity packages the beta product without enumerating all `n=3107441`
translates.

The residual-tail origin audit sharpened this boundary:

```text
p24/trace_frame_residual_tail_origin_action_audit.py
p24/trace_frame_residual_tail_origin_boundary.md
```

In the pinned proper residual-tail toy rows, beta moved individual determinant
norms through all `n=13` values, but the product over beta was alpha-constant
and nonzero.  So beta is not harmless pointwise, but a beta-product p-unit is
a credible theorem target if it can be identified with a packet norm or
resultant.

## Consequence

The leading trace-frame route is not dead, but the proof target must not rely
on free origin covariance.  Alpha is solved by the frequency-sum sign.  Beta
is the actual arithmetic content.
