# Fixed-Frequency p24 Raw Coboundary Transfer Gate

Date: 2026-06-06

## Point

The nested internal trace gives a useful noncircular proof strategy if the
potential is constructed before the trace-zero conclusion.

Let `sigma` be the raw `p^780` action on a full relative factor cycle, and let
`epsilon` be the nontrivial order-7 eigenvalue attached to the right quotient
character.  If the raw Gauss-normalized contribution satisfies

```text
x = sigma(Y) - epsilon*Y
```

then the nested internal trace commutes with this coboundary:

```text
Tr_{B/E}(x)
  = sigma(Tr_{B/E}(Y)) - epsilon*Tr_{B/E}(Y).
```

Since

```text
Tr_{B/E} = Tr_{C/E} o Tr_{B/C},
```

a raw CM/Lang potential `Y` automatically supplies the E-valued quotient-cycle
Hilbert-90 potential after the degree-31 and degree-179 internal traces.

## Noncircular Target

This gives a sharpened p24 theorem target:

```text
Construct Y in the raw relative factor-cycle algebra such that

  raw_trace_resolvent_term = sigma(Y) - epsilon*Y,

before applying Tr_{B/C}, Tr_{C/E}, or the quotient twisted trace.
```

If such a `Y` is constructed from CM/Lang data, the rest is formal:

```text
raw coboundary
=> nested E-valued seed coboundary
=> quotient twisted trace zero
=> six L-valued character payload zeros
=> 1092 H-coset verifier equations.
```

## Circular Boundary

In a semisimple cyclic model,

```text
im(sigma - epsilon) = ker(Tr_full,epsilon).
```

So solving for `Y` after first proving the trace is zero is circular.  The
potential is useful only if it is constructed independently from the embedded
CM/Lang tower.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate.py
```

Key output:

```text
rho_order_mod_n=38843
rho7_order_mod_n=5549
p24_C_degree_over_E=179
p24_B_over_C_degree=31
raw_coboundary_transfer_failures=0
quotient_trace_nonzero_after_transfer=0/48
transferred_seed_not_quotient_fixed=0/48
random_nested_seed_quotient_trace_zero=1/48
random_nested_seed_not_forced_coboundary=47/48
circular_inverse_rank_kernel_checks=[(104, 104), ...]
nested_internal_trace_commutes_with_twisted_coboundary=1
raw_cm_lang_coboundary_would_supply_quotient_potential=1
solving_potential_after_zero_is_hilbert90_circular=1
```
