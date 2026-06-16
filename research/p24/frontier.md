---
type: operations
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# p24 Frontier

## Purpose

Research cockpit for `p = 10^24 + 7`.  This page should let a new reader
recover the current state without opening the archive.

## Current Claim

No final p24 certificate has been found.  The current best route is a
conditional sub-sqrt verifier whose missing input is an arithmetic producer:
a selected p-integral CM/Lang/R179 product-formula packet after `Tr_{B/C}` on
`C_7 x C_179`.

The downstream formal chain is increasingly tight:

```text
selected product-formula producer
  -> value-side identities
  -> dual Fourier families
  -> admissible C-axis carry
  -> 1092 H-coset verifier / 48 compressed equations
  -> sub-sqrt certificate surface.
```

The strict/no-CM path remains open only as a need for a new finite-field
identity; known trace-residue and filtering routes price back to sqrt scale.

## Decisive Evidence

- [selected product formula verdict](evidence/selected-product-formula-verdict.md)
- [strict non-CM verdict](evidence/strict-non-cm-verdict.md)
- [p24 certificate surface verdict](evidence/p24-certificate-surface-verdict.md)
- [DANGER3 source rule verdict](evidence/danger3-source-rule-verdict.md)
- [selected product formula lane](lanes/selected-product-formula.md)
- [certificate surfaces](concepts/certificate-surfaces.md)
- [orbit arithmetic](concepts/orbit-arithmetic.md)
- [Lean gates](concepts/lean-gates.md)
- [strict non-CM lane](lanes/strict-non-cm.md)
- [run status](operations/run-status.md)

## Open Blockers

- Construct the selected product-formula packet or an equivalent
  determinant/p-unit object without class-set enumeration.
- Prove the normalized degenerate anchor is the `R_179` / kernel-polynomial
  local unit at the selected p24 prime.
- Clarify whether the current challenge forbids exploiting CM; if binding,
  the CM/Lang route must be recast as a non-CM finite-field identity.

## Next Reads

1. [selected product formula](lanes/selected-product-formula.md)
2. [trace-frame p-unit](lanes/trace-frame-punit.md)
3. [strict non-CM](lanes/strict-non-cm.md)
4. [expert ask Drew](operations/expert-ask-drew.md)

## Linked Artifacts

- [fresh-eyes synthesis](archive/handoffs/00_FRESH_EYES_SYNTHESIS_20260607.md)
- [current context archive](archive/handoffs/00_CURRENT_CONTEXT.md)
- [global synthesis archive](archive/handoffs/00_GLOBAL_SYNTHESIS_HANDOFF.md)
- [theorem attempts ledger](archive/handoffs/00_THEOREM_ATTEMPTS_LEDGER.md)
