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

Update: [P27 Conic-Pair B/K-Enhanced Pullback Screen](p27_conic_pair_b_enhanced_pullback_20260622.md)
found a useful staging equation,
`m^2*(B^2+s^2-4)=4*s^2*(s^2-4)`, but it does not impose the sparse legal
B-domain.  Treat it as CAS input, not as a direct GPU sampler.
[P27 BSM Surface Incidence Probe](p27_bsm_surface_incidence_20260622.md)
confirms this pricing: the surface is about `q^2`-sized and d3-plus incidence
is still `constant/q`.
[P27 BSM Legal-Restricted Relation Screen](p27_bsm_legal_restricted_relations_20260622.md)
then tests the closest promotion path after imposing legal B.  The target rows
have no extra low-degree relation beyond the inherited BSM equation in
q1607/q1847/q2087, so this remains a CAS/extraction surface rather than a GPU
sampler.

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

### Test 3: B-Line Exact Quartic Support

Run this as a bounded math-structure screen, not as p27 production search:
[P27 B-Line Quartic GPU Test Card](p27_b_line_quartic_gpu_test_card_20260622.md).

Test exact monic quartic support

```text
chi(B^4 + aB^3 + bB^2 + cB + d)
```

for `d3_on_legalB` and `gate4_prefix_on_legalB` over q1847/q2087, with q1607
as implementation smoke.  A stable positive gives a genus-1 B-line source
candidate; a stable negative closes the visible quartic branch-support route.
Use the frozen target packet:

```text
research/p27/archive/fixtures/p27_b_line_quartic_targets_20260622.json
```

### Test 4: K-Line Exact Quartic Support

Run this as the signed-doubling `E'` quotient counterpart to Test 3:
[P27 K-Line Quartic GPU Test Card](p27_kline_quartic_gpu_test_card_20260622.md).

Test exact monic quartic support

```text
chi(K^4 + aK^3 + bK^2 + cK + d)
```

for `d3_on_K` over q1471/q1607/q1847.  A stable q1847 positive is a genus-1
K-line source candidate; a stable negative closes the visible degree-4
K-polynomial source shape.

Use the frozen target packet:

```text
research/p27/archive/fixtures/p27_kline_quartic_targets_20260622.json
```

Coordination note:
[P27 B-Line / K-Line Bridge](p27_b_kline_bridge_20260622.md) proves that the
B-line and K-line targets agree under
`K^2=(B-2)^4/(8B(B+2)^2)` in q1471/q1607/q1847/q2087.  Run the two quartic
screens as coordinate alternatives for one descended class, not as independent
confirmation streams.
[P27 B/K Signed-Root Relation Screen](p27_b_kline_signed_root_relation_20260622.md)
then rules out the nearest shortcut: selecting the signed K root over B is not
an extra low-degree plane relation beyond the bridge cover.
[P27 K-Line Even-Quartic Screen](p27_kline_even_quartic_screen_20260622.md)
also rules out the descended `K^2`-only subfamily
`chi(K^4+a*K^2+b)` over q1471/q1607/q1847.  So the next GPU quartic screen
should test the full signed K-line quartic, not a cheaper even-only proxy.
[P27 K-Line Belyi-Reciprocal Quartic Screen](p27_kline_reciprocal_quartic_screen_20260622.md)
rules out the other natural q^2 shortcut, the Belyi-reciprocal quartics
preserved by `K -> 4/K`.  The remaining K-line GPU test is the full q^3
coefficient-triple search.

## Do Not Run Yet

```text
do not launch a large p27 production GPU search based only on fixed quadratic
gate prechecks

do not promote Bplus/K/Sroot buckets without a new quotient, recurrence, or
direct sampler

do not score broader random buckets unless they are pre-registered from a
named algebraic object

do not spend GPU time on the K-line even-quartic subfamily alone

do not spend GPU time on the K-line Belyi-reciprocal subfamily alone
```

## Continue / Kill

```text
continue = bounded GPU recurrence-coupling telemetry
continue = direct legal-pullback sampler only after a quotient/sampler exists
continue = CAS/math normalization of the d3 legal cover over P1_Sroot or P1_B
continue = full B-line/K-line quartic exact-support GPU screen

kill = production GPU run from the quadratic formula alone
kill = interpreting conditional 2x lift as source shrink
kill = fixed-prefix GPU filters without target/source_draw improvement
kill = short conic sign-word bucket searches without a new invariant
kill = K-line even-quartic-only GPU screen
kill = K-line Belyi-reciprocal-only GPU screen
```

```text
p27_gpu_test_decision_after_quad_rows=1/1
```
