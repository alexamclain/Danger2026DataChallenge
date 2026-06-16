# P25 KSY-y H90 / Y507 Value-Theorem Intake

Updated: 2026-06-14 19:57 PDT

## Purpose

The bridge spine gives a narrow value-side target:

```text
exact P -> Y_507 -> Norm_156(Y_507) -> legal sparse H0
```

This note records what a future theorem hit must contain before it counts as
moonshot progress.

## Live Targets

Accepted target objects are:

```text
exact_P
Y_507
canonical_H0
H0_translate
conductor39_U_chi
```

The canonical H0 product is:

```text
P0 = {7, 17, 23, 34, 37, 38}
N0 = {4, 8, 10, 11, 20, 25}

H0 = 6 * (
  sum_{a in P0, k=0..12} [a + 39k]
  -
  sum_{b in N0, k=0..12} [b + 39k]
)
```

with:

```text
positive factors = 78
negative factors = 78
boundary         = (1 - Frob_p)H0 = Norm_156(Y_507)
```

Any `<2>` translate of H0 is equivalent for theorem intake.

## Reject Immediately

The gate rejects:

```text
formal_one_coset_H
prime13_projection
c169_projection
ambient_780_value
field-generation claims
```

Reason: these either lose the mixed source, fail legal H90/Yang selection, or
leave the wrong branch/root ambiguity.

## Required For Closure

A live theorem hit must supply all of:

```text
verified theorem body
exact target object
75->300->12->312->156 bridge-spine context
Yang/Yu or legal H90 object
H0 boundary / period-156 context when value-level
finite-field value identity or divisor/additive theorem
challenge-legal arithmetic source theorem
DANGER3 finite-identity/non-CM framing
extraction to concrete (A, x0)
official vpp.py verification
```

The gate separates intermediate states:

```text
finite payload only                    -> not a theorem
exact target, no value/divisor theorem -> live target only
value theorem without period 156       -> branch/root missing
finite identity without source theorem -> verifier payload only
source theorem without DANGER3 framing -> policy/framing missing
DANGER3 framing without extraction     -> extraction missing
extraction without verified triple     -> run official vpp.py
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py
```

Marker:

```text
ksy_y_h90_value_theorem_intake_rows=1/1
```

Dependency marker:

```text
ksy_y_yang_ksy_product_h90_bridge_spine_rows=1/1
```

The routine gate uses the recorded bridge-spine marker and fixed bridge
constants, while still running the local value-theorem classifier rows.
