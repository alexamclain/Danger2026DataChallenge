# P25 Lane B: KSY-y Submission Extraction

Updated: 2026-06-13 20:21 PDT

## Purpose

The finite KSY/theta gates now accept several sub-sqrt payload interfaces, but
DANGER3 still has a concrete final surface: a Pomerance triple `(p,A,x0)`
verified by `vpp.py` / `lean_vpp.py`.  This gate records the extraction
boundary so that a theorem hit is not confused with a submission.

## States

```text
finite payload only:
  local universal intake accepts the payload
  missing = challenge-legal arithmetic source theorem

source theorem:
  exact product/value theorem emits the finite identity
  missing = DANGER3 policy framing or A,x0 extraction

policy-unblocked theorem:
  finite identity is accepted as challenge-legal framing
  missing = concrete A,x0 derivation or accepted submission framing

extraction algorithm:
  theorem claims a way to derive A,x0
  missing = actual output and official vpp.py verification

concrete triple:
  closes only if vpp.py verifies
```

## Completed Gate

```text
dependency gates:
  universal finite intake      = pass
  arithmetic producer contract = pass
  DANGER3 framing              = pass

vpp regression:
  known p24 triple             = True
  p24 x0+1 control             = rejected

regression rows:
  finite_live_rows             = 5
  source_closed_rows           = 4
  submission_ready_rows        = 1
  conditional_rows             = 4
  rejected_rows                = 1
```

Local audit gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py
```

Concrete triple candidate mode:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py \
  --p P --A A --x0 X0
```

Marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_rows=1/1
robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_candidate_rows=1/1
```

## Consequence

The moonshot route is now staged cleanly:

1. finite payload passes universal intake;
2. source theorem proves the exact product/value identity;
3. DANGER3 policy or non-CM finite-field framing is resolved;
4. an extraction step produces concrete `(A,x0)`;
5. official `vpp.py` verifies the triple and Lean certificate generation can
   proceed.

Anything before step 5 is useful progress, but not a p25 submission.
