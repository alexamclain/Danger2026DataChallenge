# Fixed-Frequency H-Kernel Inclusion Gate

Date: 2026-06-06

## Point

The p24 H-coset theorem can be stated as a right-kernel inclusion for the
centered mixed marginal:

```text
C : F_p^{210} -> F_p^{156}.
```

Let `P_H` be the `210 x 7` matrix whose columns are the indicators of the
seven cosets of

```text
H = <2^7> <= (Z/211Z)^*.
```

Then the `1092` scalar equations are exactly:

```text
C P_H = 0.
```

Equivalently, the 7-dimensional Gaussian-period indicator subspace lies in
the right kernel of `C`, or the rowspace of `C` lies in its orthogonal
complement.

## Why This Is The Right Finite Target

This separates the remaining arithmetic theorem from both nearby facts:

```text
full row rank of C
  does not imply C P_H = 0;

C P_H = 0
  is compatible with full row rank, since dim(P_H^perp)=203 > 156.
```

So the H-coset theorem is not a normality/span theorem and not a generic
linear-algebra consequence of the determinant square.  It is an additional
structured right-kernel inclusion.

## Sufficient But Too Strong

Right multiplication by

```text
eta = p^156 mod 211
```

shifts the seven H-cosets by a generator of the quotient.  Therefore, if a
centered row were invariant under `s -> eta*s`, then its seven H-coset sums
would all be equal, and ordinary centering would force them all to vanish.

This is only a sufficient fantasy symmetry.  The earlier multiplicative
resolvent and unit-symmetry boundaries show that the actual theorem cannot be
deduced from Frobenius covariance or free right-unit multiplier invariance.
The proof must produce the kernel inclusion `C P_H=0` directly for the p24
mixed CM/Lang packet.

## Check

The finite gate is:

```text
p24/trace_gcd_fixed_frequency_h_kernel_inclusion_gate.py
```

It verifies:

```text
H-indicator rank is 7;
P_H^perp has dimension 203;
random rows in P_H^perp can have full rank 156;
random centered full-rank rows have six-dimensional H-leak;
p^156 multiplier invariance would imply the H-kernel inclusion, but is only a
  sufficient stronger condition.
```
