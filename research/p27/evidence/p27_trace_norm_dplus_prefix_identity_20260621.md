# P27 Trace/Norm D_plus Prefix Identity

Date: 2026-06-21

## Claim

Trace/norm `D_plus` is not an unexplained deep-survivor law.  In the current
p27 C sampler it is exactly a two-gate continuation prefix:

```text
D_plus => selected first-branch depth >= 6
```

Equivalently, relative to the ordinary nonsplit X1(16) stream, it enforces the
first two selected halving gates.  This explains the GPU `4x` conditional lift:
it is the expected lift from conditioning on two independent half-density
gates.

This is still useful because `D_plus` gives a named trace/norm cover for the
first two gates, but it should not be interpreted as evidence of a hidden
late-depth recurrence by itself.

## Evidence

Baseline run:

```text
research/p27/archive/probe_outputs/p27_practical_baseline_x16halvestatsnonsplit_1M_20260621.txt
```

Trace/norm D_plus run:

```text
research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittraced_1M_20260621.txt
```

Baseline depth survival:

```text
depth=4 survive=1000000 rate=1.000000000
depth=5 survive=500052  rate=0.500052000
depth=6 survive=250756  rate=0.250756000
depth=7 survive=124978  rate=0.124978000
depth=8 survive=62652   rate=0.062652000
```

Trace/norm `D_plus` depth survival:

```text
depth=4 survive=1000000 rate=1.000000000
depth=5 survive=1000000 rate=1.000000000
depth=6 survive=1000000 rate=1.000000000
depth=7 survive=499210  rate=0.499210000
depth=8 survive=249864  rate=0.249864000
depth=9 survive=124348  rate=0.124348000
```

The `D_plus` depth histogram has no stops before depth 6:

```text
depth=6 count=500790
depth=7 count=249346
depth=8 count=125516
...
```

After depth 6, the conditioned stream returns to approximately geometric
half-loss.

## Relation To GPU A/B

The GPU narrowing note reported:

```text
ordinary_emitted_candidates = 1,000,051,462
candidate_emitted_candidates = 249,990,346
candidate/raw_y = 0.124995173
conditional_lift = 4.000 through observed depths 20..30
```

This is now interpreted as:

```text
D_plus = exact two-gate prefix
candidate/raw_y ~= 1/8 because:
  nonsplit_y ~= 1/2 raw_y
  two selected gates ~= 1/4 of ordinary nonsplit candidates
conditional_lift ~= 4x because two gates have already been paid
```

The GPU result remains valuable as a same-stream confirmation that this
trace/norm prefix is exact at scale.  It is not, by itself, a raw source-space
shrink beyond the continuation gates.

## Interpretation

Positive:

```text
The trace/norm cover is a clean algebraic handle on the first two selected
halving gates.
The Dplus cover equation and source-orientation pricing remain useful
mathematical artifacts.
```

Negative:

```text
Dplus does not currently show a recurrence to later gates.
After conditioning on Dplus, the observed later gates are random-looking.
The full orientation-source cover is genus 69, so direct full-cover sampling is
not the cheap route.
```

## Concrete Next Tests

1. Later-gate recurrence test:

```text
Ask GPU to report whether any additional trace/norm class on the Dplus
conditioned stream predicts depth >= 8, depth >= 10, or the next selected
x-square gate.
```

2. Quotient/Prym test:

```text
Do not sample the full genus-69 source cover.  Look for a low-genus quotient
or Prym factor that remembers Dplus and also couples to later d_j gates.
```

3. Practical interpretation:

```text
Dplus can be benchmarked as a two-gate prefix implementation.  Promote it only
if its exchange rate beats other ways to impose the same two gates.
```

## Continue / Kill

```text
continue = trace/norm as an algebraic description of early halving gates
continue = search for new trace/norm classes that predict post-Dplus gates
continue = quotient/Prym decomposition if it targets later-gate coupling

kill = interpreting the 4x GPU lift as a late-depth law
kill = calling Dplus a raw source-space shrink without a direct sampler
kill = full orientation-cover sampling as the first Dplus production plan
```

## Linked Artifacts

- Baseline output: `research/p27/archive/probe_outputs/p27_practical_baseline_x16halvestatsnonsplit_1M_20260621.txt`
- Dplus output: `research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittraced_1M_20260621.txt`
- GPU note: [P27 GPU Search-Space Narrowing Probe](p27_gpu_search_space_narrowing_20260621.md)
- Dplus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- Source orientation pricing: [P27 Trace/Norm Source-Orientation Cover](p27_trace_norm_source_orientation_cover_20260621.md)

```text
p27_trace_norm_dplus_prefix_identity_rows=1/1
```
