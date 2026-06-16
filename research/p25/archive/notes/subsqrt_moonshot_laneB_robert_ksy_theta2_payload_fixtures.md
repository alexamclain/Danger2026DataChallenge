# P25 Lane B: Robert KSY/Hilbert-90 Payload Fixtures

Updated: 2026-06-13 15:48 PDT

## Purpose

The universal producer intake now has stable file fixtures for the file-based
payload modes. These fixtures make future theorem or literature hits
byte-comparable against the accepted finite targets and the most important
near misses.

The fixtures are finite targets, not arithmetic producer proofs.

## Fixture Directory

```text
research/p25/producer_payload_fixtures
```

## Export Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_payload_fixture_export.py
```

Expected marker:

```text
robert_ksy_theta2_payload_fixture_export_rows=1/1
```

## Files

```text
source_packet_target.txt                  6 lines
source_packet_q_cycle_reject.txt          6 lines
theta2_sparse_target.txt                300 lines
theta2_inverse_sparse_target.txt        300 lines
theta2_sparse_plain_bridge_reject.txt   150 lines
universal_intake_commands.sh             17 lines
```

SHA-256:

```text
88944523b09ff57b3cbe702bd6fddaeaf5be96788d954f908091abe450b74a2d  source_packet_target.txt
1bd718e67698e38a409c09fedc00592bd6ce6e53852c59216e0757a6a662c820  source_packet_q_cycle_reject.txt
e43bffeb899fcfe36525212ce23014fa0dc782466f8984c9bd16c4a73887686d  theta2_sparse_target.txt
1c367e6fd1875436151c583634add0dc4544cb6f14ceef6849929002ced45ac1  theta2_inverse_sparse_target.txt
2951a0fb2d7cd5c1577f97baac0052ef2113fc4dc2754f993c62d663c63f809f  theta2_sparse_plain_bridge_reject.txt
af99ee02104210ccc4f4eed7ee9151b394c2542f63096419709fa60838e42159  universal_intake_commands.sh
```

## Verified Commands

Source packet:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode source-packet \
  --packet research/p25/producer_payload_fixtures/source_packet_target.txt \
  --k-multiplier 1
```

Theta2 sparse:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode theta2-sparse \
  --sparse-source research/p25/producer_payload_fixtures/theta2_sparse_target.txt
```

Both produce:

```text
robert_ksy_theta2_universal_producer_intake_candidate_rows=1/1
```

## Interpretation

A theorem hit can now be reduced to one of these comparisons:

```text
sign data       -> command arguments
source packet   -> source_packet_target.txt
theta2 divisor  -> theta2_sparse_target.txt
theta2 inverse  -> theta2_inverse_sparse_target.txt
```

Near misses should fail against the reject fixtures before any further theory
time is spent on them.
