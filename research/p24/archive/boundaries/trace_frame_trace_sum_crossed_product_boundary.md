# Trace-Frame Trace-Sum Crossed-Product Boundary

Date: 2026-06-05

This note sharpens the beta-product resultant layer from:

```text
prod_beta D_beta = Res_Y(Y^n - 1, f(Y))
```

to the Frobenius-orbit block and crossed-product norm form.

## Setup

Let `B/E` be the degree-`d` tensor factor, with `sigma(x)=x^Q`.  The beta
interpolant from either the full leading determinant or the residual-tail
determinant satisfies:

```text
f(theta^(-beta)) = D_beta in E
c_{Q*l} = sigma(c_l)
```

Equivalently, for exponent-orbit representatives `ell_j`:

```text
D_beta =
  c_0 + sum_j Tr_{B/E}(c_j * theta^(-beta*ell_j)).
```

For a beta orbit:

```text
Omega = { beta, beta*Q, ..., beta*Q^(d-1) },
```

define:

```text
phi_Omega(Y) = prod_{gamma in Omega} (Y - theta^(-gamma)) in E[Y].
```

Then the orbit product is exactly the block determinant:

```text
R_Omega =
  det_B(mul_f on B[Y]/phi_Omega)
  = prod_{gamma in Omega} D_gamma.
```

This is a concrete commutative model of the semilinear fixed algebra

```text
(B[Y]/phi_Omega)^(sigma on coefficients, Y -> Y^Q).
```

There is also a pure crossed-product weighted-cycle form.  Put

```text
T_r = D_{beta*Q^r}.
```

Let `M_Omega` be the weighted cyclic shift:

```text
M_Omega e_r = T_r e_{r+1},
M_Omega e_{d-1} = T_{d-1} e_0.
```

Then:

```text
det(M_Omega) = (-1)^(d-1) * prod_r T_r.
```

For p24 the nonzero beta orbits have `d=5549`, so the sign is `+`.

## Audit

I added:

```text
p24/trace_frame_trace_sum_crossed_product_audit.py
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_trace_sum_crossed_product_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

reported `24` orbit rows.  Every row had:

```text
block_det_match=1
block_det_in_E=1
block_det_zero=0
weighted_shift_match=1
```

For every nonzero beta orbit:

```text
constant=0
ordinary_power_match=0
```

So the orbit factor identity is exact, and the ordinary-norm collapse is
falsified in the same proper residual-tail toy rows.

Representative proper residual-tail rows:

```text
target=constant_plus_3 subdeg=2 tail:
  orbit rep=1 len=6 block_det_norm=3816 ordinary_power_match=0
  orbit rep=2 len=6 block_det_norm=3448 ordinary_power_match=0

target=constant_plus_4 subdeg=3 tail:
  orbit rep=1 len=6 block_det_norm=8442 ordinary_power_match=0
  orbit rep=2 len=6 block_det_norm=8219 ordinary_power_match=0
```

## p24 Shape

For p24:

```text
n = 3107441
Q = p^5460 mod n
ord_n(Q) = 5549
(n-1)/5549 = 560
```

Thus the beta product decomposes as:

```text
D_0 * product_{560 nonzero Omega} R_Omega
```

where each nonzero `R_Omega` is a degree-`5549` crossed-product reduced norm.
The `560` nonzero orbit factors are exactly the scalar-extension refinement
of the eight `F_p` H-packets after adjoining `E=F_p(mu_m)`:

```text
8 H-packets * 70 tensor factors per packet = 560 E-Frobenius orbits.
```

This bridge is recorded in:

```text
p24/beta_orbit_tensor_factor_bridge.md
```

For the older residual-tail split, this is the useful theorem target:

```text
For the selected p24 residual-tail CM packet, every nonzero beta-orbit
weighted-cycle reduced norm R_Omega is a p-unit, and D_0 is a p-unit.
```

For the denominator-free route, replace the residual-tail determinant by the
full leading Plucker determinant `Delta_lead`.  The resulting target is now
recorded in:

```text
p24/trace_frame_lead_crossed_product_norm.md
```

It has the same finite crossed-product algebra and the same `560=8*70`
orbit count, but avoids kernel-basis denominators.

That theorem would give all beta translates at once without testing
`n=3107441` beta values, and the selected beta follows from the existing
orbit-product gate.

## Consequence

The viable route is not:

```text
f descends to E[Y],
or product_Omega D_beta = D_rep^d,
or one Hilbert-90 ordinary norm of a single seed.
```

The viable route is:

```text
trace-sum word -> split Frobenius orbit algebra -> crossed-product reduced norm
```

plus a class-field p-unit theorem for the actual p24 leading or residual-tail
packet.

I also extended:

```text
p24/lean/TraceFrameBetaResultantGate.lean
```

with the abstract reduced-norm-to-orbit-product implication.  Lean only checks
the finite gate; the missing arithmetic input is still the p-unit theorem for
the named crossed-product norms.  The leading version is now the preferred
descent object.
