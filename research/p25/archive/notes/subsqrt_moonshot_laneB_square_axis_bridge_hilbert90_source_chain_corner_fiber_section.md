# Lane B: Bridge Hilbert-90 Source-Chain Corner Fiber Section

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_fiber_section_gate.py`

## Result

After the forced `K` trace projects the raw corner down to the quotient, the
remaining active `C_169` corner lift is a genuine quadratic fiber section over
its `C_13` shadow.

Write:

```text
c = c0 + 13*f,  c0,f in F_13
```

For the canonical active corner:

```text
C_169 row values = (0, 3, 144)
C_13 shadow      = (0, 3, 1)
fiber values     = (0, 0, 11)
fiber section    = f(c0) = c0*(c0 - 3)
```

Across the four active half-bridge corners:

```text
no row is the Teichmuller lift of its C_13 shadow
no row admits an affine fiber section
each row has a unit quadratic fiber section over F_13
```

## Interpretation

The `K` trace is clean, but the quotient corner still carries a nontrivial
`13`-adic lift.  The active lift is not obtained by a Teichmuller shortcut and
not by a linear/affine fiber gauge.  A producer must supply a genuine quadratic
fiber correction, or an arithmetic identity that explains the same correction,
after the raw `K` trace has been accounted for.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_fiber_section_rows=1/1
```
