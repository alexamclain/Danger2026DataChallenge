# P27 U+2 Sequence Recurrence Screen

Date: 2026-06-21

## Claim

Starting from the p27 compactD/d2 stratum, the selected sequence of
`chi(u_j+2)` gates behaves like independent half-losses through the measured
range.  No short prefix-conditioned recurrence is visible.

This is a negative moonshot result: the `u+2` identity gives a cleaner local
gate and a possible GPU cost optimization, but not a tower law by itself.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p27/archive/gates/p27_usquare_sequence_recurrence_probe.py \
  --target 30000 \
  --max-draws 6000000 \
  --max-gates 12 \
  | tee research/p27/archive/probe_outputs/p27_usquare_sequence_recurrence_probe_20260621.txt
```

The probe samples compactD/d2 rows and follows one representative selected
path.  At each successful gate it records:

```text
x_next + 1/x_next = u
next gate bit = chi(u+2)
```

The paired T/branch probe already showed the obvious paired roots and half
branches agree on d3/d4, so this recurrence screen uses one representative per
pair.

## Result

Input sample:

```text
sampled_pairs = 30000
x_draws = 235889
candidate_invalid_not_nonsplit = 59140
compact_not_target = 58926
pair_incomplete = 29570
```

Gate-prefix rates:

```text
gate  samples  plus   minus  plus_rate
3     30000    15004  14996  0.500133333
4     15004     7464   7540  0.497467342
5      7464     3706   3758  0.496516613
6      3706     1854   1852  0.500269833
7      1854      964    890  0.519956850
8       964      516    448  0.535269710
9       516      220    296  0.426356589
10      220      114    106  0.518181818
11      114       54     60  0.473684211
12       54       22     32  0.407407407
```

The first four tested gates after compactD are essentially exact half-losses.
The later rates have small sample sizes and do not show a stable drift.

Prefix-success histogram:

```text
plus_prefix_len=0 count=14996 rate=0.499866667
plus_prefix_len=1 count=7540  rate=0.251333333
plus_prefix_len=2 count=3758  rate=0.125266667
plus_prefix_len=3 count=1852  rate=0.061733333
plus_prefix_len=4 count=890   rate=0.029666667
plus_prefix_len=5 count=448   rate=0.014933333
plus_prefix_len=6 count=296   rate=0.009866667
plus_prefix_len=7 count=106   rate=0.003533333
plus_prefix_len=8 count=60    rate=0.002000000
plus_prefix_len=9 count=32    rate=0.001066667
plus_prefix_len=10 count=22   rate=0.000733333
```

No anomalies were observed:

```text
anomaly_stats = none
```

## Interpretation

Positive:

```text
The u+2 gate is stable enough to use as a clean prefix-gate telemetry target.
GPU can implement fixed-prefix tests as chi(u_j+2) checks and report actual
cost.
```

Negative:

```text
No prefix-conditioned recurrence appears through gate 12.
The prefix histogram is consistent with geometric half-loss.
Independent u+2 checks remain constant-factor filters.
```

## Consequence

The immediate sqrt-beating hope:

```text
compactD enters a stratum where later chi(u_j+2) bits become biased
```

is not supported by this probe.

The remaining moonshot must be stronger:

```text
find a non-local Kummer/theta/Hilbert-90 relation coupling many chi(u_j+2)
characters at once, or construct a source that samples the all-plus locus
without paying one random bit per gate.
```

The norm/coboundary follow-up further narrows this:
[P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md).
The local norms through `s -> -s` are exact, but the selected branch's `u+2`
orientation is not in the small local `A,x` norm span.

The selected-orientation follow-up narrows it again:
[P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md).
Even after allowing selected `s`-branch orientation characters from the whole
successful prefix, no exact GF(2) product predicts the next `u+2` bit through
gates 3-6 on two 30,000-row seeds.

## Concrete Next Tests

1. GPU cost test:

```text
baseline fixed prefix: materialize x_next then test next d
candidate fixed prefix: test chi(u+2) before sqrt(w)/x_next materialization
metric: effective survivors per GPU-second
```

2. Symbolic recurrence test:

```text
derive explicit formulas for u_{j+1}+2 in terms of u_j, A, and the chosen
Kummer square roots; look for a norm/coboundary product spanning multiple
successive gates.
```

3. Source test:

```text
try to parameterize the all-plus locus for chi(u_3+2),...,chi(u_m+2) as an
iterated 2-cover, then ask whether it has a low-genus quotient or cheap walk.
```

## Continue / Kill

```text
continue = GPU u+2 precheck as a cost optimization
continue = symbolic multi-gate Kummer/theta recurrence for chi(u_j+2)
continue = reverse-doubling all-plus source / non-visible H90 quotient
continue = low-genus/source test for the all-plus iterated 2-cover

kill = expecting compactD alone to bias the later u+2 sequence
kill = local A,x norm-character selector for selected u+2
kill = small selected-orientation product span for selected u+2
kill = claiming fixed-prefix u+2 filters beat sqrt scaling
kill = branch-choice or T-deck-choice selector for the u+2 sequence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_usquare_sequence_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_usquare_sequence_recurrence_probe_20260621.txt`
- Related: [P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md)
- Related: [P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md)
- Related: [P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md)
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)
- Related: [P27 Selected Halving Tower Profile](p27_halving_tower_profile_20260621.md)

```text
p27_usquare_sequence_recurrence_rows=1/1
```
