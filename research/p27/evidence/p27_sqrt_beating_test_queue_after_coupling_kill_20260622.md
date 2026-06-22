# P27 Sqrt-Beating Test Queue After Coupling Kill

Date: 2026-06-22

## Claim

After the GPU recurrence-coupling kill, there are only two live ways to beat
sqrt-scale search for:

```text
p = 1000000000000000000000000103
sqrt_floor = 31622776601683
```

They are:

```text
1. find a sourceable/recurrent A-level Kummer class sequence controlling
   d3,d4,d5,... with less than independent half-loss;
2. make Dplus a cheaper native source and then couple it to a later selected
   gate through the same A-level class surface.
```

Everything else is now support work.  Fixed sign-word buckets, gamma buckets,
visible low-degree A/B/K fits, and standalone H90 payload signs have all failed
source-normalized promotion.

Machine-readable queue:

```text
research/p27/archive/fixtures/p27_sqrt_beating_test_queue_after_coupling_kill_20260622.json
```

## Test 1: A-Level Kummer Sequence Extraction

Question:

```text
Are the selected A-level classes d3,d4,d5,... pullbacks, translates,
coboundaries, iterates, or fresh independent half-covers?
```

Inputs:

```text
research/p27/evidence/p27_a_level_kummer_extraction_packet_20260622.md
research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json
research/p27/evidence/p27_b_a_fixture_bridge_20260622.md
research/p27/evidence/p27_trace_norm_dplus_a_descent_20260622.md
```

Required outputs:

```text
normalized A-level cover carrying d3
branch divisor degree and support field degrees
genus/component count after obvious quotients
d4 class on the d3-plus prefix
first explicit relation or obstruction among d3,d4,d5,d6
```

Promote:

```text
low-genus/sourceable class, or one named correspondence controlling multiple
selected gates with source-normalized denominator better than independent
half-loss
```

Kill:

```text
d3 is high/generic after quotienting, and d4/d5/d6 are fresh independent
Kummer layers
```

## Test 2: Gamma4/Gamma5 Repeated-Kummer Comparison

Question:

```text
Does the repeated transition F_A(U,V), gamma^2=V+2 produce a reusable Kummer
class, or does it add a fresh half-cover at each layer?
```

Inputs:

```text
research/p27/evidence/p27_abk_symbolic_kummer_cas_brief_20260622.md
research/p27/evidence/p27_abk_gamma4_gamma5_cas_fixture_20260622.md
research/p27/archive/fixtures/p27_abk_gamma4_gamma5_localized_noR_q7_magma.m
```

Required outputs:

```text
normalize selected components of the localized no-R chart
compare div(V+2) and div(Wnext+2) modulo squares
decide whether gamma5/gamma4 is a square, pullback, translate, coboundary, or norm
```

Promote:

```text
gamma4 and gamma5 become related on a low-genus/sourceable quotient, or the
relation yields a direct selected-chain sampler
```

Kill:

```text
gamma4 and gamma5 are unrelated fresh Kummer layers, or the only positive is a
sign-word bucket already killed at GPU scale
```

## Test 3: Dplus Fused/Native Exchange Rate

Question:

```text
Can Dplus be imposed cheaper than letting the ordinary first two selected
halving gates fail naturally?
```

Inputs:

```text
research/p27/evidence/p27_gpu_dplus_native_source_handoff_20260622.md
research/p27/evidence/p27_trace_norm_dplus_prefix_identity_20260621.md
research/p27/evidence/p27_trace_norm_post_dplus_screen_20260621.md
```

Required GPU outputs:

```text
baseline ordinary raw_y_draws/sec and accepted roots/sec
fused/native Dplus raw_y_draws/sec and accepted roots/sec
depth-20/24/26/28/30 survivors
target/source_draw
target/sec
validation replay mismatch count
```

Promote as engineering:

