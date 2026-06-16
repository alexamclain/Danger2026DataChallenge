# Quotient-Spectrum Support Refinement

This note sharpens the reduced-normality requirement in the additive selector
barrier, but also records the trap in the tempting shortcut.  Full reduced
normality of the whole `j`-cycle is stronger than needed for some restricted
operator classes.  However, quotient-character nonvanishing alone is not
enough for arbitrary sparse group-algebra operators.

## Setup

Let

```text
G = <g> ~= Z/hZ,       h = m n,
H = <g^m>,             |H| = n,     |G/H| = m.
```

Write the reduced embedded CM vector as

```text
J(T) = sum_{a=0}^{h-1} j_a T^a in F_p[T]/(T^h - 1),
j_a = g^a(j_0).
```

The subgroup projector is

```text
e_H(T) = sum_{k=0}^{n-1} T^{m k}.
```

Let `zeta` be a primitive `h`-th root of unity in a splitting extension.  The
characters trivial on `H` are exactly

```text
Q_H = {s mod h : n divides s},
|Q_H| = m.
```

For `s in Q_H`,

```text
e_H(zeta^s) = n,
```

and for `s notin Q_H`, `e_H(zeta^s)=0`.

## Restricted Theorem

Let `A` be any additive oriented correspondence formula whose restriction to
the CM torsor is a group-algebra element

```text
A(T) in F_p[T]/(T^h - 1).
```

Assume:

```text
1. A produces the H-period on every translate:

      A * J = e_H * J.

2. A already factors through the quotient G/H, equivalently its coefficient
   vector is H-invariant, equivalently its Fourier transform is supported on
   Q_H.
```

If the quotient-spectrum nonvanishing condition holds,

```text
J(zeta^s) != 0        for every s in Q_H,
```

then

```text
A = e_H.
```

Thus any exact quotient-factored additive selector has support exactly

```text
|H| = n.
```

## Proof

Taking the Fourier transform of

```text
A * J = e_H * J
```

gives, for every character `s`,

```text
A(zeta^s) J(zeta^s) = e_H(zeta^s) J(zeta^s).
```

On the quotient spectrum `Q_H`, the nonvanishing hypothesis lets us cancel
`J(zeta^s)`, so

```text
A(zeta^s) = e_H(zeta^s) = n.
```

Both `A` and `e_H` have Fourier support contained in `Q_H`, so their Fourier
transforms agree everywhere.  Hence `A=e_H`.

This is useful when the proposed construction is already a quotient-level
object.  It is not enough for arbitrary sparse Hecke-word sums.

## Failed Temptation

One might hope that the same conclusion follows from quotient nonvanishing
alone, because it forces

```text
A(zeta^s) = n         for s in Q_H.
```

But this gives only `m` forced Fourier values.  The remaining non-quotient
Fourier values can be arbitrary on character packets where `J(zeta^s)=0`, and
those free values can change the coefficient support of `A`.

A simple algebra model shows the issue.  If `J` is constant on `H`-cosets,
then its Fourier support is contained in `Q_H`, and quotient nonvanishing can
hold.  The one-term operator

```text
A(T) = n
```

satisfies `A*J=e_H*J`, since it agrees with `e_H` on `Q_H`; but its support is
`1`, not `n`.  Such a `J` is not a distinct CM torsor, but it proves that
quotient nonvanishing by itself cannot be the theorem.

The exact arbitrary-operator statement is therefore coding-theoretic:

```text
exact selectors = e_H + Ann(J),
minimum support = min_{B in Ann(J)} wt(e_H + B).
```

Full reduced normality is the clean sufficient condition because
`Ann(J)=0`.  Without it, the needed theorem is the minimum-weight assertion
itself, not merely quotient packet nonvanishing.

## Cyclic-Code Form

For cyclic `G`, put

```text
F(T) = T^h - 1,
D(T) = gcd(J(T), F(T)).
```

Since `p` does not divide `h`, `F` is squarefree and

```text
Ann(J) = (F/D) in F_p[T]/(F).
```

An arbitrary additive selector beats the projector if and only if the affine
cyclic-code coset

```text
e_H + (F/D)
```

contains a word of Hamming weight below `n`.

This is the exact finite-field version of the missing theorem.

## Why This Matters

```text
old sufficient input:
  full reduced normality, D=1;

restricted improvement:
  quotient nonvanishing is enough for operators known to factor through G/H;

exact arbitrary-operator input:
  the coset e_H + Ann(J) has minimum weight n.
```

For the third p24 target, the quotient has

```text
m = 66254 = 2 * 157 * 211.
```

Over `F_p`, Frobenius groups these into just `28` packet residues:

```text
degree 1:      2 factors
degree 35:    12 factors
degree 156:    2 factors
degree 5460:  12 factors
```

The full third-trace class cycle is much larger.  The reproducible packet map
is:

```text
p24/p24_frobenius_packet_map.py
```

It reports:

```text
quotient_m packet_count = 28
subgroup_n packet_count = 9
class_h packet_count = 10156
```

So quotient-factored period normality is a 28-packet statement, while full
reduced normality for arbitrary additive selectors is a 10156-packet
annihilator statement.

So the exact missing nonvanishing input for the additive `H`-period lower
bound can sometimes be checked at the quotient level:

```text
Y(T) = sum_{r=0}^{m-1} y_r T^r,    y_r = sum_{h in H} j_{r+h},
gcd(Y(T), T^m - 1) = 1 over F_p.
```

But that only certifies the quotient-period vector once `Y` is known.  It
does not by itself prove that no sparse representative of `e_H + Ann(J)`
exists.

The cyclic-code formulation is the one already used in

```text
p24/frobenius_packet_testing_barrier.md
p24/cyclic_code_projector_weight_scan.py
```

