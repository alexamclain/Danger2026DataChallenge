# P25 KSY-y Post-Surface Halving/VPP Intake

Updated: 2026-06-14 21:03 PDT

## Purpose

This intake starts after the active `X_1(16)` surface has reached `A,xP16`.
It separates:

```text
surface reached
verified halving prefix
full x_4 ... x_42 chain
direct A,x0 payload
official vpp.py submission boundary
```

The active shape is:

```text
start_depth   = 4
final_depth   = 42
halving_links = 38
x_chain_points = 39
```

## Route Rows

```text
surface_only:
  decision = surface_reached_certificate_missing
  missing  = x-chain, sqrt-witness chain, direct x0, or vpp-verified triple

one_link_verified_prefix:
  decision = partial_x_chain_verified_not_extraction
  links    = 1/1
  missing  = full 39-point chain x_4 through x_42

chain_without_xP16:
  decision = conditional_chain_without_xP16_start
  missing  = xP16 start value for x_4

chain_start_mismatch:
  decision = reject_chain_start_mismatch
  missing  = chain first value must equal xP16

chain_link_mismatch:
  decision = reject_chain_link_mismatch
  missing  = xDBL link at depth 4 failed

chain_x0_tail_mismatch:
  decision = reject_x0_tail_mismatch
  missing  = x0 must equal the final chain value

direct_A_x0_no_vpp:
  decision = direct_x0_vpp_missing
  missing  = official vpp.py verification

direct_A_x0_vpp_fails:
  decision = reject_vpp_failed
  missing  = official vpp.py rejected the supplied A,x0

missing_A:
  decision = reject_missing_A
  missing  = Montgomery A
```

## Counts

```text
row_count             = 9
current_evidence_rows = 0
surface_missing_rows  = 1
partial_chain_rows    = 1
full_chain_rows       = 0
direct_x0_rows        = 1
extraction_ready_rows = 1
vpp_executed_rows     = 1
submission_ready_rows = 0
rejected_rows         = 5
boundary_rows         = 0
```

## Dependencies

```text
ksy_y_post_bridge_x16_surface_intake_rows=1/1
ksy_y_h0_x16_halving_chain_payload_intake_rows=1/1
ksy_y_x1_16_halving_certificate_payload_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_surface_halving_vpp_intake_gate.py
```

The gate also accepts copied packet JSON:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_surface_halving_vpp_intake_gate.py \
  --packet-json <packet.json>
```

Sample packet:

```text
research/p25/post_surface_halving_vpp_packet_samples/one_link_verified_prefix.json
```

Expected:

```text
partial_x_chain_verified_not_extraction
ksy_y_post_surface_halving_vpp_packet_candidate_rows=1/1
```

Marker:

```text
ksy_y_post_surface_halving_vpp_intake_rows=1/1
```

## Interpretation

A verified halving prefix is real progress but not extraction-ready.  The
submission path needs one of:

```text
full x_4=xP16, x_5, ..., x_42=x0 chain, then official vpp.py
direct A,x0 payload, then official vpp.py
official vpp.py-verified A,x0
```

Any failed official `vpp.py` run kills that concrete payload.
