# p24 Admissible Jacobi Decomposition Theorem

Date: 2026-06-07

## Status

This is the current sharpest theorem target for the fixed-frequency
trace-GCD route.  It is a better formulation, not a proof yet.

Confidence status:

```text
finite handoff to verifier: high
support/rank guardrails: high
existence of the CM/Lang decomposition: still highly uncertain
```

So we are closer in the sense that the missing theorem is now narrow and
falsifiable.  We are not close in the sense of having a producer proof in
hand.

## Objects

After the right Gauss transform, the obstruction is the named weighted
relative polynomial

```text
G_chi(X) = sum_r chi^(-1)(r mod 211) F_r(X),
F_r(X) = sum_k j_{r+m*k} X^k,
m = 2 * 157 * 211.
```

The internal tower is

```text
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7.
```

The target after `Tr_{B/C}` is a distribution on the exact quotient

```text
C_7 x C_179.
```

The forbidden bidegrees are

```text
C_7^nontrivial x {C/E trivial}.
```

Their vanishing is equivalent to final internal trace zero in the six
nontrivial right projector channels, which the Lean/Python handoff gates
already connect to the `1092` H-coset verifier.

## Admissible Carries

For `N=7*179`, a Jacobi carry is

```text
theta_{u,v}(t) = [ut]_N + [vt]_N - [(u+v)t]_N.
```

The termwise-safe family is:

```text
u is right-trivial and C/E-nontrivial;
v has nontrivial C/E component;
u+v has nontrivial C/E component.
```

This excludes the pure-right partner and `C/E`-cancelling cases.  Those cases
look superficially close but individually leak in the forbidden bidegrees.

The finite rank evidence is:

```text
admissible C-axis carry rank:       621
broad C-axis carry rank:            625
origin-normalized no-forbidden dim: 1246
```

Thus support vanishing is much weaker than membership in the admissible carry
span.  The older `625` number is a useful warning: it is the rank of a broader
C-axis family that includes four leaky directions.

The Fourier fingerprint of the admissible rank is:

```text
C/E-trivial slice rank:       1
nontrivial C/E slice rank:    7
conjugate C/E-pair rank:      8, not 14
cumulative increments:        1, 7, ..., 7, 4
p24 rank formula:             1 + 7*88 + 4 = 621
```

So the proof should construct compatibility between conjugate `C/E`
characters `b` and `-b`.  Proving only that the forbidden
`C_7^nontrivial x {C/E trivial}` slots vanish is far too weak.

The dual-condition gate makes this compatibility explicit.  In small exact
models, admissible-span membership is equivalent to the following Fourier
conditions for coefficients `F(a,b)` on `C_7 x C_179`:

```text
1. F(a,0)=0 for a=1,...,6;
2. F(a,b)+F(-a,-b)=0 for nontrivial right a and conjugate C/E pairs b;
3. F(0,b)+F(0,-b)=lambda_179*F(0,0) for right-trivial C/E pairs;
4. sum_{b>0}(F(-a,b)-F(a,b))=0 for a=1,2,3.
```

The p24 count is:

```text
6 + 6*89 + 89 + 3 = 632 equations
1253 - 632 = 621 dimensional solution space.
```

Thus the theorem can be targeted either constructively as an admissible
Jacobi-carry decomposition or dually as these four Fourier condition families.
The dual form is currently the more concrete shape for proof search and small
analogue mining.

The Jacobi-carry Fourier formula gate explains why these four families are the
right dual shape for an admissible carry.  For `g_m(t)=[m*t]_N`, with
`d=gcd(m,N)` and `M=N/d`, the nonzero supported Fourier coefficients are:

```text
hat g_m(k) = -d^2*M/(1-zeta_M^(-k/d*(m/d)^(-1))).
```

Consequences for an admissible C-axis carry:

```text
F(a,0)=0                     from C/E-centering of the carry;
F(a,b)+F(-a,-b)=0            from cancellation of hat g_m(k)+hat g_m(-k);
lambda_c=-2/(c-1)            so lambda_179=-1/89 for p24;
global balances              from vanishing on the C-zero fiber.
```

So the constructive theorem target is now very concrete:

```text
construct the selected weighted packet after Tr_{B/C} as a p-integral
combination of admissible C-axis Jacobi carries, or prove that it satisfies
the same sawtooth identities directly.
```

The value-side equivalent of the dual Fourier system is even more packet
facing.  For the post-`Tr_{B/C}` packet `f(r,c)` on `C_7 x C_179`, prove:

```text
1. sum_c f(r,c) is independent of r;
2. f(r,0)=0 for all r;
3. f(r,c)+f(-r,-c) is one constant for all c != 0.
```

These three identities are equivalent to the `632` Fourier equations with
`lambda_179=-1/89`, hence to rank-`621` admissible-span membership.

The strength accounting refines this again.  The last two identities,

```text
f(r,0)=0,
f(r,c)+f(-r,-c)=constant for c != 0,
```

have p24 rank `629`; adding the row-sum condition contributes only three
independent equations.  So a plausible proof can split as:

