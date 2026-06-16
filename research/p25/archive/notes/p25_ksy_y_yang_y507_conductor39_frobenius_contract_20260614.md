# P25 KSY-y Yang Y507 Conductor-39 Frobenius Contract

Updated: 2026-06-14 09:16 PDT

## Purpose

The period-norm conductor gate reduced the dense norm to a conductor-`39`
quadratic character inflated to level `507`.  This checkpoint records the
finite-field arithmetic that any value-side explanation must respect.

## Cyclotomic Arithmetic

For

```text
p = 10^25 + 13
```

we have:

```text
p mod 39 = 23
ord_3(p)  = 2
ord_13(p) = 6
ord_39(p) = 6
p^3 = -1 mod 39
p^6 =  1 mod 39
```

So primitive `39`th roots are not in `F_p`; they first appear in degree `6`.
Primitive `13`th roots also first appear in degree `6`, while primitive `3`rd
roots first appear in degree `2`.

The small gcd scan is:

```text
degree 1: gcd(39, p^d - 1) = 1,  gcd(39, p^d + 1) = 3
degree 2: gcd(39, p^d - 1) = 3,  gcd(39, p^d + 1) = 1
degree 3: gcd(39, p^d - 1) = 1,  gcd(39, p^d + 1) = 39
degree 4: gcd(39, p^d - 1) = 3,  gcd(39, p^d + 1) = 1
degree 5: gcd(39, p^d - 1) = 1,  gcd(39, p^d + 1) = 3
degree 6: gcd(39, p^d - 1) = 39, gcd(39, p^d + 1) = 1
```

## Quadratic Field Check

The conductor-`39` primitive quadratic character is associated to the
fundamental discriminant:

```text
D = -39
```

Here:

```text
p mod 4 = 1
D mod 4 = 1
(-39 / p) = -1
```

So `sqrt(-39)` is not in `F_p`.

## Verdict

Positive payload:

```text
the conductor-39 character is the right value-side shadow, but literal
order-39 root data lives first over degree 6, and sqrt(-39) is not in F_p
```

First missing clause:

```text
this is a routing constraint, not the finite-field value/divisor theorem or
DANGER3 extraction
```

Practical effect:

```text
accept conductor-39 value explanations only if they include the degree-6
cyclotomic orbit or a conjugate/norm descent back to F_p; reject direct F_p
order-39-root or sqrt(-39) scalar shortcuts
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_frobenius_contract_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_frobenius_contract_rows=1/1
```
