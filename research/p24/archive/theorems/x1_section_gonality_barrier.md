# X1 Section Gonality Barrier For p24

The strict DANGER3 verifier needs an x-only point of exact order

```text
N = 2^40 = 1099511627776.
```

Up to the harmless sign quotient `P ~ -P`, this is the modular curve
`X1(N)`: a curve plus a marked point of order `N`.  The Montgomery condition
adds rational 2-torsion, but that is fixed-level structure and does not change
the asymptotic growth in `N`.

For powers of two,

```text
[SL2(Z) : Gamma1(N)] = N^2 * (1 - 1/2^2) = (3/4) * N^2.
```

Abramovich's gonality lower bound is linear in the modular-curve index, so

```text
gonality(X1(2^a)) = Omega(N^2).
```

Quotienting by the sign of the marked point changes this by at most a constant
factor.  Thus any algebraic one-parameter sampler that truly marks order `N`
torsion has degree at least `Omega(N^2)`.

This matters for the requested asymptotic speedup.  Prescribing order `N`
torsion improves the DANGER target density by about `N`, but a generic
algebraic sampler for that condition costs at least `N^2`.  If a proposed
tower section has overhead `N^alpha`, it must have `alpha < 1` to beat
sqrt-scale search.  Gonality rules out such a section when it is a genuine
rational or bounded-genus parametrization of the growing `X1(2^a)` condition.

For p24 specifically:

```text
N = 2^40
index(Gamma1(N)) = 3 * 2^78
```

so the geometry is wildly beyond the range where an optimized plane model or a
hidden rational line can explain the target.  This is consistent with the
local equation audit:

```text
X1(32): degree_y=10
X1(64): degree_y=40
```

and with the failed inverse-chain section probes in `x`, `s=x+1/x`, and the
edge coordinate `r`.

What remains possible is not a rational tower section.  A surviving p24 route
would need genuinely p-specific arithmetic, such as a special exact-trace
construction, a non-generic finite-field root-squareclass identity, or a
certificate format outside the strict DANGER3 x-only order-`2^40` condition.
