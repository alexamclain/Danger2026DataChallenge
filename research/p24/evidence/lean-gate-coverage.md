---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Lean Gate Coverage

## Purpose

Record what the p24 Lean gates prove, and avoid overstating them as a proof of
the missing arithmetic producer theorem.

## Current Claim

Lean is useful here as a finite-logic and bookkeeping layer.  The gates verify
that named hypotheses imply the desired verifier surfaces, equation counts,
orbit decompositions, and payload reductions.  Lean does not currently prove
the selected CM/Lang product-formula theorem, the determinant-line p-unit
theorem, or any strict/no-CM trace selector.

## Decisive Evidence

- `TraceGcdDualConditionsValueSideGate.lean` checks the selected
  product-formula contract from value identities through dual families and
  H-coset verifier implications.
- `TraceFrameNormCompressedCertificateGate.lean` checks that inverse payloads
  imply the harmful beta orbits are excluded under external determinant-line
  hypotheses.
- `TraceGcdProjectorTracePipelineGate.lean` records the p24 quotient
  arithmetic and post-`B/C` Artin/axis bookkeeping.
- `TraceGcdRecombinedMixedSpectrumGate.lean` records the `42+6=48`
  compressed-equation split.
- The Lean README repeatedly marks the arithmetic input as external: p-adic
  unit, nonvanishing, trace-formula, or selected CM embedding statements must
  be supplied outside the finite gates.

## Open Blockers

- Formalize the missing theorem only after the theorem statement is
  mathematically stable enough to be worth encoding.
- Update Lean imports if anyone wants to compile from the reorganized archive
  path instead of treating the files as archived gates.
- Add a small evidence note for any Lean gate that graduates from conditional
  bookkeeping to a proof of an arithmetic input.

## Next Reads

- [Lean gates concept](../concepts/lean-gates.md)
- [certificate surface verdict](p24-certificate-surface-verdict.md)
- [selected product formula verdict](selected-product-formula-verdict.md)

## Linked Artifacts

- [Lean archive](../archive/gates/lean/)
- [archived Lean README](../archive/gates/lean/README.md)
- [value-side Lean gate](../archive/gates/lean/TraceGcdDualConditionsValueSideGate.lean)
- [norm-compressed Lean gate](../archive/gates/lean/TraceFrameNormCompressedCertificateGate.lean)
- [projector trace pipeline Lean gate](../archive/gates/lean/TraceGcdProjectorTracePipelineGate.lean)
- [recombined mixed spectrum Lean gate](../archive/gates/lean/TraceGcdRecombinedMixedSpectrumGate.lean)
