# P25 KSY-y Subsqrt Moonshot Budget Ladder

Updated: 2026-06-14 13:20 PDT

## Purpose

This checkpoint ties the current compact KSY/Yang/Hilbert-90 theorem route to
the actual Pomerance scale:

```text
p = 10^25 + 13
sqrt_floor = 3162277660168
```

The result is positive but carefully bounded: every current finite moonshot
checkpoint is far below `sqrt(p)`, but none is a DANGER3 submission until it
produces a concrete `(p,A,x0)` triple passing official `vpp.py`.

## Current Finite Budgets

```text
quotient factor input cells        = 3
source quotient packet support     = 6
quotient factor support budget     = 31
Y_507 quotient support             = 12
KSY fixed atoms                    = 75
H0 positive factors                = 78
H0 negative factors                = 78
H0 potential support               = 156
raw Siegel footprint               = 300
period norm support                = 312
telescoping compact budget         = 975
support-resolvent union support    = 11700
support-resolvent term budget      = 46800
```

The current maximum is:

```text
support_resolvent_term_budget = 46800
sqrt_floor // 46800           = 67570035
```

The older ambient-period shadow budget is:

```text
old_ambient_resolvent_shadow = 234000
sqrt_floor // 234000         = 13514007
```

It is still below `sqrt(p)`, but it is not the selected route because the
support-period `156` route is sharper.

## Value Route

```text
period 156: gcd(4^156 - 1, p - 1) = 1
period 780: gcd(4^780 - 1, p - 1) = 11
```

So period `156` is the selected value route: the `F_p^*` root is unique there.
The ambient period-`780` route keeps a `mu_11` ambiguity.

## Acceptance Ladder

```text
finite_spine_payload:
  missing = challenge-legal arithmetic producer theorem

period156_value_theorem:
  missing = DANGER3 finite-identity/non-CM framing

danger3_policy_unblocked:
  missing = X_1(8112)/X_1(16) bridge and concrete A,x0

x16_surface_reached:
  missing = valid halving chain from xP16 to x0

verified_pomerance_triple:
  missing = none
```

Current submission-ready rows:

```text
0
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_subsqrt_moonshot_budget_ladder_gate.py
```

Marker:

```text
ksy_y_subsqrt_moonshot_budget_ladder_rows=1/1
```
