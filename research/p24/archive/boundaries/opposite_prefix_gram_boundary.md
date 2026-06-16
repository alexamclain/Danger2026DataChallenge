# Opposite-Prefix Gram Boundary

The opposite-pair certificate makes each prefix stable under inversion:

```text
exclude O1/O4: prefix O2,O3,O5,O6
exclude O2/O5: prefix O1,O3,O4,O6
exclude O3/O6: prefix O1,O2,O4,O5
```

This suggests a Hermitian Gram packaging of the three prefix p-units.  Such a
packaging is attractive because it has a characteristic-zero positivity
interpretation and may be closer to local-intersection or Borcherds p-unit
methods.

## Candidate

For an opposite-stable prefix `A`, let

```text
T_A : L -> V_A
```

be the four-packet right-trace map in Lang coordinates.  The prefix p-unit
`B_A` proves:

```text
rank T_A = dim V_A = 140.
```

If the inversion-stable target has a compatible Hermitian pairing, a stronger
certificate is:

```text
det(T_A T_A^*) != 0.
```

This would imply `rank T_A=140`, hence it would be a sufficient prefix
certificate.

## Boundary

Over finite fields, the Gram determinant is not equivalent to row rank.  A
full-rank subspace can be degenerate for the ambient Hermitian form.  Thus
the Gram determinant is a stronger p-unit target, not a free reformulation of
`B_A`.

The finite-field obstruction is recorded in:

```text
p24/opposite_prefix_gram_toy.py
```

Two runs:

```text
q=3, rows=4, cols=8, trials=2000:
  full_row_rank=2000
  full_row_and_full_gram=1398
  full_row_singular_gram=602

q=2, rows=3, cols=6, trials=2000:
  full_row_rank=1991
  full_row_and_full_gram=1040
  full_row_singular_gram=951
```

So even when ordinary prefix rank is full, the Hermitian Gram determinant can
vanish.

## Consequence

The opposite-stable prefix structure is still useful, but only in this form:

```text
prove a stronger Hermitian Gram p-unit
  => prefix rank p-unit B.
```

It cannot replace the prefix theorem by positivity or by formal
nondegeneracy.  A successful Gram route would need the same kind of
selected-prime p-adic input as the Hermitian packet norm route: a local
intersection, Borcherds, or explicit finite-field p-unit theorem for the
actual p24 opposite-prefix Gram determinant.

Thus the current sharp target remains:

```text
3 opposite-prefix p-units B
+ 3 representative opposite-tail p-units T.
```

The Gram determinant may be a better way to prove the three `B` p-units, but
it is not an automatic consequence of the finite linear algebra.
