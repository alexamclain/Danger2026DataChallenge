# P25 KSY-y Yang Y507 Period-Norm Character

Updated: 2026-06-14 09:09 PDT

## Purpose

The compact target

```text
Y_507 = [2]^*U_507 / U_507^4
U_507 = z^121(1+z+z^2)(1-z^263)
```

has support period `156` under doubling.  This checkpoint tests a tempting
value-side shortcut: perhaps the product over the support period telescopes
away.  It does not.

## Period Orbit

For `U_507`:

```text
word support                 = 6
doubling period              = 156
orbit union support          = 468
orbit visit counts           = 2 per occupied residue
period-norm support          = 312
period-norm coefficient count = (-2,156), (2,156)
period-norm gcd classes      = gcd 1 only, 312 residues
```

For `Y_507`:

```text
word support                 = 12
doubling period              = 156
orbit union support          = 468
orbit visit counts           = 4 per occupied residue
period-norm support          = 312
period-norm coefficient count = (-6,156), (6,156)
period-norm gcd classes      = gcd 1 only, 312 residues
```

The nonunit layer cancels in the period norm.

## Character Shape

Let

```text
H = <2> inside (Z/507Z)^*
```

Then `|H|=156`, and the unit group is the disjoint union `H union -H`.

The `Y_507` period norm is:

```text
+6 on -H
-6 on  H
```

Equivalently, it is the dense signed index-two unit character.  The same scan
also verifies the CRT/log-parity description of `H`: for unit `r`, membership
in `<2>` is determined by the parity of `log_2(r mod 169)` together with
`r mod 3`.

The exact relation to the `U_507` norm is:

```text
Norm_156(Y_507) = -3 * Norm_156(U_507)
```

in additive exponent-word notation.

## Verdict

Positive payload:

```text
the support-period norm of Y_507 is a dense signed unit character, not a
trivial telescope
```

First missing clause:

```text
this period-norm character is structural value-side data, not the finite-field
value/divisor theorem or DANGER3 extraction
```

Practical effect:

```text
value-side theorem hits must explain this dense unit-character period norm;
reject claims that treat the support-period product as trivial, lower-level, or
sparse after period telescoping
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_period_norm_character_gate.py
```

Marker:

```text
ksy_y_yang_y507_period_norm_character_rows=1/1
```
