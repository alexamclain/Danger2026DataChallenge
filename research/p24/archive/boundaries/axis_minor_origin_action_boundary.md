# Axis Minor Origin-Action Boundary

This note refines the leading coefficient-minor route by separating the two
CRT directions of an origin shift.

## Origin Action

For `h=m*n` and an origin shift `s`, write

```text
s == n*alpha + m*beta mod h.
```

Then the packet fibers transform as

```text
F'_r(X) = X^(-beta) F_{r+alpha}(X).
```

For the axis coefficient space, the `alpha` part is only a translation of the
axis coordinate.  Since `W_axis` is stable under `r -> r+alpha`, this gives an
invertible integral change of axis basis.  Therefore any coordinate minor's
zero/nonzero status is invariant under pure `alpha` shifts, although the value
may change by a unit depending on the chosen basis.

The `beta` part is different: it multiplies the whole axis subspace by
`X^(-beta)` before projecting to the leading coordinate window.  Thus the
leading-minor route asks for a cyclic consecutive-Pluecker condition:

```text
det(P_0 X^(-beta) V_axis) != 0
```

for the relevant chosen `beta`, or for every `beta` if one wants an
origin-independent coordinate-minor certificate.  Here `P_0` projects to the
first `dim(W_axis)` packet coordinates.

## Audit

I added:

```text
p24/axis_minor_origin_action_audit.py
```

Tiny dimension-forced row:

```text
D=-671, q=2693, h=30, m=6, n=5
```

reported:

```text
all_origins count=30 distinct=2 zeros=0
pure_alpha_beta0 count=6 distinct=2 zeros=0
pure_beta_alpha0 count=5 distinct=1 zeros=0
alpha_fixed_distinct_hist={1: 6}
beta_fixed_distinct_hist={2: 5}
```

First extra-coordinate row:

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
```

reported:

```text
all_origins count=132 distinct=22 zeros=0
pure_alpha_beta0 count=12 distinct=2 zeros=0
pure_beta_alpha0 count=11 distinct=11 zeros=0
alpha_fixed_distinct_hist={11: 12}
beta_fixed_distinct_hist={2: 11}
```

So beta shifts really move the leading minor through many values, while no
zero appeared in this CM row.

## Consequence

The coefficient-minor certificate now has a clean finite-field target:

```text
the axis packet subspace is cyclically consecutive-superregular
for the required leading window.
```

The packaged p-unit form is recorded in:

```text
p24/axis_sliding_window_product_audit.py
p24/axis_sliding_window_product_theorem.md
```

It defines

```text
Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a).
```

Beta origin shifts permute the factors; alpha shifts multiply the product by
the `n`th power of a unimodular axis-basis determinant.  Thus the product's
zero/nonzero status is origin-stable, and `Pi_axis,a^2` removes the sign
ambiguity in the value.

This target implies axis injectivity directly, but it is less class-field
invariant than the Hermitian determinant.  A proof must control monomial
shifts of the selected CM axis subspace in the packet power basis; it cannot
borrow the Hermitian origin-cancellation argument.

The random baseline is recorded in:

```text
p24/cyclic_superregular_random_baseline.py
p24/cyclic_superregular_random_baseline.md
```

On the targeted `D=-8711` row, random subspaces failed some beta-shifted
leading minor only `4/5000` times, close to the naive `n/q` heuristic.  Thus
small-data success of cyclic consecutive-superregularity is generic-looking;
the route still needs an arithmetic proof for the actual CM axis subspace at
the selected p24 prime.
