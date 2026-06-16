# Oriented Recovery-Cycle Payload Gate

Date: 2026-06-07

## Point

The selected-chain certificate carries a selected degree-`3107441` recovery
polynomial.  A more literal fallback surface is to carry one full oriented
recovery cycle for the composite class

```text
a = 2 * 463 * 223^(-1)
order(a) = 3107441.
```

One step can be verified without a huge composite modular polynomial by
carrying two intermediate `j`-values:

```text
j_i --Phi_2-- u_i --Phi_463-- v_i <--Phi_223-- j_{i+1}.
```

Thus the cycle payload is `3n` field elements, plus the tiny post-`j`
Montgomery tail `A,x0`.

## p24 Accounting

```text
selected_chain_slots = 3107811
full_relative_table_slots = 3174011
oriented_cycle_path_slots = 9322323
oriented_cycle_plus_A_x0_slots = 9322325
dense_phi_table_slots_if_serialized = 266866
cycle_plus_tail_plus_dense_phi_slots = 9589191

oriented_cycle_plus_A_x0_over_sqrt = 9.322325e-6
cycle_plus_tail_plus_dense_phi_over_sqrt = 9.589191e-6
```

So this fallback is larger than the selected-chain artifact but still a strict
sub-sqrt finite surface for p24.

## Verifier Contract

The finite verifier would check:

```text
j0 = j(A)
DANGER x-only replay accepts (A,x0)
the cycle closes after n steps
the n j-vertices are distinct
each step satisfies Phi_2, Phi_463, and Phi_223 in the oriented pattern
```

The modular-polynomial tables are canonical verifier data, not an `h`-sized
class table.  Even if serialized densely, they are negligible against
`sqrt(p)` for this fixed p24 surface.

## Caveat

This does **not** remove the hard part.  It only says that if a producer lands
at one honest target recovery cycle rather than a selected recovery
polynomial, the resulting artifact is still sub-sqrt.  The seedless
construction of such a target cycle remains open.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/oriented_recovery_cycle_payload_gate.py
```

Key markers:

```text
oriented_cycle_payload_is_larger_than_selected_chain_but_subsqrt=1
modular_polynomial_tables_are_canonical_not_h_sized=1
producer_still_must_find_one_target_cycle_or_final_A_x0=1
this_surface_does_not_remove_the_seedless_cycle_problem=1
conclusion=reported_oriented_recovery_cycle_payload_gate
```
