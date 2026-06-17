# P25 v2 Q-Route Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_q_route_candidate_sweep_rows=1/1`

## Purpose

Audit the conductor-39 `Q` support route after its selector, split, square,
extraction, and source-hook screens were separated across several evidence
pages. The question is whether any existing `Q` artifact is already a
source-stage theorem closer. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quotient_complexity_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_route_candidate_sweep_gate.py
```

The gate returned `p25_v2_q_route_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
norm_one_q_value_period156_context
  prior_shape = finite Q value theorem with period-156 context
  decision    = support_route_selector_debt_remains
  missing     = one oriented C4 edge, boundary-zero value, or direct one-edge
                theorem

q3_h90_preimage_finite_theorem
  prior_shape = finite theorem for Q^3 with Q^6=(1-Frob_p)(Q^3)
  decision    = support_route_selector_debt_remains
  missing     = selector/normalization to one legal edge

q6_boundary_only
  prior_shape = Q^6 or Hilbert-90 boundary data only
  decision    = repair_additive_or_value_normalization_missing
  missing     = scalar-fixed finite value/additive theorem plus selector

q_diagonal_value_only
  prior_shape = Q_antisym=m1+m4=m2+m8 diagonal aggregate
  decision    = support_diagonal_aggregate_selector_missing
  missing     = boundary-zero split/orientation or direct one-edge theorem

q_diagonal_plus_support12_row_quotient
  prior_shape = Q diagonal plus support-12 boundary-zero row quotient
  decision    = reject_wrong_split_for_q_diagonal
  falsifier   = support-12 row quotients are not m1-m4 or m2-m8

q_diagonal_plus_correct_split_without_root
  prior_shape = Q diagonal plus m1-m4 or m2-m8 pure quartic split
  decision    = repair_oriented_square_root_missing
  missing     = diagonal plus split reaches 2*edge, not a scalar-fixed edge
                value

q_diagonal_plus_correct_split_with_oriented_root
  prior_shape = Q diagonal plus matching pure quartic split and oriented
                root/sign
  decision    = normalize_to_one_edge_then_apply_source_snippet_intake
  missing     = not present in prior artifacts; still needs theorem data and
                extraction

q_square_exact_fp_value
  prior_shape = exact scalar-fixed finite F_p value for the resulting Q square
  decision    = bounded_two_root_payload_not_source_close
  missing     = two row-value roots still need DANGER3 extraction map

q_square_divisor_boundary_phase_or_scalar_only
  prior_shape = divisor, H90 boundary, quartic phase, or value-up-to-scalar
                for Q square
  decision    = repair_or_reject_sign_and_scalar_missing
  falsifier   = constant sign is invisible to divisor/H90/phase data

local_source_q_language
  prior_shape = local Koo-Shin/KSY/Sprang source language mentioning Q, split,
                theta, or distribution vocabulary
  decision    = no_q_route_source_hook_in_local_sources
  missing     = conductor-39 Q product, Q^3/Q^6 theorem, split/root data,
                Norm_156, or period-156 hook

pure_character_degree6_norm
  prior_shape = degree-6 norm of the pure conductor-39 character word
  decision    = reject_pure_character_degree6_norm_cancels
  falsifier   = Frobenius alternation makes the degree-6 norm zero
```

## Counts

```text
evidence_markers_ok = 11/11
newly_promoted_prior_candidates = 0
surviving_q_intake_families = 4
q_support_route_live = 1
q_square_payload_bounded = 1
current_q_source_hooks = 0
current_source_stage_closers = 0
current_extraction_ready = 0
current_submission_ready = 0
p25_v2_q_route_candidate_sweep_rows=1/1
```

The four surviving Q-route intake families are:

```text
Q or Q^3 theorem data plus selector/boundary-zero normalization to one edge
Q diagonal plus matching pure quartic split plus oriented root/sign
exact scalar-fixed Q-square value plus an extraction map from row roots
direct one-edge finite value/divisor theorem
```

## Verdict

```text
positive_artifact = Q-route prior-art candidate sweep
continue_q_route = yes, but only as a support/normalization route
new_candidate_from_prior_art = no
surviving_q_ask = Q/Q^3 theorem plus selector normalization, Q diagonal plus
                  pure quartic split plus oriented root/sign, exact Q-square
                  value with extraction map, or direct one-edge theorem
discard_condition = answer only supplies Q source language, Q^6 boundary,
                    diagonal aggregate, wrong support-12 split, split without
                    oriented root, square value without extraction map,
                    value-up-to-scalar, generic source Q/split vocabulary, or
                    pure-character degree-6 norm
```

This keeps the Q route alive without overcounting it. It is a compact support
object and a possible normalization/extraction hook, not a replacement for the
one-edge finite theorem.
