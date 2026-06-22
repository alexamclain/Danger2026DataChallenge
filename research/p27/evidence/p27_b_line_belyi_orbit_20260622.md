# P27 B-Line Belyi-Orbit Screen

Date: 2026-06-22

## Claim

The visible Belyi automorphisms of the B-line quotient do not produce a
sqrt-beating sampler or quotient shortcut.

The B-line branch set is:

```text
{0, -2, infinity}
```

After normalizing `u=-B/2`, this is `{0,1,infinity}`, with the usual six
Möbius transformations.  In B-coordinates these are:

```text
B
-B - 2
4/B
-4/(B+2)
-2B/(B+2)
-2(B+2)/B
```

In all three p27-signature promotion fields, every non-identity transform
sends every core B value outside the core bucket.  Therefore the legal
B-domain and `d3(B)` cannot be compressed by this visible branch-set orbit.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_belyi_orbit_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_belyi_orbit_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_belyi_orbit_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_belyi_orbit_probe_q1607_q1847_q2087_20260622.txt
```

## Results

For the core B bucket:

```text
q1607: core_B = 200, legal_B = 49
q1847: core_B = 230, legal_B = 63
q2087: core_B = 260, legal_B = 57
```

For every non-identity transform and every field:

```text
image_core = 0
image_legal = 0
image_out_domain = core_B
```

The same pattern holds after restricting to legal B and to the d4 domain:

```text
non-identity images leave core and legal domains completely
```

Thus the only in-domain orbit is the identity orbit:

```text
core orbit_size_1 = core_B
legal d3 orbit_size_1 = legal_B
d4 orbit_size_1 = d4_labeled_B
```

## Interpretation

Positive:

```text
The B branch chamber is now understood: the core bucket is a single visible
branch chamber, not an S3-stable source.
```

Negative:

```text
No visible Belyi automorphism maps core/legal B values to other usable
core/legal B values.
No orbit quotient reduces the legal-domain or d3(B) problem.
No GPU sampler follows from B-line branch-set symmetry.
```

The B-line route remains live only as actual Kummer/divisor extraction:

```text
extract f3(B), f4(B), ...
compute branch support/genus/quotients
look for non-visible recurrence or coupling
```

Follow-up:
[P27 B-Line Belyi-Involution Quartic Screen](p27_b_line_involution_quartic_screen_20260622.md)
tests the nearest quartic branch-support families preserved by the three
order-2 Belyi symmetries.  Those q^2/q families have zero exact hits over
q1607/q1847/q2087 for both `d3_on_legalB` and `gate4_prefix_on_legalB`, so
the visible branch-set symmetry is also negative inside the remaining quartic
GPU family.

## Continue / Kill

```text
continue = B-line Kummer/divisor extraction over P1_B
continue = low-genus quotient or non-visible recurrence search
continue = CAS normalization of the legal/d3 B-line cover

kill = visible Belyi S3 orbit sampler on B
kill = branch-set automorphism quotient as a GPU reason
kill = using Belyi transforms to explain legal B or d3(B)
```

```text
p27_b_line_belyi_orbit_rows=1/1
```