```text
1. prove the structural symmetry by a product formula, involution, or
   admissible-carry construction;
2. prove three global balance equations, possibly via the right-difference
   telescope or a residue/product formula.
```

This is now the most economical theorem shape for direct proof work.

In terms of a raw packet `g` and selected defect `f(r,c)=g(r,c)-g(r,0)`, this
becomes a concrete producer theorem:

```text
g(r,0)+g(-r,0)=A_0,
g(r,c)+g(-r,-c)=A_1 for c != 0,
sum_c g(r,c)-179*g(r,0) is independent of r.
```

The first two equations are a two-level complement/product-formula law; the
third is the selected affine row balance.  Together they are equivalent to
the three value-side identities for `f`.

In multiplicative form, for a torus or modular-unit packet
`U(r,c)=omega^g(r,c)`, the same theorem is:

```text
U(r,0)U(-r,0)=alpha_0,
U(r,c)U(-r,-c)=alpha_1 for c != 0,
prod_c U(r,c)/U(r,0)^179 = beta.
```

This is the preferred product-formula target for the actual CM/Lang producer.

## Theorem Target

For each nontrivial right quotient character `chi`, prove that the actual
selected trace-GCD obstruction satisfies

```text
Tr_{B/C}(Pi_chi G_chi) lies in the admissible C-axis Jacobi-carry span.
```

Equivalently, construct p-integral coefficients `lambda_{u,v,chi}` such that

```text
Tr_{B/C}(Pi_chi G_chi)
  = sum_{admissible (u,v)} lambda_{u,v,chi} theta_{u,v}
```

in the quotient divisor/module seen by `C_7 x C_179`.

This would imply:

```text
no forbidden C_7^nontrivial x {C/E trivial} bidegrees
=> final internal trace zero in all six right projectors
=> matching right coboundary
=> product coboundary
=> six nontrivial character payloads vanish
=> ordinary centering + six characters gives 156*7 = 1092 verifier equations.
```

The alternative valid theorem is broader but messier:

```text
Tr_{B/C}(Pi_chi G_chi) lies in the broad rank-625 C-axis span
and the four leaky directions cancel.
```

The rank-621 admissible theorem should be preferred unless the arithmetic
naturally produces the four leak-cancellation equations.

## Why This Is Not Yet Success

The following shortcuts have already failed or been demoted:

```text
plain cyclic Stickelberger;
plain right-axis Stickelberger;
generic Jacobi carries;
pure-right Jacobi partners;
C/E-cancelled Jacobi sums;
projector nontriviality alone;
generic actual-CM two-axis packets;
right-combo/product packet shape without the selected trace-GCD weights;
trace-defect anchor zero as a substitute for C/E-centering.
```

The latest actual-CM admissible-span boundary strengthens this warning:

```text
raw D=-5000 projector row:
  admissible-span origins = 0/30
  broad-span origins      = 0/30

pinned D=-13319 right-combo row:
  right-combo resolvents:
    admissible-span origins = 0/140
    broad-span origins      = 0/140

  raw weighted coefficients:
    admissible-span origins = 0/140
    broad-span origins      = 0/140

  selected-child defects c_k-c_0:
    admissible-span origins = 0/140
    broad-span origins      = 0/140
```

So admissible Jacobi decomposition is not generic embedded-CM geometry or
generic right-combo/coefficient packet structure.

The remaining theorem must use the specific selected weighted CM/Lang packet.
That is why the route is promising but still highly uncertain.

## Lean Use

Lean should now be used more heavily for the proof scaffold:

```text
admissible decomposition => no forbidden bidegrees;
no forbidden bidegrees <=> final internal trace zero;
final internal trace zero => product-coboundary handoff;
ordinary centering + six characters => 1092 H-coset verifier;
payload/count inequalities.
```

Lean should not be expected to discover the CM/Lang decomposition.  Its job is
to prevent another hidden-hypothesis mistake like confusing the broad
rank-625 family with the admissible rank-621 family.

## Useful Local Computation

Large local compute is useful while this remains conjectural, but only as a
theorem microscope.

High-value jobs:

```text
1. materialize small two-axis CM analogues where the weighted packet is known,
   then test membership in the admissible carry span and separately in the
   broad span plus leak coordinates;

2. mine any positive small rows for the coefficients lambda_{u,v,chi} and
   look for a recognizable Jacobi/Stickelberger/Lang divisor formula,
   especially a conjugate-C-pair compatibility formula;

3. run long negative-control searches for rows where ordinary CM geometry
   fails the admissible-span test, so we do not overgeneralize;

4. if p24 projections can be computed without enumerating the class set,
   test the 621-dimensional membership directly and inspect the residual;

5. formalize the finite implication chain in Lean while computation searches
   for coefficient patterns.
```

Low-value jobs:

```text
full p24 class-set enumeration;
sqrt-scale seed search;
large jobs that only re-test support vanishing instead of admissible-span
membership.
```

If a materialized weighted packet lands in the admissible span across several
nontrivial small analogues, that would materially raise confidence.  If the
actual p24 projected packet misses the admissible span, this branch should be
demoted immediately unless the residual lies exactly in the four leaky
broad-family directions and those leaks have a separate arithmetic
cancellation.
