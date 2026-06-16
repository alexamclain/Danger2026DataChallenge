# Siegel-unit and split-cycle theorem attempt

This is the next pass on the missing embedded theorem.  I checked the two most
plausible ways to turn the abstract p24 class-field quotient into an actual
selector:

```text
1. explicit Siegel-Ramachandra / modular-unit generators;
2. split-prime cycle quotients in the horizontal CM isogeny graph.
```

The second route produces the sharpest concrete candidate so far, but still
lacks the root/cycle selector.

## Literature inventory

The relevant primary sources confirm the available explicit machinery:

```text
Gee-Stevenhagen, Generating class fields using Shimura reciprocity:
  CM values of level-N modular functions generate ray class fields, and
  Shimura reciprocity gives an explicit finite matrix action.

Jung-Koo-Shin, Ray class invariants over imaginary quadratic fields:
  singular values of certain Siegel functions generate K_(N) over K and
  there is an algorithm to find their conjugates.

Shin / Koo-Yoon, Siegel-Ramachandra invariants and smaller generators:
  quotients of Siegel-Ramachandra invariants can generate ray class fields
  with smaller class polynomials.
```

Useful references:

```text
https://arxiv.org/abs/1007.2317
https://arxiv.org/abs/1009.2253
https://arxiv.org/abs/1407.5713
```

What these theorems give:

```text
explicit generators of ray class fields;
explicit Shimura-reciprocity action;
smaller coefficient generators in many ray-class settings;
algorithms for all conjugates/minimal polynomials.
```

What they do not give for p24:

```text
an arbitrary unramified Hilbert subfield H^G;
a low-degree relation from an abstract quotient generator to j;
a way to compute a subgroup trace/norm without summing over that subgroup;
a root above p when Frobenius is trivial and every quotient splits.
```

The conjugate/minimal-polynomial algorithms still iterate over form classes or
ray classes.  The smaller-generator theorems prove primitivity of a chosen
ray-class generator; they do not supply a sublinear algorithm for the trace to
an arbitrary subgroup of the Hilbert class group.

## Split-prime cycle theorem shape

Let `O` be the target CM order and let `a` be a split prime ideal of norm
`ell`, with class `c=[a]` of order `n` in `Cl(O)`.  Over a prime where the CM
class polynomial splits and away from special automorphism cases, the
horizontal `ell`-isogeny graph on `Ell_O(F_p)` decomposes into cycles that are
orbits of `<c>`.

Thus:

```text
number of cycles = h/n
cycle length = n
```

For each cycle `C`, any symmetric expression such as

```text
s_C = sum_{j in C} j
```

is fixed by `<c>` and therefore lies in the embedded fixed field
`H^{<c>}`.  The polynomial

```text
prod_C (Y - s_C)
```

has degree `h/n`, and recovering a `j` from a selected `s_C` has degree `n`.

This is the exact embedded version of the abstract quotient.  It uses an
actual modular relation, because the vertices are ordinary CM `j`-invariants
and the edges are cut out by `Phi_ell(j,j')=0`.

## Toy proof-of-shape

I added:

```text
p24/split_cycle_quotient_toy.py
```

For the existing toy `D=-5000`, `q=1259`, `h=30`, the split prime `ell=11` has
class order `3`.  The horizontal `11`-isogeny graph on the 30 CM roots breaks
into ten 3-cycles:

```text
component_count=10
component_sizes=[3]
```

Plain `X0(11)` edge values do not quotient the class set:

```text
unordered_edges=30
distinct_edge_sums=30
distinct_edge_products=30
```

Whole-cycle symmetric values do:

```text
distinct_cycle_sums=10
cycle_sum_polynomial_degree=10
```

So the correct embedded object is not an edge invariant but a whole
split-prime-cycle invariant.

## p24 cycle candidates

I added:

```text
p24/p24_split_cycle_selector_audit.py
p24/composite_split_cycle_audit.py
```

Default run:

```text
python3 p24/p24_split_cycle_selector_audit.py --prime-bound 250000
```

Best observed formal splits:

```text
ell=7349:
  class_order = 487868237 = 157 * 3107441
  cycle_count = 422 = 2 * 211
  largest formal degree = 487868237 = 4.88e-4 * sqrt(p)
  X0(ell) edge degree = 7350
  seeded walk proxy = 7350 * 487868237 = 3.59 * sqrt(p)

ell=677:
  class_order = 655670051 = 211 * 3107441
  cycle_count = 314 = 2 * 157
  largest formal degree = 655670051 = 6.56e-4 * sqrt(p)
  X0(ell) edge degree = 678
  seeded walk proxy = 678 * 655670051 = 0.445 * sqrt(p)

ell=2:
  class_order = 102940198007
  cycle_count = 2
  largest formal degree = 102940198007 = 0.103 * sqrt(p)
  X0(ell) edge degree = 3
  seeded walk proxy = 3 * 102940198007 = 0.309 * sqrt(p)
```

