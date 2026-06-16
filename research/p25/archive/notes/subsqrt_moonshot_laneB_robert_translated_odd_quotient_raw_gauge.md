# Subsqrt Moonshot Lane B Robert/Siegel Translated Odd Quotient Raw Gauge

Date: 2026-06-13

## Result

After the visible quotient factorization is fixed, the remaining raw-source
freedom is exactly kernel gauge.

The kernel shift is:

```text
K = (57,0) in C_75 x C_169
```

For the forward quotient factorization:

```text
base=(25,25)
D=(22,3)
T=(38,113)
```

all choices:

```text
base + i*K
D    + j*K
T    + k*K
```

with `0 <= i,j,k < 25` give the exact bridge.

The reversed `D` segment has the same count.  Total valid raw gauges:

```text
2 * 25^3 = 31250
```

## Controls

Simple non-kernel perturbations fail:

```text
base + (0,1)
D    + (0,1)
T    + (0,1)
base + (1,0)
D    + (1,0)
T    + (1,0)
```

for both the forward and reversed `D` segment.

## Consequence

A Robert/Siegel producer can choose any raw representative in the kernel class,
but it cannot hide a different raw edge, segment, or base outside that class.

This is useful for source-matrix intake: if a Kato-Siegel or `y`/differential
quotient emits raw coordinates, we should normalize only by kernel gauge, not
by arbitrary raw relabeling.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py
```
