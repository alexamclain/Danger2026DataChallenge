# P25 KSY-y Yang Y507 Primitive-Factor Word

Updated: 2026-06-14 09:06 PDT

## Purpose

`Y_507` is now the compact quotient target.  This checkpoint translates it from
Yang's one-dimensional `X_1(507)` residue coordinate into the earlier
primitive-`D` word coordinate, so source queries can use either language
without mixing them up.

## Coordinate Change

Yang residue `a` and the earlier `q = 169*row + 3*c` coordinate differ by:

```text
q = 172*a mod 507
```

The primitive-`D` coordinate then multiplies by:

```text
D_q^-1 = 94 mod 507
```

So the direct Yang-to-primitive multiplier is:

```text
172 * 94 = 451 mod 507
```

## Factor Word

The older primitive bridge word is:

```text
U_507 = z^121 * (1 + z + z^2) * (1 - z^263)
```

The compact normalized-y target is exactly:

```text
Y_507 = [2]^*U_507 / U_507^4
```

In exponent-word form:

```text
121 -> -4
122 -> -4
123 -> -4
242 ->  1
244 ->  1
246 ->  1
261 -> -1
263 -> -1
265 -> -1
384 ->  4
385 ->  4
386 ->  4
```

Equivalently, the four blocks are:

```text
-4 * {121,122,123}
 +1 * {242,244,246}
 -1 * {261,263,265}
 +4 * {384,385,386}
```

## Verdict

Positive payload:

```text
Y_507 is exactly [2]^*U_507/U_507^4 in the primitive-D word coordinate, with
U_507=z^121(1+z+z^2)(1-z^263)
```

First missing clause:

```text
the primitive factor word still needs a theorem proving its finite-field
value/divisor identity and DANGER3 extraction
```

Practical effect:

```text
use this primitive factor word as the compact source-query form when searching
for Kubert-Lang/Sprang/KSY theorem hits
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_primitive_factor_word_gate.py
```

Marker:

```text
ksy_y_yang_y507_primitive_factor_word_rows=1/1
```
