# P25 v2 Period-156 Row Bridge Packet

Updated: 2026-06-17

Marker: `p25_v2_period156_row_bridge_packet_rows=1/1`

## Purpose

Make the period-156 value route packet-shaped. A value-side answer helps only
when it is not just a period value, norm, or class-field statement, but a
finite arithmetic theorem with enough bridge data to select one legal
support-156 row.

This page is a classifier for future source snippets and expert replies. It is
not a new value theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_period156_lookup_row_status_20260617.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_period156_value_candidate_sweep_20260617.md`
- `evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md`
- `evidence/p25_v2_norm_only_descent_ambiguity_20260616.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_period156_row_bridge_packet_gate.py
```

The gate returned `p25_v2_period156_row_bridge_packet_rows=1/1`.

## Arithmetic Checks

```text
p mod 39 = 23
ord_39(p) = 6
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
sqrt(-39) in F_p = no
```

So support-period-156 value roots are unique in `F_p^*`, while ambient-period
780 value claims keep an 11-branch ambiguity.

## Required Clauses

An accepted period-156 bridge packet must include all six clauses:

```text
finite F_p value or divisor/additive payload
arithmetic source theorem
support-period-156 branch/root/telescoping or additive normalization
legal support-156 row bridge
Norm_156(Y_507) boundary
scalar/branch/additive normalization over F_p
```

## Packet Rows

```text
canonical_h0_period156_value_packet
  decision = source_stage_value_candidate
  accepted = all six clauses present

y507_value_with_legal_row_bridge
  decision = source_stage_value_candidate
  accepted = Y_507 finite value plus period-156 context and legal-row bridge

theta2_payload_with_period156_bridge
  decision = theta2_or_exactp_bridge_candidate
  accepted = exact theta2/theta2-inverse payload plus period-156 bridge

y507_value_without_legal_row_bridge
  decision = repair_legal_row_bridge_missing
  falsifier = Y_507 value does not select one legal support-156 row

canonical_value_without_period156_context
  decision = repair_period156_branch_missing
  falsifier = value lacks support-period-156 branch/root/telescoping or additive normalization

ambient780_value_or_mu11_quotient
  decision = repair_ambient_mu11_branch
  falsifier = ambient-period-780 route leaves 11 F_p branches

degree6_value_without_fp_row_descent
  decision = repair_fp_descent_and_row_selection_missing
  falsifier = degree-6 value lacks F_p descent and selected legal row

norm_or_boundary_only
  decision = repair_finite_value_or_divisor_theorem_missing
  falsifier = Norm_156(Y_507) boundary does not choose a legal preimage row value

finite_payload_without_source
  decision = repair_arithmetic_source_theorem_missing
  falsifier = finite payload is a target, not a source theorem

direct_fp_order39_or_sqrt_minus39_shortcut
  decision = reject_arithmetic_shortcut
  falsifier = ord_39(p)=6 and sqrt(-39) is not in F_p
```

## Counts

```text
evidence_markers_ok = 8/8
packet_rows = 10
accepted_period156_bridge_shapes = 3
source_stage_value_shapes = 2
theta2_bridge_shapes = 1
repair_rows = 6
reject_rows = 1
current_period156_value_packets = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_period156_row_bridge_packet_rows=1/1
```

## Verdict

The value-side route is still live, but it has one packet boundary:

```text
finite value theorem
+ arithmetic source
+ period-156 branch/additive normalization
+ legal-row bridge
+ Norm_156(Y_507) boundary
  -> current-kernel source-stage candidate
```

Anything missing the row bridge, period branch/additive normalization, source
theorem, or finite selected value remains repair. Direct order-39-root or
`sqrt(-39)` shortcuts are arithmetically rejected for p25.
