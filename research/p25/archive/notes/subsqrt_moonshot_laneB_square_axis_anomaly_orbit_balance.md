# Subsqrt Moonshot Lane B Square-Axis Anomaly-Orbit Balance

Date: 2026-06-12

## Result

The q-binomial coefficient mismatch is exactly one three-point orbit:

```text
S*X^3Y = {138, 310, 482}
```

On this orbit the q-binomial shadow has coefficient `2` for `q=1`, while the
target all-one residual has coefficient `1`.

The exact visible correction is therefore

```text
-S*X^3Y
```

but that correction has degree `-3`, nonzero in the working odd fields.

## Fourier Warning

The anomaly orbit is tiny, but it is not low-frequency:

```text
Fourier zeros = {169, 338}
```

These are the same two `S`-factor zeros seen by the full residual, the
rectangle, and the borrow corner.  So a Fourier-support test cannot detect or
repair the coefficient anomaly.

## Two-Orbit Obstruction

If the repair is forced to stay inside the small `S`-orbit vocabulary, a
degree-zero repair must balance `-S*X^3Y` with another `S`-orbit.  Exhausting
the other eight `3x3` rectangle orbits:

```text
5 target orbits distort an already-correct coefficient;
3 borrow-corner orbits create forbidden support;
0 balanced two-orbit repairs preserve the target.
```

## Producer Consequence

A modular-unit / ray-local candidate cannot simply subtract the q-binomial
anomaly at the quotient level, and it cannot repair it by adding one more
small `S` orbit.  It must supply scalar, nonlocal, or hidden degree balance
while still tracing to the exact all-one residual.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_anomaly_orbit_balance_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_anomaly_orbit_balance_gate.py
```
