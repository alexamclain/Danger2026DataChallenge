# P25 KSY-y Priority-1 Sprang Source Split

Updated: 2026-06-13 21:34 PDT

## Purpose

Priority 1 keeps Sprang/Kronecker alive, but the source handles must not blur.
There are two nearby Sprang papers in play, and neither currently supplies the
exact p25 anti-invariant product by itself.

## Source Handles

```text
arXiv:1801.05677
title: Eisenstein-Kronecker series via the Poincare bundle
role: Kronecker-section / Eisenstein-Kronecker construction and distribution vocabulary
status: conditional_formula_language_without_product_proof
missing: explicit specialization to exact P or theta2/theta2^-1 divisor data

arXiv:1802.04996
title: The algebraic de Rham realization of the elliptic polylogarithm via the Poincare bundle
role: algebraic de Rham polylogarithm / Eisenstein-class differential-form surface
status: conditional_formula_language_without_product_proof
missing: exact D=2 differential/additive output for the p25 anti-invariant product
```

Both handles remain useful, but only as source vocabulary until they are
specialized to the exact p25 payload:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Closing Shape

The Sprang lane closes priority 1 only if a source theorem emits:

```text
exact D=2 p25 product identity
or exact theta2/theta2^-1 divisor/additive data
with mixed graph, equal weights, orientation, finite intake, arithmetic producer,
and DANGER3-legal framing
```

That hypothetical routes through exact-product intake as:

```text
closing_exact_product_identity
```

## Rejected Import

The ordinary Kato-Siegel `theta_D` route remains killed as a direct `D=2`
proof.  It is an odd-`D` control, not the Sprang even-`D` upgrade path.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_sprang_source_split_gate.py
```

## Completed Gate

```text
distinct_primary_sources     = 3
conditional_source_handles   = 2
rejected_imports             = 1
closing_hypotheticals        = 1
```

Marker:

```text
ksy_y_priority1_sprang_source_split_rows=1/1
```
