# P25 v2 Matched Zero-Lattice Target Audit

Updated: 2026-06-17

Marker: `p25_v2_matched_zero_lattice_target_audit_rows=1/1`

## Purpose

Name the exact boundary-zero values required by the matched-affine route.

After the matched-quotient burden audit, the remaining support debt is not a
generic zero-lattice theorem. The currently accepted matched-affine packets
need three specific targets, spanning rank `2` in the zero lattice up to sign:

```text
R1/R2
R2/R1
q2_1*q4_1*q8_1
```

Exact scalar-fixed finite values for those targets are not in hand.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_zero_lattice_candidate_sweep_20260617.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_matched_quotient_burden_audit_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_matched_zero_lattice_target_audit_gate.py
```

The gate returned `p25_v2_matched_zero_lattice_target_audit_rows=1/1`.

## Target Rows

```text
unit_sum_inverse_q2_1
  aggregate_vector = (2,-1,0,0)
  coefficient_sum = 1
  matched_zero_vector = (1,-1,0,0)
  zero_coordinates = (-1,0,0)
  source_target = exact inverse of q2_1, equivalently R1/R2
  missing = quotient relation or zero boundary without scalar-fixed finite value

unit_power_q2_1
  aggregate_vector = (2,1,0,0)
  coefficient_sum = 3
  matched_zero_vector = (-1,1,0,0)
  zero_coordinates = (1,0,0)
  source_target = exact q2_1, equivalently R2/R1
  missing = quotient relation or zero boundary without scalar-fixed finite value

full_zero_basis_product
  aggregate_vector = (2,1,1,1)
  coefficient_sum = 5
  matched_zero_vector = (-3,1,1,1)
  zero_coordinates = (1,1,1)
  source_target = exact q2_1*q4_1*q8_1
  missing = individual quotient vocabulary without exact product value theorem
```

## Counts

```text
evidence_markers_ok = 5/5
matched_zero_targets = 3
zero_coordinate_rank = 2
unique_zero_lines_up_to_sign = 2
scalar_fixed_zero_values_in_hand = 0
matched_zero_source_theorems_in_hand = 0
current_matched_source_packets = 0
current_source_stage_closers = 0
p25_v2_matched_zero_lattice_target_audit_rows=1/1
```

## Verdict

This narrows the matched-affine support route:

```text
do not ask for generic zero-lattice quotient data
ask for exact scalar-fixed finite values for R1/R2 or R2/R1,
or the exact product q2_1*q4_1*q8_1,
paired with the aggregate theorem
```

These targets are still support data, not first anchors. A zero-boundary
divisor relation, quotient vocabulary, or unspecialized row-comparison theorem
does not change source-stage status unless paired with the aggregate theorem
and the invertible coefficient-sum normalization.
