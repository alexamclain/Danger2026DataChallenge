# P27 B-Line Reduced-Lift Classifier Screen

Date: 2026-06-22

## Claim

The reduced-cover `0 / mixed / full` B-fiber lift profile is not explained by
two visible low-degree B-line characters in the promotion fields.

This closes the nearest sampler-shaped shortcut suggested by the reduced-cover
point count:

```text
lift_units(B) != 1_{chi(F(B))=+1} + 1_{chi(G(B))=+1}
```

for tested named atoms, all rational-linear factors, and all pairs of monic
irreducible quadratic factors.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_reduced_lift_classifier_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_linear_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_q1607_quad_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_q1847_q2087_quad_20260622.txt
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reduced_lift_classifier_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_linear_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reduced_lift_classifier_probe.py \
  --small-primes 1607 \
  --quadratic-pair \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_q1607_quad_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reduced_lift_classifier_probe.py \
  --small-primes 1847,2087 \
  --quadratic-pair \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_lift_classifier_probe_q1847_q2087_quad_20260622.txt
```

## Method

For each B-fiber from
[P27 B-Line Reduced-Cover Point Count](p27_b_line_reduced_cover_pointcount_20260622.md),
define:

```text
lift_units = selector_chi_1 / 16
```

so the promotion-field profiles are:

```text
0 = no selector-square U branches
1 = mixed selector-square U branches
2 = all selector-square U branches
```

The exact classifier test asks whether there are two characters `F,G` such
that every row satisfies:

```text
lift_units(B) =
  1_{chi(F(B))=+1} + 1_{chi(G(B))=+1}.
```

Families screened:

```text
named B-line atoms and simple Belyi/branch expressions
all rational-linear factors B-a
all pairs of monic irreducible quadratics B^2+uB+v
```

## Results

Profile sizes:

```text
q1607: rows=100, lift_units 0/1/2 = 22 / 50 / 28
q1847: rows=128, lift_units 0/1/2 = 19 / 64 / 45
q2087: rows=114, lift_units 0/1/2 = 32 / 57 / 25
```

Named atom and rational-linear verdicts:

```text
q1607: atom pair none, linear pair none
q1847: atom pair none, linear pair none
q2087: atom pair none, linear pair none
```

Irreducible quadratic-pair verdicts:

```text
q1607:
  irreducible_quadratic_masks = 1,290,421
  unique_quadratic_masks = 2,580,842
  result = none

q1847:
  irreducible_quadratic_masks = 1,704,781
  unique_quadratic_masks = 3,409,562
  result = none

q2087:
  irreducible_quadratic_masks = 2,176,741
  unique_quadratic_masks = 4,353,482
  result = none
```

## Interpretation

Positive:

```text
The reduced-cover lift profile is now a precise finite-field target.
The nearest two-character sampler shape has a direct promotion-field verdict.
```

Negative:

```text
No visible atom, rational-linear pair, or irreducible-quadratic pair explains
the 0/mixed/full lift profile.
This gives no GPU source bucket.
The reduced-cover lane still needs actual branch/Kummer extraction, not more
visible low-degree classifier hunting.
```

## Continue / Kill

```text
continue = offline branch/Kummer extraction for the reduced cover with selector layer
continue = derive the true branch support from normalization, then test it
continue = compare f4/f3 after the f3 class is extracted

kill = two-visible-character classifier for reduced-cover lift profile
kill = rational-linear B bucket sampler from this profile
kill = irreducible-quadratic-pair B bucket sampler from this profile
kill = GPU production from reduced-cover lift buckets alone
```

```text
p27_b_line_reduced_lift_classifier_rows=1/1
```
