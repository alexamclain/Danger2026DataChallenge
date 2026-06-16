# P25 KSY-y H0 Source-Theorem Candidate Matcher

Updated: 2026-06-14 16:18 PDT

## Purpose

This is the executable intake sheet for future paper snippets, expert answers,
or subagent reports about the H0 lane.  It classifies whether a proposed
theorem hits one of the four exact legal H0 products, whether it is one of the
two source-closing answer shapes, and how far it gets through the downstream
DANGER3 extraction ladder.

## Legal Product Targets

```text
support_period        = 156
ambient_period        = 780
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

The target theorem must hit exactly one of these four rows:

```text
m=1, canonical_H0
  constants = (3, 3, -3, -3)
  P = (7, 17, 23, 34, 37, 38)
  N = (4, 8, 10, 11, 20, 25)

m=2, H0_translate
  constants = (-3, 3, 3, -3)
  P = (7, 14, 29, 34, 35, 37)
  N = (1, 8, 11, 16, 20, 22)

m=4, H0_translate
  constants = (-3, -3, 3, 3)
  P = (14, 19, 28, 29, 31, 35)
  N = (1, 2, 5, 16, 22, 32)

m=8, H0_translate
  constants = (3, -3, -3, 3)
  P = (17, 19, 23, 28, 31, 38)
  N = (2, 4, 5, 10, 25, 32)
```

## Classifier

```text
source-certification only:
  decision = source_certified_value_or_divisor_missing

exact value without period-156 context:
  decision = conditional_missing_period_156_context

exact value with period-156 context:
  decision = source_theorem_closed_policy_or_framing_missing

divisor/additive identity without H90 boundary:
  decision = conditional_divisor_identity_missing_h90_boundary

divisor/additive identity with H90 boundary:
  decision = source_theorem_closed_policy_or_framing_missing

computed payload without arithmetic source theorem:
  decision = conditional_finite_payload_without_source_theorem

wrong residue sets or nonlegal product:
  decision = reject_wrong_or_nonlegal_h0_product
```

After a source yes, the downstream classifier continues:

```text
DANGER3 framed, no same-j bridge:
  decision = upstream_odd_value_no_cross_level_bridge

same-j bridge, no X1(16) specialization:
  decision = cross_level_target_identified_specialization_missing

X1(16) surface, no x0:
  decision = x16_surface_reached_halving_or_vpp_missing

concrete x0, no official vpp.py:
  decision = extraction_ready_vpp_missing

official vpp.py-verified (p,A,x0):
  decision = submission_ready
```

## Counts

```text
row_count                   = 13
legal_product_rows          = 11
source_closing_rows         = 7
source_certified_only_rows  = 1
conditional_rows            = 3
rejected_rows               = 2
downstream_unblocked_rows   = 3
submission_ready_rows       = 1
```

## CLI Examples

Classify a promising value theorem that has period-156 context but no DANGER3
framing yet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_source_theorem_candidate_matcher_gate.py \
  --product-multiplier 2 --residue-exact --source-theorem \
  --output-kind value --period-156
```

Expected decision:

```text
source_theorem_closed_policy_or_framing_missing
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_source_theorem_candidate_matcher_gate.py
```

Marker:

```text
ksy_y_h0_source_theorem_candidate_matcher_rows=1/1
```
