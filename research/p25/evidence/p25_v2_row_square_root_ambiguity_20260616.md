# P25 v2 Row Square Root Ambiguity

Updated: 2026-06-16

## Purpose

Record the first falsifier for promoting a row-square theorem to the one-row
source-stage theorem. The row quotient invariant bridge shows that a diagonal
aggregate plus a matching quotient recovers `2*row` in the exponent lattice.
This pass records why that is still not enough.

A row-square value has two roots, `R` and `-R`. The sign is a constant, so it
has zero divisor and zero Hilbert-90 boundary. Therefore square data, even with
the doubled `2W` boundary, does not select the oriented row.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_row_square_root_ambiguity_gate.py
```

The gate returned `p25_v2_row_square_root_ambiguity_rows=1/1`.

## Arithmetic Invariants

```text
p mod 4 = 1
p is odd = yes

two roots for a nonzero square: R and -R
constant sign divisor: zero
constant sign Hilbert-90 boundary: zero
same square after sign flip: (-R)^2 = R^2
same boundary after sign flip: boundary(-R) = boundary(R)
```

The important point is not the existence of a square root algorithm. It is that
the theorem shape does not name which root is the oriented legal row.

## Routing Decisions

```text
one_row_value_or_divisor_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

row_square_value_theorem
  decision = repair_row_square_root_sign_missing
  missing  = explicit root/sign/orientation data selecting R rather than -R,
             or direct one-row theorem

aggregate_plus_quotient_square_bridge
  decision = repair_row_square_bridge_halving_missing
  missing  = halving/root/orientation data selecting the legal row, or direct
             one-row theorem

row_square_with_h90_boundary_2w
  decision = repair_boundary_scale_and_root_sign_missing
  missing  = one-row W-boundary theorem plus explicit root/sign/orientation

row_square_with_explicit_oriented_root
  decision = normalize_root_then_apply_source_snippet_intake
  missing  = same theorem data after oriented-root normalization
```

## Meaning

This closes a subtle escape hatch in the row quotient bridge. Proving the
square of the desired row, or proving the broad diagonal aggregate plus the
matching quotient, gives useful structure but not the source-stage close. It
must be paired with explicit root/sign/orientation data, or replaced by a
direct theorem for one normalized legal row.

## Counts

```text
source_candidate_shapes = 2
repair_rows = 3
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = sign/root ambiguity for row-square theorem shapes is now
                    explicit
continue_first_pass = yes
intake_rule = square, doubled-boundary, or aggregate-plus-quotient claims are
              repair rows unless they include an explicit oriented root or a
              direct one-row theorem
discard_condition = row-square theorem presented as a one-row W-boundary
                    source close
```
