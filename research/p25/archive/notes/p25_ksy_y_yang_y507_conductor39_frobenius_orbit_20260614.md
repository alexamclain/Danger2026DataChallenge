# P25 KSY-y Yang Y507 Conductor-39 Frobenius Orbit

Updated: 2026-06-14 09:20 PDT

## Purpose

The conductor-`39` Frobenius contract says primitive `39`th roots first appear
over degree `6`.  This checkpoint records the action of `Frob_p` on the pure
conductor-`39` period-norm exponent word.

## Frobenius Action

For

```text
p = 10^25 + 13
p mod 39 = 23
chi_39 = chi_3 * chi_13
Norm_156(Y_507) = -6 * chi_39
```

we have:

```text
chi_39(p)  = -1
chi_39(-1) = -1
```

Thus `Frob_p` sends the conductor-`39` word to its negative.

The multiplier sequence is:

```text
p^1 = 23 mod 39  -> negative word
p^2 = 22 mod 39  -> same word
p^3 = 38 mod 39  -> negative word
p^4 = 16 mod 39  -> same word
p^5 = 17 mod 39  -> negative word
p^6 =  1 mod 39  -> same word
```

So the signed word has exact Frobenius period `2`, even though the underlying
primitive root data lives in degree `6`.

## Unit Orbits

The `24` unit residues modulo `39` split into four Frobenius orbits of length
`6`, each with alternating coefficients:

```text
(1, 23, 22, 38, 16, 17)   -> (-6, 6, -6, 6, -6, 6)
(2, 7, 5, 37, 32, 34)     -> (-6, 6, -6, 6, -6, 6)
(4, 14, 10, 35, 25, 29)   -> (-6, 6, -6, 6, -6, 6)
(8, 28, 20, 31, 11, 19)   -> (-6, 6, -6, 6, -6, 6)
```

Consequences in additive exponent notation:

```text
word + Frob_p(word) = 0
sum_{i=0..5} Frob_p^i(word) = 0
sum_{i=0..2} Frob_p^i(word) = word
```

## Verdict

Positive payload:

```text
Frob_p flips the conductor-39 period-norm word, so a naive degree-6 norm of the
pure character word is trivial
```

First missing clause:

```text
this Frobenius orbit law is not the finite-field value/divisor theorem or
DANGER3 extraction
```

Practical effect:

```text
reject value-side candidates that simply norm the pure conductor-39 character
down from degree 6; continue only with a twisted trace, ratio, non-pure lift,
or explicit conjugate descent that survives the alternating Frobenius signs
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_frobenius_orbit_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_frobenius_orbit_rows=1/1
```
