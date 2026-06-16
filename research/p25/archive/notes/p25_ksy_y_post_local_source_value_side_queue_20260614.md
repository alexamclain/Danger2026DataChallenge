# P25 KSY-y Post-Local-Source Value-Side Queue

Updated: 2026-06-14 08:40 PDT

## Purpose

The post-local-source exact-product queue covers the local KSY, Kubert-Lang,
Sprang, and Koo-Shin source families.  The adjacent Schertz/Shin
Siegel-Robert value-unit route needs its own compact boundary so it does not
collapse back into broad class-field-generation reading.

This queue keeps only one value-side moonshot target alive:

```text
exact finite-field value identity for P,
preserving the mixed C_3 x C_169 graph,
with period-156 branch/root/telescoping context
```

## Source Boundaries

```text
Schertz/Shin class-field generator boundary
boundary = p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md
status   = elliptic-unit / Siegel-Ramachandra generator language
decision = reject_field_generation_not_value_theorem
upgrade  = exact finite-field value identity for P, preserving mixed graph
reject   = generator theorem, class invariant, or generic unit vocabulary alone

Bare exact value boundary
boundary = p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md
status   = exact value without support-period branch/root context
decision = conditional_missing_period_156_context
upgrade  = period-156 branch/root/telescoping context
reject   = bare finite-field value that leaves the p25 root branch unspecified

Ambient period-780 value boundary
boundary = p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md
status   = gcd(4^780 - 1, p - 1) = 11, so the F_p value has 11 branches
decision = reject_ambient_780_mu11_branch
upgrade  = support-period 156 fixedness, where gcd(4^156 - 1, p - 1) = 1
reject   = ambient-period value only

Exact period-156 value target
boundary = p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md
status   = active theorem target, not supplied by inspected sources
decision = active_value_side_target
upgrade  = named source theorem giving exact P as a finite-field value with
           period-156 context
reject   = value theorem that drops the mixed graph, orientation, P, or
           finite-field framing
```

## Intake Routers

Any value-side theorem hit should route through these gates:

```text
period_value_upgrade
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py
  accepts exact P value, mixed graph, finite-field identity, and period-156
  context

source_claim_intake
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py
  accepts exact finite-field value P with mixed graph and period-156 context

theorem_hit_router_raw_value
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py
  accepts raw-value theorem hit with raw C/D/K geometry and period-156 context

exact_product_intake
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py
  accepts exact P payload with mixed graph, equal weights, orientation, and
  legal framing

closing_theorem_obligation
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py
  accepts source theorem, DANGER3 framing, extraction path, and vpp-verified
  triple
```

## Gate

This queue gate is intentionally lightweight and does not re-run the heavier
period-value or finite-root harnesses.

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_local_source_value_side_queue_gate.py
```

Marker:

```text
ksy_y_post_local_source_value_side_queue_rows=1/1
```
