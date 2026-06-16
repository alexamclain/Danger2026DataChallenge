# P25 KSY-y H0 Koo-Shin Source-Clause Matrix

Updated: 2026-06-14 16:22 PDT

## Purpose

This packet applies the H0 source-theorem matcher to the actual Koo-Shin 2010
Math. Z. text.  It records which source clauses are present, what they are good
for, and why none of them currently closes the H0 source stage.

## Source

```text
text = /Users/agent/Documents/Codex/pomerance-p25-run/incoming/extracted/s00209-008-0456-9.pdf.extract.txt
```

Small p25 branch arithmetic:

```text
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

## Clause Matrix

```text
theorem3_9_orbit_integrality_hygiene:
  surface  = Koo-Shin 2010 Theorem 3.9
  decision = context_only_not_h0_source_candidate
  missing  = exact H0 product value/divisor theorem

theorem5_2_prime_level_root_descent:
  surface  = Koo-Shin 2010 Theorem 5.2
  decision = context_only_not_h0_source_candidate
  missing  = mixed-level H0 lift preserving C3 row graph and T edge

theorem6_2_exact_h0_source_legality:
  surface  = Koo-Shin 2010 Theorem 6.2 plus exact H0 translate screen
  decision = source_certified_value_or_divisor_missing
  missing  = finite-field value/divisor theorem for one exact H0 product

theorem6_2_as_h0_value_closer_control:
  surface  = Koo-Shin 2010 Theorem 6.2 misread as value/divisor theorem
  decision = source_certified_value_or_divisor_missing
  missing  = finite-field value/divisor theorem for one exact H0 product

section7_ramanujan_value_evaluation:
  surface  = Koo-Shin 2010 Section 7 / Corollary 7.3
  decision = context_only_not_h0_source_candidate
  missing  = one of the four exact legal H0 products

theorem9_8_ray_class_sum_generator:
  surface  = Koo-Shin 2010 Theorem 9.8
  decision = context_only_not_h0_source_candidate
  missing  = exact H0 finite value/divisor identity

theorem9_10_ray_class_product_generator:
  surface  = Koo-Shin 2010 Theorem 9.10
  decision = context_only_not_h0_source_candidate
  missing  = exact H0 finite value/divisor identity

theorem9_11_prime_ray_class_generator:
  surface  = Koo-Shin 2010 Theorem 9.11
  decision = context_only_not_h0_source_candidate
  missing  = mixed H0 product at conductor 39/507, not prime-only generator
```

## Counts

```text
row_count                     = 8
present_rows                  = 8
h0_candidate_rows             = 2
source_closing_rows           = 0
source_certified_only_rows    = 2
context_only_rows             = 6
rejected_as_closer_rows       = 8
value_or_divisor_missing_rows = 5
```

## Meaning

Koo-Shin 2010 remains valuable prior art, especially Theorem 6.2 as H0 source
legality and Theorem 5.2 as root-descent/constant-rigidity context.  But the
current paper clauses do not supply the missing source closer:

```text
period-156 finite value identity for one exact H0 product
or
exact divisor/additive identity for one exact H0 product with H90 boundary
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_koo_shin_source_clause_matrix_gate.py
```

Marker:

```text
ksy_y_h0_koo_shin_source_clause_matrix_rows=1/1
```
