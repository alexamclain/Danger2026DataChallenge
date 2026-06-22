# P27 K-Line Reverse-Z Extension Counts

Date: 2026-06-21

## Claim

Extension-field counts sharpen the K/S reverse-root read:

```text
The actual d3 all-plus reverse-root cover has a clean constant-degree
projection to K and Sroot, but K and Sroot themselves remain field-sized
sources.  This does not give a direct below-sqrt sampler.
```

This is a lightweight count proxy for the normalization/branch-cover problem.
It keeps the same source as the reverse-root relation screen:

```text
residual E/T source
compactD = -1
label-2 candidate map to (A,x5)
d2 square
x6 = z^2
K = x([2]P) on E': V^2 = U^3 + 4U
Sroot = (U^2 - 4)/(2V), so Sroot^2 = K
```

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q607_validation_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q1607_validation_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q1847_validation_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q2087_validation_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q7_degrees1_5_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q23_degrees1_3_20260621.txt
```

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 607 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q607_validation_20260621.txt
```

The q607 validation reproduces the promoted prime-field reverse-root counts:

```text
candidates = 512
z_rows = 1024
unique_K = 16
unique_S = 32
unique_K_z = 256
unique_S_z = 512
```

Main commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 1607 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q1607_validation_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 1847 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q1847_validation_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 2087 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q2087_validation_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 7 \
  --degrees 1,2,3,4,5 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q7_degrees1_5_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_extension_count_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_extension_count_probe_q23_degrees1_3_20260621.txt
```

## Counts

Promotion fields:

```text
q1607:
  z_rows = 1792
  unique_K = 28
  unique_S = 56
  unique_K_z = 448
  unique_S_z = 896

q1847:
  z_rows = 2880
  unique_K = 45
  unique_S = 90
  unique_K_z = 720
  unique_S_z = 1440

q2087:
  z_rows = 1600
  unique_K = 25
  unique_S = 50
  unique_K_z = 400
  unique_S_z = 800
```

Nonempty extension fields:

```text
GF(7^4), N=2401:
  z_rows = 1024
  unique_K = 16
  unique_S = 32
  unique_A = 168
  unique_Ax = 672

GF(7^5), N=16807:
  z_rows = 20160
  unique_K = 315
  unique_S = 630
  unique_A = 590
  unique_Ax = 2360

GF(23^2), N=529:
  z_rows = 256
  unique_K = 4
  unique_S = 8
  unique_A = 24
  unique_Ax = 96

GF(23^3), N=12167:
  z_rows = 13824
  unique_K = 216
  unique_S = 432
  unique_A = 399
  unique_Ax = 1596
```

Stable fiber laws on all nonempty guard fields:

```text
z_rows / unique_K = 64
z_rows / unique_S = 32
unique_Ax / unique_A = 4
```

The `K_z`, `S_z`, `K_r`, and `S_r` fibers are also constant-sized in the
nonempty fields, with small even-extension variants, but they do not change
the source-size conclusion.

## Interpretation

Positive:

```text
The K/S projection is not random bookkeeping.  It has a reproducible
constant-degree fiber over q607, q1607, q1847, q2087, GF(7^n), and GF(23^n).
This is a good target for actual divisor/branch/genus extraction.
```

Negative for sqrt beating:

```text
unique_K and unique_S still grow at field-size scale in the nonempty extension
fields.  The projection removes only a fixed fiber, not a growing source
dimension.  Enumerating K or Sroot is still sqrt(p)-scale at p27.
```

So this does not justify a direct GPU sampler over K/Sroot, nor another
bucket search in the visible reverse-root coordinates.  The possible win
remains an additional quotient, recurrence, or branch-class theorem that
controls many selected squareclass gates at once.

## Continue / Kill

```text
continue = literal normalization / branch divisor / genus extraction over P1_K
continue = same extraction over P1_Sroot and the Sroot -> -Sroot action
continue = CAS packet that explains the degree-64 K fiber and its branch places
continue = compare d4 only after the d3 branch class is named

kill = treating K/Sroot enumeration as a below-sqrt source
kill = GPU K/S bucket searches based only on this projection
kill = more plane relation scans in z, x6, r, z+1/z, or z-1/z
kill = reading the constant fiber as a production speedup without a sampler
```

```text
p27_kline_reverse_z_extension_count_rows=1/1
```
