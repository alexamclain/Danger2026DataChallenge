# P27 GPU Recurrence-Coupling Telemetry

Date: 2026-06-22

## Claim

The GPU recurrence-coupling run is a clean kill for the current sign-word
coupling production idea.

It validates the recurrence/gamma telemetry formulas at GPU scale, but after
normalizing by raw X1(16) source draws the selected signs thin like independent
half-gates.  No heldout bucket meets the `1.25x` promotion bar.

This does not kill the A/B/K gamma class as a CAS object.  It kills the
production interpretation:

```text
run GPU from sign-word/gamma buckets before a named quotient, coboundary,
source map, or recurrence is extracted
```

## Source Artifacts

GPU branch:

```text
codex/add-cuda-p26-search
```

Commit:

```text
11c89c8 Add p27 recurrence coupling GPU telemetry
```

Compare link:

[main...codex/add-cuda-p26-search](https://github.com/alexamclain/Danger2026DataChallenge/compare/main...codex/add-cuda-p26-search?expand=1)

Primary result directories on that branch:

```text
results/p27/gpu_coupling_20260622T120157Z/
results/p27/gpu_coupling_g16_20260622T120332Z/
```

Local supporting paths:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/results/p27/gpu_coupling_20260622T120157Z/README.md
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/results/p27/gpu_coupling_g16_20260622T120332Z/README.md
```

## Gates 3..12

Run shape:

```text
GPU = NVIDIA A40, CUDA sm_86
seed orders = identity, splitmix
raw source draws = 100,000,000 per seed order
total raw source draws = 200,000,000
gate range = 3..12
short sign-word buckets = up to 6 bits
```

Summary:

```text
identity:
  recurrence rows = 6,256,372
  gate-12 survivors = 5,972
  target/source_draw = 0.00005972
  target/s = 352.88
  mismatches = 0

splitmix:
  recurrence rows = 6,249,614
  gate-12 survivors = 6,188
  target/source_draw = 0.00006188
  target/s = 366.07
  mismatches = 0

combined:
  recurrence rows = 12,505,986
  gate-12 survivors = 12,160
  target/source_draw = 0.0000608
```

Validation:

```text
B=sqrt(A+2) available for every recurrence row
formula_unavailable = 0
materialize_fail = 0
actual_mismatch = 0
```

Promotion result:

```text
largest all-plus heldout residual lift ~= 1.028x
promotion bar = 1.25x
verdict = fail promotion
```

## Gates 3..16

Run shape:

```text
GPU = NVIDIA A40, CUDA sm_86
seed orders = identity, splitmix
raw source draws = 100,000,000 per seed order
total raw source draws = 200,000,000
gate range = 3..16
short sign-word buckets = up to 8 bits
```

Summary:

```text
identity:
  recurrence rows = 6,256,372
  gate-16 survivors = 434
  target/source_draw = 0.00000434
  target/s = 25.62
  mismatches = 0

splitmix:
  recurrence rows = 6,249,614
  gate-16 survivors = 430
  target/source_draw = 0.00000430
  target/s = 25.42
  mismatches = 0

combined:
  gate-16 survivors = 864
  target/source_draw = 0.00000432
```

Validation:

```text
B=sqrt(A+2) available for every recurrence row
formula_unavailable = 0
materialize_fail = 0
actual_mismatch = 0
```

Promotion result:

```text
largest all-plus heldout residual lift ~= 1.053x
promotion bar = 1.25x
verdict = fail promotion
```

## Interpretation

Positive:

```text
The GPU implementation validates the recurrence/gamma formulas at scale.
The raw-source denominator is explicit.
The result agrees with the CPU 20k train/heldout telemetry boundary.
The A/B/K gamma lane remains a precise CAS class-comparison problem.
```

Negative:

```text
No sign-word bucket produces a source-normalized win.
No heldout promotion appears through gates 3..16.
The observed deviations are consistent with independent half-gate thinning.
The current GPU recurrence-coupling mode is not a production search strategy.
```

## Consequence

The front-door A/B/K task is now:

```text
offline CAS: compare gamma_4^2 = V+2 and gamma_5^2 = W+2 as Kummer/divisor
classes on selected components
```

The front-door GPU task is only:

```text
Dplus fused/native pricing, or bounded telemetry after CAS names a new
quotient/coboundary/source coordinate
```

## Continue / Kill

```text
continue = CAS normalize selected gamma components and compare repeated classes
continue = Dplus fused/native pricing as the separate GPU practical ask
continue = keep GPU recurrence telemetry as regression instrumentation

kill = production GPU run from current sign-word/gamma buckets
kill = all-plus residual buckets through gates 3..16 without a new invariant
kill = treating guard-field f5 one-sided tails as a source law
```

## Linked Artifacts

- [P27 Gamma-Chain 20k Telemetry](p27_gamma_chain_p27_20k_telemetry_20260622.md)
- [P27 A/B/K F4/F5 Transition Count](p27_abk_f4_f5_transition_count_20260622.md)
- [P27 A/B/K F3/F4 Chart Count](p27_abk_f3_f4_chart_count_20260622.md)
- [P27 A/B/K Symbolic Kummer CAS Brief](p27_abk_symbolic_kummer_cas_brief_20260622.md)

```text
p27_gpu_recurrence_coupling_rows=1/1
```
