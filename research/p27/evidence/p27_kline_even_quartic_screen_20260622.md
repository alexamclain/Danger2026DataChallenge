# P27 K-Line Even-Quartic Screen

Date: 2026-06-22

## Claim

The descended even-quartic subfamily

```text
chi(K^4 + a*K^2 + b)
```

does not explain the p27 K-line `d3` or `d4` target bits in the promotion
fields q1471/q1607/q1847.

This kills the cheap `K^2`-descended quartic shortcut.  Any surviving K-line
quartic source must use odd powers of `K`, hence the signed K sheet rather
than only the bridge coordinate `K^2`.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_even_quartic_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_even_quartic_probe_q1471_q1607_q1847_20260622.txt
```

Frozen target packet:

```text
research/p27/archive/fixtures/p27_kline_quartic_targets_20260622.json
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_kline_even_quartic_probe.py \
  --small-primes 1471,1607,1847 \
  --families d3_on_K,d4_on_K_after_d3 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_even_quartic_probe_q1471_q1607_q1847_20260622.txt
```

## Results

All tested fields and families had zero exact even quartics:

```text
q1471 d3_on_K:          rows=50, pairs=2,163,841, exact_even_quartics=0
q1607 d3_on_K:          rows=49, pairs=2,582,449, exact_even_quartics=0
q1847 d3_on_K:          rows=63, pairs=3,411,409, exact_even_quartics=0

q1471 d4_on_K_after_d3: rows=28, pairs=2,163,841, exact_even_quartics=0
q1607 d4_on_K_after_d3: rows=28, pairs=2,582,449, exact_even_quartics=0
q1847 d4_on_K_after_d3: rows=45, pairs=3,411,409, exact_even_quartics=0
```

Crude random expected exact counts for the decisive d3 rows are already tiny:

```text
q1471 d3: 3.84e-9
q1607 d3: 9.17e-9
q1847 d3: 7.40e-13
```

The negative result is therefore not surprising statistically.  Its value is
structural: it tells the GPU agent not to spend time on the much smaller
descended-only subfamily.

## Interpretation

Positive:

```text
The full K-line q1847 d3 screen had to include odd K terms.
The completed negative screen cannot be blamed on the trivial even subcase.
```

Negative:

```text
Do not test only chi(K^4+a*K^2+b) on GPU.
Do not treat K^2 alone as the current K-line source coordinate.
```

Continue:

```text
use full monic quartic oracle only for closure/hit verification
otherwise move to normalized branch/genus/Kummer extraction
```

Kill:

```text
the cheap K^2-descended even-quartic shortcut
```

```text
p27_kline_even_quartic_screen_rows=1/1
```
