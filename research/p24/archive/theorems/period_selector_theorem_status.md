# Period-selector theorem status

This note records the current state of the attempted embedded class-field
theorem for the strict p24 traces.  There are two useful notions of "best":
the first trace gives the cleanest small-character theorem target, while the
smooth third trace still gives the best balanced certificate target.

See also:

```text
p24/all_trace_period_frontier.md
p24/embedded_selector_theorem_attempt.md
p24/structural_lifting_support_lemma.md
p24/all_target_split_cycle_audit.py
p24/all_trace_composite_order_search.py
p24/period_target_tradeoff_audit.py
p24/composite_orientation_ambiguity_audit.py
p24/composite_orientation_toy.py
p24/composite_orientation_degree_tradeoff.py
p24/oriented_composite_path_toy.py
```

## Best Theorem Toy Target

The cleanest small-character theorem target is the first strict trace:

```text
t = 1020608380936
D_K = -739589633190799177940983
h = 278733727154 = 2 * 19 * 7335098083
Cl(O_K) cyclic

ell=19:
  cycle_count = 19
  cycle_length = 14670196166 = 2 * 7335098083
  X0 degree = 20
  seeded_walk_proxy = 293403923320 = 0.293404 * sqrt(p)
  root_of_unity_extension_degree = 2
```

Equivalently, the missing primitive is an embedded order-19 class-character
period computation, paired back to `j`, without class enumeration.

But its recovery degree is still `14670196166`, so this is not the best
certificate target.  It is a simpler model of the missing non-genus period
theorem.

## Order-19 Kummer/Hecke Narrowing

I added focused audits for the first-trace order-19 target:

```text
p24/order19_kummer_shortcut_audit.py
p24/order_l_kummer_phase_toy.py
p24/order19_component_mover_audit.py
p24/order19_ring_ray_sequence_audit.py
p24/hecke_projector_barrier_audit.py
```

The good news is that the quotient is as clean as it looked:

```text
p mod 19 = -1
zeta_19 is in F_{p^2}
the split prime above 2 has full class-group order h
its image moves the 19 components with quotient log 1
Phi_2 and Phi_19 give a combined local level proxy 60
```

So orientation of the quotient components is cheap once the components exist.
The bad news is that none of this constructs the component periods.  The
Kummer/Fourier layer only says

```text
T_s = sum_i zeta_19^(s*i) j_i,        T_s^p = T_{-s}
y_r = (1/19) sum_s zeta_19^(-s*r) T_s.
```

It diagonalizes an already oriented period vector over `F_{p^2}`.  Because the
prime `p` splits completely in the Hilbert class field, the degree-19 quotient
also splits completely over `F_p`; passing to `F_{p^2}` does not create a
Frobenius orbit or canonical root.

The ring/ray exact sequence rules out the most tempting level-19
reinterpretation:

```text
ring class conductor 19 kernel = 18
ray modulus one split prime above 19 kernel = 9
first ray kernel with a factor 19 occurs at prime-square modulus and is ramified
```

Thus the unramified degree-19 quotient is a quotient of the base class group,
not a small-conductor layer.

Finally, the group-algebra projector bookkeeping makes the remaining missing
piece explicit.  If `h = 19*n`, the component period applies

```text
e_H = sum_{k=0}^{n-1} g^{19*k},  n = 14670196166.
```

The split prime over 2 gives a full generator `g`, but the exact projector has
support `n`.  Using the unoriented `Phi_19` adjacency inside `H` still needs
radius at least `n/2`.  Escaping this support bound is precisely the desired
nonlocal high-order class-character trace theorem; local low-degree
correspondences do not supply it by themselves.

Banach sharpened the no-go boundary: the support argument is rigorous only
after a proposed finite-field formula is known to restrict to a sparse
group-algebra operator on the CM torsor, or to the same order-19 character
traces.  A complete exclusion of all bounded `Phi_2`/`Phi_19` identities would
need a faithfulness/lifting lemma:

```text
any bounded-degree, bounded-height formula in the local correspondences that
produces the component periods mod p must lift to a characteristic-zero
identity on the CM torsor, unless p is smaller than the formula height.
```

Toy scans give the expected negative signal, but this is the exact theorem gap
if one wants to rule out accidental one-prime collapses rather than merely
ordinary local-Hecke projectors.

I also tested the tempting high-power-generator variant in:

```text
p24/power_level_stabilizer_toy.py
p24/order19_power2_level_audit.py
p24/generator_crater_sequence_complexity.py
p24/local_coset_invariant_scan.py
p24/normal_basis_support_toy.py
p24/singular_moduli_normality_bound.py
p24/finite_field_lifting_height_audit.py
p24/class_invariant_lifting_height_audit.py
p24/modular_function_degree_lower_bound.py
p24/finite_field_selector_degree_theorem.md
p24/finite_field_modular_zero_lemma.md
p24/relative_coset_polynomial_height_audit.py
p24/relative_coset_phase_toy.py
p24/tower_phase_refinement_toy.py
p24/class_field_tower_phase_audit.md
p24/non_genus_trace_formula_boundary.md
p24/exact_trace_crt_modular_degree_barrier.py
p24/abstract_embedded_pairing_non_genus_toy.py
p24/principal_singular_modulus_reduction_audit.py
p24/frobenius_principal_ideal_origin_audit.py
p24/near_singular_window_audit.py
p24/near_singular_window_audit.md
p24/low_height_formula_window_audit.py
p24/low_height_formula_window_audit.md
p24/fixed_trace_cm_root_toy.py
p24/fixed_trace_cm_root_toy.md
p24/tower_section_obstruction.md
p24/relative_tower_character_toy.py
p24/odd_relative_phase_source_audit.py
p24/odd_relative_phase_source_audit.md
p24/genus_odd_phase_obstruction.md
p24/correspondence_recurrence_resultant_boundary.md
p24/hecke_correlation_trace_boundary.md
p24/period_correlation_idempotent_toy.py
p24/reduced_resolvent_vanishing_scan.py
p24/reduced_resolvent_normality_boundary.md
p24/smooth_torsor_search_tradeoff_audit.py
p24/smooth_torsor_search_boundary.md
p24/admissible_seedless_selector_theorem.md
p24/prime_torsor_obstruction_theorem.md
p24/direct_verifier_ray_section_theorem.md
p24/p23_transfer_to_p24_scaling_audit.md
```

On the complete `D=-5000`, `h=30` CM torsor, the norm-3 ideal is a full
generator.  For moves `m = 2,3,5,6,10,15`, oriented paths

