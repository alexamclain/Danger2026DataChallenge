---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# p24 Orbit Arithmetic

## Purpose

Keep the fixed p24 constants and quotient arithmetic in one canonical place.

## Current Claim

The p24 arithmetic gives strong bookkeeping and small verifier orbits, but it
does not by itself select the embedded class-field root.

## Decisive Evidence

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2*157*211*3107441
m = 66254 = 2*157*211
n = 3107441
sqrt_floor = 10^12

E = F_p(mu_m), [E:F_p] = 5460
B/E degree = 5549 = 31*179
B/C degree = 31
C/E degree = 179
right quotient = C_7
rho = p^780
ord_n(rho)=38843 = 7*5549
```

After `B/C` trace the visible quotient is `C_7 x C_179` of order `1253`.

## Open Blockers

- Cyclic squarefree class-group indexing does not select an embedded child
  root over the ordinary split prime.
- Plain cyclotomic Frobenius has order `89`, not the post-`B/C` order `1253`.

## Next Reads

- [selected product formula](../lanes/selected-product-formula.md)
- [Jacobi and CM units](../sources/jacobi-cm-units.md)

## Linked Artifacts

- [projector trace pipeline Lean gate](../archive/gates/lean/TraceGcdProjectorTracePipelineGate.lean)
- [symbolic Hasse-Davenport gate](../archive/gates/py/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.py)
- [group structure audit](../archive/audits/group_structure_audit.py)
