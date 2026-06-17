# P25 v2 End-to-End Answer Router

Updated: 2026-06-16

## Purpose

Classify any future p25 answer without over-counting it. The first-pass
theorem ask, DANGER3 finite-identity framing, extraction payload, and official
verifier boundary are all already promoted. This page stitches them into one
router for Drew answers, source snippets, theorem hits, extraction payloads,
and practical-search hits.

This page does not claim a theorem or certificate exists.

## Pages Read

- `frontier.md`
- `lanes/practical-search.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md`
- `evidence/p25_v2_extraction_minimal_hook_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_end_to_end_answer_router_gate.py
```

The gate returned `p25_v2_end_to_end_answer_router_rows=1/1`.

## Router Stages

```text
stage_0_reject_or_repair
  examples =
    source_legality_only
    boundary_only
    selector_only
    finite_payload_without_source
    generic_cm_or_class_field_generation
    same_j_invariant_only
    independent_p16_q507
    branch_word_without_values
  decision =
    do not promote; route to the first missing clause

stage_1_source_stage_candidate
  accepts =
    one promoted first-pass source theorem from the expert intake packet, or
    heavier exact-P/theta2 upstream theorem
  still_missing =
    DANGER3 finite-identity / non-CM framing

stage_2_danger3_framed_theorem
  accepts =
    source theorem specialized as an exact p25 finite identity, with accepted
    non-CM or challenge-policy framing
  still_missing =
    same-j X_1(8112) bridge or equivalent cross-level map

stage_3_same_j_bridge
  accepts =
    same-curve P16/Q507 pair, order-8112 generator R, or equivalent same-j
    fiber-product data
  still_missing =
    practical X_1(16) y plus model root, or direct A,xP16

stage_4_practical_x1_16_surface
  accepts =
    practical X_1(16) payload: A,xP16 or y plus model root
  still_missing =
    38-link halving chain from depth 4, or direct x0

stage_5_x0_or_x_chain
  accepts =
    concrete A,x0 or a checkable x-coordinate halving chain/witness chain
  still_missing =
    official src/vpp.py verification

stage_6_official_vpp_verified
  accepts =
    official vpp.py verifies concrete (p,A,x0)
  decision =
    submission_ready
```

## Current State

```text
current_source_theorems = 0
current_danger3_framed_theorems = 0
current_same_j_bridges = 0
current_x1_16_payloads = 0
current_x0_or_x_chain_payloads = 0
current_extraction_ready_rows = 0
submission_ready_rows = 0
```

The production fleet remains the only concrete certificate path today. A
theorem-stage answer would be real progress, but it only reaches a certificate
after every downstream stage above.

## Intake Rule

For a future answer, stop at the first failed stage:

```text
source snippet or Drew theorem
-> first-pass expert intake packet
-> DANGER3 finite-identity framing contract
-> extraction minimal hook
-> extraction payload contract
-> official vpp.py regression/verifier boundary
```

This deliberately separates four different wins:

```text
mathematical target pinned
source-stage theorem found
DANGER3-framed theorem found
verified p25 certificate found
```

Only the last one is a challenge submission.

## Counts

```text
source_markers_ok = 5/5
vpp_boundary_ok = 3/3
router_stages = 7/7
repair_or_reject_examples = 7
accepted_submission_stage = 1
current_source_theorems = 0
current_danger3_framed_theorems = 0
current_extraction_ready_rows = 0
submission_ready_rows = 0
p25_v2_end_to_end_answer_router_rows=1/1
```

## Verdict

Use this router after any future expert answer, source snippet, theorem hit, or
candidate extraction payload. A result is promoted only to the highest stage
whose clauses it actually satisfies. In particular, source legality,
CM/class-field generation, boundary data, matching `j`, independent
`P16/Q507`, branch words, and unverified `x0` payloads remain repair or reject
rows until the missing downstream clauses are supplied.
