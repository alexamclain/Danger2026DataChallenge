# Embedded class-field tower worklog

This note sharpens the remaining smooth-class lead for the third strict p24
trace.  The target is not merely to know that class-field quotients exist; it
is to produce an embedded quotient or finite-field identity that selects a CM
`j` root over `F_p` without enumerating the full class set.

## Target data

```text
p = 1000000000000000000000007
sqrt(p) ~= 1000000000000
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = 205880396014 = 2 * 157 * 211 * 3107441
Cl(O_K) = cyclic of order h
conductor of Z[pi] in O_K = 2
conductor-2 ring-class multiplier = 1
```

The useful observed split-prime actions are:

```text
ell=23     generates the full class group
ell=2      generates the odd subgroup, index 2
ell=2897   generates subgroup index 157
ell=14057  generates subgroup index 211
```

The best decomposed-CM split is

```text
h = 66254 * 3107441.
```

If `g` is the class of the split prime above `23`, an ideal embedded quotient
would use the subgroup

```text
H = <g^66254>,        |H| = 3107441,
Cl(O_K)/H has degree 66254.
```

The full smooth tower can be written as:

```text
<g> > <g^2> > <g^314> > <g^66254> > 1
relative degrees: 2, 157, 211, 3107441
```

For a seed CM root `j_0`, the formal embedded invariant would be

```text
j_i = g^i(j_0)
y_r = sum_{k=0}^{3107440} j_{r + 66254*k}
V(Y) = product_{r=0}^{66253} (Y - y_r)
U_r(X) = product_{k=0}^{3107440} (X - j_{r + 66254*k}).
```

Then `deg V = 66254` and `deg U_r = 3107441`, both far below `sqrt(p)`.  This
is the right asymptotic shape.  The missing primitive is how to construct
`V` and one matching recovery polynomial `U_r` without first computing the
orbit `{j_i}`.

## Abstract quotient probe

I added:

```text
p24/p24_abstract_classfield_quotient_probe.py
```

Default run:

```text
python3 p24/p24_abstract_classfield_quotient_probe.py
```

Key output:

```text
bnf_cyc=[205880396014]
bnr_cyc=[205880396014]

request_n       quotient degree
2               2
157             157
211             211
66254           66254
3107441         3107441
205880396014    205880396014

bnrclassfield(bnr,2,1) = x^2 + 599
```

So PARI sees all abstract unramified quotient degrees, and the quadratic layer
is the genus field layer.  I also tried materializing the degree-157 defining
equation with a 1GB PARI stack; it was still running after several minutes and
was killed.  That is not a mathematical obstruction, but it confirms that
defining-equation materialization is not the intended certificate route.

The important distinction:

```text
abstract quotient field over K
  !=
embedded invariant with a computable relation to j
```

Reducing a `bnrclassfield` polynomial modulo the chosen prime can give split
roots in `F_p`, but by itself it does not label which root corresponds to which
coset of CM `j` roots, nor does it provide a recovery relation `R(alpha,j)=0`.

I added a tiny explicit check of this distinction:

```text
p24/abstract_vs_embedded_quotient_toy.py
```

For `D=-87`, the abstract degree-2 unramified quotient is

```text
bnrclassfield(bnr,2,1) = x^2 + 3.
```

Over `F_103`, this has roots `[10,93]`.  The embedded horizontal `ell=7`
cycle-sum quotient has roots `[4,29]`.  Both quadratics split over the same
field, but there are two possible affine pairings between their roots; the
abstract quotient polynomial alone does not choose one.  This is the small
degree version of the p24 problem: degree-314 or degree-422 quotient roots
must still be paired with recovery factors in `j`.

## Finite-field identity form

The equivalent finite-field selector problem can be phrased as either:

```text
1. find a low-degree quotient map q(j) whose fibers on the CM root set are
   exactly the H-cosets; or
2. find a class-action eigenfunction e(j) such that
      e(g*j) = chi(g) e(j)
   for a character chi of order 66254 or 3107441.
```

The second form would give quotient layers by Kummer/Fourier projection.  The
catch is that a generic function on the CM torsor has degree comparable to the
class set.  A useful identity must come from modular/class-field structure,
not from interpolation after the orbit is known.

I added a toy check:

```text
p24/embedded_selector_identity_toy.py
```

