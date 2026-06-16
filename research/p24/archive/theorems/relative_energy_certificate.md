# Relative Energy Certificate

This note records a weaker scalar certificate that may be more approachable
than a full content/Bezout certificate.

## Definition

Keep the notation

```text
h = m n,       H=<sigma^m>,
P_u(a)=sum_k zeta_n^(a k) j_{u+m k}.
```

For a nontrivial relative character `a`, define the quadratic energy

```text
E_a = sum_{u=0}^{m-1} P_u(a) P_u(-a).
```

If all `P_u(a)` vanish, then certainly

```text
E_a = 0.
```

Therefore

```text
E_a != 0
```

is a sufficient certificate that the harmful dual coset for `a` does not
vanish.  It is weaker than product nonvanishing and weaker than a content
certificate, but it is only one scalar per Frobenius orbit.

## Autocorrelation Form

Expanding and setting `d=k-l` gives

```text
E_a = sum_{d mod n} zeta_n^(a d) C_d,
```

where

```text
C_d = sum_{i=0}^{h-1} j_{i+m d} j_i.
```

So `E_a` is the relative character transform of the autocorrelation of the
CM cycle along the recovery subgroup.  In class-field terms,

```text
Tr_{L E/E}(Theta_a Theta_-a) = n E_a.
```

This is useful because it turns the exact harmful event into a possible
nonvanishing problem for a toric second moment rather than a vector of
`66254` relative periods.

## Parseval Packet Form

The full dual-coset resolvents are

```text
R_{a+r n} = sum_u zeta_h^(a u) zeta_m^(r u) P_u(a).
```

Fourier orthogonality over the quotient gives

```text
sum_{r=0}^{m-1} R_{a+r n} R_{-a-r n} = m E_a.
```

This is not the false coordinate-product identity.  It is an additive
Parseval identity: the scalar energy is the paired spectral mass of the full
dual coset.  Thus `E_a != 0` rules out harmful vanishing, but `E_a = 0` only
says that this paired spectral mass cancels.

## Why This Is A Real, But Not Yet Solved, Route

For p24 third trace, a complete energy certificate would require eight scalar
nonvanishing checks, one for each nontrivial Frobenius orbit of relative
`H`-characters:

```text
n = 3107441,
ord_n(p) = 388430,
(n-1)/ord_n(p) = 8.
```

Because `C_d=C_-d`, the energy satisfies `E_a=E_-a`.  For p24,

```text
p^(388430/2) == -1 mod n.
```

Therefore each scalar energy packet lies in the real cyclotomic subfield of
degree

```text
194215
```

instead of the full relative-content packet degree `388430`.  The number of
packets remains eight, because `-a` is already in the same Frobenius orbit of
`a`.

This degree accounting is recorded in:

```text
p24/energy_real_cyclotomic_packet_audit.py
```

The scalar nature is attractive: second moments and autocorrelations are the
kind of objects that sometimes admit trace formulas, relative trace formulas,
or `p`-adic unit criteria.

There is now a characteristic-zero dominance audit for the ordinary scalar:

```text
p24/ordinary_energy_principal_dominance_audit.py
```

For the p24 third trace, `C_0` contains the unique principal-square term
`j_0^2`.  Every `d != 0` autocorrelation has at most one principal factor, and
every other singular modulus has reduced-form denominator at least `2`.  The
audit reports:

```text
log_principal_square=1.015340e13
log_one_principal_bound=7.615049e12
log_nonprincipal_bound=5.076699e12
dominance_margin=2.538350e12
dominance_margin_over_log_p=4.593297e10
```

Thus ordinary energy is also nonzero in characteristic zero by a huge margin.
Its failure mode is selected-prime divisibility/cancellation after reduction,
not complex cancellation.

The obstruction is also clear.  The autocorrelation values `C_d` are traces
over CM pairs related by the class `(sigma^m)^d`.  For `d=1`, this is already
the oriented composite correspondence

```text
2 * 463 * 223^(-1)
```

of norm `206498`; for general `d`, it ranges over the entire order-`3107441`
subgroup.  Thus a direct computation of all `C_d`, or of their high-order
character transform, is still the missing non-genus period computation in
second-moment form.

## Certificate Hierarchy

```text
content/Bezout:
  exact, vector-valued, strongest target for finite-field verification;

product:
  sufficient, rules out even one zero quotient fiber;

energy:
  sufficient, scalar, can survive individual zero fibers but may cancel;

harmful:
  all P_u(a) vanish.
```

The energy target is worth keeping because it is the first reduction from the
exact vector condition to eight scalar nonvanishing statements without asking
for every quotient fiber to be nonzero.

## Gram-Isotropy Boundary

There is a useful but limiting identity:

```text
C(X) = sum_u J_u(X) J_u(X^-1)
```

in `F_p[X]/(X^n-1)`, where

```text
J_u(X)=sum_k j_{u+m*k} X^k.
```

Thus the energy packet is the Hermitian Gram scalar of the relative-content
packet vector.  This proves only the one-way implication:

```text
all J_u == 0 mod f_a  =>  C == 0 mod f_a.
```

The converse is false by finite-field linear algebra.  The toy

```text
p24/energy_isotropy_obstruction_toy.py
```

uses the same quadratic packet field as the `D=-5000` calibration and finds a
nonzero vector `(1,y)` with zero Hermitian energy.  So content nonzero does
not imply energy nonzero.  Any p24 proof of energy nonvanishing must use the
specific CM/autocorrelation origin of `C(X)`, not just the fact that the
content vector is nonzero.
