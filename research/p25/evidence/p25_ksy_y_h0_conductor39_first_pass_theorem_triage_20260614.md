# P25 KSY-y H0 / Conductor-39 First-Pass Theorem Triage

Updated: 2026-06-14 23:10 PDT

## Purpose

This is the immediate triage surface for the two first-pass source-theorem
targets selected by the external obligation matrix: H0 and conductor-39.  It
routes an incoming theorem snippet into the existing H0 product-file classifier
or conductor-39 source-theorem classifier and separates:

```text
source certification only
value theorem missing period-156 context
H0 divisor theorem missing Hilbert-90 boundary
projection shortcut kill
divisor/additive source-stage yes
```

## Positive First-Pass Targets

```text
h0_divisor_additive_source_yes:
  accepted = exact legal H0 product file + theorem body + arithmetic source
             + divisor/additive output + Hilbert-90 boundary
  decision = source_theorem_closed_policy_or_framing_missing

conductor39_divisor_additive_source_yes:
  accepted = U_chi/W mixed conductor-39 object + Yang lift + descent
             + finite divisor/additive theorem
  decision = source_theorem_closed_policy_or_framing_missing
```

Both positives deliberately stop at source-stage closure.  They still route to
DANGER3 policy/framing, same-`j` `X_1(8112)`, `X_1(16)`, halving/direct `x0`,
official `vpp.py`, and archive.

## Counts

```text
row_count                         = 8
h0_rows                           = 4
conductor39_rows                  = 4
candidate_command_rows            = 8
source_stage_closing_rows         = 2
source_certified_only_rows        = 2
period156_repair_rows             = 2
boundary_repair_rows              = 1
kill_route_rows                   = 1
selected_positive_target_rows     = 2
avoids_period_value_branch_rows   = 2
current_source_theorem_rows       = 0
```

## Dependencies

```text
ksy_y_external_source_theorem_obligation_matrix_rows=1/1
ksy_y_h0_product_file_claim_intake_rows=1/1
ksy_y_conductor39_source_theorem_intake_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_gate.py
```

Marker:

```text
ksy_y_h0_conductor39_first_pass_theorem_triage_rows=1/1
```

## Interpretation

The next theorem-search action is now narrow: search or ask for either an H0
divisor/additive theorem with the Hilbert-90 boundary, or a conductor-39
`U_chi/W` divisor/additive theorem preserving the mixed tensor, Yang lift, and
descent.  Bare source certification and value-only snippets remain repair rows,
not wins.
