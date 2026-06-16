# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Boundary

Date: 2026-06-12

## Result

The bridge-compatible four-block Hilbert-90 potentials have a smaller source
target than the previous handoff stated.  In the cyclic quotient/source
coordinate `q in C_507`, masks `1` and `6` are optimal first boundaries of
three-point antiderivatives.

For mask `1`:

```text
F_1 = -[0] + [197] + [369] - [482]
F_1 = (1 - T_197) * ( -[0] - [172] - [482] )
F_1 = (1 - T_310) * (  [172] + [197] + [369] )
```

For mask `6`:

```text
F_6 = [0] + [25] - [138] - [310]
F_6 = (1 - T_197) * ( -[138] - [310] - [335] )
F_6 = (1 - T_310) * (  [0] + [25] + [335] )
```

The two best directions are opposite primitive source directions:

```text
197 -> (2,28) in C_3 x C_169
310 -> (1,141) in C_3 x C_169
```

The scan is exhaustive over all `506` nonzero source directions.  For masks
`1` and `6`, the minimum possible first-boundary antiderivative support is
`3`, attained only by directions `197` and `310`.

The competing row-balanced orbit, masks `2` and `5`, does not get this
compression:

```text
best first-boundary support for masks 2 and 5 = 14
best directions = 243 and 264
```

So the previous row-edge target has become a sharper double-boundary target:

```text
bridge = (1 - inversion) * (1 - T_197) * A
```

with `A` a three-point skew source chain for the bridge-zero-compatible orbit.

## Interpretation

This is a positive moonshot artifact, not a certificate.  It gives a much
smaller producer-shaped object for a CM-Artin, Jacobi, modular-unit, or
finite-field identity to realize:

```text
three-point source chain
primitive first-boundary direction 197 / 310
Hilbert-90 anti-invariant inversion boundary
```

The remaining hard part is unchanged in kind: a producer must realize the
nonsplit anti-invariant identity and pass the raw DANGER3 harness.  But the
payload to ask for is now smaller and more structured than a generic
four-block potential or two unrelated row edges.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_boundary_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_boundary_rows=1/1
```
