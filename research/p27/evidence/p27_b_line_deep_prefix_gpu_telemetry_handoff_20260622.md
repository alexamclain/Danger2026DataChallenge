# P27 B-Line Deep-Prefix GPU Telemetry Handoff

Date: 2026-06-22

## Claim

The next B-line GPU use should be bounded same-stream telemetry, not a
production hunt.

The B-line quotient is the best current multi-gate structural clue:

```text
B = 8X^2/(X^2 - 1)^2
A + 2 = B^2
```

CPU and small-field tests show that the original `Bplus` value determines the
active selected gate bits through `d12` in the tested p27 samples, with no
mixed B groups.  That could become sqrt-beating only if it yields a Kummer
sequence, recurrence, or source for many all-plus gates at once.

## Manifest

Machine-readable GPU contract:

```text
research/p27/archive/fixtures/p27_b_line_deep_prefix_gpu_telemetry_suite_20260622.json
```

## What To Run

Emit, from the same p27 candidate stream:

```text
Bplus
legal d2/domain status
selected gate bits d3,d4,...,dN
first failing gate
candidate replay key
raw source draw denominator
accepted/legal row denominator
```

Minimum useful depth is `d3..d12`, matching the current CPU deep-descent
frontier.  If the native code can expose deeper bits cheaply, extend to
`d3..d16`.

Use three bounded tiers:

```text
1. implementation smoke: at least 100000 legal d2 rows
2. large telemetry: at least 10000000 accepted/legal rows if cheap
3. optional deep tail: only after a recurrence or coupling signal appears
```

## What To Report

Required fields:

```text
raw_source_draws
accepted_candidates
legal_d2_rows
unique_Bplus_values_or hashes
B_group_size_histogram
per-gate active/plus/minus/mixed/missing B-group counts
all-plus prefix counts by gate
examples of any mixed B groups with full replay payload
pairwise and lagged correlations between selected bits
short sign-word bucket counts
target_survivors_per_raw_source_draw
target_survivors_per_gpu_second
overhead_vs_baseline
build commit and replay command
```

The raw-source denominator is mandatory.  Conditional lifts are useful only
when they improve the actual source-space exchange rate.

## Promotion

Promote only if at least one of these happens:

```text
zero or explainable mixed B groups persist at large scale through meaningful depth
all-plus prefixes beat independent half-loss by >=1.25x source-normalized
a sign-word state or recurrence survives heldout accounting
the output names a Kummer/divisor hypothesis for f3(B), f4(B), f5(B), ...
```

If promoted, the next artifact is not another bucket run.  It is either a
direct sampler/source law or an exact CAS extraction target for the B-line
classes.

## Kill

Kill this telemetry lane if:

```text
mixed B groups occur materially
prefix counts are geometric half-loss after source normalization
no recurrence/coupling appears
telemetry overhead is high and the rows do not feed class extraction
only bucket lifts are reported without raw source accounting
```

## Relationship To The Quartic Suite

The full B/K quartic GPU suite remains the sharper visible low-genus screen:
[P27 Full Quartic GPU Suite Handoff](p27_full_quartic_gpu_suite_handoff_20260622.md).

This B-line telemetry suite is complementary.  It asks whether the no-mixed-B
deep descent persists at GPU scale and whether the selected bit sequence has a
coupling that can feed the post-quartic CAS route:
[P27 Post-Quartic CAS Suite Handoff](p27_post_quartic_cas_suite_handoff_20260622.md).

## Linked Artifacts

- [P27 B-Line Extension Counts And Deep Descent](p27_b_line_extension_and_deep_descent_20260622.md)
- [P27 B-Line Kummer Extraction Packet](p27_b_line_kummer_extraction_packet_20260622.md)
- [P27 GPU Test Decision After Quadratic Probe](p27_gpu_test_decision_after_quad_20260622.md)
- [P27 Full Quartic GPU Suite Handoff](p27_full_quartic_gpu_suite_handoff_20260622.md)
- [P27 Post-Quartic CAS Suite Handoff](p27_post_quartic_cas_suite_handoff_20260622.md)

```text
p27_b_line_deep_prefix_gpu_telemetry_handoff_rows=1/1
```
