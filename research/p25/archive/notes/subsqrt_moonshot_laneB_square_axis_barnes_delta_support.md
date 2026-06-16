# Subsqrt Moonshot Lane B Square-Axis Barnes Delta Support Screen

Date: 2026-06-13

## Result

The first Barnes/Greene screen is now finite and support-only.

It separates three cases:

```text
order-3 HP product delta       -> killed
full C507 seed-exponent delta  -> support-live
p^2 orbit-closed delta         -> killed
```

The target remains:

```text
O*(1-E) = indicator((h,t) = (2,1))
```

## Evidence

A single order-3 affine product delta through the anomaly always has line
support.  The four unique supports are:

```text
(0,0), (1,2), (2,1)
(0,1), (1,1), (2,1)
(0,2), (1,0), (2,1)
(2,0), (2,1), (2,2)
```

So an HP identity that only sees the order-3 Jacobi product parameters fires
on two extra cells and is killed.

The full seed-exponent point delta is different:

```text
q = 43*(h+1) + 9*t
q = 138
```

This fires exactly at:

```text
(h,t) = (2,1)
```

and its outer `S` image is exactly:

```text
138, 310, 482
```

Finally, making the same point delta `p^2`-orbit closed is much too large:

```text
p^2 mod 507 = 373
orbit length = 39
outer S support = 117 quotient classes
```

## Consequence

The Barnes/Greene lane is still alive, but only in a narrow form:

- kill HP-only if the delta is only an order-3 product condition;
- continue if the identity realizes the full `C_507` seed-exponent point
  delta `q=138`;
- kill any version that first closes under the full `p^2` orbit before the
  local point/endpoint correction appears.

No Gauss-sum evaluation should happen before this support screen.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_barnes_delta_support_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_barnes_delta_support_gate.py
```
