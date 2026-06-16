# P25 KSY-y H0/X1(16) Final Certificate Boundary

Updated: 2026-06-14 16:06 PDT

## Purpose

This packet is the final extraction boundary for the H0/order-8112 route after
it reaches the practical `X_1(16)` chart.  It prevents an H0 chart surface,
branch word, or internal verifier from being mistaken for a DANGER3
submission.

## Shape

```text
p mod 8        = 5
start_depth    = 4
final_depth    = 42
halving_links  = 38
x_chain_points = 39
vpp_doublings  = 42
```

The active route starts from `(A,xP16)` at depth `4`.  A certificate can be
made checkable by giving the x-coordinate chain
`x4=xP16, x5, ..., x42=x0`, or by giving square-root witnesses and active
branch provenance.  Neither is a submission until official `vpp.py` verifies
the concrete `(p,A,x0)` triple.

## Boundary Rows

```text
h0_order8112_chart_surface_only:
  decision = surface_reached_certificate_missing
  missing  = x-chain, sqrt-witness chain, direct x0, or vpp-verified triple

h0_branch_word_without_values:
  decision = reject_branch_word_without_values
  missing  = actual square-root witnesses, x-chain, or x0

h0_sqrt_witness_chain:
  decision = active_path_provenance_vpp_missing
  missing  = official vpp.py verification

h0_x_coordinate_chain:
  decision = checkable_x_chain_vpp_missing
  missing  = official vpp.py verification

h0_direct_A_x0:
  decision = direct_x0_vpp_missing
  missing  = official vpp.py verification

h0_internal_verify_only:
  decision = internal_verify_not_submission
  missing  = official vpp.py verification and archived output

h0_vpp_verified_triple:
  decision = submission_ready
  missing  = none
```

## Counts

```text
row_count              = 7
surface_reached_rows   = 5
rejected_rows          = 1
x_chain_rows           = 2
sqrt_witness_rows      = 2
direct_x0_rows         = 5
internal_verify_rows   = 2
official_vpp_rows      = 1
non_submission_rows    = 6
submission_ready_rows  = 1
```

## Meaning

The H0/order-8112 chart surface is a real downstream target, but it is still
not a certificate.  The last mile is one of:

```text
A,xP16 + x-chain -> x0 -> official vpp.py
A,xP16 + sqrt witnesses/branch provenance -> x0 -> official vpp.py
A,x0 directly -> official vpp.py
```

Only the last verified `(p,A,x0)` state is submission-ready.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_final_certificate_boundary_gate.py
```

Marker:

```text
ksy_y_h0_x16_final_certificate_boundary_rows=1/1
```
