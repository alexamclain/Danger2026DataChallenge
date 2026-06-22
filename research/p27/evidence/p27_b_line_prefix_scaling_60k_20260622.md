# P27 B-Line 60K Prefix Scaling

Date: 2026-06-22

## Claim

The B-line multi-gate descent is structurally real, but it is not a
source-normalized sampler by itself.

On `60000 + 60000` p27 train/heldout source rows, the original `Bplus` value
still determines the active selected gate bits with zero mixed B groups
through the tested depth.  However, all-plus prefix counts thin like
independent half-gates through the meaningful range.  Any late apparent lift
is in single-digit or low-double-digit tails and does not transfer cleanly
between train and heldout.

This keeps the live B-line route focused on Kummer/divisor sequence extraction
`f3(B), f4(B), ...`, not B-bucket production or count-only GPU runs.

## Artifact

Probe:

```text
research/p27/archive/gates/p27_b_line_deep_descent_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_60k_heldout_60k_gate18_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes '' \
  --p27-target 60000 \
  --p27-heldout-target 60000 \
  --max-draws 1500000 \
  --max-gate 18 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_60k_heldout_60k_gate18_20260622.txt
```

## Train

```text
raw x-draws = 474936
B groups = 30000
B group size = 8 uniformly
mixed B groups = 0 through d18
```

Source-normalized prefix table:

```text
gate  plus  scaled_half_loss  source_draws_per_plus
d3    14967 0.997800000       31.732211
d4     7485 0.998000000       63.451703
d5     3760 1.002666667       126.312766
d6     1856 0.989866667       255.892241
d7      954 1.017600000       497.836478
d8      490 1.045333333       969.257143
d9      222 0.947200000       2139.351351
d10     117 0.998400000       4059.282051
d11      62 1.058133333       7660.258065
d12      28 0.955733333       16962.000000
d13      18 1.228800000       26385.333333
d14       9 1.228800000       52770.666667
d15       2 0.546133333       237468.000000
```

The only `>=1.20x` scaled values are in the `18` and `9` row tail.

## Heldout

```text
raw x-draws = 477180
B groups = 30000
B group size = 8 uniformly
mixed B groups = 0 through d18
```

Source-normalized prefix table:

```text
gate  plus  scaled_half_loss  source_draws_per_plus
d3    15065 1.004333333       31.674743
d4     7549 1.006533333       63.211021
d5     3820 1.018666667       124.916230
d6     1907 1.017066667       250.225485
d7      954 1.017600000       500.188679
d8      490 1.045333333       973.836735
d9      231 0.985600000       2065.714286
d10     120 1.024000000       3976.500000
d11      55 0.938666667       8676.000000
d12      31 1.058133333       15392.903226
d13      13 0.887466667       36706.153846
d14       7 0.955733333       68168.571429
d15       5 1.365333333       95436.000000
d16       2 1.092266667       238590.000000
d17       2 2.184533333       238590.000000
d18       1 2.184533333       477180.000000
```

The train `d13/d14` bump does not transfer; heldout's larger late scaled
values are based on only `5`, `2`, `2`, and `1` surviving B groups.

## Interpretation

Positive:

```text
Bplus remains an exact organizing coordinate for the selected tower.
No mixed B groups appeared in 60000/60000 p27 samples through d18.
The data are now strong enough to ask CAS/GPU for the B-line sequence itself.
```

Negative:

```text
No robust source-normalized lift appears through the meaningful counts.
All-plus prefixes behave like independent half-gates after B conditioning.
Large GPU telemetry should not be promoted merely to chase B buckets.
```

## Continue / Kill

```text
continue = B-line Kummer/divisor sequence extraction f3(B), f4(B), ...
continue = optional gate4/q2087 quartic closure only if needed for bookkeeping
continue = bounded GPU B-line telemetry only if it feeds class extraction

kill = Bplus prefix counts alone as a below-sqrt sampler
kill = large B-bucket production run without a named source or recurrence
kill = interpreting late single-digit tails as evidence of lift
kill = visible monic quartic d3 promotion after the q1847 B/K negatives
```

```text
p27_b_line_prefix_scaling_60k_rows=1/1
```
