# P25 KSY-y Priority-1 Theorem Query Packet

Updated: 2026-06-13 21:42 PDT

## Purpose

The priority-1 Sprang and KSY source splits are now precise enough to drive a
source pass by snippet contracts instead of broad reading.  This packet lists
the exact theorem questions, the first falsifier, and the local probe that
should classify any claimed hit.

Target:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Closing Queries

```text
Sprang arXiv:1801.05677:
  question = Is there a Kronecker-section, distribution, or
             Eisenstein-Kronecker clause that specializes at D=2 to exact P
             or theta2/theta2^-1 divisor data?
  falsifier = vocabulary without exact C/D/K product specialization

Sprang arXiv:1802.04996:
  question = Is there an algebraic de Rham polylogarithm or Eisenstein-class
             differential-form clause whose D=2 specialization emits exact P
             or theta2/theta2^-1 divisor data?
  falsifier = cohomology representative without exact anti-invariant
              normalized-y product output

KSY arXiv:1007.2307 Equation (3.4):
  question = Does y(Q)=-g(2Q)/g(Q)^4 come with a distribution/product theorem
             selecting all 75 p25 atoms in P?
  falsifier = formula language, one y-value, or broad class-field generation
              without exact P
```

Each closing query must route to:

```text
closing_exact_product_identity
```

## Non-Closing Rows

```text
KSY Theorem 5.3 ray-class generation:
  expected probe decision = reject_field_generation_not_product_identity
  recommendation = kill as direct closer

KSY Theorem 6.2 / Corollary 6.4 single-y invariant:
  expected probe decision = conditional_missing_exact_product
  recommendation = keep only as context until exact P and mixed graph appear
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_theorem_query_packet_gate.py
```

## Completed Gate

```text
source_query_rows    = 5
closing_query_rows   = 3
context_only_rows    = 1
rejected_shadow_rows = 1
all_rows_have_probe  = 1
```

Marker:

```text
ksy_y_priority1_theorem_query_packet_rows=1/1
```

## Primary-Source Verdict Follow-Up

The first direct TeX source pass is recorded in:

```text
research/p25/p25_ksy_y_priority1_primary_source_verdict_20260613.md
```

Its gate reports:

```text
ksy_y_priority1_primary_source_verdict_rows=1/1
direct_closing_rows=0
```

Interpretation: Sprang `1801.05677` and `1802.04996` provide real additive
Kronecker/de Rham distribution machinery, and KSY `1007.2307` provides the
normalized-y atom formula plus field-generation context.  None of those
inspected blocks directly supplies the exact p25 K-traced product `P`; continue
only on an external exact product/distribution specialization or a new theorem
snippet that passes the exact-product intake.
