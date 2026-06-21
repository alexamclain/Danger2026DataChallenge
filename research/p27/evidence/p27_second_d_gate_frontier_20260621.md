# P27 Second-D Gate Frontier

Date: 2026-06-21

## Claim

After the first-halving/domain gate, the next obstruction is cleanly another
Montgomery `d` squareclass:

```text
d2 = x5^2 + A*x5 + 1
```

where `x5` is the selected first half of the original X1(16) point.  The
current `T_line`, p24 label2 quotient features, residual classes, H90
orientation, and small quotient-line characters do not predict this second
`d` gate on p27.

This is now the concrete post-domain moonshot target.

Follow-up tower profiling extended this beyond `d2`: through eight selected
halving gates, the observed obstruction is always the next `d_j` squareclass,
with no `d_j` square / `w` failures and no two-`w` branches.  See
[P27 Selected Halving Tower Profile](p27_halving_tower_profile_20260621.md).

## Code

Added a bounded gate profiler to `src/pomerance.c`:

```text
halve_once_gate_profile128
```

and extended `x16halvestatsnonsplittraceline` with:

```text
trace_norm_post_domain_next_gate
```

The table distinguishes:

```text
first_gate_fail
next_d_nonsquare
next_d_square_w_none
next_pass_one_w
next_pass_two_w
```

## Same-Stream P27 Result

Run:

```bash
./src/pomerance 1000000000000000000000000103 \
  127 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_postgate_seed127_1M_20260621.txt
```

Result:

```text
domain_minus:
  first_gate_fail = 499466 / 499466

domain_plus_Tline_minus:
  next_d_nonsquare    = 125524 / 250374 = 0.501345986
  next_d_square_w_none = 0
  next_pass_one_w     = 124850 / 250374 = 0.498654014
  next_pass_two_w     = 0

domain_plus_Tline_plus:
  next_d_nonsquare    = 124598 / 250160 = 0.498073233
  next_d_square_w_none = 0
  next_pass_one_w     = 125562 / 250160 = 0.501926767
  next_pass_two_w     = 0
```

Interpretation:

```text
T_line is flat against the second-d gate.
Once d2 is square, the selected branch has exactly one good w root in this
sample; there are no d-square/w-none failures and no two-w successes.
```

## P24 Label2 Harness Reuse

Run:

```bash
./src/pomerance 1000000000000000000000000103 \
  128 100000 x16label2depth6stats 20 \
  | tee research/p27/archive/probe_outputs/p27_label2_depth6_seed128_100k_20260621.txt
```

Result:

```text
d_nonsquare = 50092
w_none      = 0
plus_only   = 24788
minus_only  = 25120
both        = 0
```

The old p24 label2 feature screen is negative on p27:

```text
den_class, cover factors, quotient features, residual_w features,
H90 orientation, and E0_mod3 classes all stay near 50% for depth6_success.
```

The H90 orientation is not the second-d selector:

```text
h90_orientation_mismatch = 50086 / 100000
```

## Small Quotient-Line Sweep

Run:

```bash
./src/pomerance 1000000000000000000000000103 \
  129 50000 x16label2depth6qlinestats 3 \
  | tee research/p27/archive/probe_outputs/p27_label2_depth6_qline_seed129_50k_bound3_20260621.txt
```

This tests the tiny family:

```text
chi(V + aU + b),  -3 <= a,b <= 3
```

Result:

```text
No exact or high-lift tiny quotient line.
Largest absolute split in the 50k screen was about 0.017, consistent with
small-sample fluctuation and far below a promotion bar.
```

## Interpretation

Positive:

```text
The post-domain problem is now sharply named: compute or predict chi(d2).
The first two halving layers are both clean d-square gates for this p27 path:
  domain_line = chi(d1)
  second target = chi(d2)
```

Negative:

```text
T_line is not chi(d2).
The reused p24 label2/H90 visible feature set is not chi(d2).
Tiny quotient-line characters V+aU+b are not chi(d2).
```

## Concrete Next Tests

1. GPU practical A/B:

```text
baseline X1(16)
vs domain_line first-d filter
vs domain_line + second-d filter, if the GPU can compute d2 cheaply
```

Report per GPU-second throughput and survivor lift.  This is practical
filtering; by itself it is still constant-factor, not sqrt-beating.

2. Algebraic target:

```text
derive d2 as a squareclass on the depth-5 / label2 cover
test named formulas only:
  quotient variables U,V
  residual coordinates X,W
  H90 orientation class
  theta/Kummer/2-descent functions tied to the second 2-cover
```

3. True moonshot test:

```text
look for a recurrence or tower law for chi(d_j) after the first domain gate.
One or two extra d-gates gives constants; a submit-worthy sqrt-beating route
needs a way to generate a long chain of d_j=+1 without paying one random
Legendre test per layer.
```

4. Expert/literature ask:

```text
On the X1(16) Montgomery halving tower, is the squareclass of the next
preimage discriminant d_j = x_j^2 + A*x_j + 1 a known theta/Kummer/2-descent
character on the iterated 2-cover?  For p27, the first such character is
domain_line; we need the second one, chi(d2), in quotient/source coordinates.
```

## Continue / Kill

```text
continue = second-d formula or source sampler
continue = GPU report domain+second-d only if it is cheap in the native code
continue = ask experts about iterated 2-cover discriminant characters

kill = T_line as the second-d predictor
kill = p24 label2 visible feature set as already implemented
kill = tiny V+aU+b quotient-line scans without a named theorem
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_trace_norm_postgate_seed126_100k_smoke_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_postgate_seed127_1M_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_depth6_seed128_100k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_depth6_qline_seed129_50k_bound3_20260621.txt`
- Related: [P27 Domain Line Equals First-Halving Gate](p27_domain_first_halving_gate_20260621.md)
- Related: [P27 Post-Domain Next-Gate Telemetry](p27_post_domain_next_gate_telemetry_20260621.md)

```text
p27_second_d_gate_frontier_rows=1/1
```
