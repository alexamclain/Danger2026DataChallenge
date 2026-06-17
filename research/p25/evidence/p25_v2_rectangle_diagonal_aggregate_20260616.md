# P25 v2 Rectangle Diagonal Aggregate

Updated: 2026-06-16

## Purpose

Record the diagonal relation among the four legal H0/conductor-39 rectangle
rows. This pass checks whether products of legal rows create a broader theorem
target that could replace the one-row source ask.

They do not. The diagonal products are equal and give the broad quadratic
aggregate with boundary `2W`, not the sparse `W` target. The all-four product
is the square of that aggregate with boundary `4W`.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_rectangle_diagonal_aggregate_gate.py
```

The gate returned `p25_v2_rectangle_diagonal_aggregate_rows=1/1`.

## Aggregate Relations

```text
diagonal_m1_m4:
  multipliers = (1, 4)
  support = 24
  coefficients = (-6, 6)
  boundary = 2W
  sha256 = 2e64d7efabb4c09621db06fa5ab6930f9d42456da7a4d9fd5bfbae0b9477555c

diagonal_m2_m8:
  multipliers = (2, 8)
  support = 24
  coefficients = (-6, 6)
  boundary = 2W
  sha256 = 2e64d7efabb4c09621db06fa5ab6930f9d42456da7a4d9fd5bfbae0b9477555c

all_four_rows:
  multipliers = (1, 2, 4, 8)
  support = 24
  coefficients = (-12, 12)
  boundary = 4W
  sha256 = 6c04165f721f33bd09a95dc97feea73f4c1e069c8a6f233a2c678e474a7bc976
```

Thus:

```text
m1 * m4 = m2 * m8 = broad quadratic aggregate
m1 * m2 * m4 * m8 = (broad quadratic aggregate)^2
```

## Routing Decisions

```text
single_legal_row
  decision = source_stage_candidate_if_theorem_present
  missing  = finite value/divisor theorem plus downstream framing

diagonal_pair_m1_m4
  decision = repair_broad_quadratic_aggregate_boundary_2w
  missing  = selector/factorization to one sparse edge with W boundary

diagonal_pair_m2_m8
  decision = repair_broad_quadratic_aggregate_boundary_2w
  missing  = selector/factorization to one sparse edge with W boundary

diagonal_identity_m1m4_equals_m2m8
  decision = relation_not_source_close
  missing  = arithmetic theorem for one sparse edge, not just the shared
             diagonal aggregate

all_four_rows_product
  decision = repair_overdemand_square_of_broad_quadratic
  missing  = one legal support-156 row with W boundary is enough and still
             missing
```

## Meaning

A source theorem for the broad quadratic aggregate would be relevant context,
but it would not close the first-pass target by itself. It has the wrong
boundary scale: `2W` rather than `W`. It still needs a selector or factorization
to one sparse rectangle edge with the original `Norm_156(Y_507)` boundary.

This also explains why asking for all four rows over-demands the source stage:
the all-four product is just the square of the broad aggregate and has boundary
`4W`.

## Counts

```text
source_candidate_shapes = 1
repair_rows = 3
relation_rows = 1
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = m1*m4 = m2*m8 broad quadratic aggregate relation
continue_first_pass = yes
intake_rule = broad quadratic aggregate, diagonal pair, or all-four product
              is repair/context unless it also selects/factors to one sparse
              W-boundary rectangle edge
discard_condition = source answer that only proves the 2W or 4W aggregate and
                    presents it as a one-row W-boundary theorem
```