```text
j_i -> j_{i+1} -> ... -> j_{i+m}
```

model level `3^m` data.  Endpoint and path invariants kept essentially the
full orbit of 30 starts; the quotient degree appeared only after aggregating
the whole subgroup `<g^m>`.  This is the toy analogue of the first-trace
`2^19` temptation: a high-power generator-level modular datum is a long edge
or path, not automatically a class invariant with stabilizer `<g^19>`.

For the actual first trace:

```text
X0(2^19) -> X(1) degree = 786432 = 7.86432e-7 * sqrt(p)
horizontal edge (j_i, j_{i+19}) class orbit = h = 278733727154
desired projector support = h/19 = 14670196166
```

So level `2^19` has a small map to `j`, but the specific horizontal class
edge still has the full class orbit.  It is not a degree-19 invariant unless
one also applies the same subgroup projector.

The generator-crater sequence scan tests the easy Serre-Tate/Landen hope at
toy scale.  In eight complete CM examples with a small split prime generating
the full CM cycle, the raw `j_i` sequence and simple transforms

```text
j_i, j_{i+1}-j_i, j_{i+1}/j_i, j_i+j_{i+1}, j_i*j_{i+1}
```

have Berlekamp-Massey complexity essentially equal to the full class number.
This does not rule out a deep formal-coordinate identity, but it gives no
support for a low-recurrence finite-field crater coordinate.

The local-coset invariant scan searches directly for bounded-degree formulas
`F(j_i,...,j_{i+w-1})` that are constant on cosets `i mod m` without whole
subgroup aggregation.  On the `D=-5000`, `h=30` generator cycle, there are no
nonconstant invariants for `w <= 3`, degree `<= 3` in the meaningful quotient
cases.  The only positive row is the degenerate `m=15` case, where the subgroup
order is `2` and the local window already covers more than a component.  This
supports the projector barrier for bounded local identities, while still
leaving the stated faithfulness/lifting gap for accidental p-specific
congruences.

The normal-basis support toy checks the exact algebraic hypothesis behind this
barrier.  For a CM cycle it forms `J(T)=sum_i j_i*T^i` in
`F_q[T]/(T^h-1)`.  When `gcd(J,T^h-1)=1`, the translates of `j` are a normal
basis for the cyclic torsor, and any group-algebra operator that produces an
`H`-period must equal the full projector `e_H`.  In the small rows tested, this
normality holds, so the support lower bound is exact at toy scale.

For the p24 target discriminants, characteristic-zero normality is no longer
just toy evidence.  The conductor-2 discriminant `Delta=t^2-4p` has a unique
principal reduced form with `a=1`, and all other reduced forms have `a>=2`.
Using the standard singular-modulus estimate

```text
||j(tau)| - exp(pi*sqrt(|Delta|)/a)| <= 2079
```

the principal conjugate dominates the sum of all other conjugates by an
astronomical margin.  Hence every class-character resolvent is nonzero and
`j` is a normal element for the p24 CM torsors in characteristic zero.  This
does not prove reduced normality at the chosen split prime.  The remaining
negative-theorem gap is exactly the p-adic unit/lifting step for finite-field
formulas.

I also checked the simplest possible lifting proof by norm heights.  It fails:
`log |j_principal|` is around `5e12`, while `log(p)` is only about `55`.
Therefore divisibility of a residual norm by `p^h` would not force a
characteristic-zero identity for any formula with ordinary singular-modulus
height.  The lifting lemma, if true, has to use structural modularity or
bounded-level geometry rather than crude archimedean height.

The same is true for known smaller class invariants at constant-factor height
scale.  Even an optimistic `1/28` height factor leaves log-size around
`1e11`, far above `log(p)`.  Smaller coefficient CM polynomials help
implementation, but they do not turn finite-field congruence into a
characteristic-zero identity here.

The modular-degree bound gives a complementary structural obstruction for
single class-invariant values.  A degree-`d` modular function can merge at
most `d` distinct `j`-roots in one fiber; an `H`-coset invariant of size `n`
therefore requires degree at least `n`.  This rules out all fixed-level
class-invariant selectors.  It does not rule out a growing-level degree-`n`
object for the third target, but such an object has already paid the recovery
degree and still needs an embedded recovery relation.

I sharpened this into a purely finite-field theorem in:

```text
p24/finite_field_selector_degree_theorem.md
```

If a rational function on any irreducible finite modular-correspondence cover
is regular at the embedded CM points and constant on `H`-cosets, then one
fiber contains `|H|` distinct CM points.  Therefore the function degree is at
least `|H|`.  This does not rely on characteristic-zero lifting, coefficient
height, or the normality of `j`.  It covers bounded-depth correspondence
covers and algebraic elimination/resultant covers, not just functions on
`X(1)`.

So bounded local finite-field identities are now excluded at the theorem
level.  The surviving positive route has to be a growing-degree object: for
the third target, degree at least `3107441`, plus an embedded quotient-phase
construction that does not enumerate the full class set.

I also added a finite-field modular zero lemma:

```text
p24/finite_field_modular_zero_lemma.md
```

A nonzero rational modular function on a prime-to-`p` correspondence cover
cannot vanish at more CM points than its pole degree.  Therefore a bounded
local identity that vanishes on the whole p24 CM torsor would have to be a
global mod-`p` modular identity.  For ordinary linear Hecke-word combinations,
the Tate-cusp pole orders `j(q^N)=q^{-N}+...` rule out such identities when
the selected correspondence words have distinct low norms.  This replaces the
failed height-lifting argument in the bounded-level regime, but again leaves
the intended degree-`3107441` growing object untouched.

The principal-coset relative polynomial route is the natural growing-degree
version:

```text
R_H(X)=prod_{a in H}(X-j(a)),   deg R_H = |H| = 3107441.
```

Degree-wise this is attractive and sub-sqrt, and any root of `R_H mod p`
would be a target root.  But `R_H` is a relative polynomial, not a rational
integer polynomial; its coefficients live in the quotient field and require an
embedded quotient phase before reduction modulo `p`.  Symmetrizing over all
phases recovers the full class polynomial.  Ordinary CM/class-polynomial
computation is also height-limited: the principal conjugate has log-size
around `5e12`, while `log p` is only `55`.  Computing `R_H mod p` by complex
approximations or CRT without already knowing mod-`p` roots would require
height-scale information, so this is not yet an algorithmic selector.

I tested the smoother class-field tower variant in:

