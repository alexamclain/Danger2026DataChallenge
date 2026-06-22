# P27 B-Line Prefix Profile

Date: 2026-06-22

## Claim

The B-line descent is real, but it is not yet a sqrt-beating source.

Exact small-field profiles show striking late-tail collapses, but the collapse
gate depends on the field.  A larger p27 train/heldout sample through `d16`
does not reproduce that behavior: the all-plus B population thins close to
one independent half-loss per selected gate until tails become too small.

So the B-line remains useful as a Kummer-class extraction surface, but the
current evidence kills treating B alone as a direct scope shrink or as a reason
for a large production GPU run.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_prefix_profile_probe.py
research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q7_degrees3_5_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q23_degrees1_3_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q1607_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q1847_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q2087_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_train_heldout_gate16_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q31_degrees1_3_gate8_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_12k_heldout_12k_gate14_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_profile_probe.py \
  --q 7 \
  --degrees 3,4,5 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q7_degrees3_5_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_profile_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q23_degrees1_3_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_profile_probe.py \
  --q 1607 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q1607_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_profile_probe.py \
  --q 1847 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q1847_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_prefix_profile_probe.py \
  --q 2087 \
  --degrees 1 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_profile_probe_q2087_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes '' \
  --p27-target 8000 \
  --p27-heldout-target 8000 \
  --max-draws 3000000 \
  --max-gate 16 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_train_heldout_gate16_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py \
  --q 31 \
  --degrees 1,2,3 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q31_degrees1_3_gate8_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes '' \
  --p27-target 12000 \
  --p27-heldout-target 12000 \
  --max-draws 5000000 \
  --max-gate 14 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_12k_heldout_12k_gate14_20260622.txt
```

## Exact Small-Field Profiles

The exact extension-field profile records:

```text
scaled(j) = prefix_B(d3..dj) * 2^(j-2) / legal_B
```

Representative exact fields:

```text
GF(7^5), legal_B = 590:
  gate3: plus=315, scaled=1.0678
  gate4: plus=140, scaled=0.9492
  gate5: plus=140, scaled=1.8983
  gate6: plus=0

GF(23^3), legal_B = 399:
  gate3: plus=216, scaled=1.0827
  gate4: plus=120, scaled=1.2030
  gate5: plus=84,  scaled=1.6842
  gate6: plus=84,  scaled=3.3684
  gate7: plus=84,  scaled=6.7368
  gate8: plus=84,  scaled=13.4737

GF(31^3), legal_B = 930:
  gate3: plus=465, scaled=1.0000
  gate4: plus=225, scaled=0.9677
  gate5: plus=75,  scaled=0.6452
  gate6: plus=75,  scaled=1.2903
  gate7: plus=0

GF(1607), legal_B = 49:
  gate3: plus=28, scaled=1.1429
  gate4: plus=19, scaled=1.5510
  gate5: plus=19, scaled=3.1020
  gate6: plus=0

GF(1847), legal_B = 63:
  gate3: plus=45, scaled=1.4286
  gate4: plus=19, scaled=1.2063
  gate5: plus=0

GF(2087), legal_B = 57:
  gate3: plus=25, scaled=0.8772
  gate4: plus=18, scaled=1.2632
  gate5: plus=18, scaled=2.5263
  gate6: plus=18, scaled=5.0526
  gate7: plus=18, scaled=10.1053
  gate8: plus=0
```

These tails are not stable across fields.  They look like small-field
Frobenius/component artifacts, not a transferable p27 law.

## P27 Train/Heldout Profile

The p27 check used `4000` B groups in train and `4000` B groups in heldout.
No mixed B groups were reported.

Train all-plus prefix:

```text
gate3  2018 / 4000
gate4  1024 / 4000
gate5   505 / 4000
gate6   241 / 4000
gate7   126 / 4000
gate8    66 / 4000
gate9    28 / 4000
gate10   12 / 4000
gate11    6 / 4000
gate12    2 / 4000
gate13    2 / 4000
gate14    1 / 4000
gate15    0 / 4000
```

Heldout all-plus prefix:

```text
gate3  2048 / 4000
gate4  1008 / 4000
gate5   500 / 4000
gate6   240 / 4000
gate7   110 / 4000
gate8    63 / 4000
gate9    31 / 4000
gate10   18 / 4000
gate11    6 / 4000
gate12    5 / 4000
gate13    3 / 4000
gate14    3 / 4000
gate15    2 / 4000
gate16    1 / 4000
```

Through the range with meaningful counts, this is consistent with ordinary
half-loss behavior.  The late scaled ratios are dominated by tiny tails.

The larger 2026-06-22 p27 check used `6000` B groups in train and `6000` B
groups in heldout, with no mixed B groups reported.

Train all-plus prefix:

```text
gate3  3024 / 6000
gate4  1516 / 6000
gate5   771 / 6000
gate6   374 / 6000
gate7   195 / 6000
gate8   104 / 6000
gate9    50 / 6000
gate10   25 / 6000
gate11    9 / 6000
gate12    3 / 6000
gate13    2 / 6000
gate14    1 / 6000
```

Heldout all-plus prefix:

```text
gate3  3044 / 6000
gate4  1493 / 6000
gate5   755 / 6000
gate6   363 / 6000
gate7   171 / 6000
gate8    86 / 6000
gate9    43 / 6000
gate10   23 / 6000
gate11    9 / 6000
gate12    7 / 6000
gate13    4 / 6000
gate14    4 / 6000
```

This reinforces the earlier read.  Through `gate10`, where the counts are
still meaningful, both train and heldout are close to independent half-loss.
The small-field plateaus are field-dependent and do not transfer to p27 at the
current sample scale.

Current update:
[P27 B-Line 60K Prefix Scaling](p27_b_line_prefix_scaling_60k_20260622.md)
supersedes the sample-size boundary.  On `30000 + 30000` B groups, there are
still zero mixed B groups through `d18`, but source-normalized scaled half-loss
stays close to `1` through the meaningful `d3..d12` range.  Train's late
`d13/d14` bump has only `18/9` surviving B groups and does not transfer to
heldout.  The current conclusion is therefore stronger:

```text
Bplus is an exact Kummer-sequence coordinate.
Bplus prefix counts alone are not a below-sqrt sampler.
```

## Interpretation

Positive:

```text
Bplus remains a genuine descent coordinate for the selected gate sequence.
No mixed B groups appeared in the p27 train/heldout gate16 run.
The B-line is still a clean place to extract actual divisor/Kummer classes.
```

Negative:

```text
B-line all-plus prefixes do not currently show p27 source shrink beyond
constant-factor conditioning.
Small-field all-plus plateaus are not stable enough to promote.
There is no evidence here for a B-only production GPU mode.
```

## Next Tests

Continue:

```text
exact divisor/Kummer class extraction for f3(B), f4(B), ...
comparison of those classes in the function field, not visible-factor scans
bounded GPU Bplus+d3..dN telemetry only as a no-mixed / density confirmation
large GPU B-line telemetry should report source-normalized prefix counts and
mixed-B examples, not only conditional bucket lifts
```

Shift priority back to the more credible sqrt-beating tests:

```text
staged legal pullback normalization of the conic-chain Kummer tower
E/E' double-cover class extraction for d3 and d4
trace/norm half-norm phase identity
```

Kill:

```text
B-line counts alone as a below-sqrt sampler
large production GPU search based only on Bplus buckets
using small-field late-tail plateaus as evidence for p27 scope shrink
```

```text
p27_b_line_prefix_profile_rows=1/1
```
