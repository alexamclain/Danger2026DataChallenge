# P25 KSY-y H0 Translate Source Obligation

Updated: 2026-06-14 15:10 PDT

## Purpose

This checkpoint separates two positive facts from the still-missing theorem.

Koo-Shin 6.2 certifies the compact conductor-39 source object.  The H0
translate gates certify four legal support-156 targets.  The moonshot still
needs a source theorem that emits an exact finite-field value identity or
divisor/additive identity for one legal H0 product.

## Legal Target Family

```text
support period                  = 156
legal H0 products               = 4
canonical H0 rows               = 1
noncanonical H0_translate rows  = 3
legal multipliers               = 1, 2, 4, 8
product shape                   = 78 positive / 78 negative factors
boundary                        = (1-Frob_p)H0 = Norm_156(Y_507)
```

## Obligation Ladder

Source certification only:

```text
Koo-Shin 6.2 certifies W on X_1(39)
missing = theorem that evaluates or identifies Norm_156(Y_507)
```

Live target but not closed:

```text
legal H0 translate plus boundary
missing = finite-field value identity or divisor/additive theorem
```

Conditional:

```text
value theorem without period-156 branch/root/telescoping context
finite verifier payload without an arithmetic source theorem
```

Source-stage closure:

```text
exact value identity for a legal H0 translate with period-156 context
exact divisor/additive identity for a legal H0 translate with boundary
```

Rejected:

```text
nonlegal H0 translate payload
formal one-coset H payload
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_source_obligation_gate.py
```

Expected marker:

```text
ksy_y_h0_translate_source_obligation_rows=1/1
```

## Interpretation

This is the theorem-facing ask.  A paper, proof, or expert answer helps if it
emits a value or divisor/additive identity for any one of the four legal H0
products.  Boundary-only, source-certification-only, and finite-verifier-only
answers are useful diagnostics but do not close the source stage.
