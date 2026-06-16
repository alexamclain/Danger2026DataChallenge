# Trace-Frame Translate-Minor Dominance Boundary

Date: 2026-06-05

This note records what principal singular-modulus dominance can prove for the
selected translate-minor formulation.

## Archimedean Dominance Criterion

Let:

```text
M_{a,b} = j_{a-b}
```

be a cyclic translate matrix of singular moduli in characteristic zero.  For a
selected minor:

```text
Delta_{I,J} = det(j_{i-rho(i)})_{i in I, rho(i) in J},
```

the determinant expansion is:

```text
Delta_{I,J}
  = sum_{rho:I->J bijective} sign(rho) prod_{i in I} j_{i-rho(i)}.
```

If one permutation `rho_0` has a unique dominant product of singular moduli,
and the dominance margin exceeds the sum of all other products, then:

```text
Delta_{I,J} != 0
```

over `C`.

This is the selected-minor analogue of the normal-resolvent dominance checked
by:

```text
p24/singular_moduli_normality_bound.py
```

The principal form has size roughly:

```text
exp(pi*sqrt(|Delta|)),
```

while every nonprincipal reduced form has size at most roughly:

```text
exp(pi*sqrt(|Delta|)/2).
```

So a minor whose determinant expansion contains a unique product with many
principal-class entries can be proved nonzero in characteristic zero.

## Why This Still Does Not Prove The Certificate

The p24 certificate needs:

```text
Delta_{I,J} mod P != 0
```

at the selected prime `P | p`, not just:

```text
Delta_{I,J} != 0 over C.
```

The p24 prime splits completely in the ring class field, so vanishing modulo
one selected prime is a p-adic statement:

```text
v_P(Delta_{I,J}) > 0.
```

Archimedean dominance does not prevent that.  This is the same obstruction
recorded for Hermitian packet scalars in:

```text
p24/hermitian_padic_principal_boundary.md
```

and for naive norm lifting in:

```text
p24/finite_field_lifting_height_audit.py
```

The size gap is enormous:

```text
log |j_principal| / log(p) ~= 4.6e10
```

for the third p24 target.  Therefore even large forced divisibility by `p`
at many split primes is not contradictory by height.

## What Dominance Can Still Do

Dominance is still useful for ruling out characteristic-zero identities:

```text
selected minor is not identically zero over the CM torsor;
full normal resolvents are nonzero over C;
some quotient/complement traces are nonzero over C.
```

It can also suggest good minors: a row/column choice with a unique dominant
matching is a good candidate for a stable determinant.

For the current p24 leading-prefix coordinate, the naive diagonal-principal
matching is already disfavored by:

```text
p24/trace_frame_axis_prefix_overlap_boundary.md
```

The audit shows that no cyclic translate of the length-`368` leading prefix
meets the smooth-axis frequency support in more than three points.  Thus the
obvious "many principal factors in one determinant term" dominance proof is
not available for this selected coordinate.

But to finish p24, dominance must be paired with a selected-prime mechanism,
such as:

```text
1. a p-adic unit formula for the selected translate minor;
2. a divisor/local-intersection formula showing no contribution at P;
3. an explicit finite-field Bezout certificate for the reduced minor;
4. a p-unit coordinate change to a determinant already known to be a unit.
```

Without that extra p-adic input, principal dominance is a characteristic-zero
sanity check, not the required sub-sqrt certificate.
