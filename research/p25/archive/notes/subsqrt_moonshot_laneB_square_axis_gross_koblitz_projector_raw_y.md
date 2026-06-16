# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Projector Raw-Y Control

Date: 2026-06-13

## Result

The formal Gross-Koblitz Frobenius projector closes the finite square-axis
`theta_{3,1}` payload gap.

Build the quotient packet as:

```text
507 * (C13 fiber background + S * (binom(h,t) - projector(h,t)))
```

where the projector is the quadratic Frobenius-frequency term

```text
selected(h,t) * (DC - ALT) / ord_N(p).
```

The corrected seed payload is:

```text
(0,0)=1
(1,0)=1
(1,1)=1
(2,0)=1
(2,1)=1
(2,2)=1
```

The 18 residual quotient terms are:

```text
43, 86, 95, 129, 138, 147,
215, 258, 267, 301, 310, 319,
387, 430, 439, 473, 482, 491
```

## Harness Check

The gate verifies:

```text
base support = 234
residual support = 18
quotient support = 252
quotient packet exact = true
raw Y length = 12675
raw Y nonzero positions = 6300
ray-local theta31 harness = pass
```

So if an arithmetic HD/GK/Barnes unit phase realizes the Frobenius projector,
the resulting kernel-trivial raw `Y[e]` vector already satisfies the existing
square-axis `theta_{3,1}` producer-facing harness.

## Consequence

The Jacobi moonshot is now sharply localized:

```text
finite payload shape: solved formally
raw-Y harness compatibility: solved formally
remaining gap: arithmetic realization of the projector/unit phase
```

This does not produce a certificate yet.  It removes a large class of possible
downstream finite mismatches and makes the next falsifier exact: proposed
HD/GK/Barnes identities must realize this projector, not merely reproduce its
support or a dense scalar repair.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py
```
