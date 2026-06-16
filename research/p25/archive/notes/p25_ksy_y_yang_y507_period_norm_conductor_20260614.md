# P25 KSY-y Yang Y507 Period-Norm Conductor

Updated: 2026-06-14 09:13 PDT

## Purpose

The period-norm character checkpoint showed that `Norm_156(Y_507)` is dense on
the units of `Z/507Z`.  This checkpoint asks whether that dense unit character
is genuinely conductor `507`, or whether it descends.

## Descent Result

The coefficient word descends exactly to modulus `39`:

```text
modulus 1     descends no
modulus 3     descends no
modulus 13    descends no
modulus 39    descends yes
modulus 169   descends no
modulus 507   descends yes
```

At conductor `39`, the quotient support has the `24` unit residues, with
coefficient counts:

```text
(-6,12), (6,12)
```

The failed lower/proper readings are concrete:

```text
mod 3    fails at residues 1 and 7:   -6 versus +6
mod 13   fails at residues 1 and 14:  -6 versus +6
mod 169  fails at residues 1 and 170: -6 versus +6
```

## Character Formula

Let

```text
chi_3  = nontrivial quadratic character modulo 3
chi_13 = Legendre character modulo 13
chi_39 = chi_3 * chi_13
```

Then:

```text
Norm_156(Y_507) = -6 * chi_39 inflated to level 507
Norm_156(U_507) =  2 * chi_39 inflated to level 507
```

The `+6` residues modulo `39` are:

```text
7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38
```

The `-6` residues modulo `39` are:

```text
1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32
```

## Verdict

Positive payload:

```text
the period norm is not a conductor-507 mystery; it is a conductor-39 quadratic
character inflated to level 507
```

First missing clause:

```text
conductor descent is a value-side constraint, not the finite-field
value/divisor theorem or DANGER3 extraction
```

Practical effect:

```text
search value-side sources for a conductor-39 quadratic character norm or period
formula inflated to level 507; reject conductor-3, conductor-13, conductor-169,
or arbitrary conductor-507 explanations
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_period_norm_conductor_gate.py
```

Marker:

```text
ksy_y_yang_y507_period_norm_conductor_rows=1/1
```
