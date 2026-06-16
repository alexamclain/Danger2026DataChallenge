# Subsqrt Moonshot Lane B Residue-Mask Coupling

Date: 2026-06-12

## Result

The residue-coset mask is genuinely coupled between the inert right source and
the split C-axis source.  It cannot be produced by right-only data, C-only data,
or a separated row-plus-column local unit.

For the first `C_3 x C_13` lab, the carry mask on the `3 x 13` quotient
rectangles has:

```text
row_sums = [6, 6, 6]
column_sum_histogram = {0:4, 1:3, 2:3, 3:3}
rank over F_2 = 3
rank over an odd field = 3
nonzero mixed second differences over Z = 120
nonzero mixed second differences over F_2 = 108
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_residue_mask_coupling_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_residue_mask_coupling_gate.py
```

Observed:

```text
tiny_C3xC13:
  row_sums = [6,6,6]
  column_sum_histogram = {0:4, 1:3, 2:3, 3:3}
  rank_f2 = 3
  rank_odd = 3
  mixed_second_differences_z = 120
  mixed_second_differences_f2 = 108
  right_only = 0
  c_only = 0
  additive_separable_z = 0
  additive_separable_f2 = 0

prime_axis_C3xC53:
  row_sums = [26,26,26]
  column_sum_histogram = {0:14, 1:13, 2:13, 3:13}
  rank_f2 = 3
  rank_odd = 3
  mixed_second_differences_z = 2078
  mixed_second_differences_f2 = 1852

square_axis_C3xC169:
  row_sums = [84,84,84]
  column_sum_histogram = {0:43, 1:42, 2:42, 3:42}
  rank_f2 = 3
  rank_odd = 3
  mixed_second_differences_z = 21336
  mixed_second_differences_f2 = 18984

residue_mask_coupling_rows = 3/3
conclusion=reported_p25_laneB_residue_mask_coupling_gate
```

## Consequence

This is a sharper producer falsifier:

```text
the local object must genuinely couple the 151-side right cosets to the
677-side C cosets.
```

The following cannot be the complete Lane B producer:

```text
right-source-only local units;
C-axis-only local units;
additive row-plus-column masks;
rank-1 or rank-2 local masks;
any construction whose mixed second differences vanish.
```

The first viable arithmetic object must therefore produce a rank-`3` coupled
mask on the `3 x 13` quotient rectangles, while still satisfying the previously
recorded half-arc, residue-coset, and Kummer/sign obligations.

The character-support checkpoint for this same mask is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_residue_mask_character_support.md
```

It records the complementary obstruction: the coupled mask uses every
nontrivial pure-C character and every mixed right/C character, so sparse
character-support producers are also ruled out.
