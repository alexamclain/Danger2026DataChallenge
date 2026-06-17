# P25 v2 Front-Door Count Sync

Updated: 2026-06-17

## Purpose

Explain why the current handoff pages use three different front-door counts
without changing the mathematical frontier. The difference is presentation:
the positive clause matcher splits route variants, the expert rubric groups
direct source-closing rows while routing exact unique powers through
normalize-then-intake, and the minimal expert ask phrases the same first-pass
work as three yes/no mathematical questions plus the heavier exact-P route, Q
support/normalization variants, and a Q-square extraction-map repair row.

## Pages Read

- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_frontdoor_count_sync_gate.py
```

The gate returned `p25_v2_frontdoor_count_sync_rows=1/1`.

## Count Reconciliation

```text
positive_matcher_frontdoor_presentations = 5
  canonical_h0_divisor_additive_identity
  quartic_character_finite_theorem
  canonical_h0_period156_value_identity
  Y_507_period156_value_identity
  power_normalized_row_value_theorem

expert_rubric_frontdoor_families = 3
  normalized_divisor_additive_theorem
  normalized_period156_value_theorem
  quartic_selector_finite_theorem
  note: exact_unique_power_value is normalize-then-intake in the rubric,
        not a direct source-closing row family

minimal_ask_first_pass_questions = 3
  scalar-fixed finite divisor/additive identity
  support-period-156 finite value theorem
  exact finite power-value theorem with inverse-exponent recovery

minimal_ask_accepted_routes = 7
  scalar-fixed divisor/additive theorem
  period-156 value theorem with branch context
  exact-P upstream theorem with bridge
  norm-one Q value theorem with period-156 context
  finite Q^3 Hilbert-90 preimage theorem
  Q plus explicit oriented diagonal split
  power-normalized row-value theorem

exactp_heavy_routes = 1
```

## Meaning

The counts are compatible:

- the positive matcher splits the period-156 value route into canonical H0 and
  `Y_507` presentations;
- the expert rubric groups those into one period-156 value family and keeps
  the quartic selector as a separate character-language family;
- the minimal expert ask phrases quartic data as a required selector clause
  when the answer is stated in character language, and adds the power-value
  theorem as a third mathematical question because
  `3`, `5`, `13`, `39`, `75`, `169`, and `507` are invertible modulo `p-1`;
- the minimal expert ask also lists Q/Q3/Q-split routes as support or
  normalization variants, and exact Q-square value as a row-value payload with
  extraction-map repair, not as new source-stage front doors;
- exact-P remains a heavier upstream route, not the first-pass default.

## Counts

```text
evidence_markers_ok = 7/7
current_source_theorems = 0
current_submission_ready = 0
p25_v2_frontdoor_count_sync_rows=1/1
```

## Verdict

```text
positive_artifact = front-door count compatibility audit
continue_first_pass = yes
intake_rule = do not treat 5-vs-3-vs-3 as a new theorem discrepancy; classify
              the actual clauses through the positive matcher or expert rubric
discard_condition = a future page changes one count without preserving the
                    scalar/divisor, period-value, quartic-selector,
                    power-normalized, and exact-P route alignment
```
