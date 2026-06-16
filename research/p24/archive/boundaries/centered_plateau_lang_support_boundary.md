# Centered Plateau Lang-Support Boundary

Date: 2026-06-06

This note records why the right Fourier/Lang normalization does not by
itself turn the centered consecutive-arc theorem into an ordinary
coordinate-support distance theorem.

## Actual Bad Subspace

For centered point columns `P_b`, every dual word satisfies:

```text
w(0) = 0,
```

because `P_0=0`.  A window determinant vanishes when a nonzero dual word is
constant on a plateau

```text
I_t = {t, ..., t+left-1}.
```

So the relevant bad subspace is:

```text
B_t^0 = {w : w is constant on I_t and w(0)=0}.
```

For p24:

```text
right = 211,
left = 157,
dim B_t^0 = 211 - 157 = 54.
```

This is complementary to the `156`-dimensional centered row space inside the
hyperplane `w(0)=0`, whose dimension is `210`.

## Audit

Added:

```text
p24/centered_plateau_lang_support_audit.py
p24/centered_plateau_factor_support_audit.py
```

It applies the right Fourier transform and right-orbit Lang trivialization to
`B_t^0`, then measures whether the transformed subspace is a small coordinate
or block-support subspace.

Small actual analogue parameters:

```text
q=6863,  right=7,  left=3;
q=13463, right=7,  left=4;
q=11243, right=13, left=3.
```

For the selected `start=0` plateaus:

```text
right=7,left=3:
  dim B_t^0=4,
  transformed_active_columns=7/7,
  block_rank_profile=[zero rank 1, orbit rank 4].

right=7,left=4:
  dim B_t^0=3,
  transformed_active_columns=7/7,
  block_rank_profile=[zero rank 1, orbit ranks 3 and 3].

right=13,left=3:
  dim B_t^0=10,
  transformed_active_columns=13/13,
  block_rank_profile=[zero rank 1, orbit rank 10].
```

Shifted plateaus behave the same way at the containment level:

```text
transformed_active_columns=right/right.
```

## P24-Shape Factor Audit

The exact p24 right geometry can be tested without the huge prime `p`.  Since

```text
ord_211(p24) = 35,
ord_211(5) = 35,
```

the carrier field `F_5` has the same right Frobenius orbit structure.  The
factor-level audit reduces the plateau basis polynomials modulo each
irreducible factor of `Y^211-1` over `F_5`; Lang trivialization is invertible
on each factor, so these residue ranks are the block ranks after
Fourier/Lang normalization.

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_plateau_factor_support_audit.py \
  --q 5 --right 211 --left 157 --start 0 --zero-position 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_plateau_factor_support_audit.py \
  --q 5 --right 211 --left 157 --start 17 --zero-position 0
```

Both report:

```text
plateau_subspace_dim=54
factor_count=7
nonzero_factor_blocks=7/7
linear zero-frequency block rank=1
each of the six degree-35 right-orbit blocks has rank=35
```

Thus the p24 bad plateau subspace is maximally spread across the right
Frobenius orbit blocks after the natural Fourier/Lang normalization.  Even
though its total dimension is only `54`, its projection to every nonzero
right orbit block is surjective.

## Consequence

The bad plateau subspace is sparse in the time coordinate basis, but after
the natural Fourier/Lang normalization it is **not contained in a small
coordinate support**.  It touches every transformed coordinate in the tested
analogues, and in the exact p24 right-orbit geometry it projects with full
rank to every degree-35 orbit block.

Therefore an ordinary MDS/MSRD support-distance theorem does not directly
prove the centered arc theorem after Lang normalization.  Such a theorem
would exclude vectors contained in small coordinate-erasure spaces; the
centered bad event becomes a dense Schubert subspace instead.

The LRS/MSRD route is still possible only in the stronger form:

```text
prove the actual transformed centered row space avoids the named transformed
plateau Schubert subspaces.
```

But that is again an arithmetic Schubert p-unit theorem, not a free
coordinate-support consequence.

This complements:

```text
p24/msrd_metric_boundary.md
p24/msrd_vs_mds_boundary.md
p24/centered_marginal_transversality_boundary.md
```
