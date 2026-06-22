# P27 GPU Conic-Chain Test Handoff

Date: 2026-06-21

## Decision

Yes: p27 is ready for a bounded GPU structure test.

Do not start with a giant p27 production hunt from this lead alone.  The
specific GPU question is whether the conic-chain recurrence can be used as a
source or cheap multi-gate telemetry, not whether raw throughput can brute
force the target.

## Target

```text
p = 1000000000000000000000000103
sqrt_floor(p) = 31622776601683
k = 45
p mod 8 = 7
```

No p27 hit is known yet.

## Source Evidence

Use these p27 evidence notes as inputs:

```text
research/p27/evidence/p27_quadratic_gate_recurrence_20260621.md
research/p27/evidence/p27_conic_chain_source_screen_20260621.md
research/p27/evidence/p27_gpu_search_space_narrowing_20260621.md
research/p27/evidence/p27_gpu_uprecheck_probe_20260621.md
research/p27/evidence/p27_conic_pair_invariant_relation_20260621.md
```

The recurrence is exact in the tested p27 tower:

```text
A = 2 - c^2
x_j = r_j^2
next_gate = chi(r_j^2 + c*r_j + 1)
```

Legal halving needs both conjugate conics:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

On p27 train/heldout gates 3-8 and q1607/q1847/q2087 guards, the recurrence
has zero known mismatches.  On legal label-2/compactD rows over
q1607/q1847/q2087, depth-1 conic lifts match exactly the d3-plus rows, and
depth-2 lifts match exactly d4-plus after d3.

## Direct One-Step Sampler

The one-step legal conic pair has a two-parameter rational sampler.  Pick
nonzero `R` and `L`, where `R` is the next `r` value.  Define:

```text
a = R - 1/R
s = R + 1/R
d = (L - a^2/L)/2
r = -(L + a^2/L)/4
h = (s + d)/2
g = (s - d)/2
c = s*d/(2*r)
A = 2 - c^2
x = r^2
```

Then, away from the usual zero-denominator degeneracies:

```text
h^2 = r^2 + c*r + 1
g^2 = r^2 - c*r + 1
R^2 - (h + g)*R + 1 = 0
```

I validated these identities with 10,000 random `(R,L)` pairs over each of
q1607, q1847, q2087, and the actual p27 field; all trials matched.

Durable probe:

```text
research/p27/archive/gates/p27_conic_pair_sampler_identity_probe.py
research/p27/archive/probe_outputs/p27_conic_pair_sampler_identity_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_sampler_identity_probe.py \
  --trials 10000 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_sampler_identity_probe_20260621.txt
```

## GPU Experiment A: Recurrence Telemetry

Instrument the existing p27 GPU halving path to report, for selected rows
reaching the label-2/compactD region:

```text
c
r_j
actual next x-square gate
formula gate = chi(r_j^2 + c*r_j + 1)
branch/sign mismatch count
d3, d4, d5, d6 if cheap
```

Expected result:

```text
formula mismatch count = 0
```

This experiment is mostly a GPU implementation check.  It should be small:
use same-stream telemetry, not a production cap.

## GPU Experiment B: Legal Pullback Source Probe

The direct free `(R,L) -> (c,r,h,g,A,x)` sampler is now screened:
[P27 Conic-Pair Sampler Legal Incidence](p27_conic_pair_sampler_legal_incidence_20260621.md).
It covers every legal d3-plus `(A,x5)` class tested and no d3-minus classes,
but legal hits occur at about `constant/q` per random `(R,L)` draw.  Therefore
do not benchmark a raw random `(R,L)` production sampler as if it were already
a win.

The useful GPU/CPU experiment is narrower: test a legal pullback source, if
one is implemented, that samples the conic-pair intersection with the
label-2/compactD locus rather than sampling free two-dimensional `(R,L)`.

The d4 selector on that legal pullback is now explicit:
[P27 Conic-Pair D4 Recurrence](p27_conic_pair_d4_recurrence_20260621.md).
With `a=R-1/R` and `L=h-g-2r`,

