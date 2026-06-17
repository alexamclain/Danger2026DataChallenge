# P25 v2 Constructive Value Payload Contract

Updated: 2026-06-16

## Purpose

Close the small gap between a source-stage theorem shape and the packet/extraction
workflow. A future answer must not only select a legal row and fix the
`F_p^*` scalar; it must also provide deterministic finite data that can be
evaluated or packetized. Otherwise it is still a theorem-language lead, not a
payload the DANGER3 ladder can consume.

This contract does not change the first-pass theorem target. It clarifies what
kind of finite data is constructive enough to move from source intake into
candidate-packet intake and post-theorem extraction.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_candidate_packet_intake_reorg_20260616.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_constructive_value_payload_contract_gate.py
```

The gate returned `p25_v2_constructive_value_payload_contract_rows=1/1`.

## Accepted Constructive Payload Shapes

```text
exact_fp_row_value_from_source
  decision = source_stage_packetizable_danger3_framing_missing
  missing  = DANGER3 finite-identity framing, then same-j/X_1(16)/halving
             extraction

finite_additive_or_telescoping_formula
  decision = source_stage_packetizable_danger3_framing_missing
  missing  = DANGER3 finite-identity framing, then same-j/X_1(16)/halving
             extraction

period156_value_with_branch_payload
  decision = source_stage_packetizable_danger3_framing_missing
  missing  = DANGER3 finite-identity framing, then same-j/X_1(16)/halving
             extraction

exact_product_file_plus_source_theorem
  decision = source_stage_packetizable_danger3_framing_missing
  missing  = DANGER3 finite-identity framing, then same-j/X_1(16)/halving
             extraction
```

These are not submissions. They are source-stage hits that can enter the
packet workflow because they contain enough finite data to evaluate or check
one legal support-156 row.

## Repair And Reject Rows

```text
scalar_fixed_theorem_no_evaluation_rule
  decision = repair_constructive_evaluation_missing
  missing  = deterministic finite formula, basepoint, telescoping product,
             branch data, or exact product packet

class_field_generation_or_existence_only
  decision = repair_selected_constructive_row_missing
  missing  = one legal support-156 row plus scalar-fixed finite evaluation data

local_finite_payload_no_source
  decision = repair_arithmetic_source_theorem_missing
  missing  = challenge-legal arithmetic source theorem for the finite payload

direct_vpp_from_row_value
  decision = reject_row_value_is_not_A_x0
  missing  = vpp.py verifies (p,A,x0), not a modular-unit row value
```

## Counts

```text
packetizable_source_shapes = 4
repair_rows = 3
reject_rows = 1
current_packetizable_payloads = 0
current_submission_ready = 0
```

## Verdict

```text
positive_artifact = constructive-payload intake contract
continue_first_pass = yes
intake_rule = source hit must select a legal row, fix the scalar, and provide
              deterministic finite data evaluable by packet intake
discard_condition = answer remains only existence/generation language, lacks
                    evaluation data, lacks arithmetic source, or treats a row
                    value as a direct vpp.py candidate
```
