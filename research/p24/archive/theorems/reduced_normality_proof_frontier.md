# Reduced Normality Proof Frontier

This note isolates the exact theorem still missing from the additive
projector no-go result.  It also records which nearby facts are too weak.

## Normal determinant formulation

Let `G=<g>` be a cyclic CM class group of order `h`, and write the embedded
ordinary CM roots as

```text
j_i = g^i(j_0),       0 <= i < h.
```

Set

```text
J(T) = sum_i j_i T^i.
```

Over any field of characteristic not dividing `h`, the cyclic translate
matrix

```text
M = (j_{a+b})_{a,b in Z/hZ}
```

has determinant

```text
det(M) = product_chi T_chi,
T_chi = sum_i chi(g)^i j_i.
```

This is the cyclic case of Dedekind's group determinant formula.  Therefore
the reduced CM element is normal modulo the chosen prime above `p` if and only
if

```text
P_p does not divide product_chi T_chi.
```

The dominance proof in `p24/singular_moduli_normality_bound.py` proves
`T_chi != 0` in characteristic zero for the strict p24 CM torsors.  It does
not prove that the same algebraic integer is a `P_p`-adic unit.

## False shortcuts

The following facts do not prove reduced normality.

1. `H_D(X)` splits completely and squarefreely modulo `p`.

   This says the CM roots are distinct, or equivalently that the power-basis
   discriminant

   ```text
   product_{i<j} (j_i - j_j)^2
   ```

   is nonzero modulo `p`.  The normal determinant is a different polynomial in
   the same roots.

2. `j` is a primitive generator of the split etale algebra.

   A vector can separate all primitive idempotents and still have a vanished
   Fourier component.

3. The local normal basis theorem.

   Since the ring class field is unramified at the ordinary split prime, a
   local normal integral basis exists.  This is existential; it does not say
   that the specific singular modulus `j`, or a specific class invariant
   paired to `j`, is normal after reduction.

4. Normal-basis theorems for ray/Siegel singular values.

   Results such as Jung-Koo-Shin's normal bases of ray class fields prove that
   certain Siegel singular values have all conjugates.  That is useful
   class-field generation data, but a normal generator still has to be
   projected by the subgroup idempotent to select an unramified quotient
   layer.  It is not a child selector.

The small script

```text
p24/reduced_normality_false_lemmas_toy.py
```

constructs a split squarefree degree-5 example over `F_11` with distinct
entries but a zero DFT component.

## Universal theorem is false

The stronger hope

```text
every split ordinary CM j-cycle is reduced-normal
```

is false.  I added:

```text
p24/reduced_normality_failure_audit.py
```

and ran:

```text
python3 -m py_compile p24/reduced_normality_failure_audit.py
python3 p24/reduced_normality_failure_audit.py \
  --max-failures 3 --min-h 2 --max-h 12 --max-abs-D 350
```

It found actual small CM failures:

```text
D=-216 q=103 ell=5 h=6 gcd_degree=1 zero_order=3 quotient_failure=3/2/2
D=-300 q=139 ell=7 h=6 gcd_degree=1 zero_order=2 quotient_failure=2/3/1
```

Both are low-order degree-1 packet failures.  They do not resemble the p24
primitive odd `157`/`211` packets, but they prove that splitness,
squarefreeness, and ordinary CM structure cannot imply reduced normality by
themselves.

The follow-up support audit

```text
p24/failure_projector_weight_audit.py
```

shows that these failures still do not lower the additive projector support:

```text
D=-216: best weights 3 and 2 for quotient/subgroup sizes 2/3 and 3/2
D=-300: best weights 3 and 2 for quotient/subgroup sizes 2/3 and 3/2
```

So full reduced normality is sufficient but not necessary.  The sharper
theorem target is the affine-code minimum-weight statement.

The first structured way for the affine-code statement to fail is now
identified more explicitly.  For `h=m n`, a full vanished dual coset
`a+Q_H` is equivalent to fiberwise vanishing of the relative `H`-character
sums

```text
P_u(a) = sum_k zeta_n^(a k) j_{u+m k}.
```

This reduction is in:

```text
p24/harmful_dual_coset_relative_resolvent_lemma.md
```

For the third p24 target, ruling out one `F_p`-stable harmful event means
ruling out a Frobenius orbit of `388430` such relative characters, because
`ord_3107441(p)=388430`.

