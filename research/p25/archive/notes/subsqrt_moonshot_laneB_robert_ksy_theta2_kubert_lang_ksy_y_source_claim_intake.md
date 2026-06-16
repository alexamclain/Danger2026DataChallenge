# P25 Lane B: KSY-y Source-Claim Intake

Updated: 2026-06-13 19:40 PDT

## Purpose

Use this gate when a literature scout, theorem snippet, or DANGER3 policy
answer arrives.  It classifies the claim against the closure-template route.

## Closing Claims

```text
exact divisor/additive identity for P:
  closes route

exact finite-field value identity for P with period-156 context:
  closes route
```

## Non-Closing Claims

```text
exact finite-field value identity for P without period-156 context:
  conditional, missing branch/root/telescoping

DANGER3 says finite-field identity for P is challenge-legal:
  policy unblocked, but still not a theorem

generic field generation:
  rejected as not a closure theorem

Kubert-Lang exponent hygiene alone:
  rejected without mixed C_75 x C_169 graph selector

unnamed relevant source:
  rejected until mapped to a known anchor row
```

## Candidate Mode

Closing divisor/additive example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate \
  --name closing_demo \
  --anchor ksy_normalized_y_siegel_formula \
  --output-kind divisor-additive \
  --exact-product \
  --mixed-graph \
  --divisor-additive
```

Non-closing exact value example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate \
  --name missing_period_demo \
  --anchor siegel_robert_value_units \
  --output-kind value \
  --exact-product \
  --mixed-graph \
  --finite-field-identity
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py
```

Expected markers:

```text
robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_candidate_rows=1/1
```

## Interpretation

The intake rule is now executable: a claim must name a known anchor, supply the
exact product and mixed graph, and either be divisor/additive or provide a
finite-field value with period-156 context.  Policy help is useful but does not
replace the theorem.
