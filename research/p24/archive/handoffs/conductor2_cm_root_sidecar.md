# Conductor-2 CM Root Sidecar for p24

Question: for the strict DANGER3 traces at

```text
p = 10^24 + 7 = n^2 + 7,  n = 10^12,  k = 40,
```

is there a known or plausible shortcut to find one root modulo `p` of the
relevant Hilbert/ring class polynomial, exploiting the near-square form of `p`,
the factorization of the target discriminants, the principal representation, or
genus/class-group structure, without constructing the polynomial or doing a
sqrt-scale random trace search?

## Verdict

No p24-compatible shortcut is visible in the current local evidence.

The target traces are large-discriminant CM classes.  The identity
`p = n^2 + 7` gives one genuine cheap CM curve, but it is the `D = -7` curve
with trace `+/-2n`; for p24 that curve has only `v2(order)=3`, not the required
`40`.  The strict target traces instead have

```text
Delta = t^2 - 4p = 4 D_K,
```

with `D_K` odd fundamental and `|D_K|` comparable to `p`.  Since
`D_K == 1 mod 8`, the prime `2` splits and the conductor-2 ring-class
multiplier is exactly `1`; the conductor-2 order does not create an extra
small kernel or lower-degree class field to exploit.

## Fixed p24 Data

From `p24/prescribed_order_fixed_p_audit.py`,
`p24/cm_class_size_audit.py`, `p24/genus_character_quotient_audit.py`, and
`p24/cm_relation_norm_barrier.py`:

```text
t = 1020608380936
  D_K = -739589633190799177940983
  factor(|D_K|) = 29 * 25503090799682730273827
  conductor in Z[pi] = 2
  h_est = 2.786879e11
  genus bits = 1
  residual classes per genus ~= 1.393439e11
  min non-scalar principal norm = ceil(|D_K|/4) = 184897408297699794485246

t = -78903246840
  D_K = -998443569409526507503607
  factor(|D_K|) = 7 * 211 * 4973929 * 135907507341779
  conductor in Z[pi] = 2
  h_est = 8.329662e11
  genus bits = 3
  residual classes per genus ~= 1.041208e11
  min non-scalar principal norm = ceil(|D_K|/4) = 249610892352381626875902

t = -1178414874616
  D_K = -652834595820939249713143
  factor(|D_K|) = 599 * 1089874116562502921057
  conductor in Z[pi] = 2
  h_est = 2.060276e11
  genus bits = 1
  residual classes per genus ~= 1.030138e11
  min non-scalar principal norm = ceil(|D_K|/4) = 163208648955234812428286
```

The class-size estimates are heuristic Euler-product estimates, not certified
class numbers, but the discriminant/conductor/factorization statements are
exact.  Their scale is the point: the hidden root set is still on the order of
`sqrt(p)`.

## Why the Four Proposed Sources Do Not Select a Root

### (a) The near-square identity `p = n^2 + 7`

This gives the real CM identity in `Q(sqrt(-7))`:

```text
pi = n + sqrt(-7),  Norm(pi) = p,  Trace(pi) = 2n.
```

It would be strict only if one of

```text
2^40 | (n - 1)^2 + 7
2^40 | (n + 1)^2 + 7
```

held.  For `n = 10^12`, both valuations are `3`.  Thus the near-square
identity is a valid theorem-level selector for rare other 2-adic branches, but
not for this p24 prime.

For the strict target fields, the same audit gives conductor `2` and
`|D_K|/p` equal to `0.652835`, `0.739590`, and `0.998444`; these are not small
CM/Jacobi-sum identities in disguise.

### (b) Factorization or near-prime factors of `D_K`

The factorization only gives genus information.  In the middle trace the
visible factors `7`, `211`, and `4973929` look promising, but all genus
characters together save only `3` bits.  The other two traces save only `1`
bit each.

After fixing a genus, the estimated residual class counts remain around
`1e11`.  This can be a useful rejection label, but not a sub-sqrt root
selector.  Class invariants might reduce coefficient height or constants, but
they do not reduce the number of CM conjugates that must be selected.

### (c) The principal representation `t^2 - 4p = 4D_K`

For each strict trace,

```text
alpha = t/2 + sqrt(D_K),  Norm(alpha) = p.
```

This is exactly the CM splitting condition.  It proves that the relevant class
polynomial splits over `F_p`, but it does not choose a root.  In class-field
terms, the prime above `p` is principal, so its Artin symbol is trivial; all
CM roots are fixed over `F_p`.  The representation certifies existence of the
root set, not a distinguished class representative inside it.

