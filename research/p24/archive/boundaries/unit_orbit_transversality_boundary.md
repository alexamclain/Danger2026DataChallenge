# Unit-Orbit Transversality Boundary

Date: 2026-06-05

This note closes a tempting shortcut in the representative p-unit route.

## Question

The p24 certificate uses the unit `2 mod 211` to cycle the six right
Frobenius blocks.  Could this cyclic symmetry alone force the representative
leading minor

```text
four full blocks + one 16-coordinate tail
```

to be nonzero?

## Toy

Added:

```text
p24/unit_orbit_transversality_toy.py
```

It models the six right blocks as a cyclic orbit of one observation map:

```text
L = F_q^n,
A : L -> F_q^r,
A_j = A D^j,        j=0,...,5.
```

The representative p24-style row keeps:

```text
O2,O3,O5,O6 full blocks, and a tail slice of O1.
```

Two actions are compared:

```text
D = identity;
D = permutation of order 6.
```

The identity action is perfectly cyclic-symmetric but all blocks are the same,
so it is an explicit symmetric failure mode.

## Results

Small p24-shaped dimensions:

```text
q=5, dim=14, block_dim=3, tail_len=2:
  identity:
    selected_full=0/500, tail_full=0/500.
  permutation:
    prefix_full=356/500, selected_full=0/500, tail_full=98/500.

q=7, dim=18, block_dim=4, tail_len=2:
  identity:
    selected_full=0/300, tail_full=0/300.
  permutation:
    prefix_full=280/300, selected_full=215/300, tail_full=232/300.
```

The permutation action can make transversality common, but it does not make it
formal.  The identity action shows that unit-orbit symmetry by itself is far
too weak.

## Consequence

The right-unit theorem remains a compression theorem:

```text
one representative p-unit nonzero
  => all six equivariant deletion-row p-units nonzero.
```

It is not a nonvanishing theorem.  The arithmetic proof still has to certify:

```text
L_rep = B_rep * T_rep != 0 mod p.
```

Equivalently, in the dual form, it must prove that the four full right traces
cut `L=F_p(mu_157)` to the expected 16-dimensional kernel and that the
equivariant tail map is injective on that kernel.