```text
p24/tower_phase_refinement_toy.py
p24/class_field_tower_phase_audit.md
```

The toy `D=-5000`, `h=30=2*3*5` decomposes a quotient of size `6` through a
degree-2 top period and relative degree-3 child polynomials.  This is the
same formal shape the third target wants with `66254=2*157*211`: small visible
root degrees followed by the recovery degree.  But the relative child
polynomials are extra embedded phase data; in the toy they were constructed
from the actual `j`-cycle.  The top polynomial and abstract quotient
factorization do not determine them.

So a tower remains a formal sub-sqrt route, but the missing primitive is now
more precise:

```text
compute embedded relative class-period refinements along the quotient tower
2 -> 157 -> 211 without full class enumeration.
```

Two refinements make this sharper.  First, fixed-trace construction is not a
separate selector: in the `p=103`, `t=8` toy, the fixed-trace `j`-set is
exactly `roots(H_-87) union roots(H_-348) mod 103`, so fixed trace names an
isogeny class/volcano rather than a particular embedded CM root.

Second, a seedless tower cannot canonically label children.  For a nontrivial
layer `L <= K <= G`, there is no `G`-equivariant section `G/K -> G/L` unless
`K=L`: if `s(K)=aL`, equivariance under every `k in K` gives `kaL=aL`, hence
`K <= L`.  This leaves unordered relative child polynomials as the viable
tower object, but rules out a canonical child label coming from abstract
quotient structure alone.

The new relative-character toy verifies the replacement primitive.  In the
`D=-5000`, `h=30` tower, the degree-3 child polynomials above the two top
roots are inverse DFTs of relative traces on `K/H`; since `F_1259` lacks a
primitive third root of unity, the nontrivial traces live in `F_{1259^2}` and
descend back to child periods in `F_1259`.  Thus the p24 tower theorem now
reduces to embedded non-genus relative class-character traces for the odd
`157` and `211` refinements.  The top degree-2 layer is only the known genus
split for

```text
D_K = -599 * 1089874116562502921057.
```

Equivalently, the genus quotient is `G/G^2` of order `2`, and the principal
genus `G^2` has order `157*211*3107441`.  Any construction using only
ramified prime discriminants, quadratic subfields, Kronecker symbols, or genus
characters is constant on `G^2`, so it cannot label the odd `157`/`211`
children.  The Redei audit gives 4-rank `0`, so there is no hidden
2-primary refinement beyond genus.

I also checked the visible arithmetic sources for those odd phases:

```text
p24/odd_relative_phase_source_audit.py
```

The quotient roots of unity are cheap:

```text
ord_157(p) = 156
ord_211(p) = 35
ord_33127(p) = 5460
```

but this is only the Fourier layer.  The small cyclotomic quadratic subfields
are `Q(sqrt(157))`, `Q(sqrt(-211))`, and `Q(sqrt(-599))`; none is the target
field `Q(sqrt(D_K))`, except that `-599` is the known genus factor.  A
Jacobi-sum construction for the actual target CM field would need conductor
divisible by `|D_K|`, where

```text
ord_|D_K|(p) = 14812380038735835154352.
```

That is far above the `sqrt(p)` yardstick.

I also checked the trace-of-singular-moduli literature boundary in:

```text
p24/non_genus_trace_formula_boundary.md
```

Known Zagier/Bruinier-Funke/Bruinier-Jenkins-Ono-style trace formulas explain
global traces and standard twisted traces as coefficients of weight-`3/2`
modular forms or theta lifts.  They do not currently give a finite-field
algorithm for the high-order unramified class-character traces needed here:

```text
T_s = sum_g chi_s(g) j_g,    chi_s on Cl(O)/H of order dividing 66254.
```

The automorphic formulation moves the computation to discriminant/level scale
`|D_K| ~= 0.653*p`, so it is a reformulation of the missing class-period
primitive rather than a sub-sqrt selector.

The non-genus abstract-vs-embedded toy strengthens the phase warning.  For
`D=-2239`, `h=35`, `ell=5`, the abstract degree-5 Hilbert quotient and the
embedded degree-5 cycle-period quotient both split over `F_2243`, but there
is no affine or Mobius map between their root sets.  Abstract class-field
roots and embedded period roots are not related by a visibly simple finite
field coordinate change in this small non-genus example.

The direct-principal-root idea fails for the same reason.  Over `C`, the
principal singular modulus is distinguished by the dominant `a=1` conjugate.
But reducing an algebraic integer modulo a completely split prime requires
choosing a prime above `p`, equivalently choosing one root of the class
polynomial modulo `p`.  The complex principal embedding does not select that
finite-field prime.  Computing the actual integer first is also height-scale:
for the third p24 trace, `log |j_principal|` is about `5.08e12`.

The Frobenius version of the same idea is also closed.  For fixed `p,t`, the
element `pi=(t+sqrt(Delta))/2` is principal and has norm `p`, so `p` splits
completely in the target ring class field.  But this makes Frobenius act as
the identity on every target root over `F_p`; it fixes the whole torsor and
does not label an origin.

Locke's lifting sidecar sharpened the no-go theorem into a conditional
structural lemma.  Under explicit hypotheses (additive oriented horizontal
correspondences, good reduction/no pole collapse, equivariance on the whole
CM torsor, and reduced normality), the selector is a group-algebra operator
and must equal the full projector `e_H`.  The support lower bound is then a
theorem.  The remaining gap is not this algebra; it is proving that a proposed
p-specific finite-field selector satisfies the reduced-normality/lifting and
equivariance hypotheses.

## Best Certificate Target

For an actual p24 certificate path, the third-trace composite cycle remains
the best formal target:

```text
t = -1178414874616
D_K = -652834595820939249713143
composite ideal = 2 * 463 * 223^(-1)
quotient_degree = 66254
recovery_degree = 3107441
correspondence_degree_proxy = 311808
seeded_walk_proxy = 968924963328 = 0.968925 * sqrt(p)
```

Its quotient is less elegant, but the recovery degree is four orders of
magnitude smaller than the first-trace order-19 recovery degree.

The orientation caveat is essential.  Plain `X0(2*223*463)` forgets which
prime above each split rational prime was chosen.  In the p24 target, all
eight sign choices generate an index-2 subgroup with recovery degree
`102940198007`; the good index-66254 subgroup appears only after choosing the
oriented product `2 * 463 * 223^(-1)`.

## Smooth Third-Trace Target

```text
p = 1000000000000000000000007
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
Cl(O_K) cyclic
```

