# P25 v2 Matched-Quotient Source Feasibility

Updated: 2026-06-17

Marker: `p25_v2_matched_quotient_source_feasibility_rows=1/1`

## Purpose

Separate two similar-looking aggregate routes after the matched-quotient
normalization was promoted:

```text
standard distribution aggregate + quotient
  -> usually recovers R_m^2 or R_m^4, so root debt remains

nonstandard affine aggregate + exact matched quotient
  -> can recover R_m^s with gcd(s,p-1)=1, so it normalizes to one row
```

This is not a source theorem. It is a feasibility screen for source/expert
answers that arrive as aggregate products rather than as one legal row.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`
- `evidence/p25_v2_distribution_relation_closure_screen_20260617.md`
- `evidence/p25_v2_external_distribution_relation_scout_20260617.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md`
- `evidence/p25_v2_affine_row_normal_form_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_matched_quotient_source_feasibility_gate.py
```

The gate returned `p25_v2_matched_quotient_source_feasibility_rows=1/1`.

## Source Shapes

Use row coordinates `(m1,m2,m4,m8)`, target `m1`, and

```text
matched quotient = v - (sum v)e_m.
```

```text
direct_edge_baseline
  vector = (1,0,0,0)
  coefficient_sum = 1
  decision = direct_current_kernel_if_source_theorem_present
  status = no such theorem currently in hand

unit_sum_affine_packet
  vector = (2,-1,0,0)
  matched_quotient = (1,-1,0,0)
  coefficient_sum = 1
  decision = viable_matched_quotient_packet_if_source_supplies_both
  missing = no known source emits both the affine aggregate and matched quotient

unit_power_affine_packet
  vector = (2,1,0,0)
  matched_quotient = (-1,1,0,0)
  coefficient_sum = 3
  decision = viable_matched_quotient_packet_if_source_supplies_both
  missing = no known source emits both the affine aggregate and matched quotient

standard_vertex_pair_with_quotient
  vector = (1,1,0,0)
  matched_quotient = (-1,1,0,0)
  coefficient_sum = 2
  decision = repair_even_sum_root_debt
  falsifier = recovers R_m^2, so oriented square root is still missing

standard_diagonal_pair_with_quotient
  vector = (1,0,1,0)
  matched_quotient = (-1,0,1,0)
  coefficient_sum = 2
  decision = repair_even_sum_root_debt
  falsifier = recovers R_m^2, so oriented square root is still missing

all_four_norm_with_zero_basis
  vector = (1,1,1,1)
  matched_quotient = (-3,1,1,1)
  coefficient_sum = 4
  decision = repair_fourth_root_debt
  falsifier = recovers R_m^4, so selected fourth root is still missing

aggregate_only_distribution
  vector = (1,1,0,0)
  decision = repair_matched_zero_lattice_value_missing
  falsifier = aggregate theorem alone leaves zero-lattice debt unpaid

quotient_only_zero_lattice
  vector = (-1,1,0,0)
  coefficient_sum = 0
  decision = transfer_only_not_first_anchor
  falsifier = zero-sum data cannot create the first absolute row value

koo_shin_constant_span
  decision = reject_constant_span_not_current_target
  falsifier = legal quotient-C4 span has no nonzero constant vector

external_distribution_cluster
  decision = support_framework_not_finite_matched_packet
  missing = p25 row label, matched quotient theorem, scalar-fixed finite
            payload, and boundary bridge
```

## Counts

```text
evidence_markers_ok = 8/8
source_shapes = 10
viable_matched_packet_shapes = 2
root_debt_standard_aggregate_rows = 3
missing_quotient_rows = 1
transfer_only_rows = 1
reject_rows = 1
support_rows = 1
current_viable_source_packets_in_hand = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_matched_quotient_source_feasibility_rows=1/1
```

## Verdict

The matched-quotient route is real, but it is stricter than generic
distribution language.

Standard distribution aggregates such as pair sums and all-four norms do not
become source-stage closers merely because a quotient is known: their
coefficient sums are `2` or `4`, so they leave square-root or fourth-root debt.

The actual closing aggregate shape is narrower:

```text
arithmetic theorem for R^v
+ arithmetic theorem for exact R^(v - (sum v)e_m)
+ gcd(sum v,p-1)=1
```

No current Koo-Shin, Kubert-Lang, Sprang, or external distribution source
emits that paired finite packet. Future aggregate answers should therefore be
asked for the exact matched quotient and checked for invertible coefficient
sum before changing H0 or conductor-39 status.
