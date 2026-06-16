# Tower Section Obstruction

This note isolates a small theorem about embedded class-field towers.  It is
not the full negative theorem, because unordered relative child polynomials
are still allowed.  It does explain exactly why a tower does not by itself
select a CM root.

## Setup

Let `G = Cl(O)` act simply transitively on the embedded ordinary CM roots

```text
j_g in F_p,        g in G.
```

Let

```text
L <= K <= G
```

be one refinement layer in a quotient tower.  A parent is a `K`-coset in
`G/K`; its children are the `L`-cosets lying above it, i.e. the fiber of

```text
pi : G/L -> G/K.
```

For the p24 third-trace tower these layers are:

```text
G -> K1,       [G:K1] = 2,    |K1| = 157 * 211 * 3107441
K1 -> K2,      [K1:K2] = 157, |K2| = 211 * 3107441
K2 -> H,       [K2:H] = 211,  |H|  = 3107441
```

## No Equivariant Child Selector

There is no `G`-equivariant section

```text
s : G/K -> G/L,        pi o s = id
```

unless `K=L`.

Proof: since `pi(s(K))=K`, write `s(K)=aL` with `a in K`.  For every
`k in K`, equivariance gives

```text
s(K) = s(kK) = k s(K) = kaL.
```

Thus `kaL=aL`, so `a^{-1}ka in L`.  In the p24 class groups are cyclic, hence
abelian, and this forces `k in L` for every `k in K`.  Therefore `K <= L`.
The reverse inclusion was assumed, so `K=L`.

Interpretation: a seedless modular rule cannot canonically name one child
inside a nontrivial tower fiber.  Naming a child requires extra phase data,
an external seed, or a finite-field operation that is not a modular
`G`-equivariant construction.

The finite stabilizer implication is checked in:

```text
p24/lean/TowerSectionObstructionGate.lean
```

Lean formalizes the part used here: if every element of `K` fixes the parent
point and a selector is equivariant, then every element of `K` fixes the
selected child.  If the selected child's stabilizer is `L`, this forces
`K <= L`; a witness in `K \ L` rules out the selector.

## What Remains Allowed

The theorem does not rule out the useful tower object:

```text
F_a(Y) = product_{u in K/L} (Y - y_{a u L})
```

where

```text
y_{bL} = sum_{l in L} j_{b l}.
```

This polynomial is unordered over the children and is perfectly
`G`-equivariant.  It is the right object for a root-finding tower: choose any
root of `F_a` over `F_p`, then continue to the next layer.

The hard part is computing the embedded relation

```text
F(Z,Y) = 0
```

that pairs a parent value `Z` with its correct child polynomial, without first
enumerating the embedded CM torsor.

## Relative Character Form

If a cyclic generator identifies `K/L` with `Z/rZ`, then the child periods
above a parent are recovered from relative character traces

```text
T_s(aK) = sum_{u in K/L} zeta_r^(s u) y_{a u L}
        = sum_{k in K} chi_s(k) j_{a k},
        0 <= s < r.
```

The trivial trace `T_0` is just the parent period.  The nontrivial `T_s`
carry the missing relative phase.  Once these traces are known, inverse DFT
gives the child periods and hence the relative child polynomial.

The toy check

```text
p24/relative_tower_character_toy.py
```

verifies this in the exact `D=-5000`, `h=30=2*3*5` calibration tower.  Because
`F_1259` does not contain a primitive third root of unity, the nontrivial
relative traces live in `F_{1259^2}`; inverse DFT descends back to the child
periods in `F_1259`.

## Boundary

This makes the missing theorem precise:

```text
Compute the relative non-genus class-character traces for the p24 tower
layers 2, 157, and 211, embedded relative to j, without class enumeration or
a degree-h class polynomial.
```

The finite-field degree theorem already says any single child-period
coordinate has degree at least the relevant subgroup size.  For p24 those
sizes are still below `sqrt(p)`, so this is not an impossibility theorem.  It
is a proof that the tower needs a genuine relative phase theorem; abstract
class-field degrees and quotient factorization alone cannot select the root.
