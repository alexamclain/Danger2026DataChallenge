---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Certificate Surfaces

## Purpose

Summarize the p24 verifier scales and what each still requires.

## Current Claim

Small verifier surfaces exist conditionally, but none is a completed
certificate until the arithmetic producer theorem is supplied.

## Decisive Evidence

- [p24 certificate surface verdict](../evidence/p24-certificate-surface-verdict.md)
- Four-field-element payload: `D_0,U_0,N_lead,U_lead`, about `21840` Fp slots.
- Fixed-frequency verifier: `156*7 = 1092` equations, compressed as
  `48 = 42 + 6`.
- Low-moment fallback: 30 selected constraints, 28 genuinely new values, or
  `8172` parent-field coefficients.
- Selected-chain fallback: roughly `3.1M` coefficient surface, still
  sub-sqrt but producer-dependent.

## Open Blockers

- Produce p-unit/inverse payloads without enumerating the class set.
- Prove the selected product-formula or determinant-line p-unit theorem.

## Next Reads

- [selected product formula](../lanes/selected-product-formula.md)
- [trace-frame p-unit](../lanes/trace-frame-punit.md)
- [low-moment selector](../lanes/low-moment-selector.md)

## Linked Artifacts

- [norm-compressed Lean gate](../archive/gates/lean/TraceFrameNormCompressedCertificateGate.lean)
- [recombined mixed spectrum Lean gate](../archive/gates/lean/TraceGcdRecombinedMixedSpectrumGate.lean)
- [subsqrt certificate manifest](../archive/theorems/trace_gcd_subsqrt_certificate_manifest.md)
