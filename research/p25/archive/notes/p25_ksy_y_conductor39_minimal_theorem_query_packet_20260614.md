# P25 KSY-y Conductor-39 Minimal Theorem-Query Packet

Updated: 2026-06-14 19:38 PDT

## Purpose

The smallest live theorem-source target is now the mixed conductor-`39` source,
not the full 75-atom product directly:

```text
U_chi = -chi_3 * chi_13 on X_1(39)
W = 6 * U_chi
Norm_156(Y_507) = distribution_lift_39_to_507(W)
```

The conductor-`39` source is certified.  The missing theorem is a finite-field
value identity or divisor/additive identity for that source object, with
period-`156` context if the output is a value.

The routine gate uses recorded markers for the source-theorem intake
regression, certified source stack, and subsqrt arithmetic-producer route
packet, rather than recomputing those deep dependency trees on every
theorem-query check.

## Query Rows

```text
certified_source_object_only:
  decision = conductor39_source_identified_value_or_divisor_theorem_missing
  missing  = finite-field value identity or divisor/additive theorem

period_value_without_period156:
  decision = conditional_missing_period_156_context
  missing  = period-156 branch/root/telescoping context

period156_value_policy_missing:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

divisor_theorem_policy_missing:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

formal_sparse_gauge_no_boundary:
  decision = reject_formal_sparse_gauge_without_boundary
  missing  = ratio or Hilbert-90 boundary legitimizing the sparse gauge

prime13_projection_shadow:
  decision = reject_loses_mixed_tensor
  missing  = mixed chi_3 tensor chi_13 source on X_1(39)

extraction_ready_unverified:
  decision = ready_to_extract_and_verify_concrete_triple
  missing  = official vpp.py verification of a concrete triple

verified_pomerance_triple:
  decision = submission_ready_verified_triple
  missing  = none
```

## Smoke Tests

The following source-theorem intake candidates were run through the CLI and
returned `ksy_y_conductor39_source_theorem_intake_candidate_rows=1/1`:

```text
certified_source_object_only
period156_value_policy_missing
divisor_theorem_policy_missing
formal_sparse_gauge_no_boundary
prime13_projection_shadow
verified_pomerance_triple
```

## Counts

```text
query_count                  = 8
candidate_commands           = 8
source_identified_rows       = 6
source_theorem_closing_rows  = 4
rejected_rows                = 2
conditional_rows             = 1
helper_only_rows             = 1
submission_ready_rows        = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_minimal_theorem_query_packet_gate.py
```

Marker:

```text
ksy_y_conductor39_minimal_theorem_query_packet_rows=1/1
```

Dependency markers:

```text
ksy_y_conductor39_source_certificate_stack_rows=1/1
ksy_y_conductor39_source_theorem_intake_rows=1/1
ksy_y_subsqrt_arithmetic_producer_route_packet_rows=1/1
```
