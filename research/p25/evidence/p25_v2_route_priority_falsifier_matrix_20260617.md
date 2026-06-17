# P25 v2 Route Priority / Falsifier Matrix

Updated: 2026-06-17

Marker: `p25_v2_route_priority_falsifier_matrix_rows=1/1`

## Purpose

Turn the accepted H0/conductor-39/exact-P presentations into an ordered
working table. The goal is to keep future passes from treating support
surfaces as independent moonshots, while still preserving every theorem shape
that can normalize to one scalar-fixed legal support-156 row.

This is not a new source theorem. It is the priority and first-falsifier layer
on top of the existing intake and normalization spine.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_q_route_candidate_sweep_20260617.md`
- `evidence/p25_v2_exactp_candidate_sweep_20260617.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_end_to_end_answer_router_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_route_priority_falsifier_matrix_gate.py
```

The gate returned `p25_v2_route_priority_falsifier_matrix_rows=1/1`.

## Ordered Routes

```text
1. direct_scalar_fixed_divisor_additive
   class           = first_pass_source_closer
   closer          = finite divisor/additive theorem for one normalized legal row
   first_falsifier = source legality, boundary-only, selector-only, or
                     unspecified scalar
   decision        = continue_as_preferred_ask

2. support_period156_value
   class           = first_pass_source_closer
   closer          = support-period-156 value theorem with branch/root/
                     telescoping data
   first_falsifier = ambient-period-780 value, mu11 quotient, or degree-6
                     value without Fp descent
   decision        = continue_as_value_side_ask

3. power_normalized_row_value
   class           = first_pass_normalizer
   closer          = exact source theorem for R_m^e,
                     e in {3,5,13,39,75,169,507}, plus inverse recovery
   first_falsifier = power value without row selector, boundary bridge, or
                     arithmetic source theorem
   decision        = normalize_then_route_to_one_edge

4. quartic_character_finite_theorem
   class           = first_pass_normalizer
   closer          = exact C4_1 phase, mixed row sign, orientation, and
                     scalar-fixed theorem
   first_falsifier = selector-only, coarse phase, wrong reciprocal boundary,
                     or missing finite theorem
   decision        = normalize_then_route_to_one_edge

5. row_labeled_or_reciprocal_presentation
   class           = first_pass_normalizer
   closer          = row-labeled orbit theorem or reciprocal-minus-boundary
                     theorem containing one legal row
   first_falsifier = unordered orbit, symmetric aggregate, reciprocal plus
                     boundary, or outside-orbit row
   decision        = normalize_then_route_to_one_edge

6. q_support_route
   class           = support_not_front_door
   closer          = Q/Q3 theorem plus selector normalization, or Q diagonal
                     plus split plus oriented root
   first_falsifier = Q source-only, Q6 boundary-only, wrong support-12 split,
                     split without oriented root
   decision        = continue_only_as_support_or_normalization

7. exactp_upstream
   class           = heavy_upstream
   closer          = compact C,D,K,orientation theorem, equal-weight 75 atoms,
                     theta2 payload, or reverse theorem
   first_falsifier = normalized-y vocabulary, finite packet without source,
                     branchless orientation, or unified-only theorem
   decision        = continue_only_on_exact_theorem_hook
```

## Counts

```text
evidence_markers_ok = 10/10
route_rows = 7
first_pass_source_closers = 2
first_pass_normalizers = 3
support_routes = 1
heavy_upstream_routes = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_route_priority_falsifier_matrix_rows=1/1
```

## Verdict

The current first-class run should prioritize theorem effort in this order:

```text
1. scalar-fixed divisor/additive theorem for one legal row
2. support-period-156 value theorem for one legal row or H0/Y507 bridge
3. exact power, quartic, row-labeled, or reciprocal presentations only if they
   uniquely normalize to the same row; accepted exact powers are
   e in {3,5,13,39,75,169,507}
4. Q only as support/normalization or extraction payload
5. exact-P only as the heavy upstream route with an exact theorem hook
```

This keeps the moonshot alive while preventing drift. A future pass continues
only if it either supplies one of the closers above, normalizes uniquely to one
legal row, or gives the listed first falsifier. Broad source vocabulary,
selector-only data, boundary-only data, finite payloads without arithmetic
source theorem, and exact-P vocabulary without an accepted hook should be
classified immediately as repair or reject.
