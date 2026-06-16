# Lang Pivot-Order Mining Boundary

Date: 2026-06-05

This note records the first exact pivot-order miner for the
Lang-trivialized mixed tuple.

## Purpose

The representative p24 certificate uses a leading ordered Moore minor:

```text
delete one right Frobenius orbit;
take full right-orbit blocks until crossing left degree;
take the needed tail coordinates from the next block.
```

For p24 this is the `140 + 16` split:

```text
4 full right blocks of length 35, then 16 tail coordinates.
```

The miner tests the same exact certificate shape on small actual-CM rows by
trying rule-defined right-orbit orderings and computing:

```text
leading Moore rank;
full-block prefix rank;
tail augmentation rank;
subspace-polynomial residual norm products;
whether those products descend to the base field.
```

## Audit

Added:

```text
p24/lang_pivot_order_miner.py
```

Pinned positive stress row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_pivot_order_miner.py \
  --only-D -13319 --only-m 28 --only-left 7 --only-right 7 \
  --include-linear --max-orderings 24
```

Output summary:

```text
D=-13319, q=13463, m=28, n=5, pair=(7,7)
left_orbit_len=3
right_orbit_count=2
right_orbit_lengths=[3,3]
transformed_rank=3

omitted_orbit=0:
  leading_full=1/1
  full_block_full=1/1
  tail_full=1/1
  zero residual norms all 0
  canonical_pivots=[0,1,2]
  canonical_norms leading=6609 prefix=6609 tail=1

omitted_orbit=1:
  leading_full=1/1
  full_block_full=1/1
  tail_full=1/1
  zero residual norms all 0
  canonical_pivots=[0,1,2]
  canonical_norms leading=1434 prefix=1434 tail=1
```

A small three-right-orbit row was also found:

```text
D=-5444, q=2657, m=12, n=5, pair=(3,4)
left_orbit_len=2
right_orbit_count=3
right_orbit_lengths=[1,1,1]
```

Every ordering after every deletion was full, and all residual norm products
were base-field-valued and nonzero.  This is a useful multi-orbit sanity
check, but not a p24-shaped tail check because the right blocks have length
`1`.

## Boundary

The miner is not a broad row finder.  Attempts to find richer rows with:

```text
right_orbit_count >= 3,
right_orbit_len >= 2,
left_orbit_len >= 3
```

by direct Hilbert/packet scanning exceeded the intended small-job budget and
were stopped.  The right workflow is:

```text
1. use qfbclassno / quotient-shape / Frobenius-order indexing to shortlist
   candidate rows;
2. run lang_pivot_order_miner.py on those pinned candidates.
```

The cheap prefilter for step 1 is now:

```text
p24/lang_tail_shape_index.py
p24/lang_tail_shape_index_boundary.md
```

It searches class-number, quotient-shape, local splitting, Frobenius
orbit-length, and packet-degree data before any Hilbert/packet construction.
In the bounded windows recorded there, no genuine small `full blocks + tail`
analogue was found.

The current evidence supports the representative leading-window p-unit as an
exact finite-field object, and it confirms residual products descend to the
base field in the checked rows.  It does not yet prove the p24 arithmetic
input:

```text
L_rep = B_rep * T_rep != 0 mod p.
```

The next useful mining task is to find a small actual-CM row with multiple
right orbits of length greater than one and a nonzero tail length, then test
whether the canonical ordering succeeds uniquely or robustly across orbit
orders.
