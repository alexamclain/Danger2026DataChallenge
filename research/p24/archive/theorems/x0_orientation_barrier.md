# X0(2^a) Orientation Barrier for p24

For a curve with a rational cyclic `2^a`-isogeny, Frobenius acts on the cyclic
subgroup by some odd eigenvalue `lambda mod 2^a`.  The trace satisfies

```text
t == lambda + p/lambda mod 2^a.
```

For the DANGER3 verifier, however, we need a rational `2^a` x-only point on the
curve or its quadratic twist.  In eigenvalue terms this means selecting the
special orientations

```text
lambda =  1   curve side
lambda = -1   twist side
```

up to the matching dual orientation.

For `p = 10^24 + 7`, we have

```text
p == 7 mod 16.
```

Enumeration in `x0_orientation_audit.py` shows the stable pattern:

```text
modulus = 2^a
odd eigenvalues lambda:             2^(a-1)
X0 trace-residue image size:        2^(a-3)
target-trace eigenvalue preimages:  4
```

Thus sampling from `X0(2^a)` and asking for the DANGER trace residue succeeds
with conditional probability

```text
4 / 2^(a-1) = 1 / 2^(a-3).
```

For an unconstrained trace modulo `2^a`, the same residue has probability

```text
1 / 2^a.
```

So the entire growing `X0(2^a)` condition buys only the constant factor

```text
2^a / 2^(a-3) = 8.
```

The missing information is exactly the orientation/eigenvalue lift from
`X0(2^a)` to `X1(2^a)`.  Selecting that orientation is a growing cover; the
generic version reintroduces the same level-size barrier that the X0 route was
trying to avoid.

## Half-Level Split

The seductive split is to construct only `X0(2^d)` for `d ~= k/2`.  For p24,
`d = 20` has modular index about `p^(1/4)`, so it looks like the right scale
for a meet-in-the-middle.

But `X0(2^d)` carries only the invariant cyclic subgroup, not the generator
orientation.  After that split, two independent pieces of information remain:

```text
trace lift from 2^d to 2^k:       2^(k-d) choices
X0-to-X1 orientation at level d:  2^(d-2) choices
```

Their product is independent of the split point:

```text
2^(k-d) * 2^(d-2) = 2^(k-2).
```

So the half-level trick only moves the missing entropy between trace depth and
orientation depth.  It becomes an exponent-saving algorithm only if some new
identity supplies one of those two piles of bits constructively.  The local
audits have not found such an identity: exact `X0` chain membership remains a
constant-factor trace condition, and the only stable `X0`-to-`X1` character
gate is the singular `A = +/-2` branch rejected by the verifier.
