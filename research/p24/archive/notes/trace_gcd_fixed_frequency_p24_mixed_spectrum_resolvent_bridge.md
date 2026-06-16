# p24 Mixed-Spectrum Resolvent Bridge

Date: 2026-06-07

## Point

The recombined mixed-spectrum equation

```text
sum_{k != 0} lambda(k)
  * sum_r chi^{-1}(r mod 211) j_{r+m*k} = 0
```

is not the vanishing of one additive class-character resolvent.  It is a
Gauss-weighted linear combination of additive resolvents.

In a toy model with right prime `R` and relative prime `N`, define

```text
R(v,a) = sum_{r,k} zeta_R^(v*r) zeta_N^(a*k) j_{r+m*k}.
```

Then finite Gauss inversion gives

```text
S(chi,lambda)
  = const(chi,lambda)
    * sum_{v != 0, a != 0} chi(v) lambda^{-1}(a) R(v,a).
```

This is the exact bridge between the multiplicative-index theorem and the
ordinary additive resolvent/normality language.

## Consequence

Reduced normality of the embedded CM sequence, even if proved at the selected
p24 prime, would only say the additive resolvents `R(v,a)` are nonzero.  That
does not decide the mixed-spectrum theorem:

```text
all additive resolvents nonzero  +  mixed spectrum zero      is possible;
one additive resolvent zero      +  mixed spectrum nonzero   is possible.
```

So the next proof cannot be "normality implies the mixed spectrum vanishes" or
"normality refutes the mixed spectrum."  The needed theorem is a genuine
Stickelberger/Jacobi-sum/CM-Lang relation among the additive resolvents.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_mixed_spectrum_resolvent_bridge.py
```

Key markers:

```text
gauss_bridge_failures=0
random_all_additive_resolvents_nonzero=24/24
random_normal_like_mixed_nonzero=24/24
forced_mixed_zero_with_all_additive_resolvents_nonzero=24/24
forced_additive_resolvent_zero_with_mixed_nonzero=24/24
mixed_spectrum_is_gauss_weighted_additive_resolvent_combination=1
mixed_spectrum_is_not_a_single_class_character_resolvent=1
additive_reduced_normality_does_not_imply_mixed_spectrum_nonzero=1
additive_reduced_normality_does_not_imply_mixed_spectrum_zero=1
remaining_theorem_needs_stickelberger_or_cm_lang_relation=1
```

## Updated Proof Target

The viable theorem has to produce a relation among the additive resolvents
inside the exact Gauss-weighted sum.  In class-field language, this points at
a Stickelberger/Jacobi-sum annihilator or an embedded CM/Lang divisor identity,
not at ordinary reduced normality or a single class-character nonvanishing
statement.
