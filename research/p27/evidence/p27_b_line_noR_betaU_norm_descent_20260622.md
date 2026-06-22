# P27 B-Line No-R Beta_U Norm Descent

Date: 2026-06-22

## Claim

The `beta_U_fixedB` subcover has a real quadratic norm descent:

```text
chi_GF(q^2)(Unext + 2) = chi_GF(q)(Norm_GF(q^2)/GF(q)(Unext + 2))
```

with zero mismatches in the tested guard fields.  More importantly, the
selected sign is uniform on each active base `B` row and matches the beta_U
fiber size:

```text
gamma = +1  <=>  16 beta_U points over B
gamma = -1  <=>  32 beta_U points over B
```

This is not yet a sampler, but it is a concrete structural target: extract the
divisor class of `Norm(Unext + 2)` on the `chi(B)=+1` beta_U support and ask
whether the half-size/full-size split is a quotient or Prym factor.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_betaU_norm_descent_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_descent_probe_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_descent_probe_q199_q263_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_descent_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_descent_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_betaU_norm_descent_probe.py \
  --fields 199^2,263^2 \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_betaU_norm_descent_probe_q199_q263_20260622.txt
```

## Result

Norm descent:

```text
fields = 23^2, 71^2, 103^2, 167^2, 199^2, 263^2
gamma_norm_mismatch = 0 in every field
```

Support:

```text
all beta_U_fixedB points have chi(B)=+1
```

Fiber-size/sign profile:

```text
field    active B   gamma+ B      gamma- B      beta_U points
23^2     2          0             2             64
71^2     8          8             0             128
103^2    12         0             12            384
167^2    20         6             14            544
199^2    24         16            8             512
263^2    32         12            20            832
```

In the detailed summaries, every `gamma+` active base row has `16` beta_U
points and every `gamma-` active base row has `32` beta_U points.

Norm-value profile:

```text
gamma+ rows: norm-value counts per B are 1 or 8
gamma- rows: norm-value counts per B are 9, 12, 14, or 16
```

This suggests the selected sign is tied to a splitting/branch profile inside
the beta_U subcover, not to an arbitrary pointwise filter.

## Interpretation

Positive:

```text
beta_U_fixedB is now a named Kummer descent target, not just a bucket.
The selected class descends through Norm(Unext+2) to the base field.
The selected sign is uniform per active B row.
The selected sign matches the half-size/full-size beta_U fiber split.
```

Negative:

```text
Norm descent is a theorem of quadratic finite fields, not by itself a sampler.
The base-B visible character screen already showed no stable low-degree gamma law.
The half-size/full-size split still needs divisor/class extraction.
No GPU production mode follows from the norm identity alone.
```

## CAS Consequence

The `beta_U_fixedB` subtest is now:

```text
work on the chi(B)=+1 support
construct the norm class N_B = Norm(Unext + 2)
compute div(N_B) modulo squares on the beta_U quotient/base
explain the 16-point vs 32-point fiber split
test whether that split is a low-genus quotient/Prym factor or a fresh Kummer class
```

Promote only if this norm class gives a direct source map, recurrence, or
low-genus quotient carrying gamma or coupling f3/f4.

## Continue / Kill

```text
continue = beta_U divisor/Kummer extraction for Norm(Unext+2)
continue = explain gamma+ half-size vs gamma- full-size fiber split
continue = compare the beta_U norm class with f4/f3 after normalization

kill = treating chi(B)=+1 support alone as a sampler
kill = treating norm descent alone as sqrt-beating
kill = GPU production before the norm class becomes a named source map
```

```text
p27_b_line_noR_betaU_norm_descent_rows=1/1
```
