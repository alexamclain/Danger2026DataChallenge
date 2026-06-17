# P25 v2 Row-Value Reconstruction Basis

Updated: 2026-06-17

Marker: `p25_v2_row_value_reconstruction_basis_rows=1/1`

## Purpose

Make the finite reconstruction problem explicit for the four legal
H0/conductor-39 rows. The zero-lattice and row-square artifacts show many real
support structures; this page records exactly what data would turn that
support into row values, and why it still does not create the first absolute
row theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_row_value_reconstruction_basis_gate.py
```

The gate returned `p25_v2_row_value_reconstruction_basis_rows=1/1`.

## Reconstruction Rows

Use edge coordinates `(m1, m2, m4, m8)`.

```text
one_absolute_row_anchor
  input_data = exact scalar-fixed finite theorem for one legal row R_m
  algebra = one basis vector e_m has coefficient sum 1
  decision = source_stage_candidate_if_theorem_present
  missing = DANGER3 framing, same-j extraction, and official vpp.py

one_row_plus_three_quotients
  input_data = R_1 plus q2_1, q4_1, q8_1 boundary-zero values
  algebra = e2=e1+q2_1, e4=e1+q4_1, e8=e1+q8_1
  decision = reconstruct_all_rows_after_absolute_anchor
  missing = absolute row value still required before quotients can transfer

three_quotients_only
  input_data = q2_1, q4_1, q8_1 boundary-zero values
  algebra = rank-3 zero-lattice fixes ratios but has coefficient sum 0
  decision = support_transfer_data_not_first_absolute_row
  missing = common F_p^* scalar / one W-boundary row value

diagonal_plus_matching_quotient
  input_data = d14=m1+m4 plus q14=m1-m4, or d28 plus q28
  algebra = d14+q14=2*m1 and d14-q14=2*m4; denominator 2 is unavoidable
  decision = repair_row_square_oriented_root_missing
  missing = oriented square root/sign or direct one-row theorem

nonunit_w_boundary_plus_zero_lattice
  input_data = nonunit coefficient-sum-one theorem plus exact boundary-zero
               correction
  algebra = v=e_m+z, so e_m=v-z only if z has an exact finite value
  decision = normalize_to_one_row_only_with_exact_zero_lattice_values
  missing = finite value for boundary-zero content or direct unit-edge theorem

q_square_payload
  input_data = exact scalar-fixed finite value for the Q-square row
  algebra = bounded two-root row-value payload, not a direct vpp.py candidate
  decision = bounded_payload_needs_oriented_root_and_extraction_map
  missing = oriented root/sign plus same-j/X_1(16)/halving or direct A,x0 map
```

## Counts

```text
evidence_markers_ok = 6/6
zero_lattice_rank = 3
one_anchor_plus_zero_lattice_rank = 4
reconstruction_rows = 6
source_stage_candidate_shapes = 1
quotient_only_absolute_anchors = 0
diagonal_plus_split_denominator = 2
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_row_value_reconstruction_basis_rows=1/1
```

## Verdict

The finite reconstruction basis is now explicit:

```text
one scalar-fixed legal row value
+ boundary-zero quotient basis
= all four legal row values
```

But the quotient basis alone has coefficient sum zero and determines only
ratios. Diagonal-plus-split data reaches `2*row`, so it is a row-square route
with the existing oriented-root/sign debt. Nonunit `W`-boundary data can be
normalized only if exact boundary-zero finite values are also supplied.

So the missing anchor remains exactly one absolute scalar-fixed legal row
theorem, or an equivalent theorem that includes the oriented root/sign and
finite normalization data needed to reduce to that row.
