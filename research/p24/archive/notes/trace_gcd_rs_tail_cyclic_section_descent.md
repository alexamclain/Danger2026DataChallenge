# RS-Tail Cyclic Section Descent Gate

Date: 2026-06-06

## Point

The frequency-resultant target is only useful if the local Plucker and
tail-residue values come from p-integral cyclic sections.  Arbitrary values on
the `35` frequency roots can always be interpolated over the splitting field,
but such a post-fit interpolant is not a class-set-free p-unit certificate.

## Descent Criterion

Let `omega` be a primitive `n`th root over `F_p`, and let values

```text
F_a in F_p(mu_n),      a in Z/nZ
```

be proposed local Plucker or tail-residue values.  A degree `< n` interpolant
`P(x)` has coefficients in `F_p` exactly when the values satisfy the
semilinear Frobenius condition

```text
F_{p a} = F_a^p.
```

Then

```text
P(omega^a) = F_a
```

is a descended cyclic section, and

```text
Res(P, x^n - 1) = product_a F_a
```

is a base-field determinant-line value.

For a defect selector with support `A subset Z/nZ`, the selector

```text
S_A(x) = product_{a in A} (x - omega^a)
```

has base-field coefficients exactly when `A` is Frobenius-stable.

## P24 Consequence

For p24:

```text
n = 35
p mod 35 = 22
orbit lengths under a -> 22a:
  seven fixed points and seven length-4 orbits.
```

Thus a base-field defect selector of size `16` must be four length-4
Frobenius orbits only after one extra arithmetic input: no fixed frequency is
a defect line.  Descent alone allows exactly two stable support types:

```text
0 fixed singletons + 4 length-4 orbits:   35 choices;
4 fixed singletons + 3 length-4 orbits:   1225 choices.
```

Thus base-field descent leaves `1260` possible stable size-16 supports.  If
the p24 defect set is not Frobenius-stable, the frequency-resultant route has
to be replaced by a factorwise/twisted orbit-algebra certificate rather than a
single base selector.

The current arithmetic target is therefore:

```text
construct the CM/Lang local values;
prove their semilinear Frobenius covariance;
prove no fixed-frequency defects, or otherwise identify the stable defect
  support among the 1260 possibilities;
then use the resultant gate for P_24,T_24,S_24.
```

The no-fixed-defect lemma has the local form:

```text
for every fixed a in 5Z/35Z,  rank(P_a,tau_a) = rank(P_a).
```

That is, the fixed-frequency tail value must lie in the fixed-frequency
prefix image.

## Check

The finite gate is tested in:

```text
p24/trace_gcd_rs_tail_cyclic_section_descent_toy.py
p24/trace_gcd_rs_tail_defect_support_accounting.py
p24/trace_gcd_rs_tail_fixed_frequency_ordinary_gate.py
```

It checks:

```text
Frobenius-compatible values interpolate to base coefficients;
arbitrary splitting-field values are rejected as post-fit;
Frobenius-stable defect support gives a base selector;
nonstable defect support has no base selector.
p24 stable size-16 supports have the two types listed above;
four length-4 orbits is not forced by descent alone.
mixed fixed supports still pass descent and Vandermonde;
fixed-frequency ordinary is the exact extra support-reduction theorem.
```
