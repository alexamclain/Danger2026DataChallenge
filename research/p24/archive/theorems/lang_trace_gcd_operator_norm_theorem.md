# Lang Trace-GCD Operator-Norm Theorem

Date: 2026-06-05

This note records the single-operator form of the trace-GCD origin resultant.

## Setup

After origin covariance, the representative tail determinant has the form:

```text
Delta(t) = det(P V_t A),        t mod d.
```

For p24:

```text
d = 211,
k = 16,
V_t = right multiplication by zeta_211^t,
A = T_i|K_0,       K_0 = common kernel of the four prefix trace blocks,
P = selected first-16 Lang/trace-dual coordinate projection.
```

Over a splitting field for `Y^d-1`, diagonalize:

```text
V_t e_v = zeta_d^(t v) e_v.
```

Equivalently, let `E_v` be the spectral idempotent for `e_v` and define the
universal right-origin operator:

```text
Q = F[Y]/(Y^d - 1),
V_univ = sum_v E_v Y^v in End(R) tensor Q.
```

Then:

```text
M(Y) = P V_univ A : K_Q -> Q^k,
f(Y) = det_Q M(Y).
```

Then Cauchy-Binet gives the Pluecker-Fourier polynomial:

```text
f(Y) =
  sum_{I subset O, |I|=k}
    det(P_I) det(A_I) Y^(sum_{v in I} v),
```

with exponents reduced modulo `d`, and:

```text
Delta(t) = f(zeta_d^t).
```

## Operator Norm Identity

Let:

```text
B = F[Y]/(Y^d - 1),
m_f: B -> B,   g |-> f*g.
```

Then:

```text
det_F(m_f)
  = Res_Y(Y^d - 1, f(Y))
  = prod_{t mod d} f(zeta_d^t)
  = prod_{t mod d} Delta(t).
```

Thus the trace-GCD origin product is the norm of one element:

```text
Norm_{B/F}(f mod (Y^d-1)).
```

Equivalently, the desired p24 theorem can be stated as:

```text
f is a unit in the p-integral cyclic algebra
  O_F[Y]/(Y^211 - 1)
```

for the actual CM Pluecker-Fourier element `f`.

## Proof

The equality `Delta(t)=f(zeta_d^t)` is Cauchy-Binet on:

```text
P diag(Y^v) A.
```

In universal-operator language, evaluation:

```text
Q -> F,   Y |-> zeta_d^t
```

sends `V_univ` to `V_t`, hence sends:

```text
det_Q(P V_univ A)
```

to:

```text
det(P V_t A).
```

The determinant of multiplication by `f` in `F[Y]/(Y^d-1)` is the resultant
of `f` with `Y^d-1`.  After splitting `Y^d-1`, multiplication by `f` is
diagonal in the idempotent basis, with eigenvalues:

```text
f(zeta_d^t),    t mod d.
```

Multiplying those eigenvalues gives the product of the trace-GCD
determinants.

## Toy Verification

Added:

```text
p24/lang_trace_gcd_operator_norm_toy.py
```

The right-7 analogue:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_operator_norm_toy.py \
  --field-q 337 --right 7 --orbit-generator 2 --k 2 --trials 50
```

reported:

```text
support_size_min=3
support_size_max=3
zero_product_count=3
identity_mismatches=0
```

The right-11 analogue:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_operator_norm_toy.py \
  --field-q 2113 --right 11 --orbit-generator 3 --k 3 --trials 30
```

reported:

```text
support_size_min=10
support_size_max=10
zero_product_count=0
identity_mismatches=0
```

The identity is finite algebra; the zero counts are random-toy diagnostics
only.

## What This Buys

The p24 proof target can now be phrased in three exactly equivalent ways:

```text
value form:
  Delta(t) != 0 for all t mod 211;

resultant form:
  Res_Y(Y^211 - 1, f(Y)) is a p-unit;

operator form:
  multiplication by f is an automorphism of
  O_F[Y]/(Y^211 - 1) after reduction at p.
```

The operator form is the best producer-facing language, because it separates
the finite verifier from the arithmetic construction.  A class-field proof
does not need to list `211` determinants if it can construct the integral
element:

```text
f = det(P diag(Y^v) A)
```

or equivalently:

```text
f = det_Q(P V_univ A),
```

or the multiplication operator `m_f`, and prove it is a p-local unit.

## What This Does Not Buy

This does not by itself produce `f`.  The Pluecker expression still contains:

```text
binom(35,16)
```

terms before grouping by exponents.  For p24 the possible exponent support is
all of `Z/211Z`, so generic support or recurrence arguments do not finish the
proof.

The missing arithmetic theorem is now:

```text
Construct the actual p-integral CM element
  f_trace in O_F[Y]/(Y^211 - 1)
attached to the transported trace-GCD tail map, and prove
  f_trace in (O_F[Y]/(Y^211 - 1))^*
at the selected prime over p = 10^24 + 7.
```

This is a smaller and more explicit analogue of the trace-frame Fitting-unit
theorem.  It is the current preferred producer theorem for the mixed
representative route.

The p-integrality conditions needed to interpret this as a p-unit theorem are
recorded in:

```text
p24/lang_trace_gcd_integrality_lift.md
```

The equivalent Grassmannian/local-intersection form is recorded in:

```text
p24/lang_trace_gcd_schubert_orbit_theorem.md
```

The boundary for a Borcherds/local-intersection proof of this operator norm is:

```text
p24/trace_gcd_borcherds_literature_boundary.md
```
