# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Half-Orbit Interaction

Date: 2026-06-13

## Result

The GK projector can be written using only the even and odd Frobenius
half-orbit averages.

Let:

```text
E(h,t) = even p^2 half-orbit carry average
O(h,t) = odd  p^2 half-orbit carry average
```

Then:

```text
O support = (0,1), (0,2), (2,1)
E support = (0,1), (0,2), (1,2)
```

The two top-row leak cells are exactly where both `E` and `O` are `1`.  The
anomaly is the only cell where `O=1` and `E=0`.

Therefore:

```text
projector = O * (1 - E)
```

is exactly the selected anomaly `(2,1)`, and after the outer `S` layer:

```text
138, 310, 482
```

## Payload

Subtracting this interaction projector from the Lucas/binomial payload again
gives the all-one seed:

```text
binom(h,t) - O(h,t)*(1-E(h,t)) = 1
```

on the six selected cells.

## Consequence

This is a sharper arithmetic target than the previous
`selected * odd-half-orbit` formulation.  At the anomaly level, the external
Lucas selector can be replaced by an even/odd half-orbit interaction.

The remaining producer problem is now:

```text
realize O * (1 - E)
```

as a genuine Hasse-Davenport, Gross-Koblitz unit quotient, Barnes-delta, or
equivalent finite-field phase.  A candidate that produces only odd-half-orbit
support still fails, because it leaks to `(0,1)` and `(0,2)`.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py
```
