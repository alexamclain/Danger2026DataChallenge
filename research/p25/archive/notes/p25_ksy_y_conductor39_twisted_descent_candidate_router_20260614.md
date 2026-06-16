# P25 KSY-y Conductor-39 Twisted-Descent Candidate Router

Updated: 2026-06-14 16:26 PDT

## Purpose

This is the intake form for future expert or literature claims phrased as
"take the degree-6 norm", "take a ratio", or "use Hilbert 90" on the
conductor-39 value route.

## Fixed Facts

```text
two_conjugate_sum_support              = 0
six_conjugate_sum_support              = 0
pure_character_degree6_norm_cancels    = yes
Q satisfies Frob_p(Q)=Q^-1             = yes
W=Q^6 satisfies the inverse contract   = yes
balanced_h90_support                   = 24
sparse_h90_support                     = 12
```

## Candidate Classifier

```text
pure_degree6_norm:
  decision = reject_pure_degree6_norm_cancels
  reason   = six-conjugate additive norm of the pure character word is zero

two_conjugate_pair_sum:
  decision = reject_pair_sum_cancels
  reason   = Frob_p(W)=-W, so W+Frob_p(W) has support zero

signed_shadow_only:
  decision = helper_only_signed_orbit_shadow_value_theorem_missing

quotient_ratio_only:
  decision = helper_only_ratio_boundary_value_theorem_missing

h90_boundary_only:
  decision = helper_only_hilbert90_boundary_value_theorem_missing

twisted_value_no_period156:
  decision = conditional_value_theorem_missing_period156_context

twisted_period156_value_no_source:
  decision = conditional_finite_payload_without_source_theorem

twisted_period156_source_no_framing:
  decision = source_theorem_closed_policy_or_framing_missing

danger3_framed_no_extraction:
  decision = danger3_unblocked_extraction_missing

extraction_ready_no_vpp:
  decision = extraction_ready_vpp_missing

official_vpp_verified:
  decision = submission_ready_verified_triple
```

## Counts

```text
row_count              = 14
rejected_rows          = 3
helper_only_rows       = 3
conditional_rows       = 4
source_closing_rows    = 4
danger3_unblocked_rows = 3
extraction_ready_rows  = 2
submission_ready_rows  = 1
```

## CLI Examples

Kill a pure norm claim:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_twisted_descent_candidate_router_gate.py \
  --candidate --name pure_norm_claim --theorem-body --degree6 --pure-norm
```

Expected decision:

```text
reject_pure_degree6_norm_cancels
```

Classify a real twisted period-156 source theorem before DANGER3 framing:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_twisted_descent_candidate_router_gate.py \
  --candidate --name twisted_period156_source --theorem-body --degree6 \
  --ratio --h90-boundary --finite-or-divisor --period-156 --arithmetic-source
```

Expected decision:

```text
source_theorem_closed_policy_or_framing_missing
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_twisted_descent_candidate_router_gate.py
```

Marker:

```text
ksy_y_conductor39_twisted_descent_candidate_router_rows=1/1
```
