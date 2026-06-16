# P25 KSY-y Twisted/H90 Packet Fixture Export

Updated: 2026-06-14 20:07 PDT

## Purpose

The twisted/H90 candidate-packet intake now has stable JSON examples for the
main theorem-routing boundaries.  These files are meant for future expert
answers, theorem snippets, and subagent reports: copy a nearby fixture, fill
the fields honestly, then run the intake gate.

## Fixture Directory

```text
research/p25/twisted_h90_candidate_packet_fixtures
```

## Fixtures

```text
pure_degree6_norm_reject.json
  decision = reject_pure_degree6_norm_cancels
  sha256   = bb899751f2e995e836c4352e5e270cf547d84847699a83e92cbb16122a2a8767

minimal_source_yes_no_framing.json
  decision = source_theorem_closed_policy_or_framing_missing
  sha256   = 2fb88204442d3a26c44bf6dc54516d3dc28fed91213071690a01d0a1fd93d5fa

policy_yes_no_bridge.json
  decision = danger3_unblocked_cross_level_bridge_missing
  sha256   = 21bbca2f20dbf2c1c22e8d838e345d29c0b1e75f81e8c729345a6537764c4bad

same_j_bridge_no_x16.json
  decision = cross_level_target_identified_specialization_missing
  sha256   = 856c72b3b87307bed6a9840d992d2078da9393a926cc4844f434bed967d2e8c5

official_vpp_verified_boundary.json
  decision = submission_ready
  sha256   = 0a24aa2f3277131669163554475f1a132fe7f8a120b5d67ec69661bc3761b0f1
```

## Verified Counts

```text
fixture_count              = 5
exact_field_rows           = 5
decision_match_rows        = 5
rejected_rows              = 1
source_stage_closed_rows   = 4
danger3_unblocked_rows     = 3
cross_level_bridge_rows    = 2
x16_surface_rows           = 1
extraction_ready_rows      = 1
submission_ready_rows      = 1
```

Every fixture has all `19` packet fields, no unknown fields, and routes through
`p25_ksy_y_twisted_h90_candidate_packet_intake_gate.py`.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_twisted_h90_packet_fixture_export_gate.py
```

Marker:

```text
ksy_y_twisted_h90_packet_fixture_export_rows=1/1
```
