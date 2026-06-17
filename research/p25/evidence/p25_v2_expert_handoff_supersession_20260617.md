# P25 v2 Expert Handoff Supersession

Updated: 2026-06-17

Marker: `p25_v2_expert_handoff_supersession_rows=1/1`

## Purpose

Make the expert/source-feedback reading path unambiguous after the current
theorem kernel and Drew kernel review packet were promoted.

The older minimal expert ask and first-pass expert intake packet remain useful
provenance. They are no longer the first page to hand to Drew or to use as the
current yes/no classifier, because they predate the fully expanded
unique-power set and the exact-P 75-atom separation.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_first_pass_expert_intake_packet_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_expert_handoff_supersession_gate.py
```

The gate returned `p25_v2_expert_handoff_supersession_rows=1/1`.

## Supersession Rule

```text
current expert-facing packet:
  evidence/p25_v2_drew_kernel_review_packet_20260617.md

current theorem kernel:
  evidence/p25_v2_current_theorem_kernel_20260617.md

supporting provenance:
  evidence/p25_v2_minimal_expert_ask_20260616.md
  evidence/p25_v2_first_pass_expert_intake_packet_20260616.md
```

The current handoff rows are:

```text
scalar_fixed_row_theorem
row_labeled_unique_power, e in {3,5,13,39,75,169,507}
support_period156_value
```

Support/heavy rows are:

```text
Q/Yang/H90 support until selector and finite theorem debt are paid
exact-P/theta2 heavy upstream through 75->300->12->312->156
reverse unified -> exact-P rejected without extra selector structure
```

## Canonical Page Changes

```text
frontier.md:
  minimal expert ask = supporting predecessor context
  first-pass expert intake packet = supporting classifier provenance
  Drew kernel review packet = current expert-facing handoff

lanes/h0.md:
  H0 expert replies route through the Drew kernel review packet before lane
  status changes

lanes/conductor39.md:
  conductor-39 expert replies route through the Drew kernel review packet
  before lane status changes

lanes/exact-p.md:
  Drew packet names the exact-P expert boundary and separates row-power R_m^75
  from exact-P 75 atoms
```

## Counts

```text
evidence_markers_ok = 4/4
stale_preferred_count = 0
current_handoff_rows_present = 1
p25_v2_expert_handoff_supersession_rows=1/1
```

## Verdict

The expert/source-feedback path should now start from the current theorem
kernel and Drew kernel review packet. The older minimal expert ask and
first-pass intake packet are supporting provenance, not the current handoff.
