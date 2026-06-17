# P25 v2 Matched-Quotient Closure Packet

Updated: 2026-06-17

Marker: `p25_v2_matched_quotient_closure_packet_rows=1/1`

## Purpose

Promote the algebraic repair package for affine products of the four legal
rows. This is the first row-aggregate route that can genuinely close back to
the current theorem kernel, but only when the source supplies both:

```text
1. an exact arithmetic theorem for an aggregate value R^v, and
2. an exact arithmetic theorem for the matched zero-lattice quotient R^z.
```

The rule is not another source scan. It is a normalization theorem for future
expert/source answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md`
- `evidence/p25_v2_affine_row_product_classifier_20260617.md`
- `evidence/p25_v2_affine_row_normal_form_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_matched_quotient_closure_packet_gate.py
```

The gate returned `p25_v2_matched_quotient_closure_packet_rows=1/1`.

## Closure Rule

Use row coordinates `(m1,m2,m4,m8)`. If a source gives

```text
R^v = R_1^a R_2^b R_4^c R_8^d
v = (a,b,c,d)
s = a+b+c+d
```

and we target row `R_m`, define the matched zero-lattice debt

```text
z = v - s*e_m.
```

Then `sum(z)=0`, so `z` is in the zero lattice, and the exact identity is

```text
R^v / R^z = R_m^s.
```

Therefore:

```text
gcd(s,p-1)=1 and exact R^v plus exact matched R^z
  -> recover R_m by inverse exponent
  -> route through the current theorem kernel

s=0
  -> transfer-only quotient data; not a first anchor

gcd(s,p-1)>1
  -> even matched quotient data leaves root/scalar debt
```

## Packet Rows

```text
unit_sum_matched_packet
  vector = (2,-1,0,0)
  target = m1
  matched_quotient = (1,-1,0,0)
  coefficient_sum = 1
  decision = normalize_to_current_kernel

unit_power_matched_packet
  vector = (2,1,0,0)
  target = m1
  matched_quotient = (-1,1,0,0)
  coefficient_sum = 3
  decision = normalize_to_current_kernel_after_inverse_exponent

full_zero_basis_matched_packet
  vector = (2,1,1,1)
  target = m1
  matched_quotient = (-3,1,1,1)
  coefficient_sum = 5
  decision = normalize_to_current_kernel_after_inverse_exponent

aggregate_without_matched_quotient
  vector = (2,-1,0,0)
  decision = repair_zero_lattice_value_missing
  falsifier = aggregate value alone leaves boundary-zero content unpaid

wrong_quotient_packet
  vector = (2,-1,0,0)
  supplied_quotient = (-1,1,0,0)
  decision = repair_unmatched_zero_lattice_value
  falsifier = supplied quotient is not v - s*e_m

zero_lattice_only_packet
  vector = (-1,1,0,0)
  coefficient_sum = 0
  decision = transfer_only_not_first_anchor
  falsifier = coefficient sum zero cannot reveal common scalar

nonunit_pair_matched_packet
  vector = (1,1,0,0)
  coefficient_sum = 2
  decision = repair_root_debt_remaining
  falsifier = R_m^2 remains after matched quotient; gcd(2,p-1)=2
```

## Counts

```text
evidence_markers_ok = 8/8
exhaustive_small_normal_forms_ok = 1
packet_rows = 7
positive_matched_quotient_shapes = 3
repair_rows = 3
transfer_only_rows = 1
current_matched_quotient_source_packets = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_matched_quotient_closure_packet_rows=1/1
```

## Verdict

This is a real normalization route, but not a new source-stage closer in hand.
It upgrades future aggregate answers only if the source gives an exact matched
zero-lattice quotient theorem alongside the aggregate theorem.

In compact form:

```text
aggregate theorem + matched quotient theorem + invertible coefficient sum
  = current-kernel row theorem
```

Aggregate-only, quotient-only, unmatched quotient, and nonunit-sum packets
remain repair or transfer rows.
