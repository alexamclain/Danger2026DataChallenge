# P25 Lane B: KSY-y DANGER3 Framing

Updated: 2026-06-13 19:58 PDT

## Purpose

Separate the final DANGER3 submission surface from the moonshot producer
theorem surface.

The current upstream DANGER3 README defines the accepted object as a concrete
Pomerance triple `(p,A,x0)`, and `vpp.py` verifies such triples.  The KSY-y
moonshot gates are producer machinery that might derive a triple; they are not
the final submission by themselves.

## Upstream Check

```text
remote HEAD checked = a65658b7b194546957fa62f40d60ca63efc37f93
target              = p = 10^25 + 13
official surface    = concrete (p,A,x0) verified by vpp.py / lean_vpp.py
README no-CM ban observed = true
```

## Framing Counts

```text
submission-ready rows              = 1
policy-unblocked non-submissions   = 2
policy-only rows                   = 1
conditional rows                   = 2
rejected rows                      = 2
```

Interpretation:

```text
verified (p,A,x0) triple:
  closes the final DANGER3 submission surface

exact product/value theorem + policy yes:
  unblocks the theorem route, but still must derive A,x0 and pass vpp.py

policy yes without theorem:
  not a theorem and not a submission

generic CM/Lang provenance without finite identity:
  rejected for this framing
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_rows=1/1
```

## Interpretation

For conversations with Drew, the question is now precise:

```text
If we prove a finite-field identity for the exact P product, is that accepted
as a challenge-legal producer route, provided the final output is still a
concrete vpp-verified (p,A,x0) triple?
```

Even if the answer is yes, the moonshot still needs the exact product or
value-with-period theorem and a derivation of the final triple.
