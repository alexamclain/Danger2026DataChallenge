# P25 KSY-y Post-Scout Moonshot Reduction

Updated: 2026-06-13 21:14 PDT

## Purpose

The five primary-source scouts are now complete.  This note compresses them
into the current first-class moonshot queue: what would actually count, what
the first falsifier is, and which local gate should classify the next hit.

Target:

```text
p = 10000000000000000000000013
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
support period = 156
ambient period = 780
```

Trace data kept in scope:

```text
t = 5808037298190,  v2 = 42, odd part = 2273736754431
t = 1409990787086,  v2 = 50, odd part = 8881784197
t = -2988055724018, v2 = 42, odd part = 2273736754433
```

The `v2 = 50` trace remains the default moonshot focus unless a source theorem
chooses a cheaper admissible trace.

Priority-1 follow-up artifact:

```text
research/p25/p25_ksy_y_priority1_exact_divisor_lane_20260613.md
marker: ksy_y_priority1_exact_divisor_lane_rows=1/1

research/p25/p25_ksy_y_priority1_sprang_source_split_20260613.md
marker: ksy_y_priority1_sprang_source_split_rows=1/1

research/p25/p25_ksy_y_priority1_ksy_source_split_20260613.md
marker: ksy_y_priority1_ksy_source_split_rows=1/1

research/p25/p25_ksy_y_priority1_theorem_query_packet_20260613.md
marker: ksy_y_priority1_theorem_query_packet_rows=1/1
```

## Ranked Targets

1. `sprang_or_ksy_exact_theta2_or_p_divisor`

Continue first.  A positive artifact is an exact `P` or exact
theta2/theta2-inverse divisor/additive identity with the mixed graph,
orientation, equal weights, and an arithmetic producer.  The first falsifier is
formula language, dlog/distribution, or class-field generation without exact
`P`/theta2 mixed-graph data.

2. `kubert_lang_raw_mixed_product`

Continue, but below the exact-divisor lane.  A positive artifact is exact row
labels, reflection center, or raw equal-weight `K`-traced product plus an
arithmetic producer.  The first falsifier is a `C169` projection,
Kubert-Lang congruence hygiene, or generator theorem without the mixed graph.

3. `siegel_robert_exact_period_value`

Continue after the product/divisor lanes.  A positive artifact is an exact
finite-field value identity for `P` with mixed graph and period-`156`
branch/root/telescoping context.  The first falsifier is class-field generation,
a bare value, or an ambient period-`780` value.

4. `danger3_policy_or_extraction_only`

Continue only on a theorem hit or a Drew answer.  A positive artifact is policy
acceptance plus an extraction path, or a concrete p25 `(A,x0)` accepted by
official `vpp.py`.  Policy-only, theorem-only, extraction-without-output, and
unverified triples are not submission-ready.

5. `broad_generation_shadows`

Kill as direct moonshot targets.  This includes KSY Theorem 5.3 field
generation, Schertz/Shin class-field generation, Kubert-Lang generator
theorems, ordinary theta_D at `D=2`, and generic CM/Lang provenance unless they
are upgraded into one of the exact payloads above.

## Local Gates

Reduction gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_scout_moonshot_reduction_gate.py
```

Exact product closing candidate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name full_theorem_ready --source-family KSY-KL \
  --exact-p --mixed-graph --equal-weight --orientation --arithmetic-source \
  --output-kind divisor-additive --finite-identity --danger3-framing --extraction
```

Raw divisor theorem-hit router:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type raw-divisor --center-right 47 --center-c 28 \
  --d-right 22 --d-c 3 --k-multiplier 1
```

Priority-1 exact divisor lane:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_exact_divisor_lane_gate.py
```

Priority-1 Sprang source split:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_sprang_source_split_gate.py
```

Priority-1 KSY source split:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_ksy_source_split_gate.py
```

Priority-1 theorem query packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_theorem_query_packet_gate.py
```

Raw value theorem-hit router:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type raw-value --center-right 47 --center-c 28 \
  --d-right 22 --d-c 3 --k-multiplier 1 --period-156-context
```

Concrete triple submission check:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py \
  --p P --A A --x0 X0
```

## Completed Gate

```text
active_theorem_targets             = 3
challenge_targets                  = 1
killed_shadow_targets              = 1
direct_source_closing_rows         = 0
hypothetical_source_closing_rows   = 4
hypothetical_submission_rows       = 1
```

Marker:

```text
ksy_y_post_scout_moonshot_reduction_rows=1/1
```
