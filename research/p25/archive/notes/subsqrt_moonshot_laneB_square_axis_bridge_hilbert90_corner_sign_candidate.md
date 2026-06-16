# p25 Lane B: Hilbert-90 Bridge Corner Sign-Candidate Harness

Updated: 2026-06-13 13:36 PDT

## Purpose

After the McCarthy powered route downgrade, the strongest live producer target
is again the Robert/Siegel / Hilbert-90 bridge corner.  The latest bridge gates
reduce each active half-bridge corner to two signs:

```text
eps = primitive D-unit sign in {+1,-1}
a   = branch coefficient in {+1,-1}
```

This harness lets a theorem or literature hit emit only:

```text
eps a
```

and checks whether those signs select one of the four already-vetted finite
bridge corners.

## Forced Expansion

Given `eps` and `a`, the harness expands:

```text
orientation_mask = 1 if eps=+1, else 6
recorded_direction_q = 197 if a=-1, else 310
recorded_direction_d = 122 if q=197, else 385

cancellation = (3*eps, (eps-1)/2) in signed F_13 low/fiber coordinates
neighbor = cancellation + 2*a*(1,1)

cancel_row   = (3-eps)/2
neighbor_row = cancel_row-a mod 3
off_row      = cancel_row+a mod 3
```

It records the known raw support ladder:

```text
K-traced corner support = 75
first-boundary support  = 100
signed bridge support   = 150
```

and records, rather than waives, the primitive `C_169` cost.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness.py
```

Candidate controls:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness.py \
  --eps 1 --branch -1

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_candidate_harness.py \
  --eps 0 --branch 1
```

Observed:

```text
square_axis_bridge_hilbert90_corner_sign_candidate_harness_rows=1/1
square_axis_bridge_hilbert90_corner_sign_candidate_rows=1/1  # positive control
square_axis_bridge_hilbert90_corner_sign_candidate_rows=0/1  # invalid-sign control
```

## Interpretation

This is an intake/falsifier artifact, not a producer proof.  It lowers the
interface for future Robert/Siegel/Hilbert-90 hits: emit two signs first; only
after passing this compact gate does it make sense to expand to sparse source
triples or raw `C_12675` payloads.