Composite split ideals sharpen the formal candidates further:

```text
index 422:
  composite ideal = 2 * 919
  norm = 1838
  X0 index proxy = 2760
  class_order = 487868237

index 66254:
  composite ideal = 2 * 463 * 223^(-1)
  norm = 206498
  X0 index proxy = 311808
  class_order = 3107441
  seeded walk proxy = 968924963328 = 0.968925 * sqrt(p)
```

No single split prime below `250000` has index `66254`.  So the balanced
decomposed-CM split now has an explicit low-norm composite ideal representative
for its recovery cycle.  This is the sharpest formal embedded object so far:
quotient degree `66254`, recovery degree `3107441`, and a composite
correspondence degree proxy still below `sqrt(p)`.

The single-prime `ell=677` candidate still has the cheapest odd quotient of
size `314`; the composite index-66254 candidate trades a larger quotient for a
much smaller recovery degree.

The seeded-walk proxy separates two goals.  `ell=2` is the cheapest literal
single-prime walk after a seed, but it is still a constant-factor square-root
route asymptotically and has only a two-cycle quotient.  The odd smooth cycles
and the balanced composite cycle are better theorem targets because their
recovery degrees reflect the unusually smooth p24 class group; however, the
correspondence degree matters if the only algorithm is a literal modular walk.

The abstract quotient probe now also records these degrees:

```text
bnrclassno(bnr,314) = 314
bnrclassno(bnr,422) = 422
bnrclassno(bnr,66254) = 66254
bnrclassno(bnr,487868237) = 487868237
bnrclassno(bnr,655670051) = 655670051
```

## Missing theorem in its sharpest form

The current best theorem target is:

```text
Given the p24 target field and either the split prime ell=677 or the composite
ideal 2 * 463 * 223^(-1), construct one horizontal target CM cycle over F_p,
or one vertex on such a cycle, without first enumerating the CM root set.
```

Equivalent forms:

```text
1. compute one root of the embedded cycle-sum quotient polynomial and recover
   one j from the associated cycle in o(sqrt(p)) work;
2. construct the degree-422 or degree-314 embedded quotient polynomial without
   enumerating h vertices, and pair a quotient root with a cycle;
3. give a finite-field identity that recognizes one of these cycles directly
   from Phi_ell and the CM discriminant.
```

The toy test explains why the obvious `X0(ell)` edge relation is insufficient:
edge values still have full orbit.  The whole-cycle invariant is correct, but
the toy construction formed it from the embedded vertices.

## Character-period refinement

The cycle sums are inverse Fourier transforms of quotient-character twisted
traces.  I added:

```text
p24/character_period_transform_toy.py
p24/class_character_period_route_audit.py
p24/seedless_cycle_elimination_toy.py
p24/class_character_period_reframing.md
```

For `G=<g>` and `H=<g^m>` with `|H|=n`, the period sums

```text
y_r = sum_{k=0}^{n-1} j(g^{r+mk})
```

are recovered from

```text
T_s = sum_{i=0}^{h-1} zeta_m^{s*i} j(g^i)
```

by inverse DFT.  In the p24 candidates, the root-of-unity extensions over
`F_p` are modest:

```text
ell=7349 quotient m=422: extension degree 35
ell=677  quotient m=314: extension degree 156
```

So the new missing primitive is not Fourier inversion but computation of the
high-order, non-genus twisted traces `T_s` without summing over the CM class
group.

The tiny `D=-87`, `h=6`, `ell=7` elimination toy verifies the algebraic
identity directly:

```text
H_D(x_i)=0, Phi_7(x0,x1)=Phi_7(x1,x2)=Phi_7(x2,x0)=0,
Y=x0+x1+x2
```

eliminates to

```text
(Y - 29)*(Y - 4) over F_103.
```

But this uses `H_D`; at p24 that is the degree-`205880396014` object we are
trying not to construct.

## Present obstruction

This route is closer to an embedded theorem than the abstract
`bnrclassfield` tower, because it uses an explicit modular correspondence
`Phi_ell`.  However, it has not yet removed the seed problem.

For p24, an algorithm that starts with a target CM vertex can walk a
`7349`-cycle or `677`-cycle and stay below `sqrt(p)`.  But starting from no
vertex, the equations "there exists a closed horizontal cycle of length n"
appear to reintroduce the class equation.  The abstract degree-314/422
quotient knows that the cycles exist, but not which finite-field vertices
belong to one cycle.

So the missing theorem has moved from:

```text
find an arbitrary embedded class-field quotient
```

to the sharper:

```text
find one embedded split-prime CM cycle, or prove a cycle-sum/root pairing
identity, without a seed CM vertex.
```

That is progress in shape, but not yet the certificate.
