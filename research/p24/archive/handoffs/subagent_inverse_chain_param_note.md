# p24 Inverse-Chain Parametrization Note

Date: 2026-06-04 PDT

Question: can the strict verifier inverse chain be parametrized in a genuinely
high-dimensional way that beats `sqrt(p)` for

```text
p = 10^24 + 7
k = 40
N = 2^40 = 1099511627776 ~= sqrt(p)
```

while avoiding the existing low-dimensional no-gos in `x`, `s=x+1/x`, and edge
coordinates?

## Verdict

I do not see a credible high-dimensional loophole.  The crisp obstruction is
that the full inverse-chain certificate variety is still the growing
`X1(2^k)` ray/orientation condition, up to the harmless `P ~ -P` quotient.
Adding chain variables, recurrence states, transfer matrices, or a
meet-in-the-middle midpoint changes the coordinates on that curve or on
finite covers of it; it does not remove the missing Frobenius-fixed
orientation.

A high-dimensional parametrization would beat `sqrt(p)` only if it supplied a
bounded/sublinear-degree constructive map to the strict level-`2^k` curve.  But
any bounded-complexity dominant algebraic family can be sliced down to a curve,
giving a low-degree map to `X1(2^k)/{+/-1}`.  The gonality/index barrier in
`x1_section_gonality_barrier.md` then applies: for `N=2^k`,

```text
[SL2(Z):Gamma1(N)] = (3/4) N^2
gonality(X1(N)) = Omega(N^2).
```

Since the density gain from prescribing order-`N` torsion is only about `N`,
any generic algebraic section whose degree grows enough to respect gonality has
already lost the desired exponent.

This is not a theorem against all possible p-specific identities.  It is a
no-go for the proposed high-dimensional inverse-chain packaging unless the
package contains new arithmetic that predicts the missing 2-adic ray tail for
this exact `p`.

## Why More Variables Do Not Change The Moduli Problem

The literal x-only verifier equation can be written as

```text
Z_k(A, x_0) = 0,       Z_{k-1}(A, x_0) != 0,
```

where `Z_i` is the Montgomery ladder denominator after `i` doublings.  If the
intermediate inverse-chain points are included,

```text
f_A(x_i) = x_{i+1},    x_k = infinity,
```

the added variables are constrained by the same chain equations.  Over the
algebraic closure this is not a large free-dimensional object; it is a
coordinate expansion of the modular curve carrying a point of order `2^k`.
Over `F_p`, the hard part is not geometric existence of preimages.  The hard
part is Frobenius rationality of the oriented `2^k` point, equivalently

```text
lambda == 1 mod 2^k        curve side
lambda == -1 mod 2^k       twist side.
```

The existing audits show the same separation:

```text
post_trace_construction_audit: x0 is constant expected work after A is known
x_projection_concentration_audit: fixed x has only constant-sized A fibers
pair_relation_rank_audit: no low-degree component in the accepted (A,x) set
```

So a high-dimensional chain parametrization has to select the rare trace class
of `A`; it cannot merely make inverse preimages easier.

## Multi-Variable Recurrences

A recurrence with state dimension `d`,

```text
v_{i+1} = R(v_i; theta),      A = G(v_i, v_{i+1})
```

would be useful only if the same `theta` forces `A` to remain constant for
`k` levels and makes the terminal branch rational over `F_p`.  If `d` and the
degrees are bounded or sublinear in `k`, slicing the parameter space by generic
linear conditions leaves a low-degree curve mapping into the strict
level-`2^k` certificate curve.  That is exactly the type of section forbidden
by gonality.

If the recurrence has enough independent choices to avoid this, those choices
are the inverse-branch/ray choices.  Their entropy is the missing tail.  This
matches the low-dimensional symbolic probes:

```text
inverse_chain_ansatz.py
inverse_chain_lft_ansatz.py
inverse_chain_s_coordinate_ansatz.py
edge_coordinate_ansatz.py
```

They fail by collapsing to constant or singular orbits.  A higher-dimensional
version can avoid those resultants only by retaining a growing branch space,
which is not an exponent-saving parametrization.

## Transfer-Matrix Shape

A transfer matrix would be promising if the inverse chain could be encoded as

```text
v_i = M(theta)^i v_0
```

with a low-dimensional matrix `M`, and the verifier condition became a cheap
order/eigenvalue test.  That would semiconjugate the elliptic Kummer doubling
map to a torus/Chebyshev/power map.