The best embedded quotient candidates remain split-prime cycles:

```text
ell=677:
  cycle_count = 314 = 2 * 157
  cycle_length = 655670051 = 211 * 3107441

ell=7349:
  cycle_count = 422 = 2 * 211
  cycle_length = 487868237 = 157 * 3107441

composite ideal 2 * 463 * 223^(-1):
  norm = 206498
  X0 index proxy = 311808
  cycle_count = 66254 = 2 * 157 * 211
  cycle_length = 3107441
```

Formally these degrees are far below `sqrt(p)`.  The missing theorem is not
the Fourier layer or the existence of the class-field quotient; it is the
embedded computation and pairing back to `j`.

A generic noncyclic-safe composite search over all three traces is now in:

```text
p24/all_trace_composite_order_search.py
```

## Explicit Embedded Theorem Attempt

The latest theorem boundary is now written in:

```text
p24/embedded_selector_theorem_attempt.md
```

The positive conditional theorem is clean:

```text
if the non-genus quotient-character traces
T_s = sum_i zeta_m^(s*i) j_i
can be computed in o(sqrt(p)) without H_D or class enumeration, then Fourier
inversion gives the embedded H-period quotient and the recovery polynomial.
```

For the first-trace order-19 target, the Kummer layer lives over `F_{p^2}`.
For the third-trace composite target, the root-of-unity extension degree is
`5460`.  Neither is the bottleneck.

The negative theorem still needs a lifting/faithfulness lemma.  Once a
candidate formula restricts to a bounded-support group-algebra operator on the
CM torsor, the subgroup projector

```text
e_H = sum_{k=0}^{n-1} g^(m*k)
```

forces support at least `n`.  That means `14670196166` support terms for the
order-19 toy and `3107441` support terms for the third-trace composite.  This
rules out local Hecke-word projectors under the normal-element hypothesis, but
does not by itself exclude a one-prime finite-field identity that fails to
lift to characteristic zero.

The explicit class-field sidecar reached the same boundary from the positive
direction: `bnrclassfield`, principalization, Kummer, and Siegel/Ramachandra
machinery can name abstract quotient fields or ray class fields, but known
algorithms pair them with `j` by enumerating conjugates or taking the same
subgroup trace/norm.  The tiny `D=-87`, `q=103` example remains the warning:
abstract quotient roots `[10,93]` and embedded cycle-sum roots `[4,29]` both
split over the field, but are unpaired without an explicit relation to `j`.

## Middle Trace Genus Case

Franklin's middle-trace probe is captured in:

```text
p24/middle_genus_split_alignment_audit.py
```

The quotient there is easy because it is genus data:

```text
D_K = -998443569409526507503607
h = 833035208344 = 8 * 104129401043
Cl = C_104129401043 x (C2)^3
Redei 4-rank = 0

ell=11:
  genus signature = (1,1,1,1)
  order = 104129401043
  index = 8
```

So it is a useful control case, not a certificate route.  After applying the
full genus quotient the residual recovery is still `104129401043`, which is
`0.104 * sqrt(p)`, and the seeded `ell=11` proxy is above `sqrt(p)`.

## Verifier-Native Parabolic Closure

Cicero's remaining verifier-equation gap is now reproducible in:

```text
p24/parabolic_inverse_chain_ansatz.py
```

The parabolic limit

```text
x_i = u * (1 + alpha*i)/(1 + beta*i)
```

of the split-terminal Mobius ansatz collapses after the first edge: later
compatibilities have only the factor `alpha-beta`, the constant orbit.  The
same is true in the edge square-root coordinate.  Thus the verifier-native
identity route still has no surviving low-dimensional section.

I also closed the near-singular torus-window variant in:

```text
p24/near_singular_window_audit.py
p24/near_singular_window_audit.md
```

The exact singular limits `A=+/-2` have only `v2(p-1)=1` or `v2(p+1)=3` for
p24 and are rejected by the verifier.  The remaining hope was that strict
parameters might concentrate in a sub-sqrt perturbation window around these
torus points.  Across ten exact `p=n^2+7` calibration rows, windows of sizes
`p^beta` for `beta < 1/2` had tiny capture and no stable lift; at
`W ~= sqrt(p)`, capture matched coverage and lift was about `1`.  So scanning
near `+/-2` is not a hidden asymptotic selector.

With split primes up to `200`, products of up to three factors, and norm
`<=100000`, the best formal max-degree rows still come from the third trace:

```text
third trace:
  (2, -107, -197): norm=42158, index=422, order=487868237
  (29, -191):      norm=5539,  index=314, order=655670051

first trace:
  best index-38 remains ell=107, order=7335098083

middle trace:
  best small quotients are genus-size index 4 or 8,
  with recovery 208258802086 or 104129401043
```

These do not beat the existing certificate-oriented composite target, but they
confirm that the middle trace's noncyclic structure is not hiding a balanced
small-norm quotient in this range.

## Exact Period Identity

Let `G=<g>` have order `h`, `H=<g^m>` have size `n`, and write

```text
j_i = j(g^i a_0).
```

The split-cycle periods

```text
y_r = sum_{k=0}^{n-1} j_{r+mk}
```

are recovered from high-order class-character traces

```text
T_s = sum_{i=0}^{h-1} zeta_m^{s*i} j_i
```

by inverse DFT:

```text
y_r = (1/m) * sum_s zeta_m^{-sr} T_s.
```

For p24, the root-of-unity extension degrees are:

```text
ell=677  quotient m=314: extension degree 156
ell=7349 quotient m=422: extension degree 35
composite quotient m=66254: extension degree 5460
```

For the first trace the analogous quotient size is only `19`, with
root-of-unity extension degree `2`.  For all targets, the obstacle is computing
the required non-genus traces `T_s` without summing over the class group.

## Composite Split-Ideal Refinement

`p24/composite_split_cycle_audit.py` computes class logs relative to the
norm-23 generator and searches small signed products of split prime ideals.
This improves the formal embedded cycle candidates:

```text
index 314:
  best norm <= 10000 remains ell=677
  order = 655670051

index 422:
  old single prime ell=7349
  improved composite ideal 2 * 919
  norm = 1838
  X0 index proxy = 2760
  order = 487868237

index 66254:
  no single prime below 250000 has this index
  best found product with primes <=5000:
    2 * 463 * 223^(-1)
    norm = 206498
    X0 index proxy = 311808
    order = 3107441
    seeded walk proxy = 968924963328 = 0.968925 * sqrt(p)
```

