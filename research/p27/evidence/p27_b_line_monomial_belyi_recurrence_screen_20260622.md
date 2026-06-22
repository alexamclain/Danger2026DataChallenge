# P27 B-Line Monomial Belyi Recurrence Screen

Date: 2026-06-22

## Claim

The fixed monomial Belyi maps on the B-line do not give the missing `d3 -> d4`
recurrence.

The B-line branch set is:

```text
{0, -2, infinity}
```

After normalizing:

```text
u = -B/2
```

this becomes `{0,1,infinity}`.  The nearest canonical Belyi self-maps are
therefore:

```text
u -> u^m
```

conjugated by the six visible S3 symmetries of the branch set.  The probe
tested `m=2..12` and found no exact forward or reverse `d3/d4` recurrence in
q1607/q1847/q2087.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_monomial_belyi_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_monomial_belyi_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_monomial_belyi_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,3,4,5,6,7,8,9,10,11,12 \
  --keep-best 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_monomial_belyi_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

## Test

The probe checks:

```text
d4(B) = +/- d3(phi(B))
d3(B) = +/- d4(phi(B))
```

where:

```text
phi = left_S3 o (u -> u^m) o right_S3
m = 2..12
left_S3, right_S3 in S3({0,-2,infinity})
```

This is `11 * 6 * 6 = 396` fixed maps per field.

## Results

No exact recurrence was found.

Forward `d4(B) = +/- d3(phi(B))`:

```text
q1607: best covered 5/28,  best matches 3
q1847: best covered 10/45, best matches 5
q2087: best covered 4/25,  best matches 4
```

Reverse `d3(B) = +/- d4(phi(B))`:

```text
q1607: best covered 5/49,  best matches 5
q1847: best covered 12/63, best matches 6
q2087: best covered 4/57,  best matches 4
```

Some tiny covered subsets are perfectly matched, but the coverage is far too
small to be a sourceable recurrence.

## Interpretation

Positive:

```text
This closes the canonical monomial Belyi self-map family on the B branch line.
It is distinct from the hidden-X power-map screen.
```

Negative:

```text
No S3-conjugated u -> u^m map for m=2..12 carries d3 to d4.
Coverage is lower than the already-negative hidden-X power maps.
No B-line GPU/source shortcut follows from monomial Belyi dynamics.
```

The surviving B-line task remains:

```text
extract f3(B), f4(B), f5(B), ...
compute branch support/genus/quotients
look for a non-visible Kummer/divisor relation or sourceable correspondence
```

## Continue / Kill

```text
continue = normalized B-line Kummer/divisor class extraction
continue = theorem-specified correspondences only outside PGL2, hidden-X powers, and monomial Belyi maps
continue = bounded GPU deep-prefix telemetry only if it feeds class extraction

kill = S3-conjugated monomial Belyi maps u -> u^m for m=2..12 as B-line recurrence
kill = treating small covered subsets as a sampler
kill = GPU B-bucket production from monomial Belyi dynamics
```

```text
p27_b_line_monomial_belyi_recurrence_screen_rows=1/1
```