The obstruction in `semiconjugacy_obstruction.md` is exactly that this
linearization exists only in the singular cases `A = +/-2`: the nonsingular
Montgomery Kummer map is an elliptic Lattes quotient of orbifold type
`(2,2,2,2)`, not the Chebyshev/power type `(2,2,infinity)`.  The separate
`torus_degeneration_audit.py` also records that for p24 the split and nonsplit
singular tori have only `v2(p-1)=1` and `v2(p+1)=3`, far below depth `40`, and
the verifier rejects `A = +/-2`.

Thus a transfer matrix that really beats the exponent would be a forbidden
linearization of nonsingular elliptic doubling, or it would be a disguised
description of the usual 2-adic Tate-module action whose inverse requires
choosing the same `X1` ray.

## Elliptic Divisibility Sequence Shape

Division-polynomial and elliptic-divisibility-sequence recurrences are native
to this problem:

```text
Z_k(A, x) = 0
```

is already the x-only EDS/division condition.  EDS recurrences can compute or
verify multiples quickly once `A` and `x` are supplied, but forcing the
`2^k`-th denominator to vanish over `F_p` is the assertion that the point is a
rational `2^k`-torsion point.  In moduli language, that is again `X1(2^k)`.

A special EDS identity could still be real if it came from a special trace
identity for this `p`.  The only visible near-square identity is the
`D=-7` CM trace `t=+/-2*10^12`, and
`finite_field_identity_sidecar.md` records that both curve and twist have only
`v2=3`.  The strict target discriminants have conductor `2` and fundamental
discriminant comparable to `p`, so the CM/EDS route falls back to
`Theta(sqrt(p))` class entropy.

## Meet-In-The-Middle With Algebraic Elimination

The attractive split is `h ~= k/2`:

```text
build depth h data, then eliminate/match the remaining k-h levels.
```

The half-level sidecar gives the clean entropy identity.  If the first stage is
only `X0(2^h)`, it records a stable line but not the fixed generator.  The
missing strict tail is

```text
lambda = 1 + 2^h u mod 2^k,    u == 0 mod 2^(k-h).
```

The product is invariant:

```text
[SL2:Gamma0(2^h)] * 2^(k-h)
  = 3*2^(h-1) * 2^(k-h)
  = 3*2^(k-1)
  = Theta(sqrt(p)).
```

If the first stage is `X1(2^h)`, the residual `X1` tail has the same
multiplicative bookkeeping.  This is exactly what
`inverse_chain_mitm_tradeoff_audit.py` measures at small exact scale:
partial-depth stage cost times residual full-depth cost stays equal to the
full-depth cost.  `inverse_mitm_scaling_audit.py` also finds that inverse-tree
mass is a constant-factor ranking signal, not a sub-sqrt `A` selector.

Algebraic elimination does not change that accounting.  Eliminating a
midpoint between two half-chains produces the same modular/division condition
with degree growth in the eliminated variable.  If the elimination degree is
kept small, it would be a low-degree section; if it is allowed to grow, the
growth is the saved search reappearing as resultant/root-finding cost.

## Falsifiable Remaining Loophole

The only surviving shape would be a genuinely p-specific arithmetic label on
partial chain data that predicts the high ray tail with growing advantage:

```text
condition on X0(2^h) or shallow X1 data,
compute a cheap label L from the chain,
Pr[full strict X1(2^k) | L] >> 2^-(k-h)
```

where `L` is not itself a degree-`2^(k-h)` ray-class function.  Existing scans
of low-degree characters, branch gates, additive/multiplicative spectra,
moments, and pair relations are negative.  A proposed label should be tested
on small exact `p=n^2+7` rows by conditioning on the same partial data and
measuring whether the full-depth hit rate gains a power of `2^(k-h)`, not just
a constant factor.

## Bottom Line

The high-dimensional inverse-chain idea appears to be a coordinate
repackaging of the same strict `X1(2^40)` condition.  Multi-variable
recurrences, transfer matrices, EDS formulas, and MITM elimination either:

```text
1. collapse to singular/constant/low-depth cases already rejected;
2. give only post-trace x0 construction after A is known;
3. provide X0/cyclic-subgroup data while omitting the verifier orientation; or
4. carry the full growing X1 ray tail, restoring Theta(sqrt(p)) cost.
```

So the current best report is a crisp entropy/gonality no-go, with no concrete
candidate route unless a new p24-specific finite-field identity is found.
