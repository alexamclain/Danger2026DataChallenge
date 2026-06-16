# Trace-Frame Fitting Norm Status

Date: 2026-06-05

This note tightens the current trace-frame norm-compressed route after the
latest compact audits.

## Current Theorem Target

The certificate should be built from the full leading determinant line:

```text
T_lead,Omega :
  Lambda_axis tensor A_Omega -> O_E^368 tensor A_Omega

delta_Omega = det(T_lead,Omega)
R_lead,Omega = Norm_{A_Omega/O_E}(delta_Omega)
```

The desired arithmetic statement is:

```text
delta_Omega in A_Omega^*
```

for every beta orbit `Omega`, or globally:

```text
A_all = O_E[Y]/(Y^n - 1)
delta_all = det(T_lead,all)
delta_all in A_all^*.
```

The norm-compressed p24 payload is then a scalar norm of a determinant-line
section:

```text
N_lead = Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_lead) mod p.
```

This is the same target as:

```text
p24/trace_frame_norm_compressed_certificate_spec.md
p24/trace_frame_lead_local_unit_criterion.md
p24/trace_frame_denominator_safe_fitting_attack.md
```

## Audit Update

Pinned compact row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_residual_tail_origin_action_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 \
  --max-m 40 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 \
  --target constant_plus_4 --target constant_plus_3
```

For all four target/subdegree groups:

```text
full_det zeros = 0
tail_det zeros = 0
beta_orbit_full_det_distinct = expected beta count = 13
tail_product_over_beta_zero_by_alpha = 0
full_norm_product_over_beta_by_alpha distinct = 1
tail_norm_product_over_beta_by_alpha distinct = 1
```

The tensor-factor audit on the same row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_tensor_factor_equivariance_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --target axis --max-rows 40 --include-linear
```

reported:

```text
zero_status_uniform = 1
norm_equal = 1
pivot_shape_equal = 1
```

So the compact row supports both:

```text
1. beta-product/nonzero Fitting unit behavior;
2. tensor-factor determinant-line equivariance.
```

## Boundary From Broader Compact Rows

A broader `axis` scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_residual_tail_origin_action_audit.py \
  --max-abs-D 30000 --min-h 24 --max-h 180 \
  --max-n 80 --max-m 24 --max-factor-degree 18 \
  --max-extension-degree 6 --max-tensor-factor-degree 10 \
  --min-tensor-factor-count 1 --max-top-count 4 \
  --max-cases 3 --include-linear --require-composite-m \
  --target axis
```

again found zero-free full and tail determinant families in the compact rows.
But it also showed that residual-tail norm products can vary with `alpha`:

```text
tail_norm_product_over_beta_by_alpha distinct = 6
```

in the small `m=6` axis rows.  This is expected: the residual-tail determinant
depends on a chosen kernel basis.  Its zero status is useful, but its value is
not the safest global class-field payload.

Conclusion:

```text
Use the full leading determinant line delta_all for the theorem.
Use residual-tail determinants only as diagnostics or after proving a
canonical basis/trivialization theorem.
```

## Forced-Failure Congruence Check

The low-degree congruence audit:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_low_degree_congruence_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 \
  --max-m 40 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --max-cases 1 \
  --max-kernel-basis 6 --no-require-prime-n
```

forces rank failures by taking too few top blocks.  The resulting kernel
vectors are not component-only or sparse:

```text
axis_block_touches = 2 or 3
low_nonzero_blocks fills the allowed low tail
```

So a small annihilator/component lemma is not the likely proof.  The proof has
to address the full Schubert/Fitting determinant.

## Current Proof Obligation

The missing theorem is now best stated as:

```text
Full leading determinant-line p-unit theorem:
  the p-integral CM section Xi_lead has no zero at the selected prime over p.
```

Equivalent finite-field forms:

```text
delta_all in A_all^*
Fitt_0(coker T_lead,all) = A_all
K_sel,Omega = {0} for every Omega, where
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }.
```

The full-top-three annihilator statement `W_axis cap F_27 = {0}` follows from
this selected-leading theorem but does not imply it; see
`p24/trace_frame_selected_lead_failure_module.md`.

The compact data supports this exact formulation and argues against three
tempting weaker shortcuts:

```text
residual-tail value norm as canonical payload;
component-only annihilator;
sparse low-tail obstruction.
```

The beta-interpolant support boundary is now recorded in:

