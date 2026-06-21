# P27 Trace/Norm Variant Benchmark

Date: 2026-06-21

## Claim

The p27 trace/norm `D` prefilter has three C stats variants.  On a bounded
1M-vs-1M comparison, `x16halvestatsnonsplittraced` and
`x16halvestatsnonsplittracechar` are effectively tied; the reconstructed-sqrt
variant is slower.  None changes the survivor distribution relative to the
basic trace/norm prefilter.

This keeps the GPU ask simple:

```text
baseline vs trace/norm D prefilter
```

with `tracechar` acceptable if it is easier to instrument.

## Runs

Prior baseline:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplit
```

Prior trace/norm D:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplittraced
```

New square-character variant:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplittracechar \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittracechar_1M_20260621.txt
```

New reconstructed-sqrt variant:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 \
  1000000 \
  x16halvestatsnonsplittracesqrt \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittracesqrt_1M_20260621.txt
```

## Result

Baseline:

```text
mode = x16halvestatsnonsplit
rate_Mps = 0.154794
survive depth 16 = 238
survive depth 17 = 130
survive depth 18 = 66
survive depth 19 = 36
```

Trace/norm D:

```text
mode = x16halvestatsnonsplittraced
rate_Mps = 0.043741
survive depth 16 = 928
survive depth 17 = 504
survive depth 18 = 262
survive depth 19 = 152
```

Square-character variant:

```text
mode = x16halvestatsnonsplittracechar
rate_Mps = 0.043748
survive depth 16 = 928
survive depth 17 = 504
survive depth 18 = 262
survive depth 19 = 152
square_precheck_plus = 1999752
square_precheck_reject = 1997507
```

Reconstructed-sqrt variant:

```text
mode = x16halvestatsnonsplittracesqrt
rate_Mps = 0.041520
survive depth 16 = 928
survive depth 17 = 504
survive depth 18 = 262
survive depth 19 = 152
```

Net survivor-per-second relative to baseline:

```text
traced:
  depth 16 = 1.101807194
  depth 17 = 1.095523679
  depth 18 = 1.121739313
  depth 19 = 1.193096775

tracechar:
  depth 16 = 1.101983520
  depth 17 = 1.095698998
  depth 18 = 1.121918828
  depth 19 = 1.193287710

tracesqrt:
  depth 16 = 1.045861656
  depth 17 = 1.039897193
  depth 18 = 1.064781698
  depth 19 = 1.132515903
```

Depth 19 still has moderate counts; read this as a stable modest signal, not a
large win.

## Interpretation

Positive:

```text
tracechar is a drop-in equivalent to traced for p27 stats.
Both keep the same ~1.10x to ~1.19x CPU survivor-per-second signal.
```

Negative:

```text
tracesqrt is slower in this CPU implementation.
No variant changes the mathematical selector or creates a stronger line-level
source.
```

## Continue / Kill

```text
continue = GPU same-stream A/B should test baseline vs traced or tracechar
continue = include domain_line/T_line telemetry if cheap

kill = tracesqrt as the preferred CPU-side variant
kill = expecting tracechar to improve the selector; it is instrumentation-equivalent
```

## Linked Artifacts

- [P27 Practical Trace/Norm Prefilter Smoke](p27_practical_trace_norm_prefilter_smoke_20260621.md)
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittracechar_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_prefilter_x16halvestatsnonsplittracesqrt_1M_20260621.txt`

```text
p27_trace_norm_variant_benchmark_rows=1/1
```

