# P25 v2 Row Orientation / Reciprocal Normalizer

Updated: 2026-06-16

## Purpose

Refine row normalization for source snippets that present the support-156
product with the opposite orientation. The existing row-orbit normalizer says
which unit multipliers preserve the four oriented legal rows. This pass checks
the complementary fact: every unit outside the doubling subgroup gives the
reciprocal of a legal row, not an unrelated product.

This does not change the accepted first-pass theorem target. It prevents us
from either rejecting a reciprocal theorem too harshly or accepting an
orientationless outside-unit row too generously.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_row_orientation_reciprocal_normalizer_gate.py
```

The gate returned `p25_v2_row_orientation_reciprocal_normalizer_rows=1/1`.

## Unit Split

```text
oriented_units =
  (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)

reciprocal_units =
  (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)

unclassified_unit_count = 0
```

The oriented units are exactly the doubling subgroup already recorded in the
row-orbit normalizer. The reciprocal units are the complementary coset. For
example:

```text
unit 7  -> reciprocal of normalized m=8
unit 38 -> reciprocal of normalized m=4
```

## Routing Decisions

```text
oriented_legal_row_m1
  decision = source_stage_candidate_if_theorem_present
  missing  = finite value/divisor theorem plus downstream framing

stabilizer_oriented_m16
  decision = normalize_to_m1_then_apply_source_snippet_intake
  missing  = same as normalized oriented m=1 row

outside_unit_m7_orientation_unspecified
  decision = repair_reciprocal_orientation_or_boundary_sign_missing
  missing  = explicit reciprocal orientation and -Norm_156 boundary, or rewrite
             as the oriented legal row

reciprocal_m8_with_minus_boundary
  decision = normalize_reciprocal_to_m8_then_apply_source_snippet_intake
  missing  = same theorem data after reciprocal/orientation normalization

reciprocal_row_with_plus_boundary
  decision = reject_orientation_boundary_mismatch
  missing  = reciprocal product should carry the opposite Hilbert-90 boundary
             sign

orientationless_product_hash
  decision = repair_product_orientation_missing
  missing  = oriented product row or reciprocal row with boundary sign
```

## Meaning

The reciprocal product is mathematically adjacent to the live target, but it
has the opposite Hilbert-90 boundary sign. A theorem stated for a reciprocal
row can be normalized into the current source-snippet intake only if the source
also gives the reciprocal orientation or the `-Norm_156(Y_507)` boundary
convention. If a snippet presents an outside-doubling multiplier without
orientation, it is a repair row. If it presents the reciprocal product with the
positive boundary, it is a reject row.

## Counts

```text
oriented_unit_count = 12
reciprocal_unit_count = 12
source_candidate_shapes = 3
repair_rows = 2
reject_rows = 1
current_source_stage_closers = 0
```

## Verdict

```text
continue_first_pass = yes
positive_artifact = full unit action now splits into oriented legal rows and
                    reciprocal legal rows
intake_rule = outside-doubling units are not accepted as oriented rows; require
              explicit reciprocal orientation and boundary sign, or rewrite to
              one normalized legal row
discard_condition = reciprocal row asserted with the positive Norm_156
                    boundary, or orientationless row used as a source close
```
