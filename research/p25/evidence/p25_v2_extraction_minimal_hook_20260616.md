# P25 v2 Extraction Minimal Hook

Updated: 2026-06-16

## Purpose

State the shortest post-theorem extraction checklist. This page starts after a
source-stage theorem or exact-P hook has been found. It says what is still
required before a p25 result becomes a DANGER3 certificate.

This is not a source theorem and not a certificate. It is the compact
acceptance boundary for future theorem or expert-answer payloads.

## Pages Read

- `frontier.md`
- `lanes/practical-search.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_extraction_minimal_hook_gate.py
```

The gate returned `p25_v2_extraction_minimal_hook_rows=1/1`.

## Minimal Checklist

```text
accepted_source_theorem_or_exactp_hook
danger3_finite_identity_or_non_cm_framing
same_j_x1_8112_bridge_or_order_8112_generator
practical_x1_16_payload_A_xP16_or_y_plus_model_root
thirty_eight_halving_links_x_chain_or_direct_x0
official_vpp_py_verification
```

## Accepted Routes

```text
official_vpp_verified_triple
  decision = submission_ready

direct_A_x0_plus_vpp
  decision = submission_ready_after_vpp

checkable_x_chain_plus_vpp
  decision = submission_ready_after_vpp
```

## Repair Or Reject Routes

```text
source_theorem_no_framing
  decision = repair_danger3_framing_missing

framed_source_no_same_j_bridge
  decision = repair_same_j_bridge_missing

independent_p16_q507
  decision = reject_unglued_components

same_j_invariant_only
  decision = repair_same_curve_torsion_missing

order8112_generator_only
  decision = repair_x16_surface_missing

x16_y_only
  decision = repair_model_root_missing

x16_surface_no_halving
  decision = repair_halving_or_direct_x0_missing

optional_dgate_surface_only
  decision = repair_optional_not_active_surface

branch_word_without_values
  decision = reject_concrete_values_missing

x0_extracted_vpp_missing
  decision = repair_official_vpp_missing
```

## Counts

```text
evidence_markers_ok = 6/6
required_clauses = 6
accepted_routes = 3
repair_or_reject_routes = 10
current_extraction_ready_rows = 0
current_submission_ready_rows = 0
p25_v2_extraction_minimal_hook_rows=1/1
```

## Verdict

A source theorem or exact-P theorem would be real progress, but not a
certificate. Submission readiness requires concrete same-curve torsion data,
the practical `X_1(16)` payload, a halving chain or direct `x0`, and official
`vpp.py` verification. Branch words, matching `j` alone, independent
`P16/Q507`, and optional d-gate-only payloads do not cross this boundary.
