# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Fourier

Date: 2026-06-12

## Result

The rigid support-three Hilbert-90 source chains have a minimal Fourier
footprint.

For each active bridge-compatible chain:

```text
chain support = 3
chain zeros   = (a,b) = (1,0), (2,0)
```

These are exactly the forced `C_3` row-sum zeros coming from one point in each
source row with all-equal coefficients.  All non-lifted `C_169` characters are
nonzero on the chain.

The rigid primitive first boundary in direction `197` or `310` adds only the
scalar zero:

```text
first-boundary zeros = (0,0), (1,0), (2,0)
bridge-image zeros   = (0,0), (1,0), (2,0)
```

Thus:

```text
active chain
  -> primitive first boundary
  -> inversion / Hilbert-90 boundary
```

has exactly the signed bridge's Fourier zero set.

## Lift Selectivity

The same computation was run on the thirteen primitive `C_169` projective lifts
of the active `C_13` shadow `(1,2,10)`.

Every lift has the same `C_13` shadow zero profile:

```text
(a,b) = (1,0), (2,0)
```

Upstairs in `C_169`, only two lifts acquire an extra primitive zero:

```text
(1,4,164):   extra zero (2,16)
(1,10,158):  extra zero (2,167)
```

The other eleven lifts, including the active lift `(1,18,150)`, have exactly
the same forced-zero profile.

## Interpretation

This is a useful falsifier for frequency-only producers.

A spectral-zero test can reject two of the thirteen `C_13`-shadow lifts, but it
does not select the active nonsplit `C_169` lift.  The active chain is
Fourier-generic apart from the forced row-sum zeros.  A producer must therefore
recover the actual nonsplit source-chain geometry:

```text
C_169 lift (1,18,150)
support-three curved source graph
rigid 197/310 first-boundary direction
all-equal coefficients
Hilbert-90 / inversion bridge boundary
```

Matching the `C_13` shadow, the forced row zeros, or the final bridge zero set
is not enough.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_fourier_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_fourier_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_fourier_rows=1/1
```
