---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Lean Gates

## Purpose

Map what the Lean files prove and what remains external.

## Current Claim

Lean proves the finite implication chains and size accounting.  It does not
discover or prove the missing CM/Lang arithmetic producer.

## Decisive Evidence

- [Lean gate coverage](../evidence/lean-gate-coverage.md)
- `TraceGcdDualConditionsValueSideGate.lean`: selected product-formula
  obligations imply value-side identities, dual Fourier families, and the
  H-coset verifier.
- `TraceFrameNormCompressedCertificateGate.lean`: inverse payloads imply no
  harmful beta orbits under external determinant-line hypotheses.
- `TraceGcdProjectorTracePipelineGate.lean`: p24 quotient arithmetic and
  post-`B/C` Artin/axis bookkeeping.
- `AxisInjectivityGate.lean`: one-factor Moore-coordinate injectivity implies
  base packet axis injectivity.
- `TraceGcdRecombinedMixedSpectrumGate.lean`: `42+6=48` compressed equation
  split.

## Open Blockers

- The arithmetic p-unit and selected product-formula hypotheses remain
  external.
- Lean file paths moved to `archive/gates/lean`; imports may need path updates
  before compiling from the reorganized tree.

## Next Reads

- [selected product formula](../lanes/selected-product-formula.md)
- [trace-frame p-unit](../lanes/trace-frame-punit.md)
- [L1 axis Moore](../lanes/l1-axis-moore.md)

## Linked Artifacts

- [Lean archive](../archive/gates/lean/)
- [archived Lean README](../archive/gates/lean/README.md)
