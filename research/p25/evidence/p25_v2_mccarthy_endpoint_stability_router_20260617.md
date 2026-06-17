# P25 v2 McCarthy Endpoint Stability Router

Updated: 2026-06-17

Marker: `p25_v2_mccarthy_endpoint_stability_router_rows=1/1`

## Purpose

Promote the archived Lane-B/McCarthy square-axis microscope into a compact
support-lane verdict.

The finite endpoint is real and reusable:

```text
e_138 on C_507
U(q) = 1 + (zeta_39^5 - 1) * e_138(q)
zeta_39^5 - 1 = 1375 in F_2029, inverse = 636
```

But the route is not currently a source-stage closer. The minimal auxiliary
field projection is representation-specific, and no simple target-factor
normalization repairs it across auxiliary primes.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `archive/harness/p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe.py`
- `archive/harness/p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan.py`
- `archive/harness/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py`
- `archive/gates/p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate.py`
- `archive/gates/p25_laneB_square_axis_mccarthy_idempotent_unit_gate.py`

## Commands

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/harness/p25_laneB_square_axis_mccarthy_aux_prime_invariance_probe.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/harness/p25_laneB_square_axis_mccarthy_theorem_factor_normalization_scan.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/harness/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/gates/p25_laneB_square_axis_mccarthy_idempotent_unit_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/gates/p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate.py

PYTHONDONTWRITEBYTECODE=1 \
python3 research/p25/archive/gates/p25_v2_mccarthy_endpoint_stability_router_gate.py
```

The router returned
`p25_v2_mccarthy_endpoint_stability_router_rows=1/1`.

## Evidence

```text
target_q_exp = 138
probe_multipliers = (1, 4, 7)
minimal_projection_ok = 1
other_projection_ok = (False, False)
q_power_projection_aux_prime_invariant = 0
posthoc_projection_representation_specific = 1

theorem_factor_scans = 236
theorem_factor_all_mu39_hits = 0
easy_theorem_factor_normalization_found = 0

transported_minus_one = 1375
transported_minus_one_inverse = 636
normalized_raw_y_closes = 1
unnormalized_control_fails_exact_packet = 1

endpoint_projector_ok = 1
endpoint_unit_minus_one_ok = 1
endpoint_fourier_support = 507
endpoint_unit_order = 39
endpoint_fourier_dense = 1

current_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
```

## Decisions

```text
raw_q_power_projection
  decision = repair_not_auxiliary_prime_invariant
  reason = R(138)^2029 lands in mu_39 only at the minimal auxiliary prime

easy_target_factor_normalization
  decision = reject_no_repair_found
  reason = denominator, prefactor, visible Gauss factors, and small theorem
           monomials produce zero all-prime mu_39 repairs across 236 scans

sparse_endpoint
  decision = evidence_test_object_not_source_theorem
  reason = e_138 and U(q) round-trip to the existing normalized raw-Y closure
           but do not supply the arithmetic producer

ordinary_fourier_filter_route
  decision = repair_dense_filter_debt
  reason = e_138, U - 1, and U are Fourier-dense on C_507
```

## Verdict

The McCarthy square-axis artifact should stay alive only as a support
microscope and endpoint intake:

```text
candidate source theorem -> sparse q-coefficients -> endpoint harness
```

It should not be promoted to a first-pass theorem front. A future McCarthy,
finite-hypergeometric, or Barnes-style lead must either produce the sparse
endpoint directly as an arithmetic theorem, or explain a nontrivial quotient
cancellation that is invariant across auxiliary primes. Reusing the raw
`R(138)^2029` projection or adding simple visible target factors is already
falsified.
