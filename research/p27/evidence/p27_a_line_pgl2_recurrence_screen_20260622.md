# P27 A-Line PGL2 Recurrence Screen

Date: 2026-06-22

## Claim

The full degree-one rational A-line recurrence family is negative in the
meaningful promotion-field transition:

```text
d4(A) != +/- d3((a*A+b)/(c*A+d))
```

on the selected `d3=+1` A-domain for every full-coverage PGL2 map in q1607,
q1847, and q2087.

This closes the cheap degree-one rational recurrence route after A-prefix
descent.  A sqrt-beating A-line win now needs a normalized Kummer/divisor class
relation, coboundary, non-degree-one correspondence, or another theorem-shaped
source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_pgl2_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_a_line_pgl2_recurrence_probe_q1607_q1847_q2087_depth8_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_pgl2_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 20 \
  --keep-best 5 \
  | tee research/p27/archive/probe_outputs/p27_a_line_pgl2_recurrence_probe_q1607_q1847_q2087_depth8_20260622.txt
```

## Method

For a transition `d_j -> d_{j+1}`, the probe tests:

```text
phi(A) = (a*A+b)/(c*A+d)
d_{j+1}(A) = polarity * d_j(phi(A))
```

on the selected prefix domain before `d_{j+1}`.  A full-coverage PGL2 map must
send three fixed later-domain A values to three distinct earlier-domain A
values, so the exact screen enumerates ordered triples of previous-domain
images rather than all `q^3` normalized PGL2 maps.

Promotion requires:

```text
covered = next_rows
matches = next_rows
```

Maps with poles on the later-domain rows or images outside the previous domain
do not have full coverage.

## Decisive Transition

The meaningful test is `d3 -> d4`: it is the first nontrivial recurrence after
A-prefix descent, and all three p27-signature promotion fields have enough
rows.

```text
q1607:
  prev d3 rows = 49
  next d4 rows = 28
  distinct PGL2 maps tested = 110544
  exact PGL2 recurrences = 0
  best = identity, 19/28 matches

q1847:
  prev d3 rows = 63
  next d4 rows = 45
  distinct PGL2 maps tested = 238266
  exact PGL2 recurrences = 0
  best = identity with opposite polarity, 26/45 matches

q2087:
  prev d3 rows = 57
  next d4 rows = 25
  distinct PGL2 maps tested = 175560
  exact PGL2 recurrences = 0
  best = identity, 18/25 matches
```

The best full-coverage maps are the identity maps already seen in the affine
screen.  They score only the raw `d4` plus/minus imbalance on the `d3=+1`
domain; this is not a recurrence.

## Interpretation

Positive:

```text
The A-line recurrence loophole is now narrower.
The exact screen covers every full-coverage degree-one rational map on P1_A.
```

Negative:

```text
No PGL2 map carries d3 to d4 in q1607/q1847/q2087.
Degree-one rational A-line recurrences should not be retried.
This does not justify an A-bucket GPU run.
```

## Continue / Kill

```text
continue = normalized A-level Kummer/divisor class extraction
continue = non-degree-one correspondences only if theorem-shaped
continue = compare classes as coboundaries/pullbacks after a normalized model exists

kill = degree-one rational A-line recurrence
kill = affine A-line recurrence as a special case
kill = GPU A-bucket production from A-prefix descent alone
```

```text
p27_a_line_pgl2_recurrence_screen_rows=1/1
```
