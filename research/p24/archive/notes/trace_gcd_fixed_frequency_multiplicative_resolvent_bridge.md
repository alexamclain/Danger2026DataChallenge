# Fixed-Frequency Multiplicative-Resolvent Bridge

Date: 2026-06-06

## Point

The H-coboundary target has a useful class-field-facing form.  Let

```text
G_s in L = F_p(mu_157),     s in (Z/211Z)^*
```

be the centered right profile.  For a nontrivial order-7 quotient character
`chi` of `(Z/211Z)^*/H`, where `H=<2^7>`, the missing equations are

```text
sum_s chi(s)^(-1) G_s = 0.
```

Equivalently, if

```text
H(1,v) = sum_s zeta_211^(v*s) G_s = <A_1, B_v>,
```

then

```text
sum_v chi(v) H(1,v)
  = <A_1, sum_v chi(v) B_v>
  = tau(chi) * sum_s chi(s)^(-1) G_s.
```

The Gauss sum `tau(chi)` is nonzero.  So the H-coboundary theorem is exactly:

```text
the left additive 157-resolvent A_1 is orthogonal to the six right
multiplicative order-7 resolvents sum_v chi(v)B_v.
```

This is a better proof surface than bare H-coset row sums, because it exposes
the new arithmetic object a tower proof must kill.

## Frobenius Mirage

There is a tempting false proof:

```text
p^156 fixes the left 157-frequency and cycles the seven H-cosets on the
right, so ordinary centering should force all H-coset sums to be zero.
```

The mistake is that the orbit-augmentation value before dividing by the Gauss
sum is not L-valued.  It lives in `L(mu_211)` and has a nontrivial Frobenius
eigenvalue carried by `tau(chi)`.

For p24:

```text
p = 2^198 mod 211,
p^156 mod 211 = 82,
log_2(p^156) = 4 mod 7.
```

The Gauss-sum identity gives

```text
tau(chi)^(p^156) = chi(p^-156) tau(chi).
```

Thus a nonzero L-valued projection

```text
P_chi = sum_s chi(s)^(-1)G_s
```

is compatible with Frobenius covariance:

```text
(tau(chi) P_chi)^(p^156)
  = chi(p^-156) tau(chi) P_chi.
```

The nontrivial eigenvalue does not force `P_chi=0`; it is absorbed by the
Gauss sum.  A proof still needs genuine CM/Lang arithmetic, not just
semilinear covariance plus ordinary centering.

## Check

The finite dictionary and the Frobenius mirage are checked by:

```text
p24/trace_gcd_fixed_frequency_multiplicative_resolvent_bridge.py
```

It verifies:

```text
<A_1, sum_v chi(v)B_v>
  = tau(chi) * sum_s chi(s)^(-1)G_s;

ordinary centering leaves all six multiplicative projections nonzero in a
random control;

forcing H-coset sums to vanish kills all six projections;

p^156 Frobenius twists the Gauss sum by the expected nontrivial eigenvalue,
so a nonzero divided L-projection survives the covariance.
```

## Updated Arithmetic Target

The current theorem should be attacked as:

```text
For the actual p24 mixed Hermitian packet,
<A_1, B_chi> = 0
for every nontrivial order-7 multiplicative quotient character chi on the
right 211-component.
```

This is stronger language than "Gaussian-period row sums vanish" but exactly
equivalent to it.  It points toward a relative Hecke/class-character
orthogonality theorem, not a sparse Fourier shortcut and not a Frobenius-only
argument.
