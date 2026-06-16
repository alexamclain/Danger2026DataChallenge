# Subagent MSRD Equivalence Synthesis

Date: 2026-06-05

The existing subagent was asked whether the trace-frame local-unit theorem can
plausibly be proved through a hidden MSRD/LRS block equivalence.

## Strongest Plausible Theorem

For each p24 beta-orbit algebra `A_Omega`, prove that:

```text
W_axis(A_Omega) subset C^31
```

is p-integrally block-equivalent to an MSRD/LRS sum-rank code of
`E`-dimension `368` and distance at least:

```text
5013.
```

Equivalently, every `3`-block projection among the `31` relative coefficient
blocks is injective.

This would imply the local-unit theorem by:

```text
28*179 < 31*179 - 368 + 1.
```

The finite implication is gated in:

```text
p24/lean/MSRDSupportGate.lean
```

## Required Structure

The subagent emphasized that this route needs an explicit p-unit
block-equivalence:

```text
relative coefficient map B ~= C^31
axis generator matrix
  -- p-integral source change
  -- block-diagonal GL_E(C) target changes
  -- optional block permutation preserving erasure support
= LRS/MSRD generator.
```

Arbitrary flattening or transformations that mix relative coefficient blocks
would not prove the top-three/local-unit theorem.

## Fast Falsifier

The suggested next falsifier is not another erasure scan, since random
controls pass those in the small shapes.  Instead:

```text
normalize two or three coefficient blocks by allowed block maps,
then try to solve for q-linearized/LRS evaluation data explaining the
remaining blocks.
```

Run this on the pinned:

```text
D=-10919, q=11243, m=12
```

row, with random and synthetic LRS controls.  Failure would further demote a
hidden LRS route.

## Verdict

Visible/off-the-shelf MSRD/LRS should be demoted.  The natural basis already
has random-like block ranks and maximal displacement ranks.  A hidden
class-field block equivalence remains logically possible, but it is stronger
than the direct determinant-line p-unit theorem and currently less promising.

The cleaner target remains:

```text
prove the selected leading Plucker/local-unit p-unit directly.
```

