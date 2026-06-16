# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Minimal Source Edge

Date: 2026-06-12

## Result

The eight four-block Hilbert-90 minimal potentials have now been classified in
the actual square-axis source coordinates

```text
q -> (q mod 3, q mod 169) in C_3 x C_169.
```

Under product-affine source changes plus overall sign, they collapse to four
orbits:

```text
(0,7), (1,6), (2,5), (3,4)
```

The row-balanced, rank-two minima are exactly:

```text
masks 1,2,5,6
```

All four are sums of two row-local `C_169` edges.  Each has the same primitive
short C-steps:

```text
31 and 53
```

These steps are both primitive in `C_169`, and their shadows mod `13` are
different:

```text
31 mod 13 = 5
53 mod 13 = 1
```

So the source object is not a single common C-axis edge, not an axis rectangle,
and not a low `C_13` edge lifted uniformly to `C_169`.

## Interpretation

The best Hilbert-90 producer target is now the source-affine orbit:

```text
masks 1 and 6
```

This is the only row-balanced orbit whose Fourier zero set matches the bridge.
The other row-balanced orbit, masks `2` and `5`, has an extra primitive zero
where the bridge is nonzero, so it cannot recover the bridge by any quotient
circulant ratio.

A future producer may target the four-block potential, but the shape it must
realize is now sharper:

```text
two source rows
two primitive C_169 row edges
short edge steps 31 and 53
no common C-step
no sparse quotient ratio to the bridge
```

This keeps the Hilbert-90 route alive only as a genuinely nonsplit source
function / anti-invariant-ratio problem.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_source_edge_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_source_edge_gate.py
```
