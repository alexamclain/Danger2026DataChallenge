# P25 KSY-y Conductor-39 Value-Theorem Source-Route Packet

Updated: 2026-06-14 12:43 PDT

## Purpose

The value-theorem target packet names four theorem targets.  This note gives
the source-route packet: allowed source families, first falsifier, and local
candidate command for each target.

Every successful route here is expected to stop at:

```text
source_theorem_closed_policy_or_framing_missing
```

because DANGER3 framing and extraction remain downstream.

## Routes

### U_chi Value Or Divisor

Target:

```text
conductor39_U_chi_value_or_divisor
```

Accepted source families:

```text
Yang/Yu X_1(39) modular-unit identity
Hilbert-90 or twisted-trace descent for U_chi
finite-field identity reframing of a CM/unit theorem
```

First falsifier:

```text
source product legality, ray-class generation, projection, or formal unit
vocabulary without finite-field value/divisor identity
```

Candidate command:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py \
  --candidate --name U_chi_value_theorem_hit \
  --source-object U_chi --output-kind divisor-additive \
  --theorem-body --emits-conductor39 --mixed-tensor --legal-unit \
  --yang-lift --descent --finite-or-divisor --period-156
```

### W / Norm156(Y507)

Target:

```text
period_norm_W_or_Norm156_Y507
```

Accepted source families:

```text
Yang 13-fiber distribution identity
period-norm value/divisor theorem for Y_507
conductor-39 W=6*U_chi theorem with period-156 context
```

First falsifier:

```text
level-507 statement without conductor-39 descent, Yang lift, or period-156
branch/telescoping context
```

Candidate command:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py \
  --candidate --name W_value_theorem_hit \
  --source-object W --output-kind divisor-additive \
  --theorem-body --emits-conductor39 --mixed-tensor --legal-unit \
  --yang-lift --descent --finite-or-divisor --period-156
```

### Canonical H0

Target:

```text
canonical_H0_or_translate
```

Accepted source families:

```text
Hilbert-90 ratio identity
legal sparse Yang-fiber product theorem
finite-field divisor/additive identity for H0 or a <2>-translate
```

First falsifier:

```text
formal one-coset H, missing (1-Frob_p) boundary, or ambient-period value
```

Candidate command:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py \
  --candidate --name canonical_H0_value_theorem_hit \
  --target-object canonical_H0 --output-kind divisor-additive \
  --theorem-body --exact-target --bridge-spine --legal-yang-h90 \
  --boundary-context --finite-or-divisor --period-156 --arithmetic-source
```

### Exact P Or Y507

Target:

```text
exact_P_or_Y507_bridge_identity
```

Accepted source families:

```text
KSY normalized-y exact product/distribution theorem
Kubert-Lang exact mixed row-labeled product
finite-field value identity for Y_507 with 75->300->12 bridge
```

First falsifier:

```text
formula language, field generation, C169 projection, wrong C/D/K geometry, or
value theorem without period-156 context
```

Candidate command:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py \
  --candidate --name Y_507_value_theorem_hit \
  --target-object Y_507 --output-kind value \
  --theorem-body --exact-target --bridge-spine --legal-yang-h90 \
  --boundary-context --finite-or-divisor --period-156 --arithmetic-source
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_value_theorem_source_route_packet_gate.py
```

Marker:

```text
ksy_y_conductor39_value_theorem_source_route_packet_rows=1/1
```