```text
d4 = chi(-(L+a)(L-a)cR).
```

GPU should report this selector only if the legal conic-pair variables are
already available.  It is not a reason to run free random `(R,L)`.

The d5 tower screen shows the same selector repeats one level later:
[P27 Conic-Pair D5 Tower](p27_conic_pair_d5_tower_20260621.md).  GPU should
treat this as tower telemetry or legal-pullback work, not as a production
source until a legal tower sampler exists.

The legal source depth screen is also explicit now:
[P27 Legal Conic Tower Depth](p27_legal_conic_tower_depth_20260621.md).
On p27 train/heldout samples, the legal tower still thins roughly like
successive selected half-gates through depth 4.  GPU should therefore look for
a quotient/legal tower sampler, not just evaluate the original legal source
with more depth gates.

The raw `(R,L)` low-degree quotient screen is negative:
[P27 Conic-Pair Low-Degree Relation Screen](p27_conic_pair_lowdegree_relation_20260621.md).
Do not ask GPU to search random `(R,L)` or low-degree raw plane-curve buckets.
The remaining GPU-relevant target is a quotient/source in the repeated Kummer
tower variables.

The obvious invariant-coordinate quotient screen is also negative:
[P27 Conic-Pair Invariant Relation Screen](p27_conic_pair_invariant_relation_20260621.md).
Do not spend GPU time on bucket searches in simple symmetric pairs like
`(R+1/R,L+a^2/L)`, `((R-1/R)^2,L+a^2/L)`, `(R+1/R,(L+a)(L-a))`,
or `(c,r)`.  q1847/q2087 show no extra low-degree relation through degree 20,
and the only q1607 degree-20 artifact failed to repeat.

Report:

```text
source draws/sec
nondegenerate legal-pullback outputs/sec
rows accepted by the existing legal verifier/path
d3/d4/d5 survivor rates from sampler outputs
same metrics for the ordinary raw X1(16) baseline
effective deep survivors/sec
```

Promotion bar:

```text
>= 1.25x effective deep survivors/sec on heldout seeds,
or a direct source into a named legal stratum that avoids a fresh 1/2 loss.
```

Kill condition:

```text
legal pullback is not implemented,
raw free (R,L) is the only source,
or the legal pullback costs erase the sourced conic gate.
```

## GPU Experiment C: Two-Step Chain Pressure

If Experiment B maps to legal rows, extend the telemetry one step:

```text
same c across two transitions
r0 -> r1 -> r2
both conjugate conic pairs present at each transition
actual d3 and d4 match chain lift indicators
```

Report whether the second step behaves like:

```text
fresh independent half-loss
```

or like:

```text
same low-dimensional chain source controlling multiple gates
```

This is the first GPU test that could point toward beating `sqrt(p)` rather
than merely improving a constant factor.

## Non-Goals

```text
do not run a large blind p27 production search from this handoff
do not run raw random `(R,L)` as a production sampler
do not retest fixed d2/d3/d4 prefixes as if they already shrink raw source scope
do not promote independent u+2 Legendre prechecks; that GPU result is negative
do not treat trace/norm D_plus as production until there is a direct sampler
```

## Required Report Back

For every run, report:

```text
code commit or source hash
exact command
GPU model
seed base / seed offset / cap
candidate stream definition
raw source draws
accepted or legal rows
candidate rate
accepted/legal row rate
deep survivor rates by depth
effective deep survivors/sec
mismatch counts
full log path
```

## Continue / Kill

```text
continue = formula telemetry has zero mismatches on GPU
continue = direct pair sampler reaches legal rows with useful effective rate
continue = two-step chain shows coupled gates rather than fresh half-loss

kill = direct pair sampler is only a different parametrization with no legal
       pullback advantage
kill = legal pullback requires the same independent Legendre/sqrt tolls as
       ordinary halving
kill = any nondegenerate recurrence mismatch appears in same-stream telemetry
```

```text
p27_gpu_conic_chain_test_handoff_rows=1/1
```
