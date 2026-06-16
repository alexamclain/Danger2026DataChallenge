# P25 Lane B: theta2 Source-Quotient Packet Harness

Updated: 2026-06-13 15:23 PDT

## Purpose

The quotient-factor harness accepts the factorized quotient data

```text
base=(1,25), D=(1,3), T=(2,113)
```

in `(C_75/K) x C_169`.  This harness accepts the equivalent six-cell source
quotient packet directly:

```text
base * (1 + D + D^2) * (1 - T)
```

and lifts it through a primitive 25-point `K` trace to the existing raw bridge
contract.

## Accepted Packet

```text
1 25   1
2 28   1
0 31   1
0 138 -1
1 141 -1
2 144 -1
```

This is a source quotient packet in `(right mod 3, c)` coordinates.  It is not
the older normalized `q`-cycle quotient packet.

## Result

```text
packet support                         = 6
packet coefficient counts              = (-1,3), (1,3)
primitive K lift support               = 150
bridge contract after lift             = true
primitive K multiplier 2 passes         = true
nonprimitive K multiplier 5 fails       = true
positive-only packet fails              = true
wrong c packet fails                    = true
q-cycle convention packet fails         = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_source_quotient_packet_harness.py
```

Expected marker:

```text
robert_ksy_theta2_source_quotient_packet_harness_rows=1/1
```

## Candidate Mode

Positive target:

```sh
printf '1 25 1\n2 28 1\n0 31 1\n0 138 -1\n1 141 -1\n2 144 -1\n' \
  >/tmp/p25_source_quotient_packet.txt

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_source_quotient_packet_harness.py \
  --packet /tmp/p25_source_quotient_packet.txt \
  --k-multiplier 1
```

Expected marker:

```text
robert_ksy_theta2_source_quotient_packet_candidate_rows=1/1
```

## Interpretation

This is the smallest direct finite payload target for the KSY/theta lane:
six source-quotient cells plus a primitive `K` multiplier.  It is useful for
theorem or literature hits that emit a divisor packet rather than the
factorized `base,D,T` word.

The arithmetic producer debt remains unchanged: this harness verifies a finite
payload, not the theorem that produces it.
