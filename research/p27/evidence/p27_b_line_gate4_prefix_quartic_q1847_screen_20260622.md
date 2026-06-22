# P27 B-Line Gate4-Prefix Quartic q1847 Screen

Date: 2026-06-22

## Claim

The decisive q1847 visible two-gate B-line quartic screen is negative:

```text
coordinate = B
family = gate4_prefix_on_legalB
exact_quartics = 0
```

This closes the nearest visible genus-1 source candidate that could enforce
both `d3=+1` and `d4=+1` on the B-line in the promotion field.

## Artifacts

Fast quartic oracle:

```text
research/p27/archive/gates/p27_quartic_chunk_fast.c
research/p27/archive/gates/p27_quartic_target_export.py
research/p27/archive/gates/p27_quartic_fast_shard_runner.py
```

Target packet:

```text
research/p27/archive/fixtures/p27_b_line_quartic_targets_20260622.json
```

Run outputs:

```text
research/p27/archive/probe_outputs/p27_quartic_B1847_gate4_prefix_10m_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_B1847_gate4_prefix_10m_20260622/B_1847_gate4_prefix_on_legalB_rows.txt
research/p27/archive/probe_outputs/p27_quartic_B1847_gate4_prefix_full_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_B1847_gate4_prefix_full_20260622/B_1847_gate4_prefix_on_legalB_rows.txt
```

## Target

The tested family was:

```text
chi(B^4 + aB^3 + bB^2 + cB + d)
```

with both global polarities allowed and zeros rejected.

Target rows:

```text
field = 1847
family = gate4_prefix_on_legalB
rows = 63
plus/minus = 19/44
```

Here `plus` means the legal B row survives the all-plus prefix through gate4.

## Validation

The target packet was listed with:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_quartic_verify.py --list-targets
```

The q1847 target exported as expected:

```text
field=1847 family=gate4_prefix_on_legalB rows=63 plus=19 minus=44
```

A 10M-triple timing chunk was run before the full screen:

```text
triples_scanned = 10000000
exact_quartics = 0
wall_seconds = 0.978582
wall_throughput_triples_per_second = 10218866.207
```

## Full Screen

```text
coordinate = B
field = 1847
family = gate4_prefix_on_legalB
rows = 63
plus/minus = 19/44
total_triples = 6300872423
triples_scanned = 6300872423
polarity_-1_hits = 0
polarity_1_hits = 0
exact_quartics = 0
wall_seconds = 502.721340
wall_throughput_triples_per_second = 12533528.861
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_fast_shard_runner.py \
  --coordinate B \
  --field 1847 \
  --family gate4_prefix_on_legalB \
  --out-dir research/p27/archive/probe_outputs/p27_quartic_B1847_gate4_prefix_full_20260622 \
  --workers 10 \
  --chunk-size 50000000 \
  --sample-limit 16
```

## Interpretation

Positive:

```text
The visible B-line two-gate quartic question is now a completed fact.
The fast oracle remains reusable for any future exact quartic hit validation.
```

Negative for the moonshot:

```text
There is no q1847 monic quartic B-line source for the d3+d4 all-plus prefix.
Together with the q1847 d3 B/K kills, the visible genus-1 B/K quartic route is
closed in the decisive promotion field.
```

This does not kill B-line Kummer extraction.  It kills the most visible
low-genus quartic source models.  The remaining B-line route is:

```text
actual normalized d3 Kummer/divisor class over P1_B
class comparison for f4/f3 and f5/f4 after d3 is named
higher-genus or non-visible recurrence/coboundary structure
```

## Continue / Kill

```text
continue = B-line normalized Kummer/divisor class extraction
continue = use q2087 gate4-prefix only as bookkeeping if another theorem asks
continue = compare d4/d5 only after the d3 class is explicit

kill = q1847 visible monic quartic source for d3 on B
kill = q1847 visible monic quartic source for d3+d4 all-plus on B
kill = GPU production from B quartic buckets without a new class or theorem
```

```text
p27_b_line_gate4_prefix_quartic_q1847_screen_rows=1/1
```
