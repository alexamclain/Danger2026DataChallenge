# P25 v2 Row-Sign x C4 Tensor Spectrum

Updated: 2026-06-16

## Purpose

Combine the mixed signed-column fingerprint with the quotient-`C4` character
spectrum. The legal conductor-39 source row is not just a `C4` edge and not
just a mod-3 row sign: it is a row-antisymmetric tensor times one selected
quotient-`C4` edge.

This is not the missing finite value/divisor theorem. It is a finite
source-language screen for projection-only, row-symmetric, row-sign-only,
quadratic-only, and selector-without-value answers.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_c4_character_spectrum_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_row_sign_c4_tensor_spectrum_gate.py
```

The gate returned `p25_v2_row_sign_c4_tensor_spectrum_rows=1/1`.

## Tensor Coordinates

Use quotient-`C4` coset order:

```text
0 = H
1 = 2H
2 = 4H
3 = 7H
```

For each legal row, `row1` is the mod-3 row with signs as listed in the
mod-13 rectangle page, and `row2 = -row1`.

## Legal Tensor Rows

```text
m=1  7H -> 4H
  row1 = (0,0,-1,1)
  row2 = (0,0,1,-1)
  row_symmetric = (0,0,0,0)
  row_antisymmetric DFT = (0, 2+2i, -4, 2-2i)

m=2  7H -> H
  row1 = (-1,0,0,1)
  row2 = (1,0,0,-1)
  row_symmetric = (0,0,0,0)
  row_antisymmetric DFT = (0, -2+2i, -4, -2-2i)

m=4  2H -> H
  row1 = (-1,1,0,0)
  row2 = (1,-1,0,0)
  row_symmetric = (0,0,0,0)
  row_antisymmetric DFT = (0, -2-2i, -4, -2+2i)

m=8  2H -> 4H
  row1 = (0,1,-1,0)
  row2 = (0,-1,1,0)
  row_symmetric = (0,0,0,0)
  row_antisymmetric DFT = (0, 2-2i, -4, 2+2i)
```

All four rows have:

```text
mod-3 pushforward = 0
mod-13 pushforward = 0
row-symmetric component = 0
row-antisymmetric C4 quadratic component = -4
row-antisymmetric C4 order-4 components = nonzero
```

The order-4 phases distinguish the four legal edges.

## Routing Rule

```text
row_sign_c4_edge_theorem
  decision = source-stage candidate if scalar-fixed theorem present
  requirement = row-antisymmetric C4 edge with order-4 phase

mod13_projection_only
  decision = reject_zero_pushforward_loses_mixed_tensor
  falsifier = legal rows have zero mod-13 pushforward

mod3_projection_only
  decision = reject_zero_pushforward_loses_edge
  falsifier = legal rows have zero mod-3 pushforward

row_symmetric_c4_statement
  decision = reject_row_symmetric_wrong_tensor
  falsifier = legal rows are purely row-antisymmetric

row_sign_only_no_c4_phase
  decision = repair_c4_edge_phase_missing
  missing = order-4 C4 phase selecting one legal edge

c4_edge_without_row_sign
  decision = repair_or_reject_mixed_row_sign_missing
  missing = row-antisymmetric mixed tensor structure

row_sign_quadratic_only
  decision = repair_broad_quadratic_aggregate_boundary_2w
  missing = order-4 C4 phase selecting one legal edge

tensor_selector_without_value_theorem
  decision = repair_value_divisor_theorem_missing
  missing = scalar-fixed finite value/divisor theorem
```

## Counts

```text
evidence_markers_ok = 6/6
legal_rows_ok = 4/4
rows_with_zero_symmetric_part = 4
rows_with_zero_proper_pushforwards = 4
rows_with_order4_c4_phases = 4
accepted_routes = 1
repair_rows = 4
reject_rows = 3
current_source_theorems = 0
current_submission_ready = 0
p25_v2_row_sign_c4_tensor_spectrum_rows=1/1
```

## Verdict

A conductor-39 source theorem must preserve both pieces of the mixed tensor:
the row-antisymmetric mod-3 sign and the order-4 quotient-`C4` edge phase.
Projection-only, row-symmetric, row-sign-only, or quadratic-only theorems are
not first-pass source closers. Even the correct tensor selector remains only a
selector until it comes with the scalar-fixed finite value/divisor theorem.
