# P27 Selected Halving Tower Profile

Date: 2026-06-21

## Claim

For the selected first-branch p27 path, the first eight halving gates behave as
independent-looking Montgomery discriminant squareclass gates:

```text
d_j = x_j^2 + A*x_j + 1
```

On the measured p27 stream, a gate either fails because `d_j` is nonsquare or
passes with exactly one good `w` root.  No `d_j` square / `w` failures and no
two-`w` branches were observed through gate `8`.

Follow-up: this is explained by a nonsplit Montgomery identity, not merely an
empirical pattern.  For the two `w` candidates,
`w_+*w_-=16*x^2*(A^2-4)`, so on nonsplit rows exactly one `w` branch is square
whenever `d_j` is square.  See
[P27 Nonsplit W-Obstruction Identity](p27_nonsplit_w_obstruction_identity_20260621.md).

This makes the moonshot sharper:

```text
constant-factor practical filter = precompute/test a fixed prefix of d_j bits
sqrt-beating theorem = produce or certify many d_j=+1 bits without paying a
random Legendre test per layer
```

## Code

Extended `x16halvestatsnonsplittraceline` with:

```text
trace_norm_halving_gate_profile
```

Each row reports gate `1..8`, start depth, and one of:

```text
next_d_nonsquare
next_d_square_w_none
next_pass_one_w
next_pass_two_w
```

## Run

```bash
./src/pomerance 1000000000000000000000000103 \
  131 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_multigate_seed131_1M_20260621.txt
```

## Result

As before, `domain_minus` is exactly gate-1 `d_1` nonsquare:

```text
domain_minus gate=1 samples=499956
  next_d_nonsquare = 499956
```

Inside `domain_line=+1`, both `T_line` classes show the same pattern.  For
`domain_plus_Tline_minus`:

```text
gate 1 start_depth=4 samples=249434 pass_one_w=249434
gate 2 start_depth=5 samples=249434 d_nonsquare=124540 pass_one_w=124894
gate 3 start_depth=6 samples=124894 d_nonsquare=62188  pass_one_w=62706
gate 4 start_depth=7 samples=62706  d_nonsquare=31350  pass_one_w=31356
gate 5 start_depth=8 samples=31356  d_nonsquare=15576  pass_one_w=15780
gate 6 start_depth=9 samples=15780  d_nonsquare=7970   pass_one_w=7810
gate 7 start_depth=10 samples=7810  d_nonsquare=3944   pass_one_w=3866
gate 8 start_depth=11 samples=3866  d_nonsquare=1910   pass_one_w=1956
```

For `domain_plus_Tline_plus`:

```text
gate 1 start_depth=4 samples=250610 pass_one_w=250610
gate 2 start_depth=5 samples=250610 d_nonsquare=125132 pass_one_w=125478
gate 3 start_depth=6 samples=125478 d_nonsquare=62942  pass_one_w=62536
gate 4 start_depth=7 samples=62536  d_nonsquare=30830  pass_one_w=31706
gate 5 start_depth=8 samples=31706  d_nonsquare=15788  pass_one_w=15918
gate 6 start_depth=9 samples=15918  d_nonsquare=7852   pass_one_w=8066
gate 7 start_depth=10 samples=8066  d_nonsquare=4010   pass_one_w=4056
gate 8 start_depth=11 samples=4056  d_nonsquare=2072   pass_one_w=1984
```

Across all reported gates in this 1M run:

```text
d_square_w_none = 0
pass_two_w = 0
```

The `T_line` split remains flat at every reported gate, within sampling noise.

Follow-up factor telemetry further identifies `chi(d_j)` with the x-square
2-descent character `chi(x_j)`; see
[P27 X-Square / 2-Descent Gate](p27_xsquare_2descent_gate_20260621.md).

## Interpretation

Positive:

```text
The selected branch has a very clean obstruction sequence: d_1, d_2, ... .
The domain-line result is not isolated; it is the first member of an iterated
Kummer/2-cover squareclass tower.
The w_j non-obstruction is theorem-shaped for nonsplit rows.
This gives a precise object for expert/literature review.
```

Negative:

```text
The measured d_j bits look random at this level of instrumentation.
No existing T_line/H90/visible p24 feature predicts the sequence.
Testing a fixed prefix of d_j gates improves constants but does not by itself
beat sqrt(p) scaling.
```

## Practical Test Card

Ask the GPU implementation for prefix-gate A/B telemetry:

```text
baseline
domain-only       = require d_1 square
domain+second-d   = require d_1,d_2 square
domain+second+third-d = require d_1,d_2,d_3 square
```

Report:

```text
per GPU-second rate
survivor lift at target depths
cost per extra d_j gate
whether w_j ever obstructs or branches
```

Promotion bar:

```text
Use as production filter only when the per-second survivor lift exceeds the
throughput loss.  Treat it as constant-factor unless paired with a tower law.
```

## Moonshot Test Card

The math target is:

```text
Find a source/tower law that generates rows with d_1=...=d_m=+1 for growing m,
or computes the sequence chi(d_j) from lower-dimensional quotient data with
less than one random Legendre test per layer.
```

Concrete formulations:

```text
1. Express chi(d_{j+1}) as a named Kummer character on the j-th 2-cover.
2. Find a recurrence or transfer relation for chi(d_j) on the selected branch.
3. Identify a theta/nullwert or duplication formula whose squareclass is d_j.
4. Reframe the selected path as a rational point on an iterated 2-cover whose
   solvable subfamily enforces many d_j=+1 conditions at once.
```

This is the first route in the p27 folder that plausibly points at a
sqrt-beating mechanism rather than a one-bit filter.

## Continue / Kill

```text
continue = derive symbolic d_j formulas on the iterated 2-cover
continue = GPU prefix-gate telemetry for practical constants
continue = expert ask about Kummer/2-cover characters for Montgomery halving

kill = T_line as a d_j tower predictor from current evidence
kill = claiming fixed-prefix d_j filtering beats sqrt scaling
kill = more tiny visible-feature scans unless tied to a named d_j formula
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_trace_norm_multigate_seed130_100k_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_multigate_seed131_1M_20260621.txt`
- Related: [P27 Second-D Gate Frontier](p27_second_d_gate_frontier_20260621.md)

```text
p27_halving_tower_profile_rows=1/1
```
