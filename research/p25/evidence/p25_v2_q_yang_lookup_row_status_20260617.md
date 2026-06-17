# P25 v2 Q/Yang Lookup-Row Status

Updated: 2026-06-17

Marker: `p25_v2_q_yang_lookup_row_status_rows=1/1`

## Purpose

Turn the conductor-39 Q/Yang/H90 row from the priority-1 source lookup capsule
into a compact source/expert checklist. This artifact does not re-audit the
Q route; it summarizes the validated Yang/H90 contract, selector-debt,
diagonal, quartic-split, Q-square, extraction-boundary, source-hook, and
candidate-sweep screens.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/koo-shin-ii-1007-2318.md`
- `sources/sprang.md`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_q_route_candidate_sweep_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_yang_lookup_row_status_gate.py
```

The gate returned `p25_v2_q_yang_lookup_row_status_rows=1/1`.

## Status Rows

```text
mixed_yang_h90_direct_theorem
  current_status = live_not_in_hand
  accepted_hook  = mixed U_chi/W source theorem with level-507 Yang lift,
                   Hilbert-90 descent to Norm_156(Y_507), and scalar-fixed
                   finite divisor/additive or period-156 value theorem for one
                   legal support-156 row
  first_falsifier = mixed source word only, Yang lift only, H90 boundary only,
                    source legality only, projection, suborbit, or
                    wrong-boundary lift
  decision        = continue_only_on_full_finite_theorem

q_or_q3_finite_theorem
  current_status = support_only_until_selector_paid
  accepted_hook  = finite Q value theorem with period-156 context, or finite
                   Q^3 Hilbert-90 theorem, plus selector/boundary-zero
                   normalization to one oriented edge
  first_falsifier = Q source language, Q^6 boundary, Q value without
                    period-156 context, or Q/Q^3 theorem without edge selector
  decision        = continue_only_with_selector_normalization

q_diagonal_plus_quartic_split
  current_status = live_support_normalizer_not_in_hand
  accepted_hook  = Q diagonal aggregate plus matching pure quartic split plus
                   oriented root/sign or explicit oriented diagonal-split
                   normalization
  first_falsifier = diagonal only, support-12 row quotient, wrong split, pure
                    quartic split only, or split without oriented root/sign
  decision        = normalize_then_apply_source_snippet_intake

q_square_payload
  current_status = payload_not_source_stage
  accepted_hook  = exact scalar-fixed Q-square finite value plus extraction map
                   from the two row roots to same-j/X_1(16)/halving data or
                   concrete A,x0 candidates
  first_falsifier = Q-square divisor, H90 boundary, quartic phase, value up to
                    scalar, exact row roots without extraction map, or direct
                    vpp.py on row values
  decision        = keep_as_extraction_payload_only

local_source_scan
  current_status = local_sources_negative
  accepted_hook  = none in local Koo-Shin/KSY/Koo-Shin II/Sprang source corpus
  first_falsifier = generic Q, generic splitting/diagonal, theta/distribution,
                    ray-class generation, or source-legality vocabulary
  decision        = ask_narrow_external_or_expert_question_only

direct_one_edge_fallback
  current_status = same_target_as_priority1
  accepted_hook  = scalar-fixed finite theorem for one legal oriented edge
                   with Norm_156(Y_507) boundary
  first_falsifier = aggregate, diagonal, two-edge, row-square, boundary-only,
                    or selector-only statement
  decision        = route_back_to_priority1_divisor_additive
```

## Counts

```text
evidence_markers_ok = 10/10
status_rows = 6
surviving_q_intake_families = 4
current_q_source_hooks = 0
current_source_stage_closers = 0
current_extraction_ready = 0
current_submission_ready = 0
p25_v2_q_yang_lookup_row_status_rows=1/1
```

## Verdict

The conductor-39 Q/Yang row remains live, but not as broad Q vocabulary. The
useful asks are now exactly:

```text
1. direct mixed U_chi/W Yang/H90 finite theorem for one legal support-156 row;
2. Q or Q^3 finite theorem with selector debt paid;
3. Q diagonal plus correct pure quartic split plus oriented root/sign;
4. exact scalar-fixed Q-square value plus an extraction map;
5. direct one-edge scalar-fixed finite theorem, which routes back to priority 1.
```

Everything else is support, repair, or reject. The local Koo-Shin/KSY/Koo-Shin
II/Sprang corpus has no current Q-route source hook, so the next useful
literature/expert ask should name the exact Q/Yang object, not ask for
generic conductor-39 or Hilbert-90 material.
