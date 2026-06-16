# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Minimal Potential Structure

Date: 2026-06-12

## Result

The eight minimal degree-zero Hilbert-90 potentials are four-block targets, but
they do not hide a cheap quotient product or quotient-linear bridge recovery.

All eight fail the small product screen:

```text
affine parallelogram count = 0
signed 2 x 2 product count = 0
```

Their Fourier behavior splits into three cases over the `507`-cycle:

```text
bridge zeros: {0,169,338}

mask 1,6: same zero set as the bridge
mask 2,5: extra primitive zero at 258 or 249, where the bridge is nonzero
mask 0,3,4,7: only the scalar zero
```

If we ask for a quotient-circulant multiplier `H` with `H * F = bridge`, the
two extra-zero cases are impossible.  In the remaining six cases, optimizing
over the free zero-frequency space still leaves `H` dense:

```text
mask 0 -> support at least 503 / 507
mask 1 -> support at least 500 / 507
mask 3 -> support at least 504 / 507
mask 4 -> support at least 504 / 507
mask 6 -> support at least 500 / 507
mask 7 -> support at least 503 / 507
```

## Interpretation

The Hilbert-90 route is still alive only as a genuine arithmetic producer
target.  The best-looking unit-coefficient minima, masks `1` and `6`, match the
bridge's Fourier zero set, but the bridge recovery ratio is not a sparse
quotient group-ring operator.  Masks `2` and `5` have an even sharper
obstruction: they vanish at a primitive character where the bridge does not.

So a future producer may target one of the four-block potentials, but it must
also realize the nonsplit anti-invariant ratio/function.  It cannot just:

```text
factor the potential as a hidden 2 x 2 product
use a low-frequency quotient filter
use a sparse quotient-circulant bridge ratio
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_potential_structure_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_minimal_potential_structure_gate.py
```
