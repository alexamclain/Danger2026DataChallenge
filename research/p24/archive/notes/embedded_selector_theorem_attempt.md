# Embedded selector theorem attempt

This is the sharpened form of the missing theorem after the order-19,
third-trace composite, verifier-equation, and explicit class-field sidecars.

## Setup

Let `O` be one of the p24 CM orders, and let

```text
G = Cl(O) = <g>,      |G| = h = m*n,
H = <g^m>,            |H| = n.
```

The embedded CM roots over `F_p` are a torsor

```text
j_i = j(g^i * a_0),     0 <= i < h.
```

For the current live targets:

```text
first trace order-19 toy:
  D_K = -739589633190799177940983
  h = 278733727154 = 19 * 14670196166
  m = 19
  n = 14670196166

third trace certificate target:
  D_K = -652834595820939249713143
  h = 205880396014 = 66254 * 3107441
  m = 66254
  n = 3107441
  oriented class = 2 * 463 * 223^(-1)
```

The desired quotient coordinate is any separating `H`-invariant, for example

```text
y_r = sum_{k=0}^{n-1} j_{r + m*k},        0 <= r < m.
```

Then `V(Y)=prod_r (Y-y_r)` has degree `m`, and after selecting one root `y_r`,
the recovery polynomial

```text
R_r(X) = prod_{k=0}^{n-1} (X - j_{r+m*k})
```

has degree `n`.  These degrees beat `sqrt(p)` for the third-trace target, and
the seeded proxy is just under `sqrt(p)`.

## Positive conditional theorem

If one can compute the embedded quotient-character twisted traces

```text
T_s = sum_{i=0}^{h-1} zeta_m^(s*i) j_i,      0 <= s < m,
```

in time `o(sqrt(p))`, without first constructing `H_D` or enumerating the CM
class set, then the selector follows:

```text
y_r = (1/m) * sum_s zeta_m^(-s*r) T_s.
```

The root-of-unity layer is cheap in the live cases:

```text
first trace m=19:       zeta_m in F_{p^2}
third trace m=66254:    extension degree 5460
```

So the Fourier/Kummer layer is not the missing primitive.  The missing
primitive is the non-genus high-order twisted trace itself.

## Support lemma for local Hecke formulas

The clean structural version is now separated into:

```text
p24/structural_lifting_support_lemma.md
```

Work in the group algebra on the cyclic torsor.  The component projector is

```text
e_H = sum_{k=0}^{n-1} g^{m*k}.
```

Any formula that is a bounded linear combination of local oriented Hecke words
restricts to an element

```text
L = sum_{s in S} c_s g^s
```

with support `|S|` equal to the number of class translates it actually uses.
If the `j_i` form a normal element for the relevant quotient characters, then
`L(j)` equals an `H`-period for all choices of origin only when `L=e_H` up to
translation.  In that case `|S| >= n`.

This is the precise conditional no-go for local correspondences:

```text
first trace order-19:   support >= 14670196166
third trace composite:  support >= 3107441
```

The existing toy scans support the normal-element hypothesis: small CM period
sequences have full character support/Berlekamp-Massey complexity, and local
window searches find no low-degree coset invariants except degenerate cases.
The exact finite-field normal-basis calibration is:

```text
p24/normal_basis_support_toy.py
```

For a cyclic embedded CM cycle it forms `J(T)=sum_i j_i*T^i` and checks
`gcd(J(T), T^h-1)`.  In rows where the gcd is `1`, equality
`L*j=e_H*j` forces `L=e_H` in the group algebra, so the support lower bound is
literal in the toy.

For the p24 targets, characteristic-zero normality is proved by a
dominant-conjugate estimate in:

```text
p24/singular_moduli_normality_bound.py
```

For a reduced form `[a,b,c]` of conductor-2 discriminant `Delta < 0`,

```text
||j(tau)| - exp(pi*sqrt(|Delta|)/a)| <= 2079.
```

The principal form is the unique reduced form with `a=1`; every other
conjugate has `a>=2`.  Therefore every class-character resolvent is nonzero
once

```text
exp(pi*S) - 2079 > (h-1) * (exp(pi*S/2) + 2079),
S = sqrt(|Delta|).
```

The p24 margins are on the order of `pi*S/2`, i.e. trillions in natural-log
scale.  Thus the singular modulus is a normal element for each strict p24 CM
torsor before reduction.

What is still not proved unconditionally is reduced normality at the chosen
prime.  In determinant form, one must show that the selected prime above `p`
does not divide

```text
product_chi sum_i chi(g)^i j_i.
```

Equivalently, one must rule out a one-prime finite-field identity that does
not lift to the characteristic-zero CM torsor.  This is the exact theorem gap
for negative results.  The current proof frontier is recorded in:

