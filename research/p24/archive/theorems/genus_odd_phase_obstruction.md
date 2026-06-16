# Genus Data Cannot Select Odd Tower Phases

This note records the group-theoretic closure behind the `-599` genus-factor
temptation.

## Theorem

Let `G = Cl(O)` and let `Gen(G)` be the quotient seen by genus characters.
For an imaginary quadratic order this quotient is

```text
G / G^2.
```

Any selector whose only class-field information comes from ramified prime
discriminants, Kronecker symbols, quadratic subfields, or genus characters
factors through `G/G^2`.  Therefore it is constant on the principal genus
`G^2`.

If a desired refinement lies inside `G^2`, genus data cannot distinguish its
children.

## p24 third trace

For the certificate-oriented third trace:

```text
D_K = -652834595820939249713143
    = -599 * 1089874116562502921057

G = Cl(O_K) cyclic of order
  205880396014 = 2 * 157 * 211 * 3107441.
```

Thus

```text
G/G^2 has order 2
G^2 has order 157 * 211 * 3107441 = 102940198007.
```

The degree-2 tower layer is exactly the genus layer; it corresponds to the
quadratic field `Q(sqrt(-599))` (equivalently the complementary prime
discriminant factor).

The needed odd tower refinements

```text
157 and 211
```

live entirely inside the principal genus `G^2`.  Any construction using only
genus/reflection/quadratic data is constant on this subgroup and cannot label
these children.

The Redei audit also gives:

```text
4-rank = 0.
```

So there is no hidden `4`- or `8`-rank layer refining genus before the odd
part.  The next information after genus is genuinely odd, non-genus class
character data.

## Consequence

The `-599` factor can supply at most the top degree-2 split.  It cannot
produce an embedded root selector for the `157` or `211` layers, nor a seed
for the recovery cycle.

The remaining positive theorem is still:

```text
compute embedded non-genus class-character traces on the principal genus,
especially of orders 157 and 211.
```

Supporting scripts:

```text
p24/genus_character_quotient_audit.py
p24/redei_4rank_audit.py
p24/odd_relative_phase_source_audit.py
```
