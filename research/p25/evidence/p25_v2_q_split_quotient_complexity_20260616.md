# P25 v2 Q Split Quotient Complexity

Updated: 2026-06-16

## Purpose

Record the source-side complexity of the boundary-zero split needed by the
compact `Q` diagonal route.

The Q diagonal-normalization screen shows:

```text
Q_antisym = m1 + m4 = m2 + m8
```

To normalize this diagonal aggregate to one legal edge, the relevant
boundary-zero splits are `m1-m4` and `m2-m8`. This screen checks whether those
splits are cheap one-axis or one-coset objects.

They are not. The exact Q diagonal splits are boundary-zero and
Frobenius-invariant, but they use all twelve mod-13 columns. The smaller
support-12 row quotients are real boundary-zero relations, but they are not the
diagonal splits that Q needs.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_split_quotient_complexity_gate.py
```

The gate returned `p25_v2_q_split_quotient_complexity_rows=1/1`.

## Diagonal Split Profiles

The two Q-relevant split quotients are:

```text
q1_4 = m1 - m4
q2_8 = m2 - m8
```

Both have:

```text
support = 24
coefficients = (-6, 6)
Hilbert-90 boundary = 0
Frobenius invariant = yes
mod-3 pushforward = 0
mod-13 pushforward = 0
live mod-13 columns = 12
row1 plus coset count = 2
row1 minus coset count = 2
```

Their quotient-`C4` row-antisymmetric projections are:

```text
q1_4: ( 36, -36, -36,  36)
q2_8: (-36, -36,  36,  36)
```

Thus the exact Q split is not a one-coset rectangle edge. It uses all twelve
mod-13 columns.

## Support-12 Controls

The other nontrivial row quotients are smaller:

```text
q1_2: support=12, rectangle edge yes, diagonal split no
q1_8: support=12, rectangle edge yes, diagonal split no
q2_4: support=12, rectangle edge yes, diagonal split no
q4_8: support=12, rectangle edge yes, diagonal split no
```

These are real boundary-zero relations, but they do not split the Q diagonal
aggregate `m1+m4=m2+m8`. Using one of them as the missing Q split is the wrong
split unless additional algebra changes the target.

## Routes

```text
q_split_value_only
  decision = repair_boundary_zero_split_only
  missing  = Q diagonal aggregate and oriented root/direct one-edge theorem

q_diagonal_plus_split_value_without_root
  decision = repair_oriented_square_root_missing
  missing  = halving/root/orientation data after reaching twice one edge

q_diagonal_plus_split_with_oriented_root
  decision = normalize_to_one_edge_then_apply_source_snippet_intake
  missing  = same theorem data after explicit oriented split/root normalization

support12_quotient_used_as_q_diagonal_split
  decision = reject_wrong_split_for_q_diagonal
  falsifier = support-12 row quotients are not m1-m4 or m2-m8

one_axis_or_one_coset_q_split_shortcut
  decision = reject_q_split_not_axis_or_one_coset
  falsifier = diagonal Q splits use all twelve mod-13 columns
```

## Counts

```text
evidence_markers_ok = 6/6
diagonal_split_count = 2
diagonal_support24_count = 2
diagonal_all_columns_count = 2
support12_non_diagonal_count = 4
normalize_routes = 1
repair_rows = 2
reject_rows = 2
current_source_theorems = 0
p25_v2_q_split_quotient_complexity_rows=1/1
```

## Verdict

The Q route is still live, but it has no newly discovered cheap split shortcut.
The exact Q split is a full-column boundary-zero quotient, and Q plus that
split reaches only a row square unless a source supplies oriented root/sign
data. The support-12 row quotients are useful context, but they are the wrong
splits for the Q diagonal aggregate.

Use this as the Q-route falsifier:

```text
Do not accept "support-12 quotient" or "one-coset/axis split" as the Q
normalizer.  The normalizer must be m1-m4 or m2-m8, plus oriented root data,
or a direct one-edge theorem.
```
