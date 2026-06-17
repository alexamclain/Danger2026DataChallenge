# P25 v2 C4 Character Spectrum

Updated: 2026-06-16

## Purpose

Record the quotient-`C4` character spectrum of the legal H0/conductor-39
one-edge target. The mod-13 rectangle screen says a legal row is one odd
order-3 coset against one even order-3 coset. This page makes the Fourier
obstruction explicit: every legal edge has essential order-4 `C4` character
components. The quadratic character alone is the broad odd-minus-even
aggregate, not a selected edge.

This is not the missing finite value/divisor theorem. It is a source-language
falsifier for character-only, quadratic-only, and same-parity statements.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_c4_character_spectrum_gate.py
```

The gate returned `p25_v2_c4_character_spectrum_rows=1/1`.

## Setup

Order the quotient cosets by doubling:

```text
0 = H
1 = 2H
2 = 4H
3 = 7H
```

Represent a row by a length-4 vector with `+1` on the row-1 plus coset and
`-1` on the row-1 minus coset. Use the discrete Fourier transform with
characters `1, i, -1, -i`.

## Legal Edge Spectra

```text
m=1  7H -> 4H  vector=(0, 0, -1, 1)
  DFT = (0, 1+i, -2, 1-i)

m=2  7H -> H   vector=(-1, 0, 0, 1)
  DFT = (0, -1+i, -2, -1-i)

m=4  2H -> H   vector=(-1, 1, 0, 0)
  DFT = (0, -1-i, -2, -1+i)

m=8  2H -> 4H  vector=(0, 1, -1, 0)
  DFT = (0, 1-i, -2, 1+i)
```

Every legal edge has:

```text
constant component = 0
quadratic component = -2
both order-4 components nonzero
```

The four possible order-4 phases distinguish the four legal oriented edges.

## Controls

The pure quadratic aggregate is:

```text
odd_minus_even = (-1, 1, -1, 1)
DFT = (0, 0, -4, 0)
decision = repair_broad_quadratic_aggregate_boundary_2w
```

It has no order-4 components. This is exactly the too-broad quadratic
character statement already seen as the diagonal/all-four aggregate layer: it
does not select one edge.

Same-parity differences are also not current targets:

```text
same_parity_odd_difference  = (0, 1, 0, -1)
decision = reject_zero_boundary_same_parity_edge

same_parity_even_difference = (1, 0, -1, 0)
decision = reject_zero_boundary_same_parity_edge
```

They do not supply the odd/even edge with `W = Norm_156(Y_507)` boundary.

## Routing Rule

```text
one_edge_character_theorem
  accept only if it includes the order-4 C4 phase selecting one legal edge,
  plus the finite scalar-fixed value/divisor theorem or support-period-156
  value theorem.

quadratic_character_only
  repair as broad quadratic aggregate; missing order-4 selector.

order4_selector_without_value_theorem
  repair as selector data only; missing finite value/divisor theorem.

same_parity_character_statement
  reject as zero-boundary same-parity edge for the current target.
```

## Counts

```text
evidence_markers_ok = 5/5
legal_rows_ok = 4/4
controls_ok = 3/3
rows_with_order4_components = 4
pure_quadratic_controls = 1
current_source_theorems = 0
current_submission_ready = 0
p25_v2_c4_character_spectrum_rows=1/1
```

## Verdict

The one-edge theorem target is not recoverable from quadratic-character
language alone. A source theorem stated in character language must include the
order-4 `C4` phase data that selects one of the four legal edges, and it must
still supply the scalar-fixed finite value/divisor theorem. Otherwise it is a
selector or aggregate repair row, not a source-stage close.
