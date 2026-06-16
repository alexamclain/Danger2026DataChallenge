# Lane B: Bridge Hilbert-90 Source-Chain Corner Normal Form

Date: 2026-06-12

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_normal_form_gate.py`

## Result

The active Hilbert-90 source chain has a positive corner normal form.

In primitive `D` coordinates on `C_507`, the bridge is the unique anti-invariant
length-three run, up to orientation:

```text
positive run = 121,122,123
negative run = 384,385,386
unit step    = 1
center       = 122 = -bridge_sep/2
```

In quotient/source terms:

```text
bridge_sep_q = 113
bridge_sep_d = 263
half_bridge_d = 122
half_bridge_q = 197
opposite_half_q = 310
unit_q = 172
```

Thus the canonical chain is not just an arbitrary curved support-three set:

```text
C = -(1 + z + z^(1-e)),  e = 122
```

and the source corner is:

```text
{0, S, S - E}
```

where `S` is the known outer `D/S` unit and `E` is the half-bridge edge.

## Controls

The formal cyclic corner identity has four antiderivatives in `C_507`.  All
recover the bridge, but only two are source graphs with one point in each
`C_3` row:

```text
graph:     (0, 172, 482)
non-graph: (0, 138, 335)
non-graph: (0, 172, 369)
graph:     (0, 25, 335)
```

The four active source-boundary rows all use half-bridge directions
`197/310`, all have support-four first boundaries, and all cancel at the
unit vertices `d = +/-1`, i.e. `q = 172/335`.

## Interpretation

This is a producer-facing simplification, not a certificate.  A candidate can
now target the half-bridge corner rather than an opaque three-point chain.
But it must still realize the source-graph corner: a plain cyclic `C_507`
Hilbert-90 antiderivative is too weak because the non-graph controls also
recover the same bridge.

