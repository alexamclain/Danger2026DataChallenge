# P25 v2 Quartic Selector Payload

Updated: 2026-06-16

## Purpose

State the smallest currently identified source-side selector datum for the
H0/conductor-39 edge target.

The Frobenius tensor eigenboundary explains why Hilbert-90 boundary data loses
the edge selector. This screen records the converse: an exact row-antisymmetric
quotient-`C4` order-4 phase, together with the boundary and a scalar-fixed
finite theorem, is enough to select one of the four legal edges. Coarser
phase data leaves a pair or all-four ambiguity.

This is not the missing arithmetic value/divisor theorem. It is the current
minimal selector-payload contract for source snippets or expert replies stated
in character language.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_c4_character_spectrum_20260616.md`
- `evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md`
- `evidence/p25_v2_frobenius_tensor_eigenboundary_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_quartic_selector_payload_gate.py
```

The gate returned `p25_v2_quartic_selector_payload_rows=1/1`.

## Selector Coordinates

In row-antisymmetric quotient-`C4` Fourier coordinates, all four legal rows
have the same boundary spectrum:

```text
boundary DFT = (0, 0, -8, 0)
```

The exact `C4_1` phase distinguishes them:

```text
m=1  7H -> 4H
  C4_1 =  2+2i
  C4_3 =  2-2i
  selector = R+I+

m=2  7H -> H
  C4_1 = -2+2i
  C4_3 = -2-2i
  selector = R-I+

m=4  2H -> H
  C4_1 = -2-2i
  C4_3 = -2+2i
  selector = R-I-

m=8  2H -> 4H
  C4_1 =  2-2i
  C4_3 =  2+2i
  selector = R+I-
```

`C4_3` is the conjugate selector, so one exact quartic coordinate is enough.

## Coarse Selectors

```text
real sign positive only:
  surviving edges = m1, m8
  decision = repair two-edge column pair

real sign negative only:
  surviving edges = m2, m4
  decision = repair two-edge column pair

imaginary sign positive only:
  surviving edges = m1, m2
  decision = repair two-edge row pair

imaginary sign negative only:
  surviving edges = m4, m8
  decision = repair two-edge row pair

quartic magnitude only:
  surviving edges = m1, m2, m4, m8
  decision = repair all-four ambiguity
```

Thus the minimal selector is not "some quartic character language"; it is the
exact order-4 phase in the mixed row-antisymmetric tensor setting.

## Routing Rule

```text
boundary_plus_exact_quartic_selector_value
  decision = source-stage candidate if finite theorem present
  requirement = W boundary + exact C4_1 phase + scalar-fixed finite theorem

exact_quartic_selector_without_value_theorem
  decision = repair_value_divisor_theorem_missing
  missing = finite value/divisor theorem for the selected row

boundary_plus_one_sign_of_phase
  decision = repair_two_edge_ambiguity
  missing = remaining quartic sign or direct one-edge theorem

quartic_magnitude_or_quadratic_only
  decision = repair_all_four_edge_ambiguity
  missing = exact order-4 phase selecting one legal edge

quartic_phase_without_row_sign
  decision = repair_mixed_tensor_missing
  missing = row-antisymmetric mod-3 sign and zero proper pushforwards

same_parity_quartic_phase
  decision = reject_zero_boundary_wrong_edge
  falsifier = same-parity edges have zero W boundary
```

## Counts

```text
evidence_markers_ok = 6/6
legal_rows_ok = 4/4
unique_quartic_selectors = 4
unique_boundaries = 1
coarse_selectors_ok = 5/5
accepted_routes = 1
repair_rows = 4
reject_rows = 1
current_source_theorems = 0
current_submission_ready = 0
p25_v2_quartic_selector_payload_rows=1/1
```

## Verdict

The current shortest positive character-language ask is:

```text
one legal W-boundary tensor row
+ exact row-antisymmetric C4_1 phase
+ scalar-fixed finite value/divisor theorem
```

Boundary data, quadratic data, quartic magnitude, or only one sign of the
quartic phase does not select a single edge. An exact quartic selector without
the finite theorem is still only a selector, not a source-stage closer.
