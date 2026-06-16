# CM Subfield/Tower Boundary

This note records the current status of the "use modern CM subfield/tower
algorithms" route.

## Why it is tempting

CM class-polynomial software does more than print the full Hilbert class
polynomial.  For suitable class functions it can:

```text
1. use smaller class invariants than j;
2. compute the class field as a tower of relative extensions;
3. sometimes choose a strict subfield of the class field;
4. recover j from a modular polynomial relating the class invariant to j.
```

This sounds close to the p24 target, because the third trace has

```text
h = 205880396014 = 66254 * 3107441
```

and the desired certificate shape would be:

```text
quotient/subfield degree = 66254
recovery degree          = 3107441
```

Both are far below

```text
sqrt(p) = 1000000000000.
```

## Exact positive requirement

To solve the p24 construction this way, a class function `f` must satisfy all
of:

```text
1. f(tau) lies in the p24 ring class field for
   D_K = -652834595820939249713143.

2. The stabilizer of f(tau) inside Cl(O_K) is the specific subgroup
   H = <g^66254>, |H| = 3107441.

3. The minimal polynomial of f(tau) has degree 66254, or a tower with relative
   degrees 2,157,211, and can be computed modulo p without enumerating all h
   CM classes.

4. There is an explicit relation R(f,j)=0 whose degree in j is at most
   3107441 and whose roots are paired with the same embedded H-cosets.

5. Reducing the tower over F_p and choosing compatible roots gives a j-root
   for the target isogeny class.
```

If such an `f` is found, the asymptotic shape is exactly what we want.
Arbitrary root choices in the finite-field tower are then acceptable because
the embedded recovery relation supplies the pairing back to `j`.

## Why generic CM subfield support is not enough

The standard subfield/tower machinery does not let us request an arbitrary
class subgroup.  It starts from a modular function or eta/Siegel/Atkin class
invariant whose Galois action is determined by Shimura reciprocity and level
congruence data.  The resulting stabilizer is whatever that function has.
For p24, that stabilizer must contain the odd unramified phases `157` and
`211` inside the principal genus.

The local p24 audits already rule out the easy sources of those phases:

```text
genus characters:
  only the top factor 2; the 157 and 211 layers live in G^2.

ray/kernel distribution:
  collapses principal congruence kernels, not the conductor-one Hilbert class
  subgroup H.

low-level X0/Atkin/eta edge invariants:
  have small modular degree but full class orbit; the ideal order is a walk
  period, not a stabilizer.

abstract bnrclassfield towers:
  give split roots over F_p, but no embedded relation pairing those roots to
  H-periods or recovery factors in j.
```

In other words, a CM package option called "subfield" may produce a smaller
polynomial, but unless its stabilizer is exactly the p24 `H` and its modular
polynomial recovers `j` with the correct coset pairing, it does not solve the
DANGER certificate.

## Finite-field obstruction restated

The obstruction is not root extraction.  If the right embedded tower exists,
then over the p24 prime all the relevant polynomials split and any compatible
root chain gives some target CM root.

The obstruction is producing the embedded tower itself.  The prime above `p`
splits completely in the ring class field, so an abstract tower has a torsor
of roots at each layer.  Pairing that torsor with the embedded CM `j`-torsor
is exactly the missing phase data.

The small audits in

```text
p24/cm_package_subfield_pairing_audit.md
p24/abstract_embedded_pairing_non_genus_toy.py
p24/embedded_selector_identity_toy.py
```

make this finite-field obstruction concrete.  In the non-genus degree-5 toy,
the abstract quotient roots and embedded component-period roots both split but
have no affine/Mobius pairing.  In the `D=-5000`, `h=30` selector toy, the
first rational function of the plain `j` coordinate that recovers the quotient
label appears only at degree `15`, exactly the generic interpolation threshold
for `30` data points.

The graph-relation follow-up

```text
p24/abstract_embedded_graph_relation_scan.py
```

checks equations `S(A,Y)=0` between abstract quotient roots and embedded
period roots.  For the degree-5 toy, `(1,1)` has no relation, while `(1,2)`
and `(2,1)` relations exist for all matchings and for random controls too.
So existence above the coefficient-count threshold is just interpolation; the
missing tower primitive must provide a canonical relation, not merely any
finite-field graph equation.

Equivalently, the relative tower refinements require the nontrivial traces

```text
T_s(aK) = sum_{u in K/L} zeta_r^(s*u) y_{a u L}
```

for the `157` and `211` layers.  These are not supplied by the degrees of the
abstract tower.

## Current conclusion

The CM subfield/tower route is a valid positive route only if it supplies a
specific embedded class invariant with stabilizer

```text
<g^66254>
```

and an explicit relation back to `j`.

No such invariant is currently identified.  Existing CM subfield support,
class-field tower decompositions, and smaller eta/Siegel invariants improve
ordinary CM computations, but as currently understood they either:

```text
1. still enumerate the class action;
2. produce an abstract unpaired class-field tower;
3. give a subfield unrelated to the p24 H; or
4. reduce coefficient heights only by constants.
```

So this route remains open as a precise search target, not a solved
construction.
