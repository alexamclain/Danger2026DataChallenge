---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# p24 Certificate Surface Verdict

## Purpose

Summarize the finite verifier surfaces available for p24 and separate verifier
size from producer difficulty.

## Current Claim

p24 has several sub-sqrt verifier surfaces, but none is a completed
certificate until an honest producer supplies the values without class-set
enumeration.  The best live surface is the selected product-formula route
feeding a `1092` H-coset verifier or a `48 = 42 + 6` compressed equation
split.  Broader fallback surfaces stay sub-sqrt for this fixed p24 instance,
but they shift the missing work to selected trace values or large coefficient
payloads.

## Decisive Evidence

- Four-field-element trace-frame payloads reduce the object to
  `D_0,U_0,N_lead,U_lead`, about `21840` base-field slots after expansion.
- The fixed-frequency verifier has `156*7 = 1092` equations and a compressed
  `42+6=48` split.
- The low-moment fallback needs 30 selected constraints, 28 genuinely new
  values, or `8172` parent-field coefficients.
- The selected-chain fallback is roughly `3.1M` coefficients, still below
  `sqrt(p)=10^12` for this fixed p24 instance, but not a satisfying
  asymptotic producer unless its construction is also class-set-free.
- The certificate manifest stresses the central honesty condition: small
  payloads prove something only if the producer theorem identifies them with
  the actual trace-GCD determinants or packets.

## Open Blockers

- Produce the determinant-line p-unit, product-formula packet, or selected
  relative-trace payload without enumerating the CM class set.
- Prove the values belong to the actual p24 verifier row, not just to an
  abstract finite model.
- Decide whether fallback surfaces are worth operationalizing before the
  producer theorem is known.

## Next Reads

- [certificate surfaces concept](../concepts/certificate-surfaces.md)
- [selected product formula verdict](selected-product-formula-verdict.md)
- [Lean gate coverage](lean-gate-coverage.md)

## Linked Artifacts

- [subsqrt certificate manifest](../archive/theorems/trace_gcd_subsqrt_certificate_manifest.md)
- [norm-compressed Lean gate](../archive/gates/lean/TraceFrameNormCompressedCertificateGate.lean)
- [recombined mixed spectrum Lean gate](../archive/gates/lean/TraceGcdRecombinedMixedSpectrumGate.lean)
- [low-moment selector lane](../lanes/low-moment-selector.md)
- [trace-frame p-unit lane](../lanes/trace-frame-punit.md)
