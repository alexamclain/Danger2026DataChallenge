# Two-Adic Trace Inversion Sidecar

Question: can Satoh/AGM/canonical-lift machinery, Hasse-invariant labels,
theta constants, or Legendre/Landen recurrences be inverted to construct a
Montgomery or Legendre parameter whose Frobenius has eigenvalue

```text
lambda == 1 mod 2^40
```

faster than sqrt-scale search for

```text
p = 10^24 + 7
k = 40
```

instead of only testing a supplied curve?

## Verdict

I do not see a p24-compatible inversion shortcut in the standard 2-adic
point-counting machinery.  The reason is structural: forward 2-adic trace
methods compute the Frobenius action on the 2-adic Tate module, or on a
canonical/isogeny-theoretic lift of it.  Asking for an inverse with
`lambda == 1 mod 2^40` is asking for a curve together with a Frobenius-fixed
2^40-torsion direction.  That is the `X1(2^40)` or ray-orientation condition,
not merely an `X0(2^40)` trace/cyclic-subgroup condition.

The local audits already isolate the obstruction:

```text
p24/x0_orientation_audit.py
p24/x0_eigenvalue_orientation_audit.py
p24/ray_orientation_audit.py
p24/x0_orientation_barrier.md
p24/half_level_x0_lift_sidecar.md
p24/x1_section_gonality_barrier.md
```

They show that `X0` depth is cheap only because it omits the orientation.  The
missing orientation is exactly the information needed by the strict DANGER3
verifier.

## Forward trace algorithms do not choose the inverse branch

For an ordinary elliptic curve over `F_p`, Frobenius on the 2-adic Tate module
has eigenvalues `lambda, mu` with

```text
lambda * mu == p
t == lambda + mu.
```

A strict curve-side DANGER point of order `2^k` requires a fixed vector modulo
`2^k`, equivalently

```text
lambda == 1 mod 2^k
```

on one oriented 2-primary direction.  The twist side is the analogous
`lambda == -1 mod 2^k` statement.

Satoh/canonical-lift and theta/AGM/Landen style algorithms are excellent
forward tests: given a Legendre or Montgomery parameter, they recover the
2-adic Frobenius data by following canonical square-root/isogeny choices and
then reconstructing the trace.  Reversing them requires choosing the same
2-adic branches before the curve is known.  Those branch choices are the
level-`2^k` ray data.

In moduli terms:

```text
curve parameter A or lambda            : X(1), X(2), or Montgomery line
rational cyclic 2^h subgroup           : X0(2^h)
marked point / fixed eigenvector       : X1(2^h), up to +/- for x-only
```

Thus an inversion that outputs `A` with `lambda == 1 mod 2^40` is not an
inverse to the cheap `X0` trace calculation.  It is a constructive section of
the growing `X1`/ray tower, or an equivalent p-specific trace-class selector.
The existing gonality/degree audit rules out a generic low-degree section of
that tower.

## What the p24 eigenvalue arithmetic says

The exact target trace residue on the curve side is

```text
t == p + 1 mod 2^40
t == 1020608380936 mod 2^40
```

For an `X0(2^a)` cyclic subgroup, Frobenius acts by an odd eigenvalue
`lambda mod 2^a`, and

```text
t == lambda + p/lambda mod 2^a.
```

For the DANGER residue this factors as

```text
lambda^2 - (p+1)lambda + p == 0 mod 2^a
(lambda - 1)(lambda - p) == 0          mod 2^a.
```

Since `v2(p-1)=1`, there are four roots for `a >= 2`.  The deterministic
p24 audit gives, at `a = 40`:

```text
lambda        mu             v2(lambda-1)  v2(mu-1)  X1?
1             1020608380935  40            1         yes
470852567047  549755813889   1             39        no
549755813889  470852567047   39            1         no
1020608380935 1              1             40        yes
```

So even the full `X0(2^40)` trace residue does not canonically identify the
strict `X1` orientation.  It knows a stable line; the verifier needs a fixed
generator on that line.

The size count is equally unforgiving:

```text
X0 trace-residue image at 2^a: 2^(a-3) residues = 1/8 of all residues
target eigenvalue preimages:  4
Gamma0(2^40) index:          1649267441664 = 1.649267 * sqrt(p)
Gamma0(2^41) index:          3298534883328 = 3.298535 * sqrt(p)
```

