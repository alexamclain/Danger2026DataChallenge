# P25 v2 Row Orbit Normalization

Updated: 2026-06-16

## Purpose

Promote the exact normalizer for the four legal support-156 H0/conductor-39
product rows.  The rows are one doubling orbit modulo the stabilizer
`(1,16,22)`, so future source snippets should be normalized before intake.

This page does not prove the missing arithmetic theorem.  It says which row
presentations are the same target, which presentations are outside the current
target, and why one normalized legal row is enough for the first-pass source
ask.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_row_orbit_normalization_gate.py
```

The gate returned `p25_v2_row_orbit_normalization_rows=1/1`.

## Orbit Data

```text
unit_count_mod39 = 24
doubling_subgroup = (1,2,4,5,8,10,11,16,20,22,25,32)
doubling_subgroup_size = 12
stabilizer = (1,16,22)
legal_representatives = (1,2,4,8)
legal_unit_actions = 12
outside_doubling_units = (7,14,17,19,23,28,29,31,34,35,37,38)
outside_units_matching_legal_rows = 0
```

The four legal rows are the four cosets of the stabilizer inside the doubling
subgroup:

```text
m=1 units=(1,16,22)
  P=(7,17,23,34,37,38)
  N=(4,8,10,11,20,25)
  sha256=eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e

m=2 units=(2,5,32)
  P=(7,14,29,34,35,37)
  N=(1,8,11,16,20,22)
  sha256=97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9

m=4 units=(4,10,25)
  P=(14,19,28,29,31,35)
  N=(1,2,5,16,22,32)
  sha256=28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6

m=8 units=(8,11,20)
  P=(17,19,23,28,31,38)
  N=(2,4,5,10,25,32)
  sha256=ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

For every unit in a coset, multiplying the canonical `m=1` residues by that
unit gives the same normalized representative row.  No unit outside the
doubling subgroup gives one of the four legal rows.

## Intake Decisions

```text
exact_legal_row_m1
  decision = source_stage_candidate_if_theorem_present
  normalized = m=1

stabilizer_equivalent_m16
  decision = normalize_to_m1_then_apply_source_snippet_intake
  normalized = m=1

doubling_coset_m32
  decision = normalize_to_m2_then_apply_source_snippet_intake
  normalized = m=2

outside_doubling_unit_m7
  decision = reject_not_current_legal_four_row_target
  missing  = one of the four normalized support-156 rows, or a new theorem target

all_four_rows_required
  decision = repair_overdemand_one_legal_row_is_enough_for_source_stage
  missing  = only one normalized legal row is required by the first-pass ask

one_row_without_boundary
  decision = repair_boundary_or_theorem_missing
  missing  = Norm_156(Y_507) boundary and finite value/divisor theorem
```

## Counts

```text
orbit_classes_ok = 4/4
source_stage_candidate_shapes = 3
repair_rows = 2
reject_rows = 1
current_source_stage_closers = 0
```

## Verdict

Normalize row presentations before applying the source-snippet intake:

```text
unit in (1,16,22)  -> m=1
unit in (2,5,32)   -> m=2
unit in (4,10,25)  -> m=4
unit in (8,11,20)  -> m=8
unit outside <2>   -> not the current legal four-row target
```

One normalized legal row with the finite value/divisor theorem and
`Norm_156(Y_507)` boundary is sufficient for the first-pass source ask.  Do not
over-demand all four rows; conversely, do not accept an outside-doubling-orbit
multiplier as a presentation of the current target without a new theorem.
