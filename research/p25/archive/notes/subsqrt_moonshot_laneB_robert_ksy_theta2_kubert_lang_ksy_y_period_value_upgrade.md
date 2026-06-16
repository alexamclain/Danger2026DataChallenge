# P25 Lane B: KSY-y Period-Value Upgrade

Updated: 2026-06-13 19:49 PDT

## Purpose

Make the value-route scout contract sharper.  Period-`156` context is required
for a finite-field value theorem, but it does not replace the exact product
`P`, the mixed `C_75 x C_169` graph, or an arithmetic producer theorem.

## Denominator Facts

```text
support period                         = 156
gcd(4^156 - 1, p - 1)                  = 1
ambient period                         = 780
gcd(4^780 - 1, p - 1)                  = 11
ambient F_p value branches             = 11
```

Thus a value theorem that lands on the support-period object has a unique
`F_p^*` root.  A value theorem that only lives on the ambient period-`780`
orbit still has the `mu_11` branch ambiguity.

## Upgrade Table

```text
closing:
  KSY exact value identity for P with mixed graph and period-156 context
  Siegel-Robert exact value identity for P with mixed graph and period-156 context

conditional:
  exact value of P without period-156 context
  period-156 context without exact P
  finite verifier payload without arithmetic producer theorem

rejected:
  ambient 780 value-only claim
  generic KSY ray-class generation
```

## P24 Transfer Lesson

The p24 handoff says the same thing in different coordinates: small verifier
surfaces and broad CM/Lang generation do not close the certificate without an
embedded branch/root-selected producer theorem.  For p25, that means a
value-source hit must emit exact `P`, preserve the mixed graph, prove a
finite-field identity, and carry period-`156` context.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_rows=1/1
```
