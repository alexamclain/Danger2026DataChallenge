# Trace-GCD Residual Moore/Chow Section

Date: 2026-06-06

## Point

The residual-product theorem can be made more explicit than "some
subspace-polynomial scalar is a p-unit."  It is the p-unitness of a named
Moore/Chow section and, after the `140+16` split, of a prefix Moore section
and a quotient-tail Moore section.

This does not prove the p24 arithmetic theorem, but it identifies the exact
phase-aware Fitting section a Borcherds/local-intersection proof should
construct.

## Finite Identities

Let

```text
L/F_q be degree d,
c_1,...,c_s in L,
Delta_s(c) = det(c_j^(q^(i-1)))_{1 <= i,j <= s}.
```

Let `P_i` be the monic q-linearized annihilator of the span of
`c_1,...,c_i`, and let

```text
r_i = P_{i-1}(c_i).
```

Then the ordered residual product is exactly the Moore determinant:

```text
prod_{i=1}^s r_i = Delta_s(c_1,...,c_s).
```

Consequently the all-coordinate residual norm product is

```text
R(c_1,...,c_d) = Norm_{L/F_q}(Delta_d(c_1,...,c_d)).
```

For a full tuple, choose an integral basis

```text
a_1,...,a_d of L/F_q
```

and write `C` for the coordinate matrix with columns `c_i`.  Then:

```text
Delta_d(c_1,...,c_d)
  = Delta_d(a_1,...,a_d) * det(C).
```

Thus:

```text
R(c_1,...,c_d)
  = Norm(Delta_d(a)) * det(C)^d.
```

At the p24 ordinary prime, the cyclotomic/power basis constants are p-units
because `p` is unramified and prime to the level.  Therefore the full
residual p-unit statement is exactly the ordinary coordinate Chow determinant
p-unit statement, up to a fixed p-unit.

## Prefix/Tail Quotient Section

For an ordered prefix

```text
b_1,...,b_k
```

let `U=span_Fq(b_1,...,b_k)` and let `P_U` be its monic q-linearized
annihilator.  For a tail tuple

```text
t_1,...,t_{d-k}
```

define the quotient-tail images:

```text
y_i = P_U(t_i).
```

Then:

```text
tail residual product after the prefix
  = Delta_{d-k}(y_1,...,y_{d-k}).
```

and

```text
Delta_d(b_1,...,b_k,t_1,...,t_{d-k})
  = Delta_k(b_1,...,b_k) * Delta_{d-k}(P_U(t_1),...,P_U(t_{d-k})).
```

This is the finite quotient-Schubert object behind the p24 split:

```text
d = 156,
k = 140,
d-k = 16.
```

So the fixed p24 theorem can be stated as:

```text
Delta_140(prefix O2,O3,O5,O6) is a p-unit,
Delta_16(P_U(first 16 coordinates of O1)) is a p-unit.
```

The nonzero theorem is the crossed Frobenius norm of the transported pair of
sections around the selected length-35 right orbit.

## Arithmetic Restatement

For the embedded `157/211` p24 CM trace family, construct over the localized
ordinary ring:

```text
Psi_prefix(t) = Delta_140(prefix_t),
Psi_tail(t)   = Delta_16(P_{U_t}(tail_t)).
```

The remaining arithmetic theorem is:

```text
Psi_prefix(0), Psi_tail(0) are p-units,
prod_{t in O1} Psi_prefix(t) and prod_{t in O1} Psi_tail(t) are p-units,
```

with determinant-line transition factors allowed to change these scalars by
p-units.

Equivalently, the pulled-back phase-aware Moore-Schubert divisors do not meet
the selected ordinary CM point modulo `p=10^24+7`.

## Why This Is Sharper

The older language said "prove the residual product is a p-unit."  The new
language names the section:

```text
Moore determinant of the prefix
+ Moore determinant of prefix-annihilator tail images.
```

This is the object a Fitting/Borcherds proof must recognize.  It also blocks
a possible mistake: the quotient-tail section is not a Moore determinant of
the raw tail coordinates.  It is the Moore determinant after applying the
prefix annihilator `P_U`.

## Audit

The finite identities are guarded by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_residual_moore_chow_toy.py
```

Current output:

```text
full_residual_mismatches=0
full_chow_mismatches=0
norm_chow_mismatches=0
prefix_moore_mismatches=0
tail_image_mismatches=0
prefix_tail_mismatches=0
full_zero_coordinate_zero_mismatches=0
forced_prefix_zero=1
forced_tail_zero=1
```

The audit includes a forced dependent prefix and a forced tail element whose
image modulo the prefix is zero.

## Schur-Pivot Representative

A base-field representative of the quotient-tail section is recorded in:

```text
p24/trace_gcd_residual_schur_pivot_target.md
p24/trace_gcd_residual_schur_complement_toy.py
```

After choosing a p-unit `140 x 140` prefix Plucker pivot, the
`16`-dimensional quotient-tail Moore p-unit is equivalent to the p-unitness
of the corresponding ordinary `16 x 16` Schur complement.  This gives a
concrete finite target for proof search without changing the determinant-line
or certificate surface.
