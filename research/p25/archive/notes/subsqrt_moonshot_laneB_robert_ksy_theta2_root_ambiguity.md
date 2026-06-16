# P25 Lane B: theta2 Root-Ambiguity Gate

Updated: 2026-06-13 14:35 PDT

## Purpose

The theta2 resolvent denominator

```text
D = 4^780 - 1
```

is not invertible as an exponent on `F_p^*`, because `gcd(D,p-1)=11`.  This
gate checks whether the resulting `mu_11` ambiguity affects the finite bridge
payload.

## Result

The value-level ambiguity is real:

```text
gcd(D, p25 - 1)     = 11
gcd(D, p25 + 1)     = 3
gcd(D, 126751 - 1)  = 12675
gcd(D, 2029 - 1)    = 507
```

Over `F_p`, there are `11` distinct branches killed by the denominator power.

But each branch is a global root-of-unity scalar.  It has zero divisor:

```text
scalar divisor support        = 0
distinct branch divisor masks = 1
bridge contract still passes  = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_root_ambiguity_gate.py
```

Expected marker:

```text
robert_ksy_theta2_root_ambiguity_rows=1/1
```

## Interpretation

The root ambiguity is harmless for a divisor-level theta2 producer: global
scalar branches do not change the source bridge.

It is not harmless for a value-level multiplicative-unit producer: the `11`
field-value branches are genuinely distinct, and the finite bridge contract
cannot choose among them.
