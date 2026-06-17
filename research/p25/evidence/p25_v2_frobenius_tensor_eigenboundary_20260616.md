# P25 v2 Frobenius Tensor Eigenboundary

Updated: 2026-06-16

## Purpose

Explain, at the row-sign x quotient-`C4` tensor level, why Hilbert-90 boundary
data cannot by itself select one legal conductor-39 edge.

The previous tensor screen showed that each legal row has nonzero order-4
`C4` phase data. This screen decomposes those phases under Frobenius and then
applies the boundary map `(1 - Frob_p)`.

This is not the missing finite value/divisor theorem. It is a sharper
falsifier for boundary-only, norm-only, or quadratic-only source claims.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_c4_character_spectrum_20260616.md`
- `evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_frobenius_tensor_eigenboundary_gate.py
```

The gate returned `p25_v2_frobenius_tensor_eigenboundary_rows=1/1`.

## Eigencomponent Rule

Use quotient-`C4` character index `j = 0,1,2,3`.

Frobenius acts on the tensor row by:

```text
mod-3 row flip eigenvalue = -1
C4 shift-by-two eigenvalue on character j = (-1)^j
tensor eigenvalue = -(-1)^j
```

So:

```text
j=0: Frob eigenvalue = -1, boundary multiplier 1-Frob = 2
j=1: Frob eigenvalue = +1, boundary multiplier 1-Frob = 0
j=2: Frob eigenvalue = -1, boundary multiplier 1-Frob = 2
j=3: Frob eigenvalue = +1, boundary multiplier 1-Frob = 0
```

The constant component `j=0` is already zero for legal rows. The order-4
selector phases `j=1,3` are killed by `(1 - Frob_p)`. The quadratic component
`j=2` is doubled and is the only nonzero boundary-visible part.

## Legal Tensor Rows

In row-antisymmetric normalized coordinates:

```text
m=1  7H -> 4H
  anti DFT = (0, 2+2i, -4, 2-2i)
  boundary DFT = (0, 0, -8, 0)

m=2  7H -> H
  anti DFT = (0, -2+2i, -4, -2-2i)
  boundary DFT = (0, 0, -8, 0)

m=4  2H -> H
  anti DFT = (0, -2-2i, -4, -2+2i)
  boundary DFT = (0, 0, -8, 0)

m=8  2H -> 4H
  anti DFT = (0, 2-2i, -4, 2+2i)
  boundary DFT = (0, 0, -8, 0)
```

All four legal rows have distinct order-4 selector phases before applying
`1-Frob`, and the same boundary spectrum afterward.

## Routing Rule

```text
full_tensor_edge_value_theorem
  decision = source-stage candidate if scalar-fixed theorem present
  requirement = row-antisymmetric C4 edge + order-4 selector phase + finite theorem

boundary_only_or_norm156_only
  decision = repair_frobenius_boundary_collapses_edge_phase
  missing = source selector data before applying 1-Frob

quadratic_boundary_component_only
  decision = repair_boundary_visible_but_selector_missing
  missing = order-4 phase selecting one legal edge

order4_selector_components_without_value
  decision = repair_value_divisor_theorem_missing
  missing = scalar-fixed finite value/divisor theorem

frob_invariant_selector_ignored
  decision = repair_selector_erased_by_boundary_map
  missing = theorem for the selector before Hilbert-90 projection

same_parity_zero_boundary
  decision = reject_wrong_boundary_or_wrong_tensor
  falsifier = boundary is zero or tensor row sign is wrong
```

## Counts

```text
evidence_markers_ok = 5/5
legal_rows_ok = 4/4
rows_with_order4_components_killed = 4
rows_with_quadratic_boundary_visible = 4
common_boundary_rows = 4
accepted_routes = 1
repair_rows = 4
reject_rows = 1
current_source_theorems = 0
current_submission_ready = 0
p25_v2_frobenius_tensor_eigenboundary_rows=1/1
```

## Verdict

The Hilbert-90 boundary is downstream of the selector. It sees the common
quadratic component and erases the order-4 components that distinguish the four
legal conductor-39 edges. Therefore a boundary-only theorem, a norm-only
theorem, or a quadratic-character theorem can be useful supporting structure,
but it is not a first-pass closer unless it also supplies the edge-selecting
order-4 source data and a scalar-fixed finite value/divisor theorem.
