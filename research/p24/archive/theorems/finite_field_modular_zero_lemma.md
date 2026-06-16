# Finite-field modular zero lemma

This is the structural replacement for the naive height-lifting argument in
the bounded-level case.  It does not prove the full reduced-normality theorem,
but it rules out a large class of accidental one-prime identities.

## Lemma

Let `C/F_p` be a smooth irreducible modular curve or an irreducible component
of a prime-to-`p` modular-correspondence cover.  Let

```text
F in F_p(C)
```

be a rational modular function that is regular at a set `S <= C(F_p)` of
ordinary CM points.  If

```text
F(P) = 0       for every P in S,
```

and `F` is not identically zero, then

```text
|S| <= deg_poles(F).
```

Equivalently, if `|S| > deg_poles(F)`, the vanishing is a genuine mod-`p`
modular identity on `C`.

## Proof

On a smooth projective curve, a nonzero rational function has a zero divisor
and a pole divisor of the same degree.  If `F` is regular at every point of
`S` and vanishes there, the zero divisor has degree at least `|S|`, with
multiplicity ignored.  Hence the pole divisor has degree at least `|S|`.

This is a characteristic-`p` divisor argument.  It does not compare complex
sizes and does not require lifting `F` to characteristic zero.

## Non-identity check by cusp poles

For the modular functions that arise from local Hecke/correspondence formulas,
one can often prove that the forced identity is impossible by looking at a
cusp branch.

Along the Tate cusp, the basic degeneracy pullbacks have distinct leading
poles:

```text
j(q^N) = q^{-N} + 744 + ...
```

So a finite linear combination

```text
sum_i c_i * j(q^{N_i})
```

with distinct `N_i` and `N_i < p` cannot be the zero function modulo `p`
unless every `c_i` attached to the largest pole order is zero; descending on
the pole orders kills all coefficients.  The same pole-order test applies to
oriented correspondence words whenever the selected cusp branch gives distinct
norms for the words.

Thus a small local formula cannot vanish on the entire CM torsor by a
p-specific congruence unless its pole degree is at least the number of CM
points it vanishes on, or unless it uses a characteristic-`p` operation such
as Frobenius with pole degree on the order of `p`.

## Application to selector identities

Suppose a bounded local formula tries to produce an `H`-period from a sparse
set of oriented class translates:

```text
L(j_g) = y_{gH}.
```

Taking the difference between two representatives of the same coset gives a
vanishing identity on the full CM torsor:

```text
L(j_g) - L(j_{g h0}) = 0       for all g in G, h0 in H.
```

If the formula is realized on a correspondence cover with pole degree less
than `h=|G|`, the zero lemma forces this to be an actual mod-`p` modular
identity.  The cusp-pole test then rules out ordinary linear combinations of
distinct low-norm correspondence words.

This gives a direct finite-field obstruction to accidental bounded local
selectors.  It is weaker than full reduced normality, because it only sees
relations whose correspondence cover and pole degree are small enough, but it
is exactly the regime where one would hope for a surprising bounded identity.

## p24 scale

For the live rows:

```text
first trace:
  h = 278733727154
  H-period support threshold = 14670196166

third trace:
  h = 205880396014
  H-period support threshold = 3107441
```

A bounded `Phi_ell`, bounded split-cycle edge, fixed-level Siegel/Weber
invariant, or small resultant cover has pole degree tiny compared with these
class numbers.  If it vanished on all target CM points, it would have to be a
global mod-`p` modular identity; the Tate-cusp pole orders rule out the usual
linear correspondence identities.

The lemma does not rule out the surviving sub-sqrt positive route:

```text
third target growing-degree recovery object, degree about 3107441.
```

That route intentionally pays a large fiber/pole degree, still below
`sqrt(p)`, and therefore sits outside this bounded-identity no-go theorem.
