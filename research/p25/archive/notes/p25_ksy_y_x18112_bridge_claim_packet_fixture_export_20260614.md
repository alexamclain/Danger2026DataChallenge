# P25 KSY-y X1(8112) Bridge-Claim Packet Fixture Export

Updated: 2026-06-14 22:34 PDT

## Purpose

The post-policy bridge work order now has stable JSON fixtures.  These files
are meant for future theorem snippets, Drew follow-up answers, and subagent
reports: copy the nearest fixture, fill the fields honestly, then run the
packet gate.

## Fixture Directory

```text
research/p25/x18112_bridge_claim_packet_fixtures
```

## Fixtures

```text
odd_theorem_only_control.json
  decision = upstream_odd_value_no_cross_level_bridge
  sha256   = abb0e138cd5e1a2804944e94d22f6255716ce05116bf8677b4149bcd0f2a3781

unglued_components_reject.json
  decision = reject_unvalidated_fiber_product_gluing
  sha256   = 30ddb46dfc6dd93ac17b5315cc93a83c301b0be62cf73bf9433d82fda23b7381

same_curve_bridge.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = e403dcc1ce0d43d0c9b7279415c5b4d5ec58b8d3cced771d0021dd2ed221796b

order8112_generator_bridge.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = b659f8f6faf05252eb4f4b654276cf1186c469701cfb704a94d8a907182d2de4

curved_corner_bridge.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = edfbc753633aafd86eac1f6a1ed889aeb405ece3d53131d870bb10138086258a

bridge_surface_no_halving.json
  decision = x16_surface_reached_halving_or_vpp_missing
  sha256   = 280b7ce0545d9ae6f458dad97abed55940c7557bfadb4db5705d82b3b089482b

x0_payload_vpp_missing.json
  decision = extraction_ready_vpp_missing
  sha256   = 8b9dd221fcfc5e8f70d035b8de253b56e681ddd4741a9564760e22275d35d5ce

official_vpp_verified_boundary.json
  decision = submission_ready_verified_triple
  sha256   = 0011678ce73c848d08eef0deb981de3224d08cf077a2c6be631661d1d8b6939a
```

The official-vpp fixture is a boundary shape only.  It is not current evidence.

## Verified Counts

```text
fixture_count          = 8
exact_field_rows       = 8
decision_match_rows    = 8
bridge_target_rows     = 6
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

Audit the fixture set:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x18112_bridge_claim_packet_fixture_export_gate.py
```

Classify a copied packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x18112_bridge_claim_packet_fixture_export_gate.py \
  --packet-json research/p25/x18112_bridge_claim_packet_fixtures/same_curve_bridge.json
```

Expected for the same-curve bridge fixture:

```text
cross_level_target_identified_specialization_missing
ksy_y_x18112_bridge_claim_packet_candidate_rows=1/1
```

## Gate

Marker:

```text
ksy_y_x18112_bridge_claim_packet_fixture_export_rows=1/1
```

## Interpretation

The bridge claim packet gives the post-policy lane a concrete intake format.
A positive bridge claim must preserve same-`j` gluing and be tied to one of
the recorded p25 odd targets.  Independent level-`16` and level-`507` facts
are rejected.  A same-j bridge without practical `X_1(16)` data is progress
but still not extraction.
