# P25 v2 Priority-1 Divisor/Additive Work Order

Updated: 2026-06-17

Marker: `p25_v2_priority1_divisor_additive_work_order_rows=1/1`

## Purpose

Isolate the top theorem target from the route-priority matrix: a scalar-fixed
finite divisor/additive theorem for one normalized legal support-156 row. This
page exists so future expert/source passes do not drift back into source
legality, boundary-only identities, value-up-to-scalar payloads, or Koo-Shin
constant-product repairs.

This is not a source theorem. It is the priority-1 work order and first
falsifier screen.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `evidence/p25_v2_route_priority_falsifier_matrix_20260617.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_additive_normalizer_source_scan_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md`
- `evidence/p25_v2_h0_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_priority1_divisor_additive_work_order_gate.py
```

The gate returned `p25_v2_priority1_divisor_additive_work_order_rows=1/1`.

## Work Rows

```text
one_normalized_row_divisor_additive
  decision        = priority1_source_stage_candidate_if_present
  requirement     = one legal support-156 row, Norm_156(Y_507) boundary,
                    finite scalar-fixing additive/divisor identity
  first_falsifier = source legality, boundary-only, divisor class only, or
                    unspecified F_p^* scalar

h0_h0_translate_additive_identity
  decision        = normalize_h0_product_then_priority1_intake
  requirement     = one exact legal H0/H0-translate product with H90 boundary
                    and scalar-fixed additive data
  first_falsifier = H0 source certificate, formal product, or period language
                    without finite scalar-fixing identity

conductor39_yang_additive_identity
  decision        = normalize_yang_h90_product_then_priority1_intake
  requirement     = mixed U_chi/W source, Yang lift, H90 descent, and
                    scalar-fixed finite additive theorem
  first_falsifier = prime projection, one-axis legality, Q support data, or
                    Yang lift without finite theorem

row_labeled_or_reciprocal_additive_theorem
  decision        = normalize_row_label_or_reciprocal_then_priority1_intake
  requirement     = row label or reciprocal-minus-boundary convention plus
                    scalar-fixed theorem for at least one legal row
  first_falsifier = unordered orbit, symmetric aggregate, reciprocal plus
                    boundary, or missing row label

koo_shin_2010_source_legality
  decision        = repair_finite_additive_theorem_missing
  requirement     = Theorem 6.2 legality plus a new finite scalar-fixed theorem
                    not currently in the extract
  first_falsifier = Theorem 6.2, Lemma 6.1, or Theorem 5.2 repeated as
                    source/context only

theorem52_constant_product_repair
  decision        = reject_constant_span_repair
  requirement     = nonzero constant-exponent product in legal quotient-C4 span
  first_falsifier = legal quotient-C4 span meets constant line only at zero

divisor_h90_without_additive_normalizer
  decision        = repair_scalar_normalization_missing
  requirement     = basepoint, finite additive value, telescoping product,
                    branch/root, or specified scalar
  first_falsifier = principal divisor, H90 boundary, or value up to F_p^*
                    scalar only

finite_payload_without_arithmetic_source
  decision        = repair_arithmetic_source_theorem_missing
  requirement     = challenge-legal arithmetic source theorem producing the
                    finite identity
  first_falsifier = local row value, packet, fixture, or numeric target without
                    source theorem
```

## Counts

```text
evidence_markers_ok = 10/10
work_rows = 8
source_stage_candidate_rows = 1
normalization_rows = 3
repair_rows = 3
reject_rows = 1
current_priority1_source_theorems = 0
current_submission_ready = 0
p25_v2_priority1_divisor_additive_work_order_rows=1/1
```

## Verdict

The priority-1 ask is now:

```text
Find or falsify a challenge-legal arithmetic theorem producing a finite
scalar-fixed divisor/additive identity for one normalized legal support-156
H0/conductor-39 row with Norm_156(Y_507) boundary.
```

Koo-Shin 2010 remains the closest source-language anchor, but the existing
paper scan does not contain the missing scalar-fixing theorem. Theorem 6.2
gives legality, Lemma 6.1 gives distribution context, Theorem 5.2 gives
root-descent/constant-product context, and the constant-span repair is killed
for the legal quotient-`C4` rows. Future priority-1 work should therefore ask
for a new finite additive/divisor theorem or a sharp reason such a theorem
cannot exist in this source language.
