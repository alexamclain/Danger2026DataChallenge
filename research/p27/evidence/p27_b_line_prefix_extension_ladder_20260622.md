# P27 B-Line Prefix Extension Ladder

Date: 2026-06-22

## Claim

Extension-field B-line prefix counts do not support a count-only below-sqrt
sampler.

The all-plus B subsets sometimes show dramatic local plateaus, but the plateau
and hard-stop gates move with the field.  This is useful structure for class
extraction, but it is not a transferable p27 source law.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q7_degrees1_6_gate10_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q23_degrees1_3_gate10_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q103_degrees1_2_gate10_20260622.txt
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py \
  --q 7 \
  --degrees 1,2,3,4,5,6 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q7_degrees1_6_gate10_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q23_degrees1_3_gate10_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_prefix_extension_count_probe.py \
  --q 103 \
  --degrees 1,2 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_prefix_extension_count_probe_q103_degrees1_2_gate10_20260622.txt
```

## Results

The probe counts legal B values and the all-plus prefixes for selected gates
`d3..d10` over small extension fields.  In every nonempty row below:

```text
legal_B_missing_core = 0
```

So legal B values remain inside the same core B bucket.  The interesting
question is whether all-plus prefixes become a smaller transferable source.

```text
field      legal_B   d3+   d4+   d5+   d6+   d7+   d8+   d9+
GF(7^3)          9     0     0     0     0     0     0     0
GF(7^4)         72    32     0     0     0     0     0     0
GF(7^5)        590   315   140   140     0     0     0     0
GF(7^6)       3576  1896  1128   600   360     0     0     0

GF(23^2)         8     8     8     8     0     0     0     0
GF(23^3)       399   216   120    84    84    84    84     0

GF(103^2)      288   160    96    48     0     0     0     0
```

Representative scaled half-loss values:

```text
GF(7^6):
  d3 = 1.0604
  d4 = 1.2617
  d5 = 1.3423
  d6 = 1.6107
  d7 = 0

GF(23^3):
  d3 = 1.0827
  d4 = 1.2030
  d5 = 1.6842
  d6 = 3.3684
  d7 = 6.7368
  d8 = 13.4737
  d9 = 0

GF(103^2):
  d3 = 1.1111
  d4 = 1.3333
  d5 = 1.3333
  d6 = 0
```

## Interpretation

Positive:

```text
The B-line quotient remains the right selected-bit carrier.
The extension rows have no legal-B/core-B misses.
Finite fields show real local plateau phenomena worth explaining by Kummer
classes or Frobenius action.
```

Negative:

```text
The plateau and hard-stop gates are not stable:
  GF(7^4) stops at d4
  GF(7^5) stops at d6
  GF(7^6) stops at d7
  GF(23^2) stops at d6
  GF(23^3) stops at d9
  GF(103^2) stops at d6

The all-plus sets remain field-sized before the local stop.
This does not give a transferable direct sampler or GPU bucket.
```

The p27 `60000 + 60000` train/heldout prefix check already showed near
geometric half-loss through meaningful counts.  This extension ladder explains
why the small-field plateaus should not be promoted without an extracted class
or theorem: they are field-local Frobenius/torsion phenomena, not a stable
source-normalized p27 law.

## Continue / Kill

```text
continue = extract the B-line Kummer sequence f3(B), f4(B), ...
continue = compare local plateau gates against extracted class/Frobenius data
continue = use GPU only for bounded Bplus+d3..dN telemetry or a named sampler

kill = B-line prefix counts alone as a below-sqrt sampler
kill = promoting small-field all-plus plateaus without a class recurrence
kill = large GPU production from B buckets after count-only evidence
```

```text
p27_b_line_prefix_extension_ladder_rows=1/1
```
