# Right-Unit Subspace-Orbit Boundary

Date: 2026-06-05

This note records a boundary for using right-unit equivariance in the
representative p24 proof.

## Tempting Shortcut

The verifier uses the unit `2 mod 211` to cycle right orbit labels:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

This propagates the whole representative deletion-row certificate.  A tempting
stronger claim would be:

```text
inside one fixed row, the six trace-coordinate subspaces W_j in L are all
generated from one W by a single F_p-linear operator on L.
```

If true, the representative p-unit might reduce to a cyclic subspace-code
theorem for one 35-plane.

## Boundary

The unit action is a symmetry of the full cyclotomic product algebra and of
the certificate data.  It permutes right factors and compatible Lang
coordinate choices.  It does **not** by itself imply that the six subspaces in
one fixed mixed row are equal, or that they are a trivial orbit under a known
operator on `L`.

The fixed-row subspaces are:

```text
W_j = span_Fp{ Tr_{E/L}(delta_i*S_j) : i=1..35 } subset L.
```

The right-unit symmetry transports the whole construction from one factor
labeling to another.  It preserves p-unit nonvanishing of the corresponding
certificate rows, but it is not a formal replacement for proving the
representative row determinant.

## Toy Audit

Added:

```text
p24/right_unit_subspace_orbit_toy.py
```

It builds a random finite-field DFT model with six right Frobenius orbits and
computes the Lang-trivialized subspace attached to each right orbit.

Cheap run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/right_unit_subspace_orbit_toy.py --q 2 --left 11 --right 31
```

Output:

```text
left_degree=10
right_degree=5
right_orbit_count=6
unit_cycle=3
unit_permutation_1based=[2,3,6,5,1,4]
block_ranks=[5,5,5,5,5,5]
unit_edge_join_ranks=[9,9,9,9,8,9]
unit_equal_edges=0/6
unit_frobenius_edge_shifts=[[],[],[],[],[],[]]
unit_frobenius_equal_edges=0/6
all_equal_pairs=0/15
```

Interpretation:

```text
unit_permutation_of_labels_does_not_force_fixed_row_subspace_equality.
```

This is an intentionally random DFT model, not CM evidence.  Its value is
logical: if unit equivariance alone forced fixed-row subspace equality, it
would force it here too.  It does not.

## Consequence

The one-punit proof cannot be replaced by:

```text
all six W_j are the same W in disguise.
```

A cyclic-subspace theorem is still possible, but it would need extra
arithmetic input identifying a genuine operator/action on `L` for the actual
CM periods.  The existing verifier equivariance remains valid and useful:

```text
one representative p-unit + full-product-algebra unit/Lang compatibility
=> p-units for all deletion rows.
```

It does not prove the representative p-unit itself.
