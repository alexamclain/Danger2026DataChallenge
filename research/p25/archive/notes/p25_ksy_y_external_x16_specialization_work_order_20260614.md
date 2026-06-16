# P25 KSY-y External X1(16) Specialization Work Order

Updated: 2026-06-14 22:55 PDT

## Purpose

This work order starts after a positive same-`j` `X_1(8112)` bridge answer
from one of the five live external front doors.  It makes the next accepted
payload explicit for the production search:

```text
accepted shape A = X_1(16) y + model root x, hence Montgomery A and xP16
accepted shape B = direct Montgomery A and xP16
```

Both accepted shapes route to the active `x16halvenonsplit` surface at depth
`4`; neither is a DANGER3 submission until the halving/direct-`x0` and official
`vpp.py` stages close.

## Front Doors

```text
H0/Yang/Kubert-Lang:
  odd target = canonical_H0
  variants   = y_model_root, direct_A_xP16

conductor-39/Yang distribution:
  odd target = conductor39_U_chi
  variants   = y_model_root, direct_A_xP16

twisted/Hilbert-90:
  odd target = U_507
  variants   = y_model_root, direct_A_xP16

curved-corner:
  odd target = curved_corner
  variants   = y_model_root, direct_A_xP16

exact-P:
  odd target = exact_P
  variants   = y_model_root, direct_A_xP16
```

## Counts

```text
row_count                     = 10
frontdoor_count               = 5
y_model_root_rows             = 5
direct_A_xP16_rows            = 5
active_surface_rows           = 10
continue_to_halving_rows      = 10
exact75_rows                  = 2
curved_corner_rows            = 2
optional_dgate_required_rows  = 0
current_evidence_rows         = 0
current_submission_ready_rows = 0
```

## Dependencies

```text
ksy_y_external_x18112_bridge_answer_router_rows=1/1
ksy_y_post_bridge_x16_surface_intake_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
ksy_y_x1_16_halving_chain_contract_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_x16_specialization_work_order_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_external_x16_specialization_work_order_gate.py
```

Marker:

```text
ksy_y_external_x16_specialization_work_order_rows=1/1
```

## Interpretation

The next external ask is now precise.  Once an expert/literature answer supplies
a same-`j` bridge, the useful payload is not generic `X_1(16)` data and not an
abstract `P16`; it must specialize to the production Montgomery chart used by
`x16halvenonsplit`.  The optional first-half d-gate remains useful extra data,
but it is not required for the active production mode.
