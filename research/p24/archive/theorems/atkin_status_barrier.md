# Atkin/Elkies Status Filter Barrier

For an odd prime `ell`, the cheap trace information one might hope to use is
the Atkin/Elkies status

```text
delta_ell = t^2 - 4p mod ell,
```

namely whether `delta_ell` is a square, nonsquare, or zero.  This is weaker
than knowing `t mod ell`, but can sometimes be tested by asking whether the
classical modular polynomial `Phi_ell(j,Y)` has a root over `F_p`.

The p24 target traces do force useful statuses for a few small primes.  For
example, at 2-adic depth 28 with the signed x-only target traces:

```text
ell=5   target_status=[-1]
ell=7   target_status=[-1,0]
ell=13  target_status=[-1]
```

and the best size-3 status combo among `5,7,11,13,17,19,29,31,37,41` leaves

```text
3441 / 14901 = 0.230924
```

of the `2^28` trace lattice.

This is a real constant-factor trace filter, but it does not beat the
sqrt-scale search by itself:

1. **As a rejection filter**, it does not change the entropy of drawing random
   curves.  It only avoids later work on rejected candidates.  The active
   halving predicate is already very cheap on average.

2. **As construction data**, requiring Elkies/root statuses for many primes is
   an `X0(N)`-type condition with growing level `N`.  Requiring Atkin/no-root
   statuses is an inequality condition that is naturally enforced only by
   rejection.  Neither gives a cheap direct sampler for the exact target
   isogeny class.

3. **Status is too weak to certify the exact trace.**  To isolate a trace in a
   Hasse interval using only quadratic-character bits requires many primes.
   Enforcing those bits constructively recreates a growing modular-curve
   problem; testing them rejectively preserves the original random-candidate
   scale.

So Atkin/Elkies status predicates are useful for modeling and possibly for
small constant-factor ordering, but they are not an asymptotic speedup route
for the strict DANGER3 p24 certificate.
