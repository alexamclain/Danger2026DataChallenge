# Tensor Factor K-Action Boundary

This note rules out a tempting shortcut for the one-factor tensor theorem.

## Tempting Shortcut

After adjoining

```text
E = F_p(mu_m),
```

the 368 axis resolvents in one tensor factor have distinct K-character labels.
One might hope that they are eigenvectors for an `E`-linear K-action on the
single tensor factor `B_i`.  Then distinct eigenvalues would force directness
automatically, and the axis theorem would reduce to proving the individual
resolvents are nonzero.

## Why This Cannot Be Formal

The small row

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
deg(f)=10, [E:F_q]=2
```

has two tensor factors of degree `5` over `E`.  In one factor the axis
frequencies are

```text
S_axis = {0, 3, 6, 9, 4, 8},
```

with six distinct K-character labels.  The block scan reports:

```text
factor_degree=5
axis_dim=6
full_rank=5
block_ranks=[
  ('constant', 1, 1),
  ('4',        3, 3),
  ('3',        2, 2)
]
block_fail=0
pair_fail=0
full_fail=1
```

Thus all six selected resolvents are nonzero, and the component blocks are
internally full.  The total rank is only `5` because the ambient factor has
dimension `5`.

If a single `E`-linear K-action stabilized this tensor factor and made these
six nonzero vectors eigenvectors with the six distinct eigenvalues
`zeta_12^s`, they would be linearly independent.  That would force rank `6`
inside a five-dimensional `E`-space, a contradiction.

So the K-action does **not** act as an `E`-linear diagonal operator on one
tensor factor.  It is an action on the class-field/primes before reduction;
after selecting an H-subpacket tensor factor, the action is not an internal
linear symmetry of that factor.

## Correct Consequence

The directness theorem remains a genuine p-unit/rank statement:

```text
E·R_0 ⊕ span_E{R_s : s in S_2}
      ⊕ span_E{R_s : s in S_157}
      ⊕ span_E{R_s : s in S_211}
```

inside a degree-5549 p24 tensor factor.

Nonzero support of the selected K-character resolvents is not enough.  The
small dimension-bound rows already show support without rank.

## Valid Symmetry That Remains

Semilinear Frobenius still permutes tensor factors and preserves their ranks:

```text
R_s(eta)^p = R_{p*s}(eta^p).
```

That is why `tensor_factor_rank_symmetry.md` is valid.  It proves that all
tensor factors have the same axis rank, not that the axis rows inside one
factor are automatically independent.