```text
p24/reduced_normality_proof_frontier.md
p24/reduced_normality_false_lemmas_toy.py
```

## Explicit class-field obstruction

Known explicit class-field machinery does not currently supply the positive
conditional theorem.

Known fixed-trace curve construction also does not bypass this primitive.
Waterhouse gives the existence/classification of isogeny classes, while
Honda-Tate/Tate identifies the fixed trace with a fixed ordinary isogeny
class.  CM construction algorithms such as Agashe-Lauter-Venkatesan,
Enge/Sutherland CRT, and Bröker-Stevenhagen improve how one computes class
polynomials or choose easier discriminants in flexible settings; for this
fixed `p,t` problem they still require a root of the ring/Hilbert class
equation or equivalent embedded class-field data.

Useful source anchors:

```text
Waterhouse 1969:
  https://www.numdam.org/item/?id=ASENS_1969_4_2_4_521_0
Agashe-Lauter-Venkatesan:
  https://arxiv.org/abs/math/0111159
Microsoft Research summary:
  https://www.microsoft.com/en-us/research/publication/constructing-elliptic-curves-with-a-given-number-of-points-over-a-finite-field/
Enge:
  https://arxiv.org/abs/cs/0601104
Sutherland CRT:
  https://arxiv.org/abs/0903.2785
Bröker-Stevenhagen:
  https://arxiv.org/abs/math/0511729
```

Abstract class fields:

```text
bnrclassfield / principalization can define an unramified quotient field.
```

But reducing that field modulo `p` only gives split abstract roots.  It does
not pair a quotient root with an embedded `j`-cycle.  The `D=-87`, `q=103`
toy shows the failure:

```text
abstract quotient roots:       [10, 93]       from x^2 + 3
embedded cycle-sum roots:      [4, 29]        from Phi_7 cycles
```

Both algebras split, but the relation between them is external data.

Ray/Siegel-unit fields:

```text
level-N Siegel/Ramachandra values generate ray class fields;
Shimura reciprocity gives all conjugates.
```

There are even normal-basis theorems in this direction, e.g. Jung-Koo-Shin,
`Normal bases of ray class fields over imaginary quadratic fields`
(`https://arxiv.org/abs/1007.2312`): certain Siegel-function singular values
form normal bases of ray class fields.  That is useful evidence for the
group-algebra framing, but not a selector.  If the value is normal, projecting
to an unramified subfield by a subgroup still means applying the corresponding
trace/idempotent unless an additional fast relative-period formula is supplied.

For p24, these routes either:

```text
1. enumerate conjugates or take a trace/norm over H;
2. add ramified ray/torsion degree that is much larger than the desired
   unramified quotient;
3. construct an abstract generator without the recovery relation to j.
```

A simple modular-degree bound separates constant-level class invariants from
the live route:

```text
p24/modular_function_degree_lower_bound.py
p24/finite_field_selector_degree_theorem.md
p24/finite_field_modular_zero_lemma.md
```

If `f:X_Gamma -> P^1` is a modular function of degree `d`, one value of `f`
has at most `d` preimages on `X_Gamma` and hence can merge at most `d`
distinct `j`-values.  To be constant on an `H`-coset of size `n`, a single
modular-function value must therefore have degree at least `n`.

The finite-field version is stronger and is now the right theorem statement:
on any irreducible modular-correspondence or algebraic-elimination cover, a
rational function that is regular at the selected embedded CM points and
constant on an `H`-coset must have degree at least `|H|`, because that fiber
contains `|H|` distinct CM points.  This argument happens entirely over
`F_p`; it does not use lifting, height bounds, or reduced normality.

The finite implication and p24 degree accounting are Lean-checked in:

```text
p24/lean/SelectorDegreeLowerBoundGate.lean
```

It verifies that a fiber containing an `H`-coset forces
`|H| <= deg(u)`, and that the third-trace selected-chain and full-relative
degree surfaces are still below `sqrt(p)`.  Thus this no-go is a boundary on
bounded selectors, not a no-go for the intended growing-degree recovery
object.

For the third-trace composite target this lower bound is `3107441`, still
below `sqrt(p)`, so it does not disprove a growing-level construction.  It
does rule out the hope that a fixed-level Weber/Siegel/Ramachandra-style
class invariant, bounded-depth local correspondence, or small resultant cover
secretly has the needed stabilizer.

The most tempting growing-degree variant is the principal H-coset recovery
polynomial

```text
R_H(X) = product_{a in H} (X - j(a)).
```

For the third target this has degree `3107441`, and any root of `R_H mod p`
would be a target CM root.  The obstacle is not degree but height; see:

```text
p24/relative_coset_polynomial_height_audit.py
p24/relative_coset_phase_toy.py
```

