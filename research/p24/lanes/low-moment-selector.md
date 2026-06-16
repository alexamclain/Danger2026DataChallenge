---
type: lane
status: background
updated: 2026-06-16
canonical: true
owner: llm
---

# Low-Moment Selector Lane

## Purpose

Track the selected-chain fallback surface based on low moments or selected
relative traces.

## Current Claim

The low-moment surface is sub-sqrt as a verifier/data surface, but it is not
currently an executable p24 certificate search.  The useful burden is 28 new
selected relative trace values, or `8172` parent-field coefficients if kept as
functions.

## Decisive Evidence

- [low-moment selector sweep](../archive/notes/trace_gcd_low_moment_cm_selector_sweep.md)
- [low-moment relative trace gate](../archive/gates/py/trace_gcd_low_moment_relative_trace_gate.py)
- [low-moment Lean gates](../archive/gates/lean/TraceGcdLowMomentRelativeTraceGate.lean)

## Open Blockers

- Construct selected child relative traces intrinsically without class-set
  enumeration.
- Prove sparse-relation anti-collision for the selected path.

## Next Reads

- [certificate surfaces](../concepts/certificate-surfaces.md)
- [selected product formula](selected-product-formula.md)

## Linked Artifacts

- [low moment automatic P1 gate](../archive/gates/py/trace_gcd_low_moment_automatic_p1_entropy_gate.py)
- [low moment sparse relation gate](../archive/gates/py/trace_gcd_low_moment_sparse_relation_gate.py)
- [low moment selector sweep script](../archive/harness/trace_gcd_low_moment_cm_selector_sweep.py)
- [selected-chain vs p-unit boundary](../archive/boundaries/selected_chain_vs_punit_producer_boundary.md)
