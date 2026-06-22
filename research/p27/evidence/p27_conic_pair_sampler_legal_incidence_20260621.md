# P27 Conic-Pair Sampler Legal Incidence

Date: 2026-06-21

## Claim

The rational conic-pair sampler exactly recognizes the legal d3-plus part in
the tested fields, but the naive two-parameter sampler is not itself a useful
production source.

This is positive structure and a negative raw-GPU-sampler result:

```text
positive = sampler image covers every legal d3-plus (A,x5) class tested
negative = legal hits occur at about constant/q per raw (R,L) draw
```

So the live sqrt-beating route is not "launch GPU over random `(R,L)`".  It is
to compute the legal pullback/quotient of the conic-pair surface, or derive a
recurrence that stays inside the legal curve without paying a fresh search over
the two-dimensional sampler.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_pair_sampler_legal_incidence_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q263_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q607_q1607_20260621.txt
research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q1847_q2087_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_sampler_legal_incidence_probe.py \
  --small-primes 263 \
  --raw-cr-limit 700 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q263_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_sampler_legal_incidence_probe.py \
  --small-primes 607,1607 \
  --raw-cr-limit 700 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q607_q1607_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_conic_pair_sampler_legal_incidence_probe.py \
  --small-primes 1847,2087 \
  --raw-cr-limit 0 \
  | tee research/p27/archive/probe_outputs/p27_conic_pair_sampler_legal_incidence_probe_q1847_q2087_20260621.txt
```

## Sampler

The direct conic-pair sampler uses nonzero `R,L`:

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

It satisfies:

```text
h^2 = r^2 + c*r + 1
g^2 = r^2 - c*r + 1
R^2 - (h + g)*R + 1 = 0
```

This probe projects those outputs to `(A,x)` and compares against enumerated
legal label-2/compactD `(A,x5)` classes and their d3 labels.

## Results

```text
q263:
  legal d3-plus unique (A,x) = 20
  sampler covers d3-plus = 20/20
  sampler covers d3-minus = 0
  sampler d3-plus draw rate = 0.004661733
  q * draw rate = 1.226035779

q607:
  legal d3-plus unique (A,x) = 64
  sampler covers d3-plus = 64/64
  sampler covers d3-minus = 0
  sampler d3-plus draw rate = 0.002788398
  q * draw rate = 1.692557375

q1607:
  legal d3-plus unique (A,x) = 112
  sampler covers d3-plus = 112/112
  sampler covers d3-minus = 0
  sampler d3-plus draw rate = 0.000694779
  q * draw rate = 1.116510471

q1847:
  legal d3-plus unique (A,x) = 180
  sampler covers d3-plus = 180/180
  sampler covers d3-minus = 0
  sampler d3-plus draw rate = 0.000845141
  q * draw rate = 1.560975152

q2087:
  legal d3-plus unique (A,x) = 100
  sampler covers d3-plus = 100/100
  sampler covers d3-minus = 0
  sampler d3-plus draw rate = 0.000367698
  q * draw rate = 0.767385915
```

The coverage pattern is the important structural result:

```text
sampler_unique_d3_plus_A_x / unique_d3_plus_A_x = 1.0 in every tested field
sampler_unique_d3_minus_A_x = 0 in every tested field
```

The draw-rate pattern is the practical warning:

```text
sampler_d3_plus_draw_rate ~ constant/q
```

## Interpretation

The conic-pair surface is the right mathematical object for the next selected
gate.  It is not just a convenient parametrization: on legal rows it separates
d3-plus from d3-minus exactly in all tested guard fields.

But as a GPU source, random `(R,L)` is two-dimensional while the legal
label-2/compactD locus is one-dimensional.  The observed legal hit rate scales
like `1/q`, so at p27 size this would be hopeless without an additional legal
pullback, quotient, or recurrence.

## Updated GPU Guidance

```text
keep = GPU recurrence telemetry for next_gate = chi(r^2+c*r+1)
kill = raw random (R,L) conic-pair production sampler
continue = GPU/CPU test only if it samples the legal pullback, not free (R,L)
continue = CAS/Sage/Magma legal pullback of the conic-pair surface
```

## Next Tests

```text
1. Staged legal pullback:
   solve the label-2/compactD equations together with
   A=2-c^2 and x5=r^2, then add the conic-pair sampler relation.

2. Quotient/source extraction:
   find whether the intersection has genus <= 1 or a named recurrence/walk.

3. Two-step recurrence:
   test whether the legal d4-plus subset is obtained by reusing the same
   conic-pair character after a rational transformation, rather than by a
   fresh independent cover.
```

Update: this test now has a positive answer in
[P27 Conic-Pair D4 Recurrence](p27_conic_pair_d4_recurrence_20260621.md):
`d4 = chi(-(L+a)(L-a)cR)` on the legal conic-pair lift.

## Continue / Kill

```text
continue = conic-pair legal pullback and quotient extraction
continue = d4 recurrence on the legal conic-pair intersection

kill = naive random (R,L) GPU sampler as a sqrt-beating route
kill = claiming source shrink from coverage without accounting for 1/q draw rate
```

```text
p27_conic_pair_sampler_legal_incidence_rows=1/1
```
