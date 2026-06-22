# P27 B-Line PGL2 Recurrence Screen

Date: 2026-06-22

## Claim

The descended B-line `d4` class is not a degree-one rational pullback of the
descended `d3` class in the p27-signature promotion fields.

The screen tests every full-coverage PGL2 map:

```text
d4(B) = +/- d3((a*B+b)/(c*B+d)).
```

This closes the cheap B-line recurrence/coboundary loophole.  The B-line
moonshot still has to be actual Kummer/divisor class extraction or a
higher-degree/theorem-specified correspondence.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_pgl2_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_pgl2_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_pgl2_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --keep-best 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_pgl2_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

## Method

The inputs are the descended B-line maps from `legal_b_maps(q)`:

```text
d3(B) on legal B rows
d4(B) after d3(B)=+1
```

A full-coverage PGL2 recurrence must map every `d4` B row back into the `d3`
B-domain.  Any such map is determined by the images of three distinct `d4`
B-values, so the probe enumerates ordered triples in the `d3` domain and
deduplicates the resulting PGL2 maps.

Promotion requires:

```text
covered = d4_B_rows
matches = d4_B_rows
```

## Results

```text
q1607:
  d3_B_rows = 49
  d4_B_rows = 28
  distinct PGL2 maps tested = 110544
  exact PGL2 recurrences = 0
  best full coverage = identity, 19/28 matches

q1847:
  d3_B_rows = 63
  d4_B_rows = 45
  distinct PGL2 maps tested = 238266
  exact PGL2 recurrences = 0
  best full coverage = identity with opposite polarity, 26/45 matches

q2087:
  d3_B_rows = 57
  d4_B_rows = 25
  distinct PGL2 maps tested = 175560
  exact PGL2 recurrences = 0
  best full coverage = identity, 18/25 matches
```

The best full-coverage maps are the identity maps.  Their scores are exactly
the raw majority bias of `d4` on the `d3=+1` B-domain, not a recurrence.

Some non-identity maps are exact on small partial overlaps, such as `9/9` in
q1847, but their coverage is far below the sampler-relevant domain size.

## Interpretation

Positive:

```text
The B-line recurrence loophole is now sharply delimited.
The test is structural: every full-coverage degree-one rational map on P1_B is
covered.
```

Negative:

```text
No degree-one rational B-line map carries d3 to d4.
No GPU or agent time should go to B-line PGL2 recurrence scans.
The next B-line result must come from extracted classes, not fitted maps.
```

## Continue / Kill

```text
continue = normalize/extract the B-line Kummer class f3(B)
continue = compare f4/f3 only after f3 is named
continue = higher-degree B-line correspondences only if theorem-shaped

kill = degree-one rational B-line recurrence
kill = B-line affine recurrence as a special case
kill = GPU production from B-line recurrence buckets
```

```text
p27_b_line_pgl2_recurrence_screen_rows=1/1
```
