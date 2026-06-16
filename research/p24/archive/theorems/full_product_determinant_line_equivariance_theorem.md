# Full Product Determinant-Line Equivariance Theorem

Date: 2026-06-06

## Purpose

This note pins the remaining diamond/unit-2 theorem in the form that would
complete the transport half of the p24 four-field-element certificate.

The theorem is not a nonvanishing theorem.  It says that once the
trace-GCD/Fitting determinant-line object is constructed over the full
right cyclotomic product algebra, the right-unit action transports p-unitness
between the six nonzero right Frobenius orbits by determinant-line p-unit
factors.

## p24 Product Algebra

Let `O_p` be the p-adic valuation ring at

```text
p = 10^24 + 7.
```

Since `p` is prime to `211` and `ord_211(p)=35`, the cyclotomic algebra

```text
A_211 = O_p[zeta_211]
```

is finite etale and its special fiber has six nonzero degree-35 factors:

```text
A_211 mod p = R_O1 x ... x R_O6
```

together with the separate `O0={0}` right-frequency factor in the augmented
trace-GCD bookkeeping.  The right-unit automorphism

```text
sigma_2 : zeta_211 |-> zeta_211^2
```

is integral and permutes the six nonzero factors:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

The finite support audit records the exact representative row:

```text
delete O4, tail O1, prefix O2,O3,O5,O6.
```

Under `sigma_2`, deletion and tail cycle through all six nonzero orbits, every
prefix has four orbit blocks, and each size-16 tail window stays
Frobenius-contiguous.  After six unit steps, the tail is back in `O1` with
internal Frobenius rotation start `17`, because

```text
2^6 == p^17 mod 211.
```

So the theorem must include internal Frobenius trivializations inside the
target factor.

## Structural Theorem

For each nonzero orbit `O`, suppose the full product-algebra construction
produces finite free `O_p`-lattices

```text
K_O, T_O
```

and a p-integral Fitting/block map

```text
B_O : K_O -> T_O
```

whose determinant-line section is

```text
Xi_O = det(B_O).
```

Assume these objects are not chosen factor-by-factor, but are obtained by
projecting a single full `A_211` p-integral construction:

```text
1. diamond-equivariant Lang/Fourier bases over the finite etale model;
2. prefix kernels as kernels of sigma_2-transported full-block trace maps;
3. tail windows as sigma_2-transported subbundles, with internal Frobenius
   rotations allowed when the unit cycle returns to the same factor;
4. block maps B_O induced by one universal trace-GCD/Fitting map.
```

Then `sigma_2` gives p-integral lattice isomorphisms

```text
d_K,O : K_O -> K_2O
d_T,O : T_O -> T_2O
```

and the universal construction gives a commuting square:

```text
B_2O o d_K,O = d_T,O o B_O.
```

Taking top exterior powers gives

```text
det(B_2O) * det(d_K,O) = det(d_T,O) * det(B_O),
```

or equivalently

```text
Xi_2O = epsilon_O * Xi_O,
epsilon_O = det(d_T,O) * det(d_K,O)^(-1).
```

Since `d_K,O` and `d_T,O` are p-integral lattice isomorphisms, their
determinants are p-units.  Hence

```text
epsilon_O in O_p^*.
```

Therefore

```text
Xi_O in O_p^*  =>  Xi_2O in O_p^*.
```

Iterating around the six nonzero orbits transports one representative
nonzero-orbit p-unit to all six.

## Six-Step Closure

The sixth unit step returns to the same right factor only after an internal
Frobenius rotation.  For p24 this is the explicit identity:

```text
2^6 = 64 = 114^17 = p^17 mod 211.
```

The Frobenius action on a degree-35 unramified factor is a p-integral
automorphism, and its determinant is a p-unit.  Thus the six-step closure
does not require literal equality of raw windows or printed scalar
representatives.  It requires equality in the determinant line after applying
the internal Frobenius trivialization.

This is exactly the correction found by:

```text
p24/diamond_support_transport_audit.py
```

## What This Proves

Together with:

```text
p24/lean/TraceGcdDiamondEquivarianceGate.lean
```

the theorem gives the diamond half of the conditional certificate:

```text
Xi_O1 in O_p^*
  => Xi_O2,...,Xi_O6 in O_p^*.
```

Together with the fixed orbit p-unit `Xi_O0`, the verifier payload is:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

## What Remains

This theorem reduces the diamond proof to a construction problem:

```text
construct the full p-integral A_211 trace-GCD/Fitting object and prove its
sigma_2 functoriality.
```

It does not prove the two arithmetic p-unit producers:

```text
Xi_O0 in O_p^*
Xi_O1 in O_p^*
```

Those remain the selected-prime local nonintersection statements.

