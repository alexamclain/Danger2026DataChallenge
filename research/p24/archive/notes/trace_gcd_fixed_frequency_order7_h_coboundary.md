# Fixed-Frequency Order-7 H-Coboundary Target

Date: 2026-06-06

## Point

The order-7 augmentation theorem can be phrased as an additive Hilbert-90
identity for the order-30 subgroup of the right multiplicative group.  This is
the most explicit tower-native form of the current no-fixed-defect target.

Let

```text
Gamma = (Z/211Z)^*
g = 2
H = <g^7>,          |H| = 30
Gamma/H ~= C_7
gamma = g^7 = 128 mod 211.
```

For the p24 mixed Hermitian right profile

```text
G_s in L = F_p(mu_157),     s in Gamma,
```

the order-7 augmentation target is:

```text
Tr_H(G)(qH) = sum_{h in H} G_{q h} = 0
for all qH in Gamma/H.
```

This is the same statement as the vanishing of the six nontrivial quotient
characters from `trace_gcd_fixed_frequency_order7_augmentation.md`.

## Additive Hilbert-90 Form

Since `p` does not divide `|H|`, and `H` is cyclic, the finite theorem is:

```text
Tr_H(G) = 0
iff
there exists Y_s in L, s in Gamma, such that
G_s = Y_s - Y_{gamma s}.
```

The forward direction is constructive on each H-orbit: choose one potential
value freely and recover the rest by cumulative sums.  The final cycle
condition is exactly the relative trace-zero equation.  The reverse direction
telescopes.

There is also a fixed group-algebra certificate.  Let `T` be the shift

```text
(T F)_s = F_{gamma s}
```

and let

```text
e_H = (1/30) sum_{i=0}^{29} T^i.
```

Then

```text
U = (1/30) sum_{i=0}^{29} (29-i) T^i
```

satisfies

```text
(1-T) U = 1 - e_H.
```

Thus the next arithmetic proof target is not to search for `Y`.  It is:

```text
prove e_H G = 0.
```

Then the potential is deterministic:

```text
Y = U G,
G_s = Y_s - Y_{128 s}.
```

## Base-Field Marginal Form

Let

```text
C(r,s) = M(r,s) - M(r,0) - M(0,s) + M(0,0),
1 <= r < 157, 1 <= s < 211,
```

be the centered `156 x 210` mixed marginal matrix.  The centered profile is:

```text
G_s = sum_r zeta_157^r C(r,s).
```

The nonzero powers of `zeta_157` form an `F_p`-basis of `L`, so the
H-coboundary theorem is equivalent to the purely base-field identities:

```text
sum_{s in qH} C(r,s) = 0
for every left row r and every qH in Gamma/H.
```

In words: the seven multiplicative Gaussian-period column sums of the
centered mixed marginal vanish row-wise.  This is the cleanest finite-field
identity to prove in the embedded tower.

For p24 this is an explicit small verifier surface:

```text
156 left rows * 7 H-cosets = 1092 scalar equations over F_p.
```

The verifier in
`p24/trace_gcd_fixed_frequency_p24_h_coset_sum_verifier.py` accepts either the
full `156 x 210` centered marginal or the already-compressed `156 x 7` coset
sum matrix.  It does not compute the CM class set; the tower proof must supply
the zero sums.

Equivalently, if `P_H` is the `210 x 7` H-coset indicator matrix, the target is
the right-kernel inclusion:

```text
C P_H = 0.
```

This is compatible with full row rank because `dim(P_H^perp)=203 > 156`, but
full row rank and ordinary centering do not imply it.  A stronger invariance
under right multiplication by `p^156 mod 211` would imply it, since that
multiplier cycles the seven H-cosets; this is only a sufficient symmetry, not
the known CM/Lang theorem.

The H-coset selectors are not sparse in the additive right Fourier coordinate.
After adjoining `mu_211`, each nontrivial quotient-character selector has
nonzero additive Fourier coefficient at every nonzero right frequency.  So a
proof of this row-wise identity must account for full-support Gaussian-period
cancellation across the 211-layer.

## Why This Helps

The character-projection form says what must vanish.  The H-coboundary form
says how a class-field/tower proof might produce the vanishing:

```text
right profile = difference across the H-layer.
```

For the Hermitian resolvent pairing this should be attacked as:

```text
G_s = <A_1, B_s>
directly find Y_s with G_s = Y_s - Y_{128 s}.
```

Finding `Z_s` with `B_s = Z_s - Z_{128s}` before pairing is a sufficient
stronger theorem, but it is not equivalent.  The right-resolvent family can
have H-trace leakage in the kernel of the pairing map while the paired
`L`-profile still has the required potential.  Therefore the exact next target
is the paired `L`-valued potential unless a later CM identity gives the
stronger right-resolvent potential naturally.

That would prove the order-7 augmentation without enumerating the class set.
Combined with the already checked covariance

```text
P_4 = y^(-2) T
```

and the unit `1+y^(-2)` in `F_p[y]/(y^7-1)`, it gives the fixed-frequency
tail-in-prefix syzygy and removes fixed defects from the determinant selector.

## Boundary

Ordinary centering is only the total trace over `Gamma`; it does not imply
relative trace zero over each H-coset.  Unit-2 transport and full row rank also
do not force this condition.  Those boundaries are checked by:

```text
p24/trace_gcd_fixed_frequency_symmetry_boundary.py
p24/trace_gcd_fixed_frequency_order7_character_projection_toy.py
p24/trace_gcd_fixed_frequency_order7_rank_compatibility_toy.py
p24/trace_gcd_fixed_frequency_order7_h_coboundary_toy.py
p24/trace_gcd_fixed_frequency_order7_h_bezout_operator_toy.py
p24/trace_gcd_fixed_frequency_h_coboundary_basefield_boundary.py
p24/trace_gcd_fixed_frequency_p24_h_coset_sum_verifier.py
p24/trace_gcd_fixed_frequency_h_kernel_inclusion_gate.py
p24/trace_gcd_fixed_frequency_h_coset_selector_boundary.py
p24/trace_gcd_fixed_frequency_order7_paired_potential_boundary_toy.py
p24/trace_gcd_fixed_frequency_unit_symmetry_boundary.py
```
