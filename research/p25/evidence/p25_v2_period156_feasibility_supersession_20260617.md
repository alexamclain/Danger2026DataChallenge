# P25 v2 Period-156 Feasibility Supersession

Updated: 2026-06-17

Marker: `p25_v2_period156_feasibility_supersession_rows=1/1`

## Purpose

Record that the proposed period-156 value feasibility screen is already covered
by the row-bridge packet and source-hook evidence. This is a verdict page, not
a new theorem lane.

The aim is to prevent a drift loop where the same missing period-156 source
theorem is repeatedly repackaged as a new feasibility artifact.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_period156_row_bridge_packet_20260617.md`
- `evidence/p25_v2_period156_lookup_row_status_20260617.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_period156_value_candidate_sweep_20260617.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_period156_feasibility_supersession_gate.py
```

The gate returned `p25_v2_period156_feasibility_supersession_rows=1/1`.

## Covered Rows

```text
canonical_h0_period156_value
  status = covered_by_row_bridge_accept_shape
  missing = exact arithmetic source theorem not in hand

y507_value_with_legal_row_bridge
  status = covered_by_row_bridge_accept_shape
  missing = exact arithmetic source theorem not in hand

theta2_payload_with_period156_bridge
  status = covered_by_row_bridge_accept_shape
  missing = exact arithmetic theta2 payload with bridge not in hand

ambient780_or_mu11_value
  status = covered_by_row_bridge_repair_shape
  falsifier = ambient-period-780 route leaves 11 F_p branches

degree6_value_without_fp_row_descent
  status = covered_by_row_bridge_repair_shape
  falsifier = degree-6 value lacks F_p descent and selected legal row

norm_boundary_or_payload_without_source
  status = covered_by_row_bridge_repair_shape
  falsifier = missing finite selected value, additive theorem, or arithmetic source
```

## Arithmetic Checks

```text
p mod 39 = 23
ord_39(p) = 6
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

## Counts

```text
evidence_markers_ok = 6/6
covered_accept_shapes = 3
covered_repair_shapes = 3
current_period156_value_packets = 0
current_source_stage_closers = 0
duplicate_feasibility_gate_needed = 0
continue_only_on_exact_source_theorem = 1
p25_v2_period156_feasibility_supersession_rows=1/1
```

## Verdict

Do not create another broad period-156 feasibility layer unless a source snippet
or expert answer adds new data outside the row-bridge packet.

The current positive path remains narrow:

```text
exact arithmetic source theorem
+ finite H0/Y507 value or theta2 payload
+ period-156 branch/additive normalization
+ legal support-156 row bridge
+ Norm_156(Y_507) boundary
```

Ambient-period-780 values, `mu_11` quotients, degree-6 values without `F_p` row
descent, norm-only claims, and source-less finite payloads are already classified
as repair or reject rows.