```text
p24/trace_frame_beta_interpolant_support_scan.py
p24/trace_frame_beta_interpolant_support_boundary.md
p24/axis_crt_fourier_coefficient_support.py
p24/axis_crt_fourier_support_boundary.md
```

It shows that the full leading determinant can have much smaller beta support
than residual-tail determinants in dimension-saturated compact rows, but this
does not become a uniform support-compressed theorem in genuinely partial
rows.  For p24, where the leading projection is `368` coordinates inside a
`537`-dimensional target, sparse support alone is not the certificate engine.
The CRT-axis Fourier boundary adds that the selected-origin Cauchy-Binet
support is not prime-cyclic full support; it is the support of a weighted
spanning-hypertree polynomial for parts `2,157,211`.  That is the right
combinatorial normal form for a future matrix-tree/hypergraph proof, but it
still requires p-unit noncancellation of the CM weights.

The support estimate is now quantified:

```text
p24/axis_crt_hypertree_support_estimate.py

total 368-subsets log10 = 987.668848
support lower log10     = 826.291656
support upper log10     = 957.338867
```

So the CRT support collapse is real but not payload-sized.  It is a proof
language for the determinant-line p-unit theorem, not a replacement
certificate.

The matrix-tree follow-up:

```text
p24/axis_crt_matrix_tree_factorization_toy.py
p24/axis_crt_matrix_tree_factorization_boundary.md
```

rules out the simplest upgrade of that support language.  In exact
`m=6,10,15` analogues and a sampled `m=30` tripartite analogue, the actual
Cauchy-Binet coefficients violate the pair-sum identities required by any
ordinary edge-weight factorization:

```text
c(B) = C * prod_{e in B} a_e.
```

Thus an ordinary matrix-tree/Laplacian determinant cannot be the missing
compression.  A future determinant identity would have to be a mixed
Plucker/exterior identity using the CM spectral weights, or a direct p-unit
PIT/rank-condenser theorem.

If the full determinant-line p-unit theorem is proved, the existing Lean gates
already cover the finite implication to the sub-sqrt certificate surface.

The denominator-safe hybrid gate is:

```text
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
```

It records the currently preferred global package:

```text
Xi_A, Xi_B, Xi_AB, Xi_lead
```

rather than a primary `Xi_tail`.

## Continuation: Useful Computation Boundary

After separating Kummer orbit norms from selected-chain reconstruction, the
useful computations for this route are now small falsifiers for the local-unit
theorem:

```text
does a toy leading determinant vanish?
does a forced kernel look componentwise or genuinely mixed?
does a stronger erasure/MSRD statement fail in compact CM rows?
```

The current reruns give:

```text
p24/tensor_factor_relative_block_erasure_audit.py
  rows=5
  targets=44
  subset_tests=102
  subset_failures=0
  top_failures=0

p24/trace_frame_low_degree_congruence_audit.py
  rows=9
  all high_zero=1
  forced kernels touch 2 or 3 axis blocks
  forced kernels fill the allowed low tail

p24/trace_frame_prefix_intersection_audit.py
  p24-shaped subdegree-2 row:
    component_full=1
    intersection_minimal=1
    prefix_max_rank=1
```

Thus the small data still supports the high-distance/local-unit shape, but it
also argues against trying to multiply independent component certificates.
When failures are forced, they are cross-axis Schubert failures.  The theorem
to prove remains the single denominator-free leading statement:

```text
delta_all in A_all^*
```

or equivalently:

```text
K_sel,Omega = {0}
```

for every beta orbit.  Computation should keep testing this theorem and its
possible MSRD/block-equivalence strengthenings on small CM rows, not search
for the p24 root by enumeration.

The first hidden-MSRD invariant audit is now:

```text
p24/trace_frame_msrd_invariant_audit.py
p24/trace_frame_msrd_invariant_boundary.md
```

It found that pinned `D=-10919, m=12` CM rows satisfy the expected
MSRD-profile block projection/shortening invariants, but random controls do
too.  This leaves hidden MSRD possible but not explanatory at the support
profile level.  The direct determinant-line p-unit theorem remains the
smallest non-generic certificate target.

The current consolidated arithmetic frontier is:

```text
p24/trace_frame_arithmetic_punit_frontier.md
```

It records the equivalent Fitting, crossed-product norm, weighted Fourier, and
Toeplitz selected-minor forms of the same p-unit theorem, and lists which
shortcuts are now closed.
