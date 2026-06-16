# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Primitive Word

Date: 2026-06-12

## Result

The active Hilbert-90 source chain has a compact primitive-coordinate word.

Collapse the raw `C_12675` source by the invisible `C_25` trace kernel and use
the primitive `D` coordinate on the quotient `C_507`.  For the canonical active
chain:

```text
C = -(1 + z + z^-121)
```

The rigid first-boundary direction becomes:

```text
1 - z^122
```

Then:

```text
(1 - z^122) C
  = -1 - z^-121 + z^122 + z^123
```

The `z^1` term cancels internally.  Applying the inversion boundary gives the
bridge:

```text
z^121(1 + z + z^2) - z^384(1 + z + z^2)
```

## Uniqueness

For each of the four active chains, scanning all `506` nonzero first-boundary
steps in `C_507` gives exactly one step that recovers the bridge after
inversion:

```text
mask 1, direction 197 -> D-step 122
mask 1, direction 310 -> D-step 385 = -122
mask 6, direction 197 -> D-step 122
mask 6, direction 310 -> D-step 385 = -122
```

For each chain, the first-boundary support distribution over all nonzero steps
is:

```text
support 4:   6 directions
support 6: 500 directions
```

Only the recorded `+/-122` step also gives the signed bridge after inversion.

## Interpretation

This is the cleanest producer-side target so far:

```text
three-term primitive D-quotient word
  -> unique +/-122 first boundary with one cancellation
  -> four-point Hilbert-90 potential
  -> inversion boundary
  -> signed bridge
  -> attach the C_25 raw trace
```

A modular-unit or CM-Artin candidate can now be tested against this exact
three-term word before worrying about the full raw trace.  The remaining hard
part is still arithmetic realization of the primitive `C_169` motion.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_primitive_word_rows=1/1
```
