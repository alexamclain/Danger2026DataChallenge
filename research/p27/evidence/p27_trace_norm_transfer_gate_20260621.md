# P27 Trace/Norm Transfer Gate

Date: 2026-06-21

## Claim

The p26 trace/norm quotient structure transfers to p27 as exact structure,
despite the `chi(2)` flip:

```text
p26 mod 8 = 3 -> chi(2) = -1
p27 mod 8 = 7 -> chi(2) = +1
```

On the sampled p27 K-cover, all of the following survived:

```text
E_K: w^2 = -(y^2 - 2)(y^2 - 4y + 2)
t = y - 1
a = t - 1/t
b = w(t^2 + 1)/t^2
b^2 = 16 - a^4
D(gP) / D(P) = chi((y - 1)y(y - 2)) = chi(g(y) / y)
T = D * chi(y)
T(a, -b) / T(a, b) = chi(a)
T_line = T if chi(a)=+1 else T * chi(b)
domain_line = chi((y - 1)(y^2 - 2)(y^2 - 2y + 2))
```

The domain bit and target bit both descend to the same `a`-line with zero
inconsistencies in the medium diagnostic.

## Gate

Added:

```bash
python3 -m py_compile research/p27/archive/gates/p27_trace_norm_transfer_gate.py
```

Medium runs:

```bash
python3 research/p27/archive/gates/p27_trace_norm_transfer_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 512 \
  --degree 2 \
  --coeffs=-1,0,1 \
  --prefix-size 4096 \
  --top 10 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_transfer_64tid_2chunk_512draw_d2c3_20260621.txt

python3 research/p27/archive/gates/p27_trace_norm_transfer_gate.py \
  --tids 0:64 \
  --chunks 0,1 \
  --draws-per-thread 512 \
  --degree 1 \
  --coeffs=-2,-1,0,1,2 \
  --prefix-size 4096 \
  --top 10 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_transfer_64tid_2chunk_512draw_d1c5_20260621.txt
```

## Medium Result

On the standard `65,536` raw-draw diagnostic:

```text
raw_draws = 65536
nonsplit_y = 32974
K_chi_+1 = 32974
K_chi_-1 = 0
F_chi_+1 = 32780
F_chi_-1 = 33168
k_points = 65948
```

The K-cover and quotient checks are exact:

```text
neg_inv_t compare_rows = 32780
neg_inv_ratio_matches_chi_t_y_ym2 = 32780
neg_inv_ratio_matches_chi_image_y_over_y = 32780
quotient_rows = 32780
quotient_relation_fail = 0
b_flip_pairs = 16390
b_flip_ratio_matches_chi_a = 16390
```

The two line-level bits are exact:

```text
domain_line_rows = 32974
F_line_inconsistent = 0
domain_line_+1 = 16390
domain_line_-1 = 16584

target_line mode = p26_Tline
line_rows = 16390
line_inconsistent = 0
line_target_+1 = 8284
line_target_-1 = 8106
```

The visible tiny line families are negative:

```text
degree-2 domain candidate_count = 26
degree-2 domain prefix_exact_survivors = 0
degree-2 domain full_exact_count = 0

degree-2 target candidate_count = 26
degree-2 target prefix_exact_survivors = 0
degree-2 target full_exact_count = 0

degree-1 domain candidate_count = 24
degree-1 domain prefix_exact_survivors = 0
degree-1 domain full_exact_count = 0

degree-1 target candidate_count = 24
degree-1 target prefix_exact_survivors = 0
degree-1 target full_exact_count = 0
```

The best tiny basis rows are near-flat:

```text
domain best basis score ~= 0.503851519
target best basis score ~= 0.505430140
```

## Interpretation

Positive:

```text
p27 has the same trace/norm quotient shape as p26.
The chi(2) flip does not kill the EK quotient, b-flip cocycle, or a-line descent.
The live p27 prefilter is now two balanced bits on one a-line:
  domain_line(a)=+1
  T_line(a)=+1
```

Negative:

```text
Neither bit is a tiny Legendre character in the first visible basis.
Neither bit is an exact degree-1 or degree-2 small-coefficient polynomial character.
Post-filtering these two bits is not yet a sqrt-beating source sampler.
```

The sharper theorem/computation ask is:

```text
Find a non-tiny divisor, theta, additive, or parameterized identity on the
a-line of b^2 = 16 - a^4 that directly produces the simultaneous conditions
domain_line(a)=+1 and T_line(a)=+1.
```

## Continue / Kill

```text
continue = GPU/CPU telemetry should emit a, domain_line, and T_line on p27
continue = build a candidate-row evaluator for named rational functions R(a)
continue = search only theorem-shaped or branch-divisor-shaped line identities

kill = assuming the p26 chi(2) flip killed the trace/norm structure
kill = more blind tiny degree-1/2 line fitting
kill = promoting domain_line/T_line as a practical filter without per-second lift
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_trace_norm_transfer_gate.py`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_transfer_64tid_2chunk_512draw_d2c3_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_transfer_64tid_2chunk_512draw_d1c5_20260621.txt`
- Plan: [P27 Transfer Plan](p27_p26_trace_norm_transfer_plan_20260621.md)

```text
p27_trace_norm_transfer_gate_rows=1/1
```

