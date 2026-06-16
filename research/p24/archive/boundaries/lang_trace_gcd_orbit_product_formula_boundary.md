# Lang Trace-GCD Orbit-Product Formula Boundary

Date: 2026-06-05

## Purpose

After the Plucker/Kummer descent audit, the safe payload is a Frobenius
orbit product:

```text
Pi_O = prod_{t in O} Delta(t).
```

This note asks whether the actual small-CM orbit products show an even
smaller visible formula: equality under a unit action, small power relations,
or a product relation among the orbit norms.

## Audit

Added:

```text
p24/lang_trace_gcd_orbit_product_formula_audit.py
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_orbit_product_formula_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail \
  --max-origin-shifts 140 --relation-bound 5
```

The row has:

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7
Frobenius orbits: [0], [1,2,4], [3,6,5]
```

Orbit products:

```text
omitted=0:
  [2125, 2515, 603]

omitted=1:
  [11423, 9495, 6085]
```

The two nontrivial products are distinct in both rows.  The unit `3 mod 7`
swaps the two nontrivial Frobenius orbits, but literal fixed-row equality
fails:

```text
unit=3 equal_edges=1/3
```

The single equal edge is the fixed zero orbit.  Units `2` and `4` act inside
the Frobenius orbits, so their equalities are tautological.

No small multiplicative relation was found with coefficients bounded by `5`:

```text
small_pair_power_relations=[]
small_total_relations_count=0
visible_compression_relation_found=0
```

## Consequence

The audit gives no evidence for replacing the orbit-product payload by a
smaller literal formula inside one fixed trace-GCD row.

The right-unit equivariance theorem remains useful, but only in its proper
form:

```text
unit action transports the full labeled certificate row and preserves
p-unitness.
```

It should not be silently upgraded to:

```text
all fixed-row orbit products are equal or small powers of one another.
```

The pinned row falsifies that stronger fixed-row shortcut.

## Current Payload

The honest finite target remains:

```text
for p24: seven orbit products + seven inverses = 14 base-field elements.
```

Further compression would need an extra theorem, not just visible small-data
patterning:

```text
1. full-row right-unit equivariance for the specific determinant section; or
2. a modular/class-field product formula relating orbit norms; or
3. a semi-invariant Plucker line, already disfavored by the descent audit.
```

Absent one of those, the producer theorem should construct and prove p-unitness
of the actual determinant orbit norms.
