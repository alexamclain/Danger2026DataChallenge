# P25 v2 Candidate Packet Intake Reorg

Updated: 2026-06-16

## Purpose

Restore and promote the end-to-end candidate-packet intake after the research
wiki reorganization. This is the executable front door for a future theorem or
expert packet that claims to start from one exact H0/conductor-39 product and
continue toward DANGER3 extraction.

This is not a source theorem and not a certificate. It verifies that the
current wiki layout still supports packet checking in the required order:

```text
exact product file
-> source theorem
-> DANGER3 framing
-> same-j X_1(8112) bridge
-> practical X_1(16) payload
-> halving/direct x0
-> official vpp.py
```

## Pages And Files Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_extraction_payload_contract_20260616.md`
- `archive/gates/p25_ksy_y_h0_product_file_claim_intake_gate.py`
- `archive/gates/p25_ksy_y_h0_candidate_packet_intake_gate.py`
- `archive/harness/p25_ksy_y_h0_exact_product_fixture_export.py`
- `archive/fixtures/h0_product_fixtures/`

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_product_file_claim_intake_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_candidate_packet_intake_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_candidate_packet_intake_reorg_gate.py
```

The promoted v2 wrapper returned:

```text
p25_v2_candidate_packet_intake_reorg_rows=1/1
```

## Reorg Repair

The old product-file intake imported the fixture exporter from the pre-wiki
layout. After the reorganization, the exporter lives under `archive/harness`
and the byte-stable product fixtures belong under `archive/fixtures`.

The repair:

```text
archive/harness/p25_ksy_y_h0_exact_product_fixture_export.py
  fixture_dir = archive/fixtures/h0_product_fixtures
  command snippets use archive/gates + archive/harness import paths

archive/gates/p25_ksy_y_h0_product_file_claim_intake_gate.py
  imports archive/harness explicitly
```

The wrapper verifies that no duplicate fixture directory remains under
`archive/harness`.

## Verified Layout

```text
fixture_export_ok = 1
product_file_intake_ok = 1
candidate_packet_intake_ok = 1
fixture_dir_is_archived = 1
fixture_files_present = 6/6
duplicate_harness_fixture_dir_absent = 1
```

## Packet Intake Counts

The exact-product file intake remains live:

```text
product_file_source_closing_rows = 3
product_file_submission_ready_control_rows = 1
```

The full candidate-packet intake remains stricter:

```text
candidate_packet_source_stage_closed_rows = 8
candidate_packet_cross_level_bridge_rows = 5
candidate_packet_x16_surface_rows = 2
candidate_packet_partial_chain_rows = 1
candidate_packet_extraction_ready_rows = 1
candidate_packet_vpp_executed_rows = 1
candidate_packet_submission_ready_rows = 0
current_real_submission_ready_rows = 0
```

The product-file `submission_ready` row is only a regression control where all
downstream flags are artificially supplied. The end-to-end candidate-packet
gate has zero submission-ready current packets.

## Verdict

```text
decision = candidate_packet_intake_restored_current_submissions_zero
continue = yes, use this for future theorem/expert packets
current_source_theorem = no
current_submission = no
```

Future claimed progress should be packetized through this intake when it
contains concrete product files, bridge claims, `X_1(16)` chart data,
halving-chain data, direct `(A,x0)`, or a `vpp.py` verification claim. A packet
that stalls at source theorem, same-j bridge, chart payload, partial chain, or
unverified direct `x0` should remain repair/progress, not a p25 submission.
