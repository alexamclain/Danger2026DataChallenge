# P25 KSY-y Exact-P Post-Bridge X1(16) Surface Intake

Updated: 2026-06-14 21:57 PDT

## Purpose

This intake starts after an exact-P same-`j` `X_1(8112)` bridge packet.  Each
sample names the exact-P bridge fixture it came from, then routes through the
post-bridge `X_1(16)` surface classifier.

## Sample Directory

```text
research/p25/exactp_post_bridge_x16_surface_packet_samples
```

## Samples

```text
exactP_bridge_only_control.json
  bridge  = exactP_same_curve_bridge.json
  decision = abstract_p16_not_practical_chart

exactP_y_only.json
  bridge  = exactP_same_curve_bridge.json
  decision = y_chart_missing_model_root

exactP_direct_A_xP16_surface.json
  bridge  = exactP_same_curve_bridge.json
  decision = active_surface_reached_halving_missing

exactP_y_model_root_surface.json
  bridge  = exactP_same_curve_bridge.json
  decision = active_surface_reached_halving_missing

exactP_optional_dgate_surface.json
  bridge  = exactP_bridge_surface_no_halving.json
  decision = optional_depth5_surface_reached_halving_missing

exactP_x0_payload_vpp_missing.json
  bridge  = exactP_x0_payload_vpp_missing.json
  decision = x0_extracted_official_vpp_missing

official_vpp_verified_boundary.json
  bridge  = official_vpp_verified_boundary.json
  decision = submission_ready
```

The official-vpp sample is a boundary shape only.  It is not current evidence
and its bridge fixture uses `odd_payload_object = vpp_boundary`.

## Verified Counts

```text
sample_count                = 7
exact_field_rows            = 7
decision_match_rows         = 7
exact_p_bridge_fixture_rows = 6
bridge_established_rows     = 7
active_surface_rows         = 5
optional_dgate_rows         = 1
extraction_ready_rows       = 2
submission_ready_rows       = 1
boundary_rows               = 1
current_evidence_rows       = 0
```

Every sample has all `14` exact-P post-bridge fields, no unknown fields, and
routes through `p25_ksy_y_post_bridge_x16_surface_intake_gate.py`.

## Commands

Audit the sample set:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_post_bridge_x16_surface_intake_gate.py
```

Classify a copied packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_post_bridge_x16_surface_intake_gate.py \
  --packet-json research/p25/exactp_post_bridge_x16_surface_packet_samples/exactP_direct_A_xP16_surface.json
```

Expected:

```text
active_surface_reached_halving_missing
ksy_y_exactp_post_bridge_x16_surface_packet_candidate_rows=1/1
```

## Dependencies

```text
ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_rows=1/1
ksy_y_post_bridge_x16_surface_intake_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
ksy_y_x1_16_halving_chain_contract_rows=1/1
```

## Gate

Marker:

```text
ksy_y_exactp_post_bridge_x16_surface_intake_rows=1/1
```

## Interpretation

An exact-P same-j bridge is not extraction by itself.  The useful next payload
is either direct `A,xP16` or `y` plus model root `x`, reaching the active
`x16halvenonsplit` surface.  From there the missing item is a depth-`4`
halving chain to `x0`, or direct concrete `x0`, followed by official `vpp.py`.
