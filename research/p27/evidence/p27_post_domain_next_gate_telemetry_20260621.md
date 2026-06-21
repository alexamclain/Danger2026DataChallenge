# P27 Post-Domain Next-Gate Telemetry

Date: 2026-06-21

## Claim

After conditioning on `domain_line=+1`, the current `T_line` bit does not
meaningfully predict the next few first-branch halving gates.  This demotes
`T_line` to theorem telemetry rather than a practical next-gate filter.

Follow-up narrowed the actual obstruction to the second Montgomery
discriminant `d2=x5^2+A*x5+1`; see
[P27 Second-D Gate Frontier](p27_second_d_gate_frontier_20260621.md).

## Code

The line-stratum stats mode now reports early depths:

```text
x16halvestatsnonsplittraceline
depth targets: 5,6,7,8,9,10,12,14,16,18,20,22,24,26,28,30
```

Build:

```bash
cc -O3 -o src/pomerance src/pomerance.c
```

## Runs

```bash
./src/pomerance 1000000000000000000000000103 \
  124 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed124_1M_earlydepth_20260621.txt

./src/pomerance 1000000000000000000000000103 \
  125 1000000 x16halvestatsnonsplittraceline \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed125_1M_earlydepth_20260621.txt
```

## Result

As expected from the first-halving identity, `domain_minus` has no rows past
depth `4`:

```text
seed 124: domain_minus samples=499630, depth>=5 survive=0
seed 125: domain_minus samples=501058, depth>=5 survive=0
```

Inside `domain_line=+1`, `T_line` is flat at the early gates:

```text
seed 124:
  Tline_minus depth>=6 = 0.500031974
  Tline_plus  depth>=6 = 0.499252496
  Tline_minus depth>=8 = 0.126856485
  Tline_plus  depth>=8 = 0.122702526
  Tline_minus depth>=10 = 0.031622196
  Tline_plus  depth>=10 = 0.031443122

seed 125:
  Tline_minus depth>=6 = 0.498934602
  Tline_plus  depth>=6 = 0.498503631
  Tline_minus depth>=8 = 0.125156205
  Tline_plus  depth>=8 = 0.125093272
  Tline_minus depth>=10 = 0.031833766
  Tline_plus  depth>=10 = 0.031427769
```

Deeper counts are too small and flip direction:

```text
seed 124 depth>=16:
  Tline_minus = 114/250204 = 0.000455628
  Tline_plus  = 136/250166 = 0.000543639

seed 125 depth>=16:
  Tline_minus = 142/249672 = 0.000568746
  Tline_plus  = 94/249270  = 0.000377101
```

## Interpretation

Positive:

```text
The updated stats mode can now directly inspect early post-domain gates.
The domain-first-halving interpretation is empirically exact on two more
million-row streams.
```

Negative:

```text
T_line is not the cheap predictor for the second, third, or fourth halving gate.
The H90 quotient boundary remains mathematically interesting, but it has not
yet become a sampler.
```

## Next Test

The next sqrt-beating attempt should look for a new named bit tied to the
post-domain halving discriminants:

```text
condition first on domain_line=+1
compute the next halving discriminant(s)
try to express their squareclass through the quotient variables
  a = t - 1/t
  b^2 = 16 - a^4
or through the same-boundary Hilbert-90 factors from the T_line audit
```

GPU telemetry should therefore report `T_line` only as a control unless it can
also expose the next-gate discriminant squareclasses.

## Continue / Kill

```text
continue = domain-only filter for practical A/B
continue = derive/measure named post-domain discriminant bits
continue = use T_line as an H90 control bit

kill = T_line as the next-gate practical filter from current evidence
kill = more blind line-bit fitting without a named post-domain discriminant
```

## Linked Artifacts

- Evidence: [P27 Domain Line Equals First-Halving Gate](p27_domain_first_halving_gate_20260621.md)
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed124_1M_earlydepth_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed125_1M_earlydepth_20260621.txt`

```text
p27_post_domain_next_gate_telemetry_rows=1/1
```
