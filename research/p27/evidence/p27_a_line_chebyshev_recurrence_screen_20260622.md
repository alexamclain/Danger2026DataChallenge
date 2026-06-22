# P27 A-Line Chebyshev Recurrence Screen

Date: 2026-06-22

## Claim

The canonical Chebyshev/Dickson self-maps of the A-line do not give the
missing selected-gate recurrence.

This is the natural theorem-shaped higher correspondence after the A-line S3,
affine, PGL2, and hidden-`X` power-map screens.  The A-line branch set is:

```text
{-2, 2, infinity}
```

The fixed maps preserving this postcritical set are:

```text
D_0(A) = 2
D_1(A) = A
D_{m+1}(A) = A*D_m(A) - D_{m-1}(A)
```

equivalently:

```text
D_m(A) = 2*T_m(A/2)
```

The probe tested `D_m` for `m=2..12`, conjugated on both sides by the six
visible S3 symmetries of the A branch set.  No exact full-domain recurrence
appears in q1607/q1847/q2087.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_chebyshev_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_a_line_chebyshev_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_chebyshev_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 8 \
  --degrees 2,3,4,5,6,7,8,9,10,11,12 \
  --keep-best 10 \
  | tee research/p27/archive/probe_outputs/p27_a_line_chebyshev_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

## Test

For each transition `d_j -> d_{j+1}` with enough rows, the probe checks:

```text
d_{j+1}(A) = +/- d_j(left_S3(D_m(right_S3(A))))
```

for all:

```text
m = 2..12
left_S3, right_S3 in S3({-2,2,infinity})
```

That is `11 * 6 * 6 = 396` fixed maps per transition.

## Results

No exact full-domain recurrence was found.

Main `d3 -> d4` transition:

```text
q1607: best covered 10/28, best matches 9
q1847: best covered 17/45, best matches 11
q2087: best covered 9/25,  best matches 6
```

Later transitions also fail as source laws.  Some late small-field rows have
perfect matches on the covered subset, but only with low coverage:

```text
q1607 d5 -> d6: best covered 6/19, matches 6
q1847 d4 -> d5: best covered 5/19, matches 5
q2087 d4 -> d5: best covered 6/18, matches 6
q2087 d5 -> d6: best covered 6/18, matches 6
q2087 d6 -> d7: best covered 6/18, matches 6
q2087 d7 -> d8: best covered 6/18, matches 6
```

Those rows are the already-known small-field one-sided tails: q1607 has d5
all plus then d6 all minus, q1847 has d5 all minus, and q2087 has d5/d6/d7
all plus then d8 all minus.  They do not agree across fields and do not cover
the full domain.

## Interpretation

Positive:

```text
This closes the canonical postcritically finite A-line self-map family.
It is a theorem-shaped correspondence test, not a coefficient scan.
```

Negative:

```text
No S3-conjugated Chebyshev/Dickson map D_m, m=2..12, carries d3 to d4.
The partial later hits are low-coverage small-field tails.
No A-line GPU/source shortcut follows from Chebyshev dynamics.
```

The surviving A-line task remains:

```text
extract the actual normalized A-level Kummer/divisor classes
compare d3,d4,d5,... for a non-visible coboundary, recurrence, or sourceable quotient
```

## Continue / Kill

```text
continue = normalized A-cover Kummer/divisor class extraction
continue = theorem-specified correspondences only if they are not the branch S3, PGL2, hidden-X, or Chebyshev family
continue = direct legal-pullback sampler only after a quotient/source map exists

kill = S3-conjugated Chebyshev/Dickson maps D_m for m=2..12 as A-level recurrence
kill = promoting small-field one-sided Chebyshev tails without full-domain coverage
kill = GPU A-bucket production from Chebyshev dynamics
```

```text
p27_a_line_chebyshev_recurrence_screen_rows=1/1
```
