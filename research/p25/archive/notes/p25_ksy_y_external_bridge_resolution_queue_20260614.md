# P25 KSY-y External Bridge Resolution Queue

Updated: 2026-06-14 22:43 PDT

## Purpose

This queue separates two things that were getting too easy to blend together:

```text
old external source hits       = resolved or context-only
current live external targets  = five front-door source families, each followed by policy and same-j X_1(8112)
```

The old Koo-Shin/Bannai/Scholl actions are not active retrieval tasks anymore.
The live queue is now H0, conductor-39, twisted/H90, curved-corner, and
exact-P.

## Resolved Context Rows

```text
koo_shin_2010_pdf_candidate_resolved:
  status    = pdf retrieved; Theorem 5.2 rejects as prime_power_only_missing_mixed_lift
  use       = root-descent / constant-product context only
  upgrade   = mixed-level theorem preserving the C3 row graph and T=(2,113) edge
  falsifier = prime-level or C169 projection product without the mixed lift

bannai_kobayashi_distribution_ancestor:
  status    = verified additive theta distribution, not product bridge
  use       = Sprang ancestor/context only
  upgrade   = specialization to the exact K-traced normalized-y product P
  falsifier = additive Kronecker theta distribution without finite multiplicative P

scholl_kato_siegel_odd_d_control:
  status    = multiplicative distribution but D=2 ineligible
  use       = odd-D control/context only
  upgrade   = even-D or normalized-y theorem avoiding the (6,D)=1 obstruction
  falsifier = odd-D Kato-Siegel norm relation imported directly into D=2
```

## Active Front Doors

```text
active_h0_divisor_boundary_identity:
  odd target = canonical_H0/H0_translate/Y_507
  positive   = exact legal H0 divisor/additive identity with Hilbert-90 boundary to Norm_156(Y_507)
  bridge ask = same-j X_1(8112) bridge tying the H0/Y_507 odd target to production X_1(16)
  falsifier  = H0 theorem missing the Hilbert-90 boundary, or projection-only data

active_conductor39_divisor_identity:
  odd target = conductor39_U_chi
  positive   = exact U_chi/W divisor/additive theorem preserving chi_3 tensor chi_13, Yang lift, and descent
  bridge ask = same-j X_1(8112) bridge for conductor39_U_chi and production X_1(16)
  falsifier  = prime projection, axis-only statement, or source certification without finite theorem

active_twisted_h90_divisor_identity:
  odd target = U_507/Y_507
  positive   = finite divisor/additive theorem for the twisted ratio/Hilbert-90 object with period-156 context
  bridge ask = same-j X_1(8112) bridge for twisted U_507/Y_507 and production X_1(16)
  falsifier  = H90 vocabulary without finite theorem and period-156 bridge context

active_curved_corner_divisor_identity:
  odd target = curved_corner
  positive   = finite divisor/additive theorem for the unit-triangle curved K-traced corner with period-156 context
  bridge ask = same-j X_1(8112) bridge for curved_corner and production X_1(16)
  falsifier  = curved helper only, wrong unit triangle, or theorem without period-156 context

active_exact75_product_divisor_theorem:
  odd target = exact_P
  positive   = exact P divisor/additive theorem with mixed C3 x C169 graph, all 75 equal atoms, and orientation
  bridge ask = same-j X_1(8112) bridge for exact_P and production X_1(16)
  falsifier  = field generation, one y-value, subset/nonuniform atom product, or missing orientation
```

## Counts

```text
row_count                         = 8
resolved_source_rows              = 3
killed_direct_rows                = 3
context_only_rows                 = 3
active_frontdoor_rows             = 5
active_post_policy_bridge_rows    = 5
exact75_rows                      = 1
curved_corner_rows                = 1
stale_access_blocked_rows         = 0
direct_closing_rows               = 0
```

## Dependencies

```text
ksy_y_external_frontdoor_answer_router_rows=1/1
ksy_y_external_post_policy_x18112_work_order_rows=1/1
ksy_y_x1_8112_bridge_theorem_intake_rows=1/1
ksy_y_koo_shin_2010_theorem52_actual_verdict_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_bridge_resolution_queue_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_external_bridge_resolution_queue_gate.py
```

Marker:

```text
ksy_y_external_bridge_resolution_queue_rows=1/1
```

## Interpretation

The next external/literature/expert pass should not reopen broad retrieval or
the old exact-product-only target.  It should ask whether one of the five live
front doors has an exact p25 source theorem.  A yes answer still routes through
DANGER3 finite-identity policy/framing, then same-j `X_1(8112)`, then the
production `X_1(16)` payload, halving, and official `vpp.py`.
