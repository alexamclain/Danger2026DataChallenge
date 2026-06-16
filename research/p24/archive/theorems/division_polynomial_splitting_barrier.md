# Division-Polynomial Splitting Barrier

Date: 2026-06-04 PDT

Target:

```text
p = 10^24 + 7
k = 40
N = 2^40
```

## Question

Could we avoid trace search by writing the verifier condition as an algebraic
equation

```text
Z_k(A,x) = 0
```

for the Montgomery doubling recurrence, then eliminating or solving for
`(A,x)` directly?

## Verdict

Not in a way that beats the known modular obstruction.  The equation
`Z_k(A,x)=0` is a division-polynomial condition.  Over the algebraic closure,
every nonsingular elliptic curve has full `2^k` torsion, so eliminating `x`
does not cut out the rare target `A` values.  The rare arithmetic condition is
that one of the exact-order `2^k` torsion `x`-coordinates is already defined
over `F_p`.

That splitting condition is exactly:

```text
Frobenius acts by +1 or -1 on a 2^k ray
```

or, in eigenvalue notation,

```text
lambda ==  1 mod 2^k    curve side
lambda == -1 mod 2^k    twist side.
```

Thus division-polynomial algebra is another coordinate system for the same
`X1(2^k)` orientation condition.

## Why Elimination Is Too Weak

For fixed nonsingular `A`, the `2^k`-division polynomial has roots over an
extension field.  Therefore the projection of the algebraic curve

```text
Z_k(A,x) = 0
```

to the `A`-line is essentially the whole nonsingular Montgomery line over
`Fbar_p`.  Any resultant that only asks for an algebraic root forgets the
hard part.

To recover the verifier condition, one must ask for an `F_p` root of an
exact-order factor.  This is a factorization/splitting question for a
high-degree division polynomial, controlled by Frobenius on `E[2^k]`.

## Relation To Existing Audits

This matches the literal small-field verifier audit:

```text
p24/verifier_equivalence_audit.py
```

which checks that accepted `x` values are exactly the predicted curve/twist
2-primary points.

It also matches:

```text
p24/x1_section_gonality_barrier.md
p24/two_adic_trace_inversion_sidecar.md
p24/subagent_modular_tower_note.md
```

Those notes phrase the same obstruction in modular, 2-adic, and tower
language.  A direct division-polynomial solver would need to factor or split
the same `X1(2^40)` ray condition; it is not a separate sub-sqrt construction.

## Remaining Shape

A useful algebraic attack would need more than `Z_k(A,x)=0`.  It would need a
p-specific rule that predicts which division-polynomial factor has an `F_p`
root, without enumerating the ray-orientation fiber.  No such rule is visible
from the current p24 arithmetic.
