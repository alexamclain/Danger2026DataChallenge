# P25 KSY-y External Front-Door Query Packet

Updated: 2026-06-14 22:25 PDT

## Purpose

This packet turns the external source scout into exact questions for an expert
or targeted literature pass.  It extends the priority-1 query packet by adding
the exact 75-atom product as a first-class front door.

Every useful answer must be an exact p25 specialization.

## Closing Questions

```text
ask_h0_divisor_boundary_identity:
  question = Does the source prove an exact divisor/additive identity for one
             of the four legal 78-over-78 H0 products, with the Hilbert-90
             boundary to Norm_156(Y_507)?
  accept   = exact legal H0 product + divisor/additive identity + H90 boundary
  decision = source_theorem_closed_policy_or_framing_missing

ask_conductor39_divisor_identity:
  question = Does the source prove an exact divisor/additive identity for the
             legal mixed conductor-39 source U_chi/W, preserving the chi_3
             tensor chi_13 object, Yang lift, and descent?
  accept   = U_chi/W + mixed tensor + Yang lift + H90/ratio descent + divisor/additive theorem
  decision = source_theorem_closed_policy_or_framing_missing

ask_twisted_h90_divisor_identity:
  question = Does the source prove a finite divisor/additive theorem for the
             twisted ratio/Hilbert-90 object, with the period-156 bridge
             context required by the current router?
  accept   = twisted ratio/H90 object + finite divisor theorem + arithmetic source + period-156 bridge context
  decision = source_theorem_closed_policy_or_framing_missing

ask_curved_corner_divisor_identity:
  question = Does the source prove a finite divisor/additive theorem for the
             exact unit-triangle curved K-traced corner, with period-156 context?
  accept   = unit-triangle curved corner + finite divisor theorem + arithmetic source + period-156 context
  decision = source_theorem_closed_policy_or_framing_missing

ask_exact_75_atom_product_divisor_theorem:
  question = Does the source prove an exact divisor/additive theorem for
             P = prod_{j=-1..1,k=0..24} y(C+jD+kK)/y(-C-jD-kK),
             with the mixed C3 x C169 graph, equal atom weights, and orientation?
  accept   = exact P + mixed graph + 75 equal K-traced atoms + orientation + arithmetic source theorem
  decision = source_theorem_closed_policy_or_framing_missing
```

## Falsifiers

```text
falsify_h0_boundary_missing:
  decision = conditional_divisor_identity_missing_h90_boundary
  falsifier = Hilbert-90 boundary to Norm_156(Y_507) is missing

falsify_projection_or_axis_only:
  decision = reject_loses_mixed_tensor
  falsifier = mixed chi_3 tensor chi_13 source on X_1(39) is missing

falsify_twisted_missing_period_bridge:
  decision = conditional_value_theorem_missing_period156_context
  falsifier = period-156 branch/root/telescoping context is missing

falsify_curved_missing_period_context:
  decision = conditional_missing_period156_context
  falsifier = period-156 branch/root/telescoping context is missing

falsify_exact_75_value_without_period156:
  decision = conditional_value_missing_period_156
  falsifier = period-156 fixedness/telescoping for value output is missing
```

## Counts

```text
row_count                    = 10
closing_query_rows           = 5
falsifier_rows               = 5
current_source_theorem_rows  = 0
priority1_rows               = 8
exact75_rows                 = 2
fixture_backed_rows          = 8
exact_p25_required_rows      = 10
```

## Local Commands

Four front doors use the priority-1 JSON fixtures:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json research/p25/priority1_divisor_additive_packet_fixtures/h0_divisor_close.json

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json research/p25/priority1_divisor_additive_packet_fixtures/conductor39_divisor_close.json

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json research/p25/priority1_divisor_additive_packet_fixtures/twisted_divisor_close.json

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json research/p25/priority1_divisor_additive_packet_fixtures/curved_corner_divisor_close.json
```

The exact-75 front door uses the closing-theorem obligation classifier:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name exact_75_atom_product_divisor_theorem \
  --source-family Kubert-Lang-KSY-exact-P \
  --output-kind divisor-additive --exact-p --mixed-graph --equal-weight \
  --orientation --arithmetic-source --finite-identity
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_frontdoor_query_packet_gate.py
```

Marker:

```text
ksy_y_external_frontdoor_query_packet_rows=1/1
```