The index-66254 product is the sharpest formal tower target so far: quotient
degree `66254`, recovery degree `3107441`, and a composite modular
correspondence still below `sqrt(p)` even by the crude seeded-walk proxy.  It
does not solve the seedless construction problem, but it lowers the degree of
the embedded object that a successful theorem would need to construct.

## Tested Escape Hatches

### Direct Moments

`p24/period_moment_idempotent_toy.py` shows that quotient power sums are just
convolutions of the same high-order traces:

```text
P_d = sum_r y_r^d
    = m^(1-d) * sum_{s_1+...+s_d=0 mod m} T_{s_1}...T_{s_d}.
```

Thus "construct the period polynomial by moments" is not a new primitive.  It
still requires the subgroup idempotent.  Genus-only moments reconstruct a
coarser repeated-average polynomial, not the true quotient polynomial.

### Product / Norm Periods

`p24/relative_norm_phase_toy.py` shows the analogous fact for products.  Coset
products

```text
z_r = prod_{k=0}^{n-1} j_{r+mk}
```

are valid quotient coordinates, but a global Gross-Zagier/Borcherds-style norm
only gives `prod_r z_r`, which erases the quotient phase.  A useful product
formula would need to be relative to the exact high-order subgroup; known
global/genus norm formulas do not select a cycle.

### Abstract Class Fields

`p24/abstract_vs_embedded_quotient_toy.py` illustrates the core issue.  For
`D=-87`, PARI gives the abstract degree-2 unramified quotient

```text
bnrclassfield(bnr,2,1) = x^2 + 3.
```

Over `F_103`, its roots are `[10, 93]`.  The embedded split-cycle quotient
from `Phi_7` has roots `[4, 29]`.  Both split, but they are unpaired until a
relation to `j` is supplied.  In degree 2 there are only two possible affine
pairings; in p24 the analogous ambiguity has `314` or `422` quotient roots and
large recovery factors.

### Standard Twisted-Trace Formulas

`p24/non_genus_twisted_trace_level_audit.py` records the automorphic level
obstruction.  A high-order unramified class character of `K` induces a
dihedral theta series of natural level `|D_K|`, not level `314` or `422`:

```text
weight-1 level |D_K| Sturm/index proxy ~= 5.45e22
proxy / sqrt(p) ~= 5.45e10
```

Genus characters are the exception, but they only see the order-2 quotient.
For the p24 quotients they leave buckets of size `157` or `211`.

### Raw DANGER Statistics

The upstream DANGER3 data refutes the obvious `A,x0` statistics as growing
selectors.  Trace residues, terminal branch signs, low-degree characters,
inverse-chain words, additive/multiplicative spectra, and moments give
constant-factor filters or generator artifacts.  The only data-liftable
positive invariant is the split-cycle/class-character period itself.

The softer "window around a simple formula" version is also now tested:

```text
p24/low_height_formula_window_audit.py
p24/low_height_formula_window_audit.md
```

Across exact near-square calibration rows, low-height LFT centers with
sub-sqrt or sqrt-scale windows gave only constant lifts around `1.4`, with
about one percent capture at best.  So moving intervals around simple
near-square formulas are not a hidden preselector.

### Small CM Period Complexity

`p24/cycle_period_complexity_scan.py` tests the split-cycle periods directly
on small complete CM root sets.  It finds splitting primes, a small split
prime generating a full CM cycle, and quotient period sequences

```text
y_r = sum_{k=0}^{n-1} j_{r+m*k}.
```

The first bounded scan reports full Berlekamp-Massey complexity in every row:

```text
D=-5000: m=6,10,15 all bm=m
D=-215:  m=7 bm=m
D=-279:  m=6 bm=m and dft_support=6
D=-287:  m=7 bm=m
D=-327:  m=6 bm=m and dft_support=6
D=-335:  m=6,9 all bm=m
```

This is not a proof, but it is the right negative toy signal: quotient periods
look like full high-order character data, not low-recurrence or sparse-spectrum
sequences waiting to be lifted.

### Oriented Relation Torsor

`p24/oriented_relation_torsor_toy.py` models inverse-SEA/oriented-Elkies data
on the same `D=-5000` CM torsor.  With the norm-3 ideal as generator, small
split primes act by translations on the 30 labeled roots.  The relation word

```text
3 * 11 * 43
```

has total class log `0 mod 30`, but the toy verifies:

```text
fixed_indices_count=30
fixes_every_cm_root=1
```

Similarly, the `11^3` cycle relation closes at every root and produces ten
3-cycles.  This is the inverse-SEA obstruction in miniature: oriented
split-prime constraints are equivariant on the CM torsor.  They describe the
Cayley graph or quotient cycles, but they do not choose an origin/root.

### Norm Equals Index Local Phi

`p24/norm_equals_index_local_phi_toy.py` tests the first-trace coincidence
`ell=index` at toy scale.  Odd examples such as
`D=-743,h=21,ell=3,index=3` and `D=-2239,h=35,ell=5,index=5` show the same
shape, but the horizontal cycle period is not a linear function of simple
local `Phi_ell(j,Y)` symmetric data:

```text
linear_local_formula_exists=0
```

in all five audited odd examples.  Thus the `ell=index` coincidence is not, by
itself, a local modular-polynomial selector.

### Composite Orientation

`p24/composite_orientation_ambiguity_audit.py` checks the p24 composite target:

```text
desired oriented product = 2 * 463 * 223^(-1)
desired index = 66254
desired order = 3107441

plain X0(206498) sign choices:
  subgroup_index_generated_by_all_sign_choices = 2
  subgroup_order_generated_by_all_sign_choices = 102940198007
```

The small analogue `p24/composite_orientation_toy.py` uses `D=-5000`:

```text
desired product 3 * 17^(-1):
  oriented_component_count = 6
  oriented_component_sizes = [5]

plain X0(3*17):
  unoriented_component_count = 2
  unoriented_component_sizes = [15]
```

So the composite norm saving is real only for the oriented class.  A theorem
must construct oriented period data, not just an unoriented composite
modular-polynomial relation.

`p24/composite_orientation_degree_tradeoff.py` checks what the orientation
could cost:

```text
plain X0(206498):
  correspondence_degree = 311808
  recovery = 102940198007
  seeded_proxy/sqrt = 3.21e4

binary split-prime sign labels:
  correspondence_degree = 2494464
  recovery = 3107441
  seeded_proxy/sqrt = 7.75

full X1/Gamma1-style marking:
  seeded_proxy/sqrt = 2.48e4 to 9.94e4
```

