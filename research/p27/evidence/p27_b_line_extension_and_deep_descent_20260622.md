# P27 B-Line Extension Counts And Deep Descent

Date: 2026-06-22

## Claim

The B-line quotient is now the live multi-gate moonshot target.  Extension-field
counts show that the legal B-domain stays inside the core B bucket as a
positive-density subset, and deep selected-gate tests show that the original
`Bplus` value determines the active selected gate bits far beyond `d3`.

In the largest p27 train/heldout samples, there are no mixed B groups through
`d18`; through the meaningful-count range `d3..d12`, source-normalized prefix
scaling remains close to independent half-loss.  Across q1607/q1847/q2087,
there are no mixed B groups before the finite-field all-plus population dies.

This is the first B-lane result that can plausibly beat sqrt if converted into
an explicit Kummer/divisor sequence or direct B-line all-plus sampler.

## Artifacts

Probes:

```text
research/p27/archive/gates/p27_b_line_extension_count_probe.py
research/p27/archive/gates/p27_b_line_deep_descent_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_extension_count_probe_q7_degrees1_5_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_extension_count_probe_q23_degrees1_3_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_q1607_q1847_q2087_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_q1607_q1847_q2087_gate12_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_60k_heldout_60k_gate18_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_extension_count_probe.py \
  --q 7 \
  --degrees 1,2,3,4,5 \
  | tee research/p27/archive/probe_outputs/p27_b_line_extension_count_probe_q7_degrees1_5_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_extension_count_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  | tee research/p27/archive/probe_outputs/p27_b_line_extension_count_probe_q23_degrees1_3_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 3000 \
  --p27-heldout-target 3000 \
  --max-draws 1000000 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_q1607_q1847_q2087_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 2000 \
  --p27-heldout-target 2000 \
  --max-draws 800000 \
  --max-gate 12 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_q1607_q1847_q2087_gate12_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_deep_descent_probe.py \
  --small-primes '' \
  --p27-target 60000 \
  --p27-heldout-target 60000 \
  --max-draws 1500000 \
  --max-gate 18 \
  | tee research/p27/archive/probe_outputs/p27_b_line_deep_descent_probe_p27_60k_heldout_60k_gate18_20260622.txt
```

## Extension Counts

The extension probe counts:

```text
core_B: B values satisfying the stable branch-1 core bucket
legal_B: B values realized by legal d2 rows
B_d3_plus/minus: descended d3 signs on legal B
B_d4_plus/minus: descended d4 signs after d3=+1
```

In every nonempty extension field tested:

```text
legal_B_missing_core = 0
B_d3_mixed = 0
B_d4_mixed = 0
```

Representative counts:

```text
GF(7^5), N=16807:
  core_B = 2100
  legal_B = 590
  B_d3_plus / B_d3_minus = 315 / 275
  B_d4_plus / B_d4_minus = 140 / 175
  legal_B/N = 0.035104421
  legal_B/core_B = 0.280952381

GF(23^3), N=12167:
  core_B = 1520
  legal_B = 399
  B_d3_plus / B_d3_minus = 216 / 183
  B_d4_plus / B_d4_minus = 120 / 96
  legal_B/N = 0.032793622
  legal_B/core_B = 0.262500000
```

Interpretation:

```text
The legal B-domain is positive-density, roughly field-sized, not a tiny
subfield or sub-sqrt set.
The value of d3 and d4 is nevertheless well-defined on B.
```

So this does not give a direct below-sqrt sampler by counting alone, but it
does identify the correct quotient on which the multi-gate Kummer sequence
lives.

## Deep Descent

The deep probe groups actual legal rows by original `Bplus` and computes the
selected gate bits `d3, d4, ...` along the all-plus tower.  A mixed group would
mean that B is not enough information for that gate.

No mixed groups occurred in the p27 train/heldout runs through `d12`.

Update: [P27 B-Line 60K Prefix Scaling](p27_b_line_prefix_scaling_60k_20260622.md)
extends the p27 test to `60000 + 60000` source rows and `d18`.  It again finds
zero mixed B groups through the tested depth, but the source-normalized prefix
scaling stays near independent half-loss through meaningful counts:

```text
train, 30000 B groups:
  d3..d12 scaled_half_loss =
  0.9978, 0.9980, 1.0027, 0.9899, 1.0176,
  1.0453, 0.9472, 0.9984, 1.0581, 0.9557

heldout, 30000 B groups:
  d3..d12 scaled_half_loss =
  1.0043, 1.0065, 1.0187, 1.0171, 1.0176,
  1.0453, 0.9856, 1.0240, 0.9387, 1.0581
```

