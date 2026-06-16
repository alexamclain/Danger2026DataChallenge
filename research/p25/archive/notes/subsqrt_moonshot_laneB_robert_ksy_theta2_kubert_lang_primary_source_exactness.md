# P25 Lane B: Robert KSY Kubert-Lang Primary-Source Exactness

Updated: 2026-06-13 18:40 PDT

## Purpose

This is the router-facing map from primary-source families to actual output
types.  It keeps promising sources alive only when they instantiate the exact
p25 `C/D/K/orientation` payload.

## Continue

```text
Sprang / Kronecker D-variant differential
  lane: raw-divisor-or-additive
  continue only if it emits exact theta2/theta2^-1 divisor/additive data

Koo-Shin-Yoon normalized y
  lane: raw-value-with-period-156-context
  continue only with exact 75-atom K-traced product and period-156 context

Kubert-Lang exact Siegel exponent matrix
  lane: finite-spine-verifier-target
  continue only if it preserves the mixed C3 x C169 row graph and finite intake
```

## Conditional

```text
Siegel-Robert value units
  lane: raw-value-with-period-156-context
  continue only with explicit branch/root data or period-156 fixedness
```

## Kill

```text
ordinary Kato-Siegel theta_D direct
  killed as direct D=2 proof

generic Koo-Shin-Yoon ray-class generation
  killed until instantiated as exact product or theta2 payload

raw KL exponent balance only
  killed unless paired with finite intake geometry
```

## Primary-Source Anchors

- Sprang, `arXiv:1802.04996`: algebraic D-variant
  Kronecker/polylogarithm differential representatives; ordinary Kato-Siegel
  `theta_D` appears as a specialization with its own prime-to-6 gate.
- Koo-Shin-Yoon, BK21 09-20 / `arXiv:1007.2307`: normalized
  `y(r1,r2)=-g(2r1,2r2)/g(r1,r2)^4`; Theorem 5.3 and
  Theorem 6.2 / Corollary 6.4 are field-generation statements, not the exact
  p25 product identity.
- Kubert-Lang, *Units in the Modular Function Field IV*: source of the
  Siegel-product modular-unit language, but the p25 congruence screen is
  saturated without the finite row graph.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_primary_source_exactness_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_primary_source_exactness_rows=1/1
```

## Interpretation

The next real theory move is not another source-family endorsement.  It is an
instantiated formula whose actual output type can be fed to the theorem-hit
router.
