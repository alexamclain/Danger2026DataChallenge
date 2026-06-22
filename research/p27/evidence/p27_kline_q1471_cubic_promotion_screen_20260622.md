# P27 K-Line q1471 Cubic Promotion Screen

Date: 2026-06-22

## Claim

The simplest genus-1 K-line source shape is killed in the first promotion
field.

The tested shape is:

```text
z^2 = cubic(K)
K = x([2]P) on E': V^2 = U^3 + 4U
chi(cubic(K)) = d3
```

Over `q=1471`, there is no exact monic cubic matching the descended `d3`
K-line target, even allowing a global polarity.  Since a nonzero leading
coefficient only changes the global squareclass/polarity, and degree `<=2`
was already killed, this rules out degree-3 K-polynomial characters over the
first promotion field.

## Artifact

Probe:

```text
research/p27/archive/gates/p27_kline_cubic_stdin_probe.c
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q1471_20260622.txt
```

Command:

```bash
cc -O3 -o tmp/p27_kline_cubic_stdin_probe \
  research/p27/archive/gates/p27_kline_cubic_stdin_probe.c

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 - <<'PY' | ./tmp/p27_kline_cubic_stdin_probe \
  | tee research/p27/archive/probe_outputs/p27_kline_cubic_stdin_probe_q1471_20260622.txt
from p27_k_belyi_involution_probe import collect_rows
q=1471
kd3, _kd4, _sd3, _sd4, _stats = collect_rows(q)
print(q, len(kd3))
for row in kd3:
    print(row.k, row.target)
PY
```

## Result

```text
q = 1471
rows = 50
plus = 28
minus = 22
tested_monic_cubics = 3183010111
exact_cubics = 0
exact_irreducible_cubics = 0
best good = 46/50
best coeffs = K^3 + 624*K^2 + 250*K + 250
```

The fit-significance calibration expected only about `5.65e-6` exact monic
cubics under random signs, so a positive would have been highly meaningful.
The negative result is therefore a clean falsifier for the cubic source shape,
not a small-field ambiguity.

## Interpretation

Positive:

```text
The q1471 promotion-field test is exact and bounded.
The result removes the nearest genus-1 cubic source without relying on tiny
fields or small-integer coefficient restrictions.
```

Negative:

```text
No source of the form z^2 = cubic(K) appears in q1471.
The q863 exact cubics are confirmed as local interpolation artifacts.
The K-line path now needs quartic/genus extraction or a non-polynomial branch
class, not more cubic fitting.
```

## Next Tests

Continue:

```text
Magma/Sage branch-cover normalization over P1_K/P1_Sroot
quartic or higher branch-class extraction in q1471/q1607/q1847
genus and support-degree computation for the recovered d3 cover
```

Demote:

```text
monic/nonzero-leading cubic K-polynomial source for d3
q863 cubic formulas
near-miss q1471 best score 46/50
```

Promotion remains:

```text
exact quartic or branch class stable in q1471/q1607/q1847
genus <= 1 quotient or sourceable walk
named recurrence coupling d4 to the recovered d3 class
```

```text
p27_kline_q1471_cubic_promotion_screen_rows=1/1
```