The train tail reaches `1.2288x` at `d13/d14`, but only on `18/9` surviving
B groups and does not transfer to heldout.  Heldout's larger `d15+` values are
single-digit tails.  This kills B prefix counts alone as a source-normalized
sampler while strengthening B as a Kummer-sequence extraction surface.

p27 train, 1000 B groups:

```text
gate3: 496 plus / 504 minus
gate4: 258 plus / 238 minus
gate5: 119 plus / 139 minus
gate6: 66 plus / 53 minus
gate7: 36 plus / 30 minus
gate8: 18 plus / 18 minus
gate9: 8 plus / 10 minus
gate10: 3 plus / 5 minus
gate11: 0 plus / 3 minus
```

p27 heldout, 1000 B groups:

```text
gate3: 526 plus / 474 minus
gate4: 251 plus / 275 minus
gate5: 118 plus / 133 minus
gate6: 62 plus / 56 minus
gate7: 27 plus / 35 minus
gate8: 16 plus / 11 minus
gate9: 8 plus / 8 minus
gate10: 4 plus / 4 minus
gate11: 1 plus / 3 minus
gate12: 1 plus / 0 minus
```

Promotion fields, active groups die but never mix:

```text
q1607:
  gate3 28 plus / 21 minus
  gate4 19 plus / 9 minus
  gate5 19 plus / 0 minus
  gate6 0 plus / 19 minus

q1847:
  gate3 45 plus / 18 minus
  gate4 19 plus / 26 minus
  gate5 0 plus / 19 minus

q2087:
  gate3 25 plus / 32 minus
  gate4 18 plus / 7 minus
  gate5 18 plus / 0 minus
  gate6 18 plus / 0 minus
  gate7 18 plus / 0 minus
  gate8 0 plus / 18 minus
```

## Interpretation

Positive:

```text
The original B coordinate controls a long selected-gate prefix in all tested
data.
The all-plus condition through depth m becomes a subset of P1_B, not a fresh
branching tree over the full source.
This is a plausible path to beat sqrt if the B-line classes can be extracted
or sampled directly.
```

Negative / caution:

```text
Counts still thin by about half per gate among sampled B values.
No explicit Kummer function f_j(B) has been extracted yet.
The finite-field guard fields are small enough that late-gate all-plus tails
die quickly.
```

So the current result is structural, not production-ready.

## Next Tests

First-class CAS target:

```text
Extract the B-line Kummer/divisor sequence f3(B), f4(B), ..., where
chi(f_j(B)) = d_j on the active all-plus domain.
```

Required outputs:

```text
branch divisor / degree for f3
comparison of f4/f3, f5/f4, ... in the Kummer group
genus or sourceability of the all-plus prefix covers on P1_B
```

GPU target, only after exactness plumbing:

```text
emit Bplus and selected gate bits d3..dN for same-stream p27 rows
verify no mixed B buckets at much larger scale
measure all-plus prefix bucket sizes on B
```

This GPU target is now packaged as:
[P27 B-Line Deep-Prefix GPU Telemetry Handoff](p27_b_line_deep_prefix_gpu_telemetry_handoff_20260622.md)
and
`research/p27/archive/fixtures/p27_b_line_deep_prefix_gpu_telemetry_suite_20260622.json`.

Do not run a large GPU hunt merely from this result.  The useful GPU role is
bounded telemetry for B-line exactness, all-plus density, and Kummer-sequence
extraction.

Update: [P27 B-Line Prefix Extension Ladder](p27_b_line_prefix_extension_ladder_20260622.md)
extends this count-only falsifier over `GF(7^n)`, `GF(23^n)`, and `GF(103^n)`.
Legal B still has no core-bucket misses, but the all-plus plateau and hard
stop move with the field:

```text
GF(7^5):  d3,d4,d5 survive, d6 dies
GF(7^6):  d3,d4,d5,d6 survive, d7 dies
GF(23^3): d3..d8 survive, d9 dies
GF(103^2): d3,d4,d5 survive, d6 dies
```

That kills B-prefix counts alone as a transferable below-sqrt sampler while
strengthening the real next ask: extract the Kummer sequence
`f3(B), f4(B), ...` and explain these local plateaus by class/Frobenius data.

## Continue / Kill

```text
continue = B-line Kummer/divisor sequence extraction
continue = recurrence/coupling test among f3,f4,f5,...
continue = bounded GPU telemetry for Bplus plus deep bits

kill = treating B counts alone as below-sqrt sampler
kill = broad visible-factor guessing on B
kill = large production GPU search without extracted B-line classes
```

```text
p27_b_line_extension_and_deep_descent_rows=1/1
```
