# P25 Lane B: Robert KSY Normalized-y Arithmetic Shape

Updated: 2026-06-13 16:12 PDT

## Purpose

The normalized-y product gate found the finite source law

```text
prod_{A in base*K_trace*D_segment} y(A)/y(A+T) = theta2^-1
y(Q) = -g(2Q)/g(Q)^4
```

This gate separates the honest finite arithmetic pieces from the remaining
theorem debt.

## Arithmetic Shape

```text
base class = (1,25)
D class    = (1,3)
T class    = (2,113)
```

The quotient packet is exactly the six accepted source cells:

```text
(1,25):+1  (2,28):+1  (0,31):+1
(0,138):-1 (1,141):-1 (2,144):-1
```

The `K` factor is an honest subgroup trace:

```text
K = (57,0)
order(K) = 25
K_trace size = 25
K_trace is trivial in (C_75/K) x C_169
```

The `D` factor is not a subgroup norm:

```text
D = (22,3)
raw order(D)     = 12675
visible order(D) = 507
3D               = (66,9)
visible 3D       = (0,9)
```

So the length-3 factor is a short arithmetic segment, not a hidden order-3
subgroup product.

## Payload Counts

```text
centers                  = 75
y evaluation points      = 150
expanded g-divisor terms = 300
coefficient counts       = (-4,75), (-1,75), (1,75), (4,75)
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_normalized_y_arithmetic_shape_gate.py
```

Expected marker:

```text
robert_ksy_theta2_normalized_y_arithmetic_shape_rows=1/1
```

## Interpretation

The finite payload and certificate chain are now tight.  The remaining
moonshot proof target is not a finite verifier issue; it is the theorem-side
claim that this normalized-y product is a challenge-legal KSY/Siegel-unit
identity over a true `K` trace, a short non-subgroup `D` segment, and a
nontrivial quotient edge `T`.
