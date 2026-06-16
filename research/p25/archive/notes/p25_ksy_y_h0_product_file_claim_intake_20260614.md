# P25 KSY-y: H0 Product-File Claim Intake

Updated: 2026-06-14 17:37 PDT

## Purpose

The H0 exact-product fixtures are now usable as an intake surface.  A future
paper snippet, expert answer, or subagent report can supply a two-column
level-`507` product file:

```text
residue coefficient
```

and this gate identifies whether the file is canonically one of the four exact
legal H0 targets.  It then routes the claimed theorem shape through the H0
source-theorem matcher.

The gate records raw SHA-256 fixture equality, but routes by canonical product
content, so harmless line-order changes do not hide a true match.

## Accepted Product Files

```text
research/p25/h0_product_fixtures/h0_m1_canonical_lifted_product.txt
research/p25/h0_product_fixtures/h0_m2_translate_lifted_product.txt
research/p25/h0_product_fixtures/h0_m4_translate_lifted_product.txt
research/p25/h0_product_fixtures/h0_m8_translate_lifted_product.txt
```

Each exact file has:

```text
lines     = 156
support   = 156
coeffs    = (-6,78), (6,78)
match     = 1
raw_hash  = 1
```

## Classifier Rows

```text
source certification only:
  source_certified_value_or_divisor_missing

value theorem with period-156 context:
  source_theorem_closed_policy_or_framing_missing

divisor/additive theorem with H90 boundary:
  source_theorem_closed_policy_or_framing_missing

bare value without period-156:
  conditional_missing_period_156_context

divisor/additive theorem without H90 boundary:
  conditional_divisor_identity_missing_h90_boundary

fixture match without arithmetic source theorem:
  conditional_finite_payload_without_source_theorem

fixture match without theorem body:
  reject_no_theorem_body

wrong product file:
  reject_product_file_not_exact_h0_fixture

non-product file:
  reject_unparseable_product_file
```

## CLI Examples

Classify an exact period-`156` value theorem claim for the `m=2` translate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_product_file_claim_intake_gate.py \
  --product-file research/p25/h0_product_fixtures/h0_m2_translate_lifted_product.txt \
  --theorem-body --source-theorem --output-kind value --period-156
```

Expected decision:

```text
source_theorem_closed_policy_or_framing_missing
```

Classify an exact divisor/additive theorem claim for the `m=4` translate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_product_file_claim_intake_gate.py \
  --product-file research/p25/h0_product_fixtures/h0_m4_translate_lifted_product.txt \
  --theorem-body --source-theorem --output-kind divisor-additive --h90-boundary
```

Expected decision:

```text
source_theorem_closed_policy_or_framing_missing
```

## Regression Counts

```text
row_count             = 10
parsed_rows           = 9
exact_product_rows    = 8
raw_hash_match_rows   = 8
source_closing_rows   = 3
conditional_rows      = 3
rejected_rows         = 3
submission_ready_rows = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_product_file_claim_intake_gate.py
```

Marker:

```text
ksy_y_h0_product_file_claim_intake_rows=1/1
```
