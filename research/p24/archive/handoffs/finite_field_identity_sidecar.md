# Finite-Field Identity Sidecar for p24

Task: look for a theorem-level or constructive finite-field identity that
selects the strict DANGER3 trace classes for

```text
p = 10^24 + 7 = n^2 + 7,  n = 10^12,  k = 40.
```

The strict curve-side trace condition is

```text
t == p + 1 mod 2^k.
```

The x-only verifier also allows the opposite sign, but the CM discriminant only
depends on `t^2`, so the curve-side representatives are enough for this audit.

## Real Candidate: the Near-Square CM Identity

The identity `p = n^2 + 7` gives a genuine cheap trace identity.  In
`Q(sqrt(-7))`, the Frobenius element on the `D = -7` CM curve is

```text
pi = n + sqrt(-7),   Norm(pi) = p,   Trace(pi) = 2n.
```

Thus the two possible CM traces are `+2n` and `-2n`.  This would be a strict
DANGER selector exactly when one of

```text
2^k | p + 1 - 2n = (n - 1)^2 + 7
2^k | p + 1 + 2n = (n + 1)^2 + 7
```

holds.  For p24:

```text
v2((n - 1)^2 + 7) = 3
v2((n + 1)^2 + 7) = 3
```

So the near-square CM identity misses the required depth by 37 bits.  This is a
real selector for other rare `n` that are close to a 2-adic root of `-7`, and
the small-scale audit does see accidental small-CM rows for tiny fields.  It is
not a selector for the exact p24 prime.

## Other CM/Jacobi-Sum Identities

Most closed-form finite-field trace identities for a fixed algebraic parameter
are small-CM or Jacobi-sum evaluations in disguise.  Such a selector would make
the strict target trace satisfy

```text
t^2 - 4p = D f^2
```

with fixed small fundamental discriminant `D`, or at least with a large square
conductor `f`.

I added:

```text
p24/near_square_target_discriminant_audit.py
```

The p24 run gives:

```text
t=-1178414874616  fundamental_D=-652834595820939249713143  conductor=2  |D|/p=0.652835
t=-78903246840    fundamental_D=-998443569409526507503607  conductor=2  |D|/p=0.998444
t=1020608380936   fundamental_D=-739589633190799177940983  conductor=2  |D|/p=0.739590
```

Thus the exact strict p24 traces are large-discriminant CM classes with no
useful square conductor.  A CM construction for these traces has class size
`Theta(sqrt(p))`; it is the generic target-trace problem, not an identity-level
shortcut.

## Non-CM Algebraic Identities

A bounded-complexity algebraic formula `A = F(n)` or `j = F(n)` would define a
bounded-degree family of elliptic curves.  For a non-CM family, the condition

```text
a_p(E_n) == p + 1 mod 2^k
```

is a high-level Frobenius congruence.  Equidistribution heuristics, and the
existing exact small-field scans, say it has density about `2^-k` unless the
family carries the missing `2^k` torsion orientation as structure.

Carrying that structure forces the construction through modular level:

```text
X0(2^k): records a cyclic subgroup; gives only the known constant-factor
         trace-residue gain for p == 7 mod 16.

X1(2^k): records the oriented point needed by the verifier; degree/gonality
         grows like 2^(2k), so it is not a sub-sqrt construction when
         2^k is already about sqrt(p).
```

This matches the local audits: `X0` loses the orientation, while `X1` pays the
growing cover cost.

## Falsifiable Test for Any New Claimed Selector

A proposed identity should pass one of these tests at small exact scale:

1. If it is CM-like, factor `t^2 - 4p`; a real cheap identity should show
   bounded `D` or a growing conductor.  The new discriminant audit does this.
2. If it gives a formula for `A`, `j`, or an upstream parameter, evaluate it on
   small primes `p = n^2 + 7` and use the exact Montgomery trace convolution.
   A selector should hit the strict trace bucket consistently, not merely raise
   the hit density by a constant.
3. If it constructs an `x0` chain, plug it into the literal verifier or exact
   x-only order audit.  A genuine section should survive across rows; a partial
   inverse-tree filter will decay with depth.

Conclusion: I found no p24-compatible finite-field identity selector.  The only
real theorem-level selector exposed by `p = n^2 + 7` is the `D = -7` CM trace,
and the exact 2-adic test shows that p24 is not in its strict DANGER branch.
