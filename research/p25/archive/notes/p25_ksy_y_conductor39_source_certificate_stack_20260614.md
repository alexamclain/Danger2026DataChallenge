# P25 KSY-y Conductor-39 Source Certificate Stack

Updated: 2026-06-14 12:32 PDT

## Purpose

The conductor-39 lane now has enough local and literature evidence to separate
two stages:

```text
source object certified
finite-field value/divisor theorem still missing
```

This note records the certified source stack so future work does not keep
re-proving the same source-side facts or accidentally treating them as a
submission.

## Certified Stack

```text
primitive unit:
  U_chi = -chi_39 is legal and has support 24 with +/-1 coefficients

mixed tensor:
  U_chi is -chi_3 tensor chi_13
  proper pushforwards to mod 3 and mod 13 vanish
  proper pullbacks fail

Koo-Shin 6.2:
  U_chi, V_bal=3*U_chi, and W=6*U_chi satisfy the one-axis X_1(39)
  congruences at N=39

Koo-Shin 9.x:
  ray-class all-unit and single-index generator shapes are guardrails only;
  they are not scaled U_chi and do not have vanishing proper pushforwards

Yang distribution:
  distribution_lift_39_to_507(6*U_chi) = Norm_156(Y_507)

Hilbert-90 normal form:
  canonical 78-over-78 Yang-fiber product normal form is recorded
```

## Route Classifier

```text
source_certificate_stack:
  decision = source_certified_value_theorem_missing
  missing  = finite-field value/divisor theorem for the conductor-39 source

source_certificate_as_product_closer:
  decision = reject_source_certificate_not_exact_75_atom_product
  missing  = exact p25 finite value/divisor identity and 75-atom/extraction bridge

source_certificate_as_submission:
  decision = reject_source_certificate_not_danger3_submission
  missing  = A,xP16 surface, halving payload, and vpp.py-verified x0
```

## Consequence

The source-side target is no longer diffuse.  The active conductor-39 theorem
ask is now:

```text
evaluate or identify U_chi, W, or Norm_156(Y_507)
as a finite-field value/divisor theorem with period-156/Hilbert-90 context
```

It still must pass downstream:

```text
DANGER3 framing
X_1(16) extraction surface
halving payload
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_source_certificate_stack_gate.py
```

Marker:

```text
ksy_y_conductor39_source_certificate_stack_rows=1/1
```
