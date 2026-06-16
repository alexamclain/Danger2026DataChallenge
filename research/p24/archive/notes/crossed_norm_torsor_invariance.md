# Crossed Norm Torsor Invariance

Date: 2026-06-06

## Point

The cyclic class-tower obstruction says a parent quotient root has a child
torsor above it.  Therefore a strict producer theorem should avoid depending
on a canonically selected child whenever possible.

The nonzero trace-GCD side already has the right invariant:

```text
Xi_O = Nrd_O(Phi_t)
```

where `Phi_t` is the transported square coinvariant map around one right
Frobenius orbit.

Changing the basepoint, local basis, or compatible child labeling may change
the displayed scalar, but only by determinant-line p-unit factors if the
producer has been constructed p-integrally.  Thus the intrinsic statement is:

```text
Xi_O is a p-unit as a determinant-line norm.
```

It is not:

```text
one printed local child determinant has a canonical value.
```

## Finite Gate

The finite handoff is now recorded in:

```text
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```

The added choice-invariance lemmas say:

```text
if every admissible choice of the crossed norm is related to every other by
p-unit scaling, then p-unitness or nonzero status for one choice propagates
to all choices.
```

This is the correct finite counterpart of the class-tower obstruction:
child selection is impossible in general, but orbit norms are allowed because
they are invariant up to p-unit determinant-line scale.

## Consequence

The nonzero-orbit theorem should be proved as a reduced norm in the
semilinear/crossed-product algebra:

```text
Nrd_O(Phi_t) in O_p^*
```

for one nonzero right Frobenius orbit, plus unit-2 determinant-line transport
to the other five nonzero orbits.

This avoids the false abstract-tower requirement of naming a child in the
`211` layer.  It does not prove the p24 arithmetic theorem.  The producer must
still construct the p-integral determinant line and prove its reduced norm is
a p-unit at the selected ordinary CM point.
