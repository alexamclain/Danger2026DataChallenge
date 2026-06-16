# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Cyclotomic Obstruction

Date: 2026-06-12

## Result

The primitive source-chain word is not explained by the simplest cyclotomic
unit shapes.

Recall the canonical chain in the primitive `D` quotient coordinate:

```text
C = -(1 + z + z^-121)
```

The gate checks four small producer shortcuts:

```text
1. length-three geometric / arithmetic-progression segment
2. signed product of two first-order cyclotomic edges
3. edge antiderivative of the chain itself
4. signed two-edge product for the four-point Hilbert-90 potential
```

All four shortcuts fail.

## Edge Quotients

The active chain has no edge antiderivative in `C_507`:

```text
possible directions = 0
```

The four-point Hilbert-90 potential does have edge antiderivatives, but the
minimum support is exactly `3`, and the only minimum directions are:

```text
122, 385 = -122
```

The first few support levels are:

```text
support 3:  directions 122,385
support 6:  directions 61,446
support 12: directions 223,284
support 14: directions 81,426
support 15: directions 77,430
```

## Interpretation

This keeps the target honest for modular-unit and CM-Artin attempts.

The producer must supply the actual three-term chain:

```text
-(1 + z + z^-121)
```

It cannot be replaced by:

```text
a length-three AP/geometric segment
a product of two basic edge divisors
an earlier edge boundary
```

The first cheap edge only appears at the already-recorded `+/-122` boundary
step that turns the chain into the four-point Hilbert-90 potential.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_cyclotomic_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_cyclotomic_obstruction_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_cyclotomic_obstruction_rows=1/1
```
