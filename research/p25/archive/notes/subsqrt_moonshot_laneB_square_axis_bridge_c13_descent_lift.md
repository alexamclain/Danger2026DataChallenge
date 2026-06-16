# P25 Lane B Square-Axis Bridge C13 Descent/Lift

## Purpose

The formal-unit bridge shadow has a cheap `C_13` projection.  Reducing the
`C_169` source coordinate modulo `13` preserves the same signed `150`-cell
formal word:

```text
x^base * (1 + K + ... + K^24) * (1 + D + D^2) * (1 - T)
```

This checkpoint tests whether that `C_13` shadow can replace the full
`C_169` lift.

## Result

The `C_13` shadow is real but insufficient.

```text
C13 projected support = 150
C13 projected degree = 0
C13 projected coefficients = 75 positive, 75 negative
```

The naive pullback from `C_13` to `C_169` has:

```text
raw support = 1950
quotient support = 78
kernel modes = {0}
raw D^3 = Y relation = true
trace_correct = false
```

It is kernel-trivial and relation-satisfying, but it is not the bridge.

## Character Gap

The naive pullback has only lifted `C_13` characters:

```text
pure C characters = 12
mixed right/C characters = 24
```

The true bridge has:

```text
pure C characters = 168
mixed right/C characters = 336
```

So the naive `C_13` pullback is missing:

```text
156 pure C characters
312 mixed right/C characters
```

## Fiber Lift

The true bridge selects exactly one `C_169` fiber above each `C_13` shadow
point.  The selected fiber histogram is:

```text
fiber 1: 25 points
fiber 2: 50 points
fiber 10: 50 points
fiber 11: 25 points
```

This selection is the actual `C_169` lift data.  It cannot be replaced by the
naive pullback.

## Consequence

The low-degree `C_13` shadow is a useful arithmetic clue, but not a producer.
Any successful modular-unit or CM-Artin realization must supply the `C_169`
fiber selector, not just the cheap shadow.
