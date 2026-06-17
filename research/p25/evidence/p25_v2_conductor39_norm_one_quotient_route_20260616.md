# P25 v2 Conductor-39 Norm-One Quotient Route

Updated: 2026-06-16

## Purpose

Promote the compact conductor-39 quotient

```text
Q = prod_{h in <2>} E_{7h} / E_h
```

as a value-side theorem-facing object. This is useful because it is smaller
than the 24-entry character word and has a clean Frobenius contract:
`Frob_p(Q)=Q^-1`, so `Q^6` is a Hilbert-90 boundary. This page does not claim
a source theorem exists; it records the route and first falsifiers.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_primitive_character_unit_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_coset_selector_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_coset_frobenius_pairing_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_frobenius_orbit_20260614.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_conductor39_norm_one_quotient_route_gate.py
```

The gate returned `p25_v2_conductor39_norm_one_quotient_route_rows=1/1`.

## Invariants

```text
U_chi = -chi_39 = 1_{7<2>} - 1_{<2>}
<2> = (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)
7<2> = (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)

Q = prod_{h in <2>} E_{7h} / E_h
Frob_p(Q) = Q^-1
W = 6 * U_chi
Q^6 = (1 - Frob_p)(Q^3)
```

The explicit Frobenius shifts on the ordered `<2>` cycle are:

```text
denominator index i -> numerator index i+11
numerator index i   -> denominator index i+9
Frob_p^2 shift      -> i+8 on each layer
```

The naïve degree-6 norm of the pure conductor-39 character word cancels:

```text
pure_character_degree6_norm = 0
```

## Routes

```text
norm_one_Q_value_theorem_with_period156_context
  decision = route_through_period156_value_source_hook
  missing  = downstream DANGER3 framing and extraction after a source theorem

explicit_Q3_hilbert90_preimage_with_finite_theorem
  decision = normalize_h90_preimage_then_apply_source_snippet_intake
  missing  = same theorem data after legal Hilbert-90 descent normalization

coset_selector_or_Q_source_only
  decision = repair_finite_value_divisor_theorem_missing
  missing  = finite value/divisor theorem for Q, Q^3, Q^6, or the selected
             Yang lift

Q6_boundary_only
  decision = repair_additive_or_value_normalization_missing
  missing  = scalar-fixed finite value/additive data, not just the Hilbert-90
             boundary

primitive_U_chi_power_only
  decision = repair_yang_lift_descent_and_finite_theorem_missing
  missing  = Yang lift, Hilbert-90 descent, and finite theorem for the
             selected row

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels
  falsifier = Frobenius alternation makes the degree-6 norm zero
```

## Counts

```text
invariant_rows_ok = 6/6
support_routes = 2
repair_rows = 3
reject_rows = 1
current_source_theorems = 0
p25_v2_conductor39_norm_one_quotient_route_rows=1/1
```

## Verdict

The compact `Q` route is a better value-side support object than the raw
24-entry character word: a source theorem may target a norm-one quotient with
`Frob_p(Q)=Q^-1`, or the Hilbert-90 preimage `Q^3`, then route through the
period-156 value/source hook or source-snippet intake.

This does not close source stage. The current theorem still has to supply a
finite value/divisor theorem with period-156 context, or scalar-fixing
additive/value data after the legal descent. A source answer that only norms
the pure conductor-39 character down from degree 6 is rejected because that
norm cancels.
