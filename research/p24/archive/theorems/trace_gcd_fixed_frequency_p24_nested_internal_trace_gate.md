# Fixed-Frequency p24 Nested Internal Trace Gate

Date: 2026-06-06

## Point

The internal trace required before the quotient Hilbert-90 step has its own
useful structure:

```text
B/E degree = 5549 = 31 * 179
C/E degree = 179
B/C degree = 31
```

For `rho=p^780`, the raw action on a relative factor cycle has order

```text
38843 = 7 * 5549,
```

and `rho^7=p^5460` acts internally with order `5549`.  The degree-5549 trace
can be factored as

```text
Tr_{B/E} = Tr_{C/E} o Tr_{B/C}.
```

Only after this nested internal trace has produced an E-valued seed does the
length-7 quotient Hilbert-90 potential apply.

## Operator Identity

In the small cyclic model with shape `7 * 5 * 3`, the checked identity is:

```text
Tr_full,epsilon
  = Tr_quot,epsilon o Tr_C/E o Tr_B/C.
```

The failure modes are also checked:

```text
Tr_quot,epsilon o Tr_B/C != Tr_full,epsilon
Tr_quot,epsilon o Tr_C/E != Tr_full,epsilon
```

for random raw components.  This means neither partial internal trace is
enough.

## p24 Theorem Target

The current fixed-frequency p24 proof target is now:

```text
1. Construct the B/C degree-31 trace/norm of the Gauss-normalized raw
   trace-resolvent contribution.

2. Construct the C/E degree-179 trace/norm, giving the E-valued seed on each
   of the ten p^780 quotient cycles.

3. Construct a quotient-cycle Hilbert-90 potential

       seed = sigma(Y) - epsilon*Y

   for each nontrivial order-7 quotient character.
```

Then the quotient twisted trace vanishes, the six `L`-valued character payload
entries vanish, and the 1092 H-coset scalar equations follow from the
character-payload contract.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_nested_internal_trace_gate.py
```

Key output:

```text
rho_order_mod_n=38843
rho7_order_mod_n=5549
p24_C_degree_over_E=179
p24_B_over_C_degree=31
p24_trace_subgroup_order=31
nested_internal_trace_equals_direct_failures=0
full_trace_equals_quotient_after_nested_internal_failures=0
quotient_after_B_over_C_only_mismatches=48/48
quotient_after_C_over_E_only_mismatches=48/48
B_over_C_trace_not_tau_fixed=48/48
C_over_E_trace_not_tau_fixed=48/48
p24_internal_degree_5549_splits_as_31_times_179=1
internal_trace_factors_as_C_over_E_after_B_over_C=1
quotient_hilbert90_applies_after_nested_internal_trace=1
partial_internal_trace_is_not_enough_for_quotient_hilbert90=1
cm_lang_target_is_nested_internal_trace_then_quotient_potential=1
```