The exact finite-field certificate version is:

```text
p24/relative_resolvent_content_certificate.md
```

For each of the eight nontrivial `H`-character Frobenius orbits, with minimal
polynomial `f_a`, one must prove that the vector

```text
(J_0 mod f_a, ..., J_{m-1} mod f_a)
```

is nonzero.  A Bezout identity among these components would be an exact
certificate; product nonvanishing is only a stronger sufficient condition.

## What a proof would need

A proof of the p24 reduced normality input must certify

```text
T_chi not == 0 mod P_p
```

for the relevant high-order class characters, preferably for all characters
of the strict CM torsor.  Equivalently, it must prove that the normal
determinant is a unit at the selected split prime.

Known routes do not close this:

```text
height/dominance:
  proves complex nonzero, but the algebraic integer is far larger than p;

Gross-Zagier difference norms:
  control pairwise differences of singular moduli, not the normal determinant;

Bruinier-Funke/Zagier traces:
  handle global/genus-style traces or move the problem to high-level
  non-genus trace coefficients;

abstract class-field/ray generators:
  give split prime torsors without pairing the roots to embedded j-periods;

local normal basis:
  proves some element is normal, not this element.
```

In group-algebra terms, a sparse additive formula can beat the subgroup
projector only through the kernel cut out by vanished reduced resolvents.
The larger toy CM scans in `p24/reduced_resolvent_vanishing_scan.py` found no
such kernel for the tested `h >= 12` rows.  A fresh 20-row scan over
`12 <= h <= 80` again had `normal_rows=20`, `nonnormal_rows=0`, and full
quotient DFT support in all `23` rows where roots of unity were present.  But
the `D=-216` and `D=-300` failures show that a target proof still needs an
actual p24 p-adic nonvanishing certificate or the weaker minimum-weight proof.

The weaker minimum-weight proof is not purely formal either.  The artificial
cyclic-code counterexample

```text
p24/cyclic_code_min_weight_counterexample.py
```

has

```text
q=7, h=6, quotient_size=2, subgroup_size=3,
vanished_nonquotient_characters=[1,4],
projector_weight=3,
best_weight=2.
```

Thus a structured multi-packet annihilator can reduce support even when the
quotient characters themselves do not vanish.  The actual CM failure rows do
not show this behavior, but p24 still needs arithmetic control of the
annihilator, not just a generic cyclic-code lemma.

## Probabilistic sanity check

A random-vector model predicts reduced normality overwhelmingly often.  For a
fixed character packet over `F_{p^d}`, the chance of a zero packet is about
`p^{-d}`; the crude algebraic-closure union bound is at most `h/p`.

For the strict p24 class sizes this is around

```text
first trace:   2.787337e-13
third trace:   2.058804e-13
```

This explains why the toy scans are all normal and why a p-specific collapse
would be surprising.  It is not a certificate.

## Current theorem boundary

The negative theorem can now be stated without ambiguity:

```text
If reduced normality holds at the selected p24 prime, every additive
equivariant Hecke/projector formula producing the H-period has support at
least |H|.
```

The missing theorem is exactly the p-adic unit statement for the normal
determinant, or the direct cyclic-code minimum-weight substitute:

```text
min_{B in Ann(J)} wt(e_H + B) = |H|.
```

The quotient-spectrum refinement in

```text
p24/quotient_spectrum_support_theorem.md
p24/p24_frobenius_packet_map.py
```

shows that quotient-character nonvanishing is enough only for formulas already
known to factor through `G/H`.  For the third trace this quotient statement
has `28` Frobenius packets.  Full class-cycle normality has `10156` packets,
and arbitrary sparse Hecke-word sums still require full reduced normality or
the minimum-weight statement.  Proving the p24 case therefore seems to require
either:

```text
1. a new explicit formula for high-order non-genus class-character resolvents
   modulo this split prime; or
2. a structural p-adic nonvanishing theorem for singular-modulus normal
   determinants with hypotheses strong enough to exclude the small low-order
   failures; or
3. a direct cyclic-code proof that e_H + Ann(J) has no representative of
   support below |H| for the selected p24 torsor, using arithmetic properties
   of the CM annihilator rather than a universal coding theorem.
```

Either would be new enough to materially change the p24 search.  The existing
finite-field degree theorem and prime-torsor theorem rule out the easier
bounded/local/abstract-tower substitutes.
