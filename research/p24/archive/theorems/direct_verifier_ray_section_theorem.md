# Direct Verifier Ray-Section Theorem

This note consolidates the direct `Z_k(A,x)=0` verifier route.  It is the
2-adic analogue of the CM period-selector boundary: algebraic equations for
torsion are easy to write, but selecting a finite-field point on the correct
ray is the whole problem.

## Literal Verifier

The official verifier iterates the Montgomery x-only doubling map

```text
X,Z -> U*V, W*(V+C*W)
C = (A+2)/4
```

for

```text
k = 40,       2^k = 1099511627776.
```

It accepts when `Z_k=0` and `Z_{k-1} != 0`.

The exact small-field audit

```text
p24/verifier_equivalence_audit.py
```

confirms that this is exactly the existence of an x-coordinate of exact
x-only order `2^k` on the curve or quadratic twist.

## Algebraic Torsion Is Not The Selector

Over `Fbar_p`, every nonsingular elliptic curve has full `2^k` torsion.
Therefore the algebraic equation

```text
Z_k(A,x)=0
```

projects to essentially every nonsingular `A`.  Eliminating `x` from the
division equation forgets the rare arithmetic condition.

The finite-field condition is that Frobenius fixes one exact-order ray:

```text
lambda ==  1 mod 2^k       curve side
lambda == -1 mod 2^k       twist side.
```

In moduli language this is a point of `X1(2^k)/{+-1}` above the Montgomery
`X(2)` line, not just the existence of an algebraic torsion point.

## No Generic Low-Degree Section

A rational construction that uniformly outputs such an x-coordinate from a
generic curve parameter would be a section of the growing `X1(2^k)/{+-1}`
cover.  The known modular-curve geometry rules out a bounded-degree or
bounded-genus section:

```text
[SL2(Z):Gamma1(2^k)] = 3 * 2^(2k-2),
```

and Abramovich-type gonality bounds are linear in the modular index.  Thus a
generic algebraic parametrization of marked `2^k` torsion is far larger than
the requested `sqrt(p)` scale.

The p24 search target is subtler than the full generic cover: it only needs
one `F_p` point.  But any finite-field identity that beats square-root search
must be genuinely p-specific; it cannot be the generic universal halving
section.

## Split/MITM Degree Accounting

Splitting the inverse chain at depth `a+b=k` gives two lower-degree algebraic
conditions, but their intersection degree remains the product:

```text
degree(C_a) * degree(D_b) = 2^a * 2^b = 2^k.
```

For p24:

```text
2^40 / sqrt(p) = 1.099512...
```

So a balanced `20+20` meet-in-the-middle lowers the largest individual degree
to `2^20`, but not the total ray entropy.  Exact small-field calibration in

```text
p24/inverse_chain_state_entropy_audit.md
```

shows the same reciprocity statistically: partial inverse-depth filters and
residual rarity multiply back to the full-depth cost.

## Coordinate Changes Already Tested

The following coordinate-section attempts have been tested and collapse to
constant or degenerate/singular cases:

```text
geometric x-chain
Mobius/LFT x-chain
s = x + 1/x chain
edge square-root coordinate r
power/Chebyshev semiconjugacy
second-order Lucas/Chebyshev recurrence
parabolic LFT limit
low-degree pair relations in (A,x)
fixed/simple x-coordinate fibers
```

The conceptual reason for the power-map route is especially clean:

```text
Chebyshev/power quotient:        orbifold type (2,2,infinity)
nonsingular Montgomery Lattes:   orbifold type (2,2,2,2)
```

These parabolic orbifold types are not rationally semiconjugate except in
singular limits `A=+-2`, which the verifier rejects.

## Compression Refresh

The latest verifier-side sidecar checked the remaining non-CM compression
ideas against the same boundary.

```text
resultants / MITM:
  split degrees can be balanced, but the Bezout product remains 2^40;

rational canonical forms:
  package the inverse tree or Frobenius action, but selecting lambda=+-1
  is still the marked X1 ray condition;

extension-field trace/norm:
  trace or norm of an extension-field torsion x-coordinate is not compatible
  with the x-only Lattes dynamics and fails in toy checks;

low-genus X0 quotients:
  remember a cyclic subgroup but forget the generator orientation, leaving
  the X0 -> X1 tail.
```

Thus the exact compression dichotomy is:

```text
forget the marked ray -> X0/symmetric quotient with residual orientation tail;
retain the marked ray -> X1(2^40)/+- scale.
```

No non-CM finite-field identity is visible that predicts the missing
`X0 -> X1` ray orientation for the fixed p24 prime.

The top-down tower-sampling loophole is now separated in:

```text
p24/x1_tower_sampling_conservation.md
p24/x0_x1_tail_entropy_theorem.md
```

A level-`2^h` sampler gives an exponent win only if it costs
`2^{beta*(h-4)}` with `beta < 1` from the cheap `X1(16)` base.  Ordinary
recursive lifting has `beta=1`, so its cost times the residual tail is always
`2^36 = 0.06871948*sqrt(p)`.  Branch MITM and inverse-chain intersections
move this entropy between stages but do not create the needed subdensity
sampler.

The local tail count is exact: even after fixing the oriented branch
`lambda == 1 mod 2^h`, there are `2^(k-h)` lifts modulo `2^k`, only one of
which is the true `X1` lift.  The strict trace residue has two such lifts, one
of which is the non-`X1` root with `v2(lambda-1)=k-1`.

The mixed odd/2-adic reverse-SEA branch is similarly bounded in:

```text
p24/mixed_level_oracle_refresh.md
```

A wider optimistic oracle search over `80940` mixed levels still picked pure
`2^40` as the best Gamma0/proxy tradeoff (`proxy/sqrt=1.649267`).  Shallower
2-adic prefixes plus odd exact residues can isolate the target traces, but
their Gamma0 lower bounds are several `sqrt(p)`, and a real construction
would need richer marked/eigenvalue data.

## Boundary

The direct verifier route is not closed in the absolute sense, because a
one-prime finite-field identity could still exist.  But the theorem boundary
is now precise:

```text
A successful direct construction must predict the Frobenius-fixed 2^40 ray
over F_p by p-specific arithmetic, not merely solve or parametrize the
universal division-polynomial equation.
```

No such p-specific ray label is visible in the current near-square,
low-height, dataset, or class-field audits.
