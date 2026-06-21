# P27 E-Prime Affine-Walk Recurrence

Date: 2026-06-21

## Claim

After descending from the residual elliptic curve `E` to the 2-isogenous
quotient

```text
E': V^2 = U^3 + 4U,
```

the d4 character is still not a high-coverage recurrence of d3 under a small
affine walk

```text
P -> [m]P + Q.
```

```text
tested = d4(P) ?= +/- d3([m]P + Q) on E'
multipliers = +/-1, +/-2, ..., +/-8
translations = every Q in E'(F_q)
fields = q=1471,1607,1847
result = no exact or useful high-coverage recurrence
```

This is a real sqrt-beating test: a reusable d4-from-d3 walk on `E'` would turn
later tower gates into a structured recurrence instead of fresh half-density
losses.

## Probe

Primary command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_affine_walk_recurrence_probe.py \
  --small-primes 1471,1607 \
  --multipliers 1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8 \
  --min-coverage 0.75 \
  --limit 12 \
  | tee research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_20260621.txt
```

Guard-field follow-up:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_affine_walk_recurrence_probe.py \
  --small-primes 1847 \
  --multipliers 1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8 \
  --min-coverage 0.75 \
  --limit 12 \
  | tee research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_q1847_20260621.txt
```

For each field the probe:

```text
1. enumerates the compactD=-1 label-2 rows,
2. descends d3/d4 through E -> E',
3. enumerates every Q in E'(F_q),
4. tests every P -> [m]P + Q for the listed m,
5. reports both exact-overlap coincidences and high-coverage/full-coverage maps.
```

Low-coverage exact overlaps are reported but not promoted.  A sampler needs
near-full coverage, not a perfect score on a tiny intersection.

## Results

`q=1471`:

```text
E' d3 rows = 100
E' d4 rows = 56, plus/minus = 28/28
transforms tested = 23552
transforms meeting 0.75 coverage = 2
full coverage transforms = 2
best full coverage = 28/56 = 0.500000000
```

The only full-coverage transforms are `m=+/-1`, `Q=O`.  They are exactly flat.
Tiny exact overlaps exist, such as `8/8`, but their coverage is only
`0.142857143`.

`q=1607`:

```text
E' d3 rows = 98
E' d4 rows = 56, plus/minus = 38/18
transforms tested = 25728
transforms meeting 0.75 coverage = 2
full coverage transforms = 2
best full coverage = 38/56 = 0.678571429
```

Again, the only full-coverage transforms are `m=+/-1`, `Q=O`.  The score is
the raw d4 bias in this field, not a map law.  The perfect `12/12` overlap for
`m=+/-4`, `Q=O` covers only `0.214285714` of the d4 rows and does not promote.

`q=1847`:

```text
E' d3 rows = 126
E' d4 rows = 90, plus/minus = 38/52
transforms tested = 29568
transforms meeting 0.75 coverage = 2
full coverage transforms = 2
best full coverage = 52/90 = 0.577777778
```

This third guard field confirms the pattern: only identity/negation have full
coverage, and their score is just the raw d4 majority.

## Interpretation

Positive:

```text
This closes the main recurrence loophole left by the E' quotient descent.
The test is exact over three non-degenerate guard fields.
The reporting separates tiny exact intersections from sampler-relevant coverage.
```

Negative:

```text
No affine walk on E' with |m| <= 8 gives a high-coverage d4-from-d3 recurrence.
No nontrivial transform reaches the 0.75 coverage threshold.
Full-coverage transforms are only identity/negation and score like raw d4 bias.
Tiny exact overlaps are too small to be a source.
```

Thus the `E'` quotient remains useful as a smaller function-field target, but
not as a small elliptic-walk recurrence.  The next credible sqrt-beating test
is exact cover/divisor-class extraction on `E'`, with online Magma reserved for
named small-field formulas or cover checks.

## Continue / Kill

```text
continue = exact E' function-field / divisor-class extraction for d3 and d4
continue = online Magma validation for named formulas on q=1471/q=1607
continue = exact finite-field solver for irreducible conics or divisor classes

kill = affine walk recurrence d4(P)=+/-d3([m]P+Q) on E' for |m|<=8
kill = GPU sampler from small E' walks
kill = promoting low-coverage exact overlaps as recurrence evidence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_eprime_affine_walk_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_eprime_affine_walk_recurrence_probe_q1847_20260621.txt`
- Parent: [P27 E-Quotient Kernel-8 / 2-Isogeny Screen](p27_equotient_kernel8_2isogeny_screen_20260621.md)
- Related: [P27 E-Quotient Affine-Walk Recurrence](p27_equotient_affine_walk_recurrence_20260621.md)
- Related: [P27 E-Prime Low-Pole Random Screen](p27_eprime_lowpole_random_screen_20260621.md)

```text
p27_eprime_affine_walk_recurrence_rows=1/1
```
