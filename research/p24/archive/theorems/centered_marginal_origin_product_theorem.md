# Centered Marginal Origin-Product Theorem Candidate

Date: 2026-06-05

This note packages the leading centered-marginal minor into an origin-stable
product.

## Origin Action

For `h=m*n`, write an origin shift as:

```text
shift == n*alpha + m*beta mod h.
```

The packet fibers transform as:

```text
F'_r(X) = X^(-beta) F_{r+alpha}(X).
```

For the Hermitian packet pairing, the common monomial factor cancels:

```text
<X^(-beta) A, X^(-beta) B>_H = <A,B>_H.
```

Thus the centered marginal leading minor is independent of `beta`; it varies
only with the CRT-axis translation `alpha`.

## Product

For a fixed packet and fixed component pair `(c,d)`, define:

```text
Delta_C(alpha) =
  det(C_alpha(r,s))_{1 <= r <= c-1, 1 <= s <= c-1},
```

where `C_alpha` is the centered marginal after translating the residue origin
by `alpha`.  The origin-stable package is:

```text
Pi_C = prod_{alpha mod m} Delta_C(alpha).
```

Then:

```text
Pi_C != 0
  => every alpha-origin leading minor is nonzero
  => the selected embedded origin's Delta_C_leading is nonzero.
```

For p24, the target pair is `(c,d)=(157,211)`, so the corresponding product
has `m=66254` factors.  This is much smaller than the class set and far below
sqrt(p), but it is still an arithmetic p-unit theorem unless the product can
be evaluated or proved nonzero by a class-field identity.

## Audit

Added:

```text
p24/centered_marginal_origin_product_audit.py
```

Small actual-CM rows:

```text
D=-6719, q=6863, m=21, n=5, pair=(3,7):
  alpha_count=21
  alpha_zero_count=0
  alpha_distinct_count=7
  alpha_product=1042
  beta_distinct_histogram={1: 21}
  beta_mismatch_count=0.

D=-13319, q=13463, m=28, n=5, pair=(4,7):
  alpha_count=28
  alpha_zero_count=0
  alpha_distinct_count=14
  alpha_product=3636
  beta_distinct_histogram={1: 28}
  beta_mismatch_count=0.

D=-10919, q=11243, m=12, n=13, pair=(4,4):
  alpha_count=12
  alpha_zero_count=0
  alpha_distinct_count=1
  alpha_product=11026
  beta_distinct_histogram={1: 12}
  beta_mismatch_count=0.
```

The beta cancellation is exact in these rows, as predicted by the Hermitian
origin action.  The alpha values can vary in asymmetric mixed pairs, so the
right invariant is the product `Pi_C`, not necessarily one determinant value.

## Current Status

The product route gives a better p-unit target than a single coordinate
minor:

```text
prove Pi_C is a p-unit,
or prove every factor Delta_C(alpha) is a p-unit.
```

It does not by itself solve the p24 theorem.  The next missing identity is a
class-field norm or divisor formula for `Pi_C`, or a proof that the alpha
orbit avoids the exterior trace-form incidence divisor modulo
`p=10^24+7`.

## Alpha Reduction

The alpha action splits into a left basis determinant and a right translated
window.  Translation by `alpha` on the left component changes

```text
L_1 wedge ... wedge L_{c-1}
```

by the determinant of translation on the zero-sum hyperplane of
`F[Z/cZ]`.  This determinant is:

```text
epsilon_c(alpha) = (-1)^(c - gcd(c,alpha)).
```

After dividing by `epsilon_c(alpha)`, the determinant depends only on
`alpha mod d`.

The audit checks this by reporting:

```text
left_sign_normalized_right_mismatches=0.
```

In the rows above this held for `(3,7)`, `(4,7)`, and `(4,4)`.

## p24 Consequence

For the p24 mixed block:

```text
c = 157, d = 211, m = 66254 = 2*157*211.
```

Since `157` is odd prime,

```text
epsilon_157(alpha)=1
```

for every `alpha`.  Therefore:

```text
Delta_C(alpha) = F(alpha mod 211)
```

for a 211-term cyclic right-window sequence, and:

```text
Pi_C = prod_{alpha mod 66254} Delta_C(alpha)
     = (prod_{t mod 211} F(t))^314.
```

Thus the origin-product theorem can be reduced to a **211-factor** p-unit
target:

```text
Pi_C,right = prod_{t mod 211} F(t) != 0 mod p.
```

Equivalently, all 211 cyclic right translates of the leading
`156 x 156` centered marginal minor are nonzero.  This is now the most compact
coordinate-minor p-unit package attached to `Delta_C_leading`.

This 211-factor product can also be written as a cyclic resultant over
`F_p(mu_211)`.  If `f_C(Y)` is the degree `<211` interpolant of the
right-translation sequence,
then:

```text
Pi_C,right = prod_{t mod 211} F(t)
           = Res_Y(Y^211 - 1, f_C(Y)).
```

Because `ord_211(p)=35`, the 211 values split into `{0}` and six nonzero
Frobenius orbits of size `35`.  This gives seven base-field orbit-product
factors.  These are not presently norms of a base-coefficient interpolant; see:

```text
p24/centered_marginal_cyclic_resultant_theorem.md
```

The same origin covariance gives the full-origin power bridge:

```text
prod_{all origins} Delta_origin
  = p-unit * Pi_C,right^(n*m/211).
```

For p24 the exponent is:

```text
n*m/211 = 975736474.
```

This is recorded and audited in:

```text
p24/centered_marginal_origin_norm_power_theorem.md
p24/centered_marginal_origin_norm_power_audit.py
```

## Sequence Complexity

The reduced right-translation sequence is not visibly low-recurrence in small
actual-CM rows.  See:

```text
p24/centered_marginal_alpha_sequence_complexity.py
p24/centered_marginal_alpha_sequence_complexity.md
```

The tested lengths `7`, `7`, and `13` all had full Berlekamp-Massey
complexity.  Thus the 211-factor p24 product should be regarded as a
full-support cyclic exterior product unless a new CM-adapted coordinate
system is found.
