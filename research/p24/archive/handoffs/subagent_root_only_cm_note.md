# p24 Root-Only CM / Prescribed-Order Note

Date: 2026-06-04 PDT

Question: can known root-only CM or prescribed-order algorithms plausibly find
one strict DANGER3 `j`-invariant over the fixed field

```text
p = 10^24 + 7
```

for one of the large target discriminants `|D| ~ p`, in sub-sqrt time, without
computing the full Hilbert/ring class polynomial and without a seed curve in the
target isogeny class?

## Short Verdict

No plausible known route.  The clean obstruction is that the known algorithms
that avoid integer-sized Hilbert class polynomials still need one of:

1. an explicit class polynomial or class invariant modulo the target field,
2. a seed curve/root in `Ell_O(F_p)` plus class-group/isogeny enumeration, or
3. freedom to choose a different field/discriminant pair.

The strict p24 rows give none of these.  The principal norm representation
proves that the CM roots split over `F_p`, but it does not select one root among
the estimated `2e11..8e11` class conjugates, or among roughly `1e11` residual
classes after the genus labels.

## Primary-Source Anchors

Agashe--Lauter--Venkatesan describe the fixed-prime CM step as computing a root
modulo `n` of the Hilbert class polynomial; their CRT improvement computes
`H(X) mod n` directly, avoiding huge integer coefficients, but it is still a
class-polynomial computation, not a root selector.

```text
https://arxiv.org/abs/math/0111159
```

Sutherland's CRT class-polynomial algorithm is more explicit about the root-set
work: compute `H_D mod p` by first finding one `j_1` with `End(E) ~= O`, then
enumerating the other `h(D)` roots via the class-group action.  Its headline
complexity is `O(|D|^(1+o(1)))` time and `O(|D|^(1/2+o(1)) log P)` space under
GRH.

```text
https://arxiv.org/abs/0903.2785
https://eprint.iacr.org/2010/031.pdf
```

Belding--Broeker--Enge--Lauter similarly analyze p-adic and CRT algorithms for
computing `H_D`; the improved CRT method uses class-group action on CM curves,
but all known `H_D` methods have comparable large-`D` running time.

```text
https://arxiv.org/abs/0802.0979
```

Broeker--Stevenhagen's prescribed-order algorithms are fast because the field is
part of the output.  On input an order `N`, they search for a suitable finite
field and small/useful CM discriminant.  This does not transfer to fixed p24:
once `p` and the required order are fixed, the trace and discriminant are fixed.

```text
https://arxiv.org/abs/math/0511729
https://arxiv.org/abs/0712.2022
```

Sutherland's prescribed-torsion and Shparlinski--Sutherland prescribed-subgroup
work does construct curves over fixed `F_p` with subgroup constraints, but the
published bounds are not p24-helpful for exact DANGER3: the `X_1(N)` torsion
method searches modular-curve points, and the fixed-field subgroup algorithm has
running time `m p^(1/2+o(1))` for subgroup size `m`.

```text
https://arxiv.org/abs/0811.0296
https://arxiv.org/abs/1403.7887
```

Recent work on `F_p`-roots of Hilbert class polynomials is also orthogonal here:
it treats inert primes and counts/structures the `F_p` roots via 2-torsion when
nonempty.  The p24 target is the split/principal CM situation where all target
roots lie in `F_p`; the problem is selection inside a huge split root set.

```text
https://arxiv.org/abs/2202.04317
```

## Candidate Routes Checked

### 1. Root of `H_D` without full integer `H_D`

CRT/p-adic/class-invariant methods can avoid building the enormous integer
polynomial, or can reduce coefficient heights by constants.  They do not avoid
the target-root information.  For p24 the degree is `h(D) ~ sqrt(|D|) ~ sqrt(p)`,
so even an explicit split polynomial modulo `p` has sqrt-scale degree/output.

Sutherland's CRT workflow makes the dependence concrete: the method needs one
seed root `j_1`, then uses the class group to enumerate the rest.  If we already
had the seed root over the p24 field, the DANGER3 construction would essentially
be solved up to the bounded-degree Montgomery lift and twist choice.

### 2. Principal representation as a root selector

For each strict trace, `t^2 - 4p = 4D_K` with conductor `2` in `Z[pi]`.  This
is exactly the CM splitting condition.  It says the prime above `p` is
principal and the relevant class polynomial splits over `F_p`.

But trivial Artin symbol fixes every CM conjugate over `F_p`; it does not name a
preferred ideal class.  Genus/Redei data add only constant labels, and the local
audits already leave about `1e11` residual classes per relevant genus.

### 3. Prescribed order over fixed `p`

Variable-field prescribed-order algorithms do not apply because their freedom is
spent choosing `p` and a favorable `D`.  At p24, the strict verifier fixes

```text
N = p + 1 - t
D = t^2 - 4p
```

so the prescribed-order problem collapses back to large-discriminant CM over a
fixed prime field.  The local conductor/fundamental-discriminant audit gives
`|D_K|/p` around `0.65`, `0.74`, and `1.00`, not a small-CM instance.

### 4. Fixed-field prescribed subgroup / torsion

The strict condition is stronger than "some large 2-power divides the order":
the verifier needs a Montgomery curve and exact x-only order `2^40`.  Fixed
`X_1(2^a)` construction has growing modular level; the known fixed-field
subgroup bound is at least sqrt-scale in `p` and linear in the requested
subgroup size.  Local `X0/X1` audits already identify the missing data as the
2-adic orientation tail, not a cheap trace residue.

### 5. Decomposed class polynomials / genus fields

For the p24 target discriminants the conductor-2 kernel is trivial and Redei
4-rank is zero.  The only visible class-field decomposition is genus, worth
`1, 3, 1` bits.  Since the full polynomial is already split modulo `p`, genus
factorization over `F_p` is just labeling subsets of roots that are already
linear; it does not produce a canonical linear factor.

Any further selector must live in the large odd part of the class group.  Known
CM algorithms can navigate that group after a seed root, or encode it into a
class invariant/polynomial, but they do not name one class for free.

## Crisp No-Go Statement

A sub-sqrt root-only p24 method would have to output a bounded-degree datum
leading to one `j in Ell_O(F_p)` for one fixed large discriminant
`|D| ~= p`, without:

```text
enumerating/searching random curves in the target trace bucket,
constructing a degree-h(D) class polynomial/invariant modulo p,
walking a class-group orbit from a known seed root,
or using freedom to choose a smaller discriminant/another field.
```

The known algorithms do not supply such a datum.  They either compute the class
object, assume/find a seed root, or move to a friendlier field.  The p24 local
facts remove the usual escape hatches: conductor-2 adds no class-kernel, genus
and Redei save only constants, and bounded-degree Montgomery/J maps cannot hide
sqrt-scale class selection.

Bottom line: root-only CM is not a plausible strict DANGER3 route for p24 unless
one introduces a new odd-part class selector.  Existing root-only and
prescribed-order literature gives strong evidence for a no-go rather than a
candidate construction.
