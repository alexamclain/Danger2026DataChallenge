# p24 Smooth Class-Tower Lead Audit

Date: 2026-06-04 PDT

Scope: the third strict DANGER3 target trace only.

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = 205880396014 = 2 * 157 * 211 * 3107441
Cl(O_K) ~= Z / hZ
```

For this trace the conductor of `Z[pi]` inside `O_K` is `2`, and the
conductor-2 ring-class multiplier is `1`, so the maximal-order and
trace-order class selection problems have the same class group.  The small
split-prime probe finds:

```text
ell = 23     generates the full class group
ell = 2      generates the odd subgroup, index 2
ell = 2897   generates index 157
ell = 14057  generates index 211
ell = 677    generates index 314
ell = 7349   generates index 422
```

This is the friendliest class-group structure found so far.  The question is
whether known polycyclic class polynomial, class invariant, isogeny volcano, or
explicit class-field tower methods can turn it into one CM `j` root modulo
`p` in sub-sqrt work.

## Short Verdict

No known method crosses the strict square-root barrier from this data.

The smooth cyclic class group makes an embedded decomposed CM equation much
smaller in root-finding degree and memory.  It does not, by itself, give the
embedded equation or a distinguished root.  The known methods that really map
back to `j` still construct class-polynomial/class-invariant data by CRT,
complex analytic, p-adic, or class-orbit enumeration work at about the
`sqrt(|D_K|)` scale or worse.  The known methods that cheaply produce abstract
class-field equations do not include a map from their generator to the CM
`j`-invariant.

Equivalently:

```text
abstract class field equation != embedded class invariant with j recovery
```

The smooth class group is a useful implementation fact after a root/embedded
invariant is available.  It is not a root selector.

## What Smoothness Buys

Because `h` factors into `2, 157, 211, 3107441`, a decomposed class equation
can use much lower degrees than the full class polynomial degree:

```text
best balanced divisor split:
  h = 66254 * 3107441
  m + n = 3173695

other quotient-friendly splits:
  h = 157 * 1311340102
  h = 211 * 975736474
  h = 314 * 655670051
  h = 422 * 487868237
