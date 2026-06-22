# P27 K-Line Belyi-Reciprocal Quartic Screen

Date: 2026-06-22

## Claim

The nearest Belyi-symmetric quartic subfamily on the p27 K-line is negative in
the promotion fields q1471/q1607/q1847.

For the visible involution `K -> 4/K`, a monic quartic whose branch divisor is
preserved must satisfy

```text
K^4*f(4/K) = s*16*f(K),  s in {+1, -1}.
```

Thus the two reciprocal quartic shapes are:

```text
K^4 + a*K^3 + b*K^2 + 4*a*K + 16
K^4 + a*K^3 - 4*a*K - 16
```

Exhausting both shapes gives zero exact hits for both `d3_on_K` and
`d4_on_K_after_d3`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_reciprocal_quartic_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_reciprocal_quartic_probe_q1471_q1607_q1847_20260622.txt
```

Frozen target packet:

```text
research/p27/archive/fixtures/p27_kline_quartic_targets_20260622.json
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_kline_reciprocal_quartic_probe.py \
  --small-primes 1471,1607,1847 \
  --families d3_on_K,d4_on_K_after_d3 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_reciprocal_quartic_probe_q1471_q1607_q1847_20260622.txt
```

## Results

All tested fields and families had zero exact Belyi-reciprocal quartics:

```text
q1471 d3_on_K:          rows=50, shapes=2,165,312, exact=0
q1607 d3_on_K:          rows=49, shapes=2,584,056, exact=0
q1847 d3_on_K:          rows=63, shapes=3,413,256, exact=0

q1471 d4_on_K_after_d3: rows=28, shapes=2,165,312, exact=0
q1607 d4_on_K_after_d3: rows=28, shapes=2,584,056, exact=0
q1847 d4_on_K_after_d3: rows=45, shapes=3,413,256, exact=0
```

Crude random expected exact counts for the decisive d3 rows are tiny:

```text
q1471 d3: 3.85e-9
q1607 d3: 9.18e-9
q1847 d3: 7.40e-13
```

As with the even-quartic screen, the negative result is not statistically
surprising.  Its value is structural: the full GPU quartic search should not
be replaced by the smaller Belyi-reciprocal subfamily.

## Interpretation

Positive:

```text
The K-line quartic handoff is now narrower and cleaner.
The obvious low-dimensional reciprocal subfamilies inside the full quartic
search are exhausted.
```

Negative:

```text
Do not spend GPU time only on Belyi-reciprocal quartics.
Do not expect the K -> 4/K involution to provide the missing quartic source.
```

Continue:

```text
bounded GPU exact support for full monic quartics
chi(K^4+aK^3+bK^2+cK+d)
```

Kill:

```text
Belyi-reciprocal K-line quartics as the p27 d3/d4 source
```

```text
p27_kline_reciprocal_quartic_screen_rows=1/1
```
