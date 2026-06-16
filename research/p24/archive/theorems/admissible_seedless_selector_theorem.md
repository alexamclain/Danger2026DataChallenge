# Admissible Seedless Selector Theorem

This note is a consolidated theorem statement for the p24 embedded selector
work.  It is deliberately conditional: it closes bounded, natural, modular
and abstract-tower selectors, but it does not rule out the surviving
degree-`3107441` non-genus relative-period construction.

## Setup

Let `O` be a strict p24 CM order and let

```text
G = Cl(O)
```

act simply transitively on the embedded ordinary CM root torsor

```text
J = {j_g : g in G} <= F_p.
```

Let `H <= G` be the subgroup whose cosets are the desired quotient fibers.
For the best third-trace target,

```text
|G| = 205880396014 = 2 * 157 * 211 * 3107441,
|G/H| = 66254,
|H| = 3107441.
```

For the clean order-19 theorem toy,

```text
|G/H| = 19,
|H| = 14670196166.
```

## Admissible Construction Model

Call a seedless construction admissible if it is built from the following
data without inserting an external CM root or prime-above-`p` label:

```text
1. prime-to-p modular correspondences or elimination covers;
2. rational functions regular on the ordinary CM points;
3. bounded-norm oriented Hecke words and additive combinations of them;
4. abstract class-field quotient equations and compatible tower equations;
5. genus data from ramified discriminant factors, Kronecker symbols,
   quadratic subfields, or genus characters.
6. Siegel/Ramachandra/Weber modular-unit values, Shimura-reciprocity
   conjugation, ray-class norm/distribution relations, and Kummer extraction
   after adjoining quotient roots of unity.
```

Assume also:

```text
A. scalar coordinates are rational functions on irreducible covers with pole
   degree B;
B. the construction is natural for the hidden G-action, so translating the CM
   origin translates all labels;
C. additive oriented Hecke identities restrict to group-algebra operators on
   the CM torsor, or else their all-torsor vanishing relation has pole degree
   below |G| and passes the Tate-cusp nonidentity test;
D. no denominator/pole collapse occurs on the reduced ordinary CM locus.
```

These hypotheses are exactly where a future positive construction must differ
if it wants to evade the theorem.

## Theorem

Under the admissibility hypotheses:

```text
1. Any scalar coordinate that is constant on H-cosets has degree at least |H|.
2. Any additive oriented Hecke formula that produces an H-period has collected
   class-translation support at least |H|.
3. An abstract class-field quotient tower reduced modulo p does not pair its
   roots with embedded j-periods; compatible pairings are torsors.
4. A seedless tower cannot choose one child above each parent in a nontrivial
   layer.
5. Genus-only data factors through G/G^2 and is constant on the principal
   genus.
6. Ray/modular-unit distribution relations collapse only ray-kernel or
   local-unit directions; for the p24 odd layers they do not remove the
   unramified Hilbert-class projection.
```

Consequently, for the third p24 trace, no admissible bounded local identity,
abstract quotient equation, genus label, or sparse Hecke projector can supply
the missing odd `157`/`211` embedded phase.  Any admissible embedded quotient
selector must pay at least

```text
|H| = 3107441
```

in degree or support, and it must include genuinely non-genus relative period
data.

## Proof

For scalar coordinates, choose a finite value of the coordinate on one
`H`-coset.  Its fiber contains all `|H|` distinct CM points in that coset.
The degree of a rational function bounds the degree of every fiber, so
`B >= |H|`.  This is the finite-field fiber-degree theorem:

```text
p24/finite_field_selector_degree_theorem.md
```

For additive oriented Hecke formulas, the restriction to the CM torsor is a
group-algebra element

```text
L in F_p[G].
```

If reduced normality/faithfulness holds and `L` produces the `H`-period, then
`L` and the subgroup projector

```text
e_H = sum_{h in H} [h]
```

act identically on every translate of `j`; faithfulness forces `L=e_H`, whose
support is `|H|`.  This is the structural support lemma:

```text
p24/structural_lifting_support_lemma.md
```

The exact statement without full reduced normality is cyclic-code theoretic:

