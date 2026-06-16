# P25 Lane B: Robert KSY Normalized-y Theorem Interface

Updated: 2026-06-13 16:20 PDT

## Purpose

This gate is an intake rubric for future theorem or literature hits.  It does
not prove the missing theorem; it says how to classify a proposed proof or
identity against the finite verifier chain already built.

## Primary Theorem Targets

```text
prod_{A in base*K_trace*D_segment} y(A)/y(A+T) = theta2^-1
prod_{A in base*K_trace*D_segment} y(A+T)/y(A) = theta2
```

with

```text
y(Q) = -g(2Q)/g(Q)^4
base = (25,25)
K    = (57,0), order 25
D    = (22,3), short non-subgroup segment
T    = (38,113)
```

The compact theorem target is still:

```text
center_base = (44,166)
half_shift  = (56,28)
orientation = theta2 or theta2^-1
```

## Finite-only Payloads

These are accepted verifier shadows, but they are not arithmetic proofs by
themselves:

```text
six-cell source quotient packet
quotient factor classes base=(1,25), D=(1,3), T=(2,113)
exact 300-term sparse theta2 or theta2^-1 divisor footprint
```

## Value-level Routes

The old ambient `780` denominator remains branch-ambiguous:

```text
gcd(4^780 - 1, p - 1) = 11
```

But the active support-period `156` certificate has a unique `F_p` root:

```text
gcd(4^156 - 1, p - 1) = 1
```

So a value-level theorem route is not automatically dead, but it must provide
the full period-156 fixedness/telescoping context.  A bare ambient-order value
claim still needs branch selection.

## First Falsifiers

Reject immediately if a proposed route:

```text
treats D as an order-3 subgroup norm
omits or absorbs T in the K quotient
uses a post-hoc abs(4) coefficient filter as the theorem
uses only formal [2] norm/inverse transport
submits q-cycle coordinates as source-packet coordinates
```

Recorded hard facts:

```text
visible 3D = (0,9), so D is not order 3
T class    = (2,113), so T is nontrivial in the quotient
payload    = 75 centers -> 150 y-values -> 300 g-divisor terms
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_theorem_interface_gate.py
```

Expected marker:

```text
robert_ksy_theta2_theorem_interface_rows=1/1
```

## Lit-search Brief

Look for a Kubert-Lang / Siegel-unit / KSY distribution identity that can prove
a `D=2` normalized-y product over a subgroup trace times a short non-subgroup
arithmetic segment, with the support-period telescoping context available for
value-level normalization.
