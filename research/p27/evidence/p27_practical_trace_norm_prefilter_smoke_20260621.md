# P27 Practical Trace/Norm Prefilter Smoke

Date: 2026-06-21

## Claim

The current C practical sampler handles p27 in both baseline nonsplit stats mode
and raw trace/norm `D` prefilter stats mode.  The trace/norm prefilter is not a
moonshot by itself, but it is now a concrete GPU A/B candidate: on a bounded
1M-vs-1M CPU comparison it trades candidate throughput for an approximately
two-depth survivor lift, yielding a modest positive per-second signal at stable
depths.

## Build

```bash
cc -O3 -o src/pomerance src/pomerance.c
```

## Tiny Smoke

```bash
./src/pomerance 1000000000000000000000000103 121 10000 x16halvestatsnonsplit

./src/pomerance 1000000000000000000000000103 121 10000 x16halvestatsnonsplittraced
```

Both ran cleanly with `k = 45`.

## 1M Baseline

Command:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplit \
  | tee research/p27/archive/probe_outputs/p27_practical_baseline_x16halvestatsnonsplit_1M_20260621.txt
```

Result:

```text
sample_class = nonsplit_y_filtered
samples = 1000000
elapsed_seconds = 6.460183
rate_Mps = 0.154794
full_first_branch_depth_45 = 0/1000000
survive depth 16 = 238
survive depth 17 = 130
survive depth 18 = 66
survive depth 19 = 36
survive depth 20 = 8
```

## 1M Trace/Norm Prefilter

Command:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplittraced \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittraced_1M_20260621.txt
```

Result:

```text
sample_class = nonsplit_trace_norm_D_prefilter
samples = 1000000
elapsed_seconds = 22.861659
rate_Mps = 0.043741
raw_y_draws = 7994995
raw_y_rate_Mps = 0.349712
nonsplit_y = 3997259
both_square = 1999752
D_plus = 1000084
D_minus = 999668
root_valid_decks = 1000000
emitted_candidates = 1000000
full_first_branch_depth_45 = 0/1000000
survive depth 16 = 928
survive depth 17 = 504
survive depth 18 = 262
survive depth 19 = 152
survive depth 20 = 68
```

## Per-Second Comparison

```text
trace/base emitted candidate rate = 0.282575552
depth 16 survivor_lift = 3.899159664  net_per_second = 1.101807194
depth 17 survivor_lift = 3.876923077  net_per_second = 1.095523679
depth 18 survivor_lift = 3.969696970  net_per_second = 1.121739313
depth 19 survivor_lift = 4.222222222  net_per_second = 1.193096775
depth 20 survivor_lift = 8.500000000  net_per_second = 2.401892192
```

Depth 20 is small-count and should not be overread.  The stable reading is that
the prefilter buys roughly a two-depth lift and, on CPU, nets about `1.10x` to
`1.19x` per second at depths 16-19.

## Interpretation

Positive:

```text
p27 practical target plumbing works.
The trace/norm prefilter is p27-compatible in C.
The prefilter has a measured stable-depth per-second signal above break-even.
```

Update:

```text
The cheaper domain-only filter later beat this full-D prefilter on CPU and is
now the first GPU A/B candidate.  See P27 Practical Domain-Line Filter.
```

Negative:

```text
The improvement is modest on CPU.
This is still filtering, not a direct source sampler.
The result needs same-stream GPU confirmation before any large production bet.
```

## Continue / Kill

```text
continue = GPU same-stream A/B: baseline vs trace/norm D prefilter
continue = GPU should also emit domain_line/T_line strata from the Python gate
continue = if GPU preserves or improves the 1.1x-1.2x net lift, consider a larger run

kill = treating the 1M CPU depth-20 spike as stable evidence
kill = launching a huge run without same-stream GPU telemetry
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_practical_sampler_smoke_x16halvestatsnonsplit_10k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_practical_sampler_smoke_x16halvestatsnonsplittraced_10k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_practical_baseline_x16halvestatsnonsplit_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittraced_1M_20260621.txt`

```text
p27_practical_trace_norm_prefilter_smoke_rows=1/1
```
