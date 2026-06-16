# P25 KSY-y H0 Translate Post-Koo-Shin-6.2 Upgrade Router

Updated: 2026-06-14 15:30 PDT

## Purpose

Koo-Shin 2010 Theorem 6.2 is now a positive source-certification result for
the active H0 lane: all four exact legal H0 products pass the conductor-39
congruence screen.  This note records what that does and does not buy.

## Router

```text
post-6.2 certified fact:
  all four exact 78-over-78 H0 products are legal source words

still not certified by 6.2:
  finite-field value identity
  divisor/additive identity
  DANGER3-compatible non-CM/framing decision
  X_1(8112) / X_1(16) extraction
  official vpp.py verification
```

Rows:

```text
1. Koo-Shin 6.2 product legality for exact H0 rows
   decision = source_certified_value_or_divisor_missing
   use      = keep; this is the certified source object
   missing  = finite-field value/divisor theorem for one exact H0 product

2. Koo-Shin 5.2 prime-level root descent
   decision = reject_prime_power_only_missing_mixed_lift
   use      = context for root descent and constant-product rigidity
   missing  = mixed-level lift preserving C_3 row graph and T edge

3. Koo-Shin 3.9 orbit-sum hygiene
   decision = context_only_integrality_hygiene_not_exact_selector
   use      = hygiene/integrality screen
   missing  = exact mixed selector/product producer

4. Koo-Shin 9.x ray-class generator context
   decision = context_only_ray_class_generator_not_mixed_u_chi_value_theorem
   use      = vocabulary/context
   missing  = independent mixed-character finite-field value/divisor theorem

5. H0 value with period-156 context
   decision = source_theorem_closed_policy_or_framing_missing
   use      = source-stage closer
   missing  = DANGER3 finite-identity/non-CM framing

6. H0 divisor/additive identity
   decision = source_theorem_closed_policy_or_framing_missing
   use      = source-stage closer
   missing  = DANGER3 finite-identity/non-CM framing

7. Finite payload without source theorem
   decision = conditional_finite_payload_without_source_theorem
   use      = verifier data only
   missing  = challenge-legal arithmetic source theorem

8. Formal or nonlegal H
   decision = reject_before_source_or_x1_routing
   use      = discard
   missing  = remap to one of the four exact legal products
```

## Counts

```text
row_count                  = 8
context_only_rows          = 3
source_certified_only_rows = 1
source_closing_rows        = 2
conditional_rows           = 1
rejected_rows              = 1
danger3_unblocked_rows     = 0
extraction_ready_rows      = 0
submission_ready_rows      = 0
continue_rows              = 4
kill_rows                  = 1
```

## Interpretation

The H0 lane has become sharper, not solved.  Koo-Shin 6.2 removes a legality
ambiguity for the exact sparse products, but it does not evaluate them.  The
only source-closing asks remain:

```text
exact finite-field value identity for one legal H0 product with period-156 context
exact divisor/additive identity for one legal H0 product with the Hilbert-90 boundary
```

Everything else is context, verifier-only evidence, or a reject.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_post_koo_shin62_upgrade_router_gate.py
```

Marker:

```text
ksy_y_h0_translate_post_koo_shin62_upgrade_router_rows=1/1
```
