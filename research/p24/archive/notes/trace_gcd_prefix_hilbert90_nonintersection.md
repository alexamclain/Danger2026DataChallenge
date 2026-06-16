# Trace-GCD Prefix Hilbert-90 Nonintersection

Date: 2026-06-06

## Point

The four-prefix adjoint theorem can be stated as an additive Hilbert-90
nonintersection.  This is more arithmetic than a raw rank statement, because
it asks whether a class-field period span contains a relative trace
coboundary.

Keep the p24 notation:

```text
L = F_p(mu_157),        [L:F_p] = 156
R = F_p(mu_211),        [R:F_p] = 35
E = L R,
B = {O2,O3,O5,O6},
S_j = H_{157,211}(1,v_j) in E.
```

Let:

```text
phi_B : R^4 -> E
(y_j) |-> sum_{j in B} y_j*S_j,

M_B = image(phi_B) = span_R{S_j : j in B}.
```

The prefix adjoint map is:

```text
A_B^* = Tr_{E/L} o phi_B : R^4 -> L.
```

Therefore:

```text
A_B^* injective
  <=>
phi_B is injective and M_B cap ker(Tr_{E/L}) = {0}.
```

The first clause says the four selected periods are `R`-independent.  The
second clause is the trace-kernel nonintersection.

## Additive Hilbert 90

Let `tau_R` be the generator of `Gal(E/L)`, i.e. the Frobenius power that
fixes `L` and acts as `x |-> x^p` on `R`.  In finite-field notation:

```text
tau_R(x) = x^(p^e),
e == 0 mod 156,
e == 1 mod 35.
```

For a finite cyclic extension, additive Hilbert 90 gives:

```text
ker(Tr_{E/L}) = (tau_R - 1)E.
```

So the prefix theorem is equivalently:

```text
phi_B is injective, and
span_R{S_2,S_3,S_5,S_6} cap (tau_R - 1)E = {0}.
```

Even more compactly, the quotient map

```text
bar_phi_B : R^4 -> E/(tau_R - 1)E
(y_j) |-> [sum_{j in B} y_j*S_j]
```

is injective.  This quotient formulation is the safest theorem statement:
it includes both the `R`-independence of the four periods and the
nonintersection with the trace-kernel coboundary space.

Or, in explicit coboundary form:

```text
sum_{j in {2,3,5,6}} y_j*S_j = tau_R(Z) - Z
  with y_j in R, Z in E
  =>
y_2 = y_3 = y_5 = y_6 = 0.
```

This is a useful class-field theorem candidate: no nonzero `R`-linear
combination of the four selected mixed resolvent pairings is an additive
right-cyclotomic coboundary.

## Resolvent Form

The periods are not opaque:

```text
S_j = H_{157,211}(1,v_j) = <A_1,B_{v_j}>.
```

Thus the p24 prefix theorem may be attacked as:

```text
sum_j y_j * <A_1,B_{v_j}> is not a tau_R-coboundary
```

unless all `y_j` vanish.  This is the exact place where a class-field proof
would have to use the embedded CM origin and the selected prime over `p`.

The nearby Frobenius-cocycle warning is:

```text
p24/axis_frobenius_cocycle_boundary.md
```

It says that Frobenius moves the K-character and H-character coordinates
together.  Therefore this quotient theorem should not be attacked as a bare
representation-theory constituent statement; it must control the coupled
period phase.

The relative-resolvent split-algebra language in:

```text
p24/relative_resolvent_split_algebra_theorem.md
```

is adjacent: it records vanishing as an ideal condition in split class-field
components.  The new prefix theorem asks for a stronger mixed-period
coinvariant statement for four selected right orbit resolvents.

The Hilbert-90 form connects to the earlier trace-intersection theorem:

```text
L cap span_R{S_1,...,S_6}^perp = {0}
```

but is tailored to the representative four-prefix map.  The six-orbit
theorem asks for separation of `L` by relative traces; the four-prefix theorem
asks for an `R^4` period span to avoid the relative trace coboundaries.

## Why This Helps

The direct-sum form:

```text
W_j = Tr_{E/L}(R*S_j) subset L
```

is a finite-geometric rank statement.  The Hilbert-90 form turns the same
condition into a coboundary exclusion:

```text
M_B cap (tau_R - 1)E = {0}.
```

That gives a possible route for divisor/local-unit arguments:

```text
if a nonzero prefix combination were a coboundary,
then its class-field divisor / resolvent content / origin covariance would
satisfy a verticality relation that should be impossible at the selected
prime.
```

No such divisor theorem is proved here.  The point is to replace an unnamed
`140 x 140` Plucker pivot with a precise class-field obstruction.

## Toy Gate

The finite equivalences are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_hilbert90_toy.py
```

It verifies in coprime finite extensions that:

```text
ker Tr_{E/L} = image(tau_R - 1),
A_B^* injective
  <=>
R^k -> E is injective and image(R^k) cap image(tau_R - 1)E = {0}.
```

Equivalently, the quotient map `R^k -> E/(tau_R-1)E` is injective.

The toy includes:

```text
forced repeated-period dependence;
forced coboundary intersection;
random good examples with positive residual kernel in L.
```

## Current Missing Theorem

For the actual p24 periods:

```text
sum_{j in {2,3,5,6}} y_j*H_{157,211}(1,v_j) = tau_R(Z)-Z
  =>
y_j = 0 for every j.
```

Equivalently:

```text
R^4 -> E/(tau_R-1)E,
(y_j) -> [sum_j y_j*H_{157,211}(1,v_j)]
```

is injective.

Together with the already isolated tail-on-kernel resultant, this would prove
the representative `140+16` p-unit and feed the existing sub-sqrt certificate
payload.

The p-local Fitting version of the same prefix quotient theorem is recorded
in:

```text
p24/trace_gcd_prefix_coinvariant_fitting_target.md
```

It names the maximal-minor ideal of `R^4 -> E/(tau_R-1)E` as the intrinsic
prefix p-unit object.

The trace-dual normal-basis version is recorded in:

```text
p24/trace_gcd_prefix_normal_basis_coefficients.md
```

There the same quotient injectivity becomes independence of the `140`
left-field coefficients

```text
Tr_{E/L}(alpha_i * H_{157,211}(1,v_j)).
```

This is the most explicit current finite-field identity to target with a
class-field period formula.
