# P25 KSY-y Exact-P X1(8112) Bridge-Claim Packet Fixture Export

Updated: 2026-06-14 21:53 PDT

## Purpose

The external post-policy `X_1(8112)` work order now has stable exact-P JSON
fixtures.  These files are meant for future theorem snippets, Drew follow-up
answers, and subagent reports: copy the nearest fixture, fill the fields
honestly, then run the packet gate.

## Fixture Directory

```text
research/p25/exactp_x18112_bridge_claim_packet_fixtures
```

## Fixtures

```text
exactP_odd_theorem_only_control.json
  decision = upstream_odd_value_no_cross_level_bridge
  sha256   = 7585630b5637635b9e4194e308a33faaffb1bce8449492b641a5ec3ae8bba4df

exactP_unglued_components_reject.json
  decision = reject_unvalidated_fiber_product_gluing
  sha256   = bf0b55802e8d00e8db66e00398cbc1b68b159e05b957fc199a5775ddb6fdf7d3

exactP_same_curve_bridge.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = 7333b62a85c5acc2122f13651d896c37db3248fcbd7d0beea78fb8ad0ab0c3df

exactP_order8112_generator_bridge.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = d780162372a019f9af2561b3e9d7eaece71c23bc5f30f2044413c73203cb73ab

exactP_bridge_surface_no_halving.json
  decision = x16_surface_reached_halving_or_vpp_missing
  sha256   = 6b7906b2f7c474b362537150b758a0ef731e311657743faadb4427822311f2dd

exactP_x0_payload_vpp_missing.json
  decision = extraction_ready_vpp_missing
  sha256   = b8b2c50c5c510d0a385388aec7280a294a18b1f6f4b5718e3250198e35365509

official_vpp_verified_boundary.json
  decision = submission_ready_verified_triple
  sha256   = 0e1cdb58acdfb4056bcecfbeefdd9c69e602de28f652cce6dad6e9270f3f2b5b
```

The official-vpp fixture is a boundary shape only.  It is not current evidence
and uses `odd_payload_object = vpp_boundary`, not `exact_P`.

## Verified Counts

```text
fixture_count          = 7
exact_field_rows       = 7
decision_match_rows    = 7
exact_p_payload_rows   = 6
bridge_target_rows     = 5
x16_surface_rows       = 3
extraction_ready_rows  = 2
submission_ready_rows  = 1
upstream_only_rows     = 1
rejected_rows          = 1
boundary_rows          = 1
current_evidence_rows  = 0
```

Every fixture has all `13` `X18112BridgeTheoremClaim` fields, no unknown
fields, and routes through `p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py`.

## Commands

Audit the exact-P fixture set:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_gate.py
```

Classify a copied packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_gate.py \
  --packet-json research/p25/exactp_x18112_bridge_claim_packet_fixtures/exactP_same_curve_bridge.json
```

Expected for the exact-P same-curve bridge fixture:

```text
cross_level_target_identified_specialization_missing
ksy_y_exactp_x18112_bridge_claim_packet_candidate_rows=1/1
```

## Dependencies

```text
ksy_y_external_post_policy_x18112_work_order_rows=1/1
ksy_y_x18112_bridge_claim_packet_fixture_export_rows=1/1
```

## Gate

Marker:

```text
ksy_y_exactp_x18112_bridge_claim_packet_fixture_export_rows=1/1
```

## Interpretation

The exact-P bridge claim packet gives the exact75 post-policy lane a concrete
intake format.  A positive exact-P bridge claim must preserve same-`j` gluing.
Independent level-`16` and exact-P facts are rejected.  A same-j bridge without
practical `X_1(16)` data is progress but still not extraction.
