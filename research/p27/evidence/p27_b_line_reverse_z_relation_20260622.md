# P27 B-Line Reverse-Z Relation Screen

Date: 2026-06-22

## Claim

Keeping the actual d3 all-plus reverse-source root does not reveal a
low-degree plane cover over the B-line.

This is a sharper B-line extraction proxy than sign-only support scans.  It
uses the real reverse-doubling source variable:

```text
B = 8*X^2/(X^2 - 1)^2
x6 = z^2
```

and tests low-degree relations in:

```text
(B,z), (B,x6), (B,r), r=x6+1/x6,
(B,z+1/z), (B,z-1/z),
(lambda,z), lambda=B/(B+2),
(mu,z), mu=(B-2)/(B+2),
(B,z/B), (B,z/(B+2)), (B,z/(B-2)).
```

On q1607/q1847/q2087 the actual `(B,z)` cover and the branch-normalized
`z` systems are full-rank through total degree `20`.  The only extra-nullity
rows are q1607-only degree-20 artifacts in the compressed `z+/-1/z`
projections; they do not repeat in q1847 or q2087.  On a 1,000-row p27 sample,
all systems are full-rank through degree `12`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_reverse_z_relation_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q607_smoke_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q1607_q1847_q2087_deg12_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q1607_q1847_q2087_deg14_20_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_p27_sample_deg12_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reverse_z_relation_probe.py \
  --small-primes 607 \
  --degrees 2,4 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q607_smoke_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reverse_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 2,4,6,8,10,12 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q1607_q1847_q2087_deg12_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reverse_z_relation_probe.py \
  --small-primes 1607,1847,2087 \
  --degrees 14,16,18,20 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_q1607_q1847_q2087_deg14_20_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_reverse_z_relation_probe.py \
  --small-primes '' \
  --p27-target 1000 \
  --max-draws 500000 \
  --degrees 2,4,6,8,10,12 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reverse_z_relation_probe_p27_sample_deg12_20260622.txt
```

## Results

Promotion fields:

```text
q1607:
  z_rows = 1792
  unique_B = 28
  unique_B_z = 448
  (B,z), (lambda,z), (mu,z), (B,z/B), (B,z/(B+2)), (B,z/(B-2)):
    degree 2..20 even: extra_nullity = 0
  q1607-only degree-20 artifacts:
    (B,z+1/z), (B,z-1/z), and equivalent lambda/mu compressed systems
    have extra_nullity = 2

q1847:
  z_rows = 2880
  unique_B = 45
  unique_B_z = 720
  every tested system degree 2,4,6,8,10,12,14,16,18,20:
    extra_nullity = 0, except forced interpolation in small projections

q2087:
  z_rows = 1600
  unique_B = 25
  unique_B_z = 400
  every tested system degree 2,4,6,8,10,12,14,16,18,20:
    extra_nullity = 0, except forced interpolation in small projections
```

p27 sample:

```text
sample_rows = 1000
oriented_candidates_raw = 4000
z_rows = 7744
unique_B = 242
unique_B_z = 1936
every tested system degree 2,4,6,8,10,12:
  extra_nullity = 0
```

q607 smoke:

```text
z_rows = 1024
all systems degree 2,4: extra_nullity = 0
```

## Interpretation

Positive:

```text
The probe preserves the actual source root z, so it is closer to B-line
Kummer-class extraction than sign-only branch support screens.
The p27 sample and q=7 mod 16 guard fields agree on the main systems.
```

Negative:

```text
No hyperelliptic-looking relation z^2=f(B), low-degree relation in (B,z), or
low-degree branch-normalized relation appears through degree 20 in the
promotion fields.
The only q1607 compressed-coordinate artifacts do not survive q1847/q2087.
No GPU sampler follows from the obvious B-line reverse-root projections.
```

This does not prove the B-line source cover is high genus.  It kills the next
cheap plane-model shortcut and pushes the B-line route back to actual
normalization / branch-divisor / genus extraction over `P1_B`.

## Continue / Kill

```text
continue = normalize the legal+d3 source cover over P1_B
continue = compute branch degree, support field degrees, genus, and components
continue = compare f3(B), f4(B), ... only after a stable d3 class is named

kill = plane relation searches in (B,z), branch-normalized z, Belyi B, x6, r,
       z+1/z, or z-1/z as a near-term source
kill = GPU production from B-line reverse-root projections
kill = interpreting q1607-only degree-20 compressed artifacts as structure
```

```text
p27_b_line_reverse_z_relation_rows=1/1
```
