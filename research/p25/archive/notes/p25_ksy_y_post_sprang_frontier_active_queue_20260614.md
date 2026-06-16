# P25 KSY-y Post-Sprang Frontier Active Queue

Updated: 2026-06-14 08:18 PDT

## Purpose

The Sprang exact-specialization frontier drains the current Sprang clauses as
direct p25 closers.  This checkpoint makes the next active moonshot queue
explicit so the search does not drift back into broad Sprang rereading.

## Queue

```text
priority 1: kubert_lang_ksy_exact_mixed_product
role       active front door
continue  named theorem/formula hit producing exact row-labeled pairs,
          reflection center, or raw equal-weight K-traced product
falsifier C169 projection, KL congruence hygiene, generator theorem, or
          Iwasawa freeness without exact mixed row labels

priority 2: ksy_normalized_y_exact_distribution
role       active companion front door
continue  exact K-traced normalized-y product/distribution theorem feeding
          the theta2/theta2-inverse certificate path
falsifier single y-value, ray-class generation, or formula language without
          all 75 atoms and orientation

priority 3: sprang_exact_specialization_hit
role       watchlist, not active broad reread
continue  only on a new named source theorem/formula hit emitting the exact
          mixed row-labeled p25 payload
falsifier omega^D, kernel/torsion distribution, prime-to-6 theta_D comparison,
          or cohomology formula without exact p25 payload

priority 4: kl_iv_v_direct_source_boundary
role       killed shadow with OCR/human-upgrade hook
continue  only if upgraded to exact row labels, reflection center, or raw
          product
falsifier generic modular-unit generation, multiplicative dependence, Delta
          criteria, p-primary tower, or Iwasawa module freeness
```

## Gate

This queue gate deliberately avoids the heavy mixed-graph/value-root harnesses.
It depends only on the lightweight Sprang frontier, exact-product intake, and
Kubert-Lang IV/V source-boundary profiles.

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_sprang_frontier_active_queue_gate.py
```

Marker:

```text
ksy_y_post_sprang_frontier_active_queue_rows=1/1
```
