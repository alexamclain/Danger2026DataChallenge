# P27 B-Line Power-Map Recurrence Screen

Date: 2026-06-22

## Claim

The natural hidden-`X` power correspondences on the B-line do not explain the
first B-line transition `d3 -> d4`.

This closes a theorem-shaped loophole after the PGL2 screen.  The B-line
coordinate is:

```text
B = 8X^2/(X^2 - 1)^2 = 8/(X - 1/X)^2.
```

Therefore `X -> X^m` induces explicit degree-`m` self maps on `P1_B`.  The
probe tested these maps for `m=2..6`, with all six Belyi branch symmetries of
`{0,-2,infinity}` on both sides.  No full-coverage exact recurrence appears in
q1607/q1847/q2087.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_power_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_power_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_power_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --powers 2,3,4,5,6 \
  --keep-best 12 \
  | tee research/p27/archive/probe_outputs/p27_b_line_power_recurrence_probe_q1607_q1847_q2087_20260622.txt
```

## Map Family

Let:

```text
U = (X - 1/X)^2 = 8/B.
```

For each tested `m`, the map is:

```text
B_m = 8 / (X^m - X^-m)^2.
```

The implementation evaluates the corresponding rational functions in `U`.
For example:

```text
m=2: B_2 = B^2/(4(B+2))
m=3: B_3 = B^3/(3B+8)^2
```

Each `X^m` map is composed as:

```text
left_Belyi o X^m o right_Belyi
```

where `left_Belyi` and `right_Belyi` range over:

```text
B
-B-2
4/B
-4/(B+2)
-2B/(B+2)
-2(B+2)/B
```

This gives `5 * 6 * 6 = 180` maps per field, with both polarities and both
directions checked:

```text
forward: d4(B) = +/- d3(phi(B))
reverse: d3(B) = +/- d4(phi(B))
```

## Results

No exact full-domain recurrence was found.  The best maps did not even cover a
majority of the relevant domain.

Forward `d4(B) = +/- d3(phi(B))`:

```text
q1607: best covered 7/28, best matches 6
q1847: best covered 12/45, best matches 6
q2087: best covered 6/25, best matches 3
```

Reverse `d3(B) = +/- d4(phi(B))`:

```text
q1607: best covered 11/49, best matches 7
q1847: best covered 12/63, best matches 6
q2087: best covered 6/57, best matches 5
```

The best named examples vary by field and power.  They look like small-domain
partial overlaps, not a stable correspondence.

## Interpretation

Positive:

```text
This was a targeted B-line recurrence test, not another blind polynomial scan.
It directly tested the power maps forced by the hidden X-line behind B.
```

Negative:

```text
No Belyi-conjugated X -> X^m map for m=2..6 carries d3 to d4.
Coverage is too low for a sourceable recurrence.
The nearest hidden-X doubling/tripling shortcut is closed.
```

The surviving B-line task remains actual Kummer/divisor extraction:

```text
extract f3(B), f4(B), f5(B), ...
compute branch support/genus/quotients
look for a non-visible recurrence, coboundary, or sourceable correspondence
```

## Continue / Kill

```text
continue = normalized B-line Kummer/divisor class extraction
continue = theorem-specified higher correspondences only if a source suggests them
continue = bounded GPU deep-prefix telemetry if it feeds class extraction

kill = Belyi-conjugated hidden-X power maps m=2..6 as d3 -> d4 recurrence
kill = treating X -> X^2 / X -> X^3 as a B-line GPU/source shortcut
kill = restarting degree-one or visible branch-symmetry recurrence searches
```

```text
p27_b_line_power_recurrence_screen_rows=1/1
```
