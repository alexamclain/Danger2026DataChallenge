# P25 KSY-y Exact-P Post-Surface Halving/VPP Intake

Updated: 2026-06-14 22:01 PDT

## Purpose

This intake starts after an exact-P post-bridge `X_1(16)` surface sample reaches
the active surface or a direct `x0` boundary.  Each sample names the exact-P
surface sample it came from, then routes through the numeric halving/vpp
classifier.

## Sample Directory

```text
research/p25/exactp_post_surface_halving_vpp_packet_samples
```

## Samples

```text
exactP_surface_only.json
  surface = exactP_direct_A_xP16_surface.json
  decision = surface_reached_certificate_missing

exactP_one_link_verified_prefix.json
  surface = exactP_direct_A_xP16_surface.json
  decision = partial_x_chain_verified_not_extraction
  links    = 1/1

exactP_chain_without_xP16.json
  surface = exactP_direct_A_xP16_surface.json
  decision = conditional_chain_without_xP16_start

exactP_chain_start_mismatch.json
  surface = exactP_direct_A_xP16_surface.json
  decision = reject_chain_start_mismatch

exactP_chain_link_mismatch.json
  surface = exactP_direct_A_xP16_surface.json
  decision = reject_chain_link_mismatch

exactP_chain_x0_tail_mismatch.json
  surface = exactP_direct_A_xP16_surface.json
  decision = reject_x0_tail_mismatch

exactP_direct_A_x0_no_vpp.json
  surface = exactP_x0_payload_vpp_missing.json
  decision = direct_x0_vpp_missing

exactP_direct_A_x0_vpp_fails.json
  surface = exactP_x0_payload_vpp_missing.json
  decision = reject_vpp_failed

exactP_missing_A.json
  surface = exactP_direct_A_xP16_surface.json
  decision = reject_missing_A
```

## Verified Counts

```text
sample_count                 = 9
exact_field_rows             = 9
decision_match_rows          = 9
source_surface_ready_rows    = 9
source_extraction_ready_rows = 2
surface_missing_rows         = 1
partial_chain_rows           = 1
full_chain_rows              = 0
direct_x0_rows               = 1
extraction_ready_rows        = 1
vpp_executed_rows            = 1
submission_ready_rows        = 0
rejected_rows                = 5
boundary_rows                = 0
current_evidence_rows        = 0
```

Every sample has all `10` exact-P post-surface fields, no unknown fields, and
routes through `p25_ksy_y_post_surface_halving_vpp_intake_gate.py`.

## Commands

Audit the sample set:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_post_surface_halving_vpp_intake_gate.py
```

Classify a copied packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_post_surface_halving_vpp_intake_gate.py \
  --packet-json research/p25/exactp_post_surface_halving_vpp_packet_samples/exactP_one_link_verified_prefix.json
```

Expected:

```text
partial_x_chain_verified_not_extraction
ksy_y_exactp_post_surface_halving_vpp_packet_candidate_rows=1/1
```

## Dependencies

```text
ksy_y_exactp_post_bridge_x16_surface_intake_rows=1/1
ksy_y_post_surface_halving_vpp_intake_rows=1/1
ksy_y_x1_16_halving_certificate_payload_rows=1/1
```

## Gate

Marker:

```text
ksy_y_exactp_post_surface_halving_vpp_intake_rows=1/1
```

## Interpretation

An exact-P `A,xP16` surface still needs either a full `x_4` through `x_42`
halving chain or a direct concrete `x0`.  A verified one-link prefix is real
progress but not extraction-ready.  A direct `A,x0` payload still requires
official `vpp.py`, and failed `vpp.py` rejects that concrete payload.
