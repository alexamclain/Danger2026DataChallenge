# P27 Practical Domain-Line Filter

Date: 2026-06-21

## Claim

The trace/norm `domain_line=+1` condition is the best practical p27 CPU filter
found so far.  It is cheaper than the full trace/norm `D` prefilter and appears
to preserve all observed depth-16+ first-branch halving survivors.

The `T_line` split inside the domain is not stable enough to promote as a
filter.

Follow-up audit: `domain_line=+1` is exactly the sampler's first-halving
square-root gate, because both compute
`F=(y-1)(y^2-2)(y^2-2y+2)`.  This makes the filter a practical constant-factor
win, not a standalone sqrt-beating theorem.  See
[P27 Domain Line Equals First-Halving Gate](p27_domain_first_halving_gate_20260621.md).

## Code

Added C stats modes:

```text
x16halvestatsnonsplittraceline
x16halvestatsnonsplittracedomain
```

Build:

```bash
cc -O3 -o src/pomerance src/pomerance.c
```

## Line-Stratum Telemetry

Runs:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed121_1M_20260621.txt

./src/pomerance 1000000000000000000000000103 \
  122 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed122_1M_20260621.txt

./src/pomerance 1000000000000000000000000103 \
  123 5000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed123_5M_20260621.txt
```

Observed:

```text
seed 121, 1M:
  domain_minus samples = 499948
  domain_minus depth>=16 survivors = 0
  domain_plus depth>=16 survivors = 238

seed 122, 1M:
  domain_minus samples = 499084
  domain_minus depth>=16 survivors = 0
  domain_plus depth>=16 survivors = 210

seed 123, 5M:
  domain_minus samples = 2502308
  domain_minus depth>=16 survivors = 0
  domain_plus depth>=16 survivors = 1182
```

The `T_line` split is balanced and not stable:

```text
seed 121, depth>=18:
  Tline_minus = 24
  Tline_plus  = 42

seed 122, depth>=18:
  Tline_minus = 28
  Tline_plus  = 44

seed 123, depth>=18:
  Tline_minus = 168
  Tline_plus  = 150
```

## Domain-Only Filter

Runs:

```bash
./src/pomerance 1000000000000000000000000103 \
  121 1000000 x16halvestatsnonsplittracedomain \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_domain_filter_seed121_1M_20260621.txt

./src/pomerance 1000000000000000000000000103 \
  122 1000000 x16halvestatsnonsplittracedomain \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_domain_filter_seed122_1M_20260621.txt
```

Seed `121`:

```text
baseline rate_Mps = 0.154794
domain-filter rate_Mps = 0.104499
rate_ratio = 0.675088

depth 16 survivor_lift = 466/238 = 1.957983  net_per_second ~= 1.322
depth 17 survivor_lift = 256/130 = 1.969231  net_per_second ~= 1.329
depth 18 survivor_lift = 134/66  = 2.030303  net_per_second ~= 1.371
depth 19 survivor_lift = 74/36   = 2.055556  net_per_second ~= 1.388
```

Seed `122`:

```text
baseline rate_Mps = 0.175378
domain-filter rate_Mps = 0.104347
rate_ratio = 0.595002

depth 16 survivor_lift = 456/210 = 2.171429  net_per_second ~= 1.292
depth 17 survivor_lift = 238/114 = 2.087719  net_per_second ~= 1.242
depth 18 survivor_lift = 128/72  = 1.777778  net_per_second ~= 1.058
depth 19 survivor_lift = 60/32   = 1.875000  net_per_second ~= 1.116
```

This beats the earlier full `D` prefilter CPU result, which was about
`1.10x` to `1.19x` net per second at stable depths on seed `121`.

## Interpretation

Positive:

```text
domain_line=+1 is a strong practical gate for depth>=16 on the measured p27
streams.
The domain-only filter is cheaper than the full D prefilter and gives a
stronger CPU net survivor-per-second signal.
This is now the first GPU A/B candidate.
```

Negative:

```text
This is the first-halving gate itself, so the roughly 2x survivor lift is
expected rather than mysterious.
This is a constant-factor improvement, not a sub-sqrt theorem.
T_line is not promoted as a filter.
```

## Continue / Kill

```text
continue = GPU same-stream A/B: baseline vs domain-line filter
continue = ask whether the quotient/Hilbert-90 structure predicts the next
           post-domain halving gate
continue = keep full D prefilter as secondary, not first, GPU candidate

kill = T_line as a production filter from current CPU evidence
kill = full D prefilter as the first GPU test if domain-only is available
kill = treating domain-line by itself as the moonshot
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_smoke_10k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed121_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed122_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed123_5M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_domain_filter_smoke_10k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_domain_filter_seed121_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_domain_filter_seed122_1M_20260621.txt`

```text
p27_practical_domain_filter_rows=1/1
```
