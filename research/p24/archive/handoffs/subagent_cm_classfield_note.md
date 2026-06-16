# p24 CM/Class-Field Loophole Audit

Date: 2026-06-04 PDT

Scope: focused check of whether the exact strict DANGER3 target
discriminants for

```text
p = 10^24 + 7 = n^2 + 7,  n = 10^12
```

admit a class-invariant, genus/ray quotient, Gross-Zagier-style
factorization, Weber/Atkin factor, or near-square relation that selects one
Montgomery `A` or `j` root in `o(sqrt(p))` work.

## Exact Rows

Signs only swap curve and twist, so the three CM fields are:

```text
t = 1020608380936
  D_K = -739589633190799177940983
  |D_K| = 29 * 25503090799682730273827
  h_est = 2.786879e11
  genus bits = 1

t = -78903246840
  D_K = -998443569409526507503607
  |D_K| = 7 * 211 * 4973929 * 135907507341779
  h_est = 8.329662e11
  genus bits = 3

t = -1178414874616
  D_K = -652834595820939249713143
  |D_K| = 599 * 1089874116562502921057
  h_est = 2.060276e11
  genus bits = 1
```

For all three rows:

```text
t^2 - 4p = 4D_K
D_K == 1 mod 8
conductor of Z[pi] in O_K = 2
h(4D_K) / h(D_K) = 1
Redei 4-rank = 0
```

So the conductor-2 layer is trivial, and the 2-primary class-field structure
stops at genus.  After all genus labels, the residual class count is still
about `1.0e11..1.4e11`.

## Verdict

No exploitable CM/class-field selector is visible.  The crisp obstruction is:

```text
The principal norm equation makes Frobenius at p trivial in the target ring
class field.  Therefore every class-field quotient also sees p as completely
split.  This certifies that the target roots exist in F_p, but it supplies no
distinguished prime/root above p.
```

Equivalently, class invariants and quotient class polynomials can label or
coarsen the CM root set, but any method that outputs one root must still choose
a class in the large odd residual class group.  That is the missing
`~2^36..2^37` coordinate.

The Montgomery map does not change the problem:

```text
j(A) = 256 * (A^2 - 3)^3 / (A^2 - 4)
```

has bounded fibers.  A sub-sqrt selector for `A` would be a sub-sqrt selector
for a target CM `j` root up to constant ambiguity.

## Candidate Loopholes

### Class Invariants

Weber, eta, Atkin, and other class invariants can reduce coefficient height
and sometimes quotient by a small explicit class action.  For fixed-level
invariants this changes constants only.  For the exact p24 rows, all
2-primary quotienting is already accounted for by genus and Redei; it leaves
about `1e11` roots per residual bucket.

A variable-level or large odd quotient would have to do one of two things:

```text
compute/evaluate a large odd quotient class field, or
recover j from a large fiber of class translates.
```

The first is the ordinary large-discriminant class-invariant problem; the
second is class selection in another coordinate.  No exact p24 discriminant
factor gives a cheap odd quotient with a canonical root.

### Genus and Ramified Factors

The visible factors `29`, `-7`, `-211`, `4973929`, and `-599` are useful only
as genus data.  The middle row's `-7` factor is the tempting one because
`p = n^2 + 7`, but it is still just one prime-discriminant component of the
genus field.  Imposing all available genus characters saves `1`, `3`, and `1`
bits, not a root.

### Ray Quotients

At the CM-order level, conductor `2` adds no kernel.  Deeper 2-power ray data
is exactly the DANGER3/X1 orientation tail: it names a Frobenius-fixed
`2^40` direction.  Passing through `X0` forgets this orientation; restoring it
has degree growing like `2^40`, i.e. sqrt-scale for p24.

### Gross-Zagier Style Factorization

Gross-Zagier/resultant formulas give norms or product factorizations over
pairs of CM classes.  They can explain why a prime divides a class-polynomial
value or an intersection product, but they do not identify which target root
is the reduction.

For the special `D=-7` curve, `j=-3375` is genuinely selected by
`p=n^2+7`, but its trace is `+/-2n` and both curve/twist have only `v2=3`.
It cannot also be a target `D_K` root: the reduction is ordinary, and an
ordinary curve cannot have endomorphism algebra containing two distinct
imaginary quadratic fields.  The three strict target fields are all distinct
from `Q(sqrt(-7))`.

### Weber/Atkin Class Polynomial Factors

Any factorization arising from the known small-level Weber/Atkin functions is
another class-field quotient.  Since `p` is principal, these factors split over
`F_p` rather than isolating a canonical linear factor.  Factoring by genus
leaves the same `~1e11` residual classes; factoring by a new odd quotient would
be the missing odd class selector, not a consequence of the exact p24
discriminants.

## Only Remaining Shape

A real route would need a new p24-specific odd-part class label: a bounded or
sub-sqrt computation that names one class in the residual principal genus and
then converts it through the bounded-degree `j -> A` map.  I do not see such a
label in the exact discriminant factorizations, conductor-2 structure,
near-square radical, known Weber/Atkin invariants, ray quotients, or
Gross-Zagier-style norm factorizations.

Bottom line: these CM/class-field mechanisms certify complete splitting and
give constant-bit labels, but they do not break the class-group symmetry needed
to choose one strict p24 Montgomery root in `o(sqrt(p))` work.
