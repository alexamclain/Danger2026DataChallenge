# P25 KSY-y Subsqrt Arithmetic-Producer Route Packet

Updated: 2026-06-14 19:12 PDT

## Purpose

The subsqrt budget ladder proves that the current finite objects are tiny
relative to `sqrt(p)`.  This packet says what kind of arithmetic theorem would
make one of those finite objects a real moonshot checkpoint rather than a
finite replay.

The rule is:

```text
universal intake pass = finite payload compatibility
curved-corner helper = routed through the unit-triangle minimal closing ask
arithmetic producer theorem = source proof that explains the payload
DANGER3 submission = concrete (p,A,x0) verified by official vpp.py
```

## Route Rows

```text
hilbert90_signs_source_theorem:
  finite interface = eps=1, branch=-1
  payload size     = 2
  missing          = arithmetic proof producing the signs

source_packet_source_theorem:
  finite interface = six signed C3 x C169 cells plus primitive K
  payload size     = 6
  missing          = challenge-legal arithmetic producer for the packet

quotient_factor_source_theorem:
  finite interface = base=(1,25), D=(1,3), T=(2,113), primitive K
  payload size     = 3
  missing          = arithmetic theorem selecting these classes with orientation

curved_corner_source_theorem:
  finite interface = curved Newton triangle, recorded 197/310 edge, full K trace,
                     raw D^3=Y with kernel trace, active C169 lift,
                     quadratic fiber section, nonsplit carry, unit triangle
  payload size     = 75
  missing          = finite value/divisor theorem for the curved K-traced corner payload
  closing ask      = period-156 value/divisor arithmetic source theorem

compact_theta2_exact_product_theorem:
  finite interface = center_base=(44,166), half_shift=(56,28), theta2 orientation
  payload size     = 300
  missing          = DANGER3 finite-identity/non-CM framing

period156_value_source_theorem:
  finite interface = exact finite-field value identity for P with period-156 context
  payload size     = 46800
  missing          = DANGER3 finite-identity/non-CM framing after value-source closure

extraction_ready_unverified_triple:
  finite interface = DANGER3-framed theorem plus concrete A,x0 extraction
  missing          = actual vpp.py-verified (p,A,x0)

verified_pomerance_triple:
  finite interface = official p25 (p,A,x0) triple
  missing          = none
```

## Smoke-Tested Front Doors

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode hilbert90-signs --eps 1 --branch -1

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode source-packet \
  --packet research/p25/producer_payload_fixtures/source_packet_target.txt \
  --k-multiplier 1

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode quotient-factor \
  --base-right-class 1 --base-c 25 \
  --d-right-class 1 --d-c 3 \
  --t-right-class 2 --t-c 113 \
  --k-multiplier 1

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py \
  --candidate --name curved_corner_source_shape \
  --theorem-body --triangle --curvature --half-bridge-edge \
  --full-k-trace --raw-relation --raw-kernel-trace --primitive-c169 \
  --active-c169-lift --quadratic-fiber --nonsplit-carry --unit-triangle

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode compact-theta2 \
  --center-right 44 --center-c 166 \
  --half-right 56 --half-c 28 --invert

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name subsqrt_period156_value_theorem \
  --anchor siegel_robert_value_units --output-kind value \
  --exact-product --mixed-graph --finite-field-identity --period-156

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name subsqrt_extraction_ready_unverified \
  --source-family subsqrt_arithmetic_producer --output-kind period-value \
  --exact-p --mixed-graph --equal-weight --orientation \
  --arithmetic-source --finite-identity --period-156 \
  --danger3-framing --extraction
```

All seven smoke tests returned their expected candidate marker `1/1`.

The integrated route packet also depends on:

```text
ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1
```

## Counts

```text
route_count                    = 8
universal_candidate_commands   = 4
source_claim_commands          = 1
closing_obligation_commands    = 2
finite_payload_accept_rows     = 8
source_theorem_closing_rows    = 4
value_route_rows               = 3
producer_theorem_missing_rows  = 4
danger3_remaining_rows         = 6
extraction_remaining_rows      = 6
submission_ready_rows          = 1
all_routes_subsqrt             = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_subsqrt_arithmetic_producer_route_packet_gate.py
```

Marker:

```text
ksy_y_subsqrt_arithmetic_producer_route_packet_rows=1/1
```
