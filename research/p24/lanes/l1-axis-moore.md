---
type: lane
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# L1 Axis Moore Lane

## Purpose

Track the W_axis / one-factor Moore determinant route.

## Current Claim

Define:

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}
dim W_axis = 368.
```

After adjoining `E=F_p(mu_m)`, each p24 packet splits into 70 degree-5549
tensor factors.  Since `368 < 5549`, one tensor factor can certify the base
packet axis injectivity if the 368 selected coordinates have nonzero Moore
determinant.

## Decisive Evidence

- [AxisInjectivityGate](../archive/gates/lean/AxisInjectivityGate.lean)
- [axis injectivity theorem](../archive/theorems/l1_axis_injectivity_theorem.md)
- [axis injectivity scan](../archive/scans/l1_axis_injectivity_scan.py)
- [tensor-factor Moore audit](../archive/audits/tensor_factor_moore_audit.py)

## Open Blockers

- Prove the actual p24 one-factor Moore determinant is nonzero.
- Connect the p-unit/nonvanishing proof to the final certificate without
  relying on generic random-rank heuristics.

## Next Reads

- [trace-frame p-unit](trace-frame-punit.md)
- [orbit arithmetic](../concepts/orbit-arithmetic.md)
- [Lean gates](../concepts/lean-gates.md)

## Linked Artifacts

- [L1 p-unit boundary](../archive/boundaries/l1_punit_boundary.md)
- [axis module direct sum gate](../archive/theorems/axis_module_direct_sum_gate.md)
- [tensor factor trace period identity](../archive/theorems/tensor_factor_trace_period_identity.md)
