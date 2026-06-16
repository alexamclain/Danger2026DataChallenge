# P25 search128 Three-Odd-Part Fast Path

Date: 2026-06-16

## Purpose

Document the current `pomerance.c` fast path being published alongside the p25
research archive.

## Change

The `search128()` loop now has a specialized branch for the case:

```text
nms = 3
ms[0] + 1 = 2*ms[1]
ms[1]     = 2*ms[2] + 1
```

Instead of treating the three odd parts as unrelated scalar-multiplication
targets, the code reuses the first paired multiplication and derives the other
projected candidates by a short chain of `xADD128` and `xDBL128` steps before
calling `projected_hit128()`.

## Target Regime

This is a constant-factor optimization for `u128` searches whose admissible odd
parts fall into the three-term pattern above. It was motivated by p25-style
targets, especially `p = 10^25 + 13`, where the 128-bit search path and a
three-odd-part structure are both relevant.

## Non-Claim

This does not change the verifier, the certificate boundary, or the asymptotic
search model. It is only a hot-loop reuse optimization for a specific
`search128()` shape.
