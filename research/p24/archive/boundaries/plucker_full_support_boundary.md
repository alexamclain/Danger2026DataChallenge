# Pluecker Full-Support Boundary

This note checks whether the coefficient-minor route is better understood as a
strong Grassmannian open-cell condition.

## Question

The sliding-window product checks only cyclic interval minors.  A stronger
condition is:

```text
every r x r coordinate minor of V_a is nonzero.
```

This is the uniform-matroid / MDS-generator condition for the axis subspace in
the packet power basis.

## Audit

I added:

```text
p24/plucker_full_support_audit.py
```

For the first extra-dimensional row:

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
factor_degree=10, axis_dim=6
```

there are only

```text
C(10,6)=210
```

Pluecker coordinates.  The audit reported:

```text
cm_axis:
  plucker_zero_count=0
  full_plucker_support=1
  interval_zero_count=0

random_baseline:
  full_plucker_support_trials=490/500
  plucker_zero_min=0
  plucker_zero_max=1
  interval_failure_trials=0
```

## Consequence

The CM axis subspace lies in the full-support Grassmannian open cell in this
row, but this is generic at the observed field size.  The stronger
full-Pluecker condition is therefore not currently a CM theorem lead; it is a
generic finite-field rank condition.

The cyclic interval product `Pi_axis,a` remains the smaller certificate
surface, but its observed nonvanishing is also generic-looking.  A proof still
has to use selected-prime CM arithmetic.
