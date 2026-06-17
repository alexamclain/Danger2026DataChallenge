# P25 v2 Q/Yang Row Bridge Packet

Updated: 2026-06-17

Marker: `p25_v2_q_yang_row_bridge_packet_rows=1/1`

## Purpose

Make the conductor-39 `Q`/Yang support route packet-shaped. The compact
`Q` object is useful because it has the right Hilbert-90 boundary after
powering, and its diagonal/split structure can reach a row square. It is not a
source-stage theorem unless selector debt, oriented root/edge data, and finite
theorem data are all paid.

This page is a classifier for future Q/Yang expert answers and source
snippets. It is not a new Q theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_yang_lookup_row_status_20260617.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_q_route_candidate_sweep_20260617.md`
- `evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_yang_row_bridge_packet_gate.py
```

The gate returned `p25_v2_q_yang_row_bridge_packet_rows=1/1`.

## Arithmetic And Algebra Checks

```text
p mod 39 = 23
ord_39(p) = 6
square-root kernel in F_p^* = 2
Q diagonal algebra ok = yes
```

The Q diagonal/split algebra is:

```text
(m1+m4) + (m1-m4) = 2*m1
(m1+m4) - (m1-m4) = 2*m4
(m2+m8) + (m2-m8) = 2*m2
(m2+m8) - (m2-m8) = 2*m8
```

Thus diagonal plus matching split reaches `2*edge`, not one edge. The
oriented square root/sign remains a real clause.

## Accepted Packet Shapes

```text
mixed_yang_h90_direct_finite_theorem
  decision = source_stage_candidate
  required = mixed source theorem, level-507 Yang lift, H90 descent,
             selector paid, and scalar-fixed finite theorem for one legal row

q_or_q3_with_selector_normalization
  decision = normalize_to_current_kernel
  required = Q or Q^3 finite theorem plus selector/boundary-zero normalization
             to one oriented edge

q_diagonal_split_with_oriented_root
  decision = normalize_to_current_kernel
  required = Q diagonal, matching pure quartic split, and oriented root/sign
             or explicit oriented diagonal-split normalization

q_square_value_with_extraction_map
  decision = extraction_payload_candidate
  required = exact scalar-fixed Q-square value plus map from the two row roots
             to same-j/X_1(16)/halving data or concrete A,x0 candidates
```

The first three are source-stage row-normalization shapes. The Q-square row is
an extraction payload shape: useful, but not itself a source-stage theorem and
not a direct `vpp.py` candidate.

## Repair And Reject Rows

```text
q_or_q3_without_selector
  decision = repair_selector_debt_missing
  falsifier = Q theorem data has not selected one oriented edge

q6_boundary_only
  decision = repair_value_or_additive_normalization_missing
  falsifier = Hilbert-90 boundary alone has no scalar-fixed finite payload

q_diagonal_without_split
  decision = support_diagonal_selector_missing
  falsifier = Q diagonal aggregate needs pure quartic split or direct one-edge theorem

q_diagonal_split_without_oriented_root
  decision = repair_oriented_square_root_missing
  falsifier = diagonal plus split reaches 2*edge, not one scalar-fixed edge

q_square_without_extraction_map
  decision = repair_extraction_map_missing_after_two_roots
  falsifier = two row-value roots are not vpp.py candidates

local_q_source_language
  decision = repair_exact_q_theorem_missing
  falsifier = local corpus has helper vocabulary but no conductor-39 Q hook

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels
  falsifier = Frobenius alternation makes the pure-character degree-6 norm zero

direct_vpp_on_row_value
  decision = reject_vpp_requires_A_x0_not_row_value
  falsifier = vpp.py verifies (p,A,x0), not modular-unit row values
```

## Counts

```text
evidence_markers_ok = 10/10
packet_rows = 12
source_stage_shapes = 3
extraction_payload_shapes = 1
repair_or_support_rows = 6
reject_rows = 2
current_q_source_hooks = 0
current_source_stage_closers = 0
current_extraction_ready = 0
current_submission_ready = 0
p25_v2_q_yang_row_bridge_packet_rows=1/1
```

## Verdict

The Q/Yang route remains live as a support and normalization route, not as
broad Q vocabulary. Promotion requires one of:

```text
mixed Yang/H90 finite theorem for one legal row;
Q or Q^3 theorem plus selector normalization to one oriented edge;
Q diagonal plus correct quartic split plus oriented root/sign;
Q-square value plus explicit extraction map.
```

Everything weaker stays support, repair, or reject.
