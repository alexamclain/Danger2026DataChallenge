# Augmentation Zero-Lemma Boundary

This note records why the finite-field zero lemma does not prove the
augmentation/resultant theorem.

## Harmful vs Product Vanishing

The earlier correspondence zero-lemma route targeted harmful packet vanishing:

```text
P_u(a) = 0 for every quotient coordinate u.
```

Because each coordinate zero propagates around the order-`n` recovery orbit,
harmful vanishing gives

```text
h = m*n
```

zeros on the full CM torsor.  If a weighted trace is realized by a
correspondence function with pole degree `n*delta`, then the zero lemma would
rule it out when

```text
n*delta < m*n,  i.e. delta < m.
```

This was the window tested in:

```text
p24/correspondence_zero_lemma_window.md
```

## Product/Augmentation Vanishing Is Smaller

The prime augmentation determinant route is stronger than needed.  It asks
that no individual coordinate vanish:

```text
P_u(a) != 0 for every u.
```

If one coordinate vanishes, the same eigenrelation gives only the recovery
orbit of zeros:

```text
n zeros,
```

not the full `m*n` zeros.

A natural order-`n` relative trace has pole degree at least on the scale of
`n*delta`, where `delta >= 1` for any nonconstant correspondence
realization.  The zero lemma would need

```text
n*delta < n,
```

or

```text
delta < 1.
```

So the zero lemma cannot certify individual coordinate nonvanishing by
divisor counting.  It is intrinsically aligned with the exact all-coordinate
content condition, not with the stronger product certificate.

## Consequence

The current augmentation theorem target

```text
Res(Phi_3107441, J_u) is a p-unit for every u
```

must be proved by a p-adic/normality argument, a trace formula, or an explicit
finite-field identity.  The finite-field modular zero lemma does not provide
enough zeros for the single-coordinate event.

This is not a contradiction with the usefulness of the product certificate:
product nonvanishing would still imply the exact certificate.  It just means
the proof mechanism has to be different from the full-harmful zero-lemma
window.

