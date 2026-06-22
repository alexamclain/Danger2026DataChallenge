# P27 K-Line Reverse-Z Relation Screen

Date: 2026-06-21

## Claim

Keeping the actual d3 all-plus source root does not reveal a low-degree plane
cover over the reduced K-line or S-root coordinate.

This is a sharper proxy for branch extraction than sign-only screens.  It uses
the real reverse-doubling source variable:

```text
x6 = z^2
K = x([2]P) on E': V^2 = U^3 + 4U
Sroot^2 = K
```

and tests low-degree relations in:

```text
(K,z), (Sroot,z), (K,x6), (Sroot,x6),
(K,r), (Sroot,r), r=x6+1/x6,
(K,z+1/z), (Sroot,z+1/z),
(K,z-1/z), (Sroot,z-1/z).
```

On q1607/q1847/q2087 all main systems are full-rank through degree `20`.
The only extra-nullity rows are q1607-only degree-20 artifacts in lower
multiplicity projections; they do not repeat in q1847 or q2087.  On a
1,000-row p27 sample, all systems are full-rank through degree `12`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q1607_q1847_q2087_deg12_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q1607_q1847_q2087_deg14_20_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_p27_sample_deg8_20260621.txt
research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_p27_sample_deg10_12_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py \
  --small-primes 607 \
  --degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q607_smoke_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6,8,10,12 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q1607_q1847_q2087_deg12_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 14,16,18,20 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_q1607_q1847_q2087_deg14_20_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py \
  --small-primes '' \
  --p27-target 1000 \
  --max-draws 500000 \
  --degrees 2,4,6,8 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_p27_sample_deg8_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_reverse_z_relation_probe.py \
  --small-primes '' \
  --p27-target 1000 \
  --max-draws 500000 \
  --degrees 10,12 \
  | tee research/p27/archive/probe_outputs/p27_kline_reverse_z_relation_probe_p27_sample_deg10_12_20260621.txt
```

## Results

Promotion fields:

```text
q1607:
  z_rows = 1792
  unique_K = 28
  unique_K_z = 448
  unique_S = 56
  unique_S_z = 896
  (K,z), (Sroot,z), (Sroot,x6), (Sroot,z+/-1/z):
    degree 2..20 even: extra_nullity = 0
  q1607-only degree-20 artifacts:
    (Sroot,r), (K,z+1/z), (K,z-1/z) have extra_nullity = 2

q1847:
  z_rows = 2880
  unique_K = 45
  unique_K_z = 720
  unique_S = 90
  unique_S_z = 1440
  every system degree 2,4,6,8,10,12,14,16,18,20: extra_nullity = 0

q2087:
  z_rows = 1600
  unique_K = 25
  unique_K_z = 400
  unique_S = 50
  unique_S_z = 800
  every system degree 2,4,6,8,10,12,14,16,18,20: extra_nullity = 0
```

p27 sample:

```text
sample_rows = 1000
oriented_candidates_raw = 4000
z_rows = 7744
unique_K = 242
unique_K_z = 1936
unique_S = 484
unique_S_z = 3872
every system degree 2,4,6,8,10,12: extra_nullity = 0
```

q607 smoke:

```text
z_rows = 1024
all systems degree 2,4: extra_nullity = 0
```

## Interpretation

Positive:

```text
The probe preserves the actual source root z, so it is closer to the
branch-cover problem than sign-only K-line character screens.
The p27 sample and q=7 mod 16 guard fields agree.
```

Negative:

```text
No hyperelliptic-looking relation z^2=f(K), z^2=f(Sroot), or low-degree
normalization through r, z+1/z, or z-1/z appears in these coordinates across
the promotion fields.  The only higher-degree anomaly is q1607-local and does
not survive q1847/q2087.
No GPU sampler follows from the obvious K/Sroot reverse-root projections.
```

This does not prove the K-line branch cover is high genus.  It does kill the
next cheap plane-model shortcut.  The remaining first-class K-line task is
actual normalization / branch divisor / genus extraction over `P1_K` or
`P1_Sroot`, preferably offline Magma/Sage over q1607/q1847/q2087.

## Continue / Kill

```text
continue = normalize the d3 source cover over P1_K or P1_Sroot
continue = compute branch degree, support field degrees, genus, and components
continue = carry Sroot -> -Sroot and alpha/H90 actions through the model

kill = plane relation searches in (K,z), (Sroot,z), (K,x6), (K,r), z+/-1/z
kill = GPU bucket/search restarts using these obvious reverse-root projections
kill = interpreting low-degree K/S sign near-misses as source candidates
```

```text
p27_kline_reverse_z_relation_rows=1/1
```
