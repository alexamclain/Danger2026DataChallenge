# P25 v2 Repair-Debt Closure Matrix

Updated: 2026-06-17

Marker: `p25_v2_repair_debt_closure_matrix_rows=1/1`

## Purpose

Consolidate the p25-specific root, branch, selector, scalar, and source-theorem
debts around the first-pass H0/conductor-39 target. The goal is to distinguish
the theorem shapes that normalize uniquely from the ones that only look close
but still carry a finite ambiguity or an absolute-value gap.

This is not a source theorem. It is the repair ledger for near-hit theorem
answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_row_orientation_candidate_sweep_20260617.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_value_payload_reality_ledger_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_repair_debt_closure_matrix_gate.py
```

The gate returned `p25_v2_repair_debt_closure_matrix_rows=1/1`.

## P25 Arithmetic

```text
p = 10000000000000000000000013
p mod 8 = 5

power-map kernels on F_p^*:
e=2   -> 2
e=3   -> 1
e=4   -> 4
e=5   -> 1
e=6   -> 2
e=11  -> 11
e=13  -> 1
e=22  -> 22
e=39  -> 1
e=44  -> 44
e=75  -> 1
e=156 -> 4
e=169 -> 1
e=507 -> 1
e=780 -> 4

period branch gcds:
gcd(4^39  - 1, p - 1) = 1
gcd(4^78  - 1, p - 1) = 1
gcd(4^156 - 1, p - 1) = 1
gcd(4^312 - 1, p - 1) = 1
gcd(4^507 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

## Matrix

```text
direct_one_edge_theorem
  shape  = one exact oriented row with scalar-fixed divisor/additive or
           period-156 value theorem
  debt   = none at source stage
  branch = 1
  route  = source-stage candidate if theorem present

row_labeled_orbit_theorem
  shape  = row-labeled four-row or parametric doubling-orbit theorem
           containing a legal row
  debt   = choose labeled legal row, then normal source intake
  branch = 1
  route  = normalize to one labeled row

reciprocal_minus_boundary
  shape  = reciprocal row with explicit -Norm_156(Y_507) boundary
  debt   = reciprocal orientation normalization only
  branch = 1
  route  = normalize reciprocal then intake

bijective_power_value
  shape  = exact finite value theorem for R_m^e,
           e in {3,5,13,39,75,169,507}
  debt   = unique F_p^* root
  branch = 1
  route  = normalize unique root then intake

support_period156_value
  shape  = period-156 value theorem for one legal row
  debt   = unique support-period branch
  branch = 1
  route  = source-stage candidate if theorem present

ambient_period780_value
  shape  = ambient period-780 value, 11th power, or mu_11 quotient
  debt   = mu_11 branch ambiguity
  branch = 11
  route  = repair period-156 branch context missing

projector_or_four_edge_components
  shape  = projector/character components reconstructing 4*edge
  debt   = mu_4 fourth-root/scalar ambiguity
  branch = 4
  route  = repair selected fourth root missing

pair_diagonal_or_row_square
  shape  = two-edge pair, diagonal aggregate plus quotient, or row-square value
  debt   = sign/oriented-square-root ambiguity
  branch = 2
  route  = repair oriented square root missing

q_square_exact_value
  shape  = exact scalar-fixed finite value for the Q square / 2*edge payload
  debt   = two row-value roots plus extraction-map debt
  branch = 2
  route  = bounded payload, not source close without oriented root or extraction

zero_lattice_values_only
  shape  = exact row quotients or boundary-zero lattice basis values
  debt   = absolute W-boundary row theorem missing
  branch = n/a
  route  = support transfer data, not first source close

divisor_h90_up_to_scalar
  shape  = right divisor/H90 boundary but value only up to unspecified F_p^*
  debt   = full scalar normalization debt
  branch = p - 1
  route  = repair additive or value normalization missing

finite_payload_without_source
  shape  = local finite row value, fixture, packet, or hash with no arithmetic
           source theorem
  debt   = source theorem and DANGER3 framing missing
  branch = n/a
  route  = repair arithmetic source theorem missing
```

## Counts

```text
evidence_markers_ok = 13/13
unique_normalization_rows = 5
bounded_branch_repair_rows = 4
scalar_debt_rows = 1
support_only_rows = 2
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_repair_debt_closure_matrix_rows=1/1
```

## Verdict

There are real "near" rows, but only five normalize uniquely at source intake:
direct one-edge theorem, row-labeled orbit theorem, reciprocal-minus-boundary
row, exact bijective power value, and support-period-156 value theorem. None is
currently in hand.

The other close-looking rows have concrete debt: `mu_11` for ambient-period
values, `mu_4` for projector/fourth-power data, two roots for pair/square/Q
square data, full `F_p^*` scalar debt for divisor/H90 up-to-scalar statements,
or no absolute `W`-boundary row theorem for zero-lattice transfer data.

This makes the moonshot status sharper: we are structurally close in the sense
that the legal row, selector, boundary, orbit, and root-normalization contracts
are pinned. We are not yet source-stage close, because the missing object is
still an arithmetic theorem that supplies one of the unique-normalization rows
with scalar-fixed finite value/divisor data.
