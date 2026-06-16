# P25 KSY-y External Source-Theorem Obligation Matrix

Updated: 2026-06-14 23:06 PDT

## Purpose

The external end-to-end audit made the first missing item explicit: a real
source-stage theorem.  This matrix turns the five live front doors into exact
theorem obligations and a conservative search order.

## First-Pass Targets

```text
H0/Yang/Kubert-Lang:
  odd target = canonical_H0/H0_translate/Y_507
  need       = one exact legal 78-over-78 H0/H0-translate product,
               finite divisor/additive identity,
               Hilbert-90 boundary to Norm_156(Y_507),
               arithmetic source theorem
  falsifier  = source legality only, value without period-156 context,
               or missing H90 boundary

mixed conductor-39:
  odd target = conductor39_U_chi
  need       = U_chi/W mixed conductor-39 object,
               chi_3 tensor chi_13 non-projection structure,
               Yang lift to level-507 period norm,
               Hilbert-90 or ratio descent,
               finite divisor/additive identity
  falsifier  = prime projection, axis-only statement, or source certification
               without finite theorem
```

These two are first-pass because their source objects are already certified and
the preferred divisor/additive theorem avoids the period-156 value branch.

## Other Live Targets

```text
exact-P:
  odd target = exact_P
  status     = high-payoff but heavier
  need       = exact P, mixed C_3 x C_169 graph, all 75 equal atoms,
               orientation branch, finite divisor/additive source theorem

twisted/H90:
  odd target = U_507/Y_507
  status     = live with period-156 context
  need       = twisted ratio or Hilbert-90 theorem plus period-156 context

curved-corner:
  odd target = curved_corner
  status     = live with period-156 context
  need       = exact unit-triangle curved K-traced corner theorem plus
               period-156 context
```

## Counts

```text
row_count                         = 5
source_object_certified_rows      = 3
exact_object_named_rows           = 5
divisor_additive_preferred_rows   = 5
needs_period156_context_rows      = 2
local_source_direct_hit_rows      = 0
current_source_theorem_rows       = 0
source_stage_closes_if_yes_rows   = 5
downstream_route_ready_rows       = 5
selected_first_pass_rows          = 2
high_payoff_heavy_rows            = 1
total_required_clause_count       = 22
```

## Dependencies

```text
ksy_y_external_end_to_end_route_audit_rows=1/1
ksy_y_external_bridge_resolution_queue_rows=1/1
ksy_y_source_frontdoor_router_rows=1/1
ksy_y_source_theorem_priority_selector_rows=1/1
ksy_y_external_frontdoor_query_packet_rows=1/1
ksy_y_frontdoor_local_source_scan_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_source_theorem_obligation_matrix_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_external_source_theorem_obligation_matrix_gate.py
```

Marker:

```text
ksy_y_external_source_theorem_obligation_matrix_rows=1/1
```

## Interpretation

The next real mathematical work should first try to close H0 or conductor-39
with a divisor/additive theorem.  Exact-P remains the moonshot prize, but the
certified H0/conductor-39 source objects are cheaper first-pass routes into the
same downstream DANGER3 ladder.
