# p24 Affine Quotient-Profile Gate

Date: 2026-06-07

## Point

The current `48` scalar target has an equivalent section-profile form that is
cleaner for proof work.

For each nonzero relative `<p>`-coset `D`, let

```text
M_i(D) = sum_{r in right H-coset i} sum_{k in D} j_{r + m*k}
```

where `H=<2^7> subset F_211^*`, and let

```text
b_i = sum_{r in right H-coset i} j_r
```

be the selected-child right profile.  The recombined balance conditions are
equivalent to the existence of offsets `gamma_D`, independent of the right
coset `i`, such that

```text
M_i(D) = |<p>| * b_i + gamma_D
```

for all seven right `H`-cosets and all eight nonzero relative `<p>`-cosets.

For p24,

```text
|<p>| = 388430
right H quotient order = 7
relative quotient order = 8
```

so this is exactly `6 * 8 = 48` nontrivial right-character equations.

## Relation To The Mixed-Spectrum Split

The previous split

```text
42 mixed C_7 x C_8 equations
6 anchor equations
```

is the Fourier decomposition of the same affine profile identity.

The mixed equations say that the nontrivial right-character part of `M_i(D)`
is independent of `D`.  The anchors say that this common nontrivial right
profile is exactly `|<p>|` times the selected-child profile `b_i`.

Thus the proof target can be stated without mentioning all characters:

```text
For every nonzero relative coset D, the quotient trace profile differs from
|<p>| copies of the selected child by a right-axis constant.
```

## Why This Helps

This is the most explicit embedded finite-field identity currently available.
It separates the two missing arithmetic facts:

```text
1. no right/relative interaction in the quotient matrix;
2. the surviving right profile is tied to the selected child section.
```

The actual CM boundary already showed that generic two-axis CM torsors do not
have this property.  A proof must therefore construct the column offsets from
the trace-GCD weighted CM/Lang packet, or produce an equivalent explicit
potential whose right derivative is `M_i(D)-|<p>|b_i`.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_affine_profile_gate.py
```

Key markers:

```text
affine_equivalence_failures=0
random_direct_payload_true=0/96
forced_affine_direct_payload_true=96/96
forced_affine_mixed_plus_anchor_true=96/96
mixed_only_anchor_false=96/96
anchor_only_mixed_false=96/96
p24_affine_direct_equations=48
p24_mixed_equations=42
p24_anchor_equations=6
direct_48_payload_iff_affine_right_profile_decomposition=1
direct_48_payload_iff_mixed_spectrum_plus_anchor=1
arithmetic_target_is_column_offsets_independent_of_right_H_coset=1
```

## Updated Proof Target

The next theorem should not try to prove a generic mixed-spectrum vanishing.
It should prove the affine section identity:

```text
M_i(D)-388430*b_i is independent of i
```

for each of the eight nonzero relative `<p>`-cosets `D`, using the actual
trace-GCD weighted packet and the selected embedded child section.
