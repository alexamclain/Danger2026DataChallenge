# Decomposition-Field Packet Norm Theorem

This note records a sharper p-adic target for the relative-energy route.  It
does not solve the p24 nonvanishing theorem, but it packages the eight
Frobenius packet checks into a single degree-8 decomposition-field unit
statement.

## Finite-Field Packet Statement

Let `n` be an odd prime and let `p` be a prime with

```text
C = <p> <= (Z/nZ)^*,       e = [(Z/nZ)^* : C].
```

For a polynomial

```text
A(X) in F_p[X]/(X^n-1),
```

and an orbit representative `a`, let `f_a(X)` be the irreducible factor of
`Phi_n(X)` whose roots are

```text
zeta_n^(a*c),       c in C.
```

Then the packet value vanishes iff

```text
gcd(A, f_a) != 1,
```

and the packet norm

```text
N_a = Res(f_a, A) in F_p
```

is nonzero iff the packet does not vanish.

Consequently all packets are nonzero iff

```text
prod_a N_a != 0 in F_p.
```

The Lean file

```text
p24/lean/CertificateLogic.lean
```

checks the abstract implication:

```text
global packet norm nonzero => every packet norm nonzero => no harmful packet.
```

## Cyclotomic Interpretation

Let `E=Q(zeta_n)` and `M=E^C`.  Since the Frobenius class of `p` lies in `C`,
the prime `p` splits completely in the degree-`e` decomposition field `M`.

For a lift

```text
alpha = A(zeta_n),
```

the relative norm

```text
Xi = Norm_{E/M}(alpha)
```

has one residue at each of the `e` primes of `M` above `p`.  These residues are
exactly the packet norms `N_a`.

Thus the finite-field certificate can be restated as:

```text
Xi is a unit at every prime of M above p.
```

Equivalently, for integral `Xi`,

```text
p does not divide Norm_{M/Q}(Xi).
```

This is often the cleanest p-adic theorem target because the decomposition
field has degree `e`, not the full packet degree.

## Energy Specialization

For the relative-energy certificate, take

```text
A(X) = C(X) = sum_d C_d X^d,
C_d = sum_i j_{i+m*d} j_i.
```

Because `C_d=C_-d`, the energy lives in the real cyclotomic subfield.  For
p24,

```text
n = 3107441
ord_n(p) = 388430
p^(388430/2) == -1 mod n
```

so the energy packet degree is

```text
388430 / 2 = 194215.
```

The signed Frobenius packet count is still

```text
(n-1) / 388430 = 8.
```

Equivalently, in the real cyclotomic field

```text
E^+ = Q(zeta_n + zeta_n^-1),
M^+ = (E^+)^<p>,
```

we need

```text
Xi_E = Norm_{E^+/M^+}(E_1)
```

to be a unit at all eight primes of `M^+` above `p`, or

```text
p does not divide Norm_{M^+/Q}(Xi_E).
```

The degree accounting is:

```text
[E^+ : M^+] = 194215
[M^+ : Q]   = 8
```

This replaces "prove eight independent degree-194215 energy residues are
nonzero" by "prove one degree-8 decomposition-field norm is a p-unit."

The same packet-norm packaging applies to the carry-adjusted Hermitian energy
from

```text
p24/hermitian_energy_certificate.md
```

This Hermitian scalar has the advantage that it is `sum_u |P_u(a)|^2` in
characteristic zero, while still giving a finite-field sufficient certificate
when its packet residue is nonzero.

## Toy Check

The script

```text
p24/cyclotomic_packet_norm_toy.py
```

uses the calibrated `D=-5000`, `h=30` CM cycle over `q=1259`, with

```text
m=6, n=5, q == -1 mod 5.
```

The CM roots lie in `F_q`, but the fifth roots of unity do not.  The two
Frobenius packet factors are quadratic.  The run found:

```text
packet_norms = 707, 68 mod 1259
product_of_packet_norms_mod_q = 234
all_packet_energies_nonzero = 1
```

This verifies the packet-norm formulation in the same finite-field shape as
p24.

## Boundary

This is not yet the asymptotic speedup.  The hard arithmetic input has moved
to a more focused statement:

```text
prove the p24 decomposition-field packet norm Xi_E is a p-unit.
```

Computing `Xi_E` directly still involves a relative norm of degree `194215`,
whose coefficients are built from the same non-genus class autocorrelations.
The useful improvement is conceptual: any future trace formula, p-adic unit
criterion, or explicit tower identity can now aim at a degree-8 object rather
than eight separate large extension residues.

There is also a hard boundary:

```text
p24/energy_gram_isotropy_boundary.md
p24/energy_isotropy_obstruction_toy.py
```

The energy polynomial is the Hermitian Gram scalar

```text
C(X) = sum_u J_u(X)J_u(X^-1).
```

Nonzero content vectors can have zero Hermitian energy in the packet algebra.
Thus the degree-8 packet norm is not a formal consequence of the exact content
certificate.  A proof that `Xi_E` is a p-unit must use the CM/autocorrelation
structure of the p24 vector.
