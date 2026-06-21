# P27 GPU Filter-Cost Lesson From P26

Date: 2026-06-21

## Claim

The p26 trace/norm GPU result is strong evidence that real source strata can
exist inside the X1(16) stream, but it is also a warning that a mathematically
good filter can lose as production code if its classifier is too expensive.

For p27, do not promote a stratum because it has a large conditional lift.
Promote it only if it improves effective deep survivors per GPU-second, or if
it gives a direct sampler/recurrence that avoids the classifier cost.

## Input Result

The p26 GPU note is:

[P26 GPU Trace/Norm A/B Results](../../p26/evidence/p26_gpu_trace_norm_ab_results_20260621.md).

Key p26 measurements:

```text
same-stream D_trace=+1 candidate set ~= 1/4 of ordinary candidates
all observed depth-20 through depth-28 survivors were inside D_trace=+1
baseline no-trace probe ~= 31.87M accepted roots/sec
best trace/norm filter-only run ~= 4.47M candidate roots/sec
```

So the stratum has nearly exact `4x` enrichment in survivor rate, but the
measured filter path is still slower in expected deep survivors per second
because the trace/norm classifier dominates runtime.

## P27 Consequence

The p27 compactD/order-4 work should be read through this lens:

```text
compactD=-1 is allowed to be a real source stratum.
compactD=-1 is not useful production math if it is only an expensive rejector.
```

The next GPU test should therefore report both:

```text
conditional survivor lift
effective survivor lift per GPU-second after all classifier/source costs
```

The better mathematical target is one of:

```text
direct sampling into the desired stratum
cheaper algebraic test for the same stratum
recurrence that makes d3/d4/d5 non-random after entering the stratum
```

## Acceptance Rule

For any p27 GPU filter/source test, require:

```text
same-stream baseline and candidate arms
raw or source rows per second
accepted roots per second
survivors by depth
effective survivor-per-second lift
classifier/source mismatch counts
```

A filter with `4x` enrichment and `>4x` throughput loss is a negative
production result even if it is positive structure.

## Continue / Kill

```text
continue = direct sampler into ecover/domain/compactD/order-4 strata
continue = cheaper compactD/order-4 character or cyclic-quartic test
continue = d3/d4 recurrence telemetry inside compactD=-1

kill = expensive classifier-only filters unless net GPU-second lift is positive
kill = seed-order explanations without a named invariant
kill = calling one fixed-prefix filter sqrt-beating without recurrence
```

## Linked Artifacts

- Source result: [P26 GPU Trace/Norm A/B Results](../../p26/evidence/p26_gpu_trace_norm_ab_results_20260621.md)
- Related p27 structure: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Related p27 test plan: [P27 Next Sqrt-Beating Test Cards](p27_next_sqrt_beating_test_cards_20260621.md)

```text
p27_gpu_filter_cost_lesson_from_p26_rows=1/1
```
