# P25 KSY-y Ray-Local / Conductor-39 Alignment

Updated: 2026-06-14

## Purpose

This checkpoint compares the ray-local `theta31` finite payload with the
conductor-`39` source object on the common `C_3 x C_13` quotient surface.

It answers a tempting shortcut:

```text
Can we treat U_chi=-chi_3*chi_13 as the ray-local theta31 payload?
```

No.  `U_chi` is a certified compact source/value object, not the raw
`theta31` or curved-corner finite payload itself.

## Finite Comparison

On `C_3 x C_13`:

```text
theta31 support          = 18
U_chi support            = 24
support intersection     = 12
theta-only support       = 6
U_chi-only support       = 12

theta31 row sums         = (6, 6, 6)
U_chi row sums           = (0, 0, 0)

theta31 column sums      = (0,0,0,0,1,1,1,2,2,2,3,3,3)
U_chi column sums        = (0,0,0,0,0,0,0,0,0,0,0,0,0)

raw signed dot product   = 0
```

After removing the pure C-axis component from `theta31` and multiplying by
`3`:

```text
theta31 mixed support    = 18
U_chi mixed support      = 24
mixed signed dot product = 0

theta31 mixed rank       = 2
U_chi rank               = 1
combined mixed rank      = 3
```

The mixed components are not proportional:

```text
ratios on U_chi support = {-2, -1, 0, 1, 2}
theta mixed nonzero where U_chi is zero = 6
```

## Verdict

```text
U_chi is not the theta31 payload.
U_chi is a value/source route.
```

So a conductor-`39` theorem can still be excellent progress, but only as:

```text
finite value/divisor theorem for U_chi, W, Y_507, H0, or H0 translate
```

or as an explicit bridge/evaluation theorem.  It is not itself a raw
`151 x 677` theta31 vector, a curved-corner payload, or a DANGER3 triple.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ray_local_conductor39_alignment_gate.py
```

Expected marker:

```text
ksy_y_ray_local_conductor39_alignment_rows=1/1
```

## Practical Routing

```text
If a claim says "this is U_chi":
  route it through conductor-39 value/source gates.

If a claim says "this is the ray-local payload":
  require the ray-local pullback router and raw/curved finite acceptor.

If a claim says "U_chi implies theta31":
  ask for the explicit bridge/value theorem; do not infer it from source
  certification alone.
```
