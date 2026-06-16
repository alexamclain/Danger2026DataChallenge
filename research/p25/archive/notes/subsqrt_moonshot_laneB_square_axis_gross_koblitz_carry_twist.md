# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Carry-Twist Falsifier

Date: 2026-06-13

## Result

The strict Gross-Koblitz carry-only explanation does **not** produce the
q-binomial anomaly.

The local no-borrow model writes the seed cells as

```text
a = t
b = h - t mod 3
a + b = h mod 3
```

A product-preserving character twist has the form

```text
(a,b) -> (a + tau, b - tau) mod 3.
```

The desired carry profile would be:

```text
carry = 0 on every selected no-borrow cell except (h,t) = (2,1)
carry > 0 on (h,t) = (2,1), the X^3Y anomaly
carry > 0 outside the no-borrow support
```

This is impossible in the one-digit model.  For every `h=2` cell, including
the anomaly `(2,1)`, all three product-preserving twists have carry `0`.

## Finite Scan

The gate checks:

- the arbitrary local one-cell obstruction at the anomaly;
- all affine twists in `(h,t)` over `F_3`;
- all affine twists in `(s,h,t)` over `F_3`, where `s` is the outer `S`-orbit
  layer.

Both affine scans have zero twists that make the anomaly carry-positive.

## Producer Consequence

This does not kill the whole Jacobi/Gross-Koblitz lane.  It kills the simple
valuation-only version of it.  A surviving Jacobi producer must add something
not present in the strict carry model:

- an additional unit-phase identity;
- a multi-digit/base-`p` interaction not visible in the local `F_3` digit;
- or a different collapse mechanism, such as a finite Barnes-delta resonance.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_carry_twist_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_gross_koblitz_carry_twist_gate.py
```
