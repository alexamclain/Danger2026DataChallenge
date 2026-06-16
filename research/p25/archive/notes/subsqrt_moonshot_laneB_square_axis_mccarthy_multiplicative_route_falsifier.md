# p25 Lane B: McCarthy Multiplicative-Route Falsifier

Updated: 2026-06-13 13:12 PDT

## Result

The valid q-power route is:

```text
R(q) = LHS(q) / main_sum(q)
R(q)^2029 - 1
```

The tempting additive routes are killed:

```text
(LHS(q) - main_sum(q))^2029
LHS(q)^2029 - main_sum(q)^2029
```

The subtlety is that the invalid routes are also singleton-supported.  They do
not fail a support-only test; they fail by producing the wrong target
coefficient and wrong multiplicative order.

## Verified Values In F_20574061

```text
valid R^2029 - 1:
  support = (138,)
  R(138)^2029 = 12801419
  ord(R(138)^2029) = 39
  R(138)^2029 - 1 = 12801418
  ord(R(138)^2029 - 1) = 20574060

invalid (LHS-main)^2029:
  support = (138,)
  target value = 19995471
  target order = 507

invalid LHS^2029-main^2029:
  support = (138,)
  target value = 6688559
  target order = 5143515
```

## Interpretation

Any theorem attempt that only matches singleton support is insufficient.  The
producer must form a multiplicative quotient first, then apply q-power
projection to that unit.  Additive powering or Frobenius-style subtraction is
killed even when it appears to preserve the endpoint support.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_multiplicative_route_falsifier_gate.py
```

Observed:

```text
square_axis_mccarthy_multiplicative_route_falsifier_rows=1/1
```
