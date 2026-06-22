# P27 B-Line Phase GPU Telemetry Handoff

Date: 2026-06-22

## Claim

The next B-line GPU request should be a bounded phase-sequence telemetry test,
not a production hunt and not another fixed-prefix filter.

The current B-line class decomposition is:

```text
A = B^2 - 2
H_j^2 = u_j + 2
R_j^2 = H_j^2 - 4
S_j^2 = B^2 + H_j^2 - 4

alpha_j = chi(H_j + R_j)
beta_j  = chi(H_j + S_j)
f_{j+1} = alpha_j * beta_j
```

The small p27 CPU phase screen is negative as a sampler: no phase state or
link product clears the source-normalized promotion bar.  GPU is useful only
to close the scale loophole or reveal a heldout recurrence that the CPU sample
was too small to see.

The natural phase-word source screen is also negative:
[P27 B-Line Phase-Word Source Screen](p27_b_line_phase_word_source_screen_20260622.md).
On `6000+6000` p27 train/heldout starts, pre-registered short words built from
`alpha_j`, `beta_j`, adjacent products, and cumulative products all stay below
the `1.25x` conditional promotion bar, and every selected bucket has lower
absolute target/source than baseline.  Treat GPU phase telemetry as diagnostic
or class-discovery work, not as a likely production filter.

## Manifest

Machine-readable GPU contract:

```text
research/p27/archive/fixtures/p27_b_line_phase_gpu_telemetry_suite_20260622.json
```

Candidate CUDA mode name:

```text
x16blinephaseprobe
```

## Do Not Retest As Production Filters

The latest reduced-cover result matters:
[P27 B-Line Localized Cover Layer Count](p27_b_line_localized_cover_layer_count_20260622.md).
It finds

```text
chi(compactD_R_rhs / beta_rhs) = chi(d_next)
```

with zero mismatches in the tested fields.  Since the reduced `U_next` layer
already imposes `d_next` square, `compactD_R` is a twinned beta layer after
reduced_U, not a fresh production filter.
[P27 B-Line CompactD/Beta/Dnext Squareclass](p27_b_line_compact_beta_dnext_squareclass_20260622.md)
confirms the corresponding function-field square over `GF(7)` and `GF(23)`.

Also do not promote:

```text
alpha alone
beta alone
natural short phase words from the CPU pre-screen
Bplus buckets alone
short phase words without raw source accounting
conditional lift without target/source_draw lift
```

## What To Run

Emit the phase sequence from the same p27 candidate stream:

```text
Bplus or B-line key
selected gate bits d3,d4,...,dN
u_j, or enough replay data to reconstruct u_j
alpha_j
beta_j
alpha_j * beta_j
actual f_{j+1} / selected gate bit
first failing gate
raw source draw denominator
accepted/legal denominator
```

Minimum useful depth is `d3..d12`; `d3..d16` is better if cheap.  Treat deeper
tail data as evidence only if row counts are large enough for heldout
comparison.

Run tiers:

```text
implementation smoke:
  1M raw draws, identity seed order, mismatch check only

bounded telemetry:
  100M raw draws each for identity and splitmix

promotion tier:
  1B+ raw draws only if bounded telemetry shows a source-normalized signal
```

## Required Validation

Expected exact checks:

```text
alpha_j * beta_j = f_{j+1}
actual gate mismatch count = 0
compactD_R/beta/d_next mismatch count = 0 if that ratio is emitted
```

Individual `alpha_j` and `beta_j` depend on sheet choices and flip under
`H -> -H`; the product is the canonical bit.  Therefore the report must record
the sheet convention or replay payload when reporting one-factor statistics.

## What To Report

Required fields:

```text
commit hash
GPU model and compile flags
exact command lines
raw source draws
accepted candidates
legal d2 rows
B-line rows
phase records by gate
alpha/beta/product plus-minus counts by gate
actual selected-gate plus-minus counts by gate
alpha_beta_product_mismatches
actual_gate_mismatches
phase-word bucket counts
heldout lift by phase-word bucket
target survivors per raw source draw
target survivors per GPU-second
overhead versus baseline
logs saved under results/p27/
```

## Promotion

Promote only if one of these appears on heldout streams:

```text
phase-word or state lift improves target/source_draw by >= 1.25x
a telescoping product couples multiple selected gates
a sourceable sheet choice avoids paying a fresh half-loss
a named Kummer/divisor hypothesis emerges for f4/f3 and f5/f4
```

If promoted, the next artifact should be a source law, recurrence, or CAS
class extraction target.  It should not be another bucket run.

## Kill

Kill this GPU lane if:

```text
alpha/beta pairs behave like fresh independent half-losses
phase-word lifts are only conditional and disappear source-normalized
the result matches the small CPU screen at larger scale
telemetry overhead worsens target/GPU-second
no named class or recurrence is produced
```

## Relationship To Current B-Line Work

This is a scale/telemetry companion to:

```text
P27 B-Line Gamma V4 Factorization
P27 B-Line Alpha/Beta Phase Sequence Screen
P27 B-Line Reduced-Cover Symbolic Packet
P27 B-Line Localized Cover Layer Count
```

It does not replace the main offline CAS ask: normalize the no-R reduced
B-line cover and extract the `f3`, `f4/f3`, ... Kummer classes.  It only tests
whether the phase sequence contains a recurrence strong enough to justify GPU
follow-up before that CAS extraction is complete.

## Continue / Kill

```text
continue = bounded GPU x16blinephaseprobe if instrumentation is cheap
continue = use phase columns as support for B-line Kummer extraction
continue = promote only source-normalized heldout recurrence or class evidence

kill = natural short phase words as production filters after the CPU pre-screen
kill = compactD_R standalone GPU filter after reduced_U
kill = alpha-only or beta-only bucket production
kill = Bplus-only production from no-mixed-B evidence
kill = larger phase fitting without raw-source denominators
```

```text
p27_b_line_phase_gpu_telemetry_handoff_rows=1/1
```
