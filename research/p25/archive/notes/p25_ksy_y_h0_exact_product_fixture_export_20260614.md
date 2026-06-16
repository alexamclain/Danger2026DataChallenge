# P25 KSY-y: H0 Exact-Product Fixture Export

Updated: 2026-06-14 17:31 PDT

## Purpose

The H0 theorem hunt now has stable byte-comparable fixtures for the four exact
legal product targets.  This turns future paper snippets, expert answers, or
subagent reports into a concrete comparison against files rather than a
hand-copied residue list.

These fixtures are finite targets, not arithmetic source theorems.

## Fixture Directory

```text
research/p25/h0_product_fixtures
```

## Product Family

Each row is a level-`507` lift of a conductor-`39` word with coefficient `+6`
on the positive set and `-6` on the negative set over all `13` Yang fibers.

```text
m=1, canonical_H0
  constants = (3,3,-3,-3)
  P = (7,17,23,34,37,38)
  N = (4,8,10,11,20,25)

m=2, H0_translate
  constants = (-3,3,3,-3)
  P = (7,14,29,34,35,37)
  N = (1,8,11,16,20,22)

m=4, H0_translate
  constants = (-3,-3,3,3)
  P = (14,19,28,29,31,35)
  N = (1,2,5,16,22,32)

m=8, H0_translate
  constants = (3,-3,-3,3)
  P = (17,19,23,28,31,38)
  N = (2,4,5,10,25,32)
```

Each lifted product has:

```text
positive terms = 78
negative terms = 78
support        = 156
boundary       = Norm_156(Y_507)
```

## Files

```text
h0_m1_canonical_lifted_product.txt   156 lines
h0_m2_translate_lifted_product.txt   156 lines
h0_m4_translate_lifted_product.txt   156 lines
h0_m8_translate_lifted_product.txt   156 lines
h0_exact_product_manifest.tsv          5 lines
h0_candidate_matcher_commands.sh      13 lines
```

SHA-256:

```text
e73d6e260221c3c719463d10a48dea1da68c847cce3d6c82eb6fccd8df216719  h0_m1_canonical_lifted_product.txt
b55114610c73fb5d55b7c8b9d348b1fecc9e9e9e67dbda6b1710043b1257e78e  h0_m2_translate_lifted_product.txt
ed97156c9ceb32e13b8f3421de52372e315b58349e5a88e4f2775e08ac28e16e  h0_m4_translate_lifted_product.txt
3a5bd427cd846ec9c30095315a8aacd8d387ec13605d1907262876b5d3bf686c  h0_m8_translate_lifted_product.txt
f5dc704c877dc41a29ab1bf9b0d0b2af0d0c825ba66cf191bcacdb33fca60ee6  h0_exact_product_manifest.tsv
6d922a86d22d9cd8f290fe2126c5eb2e0b584bf2887b995bd1a5fdc62c357d9e  h0_candidate_matcher_commands.sh
```

## Verified Meaning

The export gate verifies:

```text
exact_product_query_ok       = 1
candidate_matcher_ok         = 1
lifted_product_fixture_count = 4
manifest_row_count           = 4
lifted_product_line_counts   = (156,156,156,156)
value_candidate_rows_ok      = 4
divisor_candidate_rows_ok    = 4
wrong_product_rejected       = 1
```

So each fixture row is accepted by the H0 source-theorem matcher as:

```text
value + period-156 context      -> source_theorem_closed_policy_or_framing_missing
divisor/additive + H90 boundary -> source_theorem_closed_policy_or_framing_missing
```

and a nonlegal multiplier control is rejected.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_exact_product_fixture_export.py
```

Marker:

```text
ksy_y_h0_exact_product_fixture_export_rows=1/1
```
