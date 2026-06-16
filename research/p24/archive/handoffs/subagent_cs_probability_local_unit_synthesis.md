# Subagent CS/Probability Local-Unit Synthesis

Date: 2026-06-05

The existing subagent was asked whether CS, ML, statistics, or probability can
productively lift into the current trace-frame local-unit theorem.

## Verdict

Broad probability, generic uncertainty, and ML are not certificate-level proof
imports for the local-unit theorem.  They remain useful only for falsification
and exact identity discovery.

The only CS-shaped imports that still match the theorem are exact arithmetic
statements:

```text
1. hidden MSRD/LRS block equivalence;
2. direct Fitting/Schubert local-unit p-unit theorem;
3. exact CM-weighted Chebotarev minor theorem.
```

The third is the Fourier version recorded after this synthesis in:

```text
p24/trace_frame_twisted_chebotarev_boundary.md
p24/twisted_chebotarev_minor_toy.py
p24/trace_frame_weighted_fourier_expansion.md
p24/weighted_fourier_cauchy_binet_toy.py
```

## Candidate 1: Hidden MSRD Equivalence

For each beta orbit `Omega`, after reduction at the selected prime, prove that:

```text
W_axis(A_Omega) subset C^31 tensor_E A_Omega
```

is p-unit block-equivalent, preserving the 31 relative `C`-blocks, to an
LRS/MSRD code of sum-rank distance at least:

```text
5013.
```

Then the Lean-gated support implication gives:

```text
W_axis(A_Omega) cap F_27(A_Omega) = {0}.
```

This would prove the local-unit theorem.  The warning is that:

```text
p24/trace_frame_lrs_signature_boundary.md
```

found no visible Toeplitz, Hankel, cyclic, or simple LRS displacement
signature in the natural relative coefficient basis.  Thus this is not an
off-the-shelf code identification; it would require an explicit class-field
p-unit block change.

## Candidate 2: Direct Fitting/Schubert P-Unit

For every beta orbit `Omega`, prove directly that:

```text
W_axis(A_Omega) -> B(A_Omega)/F_27(A_Omega)
```

is injective.  Equivalently:

```text
det(T_lead,Omega) in A_Omega^*
```

and hence:

```text
R_lead,Omega =
  Norm_{A_Omega/O_E}(det T_lead,Omega)
```

is a p-unit.  This is exactly the formulation in:

```text
p24/trace_frame_lead_local_unit_criterion.md
p24/trace_frame_lead_crossed_product_norm.md
```

The subagent considered this cleaner than trying to prove a global MSRD
strengthening first.

## Candidate 3: CM-Weighted Chebotarev

Ordinary prime-cyclic Fourier superregularity would be enough if the bad
Schubert flag and the smooth-axis support were an untwisted Fourier support
pair.  The actual trace-frame map carries an interior singular-moduli twist.

The exact useful theorem is therefore:

```text
For the p24 singular-moduli twist Lambda_CM, the selected
Schubert/trace-frame minor of F_T * diag(Lambda_CM) * F^{-1}_S is a p-unit.
```

This is not separate from the direct local-unit theorem; it is its Fourier
normal form.

The Cauchy-Binet expansion sharpens the warning: even when every Fourier
coefficient in the multilinear determinant expansion is nonzero, a nonconstant
invertible spectral twist can make the selected minor vanish by cancellation.
Thus any successful CS/Fourier proof must prove noncancellation for the actual
CM weights, or exhibit a p-unit coordinate change that removes the interior
twist.

## What Not To Use As A Proof

The following are now demoted to diagnostics:

```text
generic random-subspace rank probability;
ordinary prime-cyclic uncertainty;
nonzero class-character resolvents alone;
component-only nonvanishing;
ML prediction or clustering without an exact identity.
```

They can still be useful for testing proposed lemmas.  They do not replace
the selected-prime p-unit theorem.

## Next Exact Experiment

The subagent suggested one targeted falsification task for the hidden MSRD
route:

```text
compute block-diagonal-equivalence invariants of W_axis subset C^31
on the smallest pinned rows, and compare with synthetic LRS/MSRD controls.
```

If Plucker cross-ratio, generalized-weight, or block-equivalence invariants
mismatch, then the hidden MSRD route should be demoted further and effort
should stay on the determinant-line/Fitting-Schubert p-unit theorem.

## Follow-Up Synthesis

A later read-only sidecar pass reached the same conclusion in the current
trace-frame/Fitting language:

```text
probability is useful as a compass, not as certificate evidence.
```

The productive lift is one of:

```text
1. pointwise Schubert/Fitting p-unit avoidance;
2. p-unit PIT for the weighted exterior polynomial;
3. rank-condenser/MSRD theorem with explicit p-unit arithmetic coordinates.
```

Average-case random-subspace estimates, learned predictors, and generic PIT
remain insufficient for the fixed prime `p = 10^24 + 7`.

The new CRT matrix-tree audit in:

```text
p24/axis_crt_matrix_tree_factorization_toy.py
p24/axis_crt_matrix_tree_factorization_boundary.md
```

adds a graph-theory boundary.  The CRT-axis support is indeed a hypertree
support, but the actual Cauchy-Binet weights violate the pair-sum identities
required by an ordinary per-edge tree polynomial.  Thus a graph import must be
a mixed Plucker/exterior identity or an arithmetic p-unit theorem, not a
standard matrix-tree determinant in hidden edge variables.

## Current Narrowed CS Import

The latest sidecar synthesis sharpened the same conclusion for the
determinant-line formulation:

```text
best coding-theory import:
  hidden MSRD/LRS block equivalence for W_axis(B) subset C^31;

best algebraic-complexity import:
  p-unit PIT / weighted Chebotarev minor theorem for the named Schubert
  determinant;

best language import:
  rank-condenser or subspace-evasive phrasing of
  W_axis(A_Omega) cap F_27(A_Omega) = {0}.
```

The hidden MSRD route is now explicitly falsifiable on small rows:

```text
compare block-equivalence invariants of the pinned D=-10919, m=12
trace-frame code against synthetic LRS/MSRD controls:
  normalized Plucker cross-ratios;
  generalized weights;
  block-diagonal normal forms for q-linearized evaluation.
```

A mismatch would demote hidden MSRD further.  It would not damage the direct
Fitting/Schubert route, whose theorem is already the selected-prime p-unit
statement:

```text
delta_all in A_all^*
```

The relevant finite implication is covered by:

```text
p24/lean/TraceFrameLeadingNormGate.lean
p24/lean/TraceFrameNormCompressedCertificateGate.lean
p24/lean/MSRDSupportGate.lean
```

The first such falsifier is recorded in:

```text
p24/trace_frame_msrd_invariant_audit.py
p24/trace_frame_msrd_invariant_boundary.md
```

Projection-rank, shortening, and generalized block-support profiles passed in
the pinned `D=-10919, m=12` rows, so hidden MSRD is not falsified at this
coarse invariant level.  Random controls passed identically, so these
invariants are also not certificate evidence.  The next MSRD test would need
sharper block-equivalence invariants, not more support-profile scans.
