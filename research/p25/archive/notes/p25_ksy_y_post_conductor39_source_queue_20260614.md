# P25 KSY-y Post-Conductor-39 Source Queue

Updated: 2026-06-14 11:15 PDT

## Purpose

The Yang `Y_507` period-norm source has been compressed to a mixed
conductor-`39` unit plus Yang distribution:

```text
U_chi = -chi_3 * chi_13 on X_1(39)
Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi)
```

This changes the moonshot queue.  The first theorem target is now the small
mixed `X_1(39)` object, not an arbitrary level-`507` or level-`12675` producer.

## Queue

```text
1. mixed_x1_39_unit_plus_yang_distribution
   decision = continue_first
   accepts  = source theorem emits U_chi, V_bal, or W on X_1(39), preserves
              chi_3 tensor chi_13 signs, and applies Yang's 13-fiber lift
   reject   = conductor-3-only, conductor-13-only, additive-separated,
              prime-projection, or level-507 story without the 13-fiber descent

2. hilbert90_period156_value_descent
   decision = continue_second
   accepts  = finite-field value/divisor theorem for the conductor-39 source
              using ratio, twisted trace, Hilbert-90 boundary, or one of the
              legal support-156 sparse Yang-lift potentials, with period-156
              branch context
   reject   = naive degree-6 norm, bare exact value, or ambient period-780 value

3. ksy_kl_exact_75_atom_product
   decision = continue_as_companion
   accepts  = exact K-traced normalized-y/theta2 product P with mixed graph,
              equal weights, orientation, arithmetic producer, and DANGER3
              framing
   reject   = formula language, field generation, KL congruence hygiene,
              single y-value, or exact product missing mixed graph

4. koo_shin_2010_theorem52_root_descent
   decision = keep_as_helper
   accepts  = constant-product/root-descent context after an independent mixed
              producer exists
   reject   = using Theorem 5.2 alone or a prime-13/C169 projection as payload

5. prime13_or_c169_projection_closer
   decision = kill
   reject   = proper pushforwards of U_chi vanish; projection erases the source
```

## Interpretation

The moonshot is now less diffuse:

```text
first theorem target     = mixed X_1(39) unit plus Yang distribution
second theorem target    = period-156 Hilbert-90/value descent, sharpened to
                           a canonical legal 78-over-78 sparse Yang-fiber
                           product, up to <2>-translate
companion theorem target = exact 75-atom normalized-y/theta2 product
killed shortcut          = prime13/C169 projection closer
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_conductor39_source_queue_gate.py
```

Expected marker:

```text
ksy_y_post_conductor39_source_queue_rows=1/1
```
