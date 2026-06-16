# Trace-GCD Dual-Sparse Uncertainty Bridge

Date: 2026-06-06

## Point

There is one finite CS-theory route that would genuinely close the
trace-GCD support obstruction if an arithmetic bridge supplied the missing
hypothesis.

The two sparse numbers already match:

```text
representative leading-erasure support = 35 + 19 = 54
centered plateau-difference support    = 211 - 157 = 54
```

For a prime cyclic group of length `211`, Tao/Chebotarev uncertainty gives:

```text
support_time(f) + support_frequency(f) >= 212
```

So a single nonzero bad object satisfying both

```text
support_time <= 54
support_frequency <= 54
```

cannot exist, because:

```text
54 + 54 < 212.
```

The finite implication is now Lean-checked in:

```text
p24/lean/TraceGcdDualSparseBridgeGate.lean
```

A new actual-CM finite identity removes one ambiguity in the bridge:

```text
p24/trace_gcd_difference_dft_bridge.md
p24/trace_gcd_difference_dft_bridge_audit.py
p24/trace_gcd_lambda_profile_bridge.md
p24/trace_gcd_lambda_profile_bridge_audit.py
p24/trace_gcd_lambda_plateau_rowspace_audit.py
p24/trace_gcd_lambda_plateau_det_ratio_audit.py
```

It verifies that cyclic difference is p-unit diagonal scaling on nonzero
right Fourier coordinates:

```text
DFT_right(P_b - P_{b-1})_v
  = (1 - zeta_right^v) * DFT_right(P_b)_v,   v != 0.
```

The audit also shows that direct time-difference rowspace equality with the
Lang trace-word rowspace is false on the holdout.  Therefore the remaining
bridge must identify the same bad parameter through the Fourier/Lang/Fitting
construction, not by literal rowspace equality.

The lambda-level audit verifies the parameter plumbing:

```text
profile_dft_mismatches=0
lambda_fourier_trace_mismatches=0
lang_reconstruction_mismatches=0
lang_zero_equivalence_failures=0
```

So the frequency-sparse half of the bridge is now the same `lambda`; the
unproved step is the plateau/time-sparse implication for that `lambda`.

The rowspace form of that unproved step is now audited separately:

```text
ker(B_leading) subset ker(C_plateau)
<=> rowspace(C_plateau) subset rowspace(B_leading).
```

On the current actual-CM rows the audit reports:

```text
rowspace_containment_failures=0
nonvacuous_containments=0
vacuous_full_leading_rank=10/10
```

This is evidence for the leading p-unit, but not a proof of the bridge: the
small rows have no bad lambda, so containment is automatic.

The determinant-ratio audit also reports nonzero but varying ratios in the
square holdout:

```text
both_nonzero=2/2
rowspace_equal=2/2
distinct_nonzero_ratios=2
```

So there is no obvious universal scalar comparison between the leading
determinant and the plateau determinant.

The generic plateau-subspace shortcut is also false: the p24-shaped
54-dimensional plateau-difference subspace touches all seven right factors
over a carrier field with `ord_211(q)=35`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_plateau_factor_support_audit.py \
  --q 5 --right 211 --left 157 --start 0 --zero-position 0

plateau_subspace_dim=54
nonzero_factor_blocks=7/7
```

So the bridge must be parameter-level and CM-specific.

## Why This Is Not Already A Proof

The current trace-GCD bad event is sparse in a right/Lang frequency-coordinate
model:

```text
O4 full block + final19(O1).
```

The centered plateau obstruction is sparse after cyclic differencing in the
time-coordinate model:

```text
complement of a 157-term cyclic plateau.
```

Existing notes show that each avatar is equivalent to a nearby Schubert
condition, but not that the same nonzero CM parameter produces both sparse
avatars in a prime cyclic Fourier pair.  Without that bridge, uncertainty
does not apply.

Plain plateau uncertainty only says that a plateau-bad word has frequency
support at least:

```text
212 - 54 = 158.
```

The actual p24 family can have all `210` nonzero right frequencies, so this
leaves room:

```text
158 <= support_frequency <= 210.
```

Similarly, the representative leading erasure gives a sparse frequency-side
word but no time-support bound.

## Exact Missing Bridge

A CS/ML/rank-metric proof could now target the following statement:

```text
For the actual p24 CM trace family, every nonzero `lambda` causing the
representative trace-GCD leading-erasure/Fitting failure

  a_2(lambda)=a_3(lambda)=a_5(lambda)=a_6(lambda)=0
  and first16(a_1(lambda))=0

maps, under the centered-profile Fourier transform and Lang/Fitting
trivialization, to the same nonzero plateau-annihilator parameter whose
cyclic difference word has

  time support <= 54
  and
  frequency support <= 54.
```

If this bridge is proved, the Lean gate supplies the finite contradiction.

## Evidence And Warnings

The surrounding audits demote the generic shortcuts:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
p24/plateau_uncertainty_boundary_toy.py
p24/centered_marginal_difference_code_boundary.md
p24/centered_marginal_cyclic_code_boundary.md
p24/cyclic_code_min_weight_counterexample.py
p24/trace_gcd_prefix_subcode_distance_boundary.md
```

They show:

```text
long plateau can coexist with full nonzero Fourier support;
cyclic differencing does not make the actual row space shift-stable;
pure group-theoretic cyclic-code minimum-weight shortcuts are false;
selected erasure is weaker than global MDS distance.
```

So the bridge must use the actual embedded `157/211` CM trace family.  It
cannot be a generic uncertainty or cyclic-code theorem.

## Relation To The Current Best Route

The semilinear Fitting theorem remains the primary proof target:

```text
p24/trace_gcd_semilinear_fitting_nonintersection_attack.md
```

The dual-sparse bridge is a possible way to prove its nonintersection lemma.
It is not a replacement payload and it does not change the current
four-field-element certificate surface:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```
