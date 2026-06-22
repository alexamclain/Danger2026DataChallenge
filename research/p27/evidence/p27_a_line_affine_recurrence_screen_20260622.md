# P27 A-Line Affine Recurrence Screen

Date: 2026-06-22

## Claim

The cheapest possible A-line recurrence is negative in the meaningful
promotion-field transition:

```text
d4(A) != +/- d3(m*A + b)
```

on the selected `d3=+1` A-domain for every affine map `A -> m*A+b` in
q1607, q1847, and q2087.

This kills the first nontrivial sourceable-map shortcut after A-prefix descent.
The live A-line route remains normalized Kummer/divisor class extraction, not
an affine A-map recurrence.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_a_line_affine_recurrence_probe.py
```

Primary output:

```text
research/p27/archive/probe_outputs/p27_a_line_affine_recurrence_probe_q1607_q1847_q2087_depth8_20260622.txt
```

Exploratory low-row output:

```text
research/p27/archive/probe_outputs/p27_a_line_affine_recurrence_probe_q1607_q1847_q2087_depth8_min8_20260622.txt
```

## Commands

Primary:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_affine_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 20 \
  --keep-best 5 \
  | tee research/p27/archive/probe_outputs/p27_a_line_affine_recurrence_probe_q1607_q1847_q2087_depth8_20260622.txt
```

Low-row exploratory tail:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_a_line_affine_recurrence_probe.py \
  --small-primes 1607,1847,2087 \
  --depth 8 \
  --min-rows 8 \
  --keep-best 5 \
  | tee research/p27/archive/probe_outputs/p27_a_line_affine_recurrence_probe_q1607_q1847_q2087_depth8_min8_20260622.txt
```

## Method

For each transition `d_j -> d_{j+1}`, the probe builds A-labeled rows using the
same selected-prefix convention as the A-level descent packet.  It then tests:

```text
d_{j+1}(A) = polarity * d_j(m*A + b)
```

for all full-coverage affine maps.  Any full-coverage map must send the first
later-domain A value to one of the earlier-domain A values, so the search only
needs `q * #previous_rows` candidate maps instead of a full `q^2` scan.

Promotion requires:

```text
covered = next_rows
matches = next_rows
```

Partial best maps are diagnostic only.

## Decisive Transition

The meaningful transition is `d3 -> d4`, because all three guard fields have
enough rows and it is the first nontrivial recurrence check after A-prefix
descent.

```text
q1607:
  prev d3 rows = 49
  next d4 rows = 28
  affine maps tested = 78694
  exact affine recurrences = 0
  best = 19/28 matches, identity map

q1847:
  prev d3 rows = 63
  next d4 rows = 45
  affine maps tested = 116298
  exact affine recurrences = 0
  best = 26/45 matches, identity map with opposite polarity

q2087:
  prev d3 rows = 57
  next d4 rows = 25
  affine maps tested = 118902
  exact affine recurrences = 0
  best = 18/25 matches, identity map
```

The identity best score is the expected tautology: the `d4` domain is already
conditioned on `d3=+1`, so identity can only reproduce the plus/minus imbalance
of `d4`; it is not a recurrence.

## Small-Field Tails

With `--min-rows 8`, later transitions sometimes show exact identity maps:

```text
q1607:
  d4 -> d5: identity, polarity +1, 19/19
  d5 -> d6: identity, polarity -1, 19/19

q1847:
  d4 -> d5: identity, polarity -1, 19/19

q2087:
  d4 -> d5: identity, polarity +1, 18/18
  d5 -> d6: identity, polarity +1, 18/18
  d6 -> d7: identity, polarity +1, 18/18
  d7 -> d8: identity, polarity -1, 18/18
```

These are local one-sided prefix tails, not p27 structure.  The signs and stop
gates disagree by field, matching the existing warning that small-field tails
are useful for bookkeeping but not production prediction.

## Interpretation

Positive:

```text
The A-line recurrence question is now sharper.
Any recurrence that beats sqrt is not the cheap affine map A -> m*A+b.
```

Negative:

```text
No promotion-field affine map carries d3 to d4.
Late exact identity maps are small-field plateau artifacts.
This does not justify an A-bucket GPU run.
```

## Continue / Kill

```text
continue = normalized A-level Kummer/divisor class extraction
continue = theorem-guided correspondence tests if a source suggests one
continue = bounded A-prefix telemetry only as class-extraction input

kill = affine A-line recurrence d_{j+1}(A)=+/-d_j(m*A+b)
kill = interpreting later small-field identity plateaus as a p27 recurrence
kill = GPU A-bucket production from A-prefix descent alone
```

```text
p27_a_line_affine_recurrence_screen_rows=1/1
```
