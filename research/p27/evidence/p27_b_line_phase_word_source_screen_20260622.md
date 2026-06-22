# P27 B-Line Phase-Word Source Screen

Date: 2026-06-22

## Claim

The natural short V4 phase words do not give a source-normalized p27 sampler.

This is a bounded follow-up to the alpha/beta phase-sequence screen.  It does
not fit arbitrary words.  It tests pre-registered observables:

```text
alpha_j, beta_j
alpha_j*alpha_{j+1}, alpha_j*beta_{j+1}
beta_j*alpha_{j+1}, beta_j*beta_{j+1}
cumulative alpha products from gate 3
cumulative beta products from gate 3
```

Each bucket is scored against a later all-plus target with the raw p27
source-draw denominator preserved.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_phase_word_source_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_phase_word_source_probe_train_heldout_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_phase_word_source_probe.py \
  --p27-target 6000 \
  --p27-heldout-target 6000 \
  --max-draws 2000000 \
  --max-gate 9 \
  --target-gate 8 \
  --min-selected 500 \
  --small-primes '' \
  | tee research/p27/archive/probe_outputs/p27_b_line_phase_word_source_probe_train_heldout_20260622.txt
```

## Train/Heldout Baseline

Train:

```text
source x-draws = 47,241
unique A/x5/B = 6,000
phase paths = 26,052
target gate = 8
baseline target/source = 0.178827713
```

Heldout:

```text
source x-draws = 48,307
unique A/x5/B = 6,000
phase paths = 27,124
target gate = 8
baseline target/source = 0.196079243
```

## Best Buckets

The best train buckets are weak:

```text
a5=+1: conditional lift 1.048, selected target/source 0.098897144
b5=+1: conditional lift 1.046, selected target/source 0.098897144
cumb3_6=+1: conditional lift 1.035, selected target/source 0.095510255
```

The best heldout buckets are different and still below the promotion bar:

```text
cumb3_4=-1: conditional lift 1.119, selected target/source 0.111288219
bb3_4=-1: conditional lift 1.119, selected target/source 0.111288219
ab3_4=-1: conditional lift 1.119, selected target/source 0.111288219
cuma3_4=-1: conditional lift 1.115, selected target/source 0.111288219
```

No bucket clears the `1.25x` conditional bar, and every selected bucket has
lower absolute target/source than the unfiltered baseline because it still
pays the phase split.

## Interpretation

Positive:

```text
The GPU phase telemetry contract now has a CPU pre-screen for natural phase words.
The raw-source denominator is explicit, so conditional lift cannot masquerade
as a sampler.
```

Negative:

```text
Natural short V4 phase words are not source-normalized wins.
Train and heldout prefer different weak buckets.
No pre-registered bucket reaches 1.25x conditional lift, even before GPU
overhead is charged.
```

The alpha/beta factorization remains useful as a Kummer-class decomposition.
It is not currently a production filter or bucket sampler.

Orientation follow-up:
[P27 B-Line Oriented Phase-Word Screen](p27_b_line_oriented_phase_word_screen_20260622.md)
checks the natural materialization convention `H=(x+1)/sqrt(x)`.  It makes
`alpha=+1` and `beta` equal to the actual gate bit, so the best conditional
lifts keep exactly the same target/source denominator as baseline.  This is a
tautological gate filter, not a source shrink.

## Continue / Kill

```text
continue = keep alpha/beta columns only as cheap bounded GPU telemetry
continue = promote GPU phase work only if it finds a new heldout recurrence,
           telescoping product, sourceable sheet choice, or named class
continue = offline Kummer/divisor extraction of the gamma class

kill = natural short phase words as p27 production filters
kill = materialization-oriented phase words as p27 production filters
kill = larger CPU phase-word fitting without a named class
kill = interpreting weak conditional phase lift as source shrink
```

```text
p27_b_line_phase_word_source_screen_rows=1/1
```