Thus the composite target cannot be turned into a literal sub-sqrt walk merely
by adding orientation labels.  It remains viable only as a non-walk embedded
period/quotient theorem whose cost is governed by the formal quotient and
recovery degrees, not by multiplying correspondence degree by cycle length.

`p24/oriented_composite_path_toy.py` checks whether binary-oriented local path
data might itself be the missing selector.  In the `D=-5000` analogue,
`3 * 17^(-1)` has index `6` and order `5`, but local oriented path values still
have full orbit:

```text
distinct_path_sums = 30
distinct_path_products = 30
distinct_path_edge_pair_sums = 30
```

Only whole-cycle aggregation gives the quotient:

```text
distinct_period_sums = 6
period_sum_polynomial_degree = 6
```

So binary orientation is not enough by itself; it produces ordered local data,
not a seedless quotient selector.

## Admissible Seedless Selector Theorem

I added:

```text
p24/admissible_seedless_selector_theorem.md
```

This is the consolidated no-go theorem for the natural selector attempts.  In
the admissible model, a seedless construction may use prime-to-`p`
correspondences, rational functions on irreducible covers, bounded oriented
Hecke words, abstract quotient towers, and genus data, but it cannot insert an
external CM root or a prime-above-`p` label.

Under those hypotheses:

```text
scalar H-coset coordinate:      degree >= |H|
additive H-period projector:    support >= |H|
abstract quotient tower:        roots unpaired with embedded j-periods
nontrivial tower child choice:  no G-equivariant section
genus-only data:                factors through G/G^2
```

For the third p24 target this lower bound is `|H|=3107441`; for the order-19
theorem toy it is `14670196166`.  Thus the theorem closes bounded local
identities, genus labels, sparse projector formulas, and bare abstract
class-field towers, while deliberately leaving open the one live route:
compute the embedded non-genus `157`/`211` relative class-character traces and
recover through the degree-`3107441` polynomial.

## Prime-Torsor Obstruction For Abstract Towers

I added:

```text
p24/prime_torsor_obstruction_theorem.md
```

This closes the clean abstract-class-field loophole.  If the ordinary prime
`frak_p | p` of `K` splits completely in the ring class field `L_rc`, then for
every intermediate quotient `M=L_rc^H`,

```text
O_M tensor_{O_K} F_p ~= product_{G/H} F_p.
```

The roots of an abstract quotient polynomial modulo `p` are therefore a
`G/H`-torsor of primes above `p`.  The embedded period quotient is another
`G/H`-torsor.  Pairing the two is extra data: the set of compatible pairings
is itself a `G/H`-torsor.  In a tower, the children above a parent form an
`H_parent/H_child` torsor, and the earlier section proof says no seedless
`G`-equivariant child selector exists unless the layer is trivial.

So `bnrclassfield`-style equations can expose quotient degrees and prove
splitting, but they do not by themselves give:

```text
abstract quotient root -> embedded H-period -> recovery polynomial in j.
```

Arbitrary finite-field root choice is useful only after those embedded
relations are already known.  Without them, it merely chooses an abstract
prime above `p`, not a CM `j` recovery factor.

This does not rule out the live positive route.  It states exactly what that
route must add: embedded non-genus relative class-character traces for the odd
`157` and `211` layers, paired back to the `j`-torsor.

## Moment And Correlation Reframing

I added:

```text
p24/hecke_correlation_trace_boundary.md
p24/period_correlation_idempotent_toy.py
```

This checks the remaining natural variant of the moment route.  In the
`D=-5000`, quotient-size-10 calibration, full-cycle autocorrelations

```text
C(d) = sum_i j_i j_{i+d}
```

recover the second quotient moment only after the same subgroup projection:

```text
sum_r y_r^2 = sum_{d in H} C(d).
```

The period autocorrelation diagonalizes to

```text
DFT(A)(s) = T_s * T_{-s},
```

and the toy has full nonzero spectrum:

```text
period_autocorrelation_bm_complexity=10
nonzero_spectral_components=10
```

So Hecke-trace/correlation bookkeeping is not a new selector by itself.  It
rephrases the same class-character traces unless there is an independent
sub-sqrt way to project global correlations onto the high-order subgroup `H`.

## Correspondence Recurrence And Resultant Boundary

I added:

```text
p24/correspondence_recurrence_resultant_boundary.md
```

This closes the natural "fast power the correspondence" variant.  A compact
chain or recurrence for repeated `Phi_ell` edges represents a long edge or
many hidden branches; it does not create the subgroup period.  In the toy
`D=-5000` cycle, high-power generator paths retain the full orbit:

```text
move=6:
  oriented_path_count=30
  distinct_path_sums=30
  component_count=6
  distinct_period_sums=6
```

The oriented composite toy has the same behavior:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_period_sums=6
```

For p24, seedless closed-cycle resultants have enormous correspondence
degree; for example the full `ell=23` generator cycle has
`log10 psi(23^order) ~= 2.8e11`, while the desired decomposed degrees
`66254` and `3107441` appear only after embedded quotient periods are known.

Thus recurrence/resultant compression is not a certificate-scale speedup
unless it also supplies the same high-order subgroup projector or
non-genus relative class-character traces.

## Reduced Resolvent Normality Scan

I added:

```text
p24/reduced_resolvent_vanishing_scan.py
p24/reduced_resolvent_normality_boundary.md
p24/reduced_normality_false_lemmas_toy.py
p24/reduced_normality_proof_frontier.md
p24/reduced_resolvent_propagation_lemma.md
p24/frobenius_packet_testing_barrier.py
p24/frobenius_packet_testing_barrier.md
p24/cyclic_code_projector_weight_toy.py
p24/cyclic_code_projector_weight_scan.py
```

This probes the p-specific finite-field loophole in the additive projector
barrier.  For a complete cyclic CM torsor, it forms

```text
J(T) = sum_i j_i T^i
```

and computes `gcd(J(T), T^h-1)`.  A nontrivial gcd is exactly a packet of
class-character resolvents that vanished after reduction.

Two small scans found no vanishing:

```text
12-row scan:
  normal_rows=12
  nonnormal_rows=0
  quotient_dft_full_support_rows=15/15

40-row scan:
  normal_rows=40
  nonnormal_rows=0
  quotient_dft_full_support_rows=46/46
