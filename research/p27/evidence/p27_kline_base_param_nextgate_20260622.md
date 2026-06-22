# P27 B-Parameter Next-Gate Probe

Date: 2026-06-22

## Claim

The stable B-parameter bucket is an `8x` legal-containment boundary, not a
visible next-gate law.  After conditioning on actual legal `d2` rows, low-weight
B/K/A squareclass atoms do not give a stable predictor for `d3` or `d4`.

This kills the immediate GPU idea "score B-atom buckets for the next gate".
It keeps the B parameterization as a normalization surface for a real
function-field/CAS extraction of the legal cover.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_base_param_nextgate_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_base_param_nextgate_probe_p27_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_base_param_nextgate_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 6000 \
  --p27-heldout-target 6000 \
  --max-draws 1500000 \
  --max-weight 4 \
  --top 12 \
  --min-bucket 24 \
  | tee research/p27/archive/probe_outputs/p27_kline_base_param_nextgate_probe_p27_q1607_q1847_q2087_20260622.txt
```

## Exact Conditioning

The probe first verifies the previous B bucket on the actual legal rows:

```text
core bucket:
  chi(K)   = +1
  chi(B+2) = +1
  chi(B-2) = -1
  chi(L)   = +1
```

On p27 train and heldout:

```text
p27_train:   legal_KA = 3000, param_rows = 6000, core_bucket_rows = 6000
p27_heldout: legal_KA = 3000, param_rows = 6000, core_bucket_rows = 6000
```

On promotion fields:

```text
q1607: legal_KA = 49, param_rows = 98, core_bucket_rows = 98
q1847: legal_KA = 63, param_rows = 126, core_bucket_rows = 126
q2087: legal_KA = 57, param_rows = 114, core_bucket_rows = 114
```

So the `8x` bucket is still exact on this sample.  The question tested here is
only whether it can see the next selected gate.

## P27 Train/Heldout

For `d3`, train has only a weak best parity fit and it does not hold out:

```text
p27_train d3:
  plus/minus rows = 2988 / 3012
  majority_rate = 0.502000000
  best parity = 0.531333333
  combo = K-1 * A+14 * 3A+10

p27_heldout d3:
  plus/minus rows = 3052 / 2948
  majority_rate = 0.508666667
  best parity = 0.522333333
  combo = L+1 * 3A+10
```

Cross-evaluation of the train-best `d3` combo on heldout is below majority:

```text
K-1 * A+14 * 3A+10
  p27_train:   accuracy 0.531333333, majority_lift 1.058433
  p27_heldout: accuracy 0.500333333, majority_lift 0.983617
```

For `d4`, the same pattern appears:

```text
p27_train d4:
  plus/minus rows = 1506 / 1482
  majority_rate = 0.504016064
  best parity = 0.548192771
  combo = B^2+1 * 3A+10

p27_heldout d4:
  plus/minus rows = 1478 / 1574
  majority_rate = 0.515727392
  best parity = 0.538663172
  combo = L+1 * B^2+1 * A+6 * 3A+10
```

Cross-evaluation of the train-best `d4` combo weakens sharply:

```text
B^2+1 * 3A+10
  p27_train:   accuracy 0.548192771, majority_lift 1.087649
  p27_heldout: accuracy 0.523591000, majority_lift 1.015248
```

The bucket screens show higher local precisions, but the winning buckets are
different between train and heldout and are not theorem-shaped.

## Guard Fields

The promotion fields are too small for reliable fitting, and their winners do
not agree:

```text
q1607 d3 best parity:
  K+1 * K-1 * L+1 * B^2+1
  accuracy 68/98 = 0.693877551

q1847 d3 best parity:
  majority classifier only
  accuracy 90/126 = 0.714285714

q2087 d3 best parity:
  K-1
  accuracy 80/114 = 0.701754386
```

For `d4`, q1607/q1847/q2087 also disagree and the sample sizes are tiny after
conditioning on `d3=+1`.

## Interpretation

Positive:

```text
The B bucket remains exact on p27 train/heldout and q1607/q1847/q2087.
It is a real algebraic boundary for the legal cover over the K/A base curve.
```

Negative:

```text
Visible B/K/A squareclass atoms do not predict d3.
Visible B/K/A squareclass atoms do not predict d4.
Train/heldout cross-evaluation kills the apparent p27 fits.
Guard-field winners are inconsistent and too small to promote.
```

## Next Test

Do not spend GPU time on B-atom next-gate buckets.

The beat-sqrt version of this lane must now be a structural extraction:

```text
Normalize the legal cover over the B-rationalized base curve, including:
  A = B^2 - 2
  L = K^2
  K = Sroot^2 on the stable core bucket
  d3 reverse-root cover over the selected legal source

Compute branch/genus/decomposition data for that cover.
Promotion requires a genus <= 1 quotient, a sourceable walk, or a repeated
multi-gate coupling law.
```

## Continue / Kill

```text
continue = B-parameter function-field/CAS cover extraction
continue = bounded GPU telemetry only for the cheap all-recall bucket cost
continue = search for a repeated coupling law after structural extraction

kill = B-atom d3 predictor
kill = B-atom d4 predictor
kill = larger GPU search based on B buckets alone
```

```text
p27_kline_base_param_nextgate_rows=1/1
```
