# Trace-GCD Prefix Semilinear Core Criterion

Date: 2026-06-06

## Point

The component-transversality theorem can be stated using only the first
collapsed Gaussian DFT component plus one semilinear operator.

Let

```text
K = F_p(mu_35) = F_{p^4},
L = F_p(mu_157) = F_{p^156},
```

and let

```text
V_{a,j} in L,        0 <= a < 35,  j in {2,3,5,6}
```

be the first collapsed Gaussian frequency table from
`trace_gcd_prefix_component_frobenius_bookkeeping.md`.

Define the first-component map

```text
M_0 : K^{35*4} -> L
M_0(x) = sum_{a,j} x_{a,j} V_{a,j}.
```

It has rank at most

```text
dim_K L = 39,
```

so its kernel is large:

```text
dim_K ker(M_0) >= 140 - 39 = 101.
```

The prefix theorem is therefore not "the first component kernel is small."
The theorem is that this large kernel contains no nonzero vector closed under
the semilinear Frobenius-frequency motion.

## Semilinear Operator

Define

```text
T : K^{35*4} -> K^{35*4}
(T x)_{b,j} = x_{p^{-1}b,j}^p,
```

where indices `b` are taken modulo `35`.  Since

```text
p^4 = 1 mod 35,
x^{p^4} = x for x in K,
```

this operator has order `4` as an `F_p`-semilinear operator:

```text
T^4 = 1.
```

The `r`th tensor component relation from the scalar-extended Gaussian DFT is

```text
sum_{a,j} x_{a,j}^{p^r} V_{p^r a,j} = 0.
```

After reindexing, this is exactly

```text
M_0(T^r x) = 0.
```

Hence a scalar-extended `K`-linear relation among all `140` DFT columns is
equivalent to

```text
T^r x in ker(M_0)        for r = 0,1,2,3.
```

Equivalently:

```text
x lies in ker(M_0) cap T^{-1}ker(M_0)
                 cap T^{-2}ker(M_0) cap T^{-3}ker(M_0).
```

## Current Safe Theorem

Let

```text
C = ker(M_0).
```

The prefix theorem is:

```text
core_T(C) := {x : T^r x in C for all r = 0,1,2,3} = {0}.
```

This is the largest `T`-stable `F_p`-subspace contained in the first-component
kernel.  It is equivalent to the four-component twisted-kernel
transversality theorem, and hence to the original prefix coinvariant Fitting
unit.

This is the cleanest CS/probability import surface so far:

```text
large structured kernel C
semilinear order-4 motion T
certificate = C is evasive for nonzero T-orbits
```

The statement resembles a deterministic subspace-evasive/rank-condenser
condition, but it remains arithmetic because `C` comes from the actual CM
Gaussian period table.

## p24 Frequency-Orbit Shape

The fixed frequencies

```text
0,5,10,15,20,25,30
```

give coordinates where `T` acts by coefficient Frobenius only.  The seven
length-4 frequency orbits

```text
[1,22,29,8],
[2,9,23,16],
[3,31,17,24],
[4,18,11,32],
[6,27,34,13],
[7,14,28,21],
[12,19,33,26]
```

give four-cycles where `T` rotates the frequency and conjugates the
coefficient.

This orbit structure is bookkeeping for the semilinear action.  It still
does not split the target `L`; the theorem is the zero `T`-core of one large
kernel, not block diagonal independence by frequency orbit.

## Proof Direction

A proof can now aim at one of the following equivalent p-local objects:

```text
1. Fitt_16(coker(R^4 -> E/(tau_R-1)E)) = O_p;
2. the scalar-extended Gaussian DFT columns are K-independent;
3. core_T(ker M_0) = {0};
4. no nonzero T-orbit of coefficients gives a relative trace coboundary.
```

The advantage of item 3 is that it separates the unavoidable large kernel
from the actual obstruction: a nonzero semilinear invariant packet inside
that kernel.

There is a further descent form.  Because `core_T(C)` is a `K`-linear
`T`-stable subspace, semilinear Hilbert 90 says it is nonzero if and only if
it contains a nonzero `T`-fixed vector.  Thus the theorem is also:

```text
ker(M_0) cap Fix(T) = {0}.
```

For p24 this gives an explicit fixed-coordinate map

```text
F_p^28 + K^28 -> L
```

whose length-4 orbit terms are linearized expressions
`sum_{r=0}^3 z^{p^r} V_{p^r a,j}`.  This descent is recorded in:

```text
p24/trace_gcd_prefix_semilinear_descent_fixed_relation.md
p24/trace_gcd_prefix_semilinear_descent_toy.py
```

## Cheap Gate

The finite equivalence is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_semilinear_core_toy.py
```

The toy uses `q=2`, DFT length `3`, `K=F_4`, and `L=F_256`.  It enumerates
all `K`-coefficient relations for a random-good table and a forced fixed
frequency core, then verifies:

```text
global product-algebra kernel = semilinear T-core of ker(M_0).
```
