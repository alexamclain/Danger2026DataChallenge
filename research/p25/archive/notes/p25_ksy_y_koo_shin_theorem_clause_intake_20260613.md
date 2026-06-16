# P25 KSY-y Koo-Shin Theorem-Clause Intake

Updated: 2026-06-13 22:12 PDT

## Purpose

This is the drop point for a future full-text/OCR/subagent result on Koo-Shin
2010 Theorem 5.2.  The key is to classify what the theorem actually emits
before treating it as a p25 source theorem.

## Intake Rules

```text
reject:
  snippet only / no theorem body
  modularity or exponent-congruence hygiene only
  odd-prime or C169 prime-power product with no mixed-level lift
  exact product missing the mixed C_3 x C_169 graph
  nonuniform or missing atom weights

conditional:
  exact P but missing theta2/theta2-inverse orientation
  exact finite payload but no arithmetic producer theorem
  exact source theorem but DANGER3/non-CM framing missing
  DANGER3-unblocked theorem but no A,x0 extraction

source-theorem closed:
  exact P, mixed graph, equal weights, orientation, arithmetic producer,
  and divisor/additive output

value-source closed:
  exact P as finite-field value identity, mixed graph, equal weights,
  orientation, arithmetic producer, and period-156 context

submission ready:
  concrete p25 (p,A,x0) passing official vpp.py
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_theorem_clause_intake_gate.py
```

```text
theorem_body_rows          = 9
hygiene_only_rows          = 1
prime_power_only_rows      = 1
exact_p_rows               = 8
mixed_graph_rows           = 7
source_theorem_closed_rows = 4
danger3_unblocked_rows     = 3
extraction_ready_rows      = 2
submission_ready_rows      = 1
rejected_rows              = 3
conditional_rows           = 6
```

Markers:

```text
ksy_y_koo_shin_theorem_clause_intake_rows=1/1
ksy_y_koo_shin_theorem_clause_intake_candidate_rows=1/1
```

## Candidate Examples

Reject a prime-power-only near miss:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_theorem_clause_intake_gate.py \
  --candidate --name c169_only --theorem-body --product-distribution \
  --prime-power-only --exact-p --equal-weight --orientation \
  --arithmetic-producer
```

Accept a full theorem as ready for extraction:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_theorem_clause_intake_gate.py \
  --candidate --name full_theorem_ready --theorem-body \
  --product-distribution --mixed-level-lift --exact-p --mixed-graph \
  --equal-weight --orientation --arithmetic-producer --finite-identity \
  --danger3-framing --extraction
```

## Verdict

This makes the Koo-Shin lead easier to use without overpromoting it.  A future
Theorem 5.2 text is useful only if it survives the mixed-level p25 clauses:
exact `P`, mixed graph, equal weights, orientation, and arithmetic producer.
Otherwise it remains context, hygiene, or a near miss.
