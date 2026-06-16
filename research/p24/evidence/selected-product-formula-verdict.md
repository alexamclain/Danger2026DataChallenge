---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Selected Product Formula Verdict

## Purpose

State what the selected CM/Lang/Jacobi product-formula work currently
establishes, and what remains unproved.

## Current Claim

The finite verifier side is credible and sharply specified: if a selected
p-integral packet after `Tr_{B/C}` satisfies the product-formula identities,
then the existing finite gates carry it to the p24 sub-sqrt verifier surface.

The missing theorem is not a generic CM symmetry.  Small actual-CM boundary
tests show that ordinary embedded projector, right-combo, weighted-coefficient,
and selected-defect packets fail the needed row-balance and inversion
identities.  The live target is therefore a specific selected trace-GCD /
CM-Lang packet, likely expressible through a reduced Jacobi principal divisor
or local unit.

## Decisive Evidence

- The reduced finite-field Jacobi model has the right shape: punctured
  Hasse-Davenport pair products plus one degenerate-anchor correction imply
  the constant pair-product and row-product identities.
- The exact small gates checked `c=5,11,13`; the symbolic gate checked the
  residue/Gauss-factor cancellation for `c=5,11,13,17,19,179`.
- For p24, the symbolic check covers all `189036` right-mixed admissible
  pairs in the finite-field Jacobi model.
- The actual-CM value-identity boundary reports generic failure of the same
  identities on nearby embedded CM packets, so the proof cannot be "CM packets
  are automatically balanced."
- The Lean value-side gate treats the product formula as a hypothesis and
  verifies the downstream implication chain.

## Open Blockers

- Construct the selected p-integral CM/Lang packet without class-set
  enumeration.
- Prove the selected degenerate anchor is the normalized `R_179` /
  kernel-polynomial local unit for the p24 embedding.
- If the no-CM rule is binding, recast the same finite identity as a non-CM
  finite-field theorem rather than a CM exploitation.

## Next Reads

- [selected product formula lane](../lanes/selected-product-formula.md)
- [Jacobi and CM units](../sources/jacobi-cm-units.md)
- [expert ask Drew](../operations/expert-ask-drew.md)

## Linked Artifacts

- [punctured Hasse-Davenport theorem note](../archive/theorems/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md)
- [symbolic Hasse-Davenport gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py)
- [anchor correction gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py)
- [selected-defect producer gate](../archive/gates/py/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.py)
- [actual-CM value identity boundary](../archive/boundaries/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.py)
- [value-side Lean gate](../archive/gates/lean/TraceGcdDualConditionsValueSideGate.lean)
