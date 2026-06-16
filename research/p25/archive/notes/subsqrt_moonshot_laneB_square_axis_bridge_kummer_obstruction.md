# Subsqrt Moonshot Lane B Square-Axis Bridge Kummer Obstruction

Date: 2026-06-12

## Result

The bridge source multiplier has no cheap Kummer descent.

The bridge step is:

```text
X^2Y^3 = 113
```

On local sources it acts by:

```text
45  mod 151
667 mod 677
```

The Kummer classes are primitive at the natural raw source orders:

```text
45  mod 151, modulo 75th powers:  class index 49, degree 75
667 mod 677, modulo 169th powers: class index 128, degree 169
```

The visible shadows also require their full visible degrees:

```text
45  mod 151, modulo 3rd powers:  degree 3
667 mod 677, modulo 13th powers: degree 13
```

Changing sign does not help: `-1` is already a power in each of these Kummer
quotients, so the negative multiplier has the same class.

## Consequence

This does not prove that every possible producer must take such roots.  It does
rule out a cheap root-based explanation of the primitive bridge edge.  A raw
source root construction would have simultaneous degree

```text
lcm(75,169) = 12675.
```

So the useful producer should explain the bridge as a finite-field identity or
structured divisor edge, not as a low-degree Kummer descent of the source
multiplier.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_kummer_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_kummer_obstruction_gate.py
```
