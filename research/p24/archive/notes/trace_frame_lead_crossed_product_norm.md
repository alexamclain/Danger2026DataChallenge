# Trace-Frame Lead Crossed-Product Norm

Date: 2026-06-05

This note ties the denominator-free leading Plucker determinant to the
beta-orbit crossed-product/resultant package.

The older crossed-product notes were written around the residual-tail
determinant.  The same finite algebra applies to the full leading determinant
`Delta_lead`, and that is the safer descent object because it is a fixed
Plucker coordinate rather than a determinant built from packetwise kernel
bases.

## Setup

Work over one scalar-extension tensor factor:

```text
E = F_p(mu_m),              [E:F_p] = 5460
B/E has degree d = 5549
Q = |E| mod n = p^5460 mod n
theta = image of zeta_n in B
```

For a fixed H-packet/tensor factor, define the beta-shifted leading
determinants:

```text
D_beta = Delta_lead(theta^(-beta)) in E,        beta in Z/nZ.
```

Let `f_lead(Y)` be the cyclic interpolant in `B[Y]/(Y^n-1)`:

```text
f_lead(theta^(-beta)) = D_beta.
```

Because every `D_beta` lies in `E`, the interpolant satisfies the semilinear
fixed relation:

```text
f_lead(Y) = sigma_E(f_lead)(Y^Q).
```

For a beta orbit:

```text
Omega = { beta, beta*Q, ..., beta*Q^(d-1) }
phi_Omega(Y) = product_{gamma in Omega} (Y - theta^(-gamma)) in E[Y],
```

define the orbit factor:

```text
R_lead,Omega =
  det_B(mul_{f_lead} on B[Y]/phi_Omega).
```

Then:

```text
R_lead,Omega = product_{gamma in Omega} D_gamma.
```

Equivalently, if `T_r = D_{beta*Q^r}`, the weighted cyclic shift

```text
M_Omega e_r = T_r e_{r+1}
```

has determinant:

```text
det(M_Omega) = (-1)^(d-1) product_r T_r.
```

For p24, `d=5549`, so the sign is `+`.

## p24 Count

For:

```text
p = 10^24 + 7
m = 66254
n = 3107441
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
ord_n(p^5460) = 5549
```

the nonzero beta powers split into:

```text
(n-1)/5549 = 560
```

orbits.  These are exactly:

```text
8 H-packets * 70 tensor factors per H-packet.
```

So the full leading beta product has the factorization:

```text
D_0 * product_{560 nonzero Omega} R_lead,Omega.
```

The finite implication is now Lean-gated in:

```text
p24/lean/TraceFrameBetaResultantGate.lean
```

as:

```text
lead_values_nonzero_from_reduced_norm_product
all_trace_frames_good_from_lead_reduced_norms
```

The Lean theorem assumes the usual product-zero implication for the named
orbit product:

```text
D_beta = 0 => orbitProduct(orbitOf beta) = 0.
```

That is the only field-product step hidden by the abstract gate.

## Small-CM Audit

The pinned audit:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_beta_product_resultant_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

reported eight rows.  For every `kind=full` row:

```text
resultant_match=1
resultant_in_E=1
resultant_zero=0
coeff_semilin_fail=0
trace_recon_fail=0
value_orbit_constants=1 out of 3
```

The full-leading rows also show the same nonordinary behavior as the tail
rows: nonzero orbits are not constant-value orbits, and the ordinary-power
collapse is false.

The block audit:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_trace_sum_crossed_product_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

reported 24 orbit rows.  For every `kind=full` nonzero orbit:

```text
block_det_match=1
block_det_in_E=1
block_det_zero=0
weighted_shift_match=1
ordinary_power_match=0
```

This confirms that the leading determinant has the same crossed-product
orbit package as the residual-tail determinant, while preserving the
denominator-free Plucker-coordinate advantage.

## The Theorem Worth Proving

The current sharp arithmetic theorem is:

```text
For the p24 CM trace-frame leading determinant, every crossed-product
reduced norm R_lead,Omega is a p-unit, and the beta-zero factor D_0 is a
p-unit.
```

Equivalently:

```text
f_lead is locally invertible at the selected prime in every beta-orbit
factor B[Y]/phi_Omega.
```

This implies:

```text
Delta_lead(theta^(-beta)) != 0 for every beta,
```

hence every H-packet/tensor factor has a good leading trace frame.

With tensor-factor rank symmetry, the desired descent statement is the
degree-8 relative norm:

```text
Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_lead) is nonzero mod p.
```

Without tensor-factor symmetry, the same statement is needed for 70 tensor
factor representatives:

```text
Xi_lead,i,        i = 1,...,70.
```

The crossed-product formulation explains why those 70 representatives are
the right objects: they are the 70 nonzero `E`-Frobenius orbit factors inside
one H-packet after adjoining `mu_m`.

The finite implication from one global reduced-norm product to all beta
trace frames is now also Lean-gated in:

```text
p24/lean/TraceFrameBetaResultantGate.lean
```

as:

```text
reduced_norms_nonzero_from_global_norm
all_trace_frames_good_from_global_reduced_norm
```

The arithmetic input remains external: one must prove that the global norm is
the product of the named orbit reduced norms, so any zero orbit factor would
force the global value to vanish.

## What This Rules Out

The route is not any of:

```text
f_lead descends to E[Y],
R_lead,Omega = D_rep^5549,
low-degree plain-j divisor support,
low-bidegree single-edge phase relation,
packetwise kernel-basis tail determinants.
```

The first two are directly contradicted by the crossed-product audits.  The
plain-`j` and single-edge variants were disfavored by:

```text
p24/trace_frame_lead_divisor_support_boundary.md
p24/trace_frame_lead_phase_shape_boundary.md
```

The remaining proof must use the full phase-aware determinant line over the
embedded class-field/cyclotomic tower.

The related Fourier/CS boundary is:

```text
p24/trace_frame_twisted_chebotarev_boundary.md
```

It explains why the promising support count

```text
368 + 28*179 << 3107441
```

does not by itself prove the reduced norms are units.  Ordinary prime-cyclic
Chebotarev would apply to an untwisted Fourier minor, but the leading
crossed-product determinant contains the singular-moduli CM twist.  The
surviving theorem is the weighted version: those exact CM-twisted Schubert
minors, equivalently the `R_lead,Omega`, are p-units.

## Proof Mechanisms To Try Next

The local-unit version of the same theorem is recorded in:

```text
p24/trace_frame_lead_local_unit_criterion.md
```

It replaces the raw orbit resultant by the statement that a universal
beta-orbit leading trace-frame map is an isomorphism after reduction at the
selected prime.

1. Determinant-line/unit proof:

```text
construct Delta_lead as a determinant of a canonical trace-frame map between
locally free modules over the p-integral crossed-product order, then prove
the map is an isomorphism after reduction at p.
```

This would make each `R_lead,Omega` a reduced norm of a local unit.

2. Divisor contradiction:

```text
interpret zeros of R_lead,Omega as an effective determinant-line degeneracy
divisor on the phase-lifted ray-class tower, then show the selected CM prime
cannot meet that divisor.
```

The small scans say this divisor is not visible in plain `j` or one edge; it
must retain the non-genus phase.

3. Fitting/annihilator proof:

```text
identify failure of Delta_lead with a nonzero annihilator in the
K-character/cyclotomic group algebra, then prove the relevant Fitting ideal is
the unit ideal after localization at p.
```

This is the CS/MSRD-adjacent version of the same theorem: nonvanishing is a
rank-condenser statement, but the condenser has to be the arithmetic
trace-frame determinant, not a random or generic one.
