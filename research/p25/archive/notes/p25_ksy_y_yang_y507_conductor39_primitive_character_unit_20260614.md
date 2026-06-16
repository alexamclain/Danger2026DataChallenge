# P25 KSY-y Yang Y507 Conductor-39 Primitive Character Unit

Updated: 2026-06-14 09:31 PDT

## Purpose

The modular-unit legality checkpoint showed that both

```text
W     = -6 * chi_39
V_bal = -3 * chi_39
```

are legal `X_1(39)` modular-unit exponent words.  This checkpoint records the
primitive legal unit underneath them:

```text
U_chi = -chi_39
```

## Primitive Unit

`U_chi` has:

```text
support                  = 24
coefficient counts       = (-1,12), (1,12)
Yang/Yu modular-unit ok  = yes
Frob_p(U_chi)            = -U_chi
```

It is the primitive legal conductor-`39` character unit in this chain.

## Power Relations

In exponent notation:

```text
V_bal = 3 * U_chi
W     = 6 * U_chi
```

Equivalently, multiplicatively:

```text
V_bal = U_chi^3
W     = U_chi^6
```

The finite-field root controls are:

```text
gcd(3, p - 1) = 1
gcd(6, p - 1) = 2
```

So if a value theorem has already descended a value to `F_p^*`, cube-root
normalization adds no branch ambiguity, while sixth-root normalization still
has the expected sign ambiguity.

## Verdict

Positive payload:

```text
the legal conductor-39 target has a primitive unit U_chi=-chi_39; V_bal is its
cube and W is its sixth power
```

First missing clause:

```text
primitive modular-unit normalization is not the finite-field value/divisor
theorem or DANGER3 extraction
```

Practical effect:

```text
allow source theorems to emit U_chi, V_bal, or W, but require the same
Frobenius/Hilbert-90 descent data; cube-root normalization in F_p^* has no
branch if the value is already in F_p
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_primitive_character_unit_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_primitive_character_unit_rows=1/1
```