```

So the toy evidence points away from a helpful p-specific character collapse.
It also supports the conditional support lemma: in normal rows,
`L*j=e_H*j` forces `L=e_H`.

This still does not prove p24 reduced normality.  The remaining target theorem
would need to show that the p24 prime does not divide the norm of any relevant
high-order non-genus resolvent.  Naive height lifting fails, and known
Gross-Zagier/intersection/norm formulas do not currently give that
all-character nonvanishing without reintroducing the same odd class-character
period primitive.

The false-lemma toy makes the logical gap explicit: over `F_11`, it constructs
a split squarefree degree-5 vector with distinct entries but vanished DFT
components.  Thus split/separable CM roots, primitive generation of the split
etale algebra, and local normal-basis existence are all weaker than reduced
normality of this specific `j`-vector.  The proof frontier is now the normal
determinant unit statement

```text
P_p does not divide product_chi sum_i chi(g)^i j_i.
```

The propagation lemma adds one useful rigidity statement.  If a resolvent
vanishes at one split prime above `p`, it vanishes at every `G`-translate of
that prime; and since `J(T)` has coefficients in `F_p`, vanished characters
come in Frobenius orbits.  For the third strict trace,

```text
ord_157(p)   = 156
ord_211(p)   = 35
ord_33127(p) = 5460
ord_66254(p) = 5460
```

So a primitive odd quotient-character collapse would erase `5460` spectral
components.  This is strong evidence against an accidental sparse-projector
kernel, but still not a contradiction because norm/height bounds are too
large.

The Frobenius-packet/cyclic-code audit turns this into a finite-field coding
statement.  For the p24 third quotient,

```text
T^66254 - 1 over F_p:
  degree 1:     2 factors
  degree 35:   12 factors
  degree 156:   2 factors
  degree 5460: 12 factors
```

So there are only `28` packet residues to check once the embedded quotient
period vector is known.  But each packet residue is still a full-support
linear functional of the period vector, and black-box sampling cannot certify
it: in the `D=-5000` toy, changing only two of ten period coordinates kills a
degree-2 packet while preserving the other eight.  In the exact cyclic-code
model, an artificial one-packet annihilator did not reduce the Hamming weight
of the subgroup projector in any tested quotient.  A broader four-cycle scan
with artificial degree-2 packet kernels found `reduced_weight_rows=0/8`.
Thus packet compression is a useful statement of the reduced-normality gap,
not a new sub-sqrt selector.

## Unit Distribution Obstruction

I added:

```text
p24/ray_kernel_distribution_audit.py
p24/unit_distribution_obstruction.md
```

This closes the one plausible modular-unit exception from the sidecar audit.
Siegel/Ramachandra distribution relations can collapse kernels of maps between
ray class groups, but those kernels are principal congruence/local-unit
directions.  Their image in the ordinary Hilbert class group is trivial.

For p24, the odd layers `157` and `211` are conductor-one unramified class
group layers inside the principal genus, not ray kernels.  The local audit
prints:

```text
ell=157: Kronecker(D,ell)=-1, |(O_K/ell)^*|=24648, no 157-factor
ell=211: Kronecker(D,ell)=-1, |(O_K/ell)^*|=44520, no 211-factor
```

The first `ell`-primary ray factors occur in the ramified filtration
`ell^2 -> ell`, and that filtration maps trivially to `Cl(K)`.  Thus modular
unit distribution can lower ramified ray directions, but it does not compute
the unramified `157`/`211` relative phase.

## Smooth Torsor Search Boundary

I added:

```text
p24/smooth_torsor_search_tradeoff_audit.py
p24/smooth_torsor_search_boundary.md
```

This separates smooth-class navigation from first-root discovery.  For the
third trace, smoothness gives excellent formal decomposed degrees:

```text
best embedded split = 66254 * 3107441
quotient + recovery = 3173695
```

But random discovery of a strict trace is still square-root density.  The audit
prints:

```text
sum_h_one_order_per_trace = 1.317649 * sqrt(p)
random_j_expected_trials_over_sqrt_using_sum_h = 0.758927
two_order_proxy_expected_trials_over_sqrt = 0.379464
generous_montgomery_A_degree_bound_expected_trials_over_sqrt = 0.063244
```

These are constants, not an exponent improvement.  The exact small-field
post-trace audit agrees: once a target `A` is known, finding `x0` is constant
expected work, but constructing the target-trace `A` remains `Theta(sqrt(p))`
density:

```text
target_A_over_sum_sqrt = 8.500883
strict_A_over_sum_sqrt = 6.005442
```

Thus BSGS/Pohlig-Hellman/smooth torsor navigation helps after a seed CM root,
two known vertices, or an embedded quotient root exists.  It does not create
the first root or the embedded quotient equations.

## Current Proof Obligation

A successful theorem must provide one of these equivalent objects:

```text
1. a non-enumerative formula for the order-157/order-211 traces T_chi;
2. a relative norm/trace formula for H_D over the subgroup <ell> that keeps
   all quotient coefficients, not only the global norm;
3. an explicit class-field generator alpha with Artin kernel <ell> plus a
   computable relation R(alpha,j)=0 and a root-pairing rule over F_p;
4. a finite-field identity using Phi_677 or Phi_7349 that constructs one
   horizontal target CM cycle without H_D or a seed vertex.
```

Everything else tested so far either enumerates the class set, uses `H_D`,
starts from a target CM root, or collapses the high-order phase to genus/global
data.

## Status

No certificate or asymptotic strict-DANGER speedup has been found yet.  The
live theorem target is now very narrow: non-genus class-character period
computation embedded relative to `j`, without class enumeration.  For theorem
experiments use the order-19 first-trace quotient; for a p24 certificate route
prioritize the third-trace composite quotient/recovery split.

## Near-Square Closure

Dalton rechecked the special form

```text
p = n^2 + 7,    n = 10^12.
```

There is no additional exact trace relation beyond the already recorded
`2^40` residue condition.  The strict curve-side traces are precisely the
three Hasse representatives of

```text
t == p + 1 mod 2^40:
  1020608380936
  -78903246840
  -1178414874616
