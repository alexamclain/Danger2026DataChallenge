# P25 v2 Affine Row-Product Classifier

Updated: 2026-06-17

Marker: `p25_v2_affine_row_product_classifier_rows=1/1`

## Purpose

Classify expert/source answers that are neither a single legal row nor a
row-labeled power, but an affine product of the four legal rows
`(m1,m2,m4,m8)`.

This narrows one remaining ambiguity in the current Drew packet: an aggregate
row product can sometimes normalize to a current-kernel row, but only if it
also carries the exact matched boundary-zero quotient value needed to remove
the aggregate part. Coefficient-sum tests alone are not enough.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_affine_row_product_classifier_gate.py
```

The gate returned `p25_v2_affine_row_product_classifier_rows=1/1`.

## Rule

Let a finite theorem produce an exact value for

```text
R^v = R_1^a R_2^b R_4^c R_8^d
v = (a,b,c,d)
s = a+b+c+d
```

Then:

```text
s = 0:
  boundary-zero quotient data only; transfer after a row anchor, never the
  first absolute row value.

gcd(s, p-1) > 1:
  even with quotient values, R_m^s retains root/scalar ambiguity.

gcd(s, p-1) = 1 and v is a row power:
  current-kernel row-labeled unique-power intake.

gcd(s, p-1) = 1 and v is not a row power:
  normalize to the current kernel only if the exact matched zero-lattice
  quotient value for v - s*e_m is also supplied.
```

## Rows

Use coordinates `(m1,m2,m4,m8)`.

```text
direct_unit_row
  vector = (1,0,0,0)
  coefficient_sum = 1
  decision = current_kernel_front_door

row_labeled_unit_power
  vector = (75,0,0,0)
  coefficient_sum = 75
  decision = inverse_power_then_current_kernel

unit_sum_nonedge_without_quotients
  vector = (2,-1,0,0)
  coefficient_sum = 1
  decision = repair_zero_lattice_value_missing
  reason = v - e1 = -q2_1; exact q2_1 value is required

unit_sum_nonedge_with_matched_zero_lattice_value
  vector = (2,-1,0,0)
  coefficient_sum = 1
  decision = normalize_to_current_kernel_if_matched_quotient_present
  reason = v - e1 = -q2_1; exact matched quotient value recovers R_1

unit_power_nonedge_with_matched_zero_lattice_value
  vector = (2,1,0,0)
  coefficient_sum = 3
  decision = normalize_to_current_kernel_if_matched_quotient_present
  reason = v - 3*e1 = q2_1, so exact q2_1 value recovers R_1^3, then inverse
           exponent 3 recovers R_1

zero_lattice_quotient
  vector = (-1,1,0,0)
  coefficient_sum = 0
  decision = transfer_only_never_first_anchor

nonunit_pair_sum
  vector = (1,1,0,0)
  coefficient_sum = 2
  decision = root_debt_repair

all_four_product
  vector = (1,1,1,1)
  coefficient_sum = 4
  decision = root_and_selector_repair
```

## Counts

```text
evidence_markers_ok = 6/6
affine_rows = 8
direct_current_kernel_rows = 2
conditional_zero_lattice_normalizers = 2
repair_rows = 3
transfer_only_rows = 1
current_matched_zero_lattice_packets = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_affine_row_product_classifier_rows=1/1
```

## Verdict

An affine aggregate theorem is not automatically a new fourth source-stage
front door. It either:

```text
already is a row or row-labeled unique power;
normalizes to a current-kernel row only with the exact matched zero-lattice
quotient value; or
remains repair/transfer because of zero-sum, nonunit-root, or selector debt.
```

This keeps the Drew packet complete without broadening the moonshot: aggregate
answers are useful only when they reduce back to one scalar-fixed legal row and
then survive the existing DANGER3 extraction ladder.
