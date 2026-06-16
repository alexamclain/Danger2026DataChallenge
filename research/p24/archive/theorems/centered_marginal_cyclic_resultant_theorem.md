# Centered Marginal Cyclic Resultant Theorem Candidate

Date: 2026-06-05

This note packages the p24 right-translation product from
`p24/centered_marginal_origin_product_theorem.md` as a cyclic resultant.

## Right-Translation Sequence

For p24, the origin-product reduction gives:

```text
Pi_C = (prod_{t mod 211} F(t))^314,
```

where `F(t)` is the leading `156 x 156` centered-marginal minor after a
right-component translation by `t`.

Let `omega` be a formal 211st root of unity, and let `f_C(Y)` be the unique
polynomial of degree `<211` over `F_p(mu_211)` satisfying:

```text
f_C(omega^t) = F(t),       t mod 211.
```

Then:

```text
Pi_C,right = prod_{t mod 211} F(t)
           = Res_Y(Y^211 - 1, f_C(Y)).
```

So the compact p24 target can be written as:

```text
Res_Y(Y^211 - 1, f_C(Y)) != 0 mod p.
```

## Frobenius-Orbit Product Split

For `p=10^24+7`:

```text
p mod 211 = 114,
ord_211(p) = 35.
```

Therefore the right exponents split into:

```text
{0} plus six nonzero Frobenius orbits O_1,...,O_6 of size 35.
```

The product splits as seven base-field orbit products:

```text
Pi_C,right =
  F(0) * prod_{j=1}^6 prod_{t in O_j} F(t).
```

This is the most compact algebraic certificate surface currently attached to
the visible centered-marginal minor:

```text
seven base-field p-unit checks:
  one value at Y=1,
  six size-35 Frobenius-orbit products.
```

This should not be confused with a norm factorization of a base-coefficient
interpolating polynomial.  A base-coefficient interpolant would force
`F(p*t)=F(t)`, which fails in the small actual-CM analogues.  The correction
is recorded in:

```text
p24/centered_marginal_resultant_factor_boundary.md
p24/centered_marginal_resultant_factor_audit.py
```

The seven factors are still base-field valued because the values `F(t)` are
base-field values.  The missing arithmetic theorem is that none of these
orbit products vanishes modulo the selected p24 prime.

The finite implication from these seven p-unit checks to the selected
centered-profile rank certificate is Lean-checked in:

```text
p24/lean/CenteredArcProductGate.lean
```

## Exterior Character Expansion

There is an exact right-character expansion of `F(t)`.  If `P_b in F_p^156`
are the centered marginal point columns and

```text
P_b = sum_s Q_s zeta_211^(s*b),
```

then Cauchy-Binet gives:

```text
F(t) =
  sum_{S subset {1,...,210}, |S|=156}
    det(Q_s)_{s in S}
    det(zeta_211^(s*i)-1)_{s in S, 1<=i<=156}
    zeta_211^(t * sum_{s in S} s).
```

This attaches the seven orbit products to an exterior character polynomial.
However, the p24 expansion has

```text
binom(210,156) ~= 10^50.79
```

subset terms before cancellations.  The small actual-CM audit in:

```text
p24/centered_marginal_exterior_dft_audit.py
p24/centered_marginal_exterior_dft_boundary.md
```

verified the formula exactly but found full term and frequency support in the
tested rows.  Thus the exterior-DFT form is useful theorem language, not yet a
compressed evaluator or proof of nonvanishing.

## Character-Support Boundary

The exterior representation does not have small cyclic character support.
For the right zero-sum representation `U_211`, the determinant lives in:

```text
wedge^156 U_211.
```

The possible cyclic characters are 156-fold distinct subset sums of
`F_211^*`.  By the Dias da Silva-Hamidoune theorem, these subset sums cover
all of `F_211`.  Thus a proof cannot come merely from small Fourier support;
full cyclic support is available before using CM arithmetic.

This is consistent with the small actual-CM sequence-complexity checks in:

```text
p24/centered_marginal_alpha_sequence_complexity.md
```

which found full Berlekamp-Massey complexity in the first nontrivial rows.

Nor is the underlying row space a cyclic code in the tested analogues.  See:

```text
p24/centered_marginal_cyclic_code_boundary.md
p24/centered_marginal_cyclic_code_boundary.py
```

The cyclic object is the determinant sequence/resultant, not an invariant
linear code to which BCH/MDS theorems apply directly.

The dual obstruction is a long plateau condition.  A factor `F(t)` vanishes
if and only if some nonzero dual trace word is constant on the 157 positions
`t,...,t+156`.  Plain prime cyclic uncertainty does not rule this out; see:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
p24/plateau_uncertainty_boundary_toy.py
```

The plateau condition is also a complementary Schubert transversality event:

```text
centered ambient H={w_0=0}: dim H = 210,
row dimension = 156,
centered plateau subspace dimension = 211 - 157 = 54,
156 + 54 = 210.
```

The random-Grassmannian failure probability is about `211/p`, but this is
only a calibration until it is lifted to an arithmetic p-unit theorem for the
actual CM row space:

```text
p24/centered_marginal_transversality_boundary.md
p24/centered_marginal_transversality_baseline.py
```

## Current Missing Theorem

The current p24 theorem can be stated as:

```text
For the actual embedded p24 centered Hermitian marginal, the cyclic resultant

    Res_Y(Y^211 - 1, f_C(Y))

is nonzero modulo p=10^24+7.
```

Equivalently, none of the seven Frobenius-orbit products above vanishes.  A
proof of this statement gives `Pi_C,right != 0`, hence
`Delta_C_leading != 0`, hence the mixed rank certificate, all with a verifier
whose formal scale is governed by the 211 right translations and six
size-35 orbit products rather than by `sqrt(p)` or the full class set.
