# P27 B-Line No-R Beta_U F4 Pair Probe

Date: 2026-06-22

## Claim

The beta_U next-gate obstruction remains fresh even at the finer x6-pair
level.

For every gamma-positive beta_U point, the probe checks:

```text
Unext = x6 + 1/x6     gives two reciprocal x6 roots,
each x6                gives two x7 halves,
f4                     is chi(x7).
```

The only exact structure found is the expected pair norm:

```text
x7_plus * x7_minus = -4 * (A*x6 + 1)
```

with zero formula or squareclass mismatches.  This tells us when the two x7
halves over a fixed x6 are same-sign or mixed.  It does not select the sign,
and the reciprocal x6-pair product patterns are not fixed.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_f4_pair_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_f4_pair_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_f4_pair_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_f4_pair_probe_20260622.txt
```

## Result

Fields:

```text
71^2, 167^2, 199^2, 263^2, 311^2
```

Setup checks:

```text
bad_curve_a = 0
x7_pair_product_formula_mismatch = 0
x7_pair_product_chi_mismatch = 0
```

Gamma-positive beta_U counts:

```text
field    beta_U gamma+ points    x6 pairs    x7 roots
71^2     128                    256         512
167^2    96                     192         384
199^2    256                    512         1024
263^2    192                    384         768
311^2    256                    512         1024
```

The four f4 signs over each gamma-positive beta_U point are genuinely mixed:

```text
field    dominant beta-point f4 patterns
71^2     p2_m2=60, p3_m1=36, p1_m3=18, p4=8, m4=6
167^2    p2_m2=48, p1_m3=18, p3_m1=14, p4=10, m4=6
199^2    p2_m2=100, p3_m1=70, p1_m3=64, m4=18, p4=4
263^2    p2_m2=66, p3_m1=52, p1_m3=40, m4=20, p4=14
311^2    p2_m2=86, p3_m1=76, p1_m3=56, p4=20, m4=18
```

At the x6-pair level, mixed and same-sign pairs both occur:

```text
field    mixed pairs    same-plus pairs    same-minus pairs
71^2     138            70                 48
167^2    100            48                 44
199^2    262            114                136
263^2    176            104                104
311^2    240            148                124
```

The reciprocal x6 pair products are also not fixed:

```text
field    product pattern summary
71^2     (-1,-1)=42, (1,1)=32, mixed orientations 54 total
167^2    (-1,-1)=34, (1,1)=30, mixed orientations 32 total
199^2    (-1,-1)=64, (1,1)=58, mixed orientations 134 total
263^2    (1,1)=58, (-1,-1)=42, mixed orientations 92 total
311^2    (1,1)=70, (-1,-1)=54, mixed orientations 132 total
```

## Interpretation

Positive:

```text
The pair norm is exact and should be part of any CAS model of f4 over beta_U:
x7_plus*x7_minus = -4*(A*x6+1).
```

Negative:

```text
The pair norm is the ordinary quadratic-halving norm, not a new sampler.
It only tells whether a two-root pair is same-sign or mixed.
It does not decide same-plus versus same-minus.
The reciprocal x6 pairs do not have a fixed product pattern.
No beta_U f4 pair bucket is promotable to GPU production.
```

## CAS Consequence

The beta_U/f4 comparison should now include the branch norm

```text
A*x6 + 1
```

as known orientation data, analogous to the B-line materialization layer.
Promote only if normalization finds that the remaining same-plus/same-minus
choice is a pullback, coboundary, quotient/Prym factor, or recurrence.  If the
remaining choice is fresh on every useful quotient, beta_U is a clean f3 class
but not a sqrt-beating multi-gate source.

## Continue / Kill

```text
continue = include x7-pair norm -4*(A*x6+1) in beta_U CAS handoff
continue = compare remaining same-sign choice after beta_U normalization
continue = treat beta_U as f3/materialization unless CAS couples f4

kill = x6-pair product as a production sampler
kill = reciprocal x6-pair product pattern as a stable source law
kill = GPU beta_U f4 pair buckets
```

```text
p27_b_line_noR_betaU_f4_pair_rows=1/1
```
