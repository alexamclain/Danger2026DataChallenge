# P25 KSY-y: Koo-Shin 2010 Theorem 5.2 Actual Verdict

Updated: 2026-06-14 07:58 PDT

## Input

User supplied the exact Koo-Shin 2010 Springer/KOASAS PDF:

```text
/Users/agent/Downloads/s00209-008-0456-9.pdf
bytes = 501978
md5   = 39bf3ab80a349709394165f27f0eafbf
```

The scanner accepts it as the expected 2010 Math. Z. paper and extracts
Theorem 5.2:

```text
intake_verdict       = accept_exact_koasas_pdf
exact_koasas_match   = 1
theorem_ready        = 1
first_theorem_5_2_page = 16
```

## Theorem 5.2 Payload

The actual theorem is a prime-level Siegel-product result:

- constant-product rigidity for products indexed by
  `(1/p Z^2/Z^2)^*/+/-`;
- an `l`-th-root descent statement for such prime-level products.

This is genuine useful structure, but it does **not** emit the p25 payload:

- no exact p25 product `P`;
- no mixed `C_3 x C_169` row graph;
- no `T=(2,113)` edge or orientation branch;
- no normalized-y product over `base*K_trace*D_segment`.

## Intake Result

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_theorem_clause_intake_gate.py \
  --candidate --name koo_shin_2010_theorem_5_2_actual \
  --theorem-body --product-distribution --prime-power-only
```

```text
decision                = reject_prime_power_only_missing_mixed_lift
exact_product_decision  = conditional_missing_exact_product
first_missing_clause    = mixed-level lift preserving C_3 row graph and T edge
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_2010_theorem52_actual_verdict_gate.py
```

Marker:

```text
ksy_y_koo_shin_2010_theorem52_actual_verdict_rows=1/1
```

## Verdict

Kill Koo-Shin 2010 Theorem 5.2 as a direct p25 closer.  Keep it as
root-descent and constant-product rigidity context for a future mixed-level
KSY/Kubert-Lang theorem hit.
