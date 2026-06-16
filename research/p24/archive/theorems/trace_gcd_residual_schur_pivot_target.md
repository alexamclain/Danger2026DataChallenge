# Trace-GCD Residual Schur-Pivot Target

Date: 2026-06-06

## Point

The residual Moore/Chow section gives an intrinsic quotient-tail determinant:

```text
Delta_16(P_U(tail_1),...,P_U(tail_16)).
```

For proof search, this can be replaced by ordinary base-field linear algebra
after choosing a p-unit Plucker pivot for the prefix.  This gives a concrete
Schur-complement target for the p24 `140+16` split.

## Finite Statement

Let `c_1,...,c_156` be written in a p-integral `F_p`-basis of

```text
L = F_p(mu_157).
```

Let the first `140` columns be the prefix matrix `B`, and the last `16`
columns be the tail matrix `T`.

Choose row indices `X`, `|X|=140`, such that:

```text
det(B_X) is a p-unit.
```

Let `Y` be the complementary `16` row indices.  The ordinary Schur complement
is:

```text
S = T_Y - B_Y * B_X^{-1} * T_X.
```

Then:

```text
det([B T]_{X,Y}) = det(B_X) * det(S).
```

Moreover, once `det(B_X)` is a p-unit:

```text
det(S) is a p-unit
  <=> the tail images are independent in L/span(prefix)
  <=> Delta_16(P_U(tail_i)) is a p-unit.
```

So one possible p24 proof shape is:

```text
1. prove a named 140 x 140 prefix Plucker minor det(B_X) is a p-unit;
2. prove the corresponding 16 x 16 Schur complement det(S) is a p-unit;
3. take the crossed/Frobenius norm of the transported pair for O1.
```

This avoids explicit manipulation of the degree-140 p-linearized annihilator
`P_U`, while proving the same quotient-tail section.

## Relation To Moore/Chow

This is not a new certificate surface.  It is a coordinate representative of
the same determinant line recorded in:

```text
p24/trace_gcd_residual_moore_chow_section.md
```

The prefix Moore determinant is intrinsic and is nonzero exactly when some
prefix Plucker pivot exists.  The Schur target becomes useful only after a
specific pivot `X` is chosen and proved p-unit by arithmetic or structure.

For p24, the most conservative first pivot candidate is the natural power
basis row order with a contiguous or Frobenius-stable `140`-row set.  That
candidate is not proved here; it is the next falsifiable theorem choice.

## Audit

The finite zero-detection identities are guarded by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_residual_schur_complement_toy.py
```

Current output:

```text
determinant_mismatches=0
prefix_zero_mismatches=0
tail_zero_mismatches=0
full_zero_mismatches=0
forced_prefix_no_pivot=1
forced_tail_schur_zero=1
```

The forced controls confirm that a dependent prefix has no pivot and that a
tail vector already lying in the prefix span gives zero Schur complement.
