# P27 GPU Search-Space Narrowing Probe

Date: 2026-06-21

## Claim

The GPU same-stream tests now distinguish continuation filtering from source
space narrowing for p27.

Fixed selected-gate prefixes `d1..d4` are exact continuation filters and raise
post-prefix survivor rates as expected, but on the raw source denominator they
do not produce a promotable narrowing signal.  The trace/norm `D_plus` gate is
different: in the 1B+1B raw-y GPU confirmation it captured every observed
depth-20 through depth-30 survivor, giving an exact-looking `4x` conditional
stratum among emitted ordinary candidates.  However, the current classifier
still pays to inspect rejected raw-y draws, so this is a structural/source
target, not yet a faster production sampler.

## Code And Runs

Repository:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge
```

GPU:

```text
RunPod RTX 6000 Ada, CUDA 12.1, sm_89
```

Local result folders copied from the pod:

```text
results/p27/gpu_dprefix_depth20_20260621T181138Z
results/p27/gpu_dprefix_depth24_20260621T181356Z
results/p27/gpu_tracenorm_depths_20260621T182506Z
results/p27/gpu_tracenorm_ab_1B_20260621T182614Z
```

The pod was stopped after copying results.  RunPod still showed a stopped
storage cost of `$0.01/hr`; it was not terminated because termination deletes
the stopped pod state.

## Fixed D-Prefix Depth-24 Scope Test

Configuration:

```text
p = 1000000000000000000000000103
target_depth = 24
accepted candidates per mode/seed = 100,000,000
seed modes = identity, splitmix
modes = x16stratumprobe, x16domainprobe, x16ecoverprobe,
        x16d2probe, x16ecoverd2probe,
        x16d3probe, x16ecoverd3probe,
        x16d4probe, x16ecoverd4probe
```

Aggregate source-normalized results across both seed modes:

```text
mode                survivors   source_draws   target/source      lift_vs_raw
x16stratumprobe          194     449020748     4.320513e-7        1.000
x16domainprobe           354     849739094     4.165985e-7        0.964
x16ecoverprobe           380     848412929     4.478951e-7        1.037
x16d2probe               736    1674464228     4.395436e-7        1.017
x16ecoverd2probe         722    1674721981     4.311163e-7        0.998
x16d3probe              1462    3278738530     4.459032e-7        1.032
x16ecoverd3probe        1504    3276302927     4.590540e-7        1.062
x16d4probe              2930    6477950276     4.523036e-7        1.047
x16ecoverd4probe        2982    6474542771     4.605731e-7        1.066
```

Held-out split check:

```text
mode                prefix_rate     held_rate       held/prefix
x16d2probe          3.58e-6         3.78e-6         1.056
x16d3probe          7.44e-6         7.18e-6         0.965
x16d4probe          1.466e-5        1.464e-5        0.999
x16ecoverd2probe    3.94e-6         3.28e-6         0.832
x16ecoverd3probe    7.30e-6         7.74e-6         1.060
x16ecoverd4probe    1.510e-5        1.472e-5        0.975
```

Interpretation:

```text
fixed d-prefix gates = exact continuation shrink
fixed d-prefix gates != observed raw-source shrink
promotion bar 1.25x at depth 24 = not met
bucket restart telemetry = not promoted; prefix-selected buckets did not hold
```

This is the key practical answer for the GPU agent: requiring `d2`, `d3`, or
`d4` before counting a candidate gives the geometric survivor lift one expects,
but it also costs the corresponding geometric raw source factor.  No tested
fixed-prefix source law beats raw by enough to justify a search-space cut.

## Trace/Norm A/B

Configuration:

```text
p = 1000000000000000000000000103
mode = x16tracenormab
raw_y_draws per seed = 1,000,000,000
seed modes = identity, splitmix
```

Aggregate across the 2B raw-y draws:

```text
raw_y_draws = 2,000,000,000
ordinary_emitted_candidates = 1,000,051,462
candidate_emitted_candidates = 249,990,346
candidate/raw_y = 0.124995173
```

Depth results:

```text
depth   ordinary_survive   candidate_survive   conditional_lift   candidate/raw_y
20      15360              15360               4.000              7.680e-6
22       3708               3708               4.000              1.854e-6
24        920                920               4.000              4.600e-7
26        204                204               4.000              1.020e-7
28         52                 52               4.000              2.600e-8
30          8                  8               4.000              4.000e-9
```

The depth-26 row clears the requested `>=100` survivor count bar.  In this run,
all ordinary deep survivors were in the trace/norm candidate stratum.

Interpretation:

```text
trace/norm D_plus = real exact-looking structural stratum
conditional ordinary-candidate shrink = about 4x
raw-y target rate = unchanged by the current filter implementation
production status = needs direct sampler or cheaper algebraic pretest
```

This is a search-space result, not a throughput result.  If a direct source can
sample only the trace/norm `D_plus` stratum without first paying the full raw-y
classification cost, it could cut the ordinary candidate space by about `4x`
with no observed loss through depth 30 in this probe.  As implemented today, it
does not reduce raw GPU work because rejected raw-y draws still have to be
classified.

## Decision

```text
promote as production throughput filter:
  none from fixed d-prefix / ecover-prefix

promote as exact structural narrowing target:
  trace/norm D_plus

next GPU-worthy implementation target:
  direct sampler or cheaper early test for trace/norm D_plus

next math target:
  explain D_plus as a source map / quotient stratum, then test whether that
  stratum recurs or couples to later d_j gates
```

The fixed-prefix family should remain useful telemetry, but it should not be
sold as reducing the 550B raw candidate search by itself.  The trace/norm
family is the one credible search-space narrowing lead from this GPU pass.
