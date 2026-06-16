# P25 KSY-y Twisted/H90 Candidate-Packet Intake

Updated: 2026-06-14 20:03 PDT

## Purpose

This is the practical intake boundary for future theorem snippets, expert
answers, or subagent reports about the twisted ratio/Hilbert-90 route.  It
routes one packet through:

```text
twisted/H90 source classifier
  -> DANGER3 finite-identity/non-CM framing
  -> same-j X_1(8112) bridge
  -> X_1(16) surface or A,xP16
  -> concrete A,x0
  -> official vpp.py
```

It returns the first missing stage or hard falsifier.

## Packet Fields

```text
name
theorem_body_verified
uses_degree6_orbit
uses_pure_norm
uses_pair_sum
uses_signed_shadow
uses_quotient_or_ratio
uses_hilbert90_boundary
finite_value_or_divisor_theorem
period156_context
arithmetic_source_theorem
finite_field_identity_for_p
generic_cm_or_class_field_generation
explicit_non_cm_finite_field_framing
danger3_policy_accepts_identity
same_j_x18112_bridge
x16_surface_or_A_xP16
concrete_A_x0
official_vpp
```

## Regression Decisions

```text
no_theorem_body:
  reject_no_theorem_body

pure_degree6_norm:
  reject_pure_degree6_norm_cancels

h90_boundary_only:
  helper_only_hilbert90_boundary_value_theorem_missing

twisted_value_no_period156:
  conditional_value_theorem_missing_period156_context

twisted_period156_payload_no_source:
  conditional_finite_payload_without_source_theorem

source_theorem_not_p_finite_identity:
  source_theorem_value_shape_missing_finite_identity

generic_cm_not_framing:
  reject_generic_cm_generation_not_framing

source_finite_identity_no_framing:
  source_theorem_closed_policy_or_framing_missing

policy_yes_no_bridge:
  danger3_unblocked_cross_level_bridge_missing

same_j_bridge_no_x16:
  cross_level_target_identified_specialization_missing

x16_surface_no_x0:
  x16_surface_reached_halving_or_vpp_missing

concrete_A_x0_no_vpp:
  extraction_ready_vpp_missing

official_vpp_verified:
  submission_ready
```

## Counts

```text
row_count                       = 13
rejected_rows                   = 3
helper_only_rows                = 1
conditional_rows                = 2
source_shape_missing_rows       = 1
policy_or_framing_missing_rows  = 1
source_stage_closed_rows        = 6
danger3_unblocked_rows          = 5
cross_level_bridge_rows         = 4
x16_surface_rows                = 3
extraction_ready_rows           = 2
submission_ready_rows           = 1
```

## Dependencies

```text
ksy_y_twisted_h90_minimal_closing_ask_packet_rows=1/1
ksy_y_danger3_finite_identity_framing_router_rows=1/1
ksy_y_cross_level_bridge_source_route_packet_rows=1/1
```

## CLI

Run the regression gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_twisted_h90_candidate_packet_intake_gate.py
```

Classify a concrete JSON packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_twisted_h90_candidate_packet_intake_gate.py \
  --packet-json <packet.json>
```

Marker:

```text
ksy_y_twisted_h90_candidate_packet_intake_rows=1/1
```

## Fixture Examples

Stable JSON examples live in:

```text
research/p25/twisted_h90_candidate_packet_fixtures
```

Validate them with:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_twisted_h90_packet_fixture_export_gate.py
```

Marker:

```text
ksy_y_twisted_h90_packet_fixture_export_rows=1/1
```

## Interpretation

This packet is stricter than the source-stage closing ask.  A period-`156`
arithmetic source theorem is real moonshot progress, but it is not DANGER3
progress until it is also a finite identity for this `p`, framed as acceptable
non-CM/challenge language or accepted by policy, bridged through the same
`j`-invariant to `X_1(16)`, and verified by official `vpp.py`.
