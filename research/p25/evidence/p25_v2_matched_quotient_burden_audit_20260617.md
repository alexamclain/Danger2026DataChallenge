# P25 v2 Matched-Quotient Burden Audit

Updated: 2026-06-17

Marker: `p25_v2_matched_quotient_burden_audit_rows=1/1`

## Purpose

Clarify what the matched-quotient aggregate route actually buys.

The route is algebraically valid:

```text
exact R^v + exact R^(v - (sum v)e_m) -> R_m^(sum v)
gcd(sum v,p-1)=1 -> R_m
```

But it is an intake normalizer, not a cheaper source theorem. Each accepted
packet still requires two exact arithmetic source theorems: one for the
aggregate and one for the matched zero-lattice quotient.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_matched_quotient_source_feasibility_20260617.md`
- `evidence/p25_v2_affine_row_normal_form_20260617.md`
- `evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_matched_quotient_burden_audit_gate.py
```

The gate returned `p25_v2_matched_quotient_burden_audit_rows=1/1`.

## Burden Rows

```text
unit_sum_affine_packet
  vector = (2,-1,0,0)
  matched_quotient = (1,-1,0,0)
  coefficient_sum = 1
  decision = accepted_intake_if_both_source_theorems_exist
  source_burden = equivalent_to_direct_row_plus_q2_1_inverse
  missing = no source theorem for both R1^2/R2 and R1/R2

unit_power_affine_packet
  vector = (2,1,0,0)
  matched_quotient = (-1,1,0,0)
  coefficient_sum = 3
  inverse_exponent mod p-1 = 6666666666666666666666675
  recovered_row_vector_mod_pminus1 = (1,0,0,0)
  decision = accepted_intake_if_both_source_theorems_exist
  source_burden = equivalent_to_direct_row_cubed_plus_q2_1
  missing = no source theorem for both R1^2*R2 and R2/R1

full_zero_basis_matched_packet
  vector = (2,1,1,1)
  matched_quotient = (-3,1,1,1)
  coefficient_sum = 5
  inverse_exponent mod p-1 = 4000000000000000000000005
  recovered_row_vector_mod_pminus1 = (1,0,0,0)
  decision = accepted_intake_if_both_source_theorems_exist
  source_burden = equivalent_to_direct_row_fifth_power_plus_full_zero_basis
  missing = no source theorem for aggregate plus q2_1*q4_1*q8_1

standard_pair_with_matched_quotient
  vector = (1,1,0,0)
  matched_quotient = (-1,1,0,0)
  coefficient_sum = 2
  gcd_sum_pminus1 = 2
  decision = repair_root_debt_remaining
  falsifier = recovers R1^2, so selected square root is still missing

all_four_norm_with_matched_quotient
  vector = (1,1,1,1)
  matched_quotient = (-3,1,1,1)
  coefficient_sum = 4
  gcd_sum_pminus1 = 4
  decision = repair_fourth_root_debt_remaining
  falsifier = recovers R1^4, so selected fourth root is still missing
```

## Counts

```text
evidence_markers_ok = 5/5
burden_rows = 5
accepted_intake_rows = 3
root_debt_rows = 2
row_equivalent_burdens = 3
independent_matched_source_packets_in_hand = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_matched_quotient_burden_audit_rows=1/1
```

## Verdict

Matched quotient remains a real route for future source/expert answers, but it
should not be searched as a loose distribution or aggregate shortcut.

Accept it only when a source supplies:

```text
1. exact arithmetic theorem for R^v
2. exact arithmetic theorem for R^(v - (sum v)e_m)
3. gcd(sum v,p-1)=1
```

Otherwise the answer is repair. In particular, the common standard
distribution shapes with coefficient sum `2` or `4` still recover only
`R_m^2` or `R_m^4`, leaving selected-root debt.
