# P27 S-Map Quartic Recurrence Probe

Date: 2026-06-21

## Claim

The `r+2` Kummer class has an exact two-gate recurrence model, but the first
named factors from that model do not give a cheap selector.

After the reciprocal quotient screen, write:

```text
r = x_next + 1/x_next = S^2 - 2.
```

Then the all-plus reverse-doubling map is:

```text
x_prev = S^2*(S^2 - 4) / (4*(S^2 + A - 2)).
```

Composing one more selected all-plus gate gives a quartic in
`Y = S_next^2`:

```text
F(Y) =
  Y^4
  - 4*S2*Y^3
  + (-4*A*S2 + 8*A + 24*S2 - 16)*Y^2
  + (16*A*S2 - 32*S2)*Y
  + 16*(A - 2)^2
```

where `S2 = S^2`.

This is real structure: over the tested guard fields, every d3-plus row has
four `Y` roots, and either all four are squares or none are.  The `d4` bit is
exactly this common root squareclass.

The negative result is that the obvious named squareclasses from the quartic
do not predict that root squareclass on heldout p27 samples.

## Artifacts

Direct all-plus S-cover Magma smoke:

```text
research/p27/archive/fixtures/p27_eprime_d3_scover_after_firsthalf_saturation_q7_magma.m
research/p27/archive/probe_outputs/p27_eprime_d3_scover_after_firsthalf_saturation_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_d3_scover_after_firsthalf_saturation_q7_magma_20260621.html
```

Quartic recurrence probe:

```text
research/p27/archive/gates/p27_smap_quartic_recurrence_probe.py
research/p27/archive/probe_outputs/p27_smap_quartic_recurrence_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_smap_quartic_recurrence_probe.py \
  --target 12000 \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_smap_quartic_recurrence_probe_20260621.txt
```

## Magma S-Cover Smoke

The direct selector cover `S^2 = r+2` reaches a dimension-1 staged curve, but
online Magma cannot normalize it:

```text
AFTER_FIRSTHALF_SAT 2 61 0
D3_SCOVER_AFTER_FIRSTHALF_SCHEME 1 62 0
System Error: User memory limit has been reached
RESULT p27_eprime_d3_scover_after_firsthalf_saturation_q7 done
```

So the S-cover is the right object, but not a web-calculator genus computation.

## Symbolic Structure

The one-step quotient map is:

```text
f_A(S) = S^2*(S^2 - 4) / (4*(S^2 + A - 2)).
```

The quartic discriminant is a square up to known degenerate divisors:

```text
disc_Y(F) =
65536*S^4*(A-2)^2*(A+2)^2*(S-2)^2*(S+2)^2*(A+S^2-2)^2.
```

The nearest quadratic factor split has discriminant:

```text
16*S^2*(S^2 + A - 6).
```

This made `chi(S^2 + A - 6)` the first natural selector candidate.

## Results

On p27 train/heldout:

```text
p27 train:
  rows after d3 plus = 6048
  d4 plus/minus = 3032/3016
  chi(S^2+A-6) plus/minus = 3046/3002
  split matches d4 = 3082/6048 = 0.5096

p27 heldout:
  rows after d3 plus = 6088
  d4 plus/minus = 2986/3102
  chi(S^2+A-6) plus/minus = 2934/3154
  split matches d4 = 2988/6088 = 0.4908
```

The named quartic-factor GF(2) span is also negative:

```text
features =
  S2, S2-4, S2+4, A-2, A+2, A+S2-2, A+S2-6,
  A*S2-2A-2S2, quartic_c2, quartic_c1

exact_train_combos = 0
best train = 3144/6048 = 0.5198
heldout for same best combos = 2982/6088 = 0.4898
```

Guard fields show the exact root-squareclass structure:

```text
q1607:
  rows = 448
  roots_4 = 448
  square_y_roots_4 / square_y_roots_0 = 304/144
  root_squareclass_matches_d4 = 448

q1847:
  rows = 720
  roots_4 = 720
  square_y_roots_4 / square_y_roots_0 = 304/416
  root_squareclass_matches_d4 = 720

q2087:
  rows = 400
  roots_4 = 400
  square_y_roots_4 / square_y_roots_0 = 288/112
  root_squareclass_matches_d4 = 400
```

## Interpretation

Positive:

```text
The d4 bit after d3 is not an unnamed black box anymore.
It is the common squareclass of the four roots of an explicit quartic F(Y).
The quartic has square discriminant and a structured two-quadratic splitting
over sqrt(S^2 + A - 6).
```

Negative:

```text
The first split class chi(S^2 + A - 6) is flat.
The natural named factor span from F(Y) has no exact train combo and collapses
on heldout.
The direct S-cover still exceeds online Magma normalization limits.
```

This is not a production sampler yet.  It is a sharper theorem/CAS target:

```text
identify the common root squareclass of F(Y)
```

as a theta/resolvent/Kummer class, or show that it is a fresh generic cover at
each stage.

## Continue / Kill

```text
continue = derive a resolvent/theta formula for the common root squareclass
continue = ask CAS/expert for the Kummer class of roots of F(Y)
continue = compare the next-stage quartic class to this one for recurrence

kill = chi(S^2 + A - 6) as d4 selector
kill = named quartic coefficient/factor GF(2) span as d4 selector
kill = online Magma Curve(S) normalization for the direct S-cover
```

```text
p27_smap_quartic_recurrence_rows=1/1
```
