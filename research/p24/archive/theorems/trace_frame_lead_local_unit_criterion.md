# Trace-Frame Lead Local-Unit Criterion

Date: 2026-06-05

This note rewrites the leading crossed-product p-unit theorem as a local
module-isomorphism criterion.  It does not prove the theorem, but it gives a
more useful object to attack than the raw resultant.

## Orbit Algebra

Let:

```text
O_E = p-integral localization of E = F_p(mu_m) lifted to K_m,
O_B = O_E[theta],
Q = p^5460 mod n.
```

For a nonzero beta orbit:

```text
Omega = beta <Q>,        |Omega| = 5549,
phi_Omega(Y) = product_{gamma in Omega} (Y - theta^(-gamma)),
```

define the finite etale orbit algebra:

```text
A_Omega = O_B[Y] / phi_Omega(Y).
```

After reduction at the selected prime, `A_Omega` is the same degree-5549
factor that appears in the beta/tensor bridge.

## Universal Leading Map

Let `Lambda_axis` be the p-integral lattice spanned by the 368 selected
axis K-character resolvents, with the fixed ordering:

```text
constant, 2-axis, 157-axis, 211-axis.
```

Let `Pi_lead` be the fixed leading projection:

```text
Top_3,lead = first 179 + first 179 + first 10 coordinates of C^3.
```

Over `A_Omega`, form the universal beta-shifted trace-frame map:

```text
T_lead,Omega :
  Lambda_axis tensor_{O_E} A_Omega
    -> O_E^368 tensor_{O_E} A_Omega.
```

Specializing `Y` to `theta^(-gamma)` gives the ordinary leading matrix whose
determinant is:

```text
D_gamma = Delta_lead(theta^(-gamma)).
```

Let:

```text
delta_Omega = det_{A_Omega}(T_lead,Omega).
```

Then the crossed-product orbit factor is:

```text
R_lead,Omega = Norm_{A_Omega/O_E}(delta_Omega)
              = product_{gamma in Omega} D_gamma.
```

This is the determinant-line version of the block determinant checked by:

```text
p24/trace_frame_trace_sum_crossed_product_audit.py
```

## Criterion

Because `A_Omega/O_E` is finite etale at the selected prime:

```text
R_lead,Omega is a p-unit
```

is equivalent to:

```text
delta_Omega in A_Omega^*
```

which is equivalent to:

```text
T_lead,Omega is an isomorphism after reduction at p.
```

Thus the missing arithmetic theorem can be stated without resultants:

```text
For every nonzero p24 beta orbit Omega, the universal leading trace-frame
map T_lead,Omega is an isomorphism modulo the selected prime over p.
```

The beta-zero orbit is the same statement with:

```text
A_0 = O_E
```

and determinant `D_0`.

## Failure Module

The cokernel:

```text
Q_Omega = coker(T_lead,Omega)
```

has zeroth Fitting ideal:

```text
Fitt_0(Q_Omega) = (delta_Omega).
```

Therefore:

```text
R_lead,Omega is not a p-unit
```

if and only if the reduced failure module is nonzero.

Unwinding the selected trace-frame flag, this means there is a nonzero
orbit-family of axis weights `w` such that:

```text
g'(theta) * x_w
```

has relative degree at most `28` over the degree-179 field `C`, and the
`theta^28` coefficient has zero first ten normal-basis coordinates.
Equivalently, with:

```text
F_j = {x : deg_C(g'(theta)*x) <= j},
g'(theta)*x = b_0 + ... + b_30 theta^30,
```

the selected-leading failure module is:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }.
```

So the theorem is the orbitwise selected Schubert-tail statement:

```text
K_sel,Omega = {0}
```

for every `Omega`.

The intrinsic full-top-three condition:

```text
W_axis(A_Omega) cap F_27(A_Omega) = {0}
```

is a necessary consequence of this selected-leading theorem, but it is not
sufficient.  The correction is recorded in:

```text
p24/trace_frame_selected_lead_failure_module.md
p24/lean/TraceFrameSelectedLeadFailureGate.lean
```

## Why This Is Better Than The Raw Resultant

The resultant statement:

```text
det_B(mul_{f_lead} on B[Y]/phi_Omega) != 0
```

is correct but opaque.  The local-unit criterion says the same theorem is the
unit-ideal statement:

```text
Fitt_0(coker T_lead,Omega) = A_Omega.
```

This opens three proof routes:

```text
1. Fitting/annihilator:
   prove the failure module has unit Fitting ideal using the axis
   K-character group algebra.

