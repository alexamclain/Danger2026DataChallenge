# P25 v2 Power / Projector Extraction Boundary

Updated: 2026-06-16

## Purpose

Consolidate the boundary between useful powered/projector finite values and
DANGER3 extraction. Exact values for powers of one legal row can be useful, but
when the power map has a nontrivial kernel they produce bounded modular-unit
row roots, not concrete `(A,x0)` candidates.

This extends the Q-square extraction-boundary rule to projector and power-value
answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_power_projector_extraction_boundary_gate.py
```

The gate returned:

```text
p25_v2_power_projector_extraction_boundary_rows=1/1
```

## Boundary Rows

```text
exact_R3_value
  kernel = 1
  row_value_payload = 1
  decision = normalize_unique_power_value_then_source_intake
  missing = source-snippet intake, then DANGER3 framing and extraction

exact_R39_value
  kernel = 1
  row_value_payload = 1
  decision = normalize_unique_power_value_then_source_intake
  missing = source-snippet intake, then DANGER3 framing and extraction

exact_R2_value_no_sign
  kernel = 2
  row_value_payload = 2
  decision = repair_power_root_selector_missing_after_bounded_row_payload
  missing = orientation/branch/scalar plus extraction map

exact_R4_projector_value_no_branch
  kernel = 4
  row_value_payload = 4
  decision = repair_power_root_selector_missing_after_bounded_row_payload
  missing = orientation/branch/scalar plus extraction map

exact_R11_value_no_branch
  kernel = 11
  row_value_payload = 11
  decision = repair_power_root_selector_missing_after_bounded_row_payload
  missing = orientation/branch/scalar plus extraction map

exact_R156_value_no_branch
  kernel = 4
  row_value_payload = 4
  decision = repair_power_root_selector_missing_after_bounded_row_payload
  missing = orientation/branch/scalar plus extraction map

exact_R4_projector_value_with_selected_root
  kernel = 4
  row_value_payload = 1
  decision = normalize_selected_power_value_then_source_intake
  missing = source-snippet intake, then DANGER3 framing and extraction

projector_components_divisor_only
  row_value_payload = 0
  decision = repair_exact_finite_value_or_additive_normalization_missing
  missing = divisor/H90/projector data alone does not fix a finite row value

direct_vpp_on_power_row_root
  decision = reject_vpp_requires_A_x0_not_row_value
  falsifier = vpp.py verifies (p,A,x0), not a modular-unit row value
```

## Counts

```text
evidence_markers_ok = 5/5
unique_root_rows = 2
bounded_row_value_payload_rows = 4
selected_root_normalize_rows = 1
repair_rows = 5
reject_rows = 1
extraction_ready_rows = 0
submission_ready_rows = 0
current_extraction_ready_rows = 0
current_submission_ready_rows = 0
```

## Verdict

```text
decision = keep_power_projector_values_as_source_intake_or_repair_payloads
current_source_theorem = no
current_extraction_ready = no
current_submission = no
```

Exact unique-power values, or ambiguous-power values with a selected root,
route back through source-snippet intake. Exact ambiguous-power values without
root selection are useful only as bounded row-value payloads. They still need
orientation/branch/scalar data and then the normal DANGER3 extraction ladder:
same-j bridge, practical `X_1(16)` payload, halving/direct `x0`, and official
`vpp.py`.
