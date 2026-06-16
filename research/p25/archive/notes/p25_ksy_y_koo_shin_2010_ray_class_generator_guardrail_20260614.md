# P25 KSY-y: Koo-Shin 2010 Ray-Class Generator Guardrail

Updated: 2026-06-14 12:20 PDT

## Purpose

Koo-Shin 2010 Theorems `9.8`, `9.10`, and `9.11` are real ray-class generator
context.  This note records why they do not by themselves produce the active
p25 conductor-39 source.

The active source is:

```text
U_chi = -chi_39
```

It is a mixed character word on the `24` units modulo `39`, with vanishing
proper pushforwards to both mod `3` and mod `13`.

## Finite Comparison

At `N=39`:

```text
phi(39) = 24
Theorem 9.8 power  = 24*N = 936
Theorem 9.10 power = 12*N = 468
```

The relevant shapes are:

```text
target U_chi:
  product word = yes
  coefficients = 12 entries -1, 12 entries +1
  proper pushforwards vanish = yes
  scaled U_chi equality = yes

Theorem 9.8 T_N:
  shape = all-unit sum, not one product word
  coefficients = 24 entries 936
  proper pushforwards vanish = no
  scaled U_chi equality = no

Theorem 9.10 M_N:
  shape = all-unit product
  coefficients = 24 entries 468
  proper pushforwards vanish = no
  scaled U_chi equality = no

Theorem 9.10 normalized single-index generator:
  shape = one spike plus all-unit background
  coefficients = one entry 10764, 23 entries -468
  proper pushforwards vanish = no
  scaled U_chi equality = no
  residual from best scaled U_chi has support 12
```

## Route Classifier

```text
ray-class generator vocabulary:
  decision = continue_as_context_only
  missing  = finite-field identity for the exact p25 source

all-unit or single-index generator as U_chi:
  decision = reject_as_direct_source
  missing  = proper pushforwards vanish and scaled U_chi equality

independent mixed-character theorem:
  decision = source_shape_ready_value_theorem_missing
  missing  = finite-field value/divisor theorem, Yang/H90 descent, and extraction
```

## Consequence

Koo-Shin 9.x remains useful vocabulary for CM/ray-class generators and Shimura
reciprocity.  It does not replace the conductor-39 source theorem target.

The remaining upgrade is still:

```text
independent mixed-character finite-field value/divisor theorem
Yang/Hilbert-90 descent
X_1(16) extraction surface
halving payload
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_2010_ray_class_generator_guardrail_gate.py
```

Marker:

```text
ksy_y_koo_shin_2010_ray_class_generator_guardrail_rows=1/1
```