2. Schubert divisor:
   identify Fitt_0 as the pullback of an open Schubert-cell divisor and show
   the selected CM prime avoids it.

3. Integral normal-basis/unit:
   build T_lead,Omega from a p-integral normal basis and prove its reduction
   is a Moore/MSRD-type isomorphism.
```

It also gives a precise computation target.  Small experiments should not
try to evaluate large p24 matrices.  They should test toy versions of:

```text
does K_sel,Omega vanish?
does the failure module have a structured annihilator?
does Fitt_0 factor through a known class-field divisor?
```

The existing small audits already check the first question for compact
trace-frame rows and find no leading/orbit failures in the pinned examples.

2026-06-08 pinned cyclic-resultant refresh: reran
`trace_frame_beta_product_resultant_audit.py --only-D -10919 --only-m 12
--target constant_plus_4 --target constant_plus_3`.  It returned `8` rows;
all had `resultant_match=1`, `resultant_in_E=1`, `resultant_zero=0`,
`coeff_semilin_fail=0`, `trace_recon_fail=0`, and `orbit_zero_products=0`.
This confirms the finite product packaging in the compact row:

```text
cyclic resultant = product of beta determinant values
= product of orbit reduced-norm factors in E.
```

The same rows still had nonconstant value orbits, so the ordinary norm
shortcut remains false; the theorem must use the semilinear crossed-product
orbit factors or a global determinant-line norm.

2026-06-08 zero-orbit refresh: reran the same pinned audit with
`--target axis` included.  It returned `12` rows; all had `zeros=0` and
`orbit_zero_products=0`.  Thus in this compact faithful model the fixed
beta-zero factor `D_0` is nonzero inside the same cyclic-resultant package as
the nonzero orbit factors.  This is support for the four-element verifier
surface `D_0, U_0, N_lead, U_lead`, not a proof of the p24 local-unit theorem.

The explicit congruence obstruction is recorded in:

```text
p24/trace_frame_low_degree_congruence_boundary.md
p24/trace_frame_low_degree_congruence_audit.py
```

In small rows where the low-degree congruence is forced by taking too few top
blocks, the relation is cross-axis and fills the entire allowed low relative
tail.  This supports proving the full Schubert/local-unit theorem rather than
looking for component-only or sparse-tail exclusions.

The closest CS-style stress test is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_relative_block_erasure_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-subsets 1000
```

It reported:

```text
rows=5
targets=44
subset_tests=102
subset_failures=0
top_failures=0
```

This supports the orbitwise flag-transversality formulation, but not as a
probabilistic proof.  The same files record that simple LRS/MSRD displacement
signatures are not visible in the natural basis, so a coding-theory proof
would still need an arithmetic block equivalence or a p-unit determinant
identity.

The exact MSRD/uncertainty boundary for this local-unit theorem is:

```text
p24/trace_frame_uncertainty_msrd_boundary.md
p24/trace_frame_twisted_chebotarev_boundary.md
p24/trace_frame_weighted_fourier_expansion.md
p24/trace_frame_toeplitz_schur_boundary.md
p24/trace_frame_translate_minor_form.md
p24/trace_frame_complement_minor_boundary.md
p24/trace_frame_translate_minor_dominance_boundary.md
p24/trace_frame_axis_prefix_overlap_boundary.md
p24/trace_frame_toeplitz_support_boundary.md
```

