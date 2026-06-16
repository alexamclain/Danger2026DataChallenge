# P25 Lane B: theta2 Factor-Gauge Normal Form

Updated: 2026-06-13 15:11 PDT

## Purpose

The factor-certificate harness accepts a literal tuple

```text
base=(25,25), K=(57,0), D=(22,3), T=(38,113)
```

for the bridge word

```text
base * K_trace * D_segment * (1 - T).
```

This note records the full `K_trace` gauge freedom.  The theorem-output
contract is quotient data plus a primitive `K`-subgroup generator, not one
rigid eight-coordinate tuple.

## Result

```text
K_subgroup size                         = 25
K_subgroup                              = right mod 3 kernel, C-coordinate 0
primitive K generators                  = 20
accepted full coordinate presentations  = 312500

quotient base class                     = (right mod 3, c) = (1, 25)
quotient D class                        = (right mod 3, c) = (1, 3)
quotient T class                        = (right mod 3, c) = (2, 113)

all primitive K generators give K_trace = true
all K_trace shifts absorb               = true
base, D, T shift independently by K     = true
all 625 base/T gauges preserve bridge   = true
all 625 base/T gauges preserve theta2^-1= true
```

Controls:

```text
target tuple passes                     = true
primitive generator K -> 2K passes      = true
mixed base/D/T K-gauge passes           = true
nonprimitive K -> 5K fails              = true
wrong D quotient class fails            = true
wrong T quotient class fails            = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_gauge_normal_form_gate.py
```

Expected marker:

```text
robert_ksy_theta2_factor_gauge_normal_form_rows=1/1
```

## Interpretation

The finite KSY/theta verifier target is now:

```text
K = any primitive generator of the right-mod-3 kernel in C_75
base class = (1,25) in (C_75/K) x C_169
D class    = (1,3)  in (C_75/K) x C_169
T class    = (2,113) in (C_75/K) x C_169
```

The harness can then choose any representative, derive the KSY half-edge, and
recover the same bridge/theta2 object.  This is still a finite verifier
normal form, not an arithmetic producer, but it is the cleanest current target
for a theorem or literature hit.
