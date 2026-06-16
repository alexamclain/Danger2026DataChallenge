---
type: lane
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Selected Product Formula Lane

## Purpose

Track the main conditional p24 route: a selected CM/Lang/Jacobi product
formula after `Tr_{B/C}` on `C_7 x C_179`.

## Current Claim

For a raw packet `g(r,c)` and selected defect `f(r,c)=g(r,c)-g(r,0)`, it is
enough to prove:

```text
g(r,0)+g(-r,0)=A_0;
g(r,c)+g(-r,-c)=A_1 for c != 0;
sum_c g(r,c)-179*g(r,0)=B independent of r.
```

Equivalently, multiplicatively:

```text
U(r,0)U(-r,0) is constant;
U(r,c)U(-r,-c) is constant for c != 0;
prod_c U(r,c)/U(r,0)^179 is independent of r;
the selected degenerate anchor is the normalized R_179/kernel unit.
```

Lean now has a direct selected-product-formula contract feeding the verifier.

## Decisive Evidence

- [selected product formula verdict](../evidence/selected-product-formula-verdict.md)
- [value-side Lean gate](../archive/gates/lean/TraceGcdDualConditionsValueSideGate.lean)
- [selected-defect producer gate](../archive/gates/py/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.py)
- [multiplicative producer dictionary](../archive/gates/py/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.py)
- [symbolic Hasse-Davenport gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py)
- [actual-CM value identity boundary](../archive/boundaries/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.py)

## Open Blockers

- The selected p-integral packet is not constructed.
- Generic actual-CM selected defects fail row balance and inversion
  complement, so the theorem is not generic CM symmetry.
- The raw Jacobi packet needs a single degenerate-anchor normalization.

## Next Reads

- [Jacobi and CM units](../sources/jacobi-cm-units.md)
- [orbit arithmetic](../concepts/orbit-arithmetic.md)
- [expert ask Drew](../operations/expert-ask-drew.md)

## Linked Artifacts

- [punctured Hasse-Davenport theorem note](../archive/theorems/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md)
- [anchor correction gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py)
- [anchor scalar search](../archive/scans/trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search.py)
- [reduced-anchor local unit gate](../archive/gates/py/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.py)
