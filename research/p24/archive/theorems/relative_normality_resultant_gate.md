# Relative Normality Resultant Gate

This note isolates the finite algebra behind the prime relative-normality
candidate.

## Fiber Resultant

For `h=m*n`, define

```text
J_u(X) = sum_{k=0}^{n-1} j_{u+m*k} X^k.
```

For a primitive relative character `a`, the coordinate is

```text
P_u(a) = J_u(zeta_n^a).
```

Therefore

```text
Res(Phi_n(X), J_u(X)) = product_{a in (Z/nZ)^*} J_u(zeta_n^a)
```

up to the usual leading-coefficient sign, which is `1` here because
`Phi_n` is monic.

Thus:

```text
Res(Phi_n, J_u) != 0 mod p
  => J_u(zeta_n^a) != 0 for every primitive relative character a
  => the u-th coordinate never vanishes in any primitive Frobenius packet.
```

If this holds for every quotient coordinate `u`, the stronger product
certificate holds and no harmful all-zero packet can occur.

## Prime `n`

For p24,

```text
n = 3107441
```

is prime.  Hence every nontrivial relative character is primitive.  The single
resultant condition

```text
Res(Phi_n, J_u) is a p-unit
```

for each `u` covers all nontrivial relative packets.

This is stronger than the exact content certificate

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1,
```

but it is clean:

```text
for every u and every packet factor f_a | Phi_n:
  J_u mod f_a is nonzero.
```

It is not the same as full cyclic normality of the fiber.  The full circulant
determinant also contains the trivial period:

```text
det(circ(j_{u+m*k})) = J_u(1) * Res(Phi_n, J_u).
```

Toy data shows that `J_u(1)` can vanish even for prime `n`, while the
primitive resultant remains nonzero.  The correct object is therefore the
augmentation determinant, not the full circulant determinant.  See:

```text
p24/relative_augmentation_normality.md
p24/relative_circulant_rank_scan.py
```

## What Lean Checks

The finite implication is in:

```text
p24/lean/RelativeNormalityGate.lean
```

It abstracts the p24 arithmetic as a family of determinants `determinant u`.
The checked theorem says:

```text
(packet u = 0 => determinant u = 0)
and determinant u != 0 for every u
  => the packet is not all zero.
```

The unproved arithmetic input is the selected-prime p-unit theorem for the
actual CM resultants.

The finite-field zero lemma does not supply this input.  A single coordinate
zero gives only `n` zeros along the recovery orbit, while the natural
relative trace has pole degree at least `n`.  The zero lemma would need a
correspondence pole factor `< 1`.  See:

```text
p24/augmentation_zero_lemma_boundary.md
```

The selected-prime scan is now recorded in:

```text
p24/relative_resultant_selected_prime_scan.py
p24/relative_resultant_selected_prime_scan.md
```

The first bounded multi-splitting run found no coordinate-resultant failures:

```text
packet_rows=361
prime_packet_rows=204
composite_packet_rows=157
coord_zero_packets=0
expected_prime_coord_zero_packets_random=0.517802
expected_composite_coord_zero_packets_random=0.274960
```

The origin-rotation correction is recorded in:

```text
p24/relative_origin_shift_invariance.md
p24/principal_fiber_punit_boundary.md
```

Rotating the class-cycle origin only permutes relative fibers and multiplies
them by powers of `X`, so origin shifts are consistency checks rather than
independent coordinate-zero tests.  The pinned composite `D=-1336, n=6`
control still gives coordinate-zero failures on every selected origin, while
exact content stays nonzero.

That early prime-`n` evidence was later superseded by a wider selected-prime
scan:

```text
p24/prime_relative_normality_counterexample.md

D=-956 q=3307 ell=5 h=15 m=5 n=3 deg=1
coord_zero=1 content_zero=0 hermitian_zero=0
```

Thus the broad prime-relative-normality statement is false, although the
p24-specific resultant statement remains a valid sufficient target.

The principal-fiber note explains the conceptual version: the all-coordinate
resultant theorem is equivalent to proving that the principal relative fiber
`P_0(a)` is a p-unit at every split prime above `p`.  This is the coordinate
where characteristic-zero dominance applies.

The packet-factor zero condition itself is clarified in:

```text
p24/relative_packet_factor_vanishing_shape.md
p24/relative_packet_factor_shape_scan.py
```

For a single factor `f_a | Phi_n`, `J_u mod f_a = 0` means the length-`n`
fiber lies in the cyclic code `(f_a)/(X^n-1)`.  It only kills one Frobenius
orbit of primitive characters.  It does not imply `J_u mod Phi_n = 0`, a
constant fiber, a proper period, or a short recurrence.  Actual composite CM
coordinate failures have generic-looking full/near-full BM complexity, so the
remaining arithmetic input cannot be replaced by an elementary
low-complexity exclusion.

## Current Proof Gap

Known normal-basis theorems for special class invariants show that some
singular values can be chosen to give normal bases of ray class fields, but
that does not immediately apply to level-1 `j` along the p24 relative
subgroup.

The p24 theorem needed is sharper:

```text
For the selected split prime p=10^24+7 and the third target CM order,
the relative normality resultants Res(Phi_3107441, J_u) are p-units for every
0 <= u < 66254.
```

The new counterexample means this cannot be justified from prime-ness of
`n`; it needs a selected-prime p24 p-unit theorem.

Equivalently, no selected-prime reduction of a prime-length relative CM
fiber has a primitive cyclotomic annihilator.

There are two separable normality statements:

```text
characteristic-zero normality:
  the class-character resolvents are nonzero as algebraic numbers;

selected-prime reduced normality:
  their reductions modulo the chosen prime over p are nonzero.
```

The first is supported by principal singular-modulus dominance and by the
normal-basis discussion in:

```text
p24/period_selector_theorem_status.md
p24/hermitian_principal_dominance_theorem.md
```

The second is not a height corollary.  The singular-modulus heights are many
orders of magnitude above `log(p)`, so a p-divisibility of the resultant need
not lift to a characteristic-zero vanishing.  This is why the remaining
theorem has to be p-adic/modular, not archimedean.

Closest known literature:

```text
Jung-Koo-Shin, Normal bases of ray class fields over imaginary quadratic
fields, arXiv:1007.2312.
Jung-Koo-Shin, Ray class invariants over imaginary quadratic fields,
arXiv:1007.2317.
```

These concern special Siegel-function ray class generators.  They are adjacent
but do not give the selected-prime p-unit statement for level-1 `j` in the
unramified p24 odd class-group layers.
