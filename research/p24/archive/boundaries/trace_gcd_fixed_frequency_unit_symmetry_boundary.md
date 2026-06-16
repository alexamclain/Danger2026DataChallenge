# Fixed-Frequency Unit-Symmetry Boundary

Date: 2026-06-06

## Tempting Shortcut

The order-7 augmentation target would follow from a strong multiplier
symmetry of the mixed centered marginal:

```text
C(a,b) = C(a, eta*b),
```

where `eta` acts trivially on the left `157` component and nontrivially on the
right order-7 quotient of `(Z/211Z)^*`.

Indeed, if `P_chi` is the right quotient-character projection, then the same
symmetry gives:

```text
P_chi = chi(eta) * P_chi.
```

For `chi(eta) != 1`, this forces:

```text
P_chi = 0.
```

This would prove the six nontrivial order-7 augmentation vanishings at once.

## Boundary

This multiplier is not a free class-field symmetry of the embedded CM torsor.
Class-field Galois acts by class translation on the torsor; multiplication of
class indices by a CRT unit is an automorphism of the abstract cyclic label
group, not automatically an automorphism of the embedded `j`-torsor or of the
Hermitian packet kernel.

The pinned actual-CM analogue:

```text
D=-13319, q=13463, h=140, m=28, n=5,
left=4, right=7.
```

has `q mod 7 = 2`, so the right nonzero frequencies split into two Frobenius
orbits and the quotient character is the quadratic character modulo `7`.
The CRT unit

```text
eta = 5 mod 7,     eta = 1 mod 4
```

is nontrivial on that quotient.

The actual mixed Hermitian packet reports:

```text
actual_multiplier_invariance_failures=18
actual_projection_for_left_u1=(2483,12626,12478,2303,9785,9985)
actual_projection_nonzero=1
```

So the formal implication is valid, but the hypothesis is false in real
CM packet data.

## Consequence

The p24 order-7 augmentation theorem cannot be justified by saying that
right-unit or diamond symmetry acts as index multiplication on the Hermitian
kernel.  Any successful proof must use a genuinely p24-specific arithmetic
identity for the mixed profile, or abandon the augmentation route in favor of
the representative p-unit / delete-one Moore determinant route.

## Check

The finite implication and actual-CM boundary are checked by:

```text
p24/trace_gcd_fixed_frequency_unit_symmetry_boundary.py
```

It verifies:

```text
multiplier invariance
  => nontrivial quotient-character projection zero;

actual pinned CM packet
  => multiplier invariance fails and the corresponding projection is nonzero.
```
