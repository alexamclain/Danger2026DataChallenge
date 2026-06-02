# X1(16) Nonsplit Branch Depth-20 Holdout

Generated locally: 2026-06-01 20:45 PDT

Purpose: test whether branch-selection work remains relevant for the active
y-filtered nonsplit X1(16) fallback. Earlier diagnostics showed that bounded
all-branch halving improves all-X1 survival, but that nonsplit first-branch and
nonsplit all-branch were identical through depth 16. This holdout extends that
check to depth 20 on fresh paired seeds.

## Commands

```bash
mkdir -p runs/branchstats_holdout_20260601_2045

nice -n 19 ./pomerance_branchstats_nonsplit \
  100000000000000000000117 17171 100000 x16branchstatsnonsplit 20 \
  | tee runs/branchstats_holdout_20260601_2045/p23_nonsplit_branch_100k_seed17171_depth20.log

nice -n 19 ./pomerance_branchstats_nonsplit \
  100000000000000000000117 17171 100000 x16branchstats 20 \
  | tee runs/branchstats_holdout_20260601_2045/p23_all_branch_100k_seed17171_depth20.log

nice -n 19 ./pomerance_branchstats_nonsplit \
  100000000000000000000117 18181 100000 x16branchstatsnonsplit 20 \
  | tee runs/branchstats_holdout_20260601_2045/p23_nonsplit_branch_100k_seed18181_depth20.log

nice -n 19 ./pomerance_branchstats_nonsplit \
  100000000000000000000117 18181 100000 x16branchstats 20 \
  | tee runs/branchstats_holdout_20260601_2045/p23_all_branch_100k_seed18181_depth20.log
```

These are low-priority bounded diagnostics. They do not touch the active p23
production workers.

## Structural Result

For both fresh nonsplit seeds, every logged depth through 20 had:

```text
nonsplit first_survive = nonsplit all_survive
```

The all-branch frontier among nonsplit survivors also grew as an exact power of
two:

```text
depth 12 avg frontier = 256
depth 14 avg frontier = 1024
depth 16 avg frontier = 4096
depth 18 avg frontier = 16384
depth 20 avg frontier = 65536
```

Interpretation:

```text
Within the y-filtered nonsplit family, the natural first branch appears to
survive exactly when any bounded branch survives, at least through depth 20 on
these p23 samples. This means branch-selection heuristics are not a promising
way to improve the active nonsplit fallback unless this equality breaks much
deeper.
```

This is not true in the all-X1 family, where all-branch survival remains above
first-branch survival and frontier sizes are irregular.

## Aggregated Counts

Two paired seeds, 100k samples each, aggregate `N = 200000`.

For a broader aggregate including the earlier paired depth-14 and depth-16
holdouts, see:

```text
notes/p23_nonsplit_lift_calibration_20260601.md
scripts/analyze_branch_lift.py
```

```text
all-X1:
  depth 12: first 423/200000 = 0.002115, all 524/200000 = 0.002620
  depth 14: first 110/200000 = 0.000550, all 138/200000 = 0.000690
  depth 16: first  20/200000 = 0.000100, all  26/200000 = 0.000130
  depth 18: first   6/200000 = 0.000030, all   6/200000 = 0.000030
  depth 20: first   2/200000 = 0.000010, all   2/200000 = 0.000010

nonsplit:
  depth 12: first 808/200000 = 0.004040, all 808/200000 = 0.004040
  depth 14: first 192/200000 = 0.000960, all 192/200000 = 0.000960
  depth 16: first  36/200000 = 0.000180, all  36/200000 = 0.000180
  depth 18: first   8/200000 = 0.000040, all   8/200000 = 0.000040
  depth 20: first   4/200000 = 0.000020, all   4/200000 = 0.000020
```

Nonsplit first relative to all-X1:

```text
depth 12: 1.91x over all-X1 first, 1.54x over all-X1 all
depth 14: 1.75x over all-X1 first, 1.39x over all-X1 all
depth 16: 1.80x over all-X1 first, 1.38x over all-X1 all
depth 18: 1.33x over all-X1 first, 1.33x over all-X1 all
depth 20: 2.00x over all-X1 first, 2.00x over all-X1 all
```

Depths 18 and 20 have very small counts and should be read as consistency
checks, not precise lift estimates.

## Decision

No production change.

This strengthens the current operational choice:

```text
keep the active y-filtered nonsplit X1(16) shard running
```

It also demotes branch-selection work for the active nonsplit fallback:

```text
all-X1 branch selection remains mathematically real, but the nonsplit filter
appears to remove the local branch-selection loss through depth 20. Future
branch work should focus on a deeper/growing-tower story, not on replacing the
current nonsplit first-branch production sampler.
```
