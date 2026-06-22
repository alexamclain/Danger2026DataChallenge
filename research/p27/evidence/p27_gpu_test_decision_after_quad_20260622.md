# P27 GPU Test Decision After Quadratic Probe

Date: 2026-06-22

## Claim

The bounded GPU quadratic-gate probe was the right test to run, and its result
is decisive for the next step:

```text
yes = GPU for bounded telemetry on recurrence coupling or a direct legal source
no  = large production GPU run from the quadratic gate/filter alone
```

The recurrence formula is real and GPU-validated, but it currently recovers
only a conditional half-loss.  It does not yet shrink the source-normalized
search space.

## Evidence

Prior evidence:

```text
research/p27/evidence/p27_kline_a_map_and_gpu_quad_20260622.md
```

External GPU result:

```text
repo = alexamclain/Danger2026DataChallenge
branch = codex/add-cuda-p26-search
commit = e153fd1 Add p27 quadratic gate GPU probe
result = results/p27/gpu_quad_20260622T005716Z/README.md
```

Headline:

```text
checked gates = 7,874,715
gates = 3..8
mismatches = 0
formula = next_gate = chi(r^2 + c*r + 1), with A = 2 - c^2 and x = r^2
```

The recurrence-coordinate domain is about half of the wider post-d2 prefix
scope, and the conditional survivor rate is about doubled.  But
`target/source_draw` is flat or slightly lower, so the current implementation
does not beat the source-space denominator.

Update: [P27 Conic Sign-Word Coupling Probe](p27_conic_signword_coupling_20260622.md)
ran the CPU-side bounded version of Test 1.  On `4000 + 4000` p27
train/heldout unique `(A,x5)` rows, all-plus conic prefixes thin like
independent half-gates through meaningful counts; small-field plateaus do not
transfer stably.  This lowers the priority of GPU sign-word bucket hunting
unless the GPU run is explicitly a much larger confirmation with the same
source-normalized accounting.

## Interpretation

The GPU has validated a mathematical coordinate system, not a production
shortcut.  The asset is the exact repeated gate:

```text
s_j = chi(r_j^2 + c*r_j + 1)
```

A one-bit test of `s_j=+1` is expected to lose one half of the source and then
recover about one factor of two conditionally.  That is not enough.  A win must
come from either:

```text
1. sampling directly inside the legal recurrence-coordinate domain, or
2. finding coupling among many s_j bits so the tower is not independent.
```

## Next GPU Tests

### Test 1: Recurrence-Coupling Telemetry

Run same-stream p27 telemetry that emits the sign vector

```text
s_j = chi(r_j^2 + c*r_j + 1)
```

for as many consecutive gates as the native code can expose cheaply, starting
with gates `3..12` or `3..16`.

Report:

```text
raw source draws
valid recurrence-domain rows
per-gate plus/minus counts
prefix survivor counts
pairwise and lagged correlations among s_j
hash/bucket counts for short sign words
target survivors per raw source draw
throughput per GPU-second
```

Promotion bar:

```text
some low-complexity word, recurrence, bucket, or state has held-out lift that
compounds across gates and improves target/source_draw by >= 1.25x
```

Kill condition:

```text
sign words behave like independent half-gates after source normalization
```

### Test 2: Direct Legal-Pullback Sampler

Only run this after the math side provides an actual sampler or quotient map
for the legal recurrence-domain cover.  The GPU should compare that sampler to
baseline on the same target-depth accounting.

Report:

```text
source draws attempted
legal rows emitted
candidate rows reaching each depth
target/source_draw
target/GPU-second
failure reasons for rejected draws
```

Promotion bar:

```text
legal emitted rows are cheap enough that target/GPU-second and
target/source_draw both beat baseline with margin
```

Kill condition:

```text
the sampler pays the same denominator as the original source or only produces
a constant-factor conditional lift
```

## Do Not Run Yet

```text
do not launch a large p27 production GPU search based only on fixed quadratic
gate prechecks

do not promote Bplus/K/Sroot buckets without a new quotient, recurrence, or
direct sampler

do not score broader random buckets unless they are pre-registered from a
named algebraic object
```

## Continue / Kill

```text
continue = bounded GPU recurrence-coupling telemetry
continue = direct legal-pullback sampler only after a quotient/sampler exists
continue = CAS/math normalization of the d3 legal cover over P1_Sroot or P1_B

kill = production GPU run from the quadratic formula alone
kill = interpreting conditional 2x lift as source shrink
kill = fixed-prefix GPU filters without target/source_draw improvement
kill = short conic sign-word bucket searches without a new invariant
```

```text
p27_gpu_test_decision_after_quad_rows=1/1
```
