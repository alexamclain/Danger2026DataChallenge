# Lang Trace-GCD Integrality Lift

Date: 2026-06-05

This note records the p-integrality hygiene for the mixed trace-GCD
operator-norm theorem.  It separates:

```text
finite statement:
  a determinant is nonzero after reduction mod p;

arithmetic statement:
  the lifted determinant/resultant is a p-unit.
```

## Integral Sources

The p24 mixed periods are built from singular moduli and roots of unity.

```text
p = 10^24 + 7
p mod 157 = 21
p mod 211 = 114
```

The singular moduli `j` are algebraic integers.  Character resolvents are
sums of singular moduli multiplied by roots of unity, hence are integral in
the ring-class/cyclotomic compositum.  The Hermitian pairings and relative
trace maps are formed from products and traces of these integral quantities,
so they remain integral before any coordinate normalization.

The roots of unity of orders `2`, `157`, and `211` are p-adic units because
`p` is prime to those orders.

## Denominators

The visible denominators in the trace-GCD construction are:

```text
1. CRT/DFT normalizations by factors dividing 2*157*211;
2. Lang/Moore change-of-basis determinants in the right degree-35 factors;
3. selected coordinate-basis determinants introduced by transporting kernels.
```

For p24, the first class is p-integral because:

```text
p does not divide 2*157*211.
```

For the Lang bases, choose integral lifts of bases whose reductions form
`F_p`-bases of the corresponding residue fields.  The Moore/Lang determinant
is nonzero after reduction, so its lift is a p-adic unit.  Thus inverting the
Lang matrix only introduces p-unit denominators.

The kernel-transport and selected-coordinate determinants are basis changes
inside finite free modules after localizing at p.  If their reductions are
invertible in the finite construction, their lifts are p-units.

## Unit Ambiguity

The origin-covariance theorem gives determinants only up to nonzero basis
and phase factors:

```text
Delta(alpha,beta) = u(alpha,beta) * F(alpha mod 211).
```

For the arithmetic theorem, this must be read as:

```text
u(alpha,beta) is a p-unit.
```

Then:

```text
Delta(alpha,beta) is a p-unit
  <=> F(alpha mod 211) is a p-unit.
```

Likewise, scaling the Pluecker-Fourier element:

```text
f(Y) -> u * f(Y)
```

with `u` a p-unit scales the operator norm by:

```text
u^211,
```

again a p-unit.  The p-unit status of the resultant is therefore independent
of compatible integral Lang/trace-coordinate choices.

## Lifted Theorem Form

The finite operator-norm target from:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
```

should be lifted as:

```text
There exists a p-integral cyclic-algebra element

  f_trace in O_F[Y]/(Y^211 - 1)

whose reduction is the finite Pluecker-Fourier element

  det(P diag(Y^v) A),

and f_trace is a unit in the local algebra at every selected prime above p.
```

Equivalently:

```text
Norm(f_trace) = det(m_f_trace)
```

is a p-unit.  After reduction this implies:

```text
prod_{t mod 211} Delta(t) != 0 mod p.
```

## Remaining Gap

This note does not prove `f_trace` is a p-unit.  It only records that the
coordinate choices, DFT normalizations, Lang inverses, and origin-covariance
unit factors do not create p-denominators.

The missing theorem is still:

```text
construct the p-integral CM element f_trace and prove its cyclic-algebra norm
is a p-unit at p = 10^24 + 7.
```

This is now the precise p-adic version of the mixed representative
trace-GCD producer theorem.

The intrinsic Chow determinant-line version of the same p-integrality
statement is:

```text
p24/trace_gcd_chow_integral_model.md
```

It records that changing integral bases, volume forms, Lang coordinates, or
right-translate trivializations scales the Chow values only by p-units.