```

The genuine near-square CM identity gives `D=-7` traces `±2n`, but those have
only `v2(#E)`/`v2(#twist)=3`.  For the strict traces, the discriminants are
all conductor-2 with fundamental discriminants comparable to `p`, and
`gcd(Delta,n)=4`; `n` is not hiding a large square conductor.  The bounded
audit

```text
python3 p24/near_square_target_discriminant_audit.py --max-rows 12 --include-p24
```

prints the p24 rows:

```text
t=-1178414874616  D=-652834595820939249713143  conductor=2
t=-78903246840    D=-998443569409526507503607  conductor=2
t=1020608380936   D=-739589633190799177940983  conductor=2
```

So the near-square identity supplies the broad `D=-7` certificate already
recorded, not a strict DANGER selector.

## Exact Trace-CRT Barrier

I also separated the residue-oracle route into:

```text
p24/exact_trace_crt_modular_degree_barrier.py
```

Exact trace residues modulo a product `N` are information-rich: once `N`
exceeds the Hasse width, they isolate a trace.  But constructing curves with
that residue data is modular level structure.  For p24 the strict condition
already imposes

```text
N = 2^40 = 1099511627776 = 1.0995 * sqrt(p),
```

and `[SL2:Gamma0(2^40)] = 3*2^39`, a constant times `sqrt(p)`.  Odd CRT
residues can distinguish the three representatives and improve constants, but
they do not change the exponent in this construction model.

## Montgomery Trace Transform Barrier

I added:

```text
p24/montgomery_trace_transform_audit.py
p24/montgomery_trace_transform_barrier.md
```

The Montgomery trace function has the exact convolution form

```text
t(A) = - sum_c chi(c^2 - 4) chi(A + c).
```

This makes exact small-field trace computation cheap, but the transform does
not appear sparse or low-frequency.  In six `p=n^2+7`, `n==0 mod 8` rows,
the additive spectrum of the full trace sequence had full support, with
median top-256 energy only `0.039016`.  The strict bucket itself had
random-sized Fourier peaks and no stable low-order additive/multiplicative
selector.

So the trace-function/hypergeometric route is another trace oracle
reformulation, not a current sub-sqrt selector.

## Reduced Normality Refinement

The missing reduced-normality theorem has been sharpened and partially
falsified in its too-broad form.

New files:

```text
p24/quotient_spectrum_support_theorem.md
p24/quotient_spectrum_support_toy.py
p24/reduced_normality_failure_audit.py
```

The universal hope

```text
every split ordinary CM j-cycle is reduced-normal
```

is false.  The focused failure audit found actual small CM failures:

```text
D=-216 q=103 ell=5 h=6 gcd_degree=1 zero_order=3 quotient_failure=3/2/2
D=-300 q=139 ell=7 h=6 gcd_degree=1 zero_order=2 quotient_failure=2/3/1
```

These are low-order degree-1 packet failures.  They prove that splitness,
squarefreeness, ordinary reduction, and class-field generation are not enough
to imply reduced normality of the specific singular modulus.

For the additive selector theorem, the exact finite-field statement is:

```text
exact selectors = e_H + Ann(J),
support lower bound = min_{B in Ann(J)} wt(e_H + B).
```

Full reduced normality gives `Ann(J)=0` and hence support `|H|`.  Quotient
packet nonvanishing is enough only for formulas already known to factor
through `G/H`; arbitrary sparse Hecke-word operators still require full
reduced normality or this direct cyclic-code minimum-distance theorem.

The quotient-support toy inserted artificial degree-1/2 packet kernels in
small cyclic Fourier rings:

```text
rows=283
nonquotient_reduced_rows=0
quotient_reduced_rows=0
```

This supports the cyclic-code barrier but is not a p24 proof.  The p24 theorem
target is now precise: prove the selected p24 singular-modulus normal
determinant is a `p`-adic unit under hypotheses excluding the low-order toy
failures, or directly prove `min wt(e_H+Ann(J))=3107441` for the third trace.

## Partial-Orbit Shortcut Closed

I added:

```text
p24/partial_orbit_invariance_theorem.md
p24/partial_orbit_window_toy.py
```

This checks a constructive temptation in the oriented-composite route: maybe a
short symmetric window along the recovery cycle already gives an invariant of
the `G/H` quotient.  It cannot.  If `H=<a>` acts freely and a subset-polynomial
from `S <= H` is invariant under shifting the origin by `a`, then `aS=S`, so
`S=H`.

The calibrated `D=-5000` toy has oriented composite move `3*17^(-1)`, index
`6`, and orbit size `5`.  Running:

```text
python3 -m py_compile p24/partial_orbit_window_toy.py
python3 p24/partial_orbit_window_toy.py
```

gave:

```text
window_length=1 distinct_window_polys=30
window_length=2 distinct_window_polys=30
window_length=3 distinct_window_polys=30
window_length=4 distinct_window_polys=30
window_length=5 distinct_window_polys=6
```

So the quotient collapse appears only at the full `H`-orbit.  For the third
p24 trace, a partial arc along `2*463*223^(-1)` cannot replace the full
degree-`3107441` recovery object.

## Split-Algebra And Energy Update

The current missing theorem is consolidated in:

```text
p24/missing_theorem_current_form.md
p24/relative_resolvent_split_algebra_theorem.md
p24/relative_energy_certificate.md
p24/lean/RelativeResolvent.lean
```

For the third target, the exact finite-field content condition is:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1
```

for each of the eight nontrivial relative-character Frobenius orbits.  The
split-algebra theorem says harmful vanishing is equivalent to the relative
resolvent `Theta_a` being zero in the entire split class algebra modulo the
selected cyclotomic prime; the finite logic of that implication is checked in
Lean core.

A weaker scalar sufficient certificate is:

```text
E_a = sum_u P_u(a)P_u(-a) != 0.
```

Equivalently, `E_a` is a relative autocorrelation transform and satisfies the
safe Parseval identity

```text
sum_r R_{a+r n}R_{-a-r n}=mE_a.
```

This gives a more trace-formula-shaped target, but computing or proving the
nonvanishing of these high-order autocorrelation transforms is still the same
embedded non-genus arithmetic problem.

The energy target has one real finite-field improvement:

```text
p24/energy_real_cyclotomic_packet_audit.py
```

Because `p^(388430/2) == -1 mod 3107441` and `E_a=E_-a`, each energy packet
has degree `194215` rather than `388430`.  There are still eight packets.

The Hecke/Brandt audit is:

```text
p24/hecke_autocorrelation_boundary.md
p24/agent_brandt_energy_sidecar.md
```

It gives the exact identity `C_d = Tr(J P_{md} J P_{-md})`, but this assumes
the oriented class-action permutation/projector.  Ordinary Hecke moments and
modular resultants repackage the same autocorrelation sequence and show full
support at toy scale; they do not yet compute the p24 energy packets below
the recovery-subgroup support.
