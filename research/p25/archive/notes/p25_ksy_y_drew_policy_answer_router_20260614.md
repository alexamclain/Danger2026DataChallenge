# P25 KSY-y Drew Policy Answer Router

Updated: 2026-06-14 20:49 PDT

## Purpose

This router turns possible Drew replies into local route states.  It is the
companion to the Drew policy question packet: the question packet says what to
ask; this packet says what to do with each kind of answer.

## Answer Rows

```text
no_policy_ruling_yet:
  answer   = Drew does not settle the finite-identity framing boundary
  decision = source_theorem_closed_policy_or_framing_missing
  route    = source stage may close, DANGER3 remains blocked
  next     = keep source theorem as upstream progress; do not spend extraction effort yet

explicit_non_cm_finite_identity_yes:
  answer   = explicit p-specialized finite-field/non-CM identity language is acceptable
  decision = danger3_unblocked_cross_level_bridge_missing
  route    = DANGER3 framing unblocked; bridge missing
  next     = continue to same-j X_1(8112) bridge construction

external_policy_yes_for_ksy_h90:
  answer   = Drew gives policy yes for p-specialized KSY/Kubert-Lang/H90 identity
  decision = danger3_unblocked_cross_level_bridge_missing
  route    = DANGER3 framing unblocked; bridge missing
  next     = continue to same-j X_1(8112) bridge construction

generic_cm_requires_rewrite:
  answer   = generic CM/class-field generation alone is not acceptable
  decision = reject_generic_cm_generation_not_framing
  route    = generic provenance rejected as DANGER3 framing
  next     = rewrite as an explicit finite-field identity for this p or kill the route

same_j_bridge_yes_no_x16:
  answer   = same-j X_1(8112) bridge evidence is accepted, but no practical X_1(16) surface yet
  decision = cross_level_target_identified_specialization_missing
  route    = cross-level target identified; X_1(16) surface missing
  next     = specialize to X_1(16) and expose y/x or A,xP16

x16_payload_yes_no_halving:
  answer   = A,xP16 or y plus model root x is accepted as the active X_1(16) payload
  decision = x16_surface_reached_halving_or_vpp_missing
  route    = X_1(16) surface reached; halving/x0 missing
  next     = derive halving chain or direct x0, then run official vpp.py

concrete_A_x0_no_vpp:
  answer   = concrete A,x0 is supplied but official DANGER3 vpp.py has not passed
  decision = extraction_ready_vpp_missing
  route    = extraction ready; verifier missing
  next     = run official vpp.py immediately and archive output

official_vpp_verified_boundary:
  answer   = concrete p25 A,x0 passes official DANGER3 vpp.py
  decision = submission_ready
  route    = submission boundary reached
  next     = archive command, logs, environment, and certificate
```

The official-vpp row is a boundary shape only.  It is not current evidence.

## Counts

```text
row_count                     = 8
current_evidence_rows         = 0
policy_unblocks_rows          = 2
rewrite_required_rows         = 1
same_j_bridge_rows            = 4
x16_surface_rows              = 3
extraction_ready_rows         = 2
submission_boundary_rows      = 1
current_submission_ready_rows = 0
rejected_rows                 = 1
```

## Dependencies

```text
ksy_y_drew_policy_question_packet_rows=1/1
ksy_y_priority1_post_source_danger3_handoff_rows=1/1
ksy_y_danger3_finite_identity_framing_router_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_drew_policy_answer_router_gate.py
```

Marker:

```text
ksy_y_drew_policy_answer_router_rows=1/1
```

## Interpretation

There are three route-changing answer classes:

```text
Drew policy yes / explicit non-CM finite identity -> same-j X_1(8112) bridge
generic CM/class-field no                         -> rewrite as p-finite identity or kill
concrete A,x0                                     -> official vpp.py immediately
```

This keeps expert feedback executable.  A satisfying but noncommittal answer
stays upstream; it does not justify shifting effort into extraction until the
DANGER3 framing boundary is actually cleared.
