# Fixed-Frequency p24 Covariance-Plus-Descent Theorem Target

Date: 2026-06-06

## Statement Shape

For each nontrivial order-7 quotient character `chi`, let

```text
S_chi = sum_a T_{1,0,a} R_{chi,-a}
```

be the class-character packet product sum for the fixed-frequency H-coset
projection.  The target theorem is:

```text
S_chi = 0 for all six nontrivial chi.
```

The p24-specific route should prove this as:

```text
1. Descent:
   S_chi lies in L = F_p(mu_157), hence is fixed by rho = p^780.

2. Semilinear covariance:
   under rho, the 70 E-factor contributions split into ten 7-cycles and
   transform with nontrivial eigenvalue lambda_chi^(-1):

       rho(S_chi) = lambda_chi^(-1) S_chi.

3. Nontrivial intersection:
   lambda_chi != 1, so the rho-fixed subspace intersects the
   lambda_chi^(-1)-eigenspace only in zero.
```

Then `S_chi=0`, giving `C P_H=0` and the 1092 H-coset scalar equations.

## Why This Is Sharper

The earlier scalar factor-cycle toy suggested geometric cancellation on each
7-cycle.  That is only a scalar shadow.  In the actual tower, `rho` acts
semilinearly on `E`, so a twisted 7-cycle sum can be nonzero.  The finite
semilinear gate shows this boundary explicitly:

```text
semilinear_covariance_alone_does_not_force_zero=1
twisted_projection_ranks=[1, 1, 1, 1, 1, 1]
twisted_fixed_intersection_dimensions=[0, 0, 0, 0, 0, 0]
```

So the proof must not stop at factor-cycle covariance.  It must identify the
factor-cycle sum with the descended `L`-valued fixed-frequency projection.

The descent input is specifically complete recombination:

```text
S_chi = sum_{delta=0}^{69} Z_delta(chi)
```

over the 70 E-tensor idempotents.  A representative factor, or even a single
7-cycle of factors, can satisfy the same covariance while remaining nonzero
and non-descended.  The complete-factor gate records this boundary.

The covariance must also be Gauss-normalized.  The unnormalized additive
resolvent has formal Frobenius covariance, but the same eigenvalue is carried
by `tau(chi)`.  After division by `tau(chi)`, the `L`-valued projection is
fixed and can be nonzero.  Therefore the remaining theorem is not the formal
additive covariance; it is an extra CM/Lang identity for the normalized
70-idempotent packet contribution.

There is one more noncircularity condition.  If one first recombines to
`S_chi in L`, then the idempotent components of `S_chi` have trivial
rho-eigenvalue.  A nontrivial idempotent covariance after that step is
equivalent to the desired vanishing.  Therefore the covariance must be proved
on the Gauss-normalized trace-resolvent summands before complete
recombination/descent.

## p24 Numerology Used

```text
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
rho = p^780
rho_order_on_E = 7
rho fixes mu_157
rho shifts the right H-quotient by 6 mod 7
rho shifts the 70 E-factors by 10 mod 70
```

The shift by `10` gives ten cycles of length `7`.

## Formal Finite Core

The pure logical implication is Lean-checked in:

```text
p24/lean/TraceGcdSemilinearEigenDescentGate.lean
p24/trace_gcd_fixed_frequency_p24_complete_factor_descent_gate.py
p24/trace_gcd_fixed_frequency_p24_gauss_normalization_boundary.py
p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary.py
```

It formalizes:

```text
fixed by rho + nontrivial rho-eigenvalue => zero.
```

The arithmetic theorem still missing is the construction of `S_chi` in the
actual CM/Lang tower by first proving Gauss-normalized covariance on the
trace-resolvent summands, then applying complete 70-factor recombination and
descent, without enumerating the class set.
