# Subagent Modular/Tower Loophole Note

Date: 2026-06-04 PDT

Target:

```text
p = 10^24 + 7
k = 40
N = 2^k = 1099511627776
sqrt_floor(p) = 1000000000000
```

## Verdict

I found no verifier-compatible modular-curve, Landen/AGM, canonical-lift, or
finite-field-tower route that constructs a strict depth-40 Montgomery x-only
point in `o(sqrt(p))` work.

The obstruction is the same in each language: the verifier needs a
Frobenius-fixed 2-adic ray,

```text
lambda ==  1 mod 2^40   curve side
lambda == -1 mod 2^40   twist side
```

on an oriented cyclic 2-primary line.  `X0` data, isogeny chains, Landen
branches, canonical-lift traces, and extension-field torsion can expose or test
a stable line, but they do not give the missing eigenvalue tail unless they
have already solved the `X1(2^40)` orientation problem.

## X1(2^k)

A strict triple `(A,x)` is a point of `X1(2^40)/{+/-1}` with the fixed
Montgomery level-2 structure.  For `N=2^a`,

```text
[SL2(Z):Gamma1(N)] = (3/4) N^2.
```

Thus at `a=40` the growing oriented level is size `3*2^78`.  The target-density
gain from prescribing `N`-torsion is only about `N`, so a generic tower section
would need sublinear overhead in `N`; a rational or bounded-genus section is
blocked by the gonality/index growth.  This does not exclude a p-specific
identity, but it excludes a hidden generic `X1` parametrization.

## X0-To-X1 Orientation

For an `X0(2^a)` cyclic subgroup, Frobenius acts by an odd eigenvalue
`lambda mod 2^a`, and

```text
t == lambda + p/lambda mod 2^a.
```

For the curve-side DANGER residue `t == p+1 mod 2^a`,

```text
(lambda - 1)(lambda - p) == 0 mod 2^a.
```

Since `v2(p-1)=1`, there are four roots for `a>=2`.  At `a=40`:

```text
lambda        mu             v2(lambda-1)  v2(mu-1)  strict X1?
1             1020608380935  40            1         yes
470852567047  549755813889   1             39        no
549755813889  470852567047   39            1         no
1020608380935 1              1             40        yes
```

So full `X0(2^40)` trace data still includes non-verifier orientations.  The
`X0` trace image has constant density `1/8` for this congruence class; the
missing information is not trace residue but the `X1` ray orientation.

The half-level split makes the bookkeeping explicit.  Constructing
`X0(2^h)` and then forcing the remaining tail costs, even generously,

```text
[SL2:Gamma0(2^h)] * 2^(40-h)
  = 3*2^(h-1) * 2^(40-h)
  = 3*2^39
  = 1.649267441664 * sqrt_floor(p).
```

Level-shifting to `X0(2^41)` can encode a rational order-`2^40` point after
doubling, but its index is

```text
[SL2:Gamma0(2^41)] = 3*2^40 = 3.298534883328 * sqrt_floor(p),
```

so it is not an asymptotic shortcut.

## Landen/AGM/Canonical-Lift Inversion

Landen and theta/AGM recurrences choose square-root branches along the
2-isogeny tree.  Forward use is cheap after `A` is known: it computes or checks
Frobenius data.  Reversing the recurrence must prescribe a coherent depth-40
branch before `A` is known.  In moduli terms, that branch sequence is exactly a
ray orientation.

There is no separate canonical 2-primary subgroup over `F_p` that would choose
the branch for free: `2` is prime to `p`, and the ordinary canonical subgroup
phenomenon belongs to the `p`-primary direction.  A proposed inverse branch rule
therefore has to be either:

```text
1. an X0/cyclic-chain construction, which misses lambda == +/-1 mod 2^40;
2. an X1/ray construction, which pays the growing orientation cover; or
3. a genuinely p-specific identity predicting the high tail.
```

I did not find such a p-specific identity.

## Finite-Field Towers

Changing representation does not relax the verifier: the submitted `x` must be
an element of the prime field `F_p`.  Since `F_p` has no nontrivial subfields,
a tower representation of `F_p` can only change arithmetic constants.

Using an extension field `F_{p^m}` also does not evade the orientation
condition.  Let `P` be a point of order `2^40` on an eigenline with
Frobenius action

```text
pi(P) = lambda P,   lambda in (Z/2^40 Z)^*.
```

Then `x(P) in F_p` iff `pi(P)=+P` or `pi(P)=-P`, i.e. iff
`lambda == +/-1 mod 2^40`, the strict curve/twist condition.

If instead `P` is merely defined over `F_{p^m}`, so `lambda^m == 1`, descent by
the trace map gives

```text
Q = P + pi(P) + ... + pi^(m-1)(P)
  = (1 + lambda + ... + lambda^(m-1)) P.
```

For odd `m`, the group `(Z/2^40 Z)^*` is 2-primary, so `lambda^m == 1` already
forces `lambda == 1`.  For even `m` and nontrivial `lambda`, the scalar
`1 + lambda + ... + lambda^(m-1)` is even, so the descended point loses at
least one 2-adic order bit.  The alternating trace for the twist has the same
statement with `lambda == -1`.

Thus an extension/tower can manufacture 2-power torsion over a larger field,
but a full-order verifier-compatible descent exists only when the original
Frobenius ray was already strict.

The CM extension trace identity gives the same obstruction at trace level:

```text
T_m^2 - 4 p^m = (t^2 - 4p) * U_{m-1}(t,p)^2.
```

The fundamental CM field is unchanged in extensions, so the p24 strict traces
do not become small-CM or small-class over a tower.

## Only Remaining Shape

The only live shape I can state is a falsifiable one, not a found route:
a p-specific finite-field identity that, after conditioning on cheap
`X0(2^h)` data, predicts the missing tail

```text
lambda = 1 + 2^h u mod 2^40,   u == 0 mod 2^(40-h),
```

with growing advantage over random while not itself being a degree
`2^(40-h)` ray-class function.  I found no such identity in the modular,
Landen/AGM/canonical-lift, or finite-field-tower formulations.
