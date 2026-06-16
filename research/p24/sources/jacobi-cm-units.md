---
type: source
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Jacobi And CM Units

## Purpose

Collect the source story for the selected product-formula route.

## Current Claim

Kubert-Lichtenbaum / Hasse-Davenport / Anderson-style Jacobi machinery
supplies the reduced Jacobi packet shape and the `R_179` anchor footprint.
It does not by itself supply the p24 unramified Artin pullback or selected
CM/Lang packet.

## Decisive Evidence

- `c=179`: `p mod 179 = 77`, `ord_179(p)=89`.
- Nonzero `179`-cyclotomic exponents split into two Frobenius orbits of size
  `89`; inversion swaps the halves.
- The real/inversion quotient gives the degree-89 kernel anchor shape.
- Plain cyclotomic Frobenius realizes order `89`, not the p24 post-`B/C`
  quotient order `1253`.

## Open Blockers

- Need selected CM-Artin pullback along the actual p24 `rho` quotient.
- Need p-integral selected finite coordinate and local-unit avoidance.
- Need selected-child subtraction compatibility.

## Next Reads

- [selected product formula](../lanes/selected-product-formula.md)
- [orbit arithmetic](../concepts/orbit-arithmetic.md)

## Linked Artifacts

- [symbolic Hasse-Davenport gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py)
- [Jacobi anchor correction gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.py)
- [reduced-anchor local unit gate](../archive/gates/py/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.py)
- [literature bundles](../archive/sources/lit/)
