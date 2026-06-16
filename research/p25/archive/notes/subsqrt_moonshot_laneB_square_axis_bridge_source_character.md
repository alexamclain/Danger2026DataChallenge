# Subsqrt Moonshot Lane B Square-Axis Bridge Source Character

Date: 2026-06-12

## Result

The bridge has an exact source-character factorization.

In `C_3 x C_169`, with

```text
D = (1,3)
T = (2,113)
base = (1,25)
```

the Fourier transform factors as:

```text
bridge_hat(a,b)
  = chi(base) * (1 + chi(D) + chi(D)^2) * (1 - chi(T)).
```

The zero set is exactly:

```text
D-segment zeros:  (a,b) = (1,0), (2,0)
bridge-edge zero: (a,b) = (0,0)
```

There are no other source-character zeros.  In particular, all `468`
non-lifted `C_169` characters are nonzero.

## C13 Shadow

The `C_13` shadow has the same zero pattern:

```text
character count = 39
zero count      = 3
nonzero count   = 36
```

So a spectral zero test alone cannot distinguish the full `C_169` lift from
its `C_13` shadow.

## Consequence

The character factorization is useful as a producer contract:

```text
realize the D-segment factor and the bridge-edge factor.
```

But it is not enough by itself.  A producer must still explain the unique
`C_169` source-line lift, not merely match the `C_13` shadow or the three
Fourier zeros.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_source_character_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_source_character_gate.py
```
