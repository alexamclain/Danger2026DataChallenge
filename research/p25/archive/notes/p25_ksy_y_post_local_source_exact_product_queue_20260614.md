# P25 KSY-y Post-Local-Source Exact-Product Queue

Updated: 2026-06-14 10:59 PDT

## Purpose

The local Sprang, Kubert-Lang, KSY, and Koo-Shin source passes are now boundary
artifacts rather than broad reread targets.  This checkpoint records the
remaining exact-product theorem queue and the routers any future theorem hit
must pass through.

## Source Boundaries

```text
KSY arXiv:1007.2307
boundary = p25_ksy_y_normalized_y_product_upgrade_frontier_20260614.md
status   = atom formula plus generation/single-value theorems, no exact p25
           product theorem
upgrade  = exact 75-atom normalized-y product/distribution identity for P
reject   = formula language, field generation, or single y-value without full P

Kubert-Lang IV/V
boundary = p25_ksy_y_kubert_lang_visual_theorem_boundary_20260614.md
status   = dependence/generation/Iwasawa vocabulary, no row labels, reflection
           center, or raw product
upgrade  = exact C3 x C169 row labels, reflection center, or raw equal-weight
           K-traced product
reject   = KL congruence, dependence, freeness, or Iwasawa tower language alone

Sprang/Kronecker
boundary = p25_ksy_y_sprang_exact_specialization_frontier_20260614.md
status   = even-D/Kronecker vocabulary drained as direct closer
upgrade  = named exact mixed row-labeled Sprang theorem/formula hit
reject   = omega^D, kernel/torsion distribution, or cohomology formula without
           exact payload

Koo-Shin 2010 supplied full paper
boundary = p25_ksy_y_koo_shin_2010_full_surface_screen_20260614.md
status   = Theorem 3.9 gives orbit-sum integrality hygiene; Theorem 6.2
           gives complete one-axis products; 9.x are CM/ray-class singular
           generators; no exact mixed p25 product theorem
upgrade  = mixed-level theorem preserving C3 row graph and T edge
reject   = orbit-sum hygiene, one-axis products, CM generation, or C169
           projection without mixed lift
```

## Intake Routers

Any future theorem/literature hit should be routed through the existing gates:

```text
source_claim_intake
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py
  accepts exact divisor/additive P, or exact finite-field value P with
  period-156 context

exact_product_intake
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py
  accepts exact P with mixed graph, equal weights, orientation, arithmetic
  producer, and legal framing

closing_theorem_obligation
  gate = p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py
  accepts source theorem closed, DANGER3 framing unblocked, extraction ready,
  and then a vpp-verified concrete triple
```

## Gate

This queue gate is intentionally lightweight and does not re-run the heavy
finite/value-root harnesses.

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_local_source_exact_product_queue_gate.py
```

Marker:

```text
ksy_y_post_local_source_exact_product_queue_rows=1/1
```
