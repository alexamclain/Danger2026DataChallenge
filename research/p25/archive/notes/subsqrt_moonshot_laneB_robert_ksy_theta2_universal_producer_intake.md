# P25 Lane B: Robert KSY/Hilbert-90 Universal Producer Intake

Updated: 2026-06-13 15:44 PDT

## Purpose

The arithmetic-producer contract defines which finite payloads are meaningful
targets. This harness gives those payloads one command-line front door while
delegating the actual checks to the existing specialized gates.

It is still a finite verifier, not the missing arithmetic producer.

## Supported Candidate Modes

```text
hilbert90-signs
source-packet
quotient-factor
source-factor
compact-theta2
theta2-sparse
```

No-argument mode runs the current positive and negative controls across all
interfaces.

## Positive Controls

```text
hilbert90-signs           ok
source-packet             ok
quotient-factor           ok
source-factor             ok
compact-theta2-inverse    ok
compact-theta2            ok
theta2-sparse             ok
theta2-inverse-sparse     ok
```

## Rejected Controls

```text
invalid-hilbert90-signs       rejected
q-cycle-as-source-packet      rejected
nonprimitive-k-source-packet  rejected
wrong-d-quotient-factor       rejected
collapsed-k-source-factor     rejected
plain-bridge-as-theta2        rejected
wrong-compact-theta2          rejected
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py
```

Expected marker:

```text
robert_ksy_theta2_universal_producer_intake_rows=1/1
```

Candidate smoke test:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py \
  --mode hilbert90-signs --eps 1 --branch -1
```

Expected marker:

```text
robert_ksy_theta2_universal_producer_intake_candidate_rows=1/1
```

## Interpretation

Future theorem or literature hits can now be routed through one harness. A
passing candidate means the finite payload matches an accepted spine interface;
it does not by itself prove the arithmetic origin of the payload.
