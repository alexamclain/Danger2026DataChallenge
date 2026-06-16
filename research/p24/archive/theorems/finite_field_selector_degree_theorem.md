# Finite-field selector degree theorem

This note sharpens the missing embedded class-field theorem after the lifting
height audits failed.  The point is to separate what can be proved purely in
characteristic `p` from the part that still needs a new idea.

## Setup

Let `O` be one of the strict p24 CM orders and let

```text
G = Cl(O),              |G| = h = m*n,
H <= G,                 |H| = n,
J = {j_g : g in G} <= F_p
```

be the ordinary embedded CM torsor.  The desired period quotient is an
`H`-coset invariant, for example

```text
y_r = sum_{h in H} j_{g_r h},      r in G/H.
```

For the live p24 rows:

```text
first trace/order-19 theorem toy:
  m = 19
  n = 14670196166

third trace/composite certificate target:
  m = 66254
  n = 3107441
```

## Theorem A: fiber degree lower bound

Let `C/F_p` be an irreducible curve carrying the selected oriented CM data
needed by a proposed embedded quotient formula.  This includes `X(1)`, an
oriented split-prime cycle cover, a bounded-depth modular correspondence
curve, or an algebraic cover introduced by resultants or root extraction.

Let

```text
u : C -> P^1
```

be a nonconstant rational function, regular at the chosen CM points.  Suppose
there is a set

```text
S = {P_g : g in G} <= C(F_p)
```

with distinct points indexed by the CM torsor, and suppose `u` is constant on
each `H`-coset:

```text
u(P_g) = u(P_{g h})      for all h in H.
```

Then

```text
deg(u) >= |H| = n.
```

If `u` separates the quotient `G/H`, this is the exact first lower bound:
every quotient value has at least `n` distinct CM preimages.

### Proof

Choose a coset `gH` where `u` is finite.  The fiber over `u(P_g)` contains the
`n` distinct points

```text
{P_{g h} : h in H}.
```

The degree of a nonconstant rational function on a curve is the degree of a
generic fiber, equivalently the degree of the pole divisor, and every special
fiber has degree at most `deg(u)` when counted with multiplicity.  Therefore
`deg(u) >= n`.

This proof is entirely in characteristic `p`; it does not use lifting,
archimedean heights, or characteristic-zero normality.

## Consequences

This proves that a bounded-level finite-field class invariant cannot be the
missing selector.  Any single embedded invariant that is actually constant on
the third target's good cosets must already have degree at least

```text
3107441.
```

For the order-19 theorem toy, it must have degree at least

```text
14670196166.
```

This covers more than the older fixed-level modular-function audit:

```text
p24/modular_function_degree_lower_bound.py
```

because `C` may be a finite modular-correspondence cover or an algebraic
elimination cover, not just `X(1)`.

It also explains why the split-prime edge invariant fails in the toys.  A
single `X0(ell)` edge value has degree about `ell+1`, so it cannot be constant
on a long horizontal cycle unless `ell+1 >= n`.  Whole-cycle symmetric values
can be correct precisely because their natural degree has already grown to
the cycle length.

## Theorem B: additive equivariant selectors

Assume in addition that a proposed selector is additive and equivariant on the
whole CM torsor, so after orienting all prime-to-`p` correspondences it acts as
a group-algebra operator:

```text
L = sum_s c_s [s] in F_p[G].
```

If the reduced CM element is normal,

```text
F_p[G] -> span_Fp(G*j),       A -> A*j
```

is injective, then an identity

```text
L(j_g) = sum_{h in H} j_{g h}      for all g in G
```

forces

```text
L = e_H = sum_{h in H} [h].
```

Therefore the additive support is at least `n`.

This is the finite-field version of the structural support lemma:

```text
p24/structural_lifting_support_lemma.md
```

The only extra hypothesis is reduced normality.  Characteristic-zero normality
for the p24 singular moduli is proved in

```text
p24/singular_moduli_normality_bound.py
```

but reduction modulo this single split prime is not yet proved normal.  The
ordinary norm-height lifting proof fails:

```text
p24/finite_field_lifting_height_audit.py
p24/class_invariant_lifting_height_audit.py
```

## What this proves and what it does not

Theorem A is unconditional and removes the bounded-local-invariant loophole.
It says a surviving finite-field selector must pay at least the recovery/coset
degree `n` somewhere in the geometry.

The finite implication and the p24 degree inequalities are checked in:

```text
p24/lean/SelectorDegreeLowerBoundGate.lean
```

Lean does not prove the curve/divisor input.  It verifies the gate used here:
if the selected fiber contains an `H`-coset of size `n` and every fiber has
size at most `deg(u)`, then `n <= deg(u)`.  It also records that the surviving
third-trace degree surfaces remain below `sqrt(p)`:

```text
3107441 < 10^12
2 + 157 + 211 + 3107441 < 10^12
2 + 157 + 211 + 3107441 + 179 + 89 < 10^12
2 + 2*157 + 314*211 + 3107441 < 10^12.
```

The same Lean gate records the guardrail that the reduced-anchor objects are
too small to be the recovery selector:

```text
89 < 3107441
179 < 3107441
5549 < 3107441
```

Thus the `R_179` / kernel-polynomial piece is a post-producer p-unit
certificate, not a bounded-degree replacement for the embedded recovery phase.
The auxiliary anchor can verify an already selected object, but cannot itself
be an invariant constant on the `3107441`-point recovery coset.

Theorem B removes sparse additive Hecke projectors once reduced normality is
known.  This is the missing nonvanishing theorem:

```text
for every relevant class character chi,
T_chi = sum_g chi(g) j_g is nonzero after reduction at the p24 prime.
```

The dominant complex conjugate proves `T_chi != 0` before reduction, but does
not prove its reduction is nonzero.

So the theorem boundary is now exact:

```text
1. Bounded local modular identities are impossible by finite-field fiber degree.
2. Additive equivariant identities are projector-sized if reduced normality holds.
3. The only plausible positive route is a growing-degree embedded object,
   such as the third target's degree-3107441 recovery polynomial or an
   equivalent oriented cycle invariant, together with a way to choose its
   embedded quotient phase without enumerating the class set.
```

This is why the third target remains the best certificate-shaped route even
after the no-go work: `n=3107441` is genuinely below `sqrt(p)`, while bounded
level is now ruled out at the theorem level.
