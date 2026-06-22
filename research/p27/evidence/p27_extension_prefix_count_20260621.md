# P27 Extension-Field Selected-Prefix Counts

Date: 2026-06-21

## Claim

Extension-field counts support the current negative read: the legal
label-2/compactD source is curve-sized, but selected conic/Kummer prefixes do
not reveal a stable smaller source.

This is a lightweight substitute for the memory-heavy online Magma
normalization.  It counts the trusted staged equations over `GF(7^n)` and
`GF(23^n)`:

```text
residual E/T source
compactD = -1
label-2 candidate map to (A,x5)
selected halving prefixes d3, d4, ...
```

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_extension_prefix_count_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q7_degree1_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q607_degree1_validation_20260621.txt
research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q7_degrees1_5_depth5_20260621.txt
research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q23_degrees1_3_depth5_20260621.txt
```

Validation command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_extension_prefix_count_probe.py \
  --q 607 \
  --degrees 1 \
  --depth 4 \
  | tee research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q607_degree1_validation_20260621.txt
```

The q607 validation matches the existing prime-field profile exactly:

```text
unique_ax = 128
unique_A = 32
depth1 ax/A = 64/16
depth2 ax/A = 0/0
```

Main commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_extension_prefix_count_probe.py \
  --q 7 \
  --degrees 1,2,3,4,5 \
  --depth 5 \
  | tee research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q7_degrees1_5_depth5_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_extension_prefix_count_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  --depth 5 \
  | tee research/p27/archive/probe_outputs/p27_extension_prefix_count_probe_q23_degrees1_3_depth5_20260621.txt
```

## Extension Counts

Selected rows over `GF(7^n)`:

```text
GF(7^1), N=7:
  unique_ax=0, unique_A=0

GF(7^2), N=49:
  unique_ax=0, unique_A=0

GF(7^3), N=343:
  source_rows=156
  unique_ax=36, unique_A=9
  depth1 ax/A = 0/0

GF(7^4), N=2401:
  source_rows=1092
  unique_ax=672, unique_A=168
  depth1 ax/A = 128/32
  depth2 ax/A = 0/0

GF(7^5), N=16807:
  source_rows=8920
  unique_ax=2360, unique_A=590
  depth1 ax/A = 1260/315
  depth2 ax/A = 560/140
  depth3 ax/A = 560/140
  depth4 ax/A = 0/0
```

Selected rows over `GF(23^n)`:

```text
GF(23^1), N=23:
  source_rows=4
  unique_ax=0, unique_A=0

GF(23^2), N=529:
  source_rows=256
  unique_ax=96, unique_A=24
  depth1 ax/A = 32/8
  depth2 ax/A = 32/8
  depth3 ax/A = 32/8
  depth4 ax/A = 0/0

GF(23^3), N=12167:
  source_rows=6232
  unique_ax=1596, unique_A=399
  depth1 ax/A = 864/216
  depth2 ax/A = 480/120
  depth3 ax/A = 336/84
  depth4 ax/A = 336/84
  depth5 ax/A = 336/84
```

## Interpretation

Positive:

```text
The staged source behaves as a curve-sized object over extension fields:
source rows and unique (A,x) counts are O(N), not O(N^2).
The extension-field implementation is validated against q607 prime-field
counts from the older probes.
```

Negative for sqrt beating:

```text
Unique A and unique (A,x) remain locked by a fixed fiber size.
Selected prefixes reduce A and (A,x) together; no smaller A-source appears.
Extension fields show local Frobenius-tail behavior, but not a stable source
collapse that would extrapolate to p27.
```

This reinforces the current frontier: the legal conic/Kummer tower is the
right mathematical object, but a beat-sqrt path still needs a quotient,
normalization/component structure, or theorem-level identity.  Extension
counts alone do not show a sampler below `sqrt(p)`.

## Continue / Kill

```text
continue = staged normalization/components or quotient extraction
continue = expert ask for repeated Kummer/Hilbert-90 boundary theorem
continue = GPU telemetry for structural capture, not source enumeration

kill = extension-field count evidence for a low-degree A/source collapse
kill = treating q7/q23 Frobenius tails as p27 source laws
kill = raw selected-prefix source enumeration as sqrt-beating
```

```text
p27_extension_prefix_count_rows=1/1
```
