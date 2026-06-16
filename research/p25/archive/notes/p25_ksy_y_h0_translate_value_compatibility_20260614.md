# P25 KSY-y H0 Translate Value Compatibility

Updated: 2026-06-14 15:00 PDT

## Purpose

This checkpoint removes an ambiguity in the H0/Y507 route.  A useful
`H0_translate` is not an arbitrary formal Hilbert-90 object: it is one of the
four legal sparse conductor-39 Yang-fiber products already certified by the
product-normal-form gate.

## Result

The legal family is:

```text
support period                         = 156
doubling subgroup mod 39               = (1,2,4,8,16,32,25,11,22,5,10,20)
canonical stabilizer                   = (1,16,22)
quotient representatives               = (1,2,4,8)
legal products                         = 4
each legal product                     = 78 positive / 78 negative factors
each legal boundary                    = (1-Frob_p)H0 = Norm_156(Y_507)
formal one-coset controls              = rejected
```

The multiplier-`1` row is the canonical `H0`; the multipliers `2`, `4`, and
`8` are the noncanonical `H0_translate` rows.  All four route as source-stage
closures if a theorem gives the exact value identity with boundary and
period-156 context.

## Guardrails

Accepted only as source-stage closure:

```text
canonical_H0 or H0_translate value
exact target
KSY/Yang/H90 bridge preserved
legal sparse Yang/H90 object
boundary to Norm_156(Y_507)
period-156 branch/root/telescoping context
challenge-legal arithmetic source theorem
```

Still conditional:

```text
missing boundary to Norm_156(Y_507)
missing period-156 value context
finite payload without an arithmetic source theorem
```

Rejected:

```text
formal one-coset H
nonlegal H0 translate payloads
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_value_compatibility_gate.py
```

Expected marker:

```text
ksy_y_h0_translate_value_compatibility_rows=1/1
```

## Interpretation

This is a positive narrowing artifact.  It lets future Koo-Shin/Yang/Hilbert-90
theorem hits target any legal translate, not only the canonical H0, while also
blocking the common mistake of accepting formal H-like products that share a
boundary shape but fail the legal sparse selector.