and avoids hiding any finite-field Fourier subtlety.

## Toy Check

I added:

```text
p24/quotient_spectrum_support_toy.py
```

and ran:

```text
python3 -m py_compile p24/quotient_spectrum_support_toy.py
python3 p24/quotient_spectrum_support_toy.py \
  --max-h 18 --max-q 120 --max-q-degree2 47
python3 p24/quotient_spectrum_support_toy.py \
  --max-h 30 --max-q 300 --max-q-degree2 47
```

It inserts artificial degree-1 or degree-2 annihilator factors into small
cyclic Fourier rings and brute-forces the best representative of
`e_H + Ann`.  In this window:

```text
rows = 283
nonquotient_factor_rows = 196
nonquotient_reduced_rows = 0
quotient_factor_rows = 87
quotient_reduced_rows = 0
```

The larger run reported:

```text
rows = 1016
nonquotient_factor_rows = 750
nonquotient_reduced_rows = 0
quotient_factor_rows = 266
quotient_reduced_rows = 0
```

An additional bounded run expanded this to:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/quotient_spectrum_support_toy.py \
  --max-h 36 --max-q 500 --max-q-degree2 101
```

with output:

```text
rows = 1600
nonquotient_factor_rows = 1205
nonquotient_reduced_rows = 0
quotient_factor_rows = 395
quotient_reduced_rows = 0
```

So the small algebra models did not find a packet-kernel support reduction,
even after inserting artificial low-degree annihilators.  This supports the
cyclic-code barrier, but it is not a proof for p24.

The restricted finite logic is now checked in:

```text
p24/lean/QuotientSupport.lean
```

Lean proves the exact support gate used above: if the candidate additive
operator is already supported on the quotient spectrum and quotient-packet
nonvanishing lets us cancel there, then it equals the subgroup projector on
all characters.  A second theorem records the failure mode: equality on the
quotient spectrum alone gives no global equality without the support
hypothesis.

## Actual Failure Rows

The two small CM reduced-normality failures also do not create sparse
projectors.  I added:

```text
p24/failure_projector_weight_audit.py
```

and ran:

```text
python3 -m py_compile p24/failure_projector_weight_audit.py
python3 p24/failure_projector_weight_audit.py
```

For both `D=-216` and `D=-300`, and for every nontrivial quotient of the
`h=6` class cycle, the best word in `e_H + Ann(J)` had the original projector
weight:

```text
D=-216: quotient 2/3 best_weight=3, quotient 3/2 best_weight=2
D=-300: quotient 2/3 best_weight=3, quotient 3/2 best_weight=2
```

Thus reduced normality is not necessary for the additive support barrier.  The
weaker minimum-weight theorem is the sharper target.

## Over-Broad Minimum-Weight Theorem Is False

The minimum-weight theorem also cannot be purely group-theoretic.  I added:

```text
p24/cyclic_code_min_weight_counterexample.py
```

and ran:

```text
python3 -m py_compile p24/cyclic_code_min_weight_counterexample.py
python3 p24/cyclic_code_min_weight_counterexample.py
```

It gives a split cyclic code example:

```text
q=7, h=6, quotient_size=2, subgroup_size=3
quotient_characters=[0,3]
vanished_nonquotient_characters=[1,4]
projector=[1,0,1,0,1,0], projector_weight=3
best_word=[6,0,0,0,4,0], best_weight=2
```

So quotient characters can remain nonzero while a structured pair of
non-quotient vanishings lowers the coset weight.  The p24 theorem cannot be a
generic cyclic-code theorem.  It must use arithmetic information about the
specific CM annihilator, such as p-adic nonvanishing or a proof that the
vanished packet set does not have this cancellation structure.

The bounded scan

```text
p24/cyclic_code_min_weight_scan.py
```

shows the first reductions are explained by complete translates of the dual
quotient subgroup.  This is recorded in:

```text
p24/dual_coset_annihilator_lemma.md
```

For `h=m n`, if the vanished characters contain `a+Q_H`, then the annihilator
contains a codeword supported on `H`, allowing `gcd(a,n)` projector positions
to be cancelled.  Since the third p24 recovery degree `n=3107441` is prime,
one such harmful coset lowers support by only one; a meaningful sparse
selector would require many harmful cosets or stronger annihilator structure.

The dual-coset condition is equivalent to a relative-resolvent condition:

```text
P_u(a) = sum_k zeta_n^(a k) j_{u+m k} = 0      for every quotient fiber u.
```

See:

```text
p24/harmful_dual_coset_relative_resolvent_lemma.md
```

Thus the missing arithmetic theorem can be aimed at fiberwise nonvanishing of
nontrivial relative `H`-character sums, rather than at the stronger global
reduced-normality determinant.

The packetized finite-field form is in:

```text
p24/relative_resolvent_content_certificate.md
```

It replaces one algebraic character `a` by its Frobenius minimal polynomial
`f_a` and asks for the vector `(J_u mod f_a)_u` to be nonzero.  This is the
exact harmful-packet negation over `F_p`.

## p24 Boundary

This refinement does not produce the certificate, but it shrinks the missing
theorem for quotient-factored constructions and makes the general obstruction
more precise:

```text
clean sufficient input:
  every class-character resolvent of the h-cycle is nonzero mod p;

restricted quotient input:
  every quotient-character packet of the m-cycle of H-periods is nonzero;

exact arbitrary additive input:
  e_H + Ann(J) has no representative of support < n,
  and this is not implied by packet location alone.
```

For the third trace this is a `66254`-spectrum statement with `28` Frobenius
packets when the operator has already descended to the quotient.  For general
sparse Hecke/projector formulas, packet language is still only a way to
describe the annihilator; the support lower bound is the minimum-distance
statement above.
