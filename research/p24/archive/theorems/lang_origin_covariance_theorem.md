# Lang Origin-Covariance Theorem

Date: 2026-06-05

This note records the finite algebra behind the trace-gcd origin action.  It
separates the part that is now proved by the coordinate model from the
remaining arithmetic p-unit theorem.

## Marginal Action

For `h=m*n` and an origin shift

```text
shift == n*alpha + m*beta mod h,
```

the complement fibers transform as:

```text
F'_r(X) = X^(-beta) F_{r+alpha}(X).
```

For the Hermitian packet factor,

```text
<X^(-beta)A, X^(-beta)B>_H = <A,B>_H,
```

so beta cancels in the Hermitian kernel.  The double marginal therefore has
the exact action:

```text
M'_{c,d}(a,b) = M_{c,d}(a+alpha, b+alpha).
```

## DFT Action

Let `zeta` have order `m`, `step_c=m/c`, and `step_d=m/d`.  The nonzero
mixed DFT coordinates are:

```text
H(u,v) = sum_{a,b} zeta^(u*step_c*a + v*step_d*b) M(a,b).
```

The translated marginal satisfies:

```text
H'(u,v)
  = zeta^(-alpha*(u*step_c + v*step_d)) H(u,v).
```

For one left Frobenius orbit with representative `u0`, this is a common
nonzero left phase:

```text
eta_alpha = zeta^(-alpha*u0*step_c),
```

times a right-orbit phase:

```text
gamma_alpha(v) = zeta^(-alpha*v*step_d).
```

## Lang Action

On a right Frobenius orbit

```text
O = {v0, q*v0, ..., q^(r-1)*v0},
```

the phase vector is:

```text
gamma_alpha(q^i v0) = gamma_alpha(v0)^(q^i).
```

Let `U=(sigma^i b_j)` be the Moore matrix used by the Lang inverse, with
`b_j` an `F_q`-basis of the right cyclotomic subfield.  Multiplication by
`gamma=gamma_alpha(v0)` gives an `F_q`-linear matrix `C_gamma` on this basis:

```text
gamma*b_j = sum_k b_k C_gamma(k,j).
```

Therefore the Lang-trivialized right block transforms as:

```text
W'_O = eta_alpha * C_gamma * W_O.
```

This is an exact finite algebra statement.  In particular:

```text
beta has no effect on the transformed blocks;
alpha mod c contributes only the common left unit eta_alpha;
alpha mod d applies invertible right-component matrices C_gamma.
```

Thus zero/nonzero status of the trace-gcd determinant is invariant under
beta and under the left-component unit action.  The real selected-window
motion is the right-component alpha action.

## Trace-Map Transport

In the trace-gcd formulation, let:

```text
T_j(lambda) = Tr_{E/R_j}(lambda*S_j),
```

where `j` is a right Frobenius orbit and `lambda in L`.  The covariance above
can be stated as:

```text
T_j^(alpha,beta)
  = V_{j,t} o T_j o U_alpha,        t = alpha mod d.
```

Here:

```text
U_alpha: L -> L
```

is multiplication by the nonzero left phase, and:

```text
V_{j,t}: R_j -> R_j
```

is the invertible right-orbit multiplication/Lang basis map.  Therefore, for
a full-prefix set `B`,

```text
K_(alpha,beta)
  = intersection_{j in B} ker T_j^(alpha,beta)
  = U_alpha^(-1) K_0.
```

After transporting `K_(alpha,beta)` back to `K_0`, the selected tail map is:

```text
P_i C_i V_{i,t} T_i | K_0,
```

where `P_i` is the first-window projection in the selected Lang coordinates
and `C_i` records the fixed trace-dual/Lang coordinate convention.  Thus the
intrinsic determinant satisfies:

```text
Delta_i(alpha,beta)
  = unit(alpha,beta) * Delta_i(alpha mod d).
```

For the p24 certificate only p-unit status is needed, so this unit ambiguity
is harmless.

## Toy Verification

Added:

```text
p24/lang_origin_covariance_toy.py
```

It checks the formula above on random marginal tables, independent of CM data.
Pinned runs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_origin_covariance_toy.py --q 5 --left 3 --right 7

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_origin_covariance_toy.py --q 2 --left 3 --right 5

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_origin_covariance_toy.py --q 3 --left 5 --right 7
```

Each reported:

```text
mismatches=0 for every alpha
conclusion=origin_covariance_formula_verified
```

## p24 Product Gate

For p24, `c=157`, `d=211`, and:

```text
m = 66254 = 2*157*211.
```

The covariance theorem reduces the origin-stable product target to the
right-component sequence:

```text
Pi_trace,i = prod_{t mod 211} Delta_i(t) != 0 mod p.
```

The finite implication is now:

```text
Pi_trace,i != 0
  => Delta_i(t) != 0 for every right translate t
  => selected representative trace-gcd determinant is nonzero.
```

The formal gate for this implication is:

```text
p24/lean/TraceOriginProductGate.lean
```

The concrete finite certificate form is recorded in:

```text
p24/lang_trace_gcd_resultant_certificate_spec.md
```

It can be checked by a 211-value/inverse certificate, or by seven right
Frobenius orbit products, once the actual determinant values are supplied.

The first sequence-complexity audit for the reduced determinant sequence is:

```text
p24/lang_trace_gcd_sequence_complexity.py
p24/lang_trace_gcd_sequence_complexity.md
p24/lang_trace_gcd_plucker_spectral_boundary.md
p24/lang_trace_gcd_plucker_spectral_toy.py
```

On the pinned nontrivial `(4,7)` actual-CM row, each length-7 determinant
sequence has linear complexity `3` and its connection polynomial is one
degree-3 factor of `X^7-1`.  This suggests a sharper p24 possibility:

```text
Delta_i(t) may have support in one degree-35 Frobenius factor of X^211-1.
```

The exact finite expansion is:

```text
Delta_i(t)
  = sum_{I subset O, |I|=16}
      det(P_I) det(A_I) zeta_211^(t * sum(I)).
```

So the product target is the cyclic resultant of this Pluecker-Fourier
polynomial with `Y^211-1`.

Without assuming any spectral collapse, that resultant is the operator norm
of one cyclic-algebra element:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
```

## Remaining Arithmetic Theorem

What remains is not origin covariance.  The missing theorem is:

```text
prod_{t mod 211} Delta_i(t) != 0 mod p,
```

or the stronger pointwise statement:

```text
Delta_i(t) != 0 for every t mod 211.
```

Equivalently, prove the cyclic resultant of the right-translation determinant
sequence is a p-unit.  Since `ord_211(p)=35`, this can be organized as one
fixed translate plus six Frobenius orbit products of length `35`.  This is
the current smallest proof surface for the representative trace-gcd
certificate.  If the single-orbit spectral-support candidate above is true,
the product becomes a Gauss-period norm for one degree-35 component.
