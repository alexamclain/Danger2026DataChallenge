# Fixed-Frequency Order-7 Augmentation Target

Date: 2026-06-06

## Point

The symmetry boundary shows that ordinary right centering and sign symmetry do
not prove the no-fixed-defect relation at the six nontrivial fixed
frequencies.  The sharper target is an order-7 augmentation identity.

Let

```text
R_7 = F_p[y] / (y^7 - 1).
```

Write the six right-orbit sections in Gaussian-coset order as:

```text
T, P_2, P_3, P_4, P_5, P_6,
```

where `T` is the selected tail orbit containing `1 mod 211`, and `P_4` is the
omitted full block containing `-1 mod 211`.

The finite group calculation gives the negation covariance:

```text
P_4(y) = y^(-2) T(y)
```

on the fixed order-7 quotient.

If the actual CM/Lang packet also satisfies the stronger augmentation:

```text
T + P_2 + P_3 + P_4 + P_5 + P_6 = 0
```

in `R_7 tensor L`, then:

```text
(1 + y^(-2)) T = -(P_2 + P_3 + P_5 + P_6).
```

Since `1 + y^(-2)` is a unit in `R_7`, this gives the desired cyclic syzygy
expressing the tail in the four selected prefix sections.

## Why This Is New

Ordinary centering is only the `y=1` part of the augmentation.  It says the
trivial fixed frequency vanishes.  The missing theorem is the six additional
order-7 vanishing statements:

```text
sum_{six right orbits} V_{a,j} = 0,
    a = 5,10,15,20,25,30.
```

The generic right-symmetry model does not imply these statements.  They must
come from the arithmetic CM/Lang construction of the mixed Hermitian packet.

## Coset Dictionary

Let `2` be the primitive root modulo `211`.  For p24:

```text
p = 2^198 mod 211.
```

The six right Frobenius orbits are the cosets of `<p>`, and the Gaussian
representatives can be taken as `2^(35*j)`, `0 <= j < 6`.  After the fixed
frequency order-5 collapse, summing across the six Gaussian labels at a fixed
`s mod 7` is exactly summing over one coset of the order-30 subgroup whose
discrete logarithms are multiples of `7`.

Therefore the order-7 augmentation is equivalently:

```text
all seven coset sums for (Z/211Z)^*/H vanish,
|H| = 30,  (Z/211Z)^*/H ~= C_7.
```

Ordinary centering is only the trivial character of this `C_7` quotient.  The
missing arithmetic theorem is the vanishing of the six nontrivial quotient
characters.

## Character-Projection Form

Let

```text
S_v = sum_s zeta_211^(v*s) G_s,     1 <= v < 211,
```

be the nonzero right DFT periods of the mixed centered-right profile.  The
p24 orbit convention is:

```text
v = 2^(35*label + 198*position) mod 211.
```

For the order-7 character

```text
chi_k(2^e) = zeta_7^(k * 198^(-1) * e),     k = 1,...,6,
```

the orbit-position augmentation is exactly:

```text
A_k = sum_{label,position} zeta_7^(k*position) S_v
    = tau(chi_k) * sum_{s != 0} chi_k(s)^(-1) G_s.
```

The Gauss sum `tau(chi_k)` is nonzero, so the six nontrivial augmentation
conditions are equivalent to:

```text
sum_{s != 0} chi_k(s)^(-1) G_s = 0,     k = 1,...,6.
```

This is the exact missing CM/Lang statement.  It is stronger than ordinary
right centering and is not forced by the generic finite symmetry model.

## Unit-Symmetry Boundary

A stronger multiplier invariance

```text
G_s = G_{eta*s}
```

for a unit `eta` nontrivial on the order-7 quotient would force the
nontrivial quotient-character projections to vanish.  However, this is not a
free class-field or diamond symmetry.  A pinned actual-CM analogue
`D=-13319, q=13463, left=4, right=7` has:

```text
actual_multiplier_invariance_failures=18
actual_projection_nonzero=1
```

So right-unit transport should be used only as p-unit determinant-line
transport, not as literal invariance of the mixed Hermitian profile.

## Check

The finite implication and controls are in:

```text
p24/trace_gcd_fixed_frequency_order7_augmentation_toy.py
p24/trace_gcd_fixed_frequency_order7_coset_dictionary_toy.py
p24/trace_gcd_fixed_frequency_order7_character_projection_toy.py
p24/trace_gcd_fixed_frequency_order7_h_coboundary.md
p24/trace_gcd_fixed_frequency_order7_h_coboundary_toy.py
p24/trace_gcd_fixed_frequency_h_coboundary_basefield_boundary.py
p24/trace_gcd_fixed_frequency_p24_h_coset_sum_verifier.py
p24/trace_gcd_fixed_frequency_h_kernel_inclusion_gate.py
p24/trace_gcd_fixed_frequency_order7_paired_potential_boundary_toy.py
p24/trace_gcd_fixed_frequency_order7_rank_compatibility_toy.py
p24/trace_gcd_fixed_frequency_unit_symmetry_boundary.py
p24/lean/TraceGcdFixedFrequencyOrder7Gate.lean
```

It checks:

```text
order-7 augmentation + P_4=y^(-2)T
  => explicit fixed-frequency syzygy;

ordinary centering only
  => no control of the six nontrivial order-7 frequencies;

augmentation without negation covariance
  => no explicit formula eliminating the omitted block.

order-5 collapsed six-orbit sums
  <=> order-7 quotient coset sums;

ordinary centering
  <=> only the trivial quotient character vanishes.

order-7 augmentation
  <=> six nontrivial right multiplicative-character projections vanish.

order-7 augmentation
  <=> relative trace to `(Z/211Z)^*/<2^7>` vanishes
  <=> there is an additive Hilbert-90 potential
      `G_s = Y_s - Y_{2^7 s}` on `(Z/211Z)^*`.

paired `L`-profile potential is the exact target;
  a full right-resolvent potential before pairing is sufficient but stronger
  than needed.

base-field H-coboundary
  <=> seven Gaussian-period column sums of the centered mixed marginal
      vanish row-wise, i.e. exactly `156*7 = 1092` scalar equations for p24.

base-field H-coboundary
  <=> the 7-dimensional H-coset indicator subspace lies in the right kernel of
      the centered `156 x 210` marginal matrix.

order-7 augmentation adds six independent equations beyond ordinary centering,
  leaves a `203`-dimensional right-frequency subspace, and is compatible with
  a full `156`-rank fixed determinant square.

unit multiplier symmetry
  => augmentation, but is refuted as a generic actual-CM packet symmetry.

Lean handoff:
  order-7 augmentation + P_4=y^(-2)T + denominator unit
  => seven fixed-frequency tail-in-prefix relations;
  those relations + prefix Plucker p-units
  => no fixed defects;
  no fixed defects reduce stable size-16 supports from 1260 to 35.
```

## Next Arithmetic Target

Prove the order-7 augmentation identity intrinsically for the p24 mixed
Hermitian resolvent packet.  The preferred form is the paired H-potential:

```text
G_s = Y_s - Y_{2^7 s},     G_s in L = F_p(mu_157).
```

Equivalently, the six nontrivial characters of `(Z/211Z)^*/H` vanish in the
right-frequency profile, where `H` is the order-30 subgroup with log exponents
divisible by `7`.

In base-field centered-marginal form, prove:

```text
sum_{s in qH} C(r,s) = 0
for every 1 <= r < 157 and every qH in (Z/211Z)^*/H.
```
