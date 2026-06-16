# Lang Trace-GCD Pluecker Spectral Boundary

Date: 2026-06-05

This note gives the finite spectral identity for the reduced right-origin
trace-gcd determinant.

## Setup

After origin covariance, the selected tail determinant has the form:

```text
Delta(t) = det(P V_t A),        t mod d.
```

Here:

```text
d = 211             for p24,
V_t                = right multiplication by zeta_d^t,
A: K -> R          = transported tail map from the prefix kernel,
P: R -> F_p^k      = selected k-coordinate Lang/trace-dual window,
k = 16             for p24.
```

After extending scalars to a splitting field, choose the eigenbasis
`e_v` for one right Frobenius orbit `O`.  Then:

```text
V_t e_v = zeta_d^(t v) e_v.
```

## Pluecker Expansion

Cauchy-Binet gives:

```text
Delta(t)
  = sum_{I subset O, |I|=k}
      det(P_I) det(A_I) zeta_d^(t * sum_{v in I} v).
```

Grouping terms by the subset-sum exponent `s mod d` gives the Fourier
polynomial over the right splitting field:

```text
f(Y) = sum_{s mod d} c_s Y^s,

c_s =
  sum_{I subset O, |I|=k, sum(I)=s}
    det(P_I) det(A_I).
```

Then:

```text
Delta(t) = f(zeta_d^t),
```

and the origin-product certificate is exactly:

```text
prod_{t mod d} Delta(t)
  = Res_Y(Y^d - 1, f(Y)) != 0 mod p.
```

This is the cleanest finite identity for the remaining p-unit theorem.
The coefficients need not lie in `F_p` individually.  What is base-field
valued are the determinant values `Delta(t)` and the Frobenius-orbit products
of those values.

## Toy Verification

Added:

```text
p24/lang_trace_gcd_plucker_spectral_toy.py
```

The small trace-gcd analogue:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/lang_trace_gcd_plucker_spectral_toy.py \
  --field-q 337 --right 7 --orbit-generator 2 --k 2 --trials 50
```

reported:

```text
orbit=[1,2,4]
possible_support_size=3
possible_support=[3,5,6]
actual_support_size_min=3
actual_support_size_max=3
cauchy_binet_mismatches=0
```

So the degree-3 recurrence seen in the actual `(4,7)` trace-gcd row is
compatible with the exterior square of a degree-3 right orbit.

A slightly larger generic analogue:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/lang_trace_gcd_plucker_spectral_toy.py \
  --field-q 2113 --right 11 --orbit-generator 3 --k 3 --trials 30
```

reported:

```text
orbit=[1,3,9,5,4]
possible_support_size=10
possible_support=[1,2,3,4,5,6,7,8,9,10]
actual_support_size_min=10
actual_support_size_max=10
cauchy_binet_mismatches=0
```

Thus generic Pluecker data fills the allowed subset-sum support.

## p24 Consequence

For p24:

```text
O = <p> in (Z/211Z)^*,     |O|=35,
k = 16.
```

The subset-sum support of `wedge^16 O` is all of `Z/211Z`; see:

```text
p24/lang_trace_gcd_exterior_support.py
```

The fixed coefficients `det(P_I)` for the selected first-16 Lang coordinates
are p-units by the Vandermonde theorem in:

```text
p24/trace_gcd_fourier_minor_unit_theorem.md
p24/trace_gcd_cm_plucker_fitting_norm_frontier.md
```

So the p24 obstruction is not loss of fixed Fourier support.  It is the
noncancellation and p-unitness of the actual CM side:

```text
sum_{I, sum(I)=s} det(P_I) det(A_I),
```

or the equivalent crossed-product/Fitting norm.

Therefore a single-degree-35 support theorem would require many nontrivial
Pluecker cancellations:

```text
c_s = 0 for all s outside one Frobenius orbit.
```

That is not forced by the right action.  It would have to come from the
special arithmetic relation between:

```text
K = common prefix trace kernel,
A = T_i | K,
P = first 16 Lang coordinates.
```

## Current Proof Options

The remaining p24 theorem can now be stated in two nested forms:

```text
strong/spectral-collapse:
  c_s is supported in one degree-35 Frobenius orbit and
  prod_t f(zeta_211^t) != 0;

direct/resultant:
  Res(Y^211 - 1, f(Y)) != 0 mod p.
```

The direct statement is exactly equivalent to the origin-product certificate.
The spectral-collapse statement would make the product look like a smaller
Gauss-period norm, but it is an additional arithmetic theorem.

Finite-field uncertainty or generic MDS/superregularity does not prove the
selected-prime p-unit.  Those tools can show that zeros are unlikely, or that
random matrices usually pass, but the certificate needs the actual resultant
for the embedded CM trace-gcd Pluecker data to be nonzero modulo
`p=10^24+7`.

The finite verifier shape for this resultant target is recorded in:

```text
p24/lang_trace_gcd_resultant_certificate_spec.md
p24/lang_trace_gcd_resultant_certificate_toy.py
```

Because the raw determinant values need not be Frobenius-compatible, the
honest verifier object is a base-value list/inverse list or seven orbit
products, unless a split-algebra coefficient representation of `f` is also
supplied.
