---
type: lane
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Trace-Frame P-Unit Lane

## Purpose

Track the determinant-line / trace-frame route to a tiny p-unit certificate
payload.

## Current Claim

The downstream verifier can be compressed to four field elements over
`E=F_p(mu_m)`:

```text
D_0, U_0, N_lead, U_lead
D_0*U_0=1
N_lead*U_lead=1
```

This is far below `sqrt(p)`, but it still needs arithmetic p-unit producers
for the selected beta-zero determinant and the nonzero leading norm.

## Decisive Evidence

- [norm-compressed Lean gate](../archive/gates/lean/TraceFrameNormCompressedCertificateGate.lean)
- [beta resultant Lean gate](../archive/gates/lean/TraceFrameBetaResultantGate.lean)
- [leading norm Lean gate](../archive/gates/lean/TraceFrameLeadingNormGate.lean)
- [trace-frame local unit criterion](../archive/theorems/trace_frame_lead_local_unit_criterion.md)

## Open Blockers

- Identify `Xi_lead` as a p-integral determinant-line/modular/Fitting object.
- Prove the selected representative leading determinant is a p-unit.
- Prove determinant-line p-unit transport across 70 tensor factors.
- Prove the beta-zero residual `D_0` p-unit separately.

## Next Reads

- [certificate surfaces](../concepts/certificate-surfaces.md)
- [L1 axis Moore](l1-axis-moore.md)
- [Lean gates](../concepts/lean-gates.md)

## Linked Artifacts

- [selected Plucker certificate](../archive/theorems/trace_frame_selected_plucker_certificate.md)
- [representative leading p-unit certificate](../archive/theorems/representative_leading_punit_certificate.md)
- [beta product resultant audit](../archive/audits/trace_frame_beta_product_resultant_audit.py)
- [beta inverse witness boundary](../archive/boundaries/trace_frame_beta_inverse_witness_boundary.md)
