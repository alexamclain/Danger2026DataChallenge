# p24 Recombined Mixed-Spectrum Gate

Date: 2026-06-06

## Point

The recombined coefficient-side target for one nontrivial right order-7
character is:

```text
sum_{k in D} c_k(chi) = |<p>| * c_0(chi)
```

for each of the eight nonzero `<p>`-cosets in `F_n^*`, where

```text
n = 3107441
|<p>| = 388430
(n-1)/|<p>| = 8.
```

Fourier inversion on the degree-8 quotient `F_n^*/<p>` splits this into:

```text
7 nontrivial octic quotient-character equations;
1 trivial quotient/anchor equation.
```

After expanding

```text
c_k(chi) = sum_r chi^(-1)(r mod 211) j_{r+m*k},
```

the seven nontrivial equations are exactly mixed character sums:

```text
sum_{k != 0} lambda(k) *
  sum_r chi^(-1)(r mod 211) j_{r+m*k} = 0,
```

where `lambda` runs through the seven nontrivial characters of
`F_n^*/<p>`.

The trivial quotient equation is the previously isolated anchor:

```text
sum_r chi^(-1)(r mod 211)
  * (Tr_relative(j_{r+m*bullet}) - n*j_r) = 0.
```

So the recombined theorem is no longer just "period cancellation"; it is the
specific vanishing of the `C_7 x C_8` mixed spectrum of the ordered embedded
CM sequence, plus the section-aware trace-defect anchor.

## p24 Counts

Across the six nontrivial right quotient characters:

```text
mixed octic equations = 6 * 7 = 42
anchor equations      = 6
total                 = 48
```

This is the same recombined compressed verifier from the period-coset balance
gate, but now with the exact Fourier characters named.

## Guardrail

The gate uses a split finite toy model and random ordered sequences.  Random
sequences fail the balance, and forced balanced coefficient profiles pass.  So
the theorem cannot be a formal consequence of the quotient dimensions; it must
come from the actual trace-GCD weighted CM/Lang packet.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_recombined_mixed_spectrum_gate.py
```

Key markers:

```text
balance_equivalence_failures=0
mixed_expansion_failures=0
anchor_expansion_failures=0
random_balanced_count=0/48
forced_balanced_count=48/48
forced_mixed_spectrum_zero=48/48
forced_anchor_zero=48/48
p24_mixed_octic_equations=42
p24_anchor_equations=6
p24_recombined_scalar_equations=48
recombined_balance_iff_mixed_octic_spectrum_plus_anchor=1
remaining_theorem_is_specific_cm_lang_mixed_spectrum_vanishing=1
```

## Next Proof Target

The live arithmetic theorem can now be stated as:

```text
For each nontrivial right order-7 character chi and each nontrivial octic
decomposition character lambda on F_n^*/<p>,

  sum_{k != 0} lambda(k) *
    sum_r chi^(-1)(r mod 211) j_{r+m*k} = 0,

and the six section-aware trace-defect anchors vanish.
```

Equivalently, after complete recombination, the trace-GCD weighted CM/Lang
packet has no nontrivial `C_7 x C_8` mixed spectrum and has zero right
order-7 spectrum in the selected-child trace defect.