Turning "principal form" into an actual `j` value is precisely the CM
evaluation problem: compute a class invariant or class polynomial, or start
from an already known curve in the target isogeny class.  The local audits do
not contain such a seed.

### (d) Class group, genus, and short-cycle structure

The conductor-2 kernel is trivial here:

```text
D_K == 1 mod 8
Kronecker(D_K, 2) = 1
ring_class_multiplier = 2 * (1 - 1/2) = 1
```

So there is no hidden 2-conductor ladder.  The split prime above `2` also does
not give a short horizontal cycle: a non-scalar principal relation of norm `N`
in an imaginary quadratic order must satisfy

```text
4N = x^2 + |D| y^2,  y != 0,
```

so `N >= |D|/4`.  For p24 this lower bound is already larger than
`1.6e23`, and the first possible split-2 principal power is `2^78`, about
`3.02e11 * sqrt(p)`.  This rules out the natural Landen/2-isogeny-cycle route
as a sub-sqrt construction.

Ramified small primes in `D_K`, including `4973929` in the middle target, give
nonprincipal genus data rather than self-loops.  They can identify a genus
class, but not one of the roughly `2^36` to `2^37` classes remaining inside it.

## Relation to Known CM Algorithms

The local prescribed-subgroup reference `p24/prescribed_subgroup.tex` records
the standard CM path:

```text
given p and t, compute H_D, find a root j mod p, and choose the correct twist.
degree(H_D) = h(D)
constructing H_D costs |D|^(1+o(1)) deterministically
deterministically finding one root of an already available split degree-d
polynomial costs ~O_p(d + p^(1/2))
```

Even if one idealizes the root-finding step, an explicit split polynomial of
degree `h(D_K) ~= sqrt(p)` already has sqrt-scale output size.  To beat sqrt,
a method would need to bypass not just coefficient construction but also the
class selection problem.  The four structures above do not supply that missing
selector.

The Montgomery parameter does not change this conclusion:

```text
j(A) = 256 * (A^2 - 3)^3 / (A^2 - 4).
```

The map from `A` to `j` has bounded degree, so a shortcut to a target
Montgomery `A` would also be a bounded-degree shortcut to a target CM root, and
vice versa up to constant ambiguity.

A small verifier toy clarifies which branch the x-only DANGER3 condition can
prefer:

```text
p24/fixed_trace_montgomery_verifier_toy.py
```

For the `p=103`, `t=8`, `D_K=-87` analogue, the fixed-trace roots split into
maximal-order roots `H_{D_K}` and conductor-2 roots `H_{4D_K}`.  The maximal
Montgomery parameters are all split and none pass the x-only verifier; the
conductor-2 parameters are all nonsplit and all verifier-valid:

```text
maximal_trace_A_torsion_shape={'split': 24, 'nonsplit': 0}
maximal_valid_A_count=0
conductor2_trace_A_torsion_shape={'split': 0, 'nonsplit': 12}
conductor2_valid_A_count=12
```

Thus the p24 construction target should not discard conductor-2 roots as
irrelevant extras.  The strict DANGER3 certificate naturally wants a
fixed-trace root with the right nonsplit Montgomery 2-primary structure, and
the Frobenius order already has conductor `2`.  The class-selection difficulty
is unchanged because the p24 conductor-2 multiplier is `1`.

## Falsifiable Test for Future Claims

A future claimed shortcut should pass this small-scale analogue before being
trusted at p24:

1. Take at least 30 small primes `p = n^2 + 7`.
2. For each row, compute the strict DANGER trace representatives and their
   conductor/fundamental-discriminant shapes.
3. Using only the proposed shortcut, output one `j` or Montgomery `A` for a
   conductor-2, large-`D_K` target trace, with no enumeration of the trace
   bucket and no construction of the full class polynomial.
4. Verify by exact point counting or the existing exact Montgomery trace
   convolution that the output lands in the predicted strict trace class.

Passing means the hit rate stays bounded away from random trace density while
the work per row grows sub-sqrt in the verifier level.  Failing modes are clear:
if the output is the `D=-7` trace, it is the wrong p24 branch; if it only fixes
genus characters, the residual hit rate should remain around `1e-11` at p24
scale; if it uses an isogeny cycle, the displayed relation degree should evade
the `|D_K|/4` norm lower bound.

## Bottom Line

The conductor-2 target roots are not made cheap by `p = n^2 + 7`, by the
factorization of `D_K`, by the principal norm representation, or by genus
structure.  Those facts prove that the relevant CM roots exist and give small
constant filters, but they do not select a root.  Any successful p24 shortcut
must introduce a genuinely new class-selector, not just a faster way to state
the usual CM splitting condition.
