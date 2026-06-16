# P25 KSY-y Yang Y507 Conductor-39 Modular-Unit Legality

Updated: 2026-06-14 09:27 PDT

## Purpose

The Hilbert-90 boundary gate produced three useful potentials for the
conductor-`39` word:

```text
W     = -6 * chi_39
V_bal = -3 * chi_39
V_pos =  6 * 1_{chi_39=-1}
V_neg = -6 * 1_{chi_39= 1}
```

This checkpoint separates formal group-ring usefulness from Yang/Yu
modular-unit legality on `X_1(39)`.

## Legal Rows

Both `W` and the balanced Hilbert-90 potential pass:

```text
W:
  support                  = 24
  coefficient counts       = (-6,12), (6,12)
  exponent sum mod 12      = 0
  quadratic sum mod 39     = 0
  signed orbit bad counts  = (3,0), (13,0)
  Yang/Yu modular-unit ok  = yes

V_bal:
  support                  = 24
  coefficient counts       = (-3,12), (3,12)
  exponent sum mod 12      = 0
  quadratic sum mod 39     = 0
  signed orbit bad counts  = (3,0), (13,0)
  Yang/Yu modular-unit ok  = yes
```

So `V_bal=-3*chi_39` is a legitimate `X_1(39)` modular-unit exponent word.

## Formal-Only Rows

The sparse one-coset gauges pass the elementary congruences but fail the
Yang/Yu signed orbit condition:

```text
V_pos:
  support                  = 12
  coefficient counts       = (6,12)
  exponent sum mod 12      = 0
  quadratic sum mod 39     = 0
  signed orbit bad counts  = (3,6), (13,1)
  Yang/Yu modular-unit ok  = no

V_neg:
  support                  = 12
  coefficient counts       = (-6,12)
  exponent sum mod 12      = 0
  quadratic sum mod 39     = 0
  signed orbit bad counts  = (3,6), (13,1)
  Yang/Yu modular-unit ok  = no
```

Thus the support-`12` gauges are formal Hilbert-90 potentials, not standalone
Yang modular units.

## Verdict

Positive payload:

```text
W=-6*chi_39 and V_bal=-3*chi_39 are legal X_1(39) modular-unit words; the
sparse one-coset Hilbert-90 gauges are formal only
```

First missing clause:

```text
modular-unit legality does not provide the finite-field value/divisor theorem
or DANGER3 extraction
```

Practical effect:

```text
ask source theorems for the balanced legal modular-unit potential, or for a
formal Hilbert-90 ratio that explains why a sparse gauge is allowed; do not
advertise V_pos/V_neg as standalone Yang units
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_modular_unit_legality_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_modular_unit_legality_rows=1/1
```
