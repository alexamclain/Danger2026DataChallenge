# P25 v2 Row Quotient Invariant Bridge

Updated: 2026-06-16

## Purpose

Record the boundary-zero quotient structure among the four legal
H0/conductor-39 rectangle rows. This is the complementary factorization check
after the rectangle diagonal aggregate pass.

It finds real structure: quotients of legal rows have zero Hilbert-90 boundary,
and a diagonal aggregate plus the matching row quotient recovers twice one
legal row. It still does not close source stage by itself, because it produces
a row-square/halving problem unless a source also supplies the missing
root/orientation data or directly proves the one-row theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_row_quotient_invariant_bridge_gate.py
```

The gate returned `p25_v2_row_quotient_invariant_bridge_rows=1/1`.

## Quotient Profiles

All six nontrivial quotients of legal rows are Frobenius-invariant and have
zero Hilbert-90 boundary:

```text
q1_2: support=12 coeffs=(-6, 6) boundary=0
q1_4: support=24 coeffs=(-6, 6) boundary=0
q1_8: support=12 coeffs=(-6, 6) boundary=0
q2_4: support=12 coeffs=(-6, 6) boundary=0
q2_8: support=24 coeffs=(-6, 6) boundary=0
q4_8: support=12 coeffs=(-6, 6) boundary=0
```

The diagonal quotients are the ones that factor the broad quadratic aggregate:

```text
q1_4 sha256 = 4a0c74d6b96955fab83c24c85987db2ef05fd7ea604cdfa92dc071b9d739c53b
q2_8 sha256 = b88f15cd9c76107f06d238c49f4537174b2fc9c10905afec423040db5e0977ff
```

## Factorization Identities

In additive exponent notation:

```text
(m1 + m4) + (m1 - m4) = 2*m1
(m1 + m4) - (m1 - m4) = 2*m4

(m2 + m8) + (m2 - m8) = 2*m2
(m2 + m8) - (m2 - m8) = 2*m8
```

At value level, this means that a broad diagonal aggregate theorem plus the
matching quotient theorem can at best recover a square of one legal row unless
the source also supplies a halving/root/orientation theorem.

## Routing Decisions

```text
one_legal_row_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = finite value/divisor theorem plus downstream framing

row_quotient_only
  decision = repair_boundary_zero_quotient_only
  missing  = one-row value/divisor theorem; quotient has zero H90 boundary

diagonal_aggregate_plus_quotient
  decision = repair_row_square_bridge_halving_missing
  missing  = halving/root/orientation data selecting the legal row, or direct
             one-row theorem
```

## Meaning

This is a useful bridge for evaluating expert answers. If someone proves only
a row quotient, they have proved a boundary-zero relation between legal rows,
not the row value/divisor theorem itself. If someone proves both the broad
quadratic aggregate and the matching quotient, the result reaches `2*row` in
the exponent lattice, or a row square at value level. That is still a repair
row unless the answer includes the missing halving/root/orientation data.

## Counts

```text
nontrivial_quotients = 6
boundary_zero_quotients = 6
row_square_bridges = 4
source_candidate_shapes = 1
repair_rows = 2
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = legal row quotients are boundary-zero Frobenius invariants
continue_first_pass = yes
intake_rule = quotient-only or aggregate-plus-quotient answers are repair rows
              unless they include halving/root/orientation data selecting one
              sparse W-boundary row
discard_condition = quotient relation or row-square bridge presented as a
                    one-row source-stage close
```
