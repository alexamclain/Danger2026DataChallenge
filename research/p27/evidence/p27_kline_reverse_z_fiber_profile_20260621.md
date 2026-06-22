# P27 K-Line Reverse-Z Fiber Profile

Date: 2026-06-21

## Claim

The selected d3 all-plus reverse-root cover has perfectly flat rational K/Sroot
fibers in every tested promotion field:

```text
K fiber:     64 z-rows, 1 A, 4 (A,x), 8 x6, 16 z, 4 r
Sroot fiber: 32 z-rows, 1 A, 4 (A,x), 8 x6, 16 z, 4 r
```

This is positive for branch extraction: K/Sroot is a clean quotient, not random
bookkeeping.  It is negative for immediate sqrt beating: there are no rational
fiber anomalies or small rational branch supports to turn into a GPU bucket or
direct sampler.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q607_validation_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q1607_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q1847_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q2087_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q7_degrees1_5_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q23_degrees1_3_20260621.txt
```

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 607 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q607_validation_20260621.txt
```

Promotion-field commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 1607 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q1607_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 1847 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q1847_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 2087 \
  --degrees 1 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q2087_20260621.txt
```

Extension-field commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 7 \
  --degrees 1,2,3,4,5 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q7_degrees1_5_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_fiber_profile_probe.py \
  --q 23 \
  --degrees 1,2,3 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_fiber_profile_probe_q23_degrees1_3_20260621.txt
```

## Promotion Fields

q1607:

```text
unique_K = 28
unique_S = 56
K_to_S_values = 28
S_to_mixed_K = 0

K fibers:
  rows: 64:28
  unique_A: 1:28
  unique_Ax: 4:28
  unique_x6: 8:28
  unique_z: 16:28
  unique_r: 4:28

S fibers:
  rows: 32:56
  unique_A: 1:56
  unique_Ax: 4:56
  unique_x6: 8:56
  unique_z: 16:56
  unique_r: 4:56
```

q1847:

```text
unique_K = 45
unique_S = 90
K_to_S_values = 45
S_to_mixed_K = 0

K fibers:
  rows: 64:45
  unique_A: 1:45
  unique_Ax: 4:45
  unique_x6: 8:45
  unique_z: 16:45
  unique_r: 4:45

S fibers:
  rows: 32:90
  unique_A: 1:90
  unique_Ax: 4:90
  unique_x6: 8:90
  unique_z: 16:90
  unique_r: 4:90
```

q2087:

```text
unique_K = 25
unique_S = 50
K_to_S_values = 25
S_to_mixed_K = 0

K fibers:
  rows: 64:25
  unique_A: 1:25
  unique_Ax: 4:25
  unique_x6: 8:25
  unique_z: 16:25
  unique_r: 4:25

S fibers:
  rows: 32:50
  unique_A: 1:50
  unique_Ax: 4:50
  unique_x6: 8:50
  unique_z: 16:50
  unique_r: 4:50
```

Every printed promotion-field histogram has:

```text
anomalous_fibers = 0
```

for `rows`, `unique_A`, `unique_Ax`, `unique_x6`, `unique_z`, `unique_r`,
`unique_zsum`, and `unique_zdiff`.

## Extension Fields

The nonempty extension fields also have flat row fibers:

```text
GF(7^4):  K rows 64:16,  S rows 32:32
GF(7^5):  K rows 64:315, S rows 32:630
GF(23^2): K rows 64:4,   S rows 32:8
GF(23^3): K rows 64:216, S rows 32:432
```

`Sroot` fibers keep `unique_A=1` in all nonempty tested extensions.  In the
even extensions `GF(7^4)` and `GF(23^2)`, K fibers merge two A-values while
Sroot separates them:

```text
GF(7^4):  K unique_A 2:16, S unique_A 1:32
GF(23^2): K unique_A 2:4,  S unique_A 1:8
```

This makes `Sroot` the cleaner extraction coordinate when descent/parity is
manageable.

## Interpretation

Positive:

```text
K/Sroot is an organized quotient of the selected source.
In the promotion fields, each selected K determines exactly one selected A.
The selected Sroot coordinate refines K without mixing K classes.
```

Negative for immediate sqrt beating:

```text
There are no anomalous rational K or Sroot fibers in the promotion fields.
The flat degree-64/32 fibers are a constant-factor quotient, not a growing
scope collapse.
```

So the K/Sroot route remains live only as a branch/genus/function-field
extraction.  A GPU test based on K/Sroot buckets alone would be measuring a
clean constant-degree projection, not a below-sqrt source.

## Continue / Kill

```text
continue = offline normalization over P1_Sroot, with K as a quotient check
continue = derive branch places/support degrees of the flat degree-32 Sroot map
continue = test whether the selected K -> A graph has a named theorem source
continue = only compare d4 after the d3 branch class is explicit

kill = rational-fiber anomaly search as a source of sqrt beating
kill = GPU K/Sroot bucket searches without a new quotient or recurrence
kill = interpreting the degree-64/32 fibers as production acceleration
```

```text
p27_kline_reverse_z_fiber_profile_rows=1/1
```
