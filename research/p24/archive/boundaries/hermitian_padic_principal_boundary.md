# Hermitian p-adic Principal Boundary

This note records why the principal-term dominance theorem does not by itself
prove the selected-prime Hermitian packet certificate.

## Characteristic-zero fact

For the third p24 target, choose the complex CM origin so that `j_0` is the
principal singular modulus.  For every nontrivial relative character `a`,

```text
P_0(a) = sum_k zeta_n^(a*k) j_{m*k}
```

contains `j_0` with coefficient `1`, and every other term has reduced-form
denominator at least `2`.  The standard singular-modulus estimate gives an
overwhelming dominance margin, so

```text
P_0(a) != 0
```

over `C`, and hence the Hermitian scalar

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{u*}(a)
```

is strictly positive over `C`.

This is the strongest archimedean statement we currently have.

## Selected-prime form

Let `L` be the ring class field with the needed roots of unity adjoined.  The
p24 prime splits completely in the ring class field.  Reducing an algebraic
integer such as `P_0(a)` or `H_a` modulo `p` therefore means choosing a prime

```text
P | p
```

of `L`.  The chosen finite-field embedding is one such prime.  Class-group
translation sends it to all the others.

Thus

```text
P_0(a) == 0 mod P
```

is not an archimedean question.  It is a selected-prime p-adic valuation
statement:

```text
v_P(P_0(a)) > 0.
```

Complex dominance proves the algebraic integer is nonzero, but a nonzero
algebraic integer may vanish at some split primes.

## Why the principal root does not select P

The phrase "principal CM root modulo p" is not intrinsic.  The principal
singular modulus is distinguished by a complex embedding, but reduction modulo
a completely split prime requires choosing a prime above `p`.  Choosing that
prime is equivalent to choosing one embedded CM root modulo `p`.

The local audits make this explicit:

```text
p24/principal_singular_modulus_reduction_audit.py
p24/frobenius_principal_ideal_origin_audit.py
p24/principal_cm_root_torsor_audit.py
```

In the toy `D=-5000`, `q=1259`, Frobenius fixes all `30` CM roots.  Any root
can be labeled principal after rotating the abstract class coordinate.  The
finite-field root set and Frobenius identity action do not distinguish the
principal label.

The same applies to the p24 Hermitian scalar.  The complex embedding where
`j_0` dominates does not identify the finite-field prime `P` at which the
certificate must be nonzero.

## Norm information is too coarse

The global norm

```text
Norm(H_a)
```

can detect whether some prime above `p` divides `H_a`, but the certificate
needs the selected packet prime to avoid divisibility.  Conversely, a product
or norm over all class translates may erase the phase information that
distinguishes the eight Frobenius packets.

This is why the clean scalar target was phrased as:

```text
prove the degree-8 decomposition-field Hermitian packet norm is a p-unit.
```

It is still a selected-prime p-unit theorem, not a consequence of positivity.

The sharper packet formulation is:

```text
Xi_a = Norm_{E^+/M^+}(H_a)
```

where `E^+ = Q(zeta_n + zeta_n^-1)` and `M^+` is the degree-8 real
decomposition field.  For p24:

```text
[E^+ : M^+] = 194215
[M^+ : Q] = 8
```

The scalar theorem needed is:

```text
Xi_a is a p-unit at every prime of M^+ above p.
```

Equivalently, each Hermitian packet residue is nonzero modulo its Frobenius
factor.  A full class norm or full product over split primes is too coarse.

The toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/selected_prime_norm_toy.py
```

shows this in the smallest possible way.  For `D=-87`, `q=103`, and
`alpha=j-5`, the global norm is nonzero but divisible by `103`; `alpha`
vanishes at the selected root `5` but not at the selected root `29`.

The selected-prime rotation scan

```text
p24/hermitian_selected_prime_zero_scan.py
p24/hermitian_selected_prime_zero_scan.md
```

then tests the packet scalar itself in bounded CM examples.  In 1456
Hermitian selected-embedding tests across 74 nonlinear packet rows, it found
no selected-prime Hermitian zeros.  The ordinary-energy control on low-order
rows found two full-orbit zero packets, showing the scan does detect scalar
cancellation when it exists.

## Consequence

The principal-dominance theorem remains valuable because it proves the
Hermitian packet is not identically zero in characteristic zero and rules out
all complex cancellation explanations.

But to finish p24, one still needs one of:

```text
1. a selected-prime p-unit theorem for the Hermitian packet;
2. an exact finite-field relative-content/Bezout certificate;
3. an embedded class-field tower relation that actually pairs quotient roots
   with recovery factors in j.
```

The missing theorem is precisely p-adic/finite-field, not archimedean.