It reuses the existing `D=-5000`, `q=1259`, `h=30` embedded decomposition and
searches for a rational function `A(j)/B(j)` that returns the coset label.
The first valid selector appears at degree `15`, exactly the generic rational
interpolation threshold for `30` data points:

```text
data_pairs=30
generic_rational_interpolation_threshold=15
first_selector_degree=15
first_degree_equals_generic_threshold=1
low_degree_plain_j_identity_found=0
```

This does not prove impossibility for p24, but it rules out the naive hope that
the subgroup quotient is automatically a low-degree plain-`j` identity once an
embedded quotient exists.

## Shimura-reciprocity obstruction to standard invariants

Known class invariants from modular functions of level `N` have Galois action
described by Shimura reciprocity through finite congruence data.  Their
stabilizers are ray/congruence kernels and small modular automorphism groups.
They do not automatically equal an arbitrary large subgroup such as
`<g^66254>`.

For example, an `X0(ell)` edge invariant attached to a split `ell`-ideal has a
small map degree to `j`, but the class group still acts by translating the
starting vertex.  The order of the split ideal is the period of a walk in the
CM graph, not a stabilizer of the edge value.  The large stabilizer only
appears after taking orbit sums/products over the subgroup, which is the full
embedded-orbit operation we are trying to avoid.

## Proof obligations for a live route

A successful embedded tower proof now has to supply all of the following.

```text
1. A modular/class invariant f(tau), or a finite-field function f(j), whose
   stabilizer in Cl(O_K) is the desired subgroup H.
2. A way to compute the class polynomial or quotient polynomial for f at cost
   sublinear in h, preferably quasi-linear in the quotient degree.
3. An explicit recovery relation R(f,j) of degree at most |H| in j.
4. A root-selection rule over F_p that pairs one root of the quotient
   polynomial with the correct recovery factor, without enumerating all cosets.
```

At the moment we have (abstract) item 1 only if "invariant" is replaced by
"class-field quotient"; we do not yet have an embedded invariant or recovery
relation.  The current evidence says the promising path is not PARI
`bnrclassfield` materialization, and not a low-degree rational expression in
the plain `j` coordinate.  It would have to be a genuinely explicit
Shimura-reciprocity/Siegel-unit construction with the desired Artin kernel, or
an equivalent new finite-field identity tied to the `23`-isogeny class action.

## Sidecar-agent synthesis

Two parallel checks agreed with this boundary.

```text
Halley: split-prime ideals give excellent navigation data, but X0(edge)
        invariants still move through the full CM orbit; the ideal order is
        a walk period, not a stabilizer.

Hegel: principal-root and class-character selectors are not intrinsic after
       reduction modulo p.  Frobenius fixes the whole CM root torsor, so
       labeling one root as principal already requires an external anchor.
```

The shared recommendation is to reject future candidates unless they specify
both the Shimura-reciprocity stabilizer and the explicit relation back to `j`.

## Current sidecar synthesis

Two newer sidecar passes sharpened the same conclusion.

```text
Gauss: no standard theorem currently computes the high-order non-genus
       twisted traces.  Siegel-unit/ray-class methods enumerate conjugates;
       theta-series trace formulas have natural level |D_K|; global product
       formulas erase the required character phase.

Laplace: raw DANGER3 statistics are constant-factor filters or generator
         artifacts.  The only data-liftable positive invariant is the
         split-cycle/class-character period itself.
```

The live theorem target is therefore not a generic dataset statistic and not
an abstract quotient equation.  It must be an embedded high-order period
formula or an explicit finite-field split-cycle identity.

## Unit Distribution Exception Closed

Ohm's sidecar pass isolated the one modular-unit route still worth checking:
perhaps a Siegel/Ramachandra distribution relation collapses a relative norm
because the desired subgroup is a ray-kernel/local-unit kernel.

I added:

```text
p24/ray_kernel_distribution_audit.py
p24/unit_distribution_obstruction.md
```

The answer is negative for p24.  Ray distribution relations lower congruence
kernels in

```text
O_K^* -> (O_K/m)^* -> Cl_m(K) -> Cl(K) -> 1.
```

Those kernels map trivially to the ordinary Hilbert class group.  The p24
odd `157` and `211` layers lie inside the conductor-one class group after the
degree-2 genus split, so they are not ray-kernel layers.  Locally,
`Kronecker(D_K,157)=Kronecker(D_K,211)=-1`, and

```text
|(O_K/157)^*| = 157^2 - 1 = 24648
|(O_K/211)^*| = 211^2 - 1 = 44520
```

