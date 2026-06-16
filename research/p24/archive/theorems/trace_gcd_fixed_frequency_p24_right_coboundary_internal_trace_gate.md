# Fixed-Frequency p24 Right Coboundary Internal-Trace Gate

Date: 2026-06-06

## Point

The right-coboundary obstruction gate says formal right-character covariance
is not enough.  This gate gives the positive replacement:

```text
R_chi in im(sigma - epsilon_chi)
```

is equivalent, in the raw cyclic tower model, to vanishing of the nested
internal trace obstruction.

For p24 the raw order has the shape:

```text
7 * 179 * 31.
```

The internal trace is:

```text
Tr_{B/E} = Tr_{C/E} o Tr_{B/C}
```

with degrees `179` and `31`.

## Proof Meaning

The noncircular theorem target is now:

```text
prove from CM/Lang packet structure that the nested internal trace of the
Gauss-normalized right packet obstruction is zero.
```

After that identity is proved, Hilbert-90 inversion is formal and can construct
the right potential.  Inverting Hilbert-90 without this independent internal
trace identity would still be circular.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_coboundary_internal_trace_gate.py
```

Key output:

```text
coboundary_ranks=[104, 104, 104, 104, 104, 104]
nested_internal_equals_direct_failures=0
full_trace_equals_quotient_after_nested_failures=0
membership_iff_internal_trace_zero_failures=0
random_internal_trace_zeroes=0/24
random_coboundary_memberships=0/24
forced_internal_trace_zeroes=24/24
forced_coboundary_memberships=24/24
matching_right_coboundary_equiv_nested_internal_trace_zero=1
internal_trace_identity_is_the_non_circular_cm_lang_target=1
hilbert90_inverse_is_formal_after_internal_trace_zero=1
generic_right_packets_do_not_satisfy_internal_trace_zero=1
```

