# P25 KSY-y Source-Family Front-Door Router

Updated: 2026-06-14 22:25 PDT

## Purpose

This checkpoint maps the real source families in play onto the priority-1
source-theorem intake.  It is meant to keep the next literature/expert pass
from drifting back into broad source rereads.

The current distinction is:

```text
known source evidence
  != source-closing theorem

hypothetical exact front-door theorem
  = useful only if it hits one of the rows below
```

## Current Evidence

```text
inspected Sprang/KSY primary sources:
  decision = current_sources_missing_exact_product_specialization
  missing  = exact finite p25 product P with mixed graph, equal weights, and orientation
  action   = do not reread broad clauses; search only for an exact specialization

Koo-Shin 2010 Theorem 6.2:
  decision = source_certified_value_or_divisor_missing
  missing  = finite-field value/divisor theorem for one exact H0 product
  action   = ask only value-period156 or divisor/additive upgrade questions
```

Current source-theorem rows remain zero.

## Positive Front Doors

These are the exact theorem shapes that would close source stage, pending
DANGER3 framing and extraction:

```text
h0_exact_divisor_boundary_theorem:
  source family = H0 / Yang / Kubert-Lang
  front door    = exact H0 divisor/additive identity with H90 boundary
  decision      = source_theorem_closed_policy_or_framing_missing

conductor39_mixed_divisor_theorem:
  source family = mixed conductor-39 unit / Yang distribution
  front door    = U_chi/W divisor or additive identity
  decision      = source_theorem_closed_policy_or_framing_missing

twisted_h90_divisor_theorem:
  source family = twisted ratio / Hilbert-90
  front door    = twisted/H90 divisor identity with period-156 bridge context
  decision      = source_theorem_closed_policy_or_framing_missing

curved_corner_divisor_theorem:
  source family = unit-triangle curved K-traced corner
  front door    = curved-corner divisor identity with period-156 context
  decision      = source_theorem_closed_policy_or_framing_missing

exact_75_atom_product_divisor_theorem:
  source family = Kubert-Lang / KSY normalized-y
  front door    = exact 75-atom P divisor/additive theorem
  decision      = source_theorem_closed_policy_or_framing_missing
```

The H0, conductor-`39`, curved-corner, and exact-75 divisor rows avoid the
finite-value branch.  The twisted/H90 and curved-corner divisor rows still
carry period-`156` context requirements because those routers currently require
that support-period bridge.

## Conditional Or Kill

```text
exact_75_atom_value_no_period:
  decision = conditional_value_missing_period_156
  missing  = period-156 fixedness/telescoping for value output

generic_modular_unit_or_cm_generation:
  decision = reject_not_exact_p
  missing  = exact P over C=(47,28), D=(22,3), K=(57,0)

finite_payload_without_source:
  decision = conditional_finite_payload_without_source_theorem
  missing  = challenge-legal arithmetic source theorem

prime_projection_or_axis_shadow:
  decision = reject_loses_mixed_tensor
  missing  = mixed chi_3 tensor chi_13 source on X_1(39)
```

## Counts

```text
row_count                       = 11
current_evidence_rows           = 2
source_closing_shape_rows       = 5
current_source_theorem_rows     = 0
priority1_rows                  = 5
avoids_value_branch_rows        = 5
needs_period156_context_rows    = 3
continue_external_search_rows   = 9
kill_as_direct_closer_rows      = 3
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_source_frontdoor_router_gate.py
```

Marker:

```text
ksy_y_source_frontdoor_router_rows=1/1
```
