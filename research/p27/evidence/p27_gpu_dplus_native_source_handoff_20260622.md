# P27 GPU Dplus-Native Source Handoff

Date: 2026-06-22

## Claim

The next useful GPU task is not a large blind p27 production run.  It is a
bounded exchange-rate test for the one trace/norm structure that still looks
real:

```text
Dplus = exact first-two-selected-gate prefix
observed conditional scope shrink = about 4x
current problem = the classifier pays to inspect rejected raw-y draws
```

The GPU agent should test whether this `4x` scope shrink can be accessed
cheaply, and whether any fused/native implementation exposes later-gate
coupling beyond the first two gates.

This is not claimed to be sqrt-beating by itself.  It becomes relevant to the
sqrt-beating goal only if it either:

```text
1. gives a genuinely cheaper direct source into Dplus plus later gates, or
2. reveals a recurrence/class that controls gates after Dplus.
```

## Evidence To Treat As Baseline

Read these first:

```text
research/p27/evidence/p27_gpu_search_space_narrowing_20260621.md
research/p27/evidence/p27_trace_norm_dplus_prefix_identity_20260621.md
research/p27/evidence/p27_trace_norm_post_dplus_screen_20260621.md
research/p27/evidence/p27_trace_norm_orientation_phase_screen_20260622.md
research/p27/evidence/p27_trace_norm_dplus_cover_20260621.md
research/p27/evidence/p27_trace_norm_source_orientation_cover_20260621.md
research/p27/evidence/p27_trace_norm_dplus_quotient_symmetry_20260622.md
research/p27/evidence/p27_trace_norm_dplus_relative_descent_20260622.md
```

Do not retest these killed routes:

```text
fixed d2/d3/d4 prefix buckets as raw source shrink
low-weight H/VQ/X/T_line/root character products
eps_h/eps_v, H/VQ, eps_h/eps_v/T_line orientation buckets
low-weight tested a/g/m quotient-character products
bare conic quotient a^2+g^2=4 as a standalone Dplus sampler
full genus-69 orientation-cover sampling as the first production plan
seed-order or compact-bucket fishing without a named invariant
```

## Test A: Fused Dplus Prefix Pricing

Goal:

```text
Can Dplus be imposed at lower cost than the ordinary first two selected gates?
```

Implement a same-stream GPU comparison:

```text
baseline = current fastest vanilla X1(16) p27 path
control = current Dplus classifier/precheck path if available
candidate = fused Dplus path that reuses branch/root/halving intermediates
```

The candidate should avoid a fresh independent Legendre toll whenever possible.
It is acceptable if it is only an engineering prototype, but it must report the
same source denominators as baseline.

Report:

```text
raw_y_draws
nonsplit_y
ordinary candidates emitted
Dplus_y
Dplus candidates emitted
depth-20/24/26/28/30 survivors
accepted roots/sec
target survivors/sec at each depth
target survivors per raw_y_draw
kernel time and total wall time
any mismatch against CPU/Python Dplus on replay rows
```

Promotion:

```text
effective survivor/sec at depth >= 26 improves by >= 2x versus baseline
and target/raw_y_draw is not worse than the expected two-gate denominator
```

Excellent:

```text
close to the theoretical 4x conditional scope shrink with tolerable throughput
```

Kill:

```text
the path is slower than just letting the ordinary halving gates fail naturally
or the improvement is only a conditional lift with worse wall-clock throughput
```

## Test B: Direct Dplus Source Prototype

Goal:

```text
Can GPU generate rows already inside Dplus without classifying rejected raw-y?
```

Acceptable prototypes:

```text
sample a named low-genus quotient that maps to Dplus candidates
sample the conic quotient a=t-1/t, g=w/t only after the descended Kummer class
  or branch divisor is named, and only together with the domain-spin cover
do not treat the genus-17 relative cover as a production source unless a
  further quotient/Prym/source map is supplied
sample a partial source that provably covers a fixed Dplus component
sample a fused recurrence source that emits Dplus plus a later selected gate
```

Not acceptable:

```text
enumerating the full genus-69 orientation cover as the first production path
choosing eps_h/eps_v buckets and calling that a source
reporting only conditional survivor rates without raw source accounting
```

Report:

```text
source parameter draws
valid source rows
mapped X1(16) candidates
dedup/collision rate
failure reasons
depth histogram through at least 30
target/source_draw
target/GPU-second
validation replay against ordinary X1(16) verifier path
```

Promotion:

```text
target/source_draw and target/GPU-second both beat baseline with margin
and the source reaches beyond the first two selected gates
```

Kill:

```text
the source pays the same random half-losses as ordinary search
or only implements the known two-gate prefix at higher cost
```

## Test C: Coupling Telemetry While Fused

If Test A is already instrumented, emit cheap later-gate telemetry on the
Dplus-conditioned stream:

```text
d3,d4,d5,... as far as cheap
pairwise and lagged correlations
short sign-word bucket counts
depth-conditioned transition rates
```

Promotion:

```text
a named low-complexity recurrence or state has heldout source-normalized lift
that compounds across gates by >= 1.25x
```

Kill:

```text
post-Dplus signs remain independent half-gates, matching the CPU orientation
and product screens
```

## Required Output

Return one compact report with:

```text
commit hash
exact command lines
GPU model and compile flags
run duration and cost
all denominators listed above
PASS/FAIL replay validation
promote/kill recommendation for each test
logs saved under results/p27/
research note saved under research/p27/evidence/
```

## Continue / Kill

```text
continue = Dplus-native/fused implementation if it improves effective deep
           survivor throughput or exposes later-gate coupling
continue = direct source only if it names the source map and denominator

kill = large p27 production run based only on the existing Dplus classifier
kill = orientation bucket telemetry as a standalone GPU task
kill = fixed-prefix filtering without source-normalized improvement
```

```text
p27_gpu_dplus_native_source_handoff_rows=1/1
```
