# Fixed-Frequency p24 Internal-Trace Then Hilbert-90 Gate

Date: 2026-06-06

## Point

The twisted Hilbert-90 payload has one more necessary layer.  The visible
`p^780` action shifts the 70 E-tensor factors by `+10`, giving ten cycles of
length `7`, but on the raw relative factor algebra it does not have order `7`.
It has order

```text
ord_n(p^780) = 38843 = 7 * 5549 = 7 * 31 * 179.
```

After seven steps, `p^5460` returns to the same E-factor and acts internally
with order

```text
5549 = 31 * 179.
```

Therefore a length-7 Hilbert-90 potential is valid only after the internal
degree-5549 contribution has been traced/normed down to an E-valued seed.
Applying the quotient length-7 trace directly to a raw factor component is the
wrong operator.

## Correct Factorization

Let `sigma` denote the raw `p^780` action on one full factor cycle, so
`sigma` has order `7*d` with `d=5549`.  For a nontrivial seventh-root
eigenvalue `epsilon`, define

```text
Tr_full,epsilon(x) = sum_{i=0}^{7d-1} epsilon^(-i) sigma^i(x)
Tr_internal(x)     = sum_{r=0}^{d-1} sigma^(7r)(x)
Tr_quot,epsilon(y) = sum_{j=0}^6 epsilon^(-j) sigma^j(y).
```

Then

```text
Tr_full,epsilon(x) = Tr_quot,epsilon(Tr_internal(x)).
```

So the live proof target has two valid forms:

```text
1. full raw form:
   construct a full-order twisted coboundary for the raw factor-cycle term;

2. traced quotient form:
   first identify the internal trace/norm as the E-valued seed, then construct
   the length-7 twisted Hilbert-90 potential for that seed.
```

The current intended route is the second form, because it matches the
70-idempotent recombination and the six `L`-valued character payload.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate.py
```

Key output:

```text
rho_order_mod_n=38843
rho7_order_mod_n=5549
rho_factor_cycle_count=10
rho_factor_cycle_length=7
full_trace_equals_quotient_trace_after_internal_trace_failures=0
naive_quotient_trace_on_raw_seed_mismatches=48/48
p780_raw_factor_action_has_order_38843_not_7=1
seven_cycle_hilbert90_requires_internal_trace_to_E_seed=1
full_twisted_trace_factors_as_internal_trace_then_quotient_trace=1
naive_length7_trace_on_raw_factor_component_is_invalid=1
cm_lang_target_must_supply_internal_trace_or_full_order_coboundary=1
```