```text
exact additive selectors = e_H + Ann(J),
required lower bound = min_{B in Ann(J)} wt(e_H + B) = |H|.
```

The quotient-spectrum refinement

```text
p24/quotient_spectrum_support_theorem.md
```

shows that quotient-character nonvanishing is enough only for operators
already known to descend to `G/H`.  General sparse Hecke-word formulas still
need full reduced normality or the direct minimum-weight statement.

For bounded p-specific vanishing accidents, subtract two representatives in
the same `H`-coset.  The difference vanishes on the whole CM torsor.  If the
pole degree is below `|G|`, the finite-field zero lemma forces a global
mod-`p` identity, and Tate-cusp pole orders rule out the usual bounded
low-norm Hecke-word identities:

```text
p24/finite_field_modular_zero_lemma.md
```

For abstract class-field towers, choose the ordinary prime `frak_p | p` of
`K`.  Since it splits completely in the ring class field `L_rc`,

```text
O_{L_rc^H} tensor_{O_K} F_p ~= product_{G/H} F_p.
```

The roots of an abstract quotient polynomial are a `G/H`-torsor of primes
above `frak_p`.  The embedded period quotient is another `G/H`-torsor, and a
pairing between them is extra data.  This is:

```text
p24/prime_torsor_obstruction_theorem.md
```

The no-child-selector statement is the same torsor fact layer by layer.  If
`H_child < H_parent`, a `G`-equivariant section

```text
G/H_parent -> G/H_child
```

would force `H_parent <= H_child`, impossible.  See:

```text
p24/tower_section_obstruction.md
```

Finally, genus characters factor through `G/G^2`.  In the third p24 target,
`G/G^2` has order `2`, so genus data can identify only the top quadratic
layer.  The odd `157` and `211` refinements live in the principal genus:

```text
p24/genus_odd_phase_obstruction.md
```

For modular-unit and ray-class distribution relations, use the exact sequence

```text
O_K^* -> (O_K/m)^* -> Cl_m(K) -> Cl(K) -> 1.
```

The kernel of a ray-modulus lowering map is represented by principal ideals
with congruence conditions, so its image in the ordinary Hilbert class group
is trivial.  The p24 odd `157` and `211` layers are conductor-one unramified
class-group layers inside the principal genus, not ray-kernel layers.  The
local audit shows that `Kronecker(D_K,157)=Kronecker(D_K,211)=-1` and that
`|(O_K/ell)^*|=ell^2-1` has no corresponding `ell`-factor; the first
`ell`-primary ray factors occur only in the ramified `ell^2 -> ell`
filtration.  See:

```text
p24/unit_distribution_obstruction.md
p24/ray_kernel_distribution_audit.py
p24/ray_kernel_embedding_boundary.md
```

The auxiliary-prime variant is covered by the same verticality argument.  One
can choose small rational primes whose ray norm-kernel modulo units contains
`157` or `211`, but the kernel still acts only on level structure above a
fixed level-1 CM root.  Any operation using only this local kernel becomes a
ray-class construction vertical over `j`, while any operation whose character
is nontrivial in `Cl(K)` has reintroduced the original unramified class-period
projection.

## What This Leaves Open

The theorem does not exclude a deliberate growing-degree embedded object of
degree `3107441`.  The surviving positive route is still:

```text
compute embedded non-genus relative class-character traces
T_s(aK) = sum_{k in K} chi_s(k) j_{ak}
```

for the odd `157` and `211` layers, then use inverse Fourier transform to
produce the relative child polynomials and recover a `j` root.

Equivalently, a successful construction must provide an explicit embedded
class-field generator with:

```text
1. Artin kernel H or the prescribed tower kernels;
2. a relation back to j of final degree at most 3107441;
3. a way to compute the relation modulo p without enumerating Cl(O) or H_D;
4. no reliance on genus data for the odd layers.
5. no reliance on ray-distribution collapse for the unramified odd layers
   unless it supplies an embedded relation to `j` rather than an abstract ray
   torsor.
```

That is the remaining theorem target.  Everything weaker is now either an
abstract unpaired tower, a bounded local identity, a genus-only label, or a
support-sized projector/ray-kernel norm.
