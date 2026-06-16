# P25 KSY-y Siegel-Robert Period-Value Scout

Updated: 2026-06-13 20:56 PDT

## Sources Inspected

Schertz, `Construction of Ray class fields by elliptic units`:
<https://eudml.org/doc/248002>.

Shin, `Generation of class fields by Siegel-Ramachandra invariants`:
<https://arxiv.org/abs/1009.2253>.

Primary clauses checked:

```text
Schertz: elliptic-unit / Klein-form quotient generators for ray class fields
Shin: Siegel-Ramachandra invariants as primitive class-field generators
local period-value classifier: support period 156 versus ambient period 780
```

## Result

The value-unit route remains live, but the inspected source handles do not close
the p25 moonshot.

Matched clauses:

```text
elliptic units / Klein-form quotients are class-field generator vocabulary
Siegel-Ramachandra invariants are class-field generator vocabulary
support-period value context would remove the F_p^* root ambiguity
```

First missing clause:

```text
exact finite-field value identity for P, preserving the mixed graph, with
period-156 branch/root/telescoping context
```

## Local Classification

```text
schertz_klein_quotient_generator:
  value decision  = reject_field_generation_not_value_theorem
  source decision = reject_not_closure_theorem

shin_siegel_ramachandra_generator:
  value decision  = reject_field_generation_not_value_theorem
  source decision = reject_not_closure_theorem

siegel_robert_bare_exact_value:
  value decision  = conditional_missing_period_156_context
  source decision = conditional_missing_period_156_context

siegel_robert_ambient_780_value:
  value decision  = reject_ambient_780_mu11_branch
  source decision = reject_not_closure_theorem

siegel_robert_exact_value_with_period_hypothetical:
  value decision  = closing_value_identity_with_period_156
  source decision = closing_value_identity_with_period_156
```

Denominator facts:

```text
support period                  = 156
gcd(4^156 - 1, p - 1)           = 1
ambient period                  = 780
gcd(4^780 - 1, p - 1)           = 11
ambient F_p value branches      = 11
```

Local gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_siegel_robert_period_value_primary_source_scout_gate.py
```

Boundary probes:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name schertz_klein_quotient_generator \
  --anchor siegel_robert_value_units --output-kind field-generation

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name siegel_robert_bare_exact_value \
  --anchor siegel_robert_value_units --output-kind value \
  --exact-product --mixed-graph --finite-field

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name siegel_robert_exact_value_with_period_hypothetical \
  --anchor siegel_robert_value_units --output-kind value \
  --exact-product --mixed-graph --finite-field --period-156
```

## Continue / Kill

Continue Siegel-Robert / Siegel-Ramachandra only for an exact finite-field value
identity for the p25 product `P` with the mixed graph and period-`156` context.

Kill class-field generation alone, generic invariant language, and ambient
period-`780` values as direct closers.  They remain useful only as vocabulary or
as possible source scaffolding for the exact value theorem.

## Completed Gate

```text
direct_closing_rows       = 0
conditional_rows          = 1
rejected_rows             = 3
hypothetical_closing_rows = 1
```

Marker:

```text
ksy_y_siegel_robert_period_value_primary_source_scout_rows=1/1
```
