# P27 B-Line Alpha/Beta Phase Sequence Screen

Date: 2026-06-22

## Claim

The V4 gamma factors give useful structure, but the first recurrence/telescoping
screen is negative for a below-`sqrt(p)` sampler.

The factorization gives:

```text
f_{j+1} = alpha_j * beta_j
alpha_j = chi(H_j + R_j),  R_j^2 = H_j^2 - 4
beta_j  = chi(H_j + S_j),  S_j^2 = B^2 + H_j^2 - 4
H_j^2 = u_j + 2
u_j = x_j + 1/x_j
```

This probe walks the selected all-plus tower and asks whether the sheet phase
state predicts the next product, or whether link products such as
`alpha_j*alpha_{j+1}` telescope.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_alpha_beta_phase_sequence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_alpha_beta_phase_sequence_probe_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_alpha_beta_phase_sequence_probe.py \
  --p27-target 3000 \
  --p27-heldout-target 3000 \
  --max-draws 1000000 \
  --max-gate 8 \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_alpha_beta_phase_sequence_probe_20260622.txt
```

## P27 Results

The corrected accounting counts each generated phase/link once, not once per
descendant path.

Train sample:

```text
source x-draws = 23574
unique A/x5/B = 3000
phase records = 15372
phase links = 12384
```

Heldout sample:

```text
source x-draws = 25214
unique A/x5/B = 3000
phase records = 14516
phase links = 11400
```

The next-product rate is essentially random through the main range:

```text
train:   gate3 0.5194, gate4 0.4897, gate5 0.5000, gate6 0.5263
heldout: gate3 0.4865, gate4 0.4776, gate5 0.5028, gate6 0.4396
```

Gate7 is higher in both samples, but it is a later branch-weighted tail, not a
source-normalized sampler:

```text
train gate7 product plus = 0.5800 on 3200 phase records
heldout gate7 product plus = 0.6250 on 2560 phase records
```

The phase state itself does not give a promotable next-bit selector.  The only
stable-looking split is small:

```text
gate4 -> gate5:
  train   state -1 next-plus = 0.4794, state +1 next-plus = 0.5215
  heldout state -1 next-plus = 0.4763, state +1 next-plus = 0.5288
```

That is only about a `1.09x` to `1.11x` conditional skew after paying a half
split for the phase state.  It is below the `1.25x` source-normalized promotion
bar and does not beat random half-loss.

The link products are also near `1/2` and do not telescope:

```text
gate3 -> gate4:
  train aa/ab plus = 0.5077 / 0.5129
  heldout aa/ab plus = 0.4960 / 0.5053

gate5 -> gate6:
  train aa/ab plus = 0.4980 / 0.4967
  heldout aa/ab plus = 0.5117 / 0.5323

gate6 -> gate7:
  train aa/ab plus = 0.5181 / 0.4881
  heldout aa/ab plus = 0.5016 / 0.4844
```

## Guard Fields

The guard fields show local all-plus/all-minus plateaus, but the stopping gates
do not agree:

```text
q1607: gate4 all plus, gate5 all minus
q1847: gate4 all minus
q2087: gates4-6 all plus, gate7 all minus
```

So these are field-tail artifacts, not a p27 recurrence law.

## Interpretation

Positive:

```text
The alpha/beta phases are computable along the selected tower.
The phase sequence gives a clean GPU telemetry column.
The gate4 -> gate5 phase-state skew is a bounded follow-up statistic if GPU telemetry is free.
```

Negative:

```text
No phase state gives a source-normalized win.
No alpha/beta link product is stable enough to count as telescoping.
The guard-field plateaus are inconsistent across q1607/q1847/q2087.
```

The V4 factorization remains valuable as a class decomposition, but the first
finite-field/p27 phase-sequence screen does not promote it to a sampler.

Orientation follow-up:
[P27 B-Line Oriented Phase-Word Screen](p27_b_line_oriented_phase_word_screen_20260622.md)
tests the natural materialization sheet convention
`H=(x+1)/sqrt(x)`.  This closes the main orientation loophole: under that
choice `alpha=+1` and `beta` equals the actual next selected gate bit, so the
phase decomposition becomes tautological rather than predictive.

## Continue / Kill

```text
continue = keep alpha/beta as optional GPU telemetry columns when a run is already instrumented
continue = only promote a larger phase test with raw-source denominator and >=1.25x target/source lift
continue = CAS class extraction may still use the V4 decomposition

kill = alpha or beta as a standalone bucket
kill = current phase-state split as a production mode
kill = materialization-oriented alpha/beta as a source law
kill = interpreting guard-field phase plateaus as p27 recurrence evidence
kill = more CPU phase-word fitting without a named class or larger GPU telemetry
```

```text
p27_b_line_alpha_beta_phase_sequence_rows=1/1
```
