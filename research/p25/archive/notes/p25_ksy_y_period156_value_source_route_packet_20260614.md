# P25 KSY-y Period-156 Value Source-Route Packet

Updated: 2026-06-14 13:13 PDT

## Purpose

The active value-side moonshot target is not a generic class-field value.  It
is:

```text
exact finite-field value identity for P
mixed C_75 x C_169 graph preserved
period-156 branch/root/telescoping context
```

This packet makes that source route executable and keeps it separate from
DANGER3 extraction.

## Denominators

```text
support period                    = 156
gcd(4^156 - 1, p - 1)             = 1

ambient period                    = 780
gcd(4^780 - 1, p - 1)             = 11
```

So the support-period value route has a unique `F_p^*` root, while the ambient
period-`780` route has an unresolved `mu_11` branch ambiguity.

## Local Rows

### Exact P Value With Period 156

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name source_exact_p_value_with_period156 \
  --anchor siegel_robert_value_units --output-kind value \
  --exact-product --mixed-graph --finite-field-identity --period-156
```

Expected:

```text
decision = closing_value_identity_with_period_156
```

### Raw Value Theorem With Period 156

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type raw-value \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1 --period-156-context
```

Expected:

```text
decision = accept
```

### Bare Exact Value

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name bare_exact_value_without_period156 \
  --anchor siegel_robert_value_units --output-kind value \
  --exact-product --mixed-graph --finite-field-identity
```

Expected:

```text
decision = conditional_missing_period_156_context
```

### Period Context Without Exact P

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py \
  --candidate --name period156_context_without_exact_p \
  --anchor siegel_robert_value_units --output-kind value \
  --mixed-graph --finite-field-identity --period-156
```

Expected:

```text
decision = conditional_missing_exact_product
```

### Ambient 780 Value

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type ambient-value \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1
```

Expected:

```text
decision = reject
missing  = ambient 780-period value route has mu_11 ambiguity
```

## Downstream

Even a closing period-`156` value theorem remains upstream of DANGER3
submission.  It still needs:

```text
DANGER3 finite-identity/non-CM framing
cross-level X_1(8112) / X_1(16) extraction
halving chain or direct x0
official vpp.py verification
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_period156_value_source_route_packet_gate.py
```

Marker:

```text
ksy_y_period156_value_source_route_packet_rows=1/1
```
