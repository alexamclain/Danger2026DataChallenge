# P25 KSY-y Source-Theorem Priority Selector

Updated: 2026-06-14 22:15 PDT

## Purpose

This selector turns the current KSY/Yang/Hilbert-90 frontier into a source
search order.  It ranks theorem clauses, not experiments, and keeps certified
source objects distinct from closure.

## Priority

Priority 1 asks avoid the period-value branch:

```text
h0_or_conductor39_divisor_additive_boundary_identity:
  ask = exact divisor/additive theorem for H0/H0-translate or conductor-39 source
  need = legal Hilbert-90 boundary
  why = closes source stage without a finite value branch

twisted_h90_divisor_identity:
  ask = finite divisor/additive theorem for the twisted ratio/H90 object
  need = exact object and arithmetic source theorem
  why = same source-stage closure without period-value branch

curved_corner_divisor_additive_identity:
  ask = finite divisor/additive theorem for the unit-triangle curved K-traced corner
  need = exact unit-triangle payload and arithmetic source theorem
  why = same source-stage closure without period-value branch
```

Priority 2 asks are still live, but require period-`156` value context:

```text
exact_p_value_with_period156_context:
  ask = exact P, Y_507, or legal H0 value
  need = exact object, mixed graph or legal boundary, finite identity, period-156 context

twisted_h90_value_with_period156_context:
  ask = twisted ratio/H90 finite value theorem
  need = period-156 branch/root/telescoping context

curved_corner_value_with_period156_context:
  ask = unit-triangle curved corner finite value theorem
  need = exact payload, arithmetic source theorem, and period-156 context
```

## Not Source Closure

```text
conductor39_source_certification_only:
  status = source object certified, value/divisor theorem missing

h0_source_certification_only:
  status = four legal H0 products certified, value/divisor theorem missing

finite_payload_fixture_without_source:
  status = exact target fixture, arithmetic source theorem missing
```

## Reject

```text
ambient_780_value:
  reject = gcd(4^780 - 1, p - 1) = 11

literal_75_atom_enumeration:
  reject = 75 atoms are fixed product factors, not 75 candidate tries

generic_generation_or_cm_language:
  reject = not an exact p25 finite product/value/divisor identity
```

## Counts

```text
row_count                   = 13
source_closing_yes_rows     = 6
priority1_rows              = 3
priority2_rows              = 3
source_certified_rows       = 8
current_evidence_only_rows  = 6
conditional_rows            = 3
rejected_rows               = 3
downstream_rows             = 1
```

Preferred first asks:

```text
h0_or_conductor39_divisor_additive_boundary_identity
twisted_h90_divisor_identity
curved_corner_divisor_additive_identity
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_source_theorem_priority_selector_gate.py
```

Marker:

```text
ksy_y_source_theorem_priority_selector_rows=1/1
```

## Interpretation

The next source/literature/expert pass should first ask for exact
divisor/additive identities with legal Hilbert-90 boundary, because those
would close the source stage without the extra period-`156` value-branch
obligation.  Exact value identities remain live only when they carry
period-`156` branch/root/telescoping context.  The unit-triangle curved-corner
producer is now a first-class priority-1 ask; literal enumeration of the 75
KSY atoms is explicitly rejected as a route.
