# Fixed-Frequency Symmetry Boundary

Date: 2026-06-06

## Point

The six right Frobenius orbits modulo `211` are the six type-6 Gaussian
cosets for the p24 right field.  Ordered by least representative, they are:

```text
1, 2, 4, 8, 16, 29.
```

The type-6 Gaussian coset

```text
<2^35> = {1,197,196,210,14,15}
```

meets those six orbits in labels:

```text
1, 6, 5, 4, 3, 2.
```

Thus the full block omitted by the selected RS-tail square is the right orbit
containing `-1 mod 211`, while the tail block is the orbit containing
`1 mod 211`.

## Boundary Tested

A tempting explanation for the fixed-frequency no-defect theorem is:

```text
right centering + Hermitian/sign symmetry
```

where centering says the nonzero right profile sums to zero and sign symmetry
models the strongest easy relation `f(s)=f(-s)`.

The finite check in

```text
p24/trace_gcd_fixed_frequency_symmetry_boundary.py
```

compresses right profiles by sign pairs and asks whether the orbit-1 DFT
functional lies in the span of the four selected orbit functionals, modulo the
centering constraint, at the seven fixed frequencies `a in 5Z/35Z`.

## Result

The easy symmetry forces the relation only at the trivial fixed frequency:

```text
a = 0.
```

At the six nontrivial order-7 fixed frequencies:

```text
a = 5,10,15,20,25,30,
```

the orbit-1 functional remains independent from the selected four modulo
centering and sign symmetry.

## Consequence

The missing cyclic syzygy

```text
T = C_2 P_2 + C_3 P_3 + C_5 P_5 + C_6 P_6
```

cannot be proved from generic centered/Hermitian right-orbit symmetry alone.
The six nontrivial fixed frequencies require a genuinely arithmetic
CM/Lang packet identity, likely involving the order-7 Gaussian-period
projection of the mixed Hermitian resolvent pairing.
