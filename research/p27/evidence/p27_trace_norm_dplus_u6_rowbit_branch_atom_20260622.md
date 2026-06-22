# P27 Trace/Norm Dplus U6 Row-Bit Branch-Atom Screen

Date: 2026-06-22

## Claim

The descended Dplus `U6` row bit is not explained by the visible branch
characters exposed by the symbolic resultant.

After

```text
chi(U6+2)=chi(x6)
```

was shown to be uniform across the four `U6` branches over each Dplus row, the
nearest cheap source hypothesis was:

```text
maybe the row bit is a product of t-branch atoms.
```

This probe screens the exact branch factors

```text
t, t-1, t+1, t^2+1, t^2+2t-1, t^2-2t-1
```

plus nearby `A` and `X=t^3+2t^2-1/t` atoms through product weight `5`.  It
finds no exact product and no stable heldout lift.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_branch_atom_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_branch_atom_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_rowbit_branch_atom_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-y 0 \
  --max-weight 5 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_rowbit_branch_atom_probe_20260622.txt
```

## Result

Rows:

```text
train:
  analyzed_y = 8199
  target_+1 = 4149
  target_-1 = 4050

heldout:
  analyzed_y = 8061
  target_+1 = 3986
  target_-1 = 4075
```

Feature profile:

```text
active_features = 13
constant_features = 5
exact_branch_atom_combos = none
```

The best heldout-ranked products are all equivalent to the same weak `A`
majority effect:

```text
combo = -A
train   = 4062/8199 = 0.495426
heldout = 4152/8061 = 0.515072
combined = 8214/16260 = 0.505166
```

This is below promotion and not stable across train/heldout.

## Interpretation

Positive:

```text
The visible branch-factor loophole is now directly tested.
The exact resultant branch atoms are not the missing source law.
```

Negative:

```text
No product of the tested t/A/X branch characters through weight 5 gives the
descended U6 row bit.
The best apparent heldout lift is a weak A-bias that reverses on train.
This does not justify GPU branch-atom buckets.
```

## Consequence

The Dplus row-bit route is now narrowed to:

```text
exact Kummer/Prym comparison of the descended row bit with A_eta,
or a non-visible quotient/theta/source relation on the selected Dplus base.
```

Do not spend more effort on visible branch-atom products unless a new theorem
supplies a different atom set.

## Continue / Kill

```text
continue = CAS/Prym comparison of descended U6 row bit with H90 A_eta
continue = selected-source A/B/K Kummer extraction
continue = fused/native Dplus pricing with row-bit telemetry

kill = visible t-branch atom products through weight 5
kill = A/X branch atom buckets as Dplus row-bit sources
kill = GPU production from Dplus row-bit buckets before a source relation
```

```text
p27_trace_norm_dplus_u6_rowbit_branch_atom_rows=1/1
```
