# Fixed-Frequency H-Coset Selector Boundary

Date: 2026-06-06

## Point

The base-field H-coboundary theorem asks each centered mixed-marginal row to
be orthogonal to the seven indicators of:

```text
H = <2^7> <= (Z/211Z)^*,     |H| = 30.
```

This note records the additive Fourier shape of those selectors.

## Result

The seven H-coset indicators have rank `7` on the `210` nonzero right
coordinates.  Ordinary centering contributes only the sum of these seven
rows, so the H-coboundary theorem adds exactly six centered equations.

After adjoining a primitive `211`st root of unity, each nontrivial quotient
character selector has additive DFT:

```text
sum_{s != 0} chi(s) zeta_211^(v*s).
```

For `v != 0` this is a nonzero Gauss sum, and for `v=0` it vanishes.  In the
p24 finite dictionary:

```text
quotient_character_nonzero_additive_supports=[210,210,210,210,210,210]
```

Thus the H-coboundary theorem is a full-support Gaussian-period cancellation
condition.  It is not a sparse right-frequency shortcut, and it is not a
condition living on one or two Frobenius blocks.

## p24 Frobenius

For p24:

```text
p mod 211 = 114 = 2^198,
198 mod 7 = 2.
```

So Frobenius cycles the seven `H`-cosets in one orbit:

```text
p24_h_quotient_frobenius_orbit_length=7.
```

That is compatible with the quotient-character package, but it does not
reduce the theorem to a fixed-coset or sparse-support identity.

## Check

The finite dictionary is checked by:

```text
p24/trace_gcd_fixed_frequency_h_coset_selector_boundary.py
```

It verifies:

```text
h_constraints_extra_rank_over_centering=6
nontrivial quotient characters have full nonzero additive support
h-coboundary is not a sparse right-frequency shortcut
```