```text
effective survivor/sec at depth >= 26 improves by at least 2x versus baseline,
with target/source_draw no worse than the known two-gate denominator
```

Promote as math only if:

```text
the fused stream also exposes a later-gate source/recurrent class, not merely
the known two-gate Dplus prefix
```

Kill:

```text
the fused path is slower than ordinary halving, or the apparent win is only
conditional enrichment paid back by classifier cost
```

## Test 4: Dplus-To-A Bridge Reconstruction

Question:

```text
Can the Dplus H90/quotient coordinates map cheaply to the A-line coordinate
that carries post-Dplus d3/d4?
```

Status update:
[P27 Trace/Norm Dplus A-Coordinate Bridge](p27_trace_norm_dplus_a_coordinate_bridge_20260622.md)
solves the coordinate part of this test.  On same-stream `Dplus` rows,

```text
A = (t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1)/(4*t^4)
A = (t - 1/t)^4/4 - 2
```

matches the candidate A exactly, and both candidate roots for one `y` share
the same A.  Therefore the remaining bridge test is not to find `A`; it is to
compare the pulled-back A-level `d3` Kummer class with the H90 second-layer
payload `A_eta = U_eta + z*W_eta`.

Second update:
[P27 Trace/Norm Dplus X6/U-Class](p27_trace_norm_dplus_x6_uclass_20260622.md)
sharpens the pulled-back `d3` class.  After `Dplus`, each y has four
reciprocal-reduced `U=x6+1/x6` values and eight `x6` values; `chi(U+A)=+1`
on every tested branch, so:

```text
d3 = chi(x6)
```

on the whole second-halving sheet.  The live comparison is therefore between
the `x6` squareclass and the H90 payload `A_eta`, not a generic d3 sign.

This is the most concrete bridge test after the coupling kill.  We know:

```text
Dplus has a real H90/quotient model;
post-Dplus d3/d4 descend to whole A fibers;
H90 payload signs alone do not predict d3/d4.
```

The missing object is the map or obstruction between the H90 model and the
A-level Kummer class surface.

Required same-stream rows:

```text
y
Dplus bit
t,w,z or enough trace/norm/H90 coordinates to recover them
eta
A
x5 or xp
d3,d4,d5,... as cheap
root/sheet ids needed for replay
```

Required analysis:

```text
use the exact map A = (t - 1/t)^4/4 - 2
use d3 = chi(x6) after U=x6+1/x6 and chi(U+A)=+1
compare the x6 squareclass with A_eta = U_eta + z*W_eta
record whether the pulled-back A-level d3 class equals, differs by coboundary,
or shares a quotient/Prym factor with the H90 class
```

Promote:

```text
a quotient/Prym/coboundary relation between A_eta and the pulled-back A-level
d3 class, or a sourceable recurrence controlling later gates
```

Kill:

```text
the pulled-back A-level d3 class is independent of the H90 payload except
through ordinary candidate materialization
```

## Priority

```text
1. A-level Kummer extraction is the mathematical mainline.
2. Dplus fused/native pricing is the only immediate GPU implementation ask.
3. Dplus-to-A coordinate reconstruction is solved; the next cross-lane task is
   class comparison between pulled-back A-level d3 and H90 A_eta.
4. Gamma4/Gamma5 is offline CAS only until it names a quotient/source.
```

## Continue / Kill

```text
continue = normalized A-level Kummer extraction
continue = offline CAS comparison of gamma4/gamma5
continue = fused/native Dplus pricing with A/d3 telemetry columns
continue = Dplus/H90 A_eta versus pulled-back A-level d3 class comparison

kill = more sign-word/gamma bucket GPU scans
kill = standalone H90 payload sign screens
kill = searching for another low-degree Dplus-to-A coordinate map
kill = visible low-degree A/B/K formula fishing without a divisor reason
kill = large p27 production run based only on the current Dplus classifier
```

```text
p27_sqrt_beating_test_queue_after_coupling_kill_rows=1/1
```
