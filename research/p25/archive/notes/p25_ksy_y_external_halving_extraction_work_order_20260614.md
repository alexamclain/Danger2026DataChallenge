# P25 KSY-y External Halving / Direct-x0 Extraction Work Order

Updated: 2026-06-14 22:59 PDT

## Purpose

This work order starts after one of the external front doors has reached the
active production `X_1(16)` surface (`A,xP16`).  For each of the ten surface
variants from the specialization work order, it records the three accepted
extraction payload shapes:

```text
x_coordinate_chain:
  A,xP16 plus x_4=xP16 through x_42=x0 with checkable xDBL links

sqrt_witness_chain:
  A,xP16 plus square-root witnesses and active branch provenance to x0

direct_A_x0:
  direct concrete A,x0 payload
```

All three require official `vpp.py` verification before submission.

## Counts

```text
row_count                         = 30
source_surface_rows               = 10
frontdoor_count                   = 5
x_coordinate_chain_rows           = 10
sqrt_witness_chain_rows           = 10
direct_A_x0_rows                  = 10
active_branch_provenance_rows     = 10
extraction_ready_rows             = 30
requires_official_vpp_rows        = 30
exact75_rows                      = 6
curved_corner_rows                = 6
current_evidence_rows             = 0
current_submission_ready_rows     = 0
```

## Dependencies

```text
ksy_y_external_x16_specialization_work_order_rows=1/1
ksy_y_x1_16_halving_certificate_payload_rows=1/1
ksy_y_post_surface_halving_vpp_intake_rows=1/1
ksy_y_official_vpp_submission_archive_contract_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_halving_extraction_work_order_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_external_halving_extraction_work_order_gate.py
```

Marker:

```text
ksy_y_external_halving_extraction_work_order_rows=1/1
```

## Interpretation

The external moonshot ladder now reaches the final pre-verifier payload
boundary without changing the practical production run.  A same-`j` bridge plus
production `A,xP16` still is not enough: the route must provide either a
checkable 39-point x-chain, active-path square-root witnesses, or direct
`A,x0`, and then official `vpp.py` plus the archive contract must close.
