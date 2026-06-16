# X1 Tower Sampling Conservation

This note records the remaining loophole in the direct `2^40` verifier route:
could one sample high-level `X1(2^h)` points top-down faster than the usual
one-bit-per-level rejection lift?

## Cost Identity

For p24 the verifier depth is

```text
k = 40.
```

Suppose a sampler produces curves with a marked rational x-only point of
order `2^h`.  The remaining tail to exact verifier depth has density
approximately

```text
2^{-(k-h)}.
```

If the level sampler costs `C_h`, then the expected work is

```text
C_h * 2^{k-h}.
```

The ordinary recursive lift from `X1(16)` costs

```text
C_h = 2^{h-4},
```

so

```text
2^{h-4} * 2^{40-h} = 2^36 = 0.06871948 * sqrt(p).
```

This is the p23-style constant factor, not an exponent change.

## What A Win Would Require

Write

```text
C_h = 2^{beta*(h-4)}.
```

Then a genuine asymptotic speedup from the tower needs

```text
beta < 1.
```

The rerun of

```text
p24/x1_tower_mitm_cost_audit.py
p24/inverse_tower_intersection_degree_audit.py
```

prints exactly this boundary.  With `beta=1`, every split has the same
`2^36` post-`X1(16)` cost.  With hypothetical `beta=0.75`, the work would
drop sharply, so the missing object is not ambiguous: it is a subdensity
sampler for nested quadratic oriented lifts.

## Why The Obvious Top-Down Attempts Do Not Supply It

```text
rejection through the tower:
  pays one bit per lift;

inverse-chain MITM:
  balances degrees but keeps Bezout product 2^40;

branch-word MITM:
  enumerating branch words leaves a positive-dimensional base family until
  one evaluates over field parameters or adds equations, returning to the
  density/high-genus cost;

X0 or symmetric quotients:
  forget the generator orientation and leave the X0 -> X1 ray tail;

generic point generation on X1(2^h):
  avoids rejection only by working on a curve whose degree/gonality/genus
  grows with the same oriented level.
```

Thus a top-down sampler is not ruled out by a formal impossibility theorem,
but it must be a genuinely p-specific section or label for the
Frobenius-fixed ray.  A mere recursive presentation of the tower does not
change the entropy accounting.

## Boundary

The direct verifier route and the CM period route now have parallel missing
objects:

```text
direct verifier:
  p-specific label for the X0 -> X1 orientation tail at depth 40;

CM quotient:
  p-specific embedded non-genus relative-period packets for 157/211.
```

Neither is visible in the current small-field calibrations.
