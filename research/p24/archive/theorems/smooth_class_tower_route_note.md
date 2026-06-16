# Smooth Odd Class-Tower Route Note

Date: 2026-06-04 PDT

Target:

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h(D_K) = 205880396014 = 2 * 157 * 211 * 3107441
```

## Why This Is A Real Lead

The third strict trace has a much smoother class group than the first two
target traces.  PARI gives:

```text
class_group = cyclic of order 2 * 157 * 211 * 3107441
```

and small split-prime actions are favorable:

```text
norm 23    generates the full class group
norm 2     generates the odd-index-2 subgroup
norm 2897  generates a subgroup of index 157
norm 14057 generates a subgroup of index 211
```

If one had explicit class invariants for a tower with relative degrees
`2,157,211,3107441`, then the largest root-selection step would be about
`3.1e6`, far below `sqrt(p)=1e12` for this fixed target.

## Why This Is Not Yet A Certificate

The exact class group does not name a CM root.  It only describes the Galois
torsor of all target CM roots.  A strict DANGER certificate still needs one
`j`-invariant in `F_p`, then one of its boundedly many Montgomery `A` values,
and finally a projected `x0`.

Known polycyclic class-polynomial / isogeny-volcano methods use small-degree
isogeny actions to enumerate the CM root set efficiently **after a seed curve
with the target endomorphism ring is known**.  In this p24 problem, finding
that seed is exactly the missing target-trace construction.  The fact that
`23` generates the class group means the roots form one low-degree isogeny
cycle; it does not provide a starting vertex on that cycle.

PARI's `bnrclassfield` can construct abstract class-field equations for
quotients.  For this target, the genus quotient appears immediately:

```text
x^2 + 599
```

but this is only the known genus character.  Attempts to materialize the first
odd quotient of degree `157` overflowed a 512 MB PARI stack, and in any case an
abstract relative class-field equation is not enough: the route needs an
embedded class invariant that maps back to the CM `j` root modulo `p`.

## What Would Count As A Breakthrough

A successful strict sub-sqrt construction along this route would need all of:

```text
1. an explicit invariant or tower for a quotient of the ring class field of
   D_K=-652834595820939249713143 with relative degrees bounded by 3107441;
2. a way to evaluate/reduce that tower modulo p and choose compatible roots;
3. an explicit recovery map from the final tower value to a target CM
   j-invariant over F_p;
4. conversion from j to a nonsingular Montgomery A;
5. constant-expected projection to an accepted x0.
```

Items 4 and 5 are already cheap once `j` is known.  Items 1-3 are the open
piece.  Without them, the smooth class group is a promising structural feature
but not a verifier-compatible certificate or proven asymptotic speedup.

## Quotient-Invariant Audit Refresh

The closest known embedded method is Sutherland's decomposed/tower CM
construction: choose `G <= Cl(O)` of size `n`, set `m=h/n`, build a degree-`m`
polynomial for the fixed field and a degree-`n` recovery polynomial for `j`.
For the attractive p24 split

```text
h = 205880396014 = 66254 * 3107441
```

this avoids a full degree-`h` root problem, but it does not avoid the orbit
primitive.  The construction of the embedded quotient requires enumerating
`G`-orbits of CM roots.  If this is done directly modulo the fixed p24 prime,
one needs a seed target CM root to walk the orbit.  If the seed is avoided via
CRT, the known algorithms enumerate CM roots over auxiliary splitting primes
and still pay the large-discriminant class-object cost.

The quotient field exists abstractly, but an arbitrary quotient generator is
not automatically an embedded modular/class invariant with a small recovery
map to `j`.  Known Weber, eta-quotient, Atkin, and generalized class
invariants reduce heights and sometimes special ramified/Atkin-Lehner degrees;
they do not provide an arbitrary fixed field of index `66254` with cheap
`j` recovery.

So the sharpened obstruction is:

```text
abstract quotient class field != orbit-symmetric embedded invariant
```

and for the best visible split the generic recovery degree is `3107441`,
already well above `sqrt(h) ~= 453740` even before the cost of constructing
the quotient object is counted.

## Kummer / Radical Tower Audit

I also checked the more algebraic version of the same hope: because

```text
h = 2 * 157 * 211 * 3107441
```

is smooth, perhaps the ring class field could be descended by radicals.  I
added:

```text
p24/smooth_class_kummer_feasibility_audit.py
```

Verification:

```text
python3 -m py_compile p24/smooth_class_kummer_feasibility_audit.py
python3 p24/smooth_class_kummer_feasibility_audit.py
```

Key output:

```text
ell      divides_p_minus_1  p_mod_ell  ord_p_mod_ell
157      False              21         156
211      False              114        35
3107441  False              2509452    388430
oddpart  False              27978800775 30297540

large_factor_radical_requires_zeta_extension_degree=388430
full_odd_part_zeta_extension_degree=30297540
```

Thus the odd class factors are not Kummer-friendly over `F_p` itself: direct
radical expressions would need the corresponding roots of unity, and the large
factor's root-of-unity extension already has degree `388430`.  More
importantly, a radical tower would still require explicit defining equations
for the embedded class-field subextensions and compatible maps back to `j`.
The smooth abstract class group supplies neither.

This does not rule out a genuinely new explicit class invariant, but it rules
out the naive implication:

```text
smooth cyclic class group => embedded F_p radical descent to one CM root
```