neither of which contains the corresponding prime factor.  The first
`ell`-primary ray factors appear only in the ramified `ell^2 -> ell`
filtration, whose image in `Cl(K)` is trivial.

So Siegel/Ramachandra/Weber normal-basis and distribution theorems still need
the same unramified relative class-character trace to touch the p24 odd
phase.

## Relative Phase Coefficient Compression Closed

I added:

```text
p24/tower_phase_coefficient_complexity_scan.py
p24/tower_phase_coefficient_complexity_boundary.md
```

This tests whether relative child-polynomial coefficients in embedded CM
towers have a small formula in the parent period.  The only universal
low-degree coefficient is the tautological one:

```text
coeff_{b-1} prod_v (Y - y_{u+a*v}) = -sum_v y_{u+a*v} = -Z_u.
```

After removing that forced coefficient, all informative coefficients in the
bounded small-CM runs had full interpolation degree:

```text
17/17 and 41/41 informative coefficient slots full-degree.
```

This closes a tempting compression route.  The p24 quotient tower can still
beat `sqrt(p)` with quotient-scale relative tables, but a successful theorem
must construct those tables or their equivalent relative character traces
from class-field structure, not from a low-degree parent-period identity.

## Phase-Lifted Certificate Surface

I added a finite verifier toy and spec:

```text
p24/phase_lifted_tower_certificate_toy.py
p24/phase_lifted_tower_certificate_spec.md
```

For the `D=-5000`, `h=30=2*3*5` toy, the verifier checks:

```text
top root -> relative child root -> selected recovery j-root
```

using `13` coefficient slots instead of the full `30`-root class set:

```text
chain_and_recovery_verify=1
selected_j_satisfies_full_H_D_sanity_check=1
```

The p24 analogue carries:

```text
2 + 2*157 + 314*211 + 3107441 = 3174011
```

field coefficients, or `3.174011e-6 * sqrt(p)`.  This is now the canonical
finite decomposed-tower artifact.  The missing theorem is not the verifier
shape; it is the embedded producer for the two odd relative phase relations
and the selected degree-`3107441` recovery polynomial.

The toy also records the smaller selected-chain variant:

```text
2 + 157 + 211 + 3107441 = 3107811
```

or `3.107811e-6 * sqrt(p)`.  This is valid when the arithmetic theorem
directly supplies the selected top root, selected degree-157 child polynomial,
selected degree-211 child polynomial, and selected recovery polynomial.  It is
not a new producer; it is a sharper statement of what the producer may output.

The matching lower-bound gate is:

```text
p24/lean/SelectorDegreeLowerBoundGate.lean
```

It formalizes the finite implication behind the selector-degree theorem:
any single embedded rational selector whose fiber contains an `H`-coset must
have degree at least `|H|`.  For the third trace this is exactly the recovery
scale

```text
|H| = 3107441 < 10^12,
```

so bounded selectors are ruled out while the selected-chain surface remains
comfortably sub-sqrt.

I separated this explicit selected-chain route from the alternative p-unit
producer route in:

```text
p24/selected_chain_vs_punit_producer_boundary.md
```

## Tower Section Gate

The seedless child-selection obstruction is now Lean-gated in:

```text
p24/lean/TowerSectionObstructionGate.lean
p24/tower_section_obstruction.md
```

It records the stabilizer logic behind the phase problem: a `G`-equivariant
selector from parent cosets to child cosets would force the parent stabilizer
`K` to fix the selected child, hence `K <= L`.  For a genuine refinement
`L < K`, this is impossible.

So the phase-lifted tower route must supply unordered relative child
relations or relative class-character traces.  A canonical child section is
not available as a seedless modular construction.

The consolidated current theorem form is:

```text
p24/phase_theorem_current_form.md
```

The relative Kummer normal form for the same phase payload is:

```text
p24/relative_kummer_phase_normal_form.md
```

The current abstract-tower and complement-generator boundaries are:

```text
p24/abstract_tower_fiber_map_boundary.md
p24/abstract_tower_morphism_payload_boundary.md
p24/complement_subgroup_generator_boundary.md
```

Together they say that split abstract root sets are not a tower morphism, that
an honest full relative morphism is still a sub-sqrt payload if produced
class-set-free, and that no low-norm split-prime-power word of norm at most
`66254` generates the useful relative factors inside the balanced complement
`K`.
