# X1(16) Exact v2 Distribution Calibration

Date: 2026-06-02 PDT

Purpose: sharpen the remaining probability uncertainty for the active p23
nonsplit run.

The prior audit showed:

```text
inside nonsplit X1(16), marked-point halving depth = v2(#E(Fp))
```

So the active run is testing a real curve-level event:

```text
v2(#E(Fp)) >= 39
```

The remaining question is whether shallow p23 diagnostics and small-prime
calibrations give a reasonable picture of the high-v2 tail.

## Helper

Script:

```text
scripts/x16_exact_v2_distribution.py
```

The helper exactly enumerates the accepted `X1(16)` candidate stream over a
small prime, with multiplicity matching the sampler's quadratic fiber roots.
For each unique Montgomery `A`, it brute-counts `#E(Fp)`, computes
`v2(#E(Fp))`, and reports the distribution by split/nonsplit class.

This is exact for the listed small primes. It is not a p23 point counter.

## New Run

The first added calibration prime:

```text
p = 30517
p mod 120 = 37 = p23 mod 120
```

Command:

```bash
nice -n 19 python3 scripts/x16_exact_v2_distribution.py --p 30517 \
  | tee runs/x16_exact_v2_distribution_20260602/p30517_mod120_37.log
```

Result:

```text
elapsed_seconds = 174.330098
rows = 30344
unique_A = 5215
split_class_counts = nonsplit:15136, split:15208

nonsplit v2 histogram:
  v2=4:  7448
  v2=5:  3928
  v2=6:  1976
  v2=7:   712
  v2=8:   336
  v2=9:   224
  v2=11:  512

split v2 histogram:
  v2=5:  3928
  v2=6:  5928
  v2=7:  2136
  v2=8:  1008
  v2=9:   672
  v2=11: 1536
```

Threshold rates:

```text
d   nonsplit Pr[v2>=d]   split Pr[v2>=d]
5      0.507928             1.000000
6      0.248414             0.741715
7      0.117865             0.351920
8      0.070825             0.211468
9      0.048626             0.145187
10     0.033827             0.100999
11     0.033827             0.100999
12     0.000000             0.000000
```

## Additional Larger Row

The next larger exact p23-residue row:

```text
p = 35317
p mod 120 = 37 = p23 mod 120
```

Command:

```bash
nice -n 19 python3 scripts/x16_exact_v2_distribution.py --p 35317 \
  | tee runs/x16_exact_v2_distribution_20260602/p35317_mod120_37.log
```

Result:

```text
elapsed_seconds = 241.502239
rows = 35144
unique_A = 6070
split_class_counts = nonsplit:17728, split:17416

nonsplit v2 histogram:
  v2=4: 8936
  v2=5: 4480
  v2=6: 2296
  v2=7:  936
  v2=8:  600
  v2=9:  480

split v2 histogram:
  v2=5: 4480
  v2=6: 6888
  v2=7: 2808
  v2=8: 1800
  v2=9: 1440
```

Threshold rates:

```text
d   nonsplit Pr[v2>=d]   split Pr[v2>=d]
5      0.495939             1.000000
6      0.243231             0.742765
7      0.113718             0.347267
8      0.060921             0.186036
9      0.027076             0.082683
10     0.000000             0.000000
11     0.000000             0.000000
12     0.000000             0.000000
```

Against the geometric baseline `2^(4-d)`, the nonsplit ratios are:

```text
d=5  0.992
d=6  0.973
d=7  0.910
d=8  0.975
d=9  0.866
d=10 0.000
```

## All Exact p23-Residue Rows

The exact p23-residue rows currently available are:

