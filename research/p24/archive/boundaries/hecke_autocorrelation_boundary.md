# Hecke Autocorrelation Boundary

The scalar energy certificate uses the autocorrelation sequence

```text
C_d = sum_i j_i j_{i+m*d}.
```

This note checks whether ordinary Hecke/correspondence data can compute these
values cheaply.

## What Hecke Data Does Give

Let `S` be a split-prime class action on a cyclic CM torsor.  The ordinary
unoriented `X_0(ell)` correspondence acts horizontally like

```text
A = S + S^(-1).
```

For the product autocorrelation,

```text
C_d = sum_i j_i j_{i+d}
```

we have `C_d=C_-d`, so the first Hecke edge moment gives

```text
<j, A j> = 2 C_1.
```

More generally,

```text
<j, A^r j> =
  sum_{k=0}^r binom(r,k) C_{r-2k}.
```

Thus Hecke walk moments determine the autocorrelations by triangular
inversion, and Chebyshev polynomials recover

```text
S^d + S^(-d)
```

from `A`.

## Why This Is Not A p24 Speedup

The inversion is not a degree collapse.  To obtain the high-order energy

```text
E_a = sum_d zeta_n^(a*d) C_d,
```

one still needs the autocorrelation sequence across the order-`n` recovery
cycle, or an equivalent spectral evaluation.  Chebyshev compression replaces
a class shift by a degree-`d` polynomial in the Hecke adjacency; for
`d ~ n`, that polynomial has recovery-scale degree/support.

The ordinary Hecke operator also erases branch labels.  Product
autocorrelation happens to be symmetric, so this erasure is harmless for
`C_d`; it is not harmless for the original relative periods `P_u(a)`.

For the third p24 target, the relevant shift is the oriented class

```text
beta = 2 * 463 * 223^(-1),
```

of order

```text
n = 3107441.
```

Even if the first moment for `beta` were available from a composite
correspondence, the energy needs the high-order Fourier transform of
`C_d` over the full beta-cycle.

## Toy Check

The script

```text
p24/hecke_autocorrelation_toy.py
```

uses the calibrated `D=-5000`, `h=30`, norm-3 generator cycle.  It verifies
the binomial Hecke-walk identity and triangular recovery of `C_d` from
`<j,A^rj>`, then reports that the recovered sequence still has full
Berlekamp-Massey complexity.  The Hecke moment sequence itself saturates the
sampled Berlekamp-Massey window, so no short recurrence is visible there
either.  Full Fourier-support checks are handled in
`relative_autocorrelation_complexity_scan.py`, which chooses primes with the
needed roots of unity in the base field.

Conclusion:

```text
Hecke moments repackage the autocorrelation sequence; they do not compute the
high-order energy packets without recovery-scale data.
```

The Brandt-matrix phrasing gives the same answer.  The bounded probe

```text
p24/agent_brandt_energy_probe.py
```

checks `Trace(D_j P_d D_j P_-d)=C_d` and finds full relative
Berlekamp-Massey complexity and full DFT support in the `D=-5000` toy:

```text
bm_complexity=5
dft_support=5
```

So the exact trace bookkeeping is useful notation, not a lower-dimensional
transfer computation.
