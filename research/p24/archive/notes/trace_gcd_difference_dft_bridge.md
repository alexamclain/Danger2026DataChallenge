# Trace-GCD Difference DFT Bridge

Date: 2026-06-06

## Point

The dual-sparse uncertainty route needs the time-sparse plateau-difference
avatar and the frequency-sparse trace-GCD avatar to be attached to the same
bad parameter.  One finite part of that bridge is now explicit:

```text
Q_b = P_b - P_{b-1}

DFT_right(Q)_v = (1 - zeta_right^v) * DFT_right(P)_v,
    v != 0 mod right.
```

Since `right` is prime to `p` and `v` is nonzero, the multiplier
`1 - zeta_right^v` is a p-unit.  Therefore cyclic differencing preserves the
nonzero right-frequency Fitting support up to p-unit diagonal scaling.

For p24 this applies to `right=211`; in the small holdouts it applies to
`right=7`.

## Actual-CM Audit

The identity is checked on the two current actual-CM rows by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
p24/trace_gcd_difference_dft_bridge_audit.py
```

Current output:

```text
dft_difference_mismatches=0
nonzero_multiplier_failures=0
direct_rowspace_equal=0/1
conclusion=reported_trace_gcd_difference_dft_bridge_audit
```

Interpretation:

```text
cyclic_difference_is_punit_diagonal_on_nonzero_right_dft=1
naive_time_difference_equals_lang_traceword_rowspace=0
remaining_bridge_is_same_kernel_parameter_through_fourier_lang_fitting=1
```

The direct rowspace shortcut is false on the holdout where it can be tested,
so the theorem cannot say that the time-difference rowspace literally equals
the Lang trace-word rowspace.  It has to pass through:

```text
centered difference
  -> nonzero right DFT
  -> p-unit diagonal multiplier
  -> Lang/Frobenius trivialization
  -> semilinear Fitting kernel parameter.
```

The lambda-level version of that pass-through is now recorded in:

```text
p24/trace_gcd_lambda_profile_bridge.md
p24/trace_gcd_lambda_profile_bridge_audit.py
```

It checks on the pinned row and holdout that:

```text
DFT_right(f_lambda)_v = Tr_{LR_v/R_v}(lambda*S_v)
```

and that the Lang coordinates preserve the same parameter's zero conditions
on each right Frobenius orbit.

## Refined Missing Bridge

For `lambda in L = F_p(mu_157)`, define the centered right-profile scalar
word:

```text
f_lambda(s) = Tr_{L/F_p}(lambda * G_s^0),     s mod 211.
```

The sharp theorem candidate is now parameter-level:

```text
For the p24 selected ordinary CM point, if nonzero lambda causes the
representative trace-GCD leading-erasure/Fitting failure

  a_2(lambda)=a_3(lambda)=a_5(lambda)=a_6(lambda)=0
  and first16(a_1(lambda))=0,

then f_lambda vanishes on the selected 157-term cyclic plateau containing 0.
```

If this is proved, the finite counts become:

```text
frequency support <= 35 + 19 = 54
time support      <= 211 - 157 = 54
54 + 54 < 212
```

and `p24/lean/TraceGcdDualSparseBridgeGate.lean` gives the contradiction.

The credible identity tying `lambda` to the nonzero right frequencies is:

```text
S_v = sum_s zeta_211^(v*s) G_s^0
hat(f_lambda)(v) = Tr_{L R_v / R_v}(lambda * S_v)
```

with the Lang trace-dual basis and the p-unit cyclic-difference multiplier
now audited as finite linear identities in small actual-CM rows.

## Negative Control

The generic subspace version is false.  The p24-shaped plateau subspace is
not supported on the representative erasure factors:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/centered_plateau_factor_support_audit.py \
  --q 5 --right 211 --left 157 --start 0 --zero-position 0
```

Current output:

```text
plateau_subspace_dim=54
nonzero_factor_blocks=7/7
degree-35 block ranks = 35,35,35,35,35,35
```

So the theorem cannot be:

```text
plateau subspace = representative leading-erasure support.
```

It must use the actual CM trace family and the selected bad parameter
`lambda`.

## What Remains

This note proves only the p-unit diagonal coordinate identity.  It does not
prove that the trace-GCD kernel vector is the centered plateau annihilator.
That remaining assertion is exactly an arithmetic Schur/Lang/Fitting
parameter-identification theorem, not a generic cyclic-code theorem.
