# Trace-Frame Uncertainty/MSRD Boundary

Date: 2026-06-05

This note records the exact coding-theory shape behind the local-unit
criterion and why generic uncertainty is not enough.

## Code Surface

After multiplying by `g'(theta)` and expanding in the relative basis:

```text
B ~= C^31,        [C:E] = 179,
```

the p24 axis module becomes an `E`-linear array code:

```text
W_axis(B) subset C^31,
dim_E W_axis(B) = 368.
```

The bad low-relative-degree congruence is a nonzero codeword supported on the
first:

```text
28
```

relative coefficient blocks.  In scalar `E`-dimension, this bad support has
size:

```text
28 * 179 = 5012.
```

The Singleton bound for an `E`-linear code of length `31*179` and dimension
`368` is:

```text
d <= 31*179 - 368 + 1 = 5182.
```

So an MSRD/LRS identification of the actual p24 relative coefficient code
would give:

```text
d_sumrank = 5182 > 5012,
```

with slack:

```text
5182 - 5013 = 169.
```

That would rule out the low-degree congruence and prove the leading
trace-frame local-unit theorem.

The finite support implication is now numerically gated in:

```text
p24/lean/MSRDSupportGate.lean
```

as:

```text
p24_trace_frame_bad_support_lt_msrd_distance
no_p24_trace_frame_bad_from_msrd_distance
```

## Why Plain Uncertainty Is Not Enough

The tempting statement is:

```text
smooth K-character support size 368
low relative coefficient support size 5012
```

should be incompatible by an uncertainty principle.  But the bases are not a
prime cyclic Fourier pair, and even in prime cyclic models uncertainty leaves
large feasible ranges.  The centered marginal toy:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
p24/plateau_uncertainty_boundary_toy.py
```

exhibits long plateau/sparse-support words with full nonzero Fourier support.
The trace-frame spectral support boundary:

```text
p24/tensor_factor_plucker_spectral_support.md
```

also shows that full beta-character support is available before using
CM-specific arithmetic.

The sharper Fourier boundary is:

```text
p24/trace_frame_twisted_chebotarev_boundary.md
p24/twisted_chebotarev_minor_toy.py
```

It records the exact false shortcut.  Prime-cyclic Fourier minors are
superregular, and row/column p-unit scalings preserve that.  But the CM
trace-frame map has an interior singular-moduli twist.  A toy `F_11`,
length-`5` example shows that an invertible nonconstant spectral twist can
already have a zero selected `2 x 2` minor.  Thus reduced normality or
nonzero Fourier weights are not enough.

Therefore the useful import is not a generic uncertainty theorem.  It is the
specific arithmetic claim:

```text
the p24 relative coefficient code W_axis(B) is block-equivalent, through
p-unit changes of coordinates, to an MSRD/LRS code,
```

or the weaker selected statement:

```text
the top-three Schubert/Plucker coordinate is a p-unit.
```

## Evidence Boundary

Small audits support the shape but not the proof:

```text
p24/tensor_factor_relative_block_erasure_audit.py
```

reported:

```text
rows=5
targets=44
subset_tests=102
subset_failures=0
top_failures=0
```

A broader bounded scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_relative_block_erasure_audit.py \
  --max-cases 8 --max-abs-D 12000 --min-h 24 --max-h 220 \
  --max-n 160 --max-m 40 --max-factor-degree 18 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-subsets 300 --include-linear
```

reported:

```text
rows=8
targets=48
subset_tests=134
subset_failures=0
top_failures=0
```

However:

```text
p24/trace_frame_lrs_signature_boundary.md
```

found no simple Toeplitz/Hankel/cyclic/LRS displacement signature in the
natural relative coefficient basis.  Thus a successful MSRD route must
produce a non-obvious class-field block equivalence, not just quote the
natural matrix as visibly structured.

A subagent synthesis reached the same conclusion:

```text
p24/subagent_msrd_equivalence_synthesis.md
p24/subagent_cs_probability_local_unit_synthesis.md
```

It recommends demoting visible/off-the-shelf MSRD and keeping only the hidden
class-field block-equivalence theorem as a possible, stronger proof import.

The block-equivalence invariant follow-up is:

```text
p24/trace_frame_msrd_invariant_audit.py
p24/trace_frame_msrd_invariant_boundary.md
```

On the pinned `D=-10919, m=12` rows, the CM code passes the necessary
projection-rank, shortening, and generalized block-support profiles expected
of an MSRD-profile code.  But random controls with the same shapes pass
identically.  Thus these support-profile invariants do not falsify hidden
MSRD, but they are too generic to explain the selected-prime p-unit theorem.
The hidden route still needs an explicit p-unit block-equivalence or a sharper
non-generic invariant.

The immediate cross-ratio idea is bounded in:

```text
p24/trace_frame_block_moduli_boundary.md
```

The current pinned rows have only two or three relative blocks, and the
three-block MDS-profile cases have no stable block-moduli after independent
block basis changes.  Thus sharper MSRD invariant mining needs a richer toy
row or an explicit arithmetic block-equivalence ansatz.

## Current Best Formulation

The proof target can now be stated in three equivalent strengths:

```text
selected Plucker p-unit:
  Delta_lead != 0;

local-unit/Schubert:
  K_sel,Omega =
    { x in W_axis(A_Omega) cap F_28(A_Omega) :
        pi_10(b_28(x)) = 0 }
    = {0};

MSRD strengthening:
  W_axis(B) has sum-rank distance at least 5013.
```

The selected Plucker statement is the smallest certificate surface.  The
MSRD statement is the cleanest possible CS import, but it remains arithmetic:
it needs an exact p-unit block-equivalence or determinant identity for the
actual CM axis module.
