# P27 Trace/Norm Dplus U6 Row-Bit Resultant

Date: 2026-06-22

## Claim

After `Dplus`, the post-gate class is not a four-way `U6` branch-choice bit.
It descends to a single balanced bit on each Dplus row.

For every analyzed p27 Dplus row in the two standard seed groups, the four
reciprocal `U6=x6+1/x6` values all have the same squareclass:

```text
chi(U6 + 2) = chi(x6).
```

So the live test is now sharper:

```text
source or identify the descended Dplus row bit,
not choose a better U6 branch.
```

The exact symbolic resultant supports the same boundary.  Eliminating `U5`
from

```text
F_A(X(t),U5) = 0
F_A(U5,U6) = 0
```

gives a degree-16 `U6` equation whose `U6=+/-2` specializations are perfect
even-power products, but the Kummer lift `U6=S^2-2` does not factor over `Q`
in this screen.

## Artifacts

Telemetry probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_parity_probe.py
```

Telemetry output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_parity_probe_20260622.txt
```

Symbolic probe:

```text
research/p27/archive/gates/p27_trace_norm_dplus_u6_symbolic_resultant_probe.py
```

Symbolic output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_symbolic_resultant_probe_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_parity_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-y 0 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_parity_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_u6_symbolic_resultant_probe.py \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_u6_symbolic_resultant_probe_20260622.txt
```

## Telemetry Result

```text
group   analyzed_y   U6 mixed rows   U6 ++++   U6 ----   product +1
1       8199         0               4149      4050      8199
2       8061         0               3986      4075      8061
```

Full counters:

```text
group1:
  raw_y_draws = 131072
  nonsplit_y = 65766
  Dplus_y = 16485
  analyzed_y = 8199
  U6_count_4 = 8199
  U6_pattern_++++ = 4149
  U6_pattern_---- = 4050
  U6_uniform_sign = 8199
  U6_sign_product_+1 = 8199

group2:
  raw_y_draws = 131072
  nonsplit_y = 65470
  Dplus_y = 16454
  analyzed_y = 8061
  U6_count_4 = 8061
  U6_pattern_++++ = 3986
  U6_pattern_---- = 4075
  U6_uniform_sign = 8061
  U6_sign_product_+1 = 8061
```

There are no mismatch counters for:

```text
candidate_A_formula_mismatch
X_formula_mismatch
F_X_U5_mismatch
F_U5_U6_mismatch
x6_u6plus2_mismatch
U6_duplicate_sign_mismatch
d1_failure
d2_failure
```

## Symbolic Result

With

```text
A = (t - 1/t)^4/4 - 2
X = t^3 + 2*t^2 - 1/t
```

the eliminated polynomial

```text
R(t,U6) = Res_U5(F_A(X,U5), F_A(U5,U6))
```

has:

```text
degree_t = 72
degree_U6 = 16
terms = 617
factorization over Q = t^8 * irreducible(degree_t=64, degree_U6=16)
```

The branch specializations are exact even-power products:

```text
R(t, 2)  = t^8 * (t-1)^32 * (t+1)^32
R(t,-2)  = t^8 * (t^2-2t-1)^8 * (t^2+2t-1)^8 * (t^2+1)^16
```

But the Kummer lift stays irreducible in this rational factor screen:

```text
R(t, S^2-2) = t^8 * irreducible(degree_t=64, degree_S=32)
```

## Interpretation

Positive:

```text
The post-Dplus x6/U6 class descends from four U6 branches to one row bit.
This is genuine mathematical structure, not just a throughput observation.
The exact resultant records square norm at U6+2 and U6-2.
```

Negative:

```text
The descended row bit is balanced on p27 samples.
The S^2=U6+2 lift does not visibly split over Q.
Simple H90/rho coboundaries were already killed on the same target.
This is not yet a source-space shrink or GPU production mode.
```

## Consequence

The next Dplus moonshot test is:

```text
compute the Kummer/Prym class of the descended U6 row bit over the selected
Dplus/H90 base, and decide whether it is A_eta, a coboundary, a quotient class,
or a fresh independent cover.
```

For GPU, fused/native `Dplus` telemetry should emit one post-Dplus row bit per
`y` with raw source denominators.  It should not fan out into four branch
buckets or treat branch choice as the missing win.

## Continue / Kill

```text
continue = exact CAS/Prym comparison of the descended U6 row bit with A_eta
continue = selected-source A/B/K Kummer extraction using this Dplus pullback
continue = fused/native Dplus pricing with one d3 row-bit column

kill = U6 branch-choice buckets after Dplus
kill = visible rational factorization of R(t,S^2-2) over Q as the easy source
kill = GPU production from chi(U6+2) before the row bit is sourced
```

```text
p27_trace_norm_dplus_u6_rowbit_resultant_rows=1/1
```
