# P27 Domain Line Equals First-Halving Gate

Date: 2026-06-21

## Claim

The p27 `domain_line=+1` filter is exactly the first-halving square-root gate
already present in the X1(16) nonsplit sampler.  It is a good practical
constant-factor filter, but it is not by itself evidence of a deeper
sqrt-beating selector.

## Code Identity

The sampler's first-halving `d` gate is:

```text
F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

In `src/pomerance.c`, `x16_y_first_d_value128` computes exactly this product,
and `x16_y_first_d_root128` accepts precisely when `sqrt(F)` exists.

The trace/norm line classifier computes the same value:

```text
B = y^2 - 2y + 2
C = y^2 - 2
ym1 = y - 1
F = ym1*C*B
domain_line = chi(F)
```

The first-half constructor path then calls `x16_y_first_d_root128` before
constructing the first halved point.  The square root `z=sqrt(F)` is used in
`x16_first_half_from_yroot128`, which verifies the Montgomery halving
discriminant and then calls `halve_once_known_d128`.

So the practical meaning is:

```text
domain_line = -1  <=> first halving gate fails
domain_line = +1  <=> first halving gate passes
```

up to zero/degenerate rows rejected elsewhere.

## Empirical Check

The line-stratum stats match this exactly on measured p27 streams.

Seed `121`, 1M nonsplit rows:

```text
depth=4 count = 499948
domain_minus samples = 499948
domain_minus depth>=16 survivors = 0
```

Seed `122`, 1M nonsplit rows:

```text
depth=4 count = 499084
domain_minus samples = 499084
domain_minus depth>=16 survivors = 0
```

Seed `123`, 5M nonsplit rows:

```text
depth=4 count = 2502308
domain_minus samples = 2502308
domain_minus depth>=16 survivors = 0
```

## Interpretation

Positive:

```text
The domain-only filter is mathematically clean and cheap.
It should still be the first GPU A/B test because it can avoid work that the
baseline sampler otherwise spends before discovering the first-half failure.
```

Negative:

```text
This is not a new sub-sqrt source sampler.
The observed 2x survivor lift is expected: it is preselecting rows that pass
the first halving square-root gate.
```

## Next Real Test

The actual sqrt-beating question moves one layer deeper:

```text
Can the same trace/norm, quotient-involution, or Hilbert-90 structure expose a
cheap predictor for the next halving gate after domain_line=+1?
```

The most useful GPU telemetry is therefore:

```text
baseline vs domain-only filter for practical throughput
domain_line=+1 rows stratified by the next one or two halving discriminants
T_line/Hilbert-90 quotient bits measured against those deeper gates
```

## Continue / Kill

```text
continue = use domain-only as a practical first GPU A/B candidate
continue = search for a cheap second-gate / post-domain predictor
continue = keep T_line as telemetry for deeper gates, not as a production filter

kill = claiming domain_line by itself is a sqrt-beating theorem
kill = treating domain_minus having zero deep survivors as surprising after
       this code identity
```

## Linked Artifacts

- Evidence: [P27 Practical Domain-Line Filter](p27_practical_domain_filter_20260621.md)
- Code output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed121_1M_20260621.txt`
- Code output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed122_1M_20260621.txt`
- Code output: `research/p27/archive/probe_outputs/p27_trace_norm_line_strata_seed123_5M_20260621.txt`

```text
p27_domain_first_halving_gate_rows=1/1
```
