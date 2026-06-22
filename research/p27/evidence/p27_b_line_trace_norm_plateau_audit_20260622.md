# P27 B-Line Trace/Norm Plateau Audit

Date: 2026-06-22

## Claim

Trace/norm buckets do not give a transferable B-line sampler.

The only exact trace/norm selectors appear in relative quadratic extensions,
where `trace+norm` identifies a Frobenius-conjugate pair.  Prime-degree
extension fields have mixed trace/norm buckets.  Thus trace/norm is useful
quotient bookkeeping for local plateaus, but it does not explain the p27
sequence or provide a below-sqrt source.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_trace_norm_plateau_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q23_3_q103_2_gate10_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q7_5_q7_6_gate10_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q7_4_q23_2_q31_3_gate8_20260622.txt
```

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_trace_norm_plateau_probe.py \
  --fields 23:3,103:2 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q23_3_q103_2_gate10_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_trace_norm_plateau_probe.py \
  --fields 7:5,7:6 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q7_5_q7_6_gate10_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_trace_norm_plateau_probe.py \
  --fields 7:4,23:2,31:3 \
  --max-gate 8 \
  | tee research/p27/archive/probe_outputs/p27_b_line_trace_norm_plateau_probe_q7_4_q23_2_q31_3_gate8_20260622.txt
```

## Results

The probe tests whether all-plus prefix survival among legal B values is an
exact union of trace, norm, or trace+norm buckets to proper subfields.

Exact cases:

```text
GF(7^4):
  trace_norm_to_2 exact for d3
  every trace_norm_to_2 bucket has size 2

GF(7^6):
  trace_norm_to_3 exact for d3,d4,d5,d6
  every trace_norm_to_3 bucket has size 2

GF(103^2):
  trace_norm_to_1 exact for d3,d4,d5
  every trace_norm_to_1 bucket has size 2
```

The `GF(23^2)` case is one-sided through `d5`, so trace/norm exactness there
is not meaningful:

```text
legal_B = 8
d3+ = d4+ = d5+ = 8
d6+ = 0
```

Mixed cases:

```text
GF(7^5):
  no trace, norm, or trace+norm invariant is exact
  best d3 trace_norm_to_1 accuracy = 0.652542, mixed_buckets = 20
  best d4/d5 accuracy = 0.762711, mixed_buckets remain nonzero

GF(23^3):
  no trace, norm, or trace+norm invariant is exact
  best trace_norm_to_1 accuracy = 0.924812 for d4..d8
  mixed_buckets = 10 for the plateau set

GF(31^3):
  no trace, norm, or trace+norm invariant is exact
  best trace_norm_to_1 accuracy = 0.961290 for d5/d6
  mixed_buckets = 12
```

The exact cases are therefore not stable across extension degrees.  They are
the expected quadratic-conjugacy quotient:

```text
B -> (Trace_{F/F0}(B), Norm_{F/F0}(B))
```

for a relative degree-2 extension `F/F0`.

## Interpretation

Positive:

```text
Relative quadratic trace+norm is an exact quotient for the local B-line
plateau sets in the tested even-degree fields.
This gives CAS a small regression check for Frobenius-conjugacy behavior.
```

Negative:

```text
Prime-degree fields are mixed.
Absolute trace, absolute norm, and trace+norm are not stable selectors.
The exact quadratic cases are only a 2-to-1 conjugate-pair quotient, not a
source-normalized p27 sampler.
```

Thus this does not promote a GPU or direct sampler lane.  It sharpens the B
route to:

```text
extract the Kummer sequence f3(B), f4(B), ...
then explain why certain local Frobenius-conjugate pairs share all-plus tails
```

## Continue / Kill

```text
continue = use trace+norm-to-half as a regression fixture in even extensions
continue = B-line Kummer sequence extraction and class/Frobenius comparison

kill = absolute trace/norm bucket sampler
kill = relative trace/norm bucket sampler as a p27 production lane
kill = promoting even-extension conjugate-pair exactness as below-sqrt
```

```text
p27_b_line_trace_norm_plateau_audit_rows=1/1
```
