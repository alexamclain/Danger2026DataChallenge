# P25 Lane B: KSY-y Exact-Product Intake

Updated: 2026-06-13 19:55 PDT

## Purpose

Classify source or theorem claims aimed at the divisor/additive route.  This is
the stronger route than value output: a theorem that emits the exact KSY-y
product identity can feed the existing theta2 certificate path without the
ambient value-root ambiguity.

## Product Contract

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28)
D = (22,3)
K = (57,0), primitive
atoms = 75
theta2 footprint = 300 terms
orientation = theta2 or theta2 inverse branch must be recorded
```

## Regression Counts

```text
closing product claims     = 3
conditional product claims = 3
rejected product claims    = 4
```

Closing shapes:

```text
KSY exact divisor/additive identity for P
Sprang/Kronecker D=2 exact additive identity for P
Kubert-Lang exact mixed product identity for P
```

Conditional shapes:

```text
KSY formula language without product proof
finite theta2 verifier payload without source theorem
exact product with DANGER3 policy/framing still unknown
```

Rejected shadows:

```text
generic KSY ray-class generation
literal Robert subgroup support
Kubert-Lang exponent hygiene alone
nonuniform weighted product variants
```

## Candidate Mode

Closing example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py \
  --candidate \
  --name closing_product_demo \
  --anchor ksy_normalized_y_siegel_formula \
  --output-kind divisor-additive \
  --exact-product \
  --mixed-graph \
  --equal-weight \
  --orientation \
  --arithmetic-producer \
  --challenge-legal \
  --finite-intake
```

Non-closing verifier-only example:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py \
  --candidate \
  --name verifier_only_demo \
  --anchor ksy_normalized_y_siegel_formula \
  --output-kind finite-verifier \
  --exact-product \
  --mixed-graph \
  --equal-weight \
  --orientation \
  --challenge-legal \
  --finite-intake
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py
```

Expected markers:

```text
robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_candidate_rows=1/1
```

## Interpretation

The exact-product route is narrowly viable: the finite certificate side is
ready, but source relevance is not enough.  A hit must supply exact `P`, the
mixed graph, equal weights, orientation, finite intake geometry, arithmetic
producer status, and DANGER3-legal framing.
