# p27 GPU Quadratic-Gate Bounded Probe

Run UTC: 2026-06-22T00:57:16Z

Prime: `p = 10^27 + 103`

GPU: NVIDIA RTX 6000 Ada Generation

Rows: 2,000,000 accepted rows per mode and seed order, `target_depth=13`,
`prefix_depth=6`, `claim_batch=1`.

This was a bounded structure test, not a production p27 search and not a raw
random `(R,L)` conic-pair sampler.  The latest legal-incidence screen showed
that unconstrained random `(R,L)` hits legal rows only at about `constant/q`, so
this run tested the legal recurrence-coordinate filter and quadratic gate:

```text
A = 2 - c^2
x = r^2
next_gate = chi(r^2 + c*r + 1)
```

## Summary

The quadratic-gate formula was validated at scale, but it is not yet evidence of
a source-normalized narrowing win.

Across the telemetry runs there were `7,874,715` checked gates over gates 3-8,
with `0` mismatches and `0` unavailable formula rows after the initial
recurrence-coordinate domain filter.

The recurrence-coordinate domain is about half of the broader post-d2 prefix
scope:

| mode | seed | accepted recurrence rows | wider prefix successes | domain fraction |
|---|---:|---:|---:|---:|
| quad precheck | identity | 2,000,000 | 3,999,594 | 0.500051 |
| quad precheck | splitmix | 2,000,000 | 4,003,023 | 0.499622 |
| quad telemetry | identity | 2,000,000 | 3,999,589 | 0.500051 |
| quad telemetry | splitmix | 2,000,000 | 4,002,968 | 0.499629 |

Conditioned on that domain, the depth-13 survivor rate is about twice the wider
post-d2 baseline rate.  But the source draws per accepted recurrence row are
also about twice as high, so target survivors per source draw stay comparable
or slightly lower.

| mode | seed | depth-13 rate | target/source draw | target survivors/sec |
|---|---:|---:|---:|---:|
| post-d2 baseline | identity | 0.007982 | 9.987e-4 | 29,532 |
| post-d2 baseline | splitmix | 0.007957 | 9.926e-4 | 30,561 |
| quad precheck | identity | 0.015789 | 9.883e-4 | 26,886 |
| quad precheck | splitmix | 0.015840 | 9.899e-4 | 26,944 |
| quad telemetry | identity | 0.015786 | 9.881e-4 | 24,430 |
| quad telemetry | splitmix | 0.015844 | 9.901e-4 | 24,492 |

## Gate Telemetry

Identity seed order, telemetry mode:

| gate | rows | formula + | formula - | actual + | actual - | mismatches |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 2,000,000 | 1,000,333 | 999,667 | 1,000,333 | 999,667 | 0 |
| 4 | 1,000,333 | 501,231 | 499,102 | 501,231 | 499,102 | 0 |
| 5 | 501,231 | 250,382 | 250,849 | 250,382 | 250,849 | 0 |
| 6 | 250,382 | 125,342 | 125,040 | 125,342 | 125,040 | 0 |
| 7 | 125,342 | 63,179 | 62,163 | 63,179 | 62,163 | 0 |
| 8 | 63,179 | 31,571 | 31,608 | 31,571 | 31,608 | 0 |

SplitMix seed order, telemetry mode:

| gate | rows | formula + | formula - | actual + | actual - | mismatches |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 2,000,000 | 997,855 | 1,002,145 | 997,855 | 1,002,145 | 0 |
| 4 | 997,855 | 498,865 | 498,990 | 498,865 | 498,990 | 0 |
| 5 | 498,865 | 249,734 | 249,131 | 249,734 | 249,131 | 0 |
| 6 | 249,734 | 125,004 | 124,730 | 125,004 | 124,730 | 0 |
| 7 | 125,004 | 62,790 | 62,214 | 62,790 | 62,214 | 0 |
| 8 | 62,790 | 31,688 | 31,102 | 31,688 | 31,102 | 0 |

## Interpretation

This confirms that the quadratic gate is a precise formula for the selected
recurrence tower:

```text
chi(x_next) = chi(r^2 + c*r + 1)
```

The current filter cuts the wider post-d2 prefix population in half and then
doubles the conditional survivor rate.  That is mathematically useful because
it isolates the recurrence-coordinate tower, but it does not yet reduce the
source-normalized search scope.

The GPU precheck short-circuited about 1.97M rejected branches per seed order
and roughly halved the expensive downstream square-root work versus full
telemetry.  It still did not beat the wider post-d2 baseline in survivor/sec,
which is expected because the current implementation pays an extra formula
domain cost to discover the half-size source.

The next useful test is not a larger brute-force run.  It is a legal
pullback/quotient sampler that lands directly in the recurrence-coordinate
domain, or a gate-coupling law that biases the sequence of selected
`chi(r_j^2 + c*r_j + 1)` signs across many gates.
