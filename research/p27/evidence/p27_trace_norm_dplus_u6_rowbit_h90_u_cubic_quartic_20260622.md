# P27 Trace/Norm Dplus U6 Row-Bit H90 U Cubic/Quartic Screen

Date: 2026-06-22

## Claim

The H90-soluble Dplus row-bit sign descends to the even coordinate

```text
u = 4/(t - 1/t)^2
```

but it is not explained by visible monic cubic support in
`q607/q1607/q1847/q2087`, nor by visible monic quartic support in the decisive
promotion field `q1847`.

Together with the prior degree `<= 2` screen, this kills the visible monic
`P^1_u` source through degree `4` in `q1847`.  The row-bit lane should move to
non-visible divisor/theta/Prym extraction rather than another visible
low-degree polynomial hunt.

## Artifacts

Target packet:

```text
research/p27/archive/fixtures/p27_dplus_rowbit_u_divisor_targets_20260622.json
```

Oracles:

```text
research/p27/archive/gates/p27_cubic_chunk_fast.c
research/p27/archive/gates/p27_quartic_chunk_fast.c
research/p27/archive/gates/p27_dplus_rowbit_u_lowgenus_verify.py
research/p27/archive/gates/p27_quartic_target_export.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_dplus_rowbit_u_cubic_20260622/
research/p27/archive/probe_outputs/p27_dplus_rowbit_u_quartic_q1847_20260622/
```

## Commands

Cubic compile:

```bash
cc -O3 -o /tmp/p27_cubic_chunk_fast \
  research/p27/archive/gates/p27_cubic_chunk_fast.c
```

Quartic compile:

```bash
cc -O3 -o /tmp/p27_quartic_chunk_fast \
  research/p27/archive/gates/p27_quartic_chunk_fast.c
```

Row export pattern:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 research/p27/archive/gates/p27_quartic_target_export.py \
  --coordinate u \
  --field <q> \
  --family dplus_h90_soluble_rowbit_u \
  > research/p27/archive/probe_outputs/<run>/u_<q>_rows.txt
```

Cubic scans were run as full single chunks over `q^2` coefficient pairs:

```bash
/tmp/p27_cubic_chunk_fast u_<q>_rows.txt 0 <q^2>
```

The q1847 quartic scan was run in eight parallel chunks over all
`1847^3 = 6300872423` triples:

```bash
/tmp/p27_quartic_chunk_fast u_1847_rows.txt <start> <count>
```

## Results

```text
field   degree   rows   candidates    exact
607     3        32     368449        0
1607    3        50     2582449       0
1847    3        64     3411409       0
2087    3        57     4355569       0
1847    4        64     6300872423    0
```

Quartic q1847 summary:

```text
p27 Dplus row-bit u quartic q1847 full screen
field = 1847
rows = 64
triples_scanned = 6300872423
polarity_-1_hits = 0
polarity_1_hits = 0
exact_quartics = 0
max_elapsed_seconds = 602.496965
sum_throughput_triples_per_second = 10567112.940
p27_dplus_rowbit_u_quartic_q1847_rows=1/1
```

All cubic outputs ended with:

```text
exact_cubics = 0
p27_cubic_chunk_fast_rows=1/1
```

## Interpretation

Positive:

```text
The descent to u remains real and useful: every tested materialized target row
has a single row-bit sign per u.
The exact-support problem is now bounded and reproducible from a frozen packet.
```

Negative:

```text
Visible monic cubic support is absent in q607/q1607/q1847/q2087.
Visible monic quartic support is absent in q1847, where a random exact quartic
would be expected only about 6.31e-7 times.
The q1847 promotion route for monic degree <= 4 on P^1_u is therefore closed.
```

## Consequence

Do not ask the GPU agent to run q1847 cubic/quartic `u` exact support again.
The q2087 quartic screen is optional closure if a GPU is already warm, but by
itself it should not override the q1847 kill unless it yields a named
field-independent divisor/class.

The next useful row-bit work is:

```text
extract the non-visible divisor/theta/Prym class on the H90/u-line cover;
compare that class with the pulled-back A-level d3/x6 squareclass;
keep Dplus fused pricing as a separate engineering test.
```

## Continue / Kill

```text
continue = optional q2087 quartic closure only if cheap
continue = non-visible theta/Prym/divisor extraction for the descended u class
continue = CAS comparison between the u row-bit class and A-level d3/x6

kill = monic cubic u-divisors in q607/q1607/q1847/q2087
kill = monic quartic u-divisors in q1847
kill = visible monic P^1_u support through degree 4 as a GPU target
```

```text
p27_trace_norm_dplus_u6_rowbit_h90_u_cubic_quartic_rows=1/1
```