```

So a tower or Hecke representation could replace a degree-`205880396014`
root-finding operation over `F_p` by smaller root-finding operations.  The
small split prime `23` also makes class-group navigation pleasant once any
target CM vertex is known.

This is real, but it is not enough.  A DANGER3 construction needs one actual
`j in F_p`, then a bounded-degree lift through

```text
j(A) = 256 * (A^2 - 3)^3 / (A^2 - 4).
```

The smooth factors only describe the Galois/class action on the root set.
They do not choose a vertex of that torsor.

## Polycyclic / Decomposed CM Algorithms

The closest known method is Sutherland's decomposed CM method:

```text
https://arxiv.org/abs/1009.1082
```

It explicitly targets this shape: given `D` and a prime `q` that splits
completely in the ring class field, it obtains a root of `H_D mod q` without
necessarily computing the coefficients of `H_D`.  It chooses a subgroup
`G <= Cl(O)`, writes `n = |G|`, `m = h/n`, constructs a degree-`m` polynomial
`V`, and then recovers a `j` root from a degree-`n` specialization `U_y`.
This is an embedded method: the construction is built from actual CM
`j`-roots/class invariants, so the final value really maps back to `j`.

For the third p24 target, the class factorization would make the root-finding
degrees attractive, especially with the `66254 * 3107441` split.  The catch is
the construction of `V` and the `W_k`.  The algorithm still computes them by
CRT over many auxiliary primes.  For each auxiliary prime it finds a seed in
`Ell_O(F_l)` and enumerates the relevant class orbits using the polycyclic
class-group action and modular polynomials.  Smoothness helps the orbit
layout and memory, but the coefficient/CRT height still carries the CM
class-equation cost.

The paper's rigorous headline remains `O(|D| log^{6+eps}|D|)` expected time
with improved space, and its average-case heuristic for the decomposed
root-only algorithms is still `O(|D|^{1/2} log^{2+eps}|D|)`, not
`o(|D|^{1/2})`.  Since `|D_K| ~= 6.5e23`, this sits at the p24 square-root
frontier.  It is a memory/root-degree improvement, not a strict DANGER3
sub-sqrt construction.

The older CRT class-polynomial and class-invariant methods have the same
issue:

```text
https://arxiv.org/abs/0903.2785
https://arxiv.org/abs/0802.0979
https://arxiv.org/abs/1001.3394
```

They compute an embedded class object, but they do so by finding/enumerating
CM roots over auxiliary fields or by another large-discriminant class
polynomial computation.

## Class Invariants

An embedded class invariant would be useful if it supplied:

```text
1. a polynomial H_D[f] or tower layer whose root f0 can be found modulo p,
2. an explicit relation Psi_f(f, j) with small degree in j,
3. enough odd class-field information to isolate one j-root or a tiny fiber.
```

Known Weber, eta-quotient, Ramanujan, and Atkin invariants can greatly reduce
coefficient heights by constants, and sometimes by small genus/ramified
factors.  They also come with a modular relation back to `j`; that is what
makes them embedded invariants rather than abstract class-field generators.

For this exact target, the visible 2-primary structure is exhausted by genus:
`D_K = -599 * 1089874116562502921057`, Redei 4-rank is zero, and genus saves
only one bit.  Fixed-level invariants therefore change constants, not the
odd residual class coordinate of size

```text
h/2 = 102940198007 = 157 * 211 * 3107441.
```

A variable-level invariant tailored to the odd factors would need to provide
the missing embedded odd quotient.  Constructing and proving the map back to
`j` is essentially the decomposed class-invariant problem above.  No standard
invariant family gives a bounded-degree `Psi_f(f,j)` that quotients exactly
these odd factors for free.

## Isogeny Volcano / Small Split-Prime Cycles

The split prime `23` generating the class group is excellent after a seed
root is known: the horizontal `23`-isogeny action walks the whole target
`Ell_O(F_p)` torsor.

It does not produce the first vertex.  A volcano or class-action walk
preserves the trace/isogeny class.  Starting from the cheap `D=-7` curve, or
from a random curve, there is no known low-degree path into this different
ordinary CM isogeny class.  Starting without a vertex and imposing a closed
`23`-cycle just repackages the class equation; eliminating the unknown cycle
or composing the correspondence reintroduces huge degree/height.  Quotient
cycles of lengths `157`, `211`, or `3107441` are useful labels only if an
embedded invariant or seed root tells us which cycle/root is the p24 one.

The 2-isogeny volcano is also not the missing structure.  The target has
conductor depth only `1` from `Z[pi]` to `O_K`; the strict `2^40` requirement
is the X1/ray-orientation tail, not a deep 2-volcano descent.

## Explicit Class-Field Towers

The cyclic factorization suggests an abstract tower such as:

```text
degree 2, then 157, then 211, then 3107441
```

or another ordering of the odd factors.  PARI's class-field routines already
materialize the degree-2 genus layer for this target as the expected genus
field equation, e.g. `x^2 + 599`.  In principle, odd layers of degrees
`157`, `211`, and `3107441` are the right abstract field-theory shape.

The obstruction is embedding.  A `bnrclassfield`-style polynomial defines a
number field isomorphic to a class-field quotient.  It does not by itself
provide a class invariant `f(tau)` or an explicit rational/algebraic relation
that recovers `j(tau)`.  Modulo the p24 prime, Frobenius is trivial in the
target ring class field, so every quotient layer splits completely over
`F_p`.  Choosing compatible roots through the tower is exactly choosing a
prime above `p`, equivalently choosing a class in the CM torsor.

Thus an abstract tower can certify and organize splitting, but it does not
select a `j` root.  To turn it into a DANGER3 construction one would still
need one of:

```text
an explicit embedded generator f(tau) with a small map back to j,
explicit resolvents expressing j in the tower generator,
a seed target CM curve/root,
or a new p24-specific odd Artin/class label that singles out a root.
```

Known explicit class-field machinery does not supply any of these in
sub-sqrt work for this discriminant.  Computing the needed resolvents is the
same embedded class-polynomial/class-invariant computation in different
coordinates.

## What Would Count As A Real Breakthrough

A successful use of the smooth class group would need to output a concrete
object like:

```text
F_1(Y_1), F_2(Y_2, Y_1), F_3(Y_3, Y_2), ...
R(J, Y_r)
```

where the tower has largest relative degree well below `sqrt(p)`, the
polynomials are embedded CM invariants rather than abstract field equations,
and solving the tower modulo `p` leaves only a bounded or genuinely sub-sqrt
number of `j` candidates.  The final relation `R(J,Y_r)` must map back to
the ordinary CM `j` line, and then to Montgomery `A` by the bounded-degree
formula above.

The present data does not provide such an object.  It only says that if such
an embedded odd tower were available, the class group is unusually friendly.

## Bottom Line

The third target remains the best CM/class-field lead, but only as a possible
new-invariant research direction.  Existing polycyclic/decomposed CM methods
are embedded but still pay square-root-scale coefficient/CRT/orbit work.
Known fixed-level class invariants map back to `j` but save only constants.
Isogeny volcanoes and the `23`-cycle navigate the torsor after a seed, not
before.  Abstract class-field towers can expose the smooth quotient structure
but do not map back to `j` or select a root above `p`.

So the smooth-ish class group does not currently recover a strict p24 CM
`j`-root in sub-sqrt work.  It sharpens the remaining loophole to a very
specific missing primitive: an explicit embedded odd class-field tower, with
small recovery map to `j`, for
`D_K = -652834595820939249713143`.
