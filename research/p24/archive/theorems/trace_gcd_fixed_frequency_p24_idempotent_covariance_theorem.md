# Fixed-Frequency p24 Idempotent Covariance Theorem Target

Date: 2026-06-06

## Point

After the complete-factor descent gate, the missing theorem can be stated
without ambiguity.  It is not:

```text
one tensor factor vanishes;
one 7-cycle vanishes;
semilinear covariance alone.
```

It is a complete, Gauss-normalized idempotent covariance theorem for the
70-factor scalar extension of the original `L`-valued fixed-frequency
projection.

## Setup

Let

```text
E = F_p(mu_66254)
L = F_p(mu_157)
rho = Frob_p^780
Gamma = (Z/211Z)^*
H = <2^7>, |H|=30
Gamma/H ~= C_7
```

For p24:

```text
rho fixes L, because p^780 = 1 mod 157;
rho has order 7 on E, because ord_m(p)=5460 and 5460/780=7;
rho shifts the right H-quotient by 6 mod 7;
rho shifts the 70 E-tensor factors by +10 mod 70.
```

Let `e_delta`, `delta in Z/70Z`, be the E-tensor idempotents for the relative
packet.  The factor shift is:

```text
rho(e_delta) = e_{delta+10}.
```

For a nontrivial order-7 quotient character `chi`, write

```text
lambda_chi = chi(p^780 mod 211).
```

Since the right quotient shift is `6 mod 7`, `lambda_chi != 1` for all six
nontrivial `chi`.

## The Required Arithmetic Identity

Define the Gauss-normalized trace-term factor contributions before complete
recombination:

```text
Z_delta,a(chi)
  = e_delta * tau(chi)^(-1) * T_{1,0,a} R_{chi,-a}.
```

Here `tau(chi)` is the right Gauss sum relating the additive resolvent to the
multiplicative `L`-projection.  The theorem to prove is a noncircular
covariance identity on these trace-term contributions, before using descent:

```text
rho(Z_delta,a(chi)) = lambda_chi^(-1) Z_{delta+10,rho*a}(chi)
```

or the same formula with the inverse convention reversed, depending on whether
the right quotient character is placed on source or target labels.  The
important invariant is that the multiplier is nontrivial for every nontrivial
`chi`.

Do not use the same statement without the `tau(chi)^(-1)` normalization.
Formal Frobenius covariance of the unnormalized additive resolvent gives the
same nontrivial eigenvalue on `tau(chi)`, so the divided `L`-projection can
remain nonzero.

Also do not define `Z_delta(chi)=e_delta*S_chi` after proving
`S_chi in L` and then try to prove nontrivial covariance.  After descent,
formal idempotent action gives eigenvalue `1`; nontrivial covariance is then
equivalent to `S_chi=0`.  The useful theorem must act on the CM trace terms
before the complete sum is recombined.

## Formal Consequence

Complete recombination gives

```text
S_chi = sum_delta sum_a Z_delta,a(chi)
```

and this is exactly the original fixed-frequency projection, hence
`S_chi in L`.  Therefore:

```text
rho(S_chi) = S_chi.
```

Summing the covariance identity over all `delta` gives:

```text
rho(S_chi) = lambda_chi^(-1) S_chi.
```

Since `lambda_chi != 1`,

```text
S_chi = 0.
```

This proves all six nontrivial order-7 character projections vanish.  Together
with ordinary centering for the trivial character, this is the H-coset
identity:

```text
C P_H = 0
```

or equivalently the 1092 p24 scalar equations.

## Proof Obligations Left

The remaining arithmetic work is now exactly:

```text
1. construct the idempotents e_delta intrinsically in the embedded
   E tensor relative-packet algebra;
2. identify the complete recombination with the original L-valued projection;
3. prove rho(e_delta)=e_{delta+10};
4. prove the trace-resolvent factor contributions transform with the
   right quotient multiplier lambda_chi^(-1) after Gauss normalization.
```

Items 2 and 3 are standard scalar-extension/idempotent bookkeeping once the
embedded packet algebra is fixed.  Item 4 is the actual CM/Lang equivariance
identity.  The unnormalized version of item 4 is formal and insufficient, and
the post-recombination version is circular.

## Checked Finite Gates

```text
p24/trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate.py
p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.py
p24/trace_gcd_fixed_frequency_p24_complete_factor_descent_gate.py
p24/trace_gcd_fixed_frequency_p24_gauss_normalization_boundary.py
p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary.py
p24/lean/TraceGcdSemilinearEigenDescentGate.lean
```

These gates show:

```text
scalar factor-cycle cancellation is only a shadow;
semilinear covariance alone can be nonzero;
complete recombination plus descent is the needed input;
formal additive covariance is only the Gauss-sum eigenvalue;
post-descent nontrivial idempotent covariance is circular;
fixed plus nontrivial rho-eigenvalue formally forces zero.
```
