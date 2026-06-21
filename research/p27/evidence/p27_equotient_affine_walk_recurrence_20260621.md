# P27 E-Quotient Affine-Walk Recurrence

Date: 2026-06-21

## Claim

The descended `d4` character is not a high-coverage recurrence of the
descended `d3` character under a small affine walk on the residual elliptic
quotient `E: W^2 = X^3-X`.

```text
tested = d4(P) ?= d3([m]P + Q)
multipliers = +/-1, +/-2, ..., +/-8
translations = every Q in E(F_q)
fields = q=1087,1471,1607
result = no exact or useful high-coverage recurrence
```

If such a recurrence existed, it would be a serious sqrt-beating shape: once
inside the quotient stratum, later all-plus gates could be predicted by a
fixed elliptic walk rather than paid for as fresh half-density filters.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_translation_recurrence_probe.py \
  --small-primes 1087,1471,1607 \
  --multipliers 1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8 \
  --min-coverage 0.75 \
  --limit 12 \
  | tee research/p27/archive/probe_outputs/p27_equotient_translation_recurrence_probe_20260621.txt
```

For each field the probe:

```text
1. enumerates the compactD=-1 label-2 quotient rows,
2. builds d3(P) on all quotient rows,
3. builds d4(P) on d3-positive rows,
4. tests every map P -> [m]P + Q for the listed m and all Q in E(F_q),
5. records coverage and agreement with d3 after either polarity.
```

Promotion would require full or near-full coverage with exact or strongly
non-random agreement.  Low-coverage coincidences are not a sampler.

## Results

`q=1087`:

```text
d3 rows = 72
d4 rows = 40, plus/minus = 20/20
transforms tested = 17408
full coverage transforms = 4
best full coverage = 20/40 = 0.500000000
```

The only full-coverage transforms are `m=+/-1` with `Q=O` or `Q=(0,0)`, and
they are exactly flat.

`q=1471`:

```text
d3 rows = 200
d4 rows = 112, plus/minus = 56/56
transforms tested = 23552
full coverage transforms = 4
best full coverage = 56/112 = 0.500000000
```

Again, only `m=+/-1` with `Q=O` or `Q=(0,0)` have full coverage, and they are
exactly flat.

`q=1607`:

```text
d3 rows = 196
d4 rows = 112, plus/minus = 76/36
transforms tested = 25728
full coverage transforms = 4
best full coverage = 76/112 = 0.678571429
```

The full-coverage transforms are the same identity/negation plus `(0,0)`
torsion variants.  Their `76/112` score is just the raw `d4` plus bias in this
field, not a recurrence.

The best non-full-coverage curiosities in `q=1607` are:

```text
[8]P variants: 24/40 = 0.600000000, coverage = 0.357142857
[4]P variants: 24/24 = 1.000000000, coverage = 0.214285714
```

These do not promote.  They cover too little of the d4 domain and do not
replicate as a high-coverage recurrence.

## Interpretation

Positive:

```text
This is an exact finite-field recurrence screen for a real sqrt-beating shape.
It tests all translations, not just visible torsion shifts.
It covers three non-degenerate validation fields.
```

Negative:

```text
No affine walk [m]P+Q with |m| <= 8 gives an exact d4-from-d3 recurrence.
No nontrivial walk reaches the 0.75 coverage threshold.
Full-coverage maps are only identity/negation and (0,0)-torsion variants.
The q1607 full-coverage lift is raw d4 bias, not a map law.
```

So the quotient route remains alive only as a cover/divisor-class extraction
problem, not as a small elliptic walk recurrence.

## Continue / Kill

```text
continue = symbolic/function-field extraction of the actual E-level f3/f4 covers
continue = exact irreducible-conic or divisor-class screen if made cheaper
continue = online Magma validation for any named candidate formula

kill = affine translation recurrence d4(P)=d3([m]P+Q) for |m|<=8
kill = GPU sampler from small elliptic walks on E
kill = treating low-coverage q1607 [4]P exactness as evidence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_equotient_translation_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_equotient_translation_recurrence_probe_20260621.txt`
- Related: [P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md)
- Related: [P27 E-Quotient Line-Product Screen](p27_equotient_line_product_screen_20260621.md)
- Related: [P27 E-Quotient Low-Pole Random Screen](p27_equotient_lowpole_random_screen_20260621.md)

```text
p27_equotient_affine_walk_recurrence_rows=1/1
```
