# P25 KSY-y H0 Translate X1(16) Route Propagation

Updated: 2026-06-14 15:05 PDT

## Purpose

The H0-translate compatibility gate says which finite odd-level targets are
legal.  This checkpoint pushes that result one step downstream: a theorem hit
on any legal `H0_translate` should enter the same X_1(8112) / X_1(16)
extraction ladder as canonical `H0`, while formal or nonlegal H-like objects
must stop before X1 routing.

## Legal Inputs

```text
support period                  = 156
legal H0 products               = 4
canonical H0 rows               = 1
noncanonical H0_translate rows  = 3
legal multipliers               = 1, 2, 4, 8
```

All four legal products are source-stage closures only after exact value,
boundary, period-156, and arithmetic-source context.  They still do not give a
DANGER3 certificate by themselves.

## Downstream Route

For each of the four legal H0 products, the no-cross-level claim is classified
as:

```text
upstream_odd_value_no_cross_level_bridge
missing = X_1(16) relation or X_1(8112) fiber-product theorem
```

A representative noncanonical translate, multiplier `2`, then exercises the
full downstream ladder:

```text
X_1(8112) bridge but no X_1(16) specialization
X_1(16) relation but no actual y
y but no Montgomery surface / xP16
X_1(16) surface but no DANGER3 framing
DANGER3-framed surface but no halving chain or x0
x0 payload but no official vpp.py verification
```

## Guardrail

The nonlegal `H0_translate` payload and the formal one-coset H payload are
blocked by H0-translate compatibility before X1 routing.  The X1 classifier
accepts the label `H0_translate`; this gate records the extra precondition
that the payload must be one of the four legal 78-over-78 products.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_x16_route_propagation_gate.py
```

Expected marker:

```text
ksy_y_h0_translate_x16_route_propagation_rows=1/1
```

## Interpretation

This makes future expert answers easier to route.  A theorem on any legal H0
translate is real upstream progress, but it still needs the cross-level
X_1(8112) bridge, X_1(16) specialization, DANGER3 framing, a halving chain or
`x0`, and official `vpp.py` before it becomes a submission.
