# P25 KSY-y / Yang / H90 Bridge Spine

Updated: 2026-06-14 11:27 PDT

## Purpose

This note records the current bridge between the KSY 75-atom product language
and the canonical sparse Yang Hilbert-90 product.  It prevents two bad readings:

```text
wrong 1: 75 atoms means 75 candidate tries
wrong 2: the 78-over-78 H90 product is unrelated to the KSY/Yang target
```

The verified picture is one structured spine, not a shortlist.

## Count Ladder

```text
75 fixed normalized-y atoms
  -> 300 raw Siegel footprint terms
  -> 12-term quotient Y_507
  -> 312-cell period norm Norm_156(Y_507)
  -> 156-cell sparse Hilbert-90 potential
```

The gate verifies:

```text
atom_count                  = 75
raw_siegel_term_count       = 300
quotient_y507_support       = 12
period_norm_support         = 312
h90_potential_support       = 156
h90_positive_factor_count   = 78
h90_negative_factor_count   = 78
```

## Shared Source Word

In the primitive-D coordinate, the KSY quotient source is:

```text
U_507 =
  z^121 + z^122 + z^123
  - z^384 - z^385 - z^386
```

The normalized-y/Yang word is:

```text
Y_507 = [2]^*U_507 / U_507^4
```

or, additively:

```text
Y_507 =
  -4 z^121 -4 z^122 -4 z^123
  +   z^242 +   z^244 +   z^246
  -   z^261 -   z^263 -   z^265
  +4 z^384 +4 z^385 +4 z^386
```

## Hilbert-90 Product

The canonical sparse Hilbert-90 preimage is the 78-over-78 Yang-fiber product:

```text
P0 = {7, 17, 23, 34, 37, 38}
N0 = {4, 8, 10, 11, 20, 25}

H0 = 6 * (
  sum_{a in P0, k=0..12} [a + 39k]
  -
  sum_{b in N0, k=0..12} [b + 39k]
)
```

It has:

```text
positive factors = 6 * 13 = 78
negative factors = 6 * 13 = 78
support          = 156
boundary         = (1 - Frob_p) H0 = Norm_156(Y_507)
```

The four legal sparse H90 products form one conductor-39 doubling orbit, with
canonical stabilizer `{1, 16, 22}`.

## Consequence

The KSY 75 atoms are fixed factors inside the exact product, not search
candidates.  The 78-over-78 H90 product is a downstream Hilbert-90 preimage of
the same KSY/Yang source, not a competing 75-atom object.

The remaining theorem debt is still:

```text
finite-field value/divisor identity for exact P, Y_507, or H0
DANGER3-compatible framing
(A, x0) extraction
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_ksy_product_h90_bridge_spine_gate.py
```

Marker:

```text
ksy_y_yang_ksy_product_h90_bridge_spine_rows=1/1
```
