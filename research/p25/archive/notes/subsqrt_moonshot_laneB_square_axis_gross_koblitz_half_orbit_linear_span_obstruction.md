# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Half-Orbit Linear-Span Obstruction

Date: 2026-06-13

## Result

The anomaly projector is not in the additive span of the basic half-orbit
signals:

```text
1, selected, O, E
```

where `O` and `E` are the odd and even Frobenius `p^2` half-orbit averages.

The gate verifies:

```text
anomaly_in_additive_half_orbit_span = 0
```

Adding a product or direct interaction closes the span:

```text
anomaly = O * (1 - E)
anomaly = selected * O
anomaly = O - O*E
```

## Consequence

A literature hit that only supplies additive averages, separate even/odd
valuation supports, or a linear combination of half-orbit traces is too weak.
The Jacobi-side producer must supply a multiplicative unit quotient, finite
Barnes delta, hypergeometric resonance, or equivalent arithmetic interaction.

This is a small but useful tightening: it separates "the half-orbit signals
are visible" from "the anomaly projector is actually produced."

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate.py
```
