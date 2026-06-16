# Subsqrt Moonshot Lane B Square-Axis Bridge Raw Source Character

Date: 2026-06-12

## Result

The raw bridge has a full source-character factorization on `C_75 x C_169`.

With

```text
base   = (25,25)
kernel = (57,0)
D      = (22,3)
T      = (38,113)
```

the raw Fourier transform factors as:

```text
bridge_hat(a,b)
  = chi(base)
    * sum_{j=0}^{24} chi(kernel)^j
    * (1 + chi(D) + chi(D)^2)
    * (1 - chi(T)).
```

The zero profile is:

```text
raw characters        = 12675
zero characters       = 12171
nonzero characters    = 504
kernel-trace zeros    = 12168
D-segment zeros       = (25,0), (50,0)
bridge-edge zero      = (0,0)
```

The only surviving right-source character indices are:

```text
a = 0, 25, 50.
```

These are exactly the `C_3 x C_169` quotient characters.

## Consequence

The raw lift is not an arbitrary sparse section and not a hidden kernel phase.
It is:

```text
25-point right-kernel trace
times
D-segment factor
times
bridge-edge factor.
```

A producer must explain the `25`-point right-kernel trace explicitly, together
with the same source-line lift geometry seen on `C_3 x C_169`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_raw_source_character_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_raw_source_character_gate.py
```
