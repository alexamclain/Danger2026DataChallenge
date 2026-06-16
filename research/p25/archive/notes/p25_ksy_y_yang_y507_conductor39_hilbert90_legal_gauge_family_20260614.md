# P25 KSY-y Yang Y507 Conductor-39 Hilbert-90 Legal Gauge Family

Updated: 2026-06-14 10:42 PDT

## Result

The Hilbert-90 boundary

```text
W = (1 - Frob_p) V
```

has a four-constant formal gauge kernel: add one constant on each of the four
length-`6` Frobenius orbits.  Yang/Yu modular-unit legality cuts this to the
two-parameter family

```text
(c0, c1, c2, c3) = (a, b, -a, -b)
```

on the Frobenius orbits

```text
(1, 23, 22, 38, 16, 17)
(2, 7, 5, 37, 32, 34)
(4, 14, 10, 35, 25, 29)
(8, 28, 20, 31, 11, 19)
```

The signed-orbit equations are:

```text
prime 3:  c0 + c2 = 0
prime 3:  c1 + c3 = 0
prime 13: c0 + c1 + c2 + c3 = 0
```

The prime-`13` equation is then redundant.

## Consequence

The balanced gauge remains the unique minimum-`L_infinity` legal gauge:

```text
V_bal = 3 * U_chi
constants = (0, 0, 0, 0)
support = 24
```

But it is not the only sparse legal option.  There are four legal mixed
support-`12` gauges, with constants:

```text
( 3,  3, -3, -3)
( 3, -3, -3,  3)
(-3,  3,  3, -3)
(-3, -3,  3,  3)
```

Each has coefficient counts:

```text
(-6, 6), (6, 6)
```

The earlier all-positive/all-negative one-coset sparse gauges remain formal
only:

```text
( 3,  3,  3,  3)  fails Yang/Yu signed orbit condition
(-3, -3, -3, -3)  fails Yang/Yu signed orbit condition
```

## Theorem Intake

Source/value hits may now target:

```text
V_bal = 3 * U_chi
one of the four legal mixed sparse Hilbert-90 gauges
```

They still must supply the finite-field value/divisor theorem, period-`156`
context for value output, DANGER3 framing, and extraction.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_hilbert90_legal_gauge_family_rows=1/1
```
