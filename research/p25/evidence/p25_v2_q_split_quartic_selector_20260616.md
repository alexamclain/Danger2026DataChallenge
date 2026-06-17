# P25 v2 Q Split Quartic Selector

Updated: 2026-06-16

## Purpose

Record the positive structure behind the Q split route after the quotient
complexity falsifier.

The Q diagonal-normalization screen showed:

```text
Q_antisym = m1 + m4 = m2 + m8
```

The Q split quotient-complexity screen showed that the needed splits `m1-m4`
and `m2-m8` are not cheap support-12 row quotients. This screen records the
useful remaining fact: in row-antisymmetric quotient-`C4` Fourier coordinates,
the Q diagonal is pure quadratic and the Q split is pure order-4 selector
data. Together they recover twice one legal edge.

This is a support/normalization structure, not a source-stage closer by
itself, because the value side still needs oriented root/sign data or a direct
one-edge finite theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quotient_complexity_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_split_quartic_selector_gate.py
```

The gate returned `p25_v2_q_split_quartic_selector_rows=1/1`.

## Fourier Profiles

Use coefficient-6 row-antisymmetric quotient-`C4` coordinates. The legal edge
profiles are:

```text
m1: vector=(  0,   0, -36,  36), dft=(0,  36+36i, -72,  36-36i)
m2: vector=(-36,   0,   0,  36), dft=(0, -36+36i, -72, -36-36i)
m4: vector=(-36,  36,   0,   0), dft=(0, -36-36i, -72, -36+36i)
m8: vector=(  0,  36, -36,   0), dft=(0,  36-36i, -72,  36+36i)
```

The two Q diagonal presentations are pure quadratic:

```text
m1+m4: vector=(-36, 36, -36, 36), dft=(0, 0, -144, 0)
m2+m8: vector=(-36, 36, -36, 36), dft=(0, 0, -144, 0)
```

The Q-relevant splits are pure quartic:

```text
m1-m4: vector=( 36, -36, -36, 36), dft=(0,  72+72i, 0,  72-72i)
m2-m8: vector=(-36, -36,  36, 36), dft=(0, -72+72i, 0, -72-72i)
```

Thus the diagonal and split components separate cleanly:

```text
Q diagonal aggregate = pure quadratic component
Q boundary-zero split = pure quartic selector component
```

## Reconstruction

The matching diagonal and split recover twice an oriented edge:

```text
(m1+m4) + (m1-m4) = 2*m1
(m1+m4) - (m1-m4) = 2*m4

(m2+m8) + (m2-m8) = 2*m2
(m2+m8) - (m2-m8) = 2*m8
```

So an exact Q diagonal theorem plus the correct pure quartic split would
normalize to a row square. It still does not select the value of one edge
unless the source supplies oriented square-root/sign data, an explicitly
oriented diagonal-split normalization, or a direct one-edge theorem.

## Routes

```text
q_diagonal_pure_quadratic_only
  decision = support_diagonal_aggregate_selector_missing
  missing  = pure quartic split or direct one-edge theorem

q_split_pure_quartic_only
  decision = repair_boundary_zero_selector_only
  missing  = Q diagonal aggregate value and oriented root/direct one-edge theorem

q_diagonal_plus_pure_quartic_split_without_root
  decision = repair_oriented_square_root_missing
  missing  = oriented root/sign data after reaching twice one edge

q_diagonal_plus_pure_quartic_split_with_oriented_root
  decision = normalize_to_one_edge_then_apply_source_snippet_intake
  missing  = same theorem data after explicit oriented split/root normalization

q_split_wrong_quartic_phase
  decision = reject_wrong_q_split_phase
  falsifier = split phase must match m1-m4 or m2-m8 for the chosen diagonal
```

## Counts

```text
evidence_markers_ok = 6/6
edge_profiles_ok = 4/4
pure_quadratic_diagonals = 2
pure_quartic_splits = 2
reconstruction_rows_ok = 2/2
support_routes = 1
normalize_routes = 1
repair_rows = 2
reject_rows = 1
current_source_theorems = 0
p25_v2_q_split_quartic_selector_rows=1/1
```

## Verdict

The Q split route has a cleaner character interpretation than the support
count alone suggested. The diagonal aggregate is pure quadratic and the
matching split is pure quartic selector data. This is worth asking about in
expert/source language.

The current acceptance boundary is still strict:

```text
Q diagonal + correct quartic split + oriented root/sign
or explicit oriented diagonal-split normalization
or direct one-edge finite value/divisor theorem
```

Without the oriented root/sign or a direct one-edge theorem, the Q route
remains a repair/support route rather than a source-stage close.