Thus shifting from `X1` to a deeper `X0` or to a trace-only 2-adic computation
does not improve the exponent for p24.

## Legendre lambda and theta recurrences

The Legendre/Landen transformation and theta-constant recurrences make the
same distinction in coordinates.  Starting with

```text
E_lambda: y^2 = x(x-1)(x-lambda),
```

the Landen step uses square-root choices of expressions such as `lambda`,
`1-lambda`, or theta ratios to move along the 2-isogeny tree.  Given
`lambda`, a point-counting algorithm can choose compatible roots and read off
Frobenius information.  But to construct a `lambda` with `lambda_Frob == 1 mod
2^40`, an inverse recurrence must prescribe a coherent depth-40 branch of the
2-isogeny/ray tree.

That coherent branch is precisely a level-`2^40` marked-torsion datum.  A
half-level split illustrates the bookkeeping.  If one first constructs
`X0(2^h)` data with `h ~= 20`, then a half-level eigenvalue near the strict
branch has the form

```text
lambda = 1 + 2^h u mod 2^40.
```

The strict condition forces

```text
u == 0 mod 2^(40-h).
```

The `X0` datum does not contain this high tail.  Choosing it is the missing
ray/X1 lift.  The product

```text
[SL2:Gamma0(2^h)] * 2^(40-h)
  = 3*2^(h-1) * 2^(40-h)
  = 3*2^39
  = Theta(sqrt(p))
```

is independent of the split point.

## Hasse invariant labels

The Hasse invariant is also a forward label, not a cheap inverse selector.
For Legendre curves, the Hasse polynomial has degree `(p-1)/2`, and its value
modulo `p` determines the trace modulo `p`; since the Hasse interval is shorter
than `p` here, that is enough to identify the trace.  But inverting

```text
H_p(lambda) == target_trace mod p
```

means solving a degree about `p/2` equation over `F_p`.  It is an exact
trace-bucket equation, not a bounded-degree construction.  Without a special
identity for this exact `p`, it is at least as much trace entropy as the
sqrt-scale search we are trying to beat.

This matches the CM audits: the strict p24 traces have conductor `2` but
fundamental discriminants comparable to `p`, with class-size estimates about
`2.06e11` to `8.33e11`.  Hasse/CM labels can verify or describe the target
classes, but they do not select one root cheaply.

## Falsifiable small-prime test

A positive inversion claim should pass this test before any p24 search:

1. Use small near-square primes `p = n^2 + 7` where exact Montgomery trace
   convolution is cheap.
2. Set `k = verifier_k(p)` and pick a half-level `h ~= k/2`.
3. Enumerate all nonsingular Montgomery or Legendre parameters only for the
   small calibration rows, and compute exact traces.
4. For each candidate 2-adic inversion label, such as a canonical-lift theta
   branch, Landen branch product, terminal isogenous `j`, branch squareclass,
   Hasse-invariant residue, or low-degree character of the chain, condition on
   the same `X0(2^h)` data available to the proposed algorithm.
5. Measure whether the label predicts the missing tail

```text
lambda = 1 + 2^h u,  u == 0 mod 2^(k-h)
```

with advantage growing as a power of `2^(k-h)`, while using only
`2^o(k)` branch work.

Passing would mean the hit rate for full strict `X1(2^k)` stays polynomially
larger than the random `2^-(k-h)` tail after conditioning on `X0(2^h)`, and
the selected parameters pass exact point counting.  Failing means the proposed
inversion is only a forward trace test or a disguised enumeration of the
missing ray branches.

The existing exact checks are negative for the visible low-degree labels:

```text
p24/x0_orientation_character_scan.py
p24/ray_orientation_audit.py
p24/isogeny_chain_compression_audit.py
p24/partial_oriented_sampler_exponent_audit.py
```

## Conclusion

Standard 2-adic point-counting machinery gives fast verification of
Frobenius data for a supplied curve.  Inverting it to construct a p24 strict
DANGER3 curve would have to supply the depth-40 Frobenius-fixed ray
orientation.  In the known moduli descriptions, that is exactly the
`X1(2^40)` tower.  Without a new p-specific identity that predicts the missing
ray tail, this route falls back to `Theta(sqrt(p))` scale rather than beating
it.
