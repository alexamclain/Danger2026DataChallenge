# Lane B: Bridge Hilbert-90 Source-Chain Corner Raw Character

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_character_gate.py`

## Result

The forced raw corner lift has an exact character factorization:

```text
corner_hat_raw(a,b) = K(a) * corner_hat_quotient(a,b)
K(a) = sum_{j=0}^{24} chi(57,0)^j
```

For each of the four active half-bridge corners:

```text
raw support       = 75
raw characters    = 12675
kernel-trace zeros = 12168
quotient zeros     = (25,0), (50,0)
nonzero a-values   = 0,25,50
```

The `K` trace kills exactly the raw right characters outside the surviving
`C_3 x C_169` quotient.  Once that trace is applied, the quotient corner has no
extra spectral shortcut: its only zeros are the two forced `C_3` row-balance
characters.

## Interpretation

This is the positive side of the raw `K`-trace story.  The trace is not messy:
it cleanly projects the corner from `C_75 x C_169` down to the quotient
characters.

But it also does not solve the producer problem.  After factoring out the
right-kernel trace, the active quotient corner remains a full primitive
`C_169` object with no hidden low-frequency or proper-quotient collapse.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_raw_character_rows=1/1
```
