# Non-genus trace formula boundary

The surviving p24 construction can be phrased as a class-character trace
problem:

```text
T_s = sum_{g in Cl(O)} chi_s(g) * j_g
```

where `chi_s` ranges over characters of the desired quotient

```text
Cl(O)/H,       |Cl(O)/H| = 66254.
```

If these embedded traces were available, the rest is straightforward:

```text
DFT over the quotient -> H-periods -> degree-3107441 recovery polynomial.
```

This note checks whether known trace-of-singular-moduli formulas supply that
primitive.

## What the known trace formulas give

Zagier's trace theorem and the Bruinier-Funke generalization identify traces
of CM values of modular functions with coefficients of weight-`3/2` modular
forms or theta lifts.  Useful anchors:

```text
Bruinier-Funke, Traces of CM values of modular functions:
https://arxiv.org/abs/math/0408406

Bruinier-Jenkins-Ono, Hilbert class polynomials and traces of singular moduli:
https://uva.theopenscholar.com/ken-ono/publications/hilbert-class-polynomials-and-traces-singular-moduli

Choi, Twisted traces of singular moduli of weakly holomorphic modular functions:
https://arxiv.org/abs/1105.1223
```

These are powerful formulas for global traces and standard twisted traces.
They explain why genus-style characters and modular-curve traces are natural.

## Why this does not solve p24

The p24 character is not a fixed genus character or a bounded-level Dirichlet
twist.  It is a high-order unramified class-group character whose quotient has
order

```text
66254 = 2 * 157 * 211.
```

For the third trace the degree-2 part is exactly the genus quotient:

```text
D_K = -599 * 1089874116562502921057.
```

So known genus traces can at best supply a constant-bit top split.  The
remaining relative layers require order-`157` and order-`211` unramified
characters in the principal genus.

The group reason is simple: genus characters factor through `G/G^2`.  Here
`G` is cyclic of order `2*157*211*3107441`, so `G/G^2` has order `2` and
`G^2` has order `157*211*3107441`.  The Redei 4-rank is `0`, so no hidden
2-primary reflection layer refines this.  The odd `157` and `211` children
therefore live completely inside the kernel of every genus character.

As an automorphic object, such a character is a ring-class/Hecke character
with conductor tied to the p24 discriminant

```text
|D_K| = 652834595820939249713143 ~= 0.653*p.
```

The theta-lift or half-integral-weight formulation therefore moves the
problem into modular forms of discriminant/level scale.  Computing the needed
coefficient or toric period by the standard modular-form machinery is not a
sub-sqrt finite-field selector; it is another way to express the same
large-discriminant class-period computation.

The level audit makes the scale explicit:

```text
p24/non_genus_twisted_trace_level_audit.py

weight-1 dihedral level |D_K| proxy:       5.449371e22
half-integral trace level 4|D_K| proxy:    4.904434e23
sqrt(p):                                   1.000000e12
```

Thus "do the odd refinements by modular forms after genus" remains many
orders of magnitude above the desired finite-field square-root yardstick.

This matches the local toy evidence:

```text
p24/abstract_embedded_pairing_non_genus_toy.py
p24/tower_phase_refinement_toy.py
p24/oriented_composite_path_toy.py
```

Non-genus quotient data exists abstractly, but pairing it with the embedded
`j`-cycle requires exactly the relative phase data.

## Resulting theorem target

The positive theorem would have to be stronger than the known global trace
formulas:

```text
For a prescribed high-order unramified class character chi of a large
imaginary quadratic order, compute the embedded finite-field trace
sum_g chi(g) j_g mod p in time polynomial in the quotient/recovery degrees,
without enumerating the full class set or computing the height-scale class
polynomial.
```

I found no existing theorem of this shape.  The literature supports the
class-character reformulation, but not the sub-sqrt selector needed here.