It records that a genuine MSRD/LRS block equivalence would prove the theorem
with distance slack `169`, while generic uncertainty and visible
low-displacement signatures do not suffice.  The twisted-Chebotarev boundary
adds the precise Fourier version: prime-cyclic Chebotarev would prove the
support count if the trace-frame map were untwisted, but the embedded
singular-moduli diagonal/circulant twist is an interior twist.  Nonzero
class-character resolvents alone do not preserve the selected Schubert minor.
The viable CS-shaped theorem is therefore a CM-weighted Chebotarev p-unit
theorem, which is the same as the orbitwise local isomorphism above.
The weighted Fourier expansion identifies the exact cancellation point:
the relevant determinant is a full-support Cauchy-Binet/exterior polynomial
in the CM class-character weights.  The theorem must prove p-unit
noncancellation for those specific weights.
The Toeplitz/Schur form says the same determinant is a selected cyclic
Toeplitz/skew-Schur value of the inverse-DFT CM symbol; nonzero symbol
coefficients alone are still too weak.
The translate-minor form identifies that symbol with the embedded CM torsor
sequence itself.  Thus reduced normality of the full translate matrix is not
enough; the arithmetic input must be selected-minor p-unitness.
Jacobi complementary minors only trade the `368 x 368` target for an enormous
inverse minor of size `3107073`, and principal archimedean dominance only
proves characteristic-zero nonvanishing.  Neither gives the selected-prime
p-unit.  The current consolidated arithmetic frontier is recorded in:

```text
p24/trace_frame_arithmetic_punit_frontier.md
```

The leading-prefix/axis overlap audit further shows that the obvious
principal-diagonal dominance term can contain at most three principal factors
among the 368 selected rows.
The Toeplitz support audit shows the selected matrix touches every symbol
position in `Z/66254Z`, with connected column-overlap support, so there is no
small support or disjoint product factorization to exploit.
The selected-minor certificate spec records the useful selected-origin
Toeplitz-symbol compression and the boundary that literal beta-orbit symbols
are already larger than `sqrt(p)`.
The beta inverse-witness audit further rules out a sparse/dense inverse table
in `B[Y]/(Y^n-1)` as a sub-sqrt unit certificate.

## Current Boundary

The criterion is still selected-phase arithmetic.  It is not implied by:

```text
random rank probability,
component nonvanishing,
ordinary norm collapse,
plain j divisor support,
single-edge phase support,
ordinary prime-cyclic uncertainty.
```

The needed new theorem is now:

```text
Orbitwise p-integral flag transversality for the p24 CM axis module:
for every beta-orbit algebra A_Omega, the leading trace-frame map
T_lead,Omega is a local isomorphism at p.
```

The norm-compressed version is the full beta-algebra Fitting theorem:

```text
A_all = O_E[Y]/(Y^n - 1)
delta_all = det(T_lead,all)
delta_all in A_all^*
```

or equivalently p-unitness of:

```text
Norm_{A_all/O_E}(delta_all)
  = D_0 * product_{Omega != 0} R_lead,Omega.
```

This is the sidecar theorem candidate recorded in:

```text
p24/subagent_selected_minor_norm_compression.md
```

The tensor-factor equivariance needed to compress the `70` scalar-extension
representatives to one degree-8 norm target is isolated in:

```text
p24/trace_frame_tensor_factor_equivariance_boundary.md
```

The direct inverse-witness boundary is:

```text
p24/trace_frame_beta_inverse_witness_boundary.md
p24/trace_frame_beta_inverse_witness_audit.py
```

The positive norm-compressed certificate surface is:

```text
p24/trace_frame_norm_compressed_certificate_spec.md
p24/lean/TraceFrameNormCompressedCertificateGate.lean
```

Together with the Lean gates in:

```text
p24/lean/TraceFrameBetaResultantGate.lean
p24/lean/TraceFrameLeadingNormGate.lean
```

this would give the desired sub-sqrt certificate route.

The latest status note is:

```text
p24/trace_frame_fitting_norm_status.md
p24/trace_frame_beta_interpolant_support_boundary.md
p24/axis_crt_matrix_tree_factorization_boundary.md
```

It records that compact origin-action rows support the full leading
determinant-line product and tensor-factor equivariance, while broader small
rows warn against using residual-tail determinant values as the canonical norm
payload without an additional basis-normalization theorem.  The
beta-interpolant support scan adds that full-leading support can be small in
dimension-saturated toys, but not uniformly enough in partial rows to replace
the local-unit/Fitting theorem.  The CRT matrix-tree factorization audit adds
that the surviving hypertree terms are not ordinary per-edge tree weights, so
standard Laplacian/matrix-tree compression is not the missing theorem either.