There are two obstructions.  First, `R_H` is not rational over `Q`; its
coefficients live in the quotient field of degree `66254`, so reducing one
coset polynomial modulo `p` already requires the missing embedded quotient
phase.  Second, the principal conjugate has log-size around `5e12`; even a
`1/28` class-invariant height factor leaves log-size around `1.8e11`.
Ordinary complex or CRT class-polynomial methods therefore cannot reduce this
relative polynomial modulo `p` without either direct mod-`p` root data or
height-scale work far beyond the finite-field sqrt yardstick.

The order-19 toy makes this especially clean:

```text
ring conductor 19 kernel = 18
one split-prime ray kernel = 9
first ray kernel with a 19-factor occurs at prime-square conductor, hence
ramified
```

Thus the degree-19 quotient is conductor-1 Hilbert class data, not a small
level-19 modular-unit layer.

## Current theorem boundary

The surviving positive theorem would be genuinely new in this project:

```text
Compute non-genus class-character traces of singular moduli, embedded relative
to j, for a prescribed high-order unramified class character, without class
enumeration or a degree-h class polynomial.
```

Equivalently:

```text
construct an H-invariant CM class invariant with a computable recovery
relation to j, without realizing it as an explicit trace/norm over H.
```

The surviving negative theorem for additive Hecke/projector formulas still
needs one new ingredient:

```text
faithfulness/lifting: any bounded-height finite-field identity built from
bounded-level modular correspondences that selects these periods modulo p must
lift to the characteristic-zero CM torsor, where the group-algebra support
lemma applies.
```

The finite-field degree theorem above already rules out bounded local
invariant functions.  What remains uncovered is reduced normality for
group-algebra identities: a sparse additive operator could only beat the
projector if some relevant class-character resolvents vanish after reduction
modulo this one split prime.

There is now a bounded-level replacement for the failed height-lifting
argument:

```text
p24/finite_field_modular_zero_lemma.md
```

If a bounded correspondence formula gives an equality on every embedded CM
point, its residual difference is a rational modular function vanishing on the
whole torsor.  When the pole degree of that function is below `h`, the divisor
argument forces a global mod-`p` modular identity; the Tate-cusp pole orders
then rule out the usual linear combinations of distinct low-norm Hecke words.
This closes the p-specific accident loophole for bounded local formulas, but
not for a deliberate growing-degree object.

The easy norm-height proof of the lifting/normality statement fails.  The audit

```text
p24/finite_field_lifting_height_audit.py
p24/class_invariant_lifting_height_audit.py
```

checks the naive argument: if a residual algebraic integer vanished at every
prime above `p`, then `p^h` divides its norm; if every complex conjugate were
smaller than `p`, it would have to be zero.  But the dominant p24 singular
moduli have log-size around `5e12`, while `log(p) ~= 55`.  A congruence modulo
one completely split prime can therefore be accidental from the archimedean
height point of view.  Even a very optimistic constant-factor class invariant
height reduction, such as `1/28`, leaves log-size around `1e11`, still far
above `log(p)`.  Proving the lifting lemma needs a more structural argument,
not just coefficient-size bookkeeping.

Until one of those two statements is proved, the class-field tower remains a
formal sub-sqrt route but not yet a certificate.

## Tower section obstruction

The tower version has one additional exact obstruction.  For one refinement
layer

```text
L <= K <= G,
```

a seedless construction that canonically chooses one child `L`-coset above a
parent `K`-coset would be a `G`-equivariant section

```text
s : G/K -> G/L.
```

No such section exists unless `K=L`.  Indeed, if `s(K)=aL`, then for every
`k in K`

```text
s(K) = s(kK) = k s(K) = kaL,
```

so `k in L` in the abelian p24 class groups.  Hence `K <= L`.

This is not a no-go for unordered tower polynomials.  It says the tower can
only advance by computing the relative child relation over each parent.  The
missing phase data is equivalent to relative class-character traces:

```text
T_s(aK) = sum_{k in K} chi_s(k) j_{a k}.
```

The companion toy

```text
p24/relative_tower_character_toy.py
```

checks this on `D=-5000`, `h=30`.  The two degree-3 child polynomials in the
`2 -> 3` toy tower are recovered by inverse DFT from relative traces on
`K/H`; the nontrivial traces live in `F_{1259^2}` because the base field lacks
`mu_3`.  This mirrors p24, where root-of-unity extensions are cheap but do
not compute the traces.

For the third strict trace, the degree-2 layer is only genus:

```text
D_K = -599 * 1089874116562502921057.
```

So the genuinely new positive theorem would need to compute the embedded
non-genus relative traces for the `157` and `211` layers, then the
degree-`3107441` recovery polynomial.
