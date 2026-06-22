# P27 Full Quartic q1847 D3 Screen

Date: 2026-06-22

## Claim

The decisive q1847 monic-quartic d3 screen is negative in both visible line
coordinates:

```text
B-line: no exact quartic for d3_on_legalB over q1847
K-line: no exact quartic for d3_on_K over q1847
```

This sharply downgrades the remaining visible genus-1 quartic route.  A stable
quartic source was supposed to appear in q1847 and at least one guard field.
The decisive promotion field has no hit in either B or K.

## Artifacts

Fast C chunk oracle:

```text
research/p27/archive/gates/p27_quartic_chunk_fast.c
```

Target-row exporter:

```text
research/p27/archive/gates/p27_quartic_target_export.py
```

Shard runner:

```text
research/p27/archive/gates/p27_quartic_fast_shard_runner.py
```

Run outputs:

```text
research/p27/archive/probe_outputs/p27_quartic_full_B1847_d3_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_full_B1847_d3_20260622/B_1847_d3_on_legalB_rows.txt
research/p27/archive/probe_outputs/p27_quartic_full_K1847_d3_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_full_K1847_d3_20260622/K_1847_d3_on_K_rows.txt
```

## Validation

The C oracle was first checked against the existing Python B-line chunk runner:

```text
B q1607 d3_on_legalB
start = 0
count = 2000
Python exact_quartics = 0
C exact_quartics = 0
```

Then 10M-triple timing chunks were run:

```text
B q1607 d3_on_legalB:
  triples = 10000000
  exact = 0
  throughput = 2.654M triples/s single process

K q1471 d3_on_K:
  triples = 10000000
  exact = 0
  throughput = 3.081M triples/s single process

B q1847 d3_on_legalB:
  triples = 10000000
  exact = 0
  throughput = 2.445M triples/s single process

K q1847 d3_on_K:
  triples = 10000000
  exact = 0
  throughput = 2.448M triples/s single process
```

## Full Screens

B-line q1847:

```text
coordinate = B
field = 1847
family = d3_on_legalB
rows = 63
plus/minus = 45/18
triples_scanned = 6300872423
polarity_-1_hits = 0
polarity_1_hits = 0
exact_quartics = 0
wall_seconds = 501.012820
wall_throughput_triples_per_second = 12576269.851
```

K-line q1847:

```text
coordinate = K
field = 1847
family = d3_on_K
rows = 63
plus/minus = 45/18
triples_scanned = 6300872423
polarity_-1_hits = 0
polarity_1_hits = 0
exact_quartics = 0
wall_seconds = 499.681562
wall_throughput_triples_per_second = 12609775.711
```

Both runs used:

```text
workers = 10
chunk_size = 50000000
zero policy = reject quartics vanishing on any target row
global polarity = allowed
flattening = index = (a*q + b)*q + c
```

## Interpretation

Positive:

```text
The full quartic suite is now locally executable, not only GPU-handoff prose.
The fast oracle gives a deterministic CPU check for future GPU chunks/hits.
```

Negative for the moonshot:

```text
The decisive q1847 d3 quartic source is absent in both B and K coordinates.
Therefore the visible monic-quartic genus-1 explanation for d3 is very unlikely.
```

This does not kill every B/K line route.  It kills the visible monic quartic
route in the decisive promotion field.  Remaining B/K routes are:

```text
1. optional q2087/q1607 closure only as bookkeeping, not promotion;
2. gate4-prefix q2087 only as bookkeeping, since q1847 is now negative;
3. offline branch/genus/Kummer extraction over P1_B/P1_K;
4. non-visible recurrence or higher-genus class sequence.
```

Follow-up:
[P27 B-Line Gate4-Prefix Quartic q1847 Screen](p27_b_line_gate4_prefix_quartic_q1847_screen_20260622.md)
closes item 2 in the decisive q1847 field with zero exact quartics.

## Continue / Kill

```text
continue = offline normalized Kummer/divisor extraction over P1_B/P1_K
continue = use fast oracle for any future GPU quartic hit/chunk validation
continue = optional q2087 gate4-prefix closure only if a theorem needs it

kill = d3 visible monic quartic source in the decisive q1847 field
kill = d3+d4 visible monic quartic B-line source in the decisive q1847 field
kill = expecting a stable B/K quartic d3 hit to beat sqrt
kill = spending GPU production time on B/K d3 quartics without new evidence
```

```text
p27_full_quartic_q1847_d3_screen_rows=1/1
```
