# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Minimal Potential

Date: 2026-06-12

## Result

The bridge is a sparse Hilbert-90 boundary, but a rational-function-style
producer would want a degree-zero potential.  If we require the repair to be
block-constant, kernel-trivial, integral, and `p^39`-invariant, the smallest
degree-zero potentials are completely classified.

There are three bridge pairs under `q -> -q`:

```text
(25,482), (197,310), (369,138)
```

Each pair must keep one oriented cell.  A degree-zero potential needs one
additional fixed `q=0` block.  Therefore every minimum has:

```text
quotient support = 4
raw support = 100
```

There are exactly `2^3 = 8` such minima.  They choose which side of each bridge
pair is present, and put coefficient `-3,-1,+1,+3` on `q=0` according to the
orientation imbalance.

## Interpretation

This is a positive producer target, not a certificate.  All eight minima:

```text
are degree zero
satisfy bridge = (1 - p^39)F
are block-constant
have kernel mode {0}
satisfy the raw D^3=Y relation
```

But none is itself the signed bridge:

```text
trace_correct = false
bridge_harness_ok = false
```

So the next arithmetic route should not look for the bridge as an invariant
potential.  It should try to realize one of these eight four-block potentials
as a divisor/function and then recover the anti-invariant ratio or equivalent
nonsplit identity.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_potential_gate.py
```
