# P25 Lane B Square-Axis Bridge Formal-Unit Shadow

## Purpose

The candidate harness made the bridge contract executable.  This checkpoint
builds the exact accepted bridge from a producer-shaped formal group-ring word
on the raw source axes `C_75 x C_169`:

```text
x^base * (1 + K + ... + K^24) * (1 + D + D^2) * (1 - T)
```

with:

```text
base = (25,25)
K = (57,0)
D = (22,3)
T = (38,113)
```

## Result

The full formal product has:

```text
support = 150
degree = 0
coefficients = 75 positive, 75 negative
kernel modes = {0}
raw D^3 = Y relation = true
mixed quotient characters = 336
```

It equals the exact raw source bridge and passes the bridge candidate harness.

## Formal Identities

The factors encode the local mechanism we now need an arithmetic producer to
realize:

```text
(1 - K) * (1 + K + ... + K^24) = 0
(1 - D) * (1 + D + D^2) = 1 - D^3
D^3 - Y = K
```

So `D^3 = Y` only after the `K` trace direction is collapsed.

## Shortcut Falsifiers

Omitting the kernel trace gives a six-point sparse section, but it exposes all
`25` kernel modes and fails raw `D^3 = Y`.

Omitting the D segment gives a kernel-trivial two-edge object, not the required
length-three segment.

Omitting the bridge edge gives the positive segment only, not the
anti-invariant bridge.

## Interpretation

This is a positive finite artifact: the local payload is tiny, exact, and far
below `sqrt(p)`.  It is not yet a certificate.  The remaining problem is to
realize this formal shadow arithmetically without losing control to the raw
Kummer costs:

```text
kernel trace: right degree 25
D segment: right degree 75, C degree 169
bridge edge: right degree 75, C degree 169
```

The next candidate should therefore supply `K`, the short `D` segment, and the
`T` bridge edge together, rather than matching only a trace, pure C shadow, or
one factor at a time.
