# Lane B: Bridge Hilbert-90 Source-Chain Corner Half Potential

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_potential_gate.py`

## Result

The recorded four-block Hilbert-90 potential is now structurally selected.

Each active chain has six support-four first-boundaries, but exactly one is a
fixed-point half-potential:

```text
q = 0 fixed block
one representative from (25,482)
one representative from (197,310)
one representative from (369,138)
```

For mask `1`, the selected half-potential is:

```text
-[0] + [197] + [369] - [482]
```

For mask `6`, the selected half-potential is:

```text
[0] + [25] - [138] - [310]
```

Both invert to the same signed `S`-layer bridge:

```text
(25,197,369) - (138,310,482)
```

## Interpretation

Sparse first-boundary support is not enough.  The producer must recover the
`q=0` fixed repair and the orientation choice on each inversion pair.  This
links the curved source-row corner to the signed `S`-orbit bridge image without
falling back to black-box equality of the final six-point bridge.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_half_potential_rows=1/1
```
