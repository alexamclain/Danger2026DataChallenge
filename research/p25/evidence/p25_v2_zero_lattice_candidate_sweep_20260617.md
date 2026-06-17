# P25 v2 Zero-Lattice Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_zero_lattice_candidate_sweep_rows=1/1`

## Purpose

Audit prior boundary-zero, diagonal, row-square, and Q-normalization artifacts
after the edge-lattice target became rigid. The question is whether any older
artifact already normalizes to a source-stage theorem for one legal
`W = Norm_156(Y_507)` row. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quotient_complexity_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_zero_lattice_candidate_sweep_gate.py
```

The gate returned `p25_v2_zero_lattice_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
unit_edge
  prior_shape = one coefficient is 1 and the other three are 0
  decision    = only_source_stage_shape_if_finite_theorem_present
  missing     = no current artifact supplies the scalar-fixed finite theorem

zero_lattice_basis_or_pair_quotients
  prior_shape = rank-3 boundary-zero quotient lattice among legal rows
  decision    = support_transfer_data_not_source_close
  missing     = zero Hilbert-90 boundary cannot create the first W-boundary row
                value

nonunit_w_boundary_vector
  prior_shape = coefficient sum 1 but not a unit edge
  decision    = repair_edge_plus_boundary_zero_lattice
  missing     = finite value for boundary-zero content or direct unit-edge
                theorem missing

diagonal_pair_or_broad_quadratic
  prior_shape = m1*m4=m2*m8 diagonal aggregate with 2W boundary
  decision    = repair_broad_quadratic_aggregate_boundary_2w
  missing     = selector/factorization down to one sparse W-boundary edge

row_quotient_square_bridge
  prior_shape = diagonal aggregate plus matching quotient reaches 2*edge
  decision    = repair_row_square_bridge_halving_missing
  missing     = halving/root/orientation data selecting one legal row

row_square_or_doubled_boundary
  prior_shape = exact value/divisor theorem for a row square or doubled 2W
                boundary
  decision    = repair_row_square_root_sign_missing
  falsifier   = constant sign has zero divisor and zero H90 boundary

two_edge_pair_data
  prior_shape = row/column/diagonal pair aggregate or pair difference
  decision    = repair_sign_or_root_or_edge_selector_missing
  missing     = pair data reaches at best 2*edge before oriented root selection

q_diagonal_value
  prior_shape = Q projection equals m1+m4=m2+m8
  decision    = support_diagonal_aggregate_selector_missing
  missing     = boundary-zero split/orientation data or direct one-edge theorem

q_diagonal_plus_split_without_root
  prior_shape = Q diagonal plus m1-m4 or m2-m8 split reaches 2*edge
  decision    = repair_oriented_square_root_missing
  missing     = oriented root/sign data missing after the split

q_square_exact_value
  prior_shape = future exact scalar-fixed value for the Q square row
  decision    = bounded_two_root_payload_not_source_close
  missing     = row-value roots still need DANGER3 extraction map

wrong_q_split_shortcut
  prior_shape = support-12 quotient or one-axis split used as Q normalizer
  decision    = reject_wrong_split_for_q_diagonal
  falsifier   = Q normalizer must be m1-m4 or m2-m8, both support 24 and all
                columns
```

## Counts

```text
evidence_markers_ok = 12/12
newly_promoted_prior_candidates = 0
surviving_normalization_families = 3
q_square_payload_bounded = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_zero_lattice_candidate_sweep_rows=1/1
```

The three surviving normalization families are useful only after a real finite
theorem or exact finite zero-lattice value appears:

```text
nonunit W-boundary theorem + exact boundary-zero values -> one unit edge
diagonal aggregate + correct split + oriented root -> one unit edge
exact Q-square value -> two row-value roots, extraction map still missing
```

## Verdict

```text
positive_artifact = zero-lattice and row-square prior-art sweep
continue_first_pass = yes
new_candidate_from_prior_art = no
surviving_zero_lattice_ask = direct unit-edge theorem, or a normalization
                             theorem with exact boundary-zero values and
                             oriented root/sign data
discard_condition = answer only supplies quotient relations, zero-boundary
                    divisor data, nonunit W-boundary vector, diagonal
                    aggregate, row square, Q diagonal, Q split without root,
                    support-12 split shortcut, or row-value roots with no
                    extraction map
```

This closes the other tempting "maybe already enough" family: boundary-zero
data is real transfer data, and Q-square data can bound a row-value payload,
but neither supplies the first absolute one-edge theorem.
