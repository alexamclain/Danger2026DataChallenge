# P25 v2 Source-Stage Normalization Spine

Updated: 2026-06-17

Marker: `p25_v2_source_stage_normalization_spine_rows=1/1`

## Purpose

Turn the accepted H0/conductor-39 theorem presentations into one normalization
spine. The repair-debt matrix says which shapes are uniquely recoverable; this
page says how each accepted presentation reduces to the same source-stage
object: one scalar-fixed legal support-156 row, then DANGER3 framing and
extraction.

This is not a source theorem. It is the intake normal form for future theorem
answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_frontdoor_count_sync_20260616.md`
- `evidence/p25_v2_repair_debt_closure_matrix_20260617.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_row_orientation_candidate_sweep_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_source_stage_normalization_spine_gate.py
```

The gate returned `p25_v2_source_stage_normalization_spine_rows=1/1`.

## P25 Normalizers

```text
inverse exponents modulo p - 1:
R_m^3  -> R_m by exponent 6666666666666666666666675
R_m^5  -> R_m by exponent 4000000000000000000000005
R_m^13 -> R_m by exponent 7692307692307692307692317
R_m^39 -> R_m by exponent 5897435897435897435897443
R_m^75 -> R_m by exponent 266666666666666666666667
R_m^169 -> R_m by exponent 5207100591715976331360953
R_m^507 -> R_m by exponent 5069033530571992110453655

support-period branch:
gcd(4^156 - 1, p - 1) = 1

ambient-period branch:
gcd(4^780 - 1, p - 1) = 11
```

## Spine Rows

```text
direct_one_edge
  presentation  = scalar-fixed divisor/additive or period-156 value theorem
                  for one oriented R_m
  normalization = identity
  route         = source-stage candidate if theorem present

quartic_selector_wrapper
  presentation  = exact row-antisymmetric C4_1 phase with mixed row sign and
                  finite theorem
  normalization = selects one oriented quotient-C4 edge, then direct one-edge
                  intake
  route         = selector-normalized first-pass theorem

row_labeled_orbit
  presentation  = row-labeled four-row or parametric doubling-orbit theorem
  normalization = choose any labeled legal m in {1,2,4,8}, then direct
                  one-edge intake
  route         = labeled-row-normalized first-pass theorem

reciprocal_minus_boundary
  presentation  = reciprocal row theorem with explicit -Norm_156(Y_507)
                  boundary
  normalization = rewrite reciprocal presentation to the corresponding
                  oriented legal row
  route         = reciprocal-normalized first-pass theorem

bijective_power_value
  presentation  = exact finite value theorem for R_m^e,
                  e in {3,5,13,39,75,169,507}
  normalization = raise to inverse exponent modulo p - 1, then direct
                  one-edge intake
  route         = unique-power-normalized first-pass theorem

support_period156_value
  presentation  = support-period-156 value theorem for canonical H0/Y507 or
                  one legal row
  normalization = unique support-period branch in F_p^*, then direct one-edge
                  intake
  route         = period-156-normalized first-pass theorem

exactp_upstream
  presentation  = exact 75-atom or accepted theta2/theta2-inverse theorem with
                  bridge
  normalization = heavy upstream bridge into unified target, then ordinary
                  extraction ladder
  route         = heavy source-stage candidate, not first-pass default
```

## Counts

```text
evidence_markers_ok = 10/10
first_pass_normalization_routes = 6
selector_wrapper_routes = 1
unique_root_routes = 2
heavy_upstream_routes = 1
repair_debt_rows = 6
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_source_stage_normalization_spine_rows=1/1
```

## Verdict

All accepted first-pass H0/conductor-39 presentations now reduce to a single
intake normal form:

```text
one scalar-fixed legal support-156 row
arithmetic source theorem
Norm_156(Y_507) boundary or accepted period-156 bridge
finite value/divisor/additive normalization
```

The spine prevents two opposite mistakes. It keeps uniquely normalizable
answers alive even when they are not phrased as a literal row value, and it
keeps projector, ambient-period, pair/square, zero-lattice, up-to-scalar, and
source-less finite payload answers from being promoted before their repair debt
is paid.
