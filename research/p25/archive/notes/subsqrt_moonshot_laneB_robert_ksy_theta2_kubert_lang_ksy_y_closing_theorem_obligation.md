# P25 Lane B: KSY-y Closing-Theorem Obligation

Updated: 2026-06-13 20:23 PDT

## Purpose

The local gates now make every intermediate boundary explicit.  This note
compresses them into one theorem-facing contract: what a source theorem must
say before the KSY-y moonshot is genuinely closed on the theory side, and what
still remains before DANGER3 submission.

## Minimal Theorem Contract

The live exact product is:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28)
D = (22,3)
K = (57,0)
y(Q) = -g(2Q)/g(Q)^4
```

Equivalent quotient anchor:

```text
C = (2,28)
D = (1,3)
T = -2C = (2,113)
T/2 = -C = (1,141)
```

A source theorem must provide all of:

```text
exact P
mixed C_3 x C_169 row graph or reflection-center payload
equal weights on all 75 K-traced atoms
theta2/theta2-inverse orientation branch
challenge-legal arithmetic source theorem
divisor/additive product identity
```

For a value theorem, replace the last line by:

```text
finite-field value identity for exact P
period-156 fixedness / branch / telescoping context
```

because the ambient period-780 route still has value-branch ambiguity.

## Staging

```text
finite verifier payload:
  useful but not a source theorem

source theorem closed:
  exact P + mixed graph + equal weights + orientation + arithmetic theorem

DANGER3 route unblocked:
  source theorem plus finite-identity/non-CM framing or policy acceptance

ready to extract:
  DANGER3 route plus A,x0 extraction algorithm

submission ready:
  concrete (p,A,x0) passes official vpp.py
```

## Completed Gate

```text
source_theorem_closed_rows = 4
danger3_unblocked_rows     = 3
extraction_ready_rows      = 2
submission_ready_rows      = 1
conditional_rows           = 5
rejected_rows              = 2
```

Local gate:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py
```

Candidate examples:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name c169_projection --source-family Kubert-Lang \
  --exact-p --equal-weight --orientation --output-kind divisor-additive

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py \
  --candidate --name full_theorem_ready --source-family KSY-KL \
  --exact-p --mixed-graph --equal-weight --orientation --arithmetic-source \
  --output-kind divisor-additive --finite-identity --danger3-framing --extraction
```

Markers:

```text
robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_candidate_rows=1/1
```

## Consequence

The remaining moonshot is now sharply phrased:

- Find or prove the exact arithmetic source theorem for `P`.
- Resolve DANGER3 finite-identity/non-CM framing if the theorem does not
  directly emit a concrete triple.
- Derive `(A,x0)` and verify it with official `vpp.py`.

Anything weaker is an intermediate payload, not the moonshot finish line.
