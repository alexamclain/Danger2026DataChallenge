# P25 Lane B: Hilbert-90 to KSY Packet Adapter

Updated: 2026-06-13 15:27 PDT

## Purpose

The Hilbert-90 lane has a two-sign finite target.  The KSY/theta lane now has
a six-cell source-quotient packet target.  This adapter records that they are
the same bridge payload in two coordinate systems.

For a Hilbert-90 quotient bridge point `q`, the source quotient coordinate is:

```text
(right mod 3, c) = (q mod 3, q mod 169)
```

## Result

All four active Hilbert-90 sign pairs

```text
eps, branch in {(-1,-1), (-1,+1), (+1,-1), (+1,+1)}
```

emit the same q-cycle bridge:

```text
q-cycle coordinates:
  (0, 46)  -1
  (0, 123) +1
  (1, 47)  -1
  (1, 121) +1
  (2, 48)  -1
  (2, 122) +1
```

Converting by `(q mod 3, q mod 169)` gives the KSY source-quotient packet:

```text
source quotient coordinates:
  (0, 31)  +1
  (0, 138) -1
  (1, 25)  +1
  (1, 141) -1
  (2, 28)  +1
  (2, 144) -1
```

The converted packet passes the source-quotient packet harness and lifts
through the primitive `K` trace to the existing bridge contract.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_hilbert90_packet_adapter_gate.py
```

Expected marker:

```text
robert_ksy_theta2_hilbert90_packet_adapter_rows=1/1
```

## Interpretation

A theorem hit in the Hilbert-90 form can still be consumed by the KSY/theta
packet verifier:

```text
two signs -> q-cycle bridge -> source quotient packet -> K trace lift -> bridge contract
```

This is a coordinate adapter between finite contracts.  It does not prove the
missing arithmetic producer.
