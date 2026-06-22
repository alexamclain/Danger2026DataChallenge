# P27 A-Level Power-Correspondence Screen

Date: 2026-06-22

## Claim

Forgetting the sign of `B` does not rescue the hidden-`X` power-map recurrence.

The B-line has a natural hidden coordinate:

```text
B = 8X^2/(X^2 - 1)^2
A = B^2 - 2
```

After the signed B-line power-map screen was negative, this companion probe
tested the A-level projection.  It asks whether the maps induced by
`X -> X^m`, `m=2..6`, become useful only after projecting to `A=B^2-2`.

No exact forward or reverse `d3/d4` correspondence appears in
q1607/q1847/q2087.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_level_power_correspondence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_a_level_power_correspondence_probe_q1607_q1847_q2087_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_level_power_correspondence_probe.py \
  --small-primes 1607,1847,2087 \
  --powers 2,3,4,5,6 \
  --keep-best 12 \
  | tee research/p27/archive/probe_outputs/p27_a_level_power_correspondence_probe_q1607_q1847_q2087_20260622.txt
```

## Test

For each target `A`, the probe takes both `B` roots of `B^2=A+2`, applies:

```text
left_Belyi o (X -> X^m) o right_Belyi
```

on the B-line, then projects the image back to:

```text
A_image = B_image^2 - 2.
```

A multivalued branch is counted only if the source images that land in the
relevant domain all have the same selected sign.  Mixed branches are not
usable recurrences.

## Results

Forward `d4(A) = +/- d3(correspondence(A))`:

```text
q1607: best covered 9/28,  best matches 8,  mixed 0
q1847: best covered 17/45, best matches 10, mixed 0
q2087: best covered 11/25, best matches 6,  mixed 0
```

Reverse `d3(A) = +/- d4(correspondence(A))`:

```text
q1607: best covered 11/49, best matches 7,  mixed 0
q1847: best covered 20/63, best matches 10, mixed 0
q2087: best covered 10/57, best matches 7,  mixed 0
```

The A projection gives slightly higher coverage than the signed B screen, as
expected, but still no full-domain map and no stable majority-domain
recurrence.

## Interpretation

Positive:

```text
This closes the natural "maybe B sign is the problem" loophole.
The test is a named hidden-X correspondence, not an arbitrary A-polynomial fit.
```

Negative:

```text
No Belyi-conjugated X -> X^m map for m=2..6 gives an A-level d3/d4 recurrence.
The best maps cover only minority subsets of the d3/d4 domains.
No GPU/source shortcut follows from hidden-X doubling, tripling, or their A projection.
```

The live A-line task remains normalized-cover Kummer extraction:

```text
recover the actual A-level classes for d3,d4,d5,...
test for low genus, coboundary, recurrence, or sourceable correspondence
```

## Continue / Kill

```text
continue = normalized A-level Kummer/divisor class extraction
continue = theorem-specified higher correspondences only with a new source
continue = direct legal-pullback sampler only after a quotient/source map exists

kill = hidden-X power-map A-level recurrence for m=2..6
kill = treating A=B^2-2 projection as the missing B-line recurrence
kill = GPU A-bucket production from this correspondence family
```

```text
p27_a_level_power_correspondence_screen_rows=1/1
```