```text
p=3037, rows=3000
  d=5  nonsplit=0.492147  nonsplit/geometric=0.984  split=1.000000
  d=6  nonsplit=0.235602  nonsplit/geometric=0.942  split=0.733696
  d=7  nonsplit=0.109948  nonsplit/geometric=0.880  split=0.342391
  d=8  nonsplit=0.062827  nonsplit/geometric=1.005  split=0.195652
  d=9  nonsplit=0.062827  nonsplit/geometric=2.010  split=0.195652
  d=10 nonsplit=0.062827  nonsplit/geometric=4.021  split=0.195652

p=10357, rows=10504
  d=5  nonsplit=0.492331  nonsplit/geometric=0.985  split=1.000000
  d=6  nonsplit=0.260736  nonsplit/geometric=1.043  split=0.771558
  d=7  nonsplit=0.165644  nonsplit/geometric=1.325  split=0.490166
  d=8  nonsplit=0.101227  nonsplit/geometric=1.620  split=0.299546
  d=9  nonsplit=0.059816  nonsplit/geometric=1.914  split=0.177005
  d=10 nonsplit=0.059816  nonsplit/geometric=3.828  split=0.177005

p=21157, rows=20864
  d=5  nonsplit=0.489521  nonsplit/geometric=0.979  split=1.000000
  d=6  nonsplit=0.231287  nonsplit/geometric=0.925  split=0.728774
  d=7  nonsplit=0.110030  nonsplit/geometric=0.880  split=0.346698
  d=8  nonsplit=0.032186  nonsplit/geometric=0.515  split=0.101415
  d=9  nonsplit=0.014970  nonsplit/geometric=0.479  split=0.047170

p=30517, rows=30344
  d=5  nonsplit=0.507928  nonsplit/geometric=1.016  split=1.000000
  d=6  nonsplit=0.248414  nonsplit/geometric=0.994  split=0.741715
  d=7  nonsplit=0.117865  nonsplit/geometric=0.943  split=0.351920
  d=8  nonsplit=0.070825  nonsplit/geometric=1.133  split=0.211468
  d=9  nonsplit=0.048626  nonsplit/geometric=1.556  split=0.145187
  d=10 nonsplit=0.033827  nonsplit/geometric=2.165  split=0.100999

p=35317, rows=35144
  d=5  nonsplit=0.495939  nonsplit/geometric=0.992  split=1.000000
  d=6  nonsplit=0.243231  nonsplit/geometric=0.973  split=0.742765
  d=7  nonsplit=0.113718  nonsplit/geometric=0.910  split=0.347267
  d=8  nonsplit=0.060921  nonsplit/geometric=0.975  split=0.186036
  d=9  nonsplit=0.027076  nonsplit/geometric=0.866  split=0.082683
  d=10 nonsplit=0.000000  nonsplit/geometric=0.000  split=0.000000
```

Here:

```text
geometric baseline at depth d = 2^(4-d)
```

because `X1(16)` already forces `v2(#E) >= 4`.

## Interpretation

What improved:

```text
The new p=30517 and p=35317 exact rows give larger p23-residue calibration
points and do not show an early nonsplit tail collapse.
```

The nonsplit stream is very close to the simple geometric tail at depths 5-7
on all five exact p23-residue rows:

```text
d=5: roughly 0.49-0.51
d=6: roughly 0.23-0.26
d=7: roughly 0.11-0.17
```

That supports the idea that nonsplit `v2(#E)` is not a branch artifact and is
not immediately hostile to high 2-adic liftability.

What remains risky:

```text
Depths above 7 are visibly p-specific. The p=21157 and p=35317 rows cut off
by depth 10, while p=3037, p=10357, and p=30517 have plateaus at higher v2
values.
```

This is expected from the finite Hasse interval and exact trace lattice, but
it means these small primes cannot prove the p23 depth-39 tail.

## Probability Impact

This calibration mildly supports the active nonsplit model:

```text
it weakens the fear that nonsplit high-v2 mass collapses immediately after the
forced X1(16) depth. The p=35317 row is especially useful here: it is larger
than p=30517 and still stays close to geometric through depth 8.
```

It does not justify narrowing the `L` prior:

```text
the target depth is 39, and the exact small-prime rows only see tails up to
about depth 10-11.
```

Operationally:

```text
keep active y-filtered nonsplit X1(16) running while decision=keep_waiting
do not restart for split or generic X1(32)
if 50B misses cleanly, use the guarded direct-y nonsplit follow-on
```

Research-wise, the missing object remains:

```text
a cheap p23-scale exact or high-capture label for curve-level v2(#E)
```
