# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Potential

Date: 2026-06-12

## Result

The anti-invariant bridge is a genuine sparse half-Frobenius boundary:

```text
bridge = (1 - sigma) F,    sigma = p^39.
```

The two sparse potentials are exactly the oriented half-bridges:

```text
positive half: support 75, degree +75
negative half: support 75, degree -75
```

They are useful as a producer target, but they are not certificates.  Among
the `15` bridge `p^39` orbits, keeping this minimal support allows `76`
possible total degrees, from `-75` to `+75`, and never degree zero.

## Degree Repair

The cheapest unrestricted degree-zero repair adds a coefficient `-75` at the
unique fixed point `(0,0)`.  This keeps the Hilbert-90 boundary equation but
breaks the producer harness:

```text
support = 76
block constancy = 506/507
kernel modes = all 25 modes
raw D^3=Y mismatches = 2
bridge_harness_ok = false
```

The cheapest block-constant / kernel-trivial repair is also unique: the only
sigma-invariant quotient block is `q = 0`, so degree repair adds the scalar
block `-3 * 1_{q=0}` to the positive half-boundary.  This preserves block
constancy and kernel mode `{0}`, but it is still not the bridge:

```text
support = 100
quotient trace = -3 at q=0, +1 on the three positive bridge cells
trace_correct = false
bridge_harness_ok = false
```

## Consequence

Hilbert-90 is a real structural clue, but it does not remove the hard part.
A producer may target the sparse half-boundary, yet it must still supply the
anti-invariant line or an equivalent nonsplit identity.  Turning the potential
into a degree-zero object either leaks a fixed-point scalar/kernel defect or
adds the wrong `q=0` scalar block.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_potential_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_potential_gate.py
```
