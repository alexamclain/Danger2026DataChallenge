# P25 Lane B: Robert KSY Kubert-Lang Theorem-Hit Router

Updated: 2026-06-13 18:28 PDT

## Purpose

The raw KL/KSY target now has several valid-looking output types.  This gate is
the single executable landing pad for a theorem or literature hit before it is
accepted or killed.

## Accepted Output Types

```text
finite spine payload
  accepted by the older universal finite intake
  still needs an arithmetic source

raw divisor/additive product
  exact raw C/D/primitive-K/orientation routes directly to theta2/theta2^-1
  then through the support-period certificate path

raw finite-field value product
  accepted only when the theorem also supplies period-156 theta2 context
```

For the accepted raw product:

```text
C=(47,28), D=(22,3), primitive K multiplier 1, forward
  -> theta2 inverse, recovered bridge sign -1
```

The same candidate is accepted as a value-level hit only with the
period-156 fixedness/telescoping obligation attached.

## Rejected Or Conditional Types

```text
ambient 780-period value only
  rejected because the F_p^* route has mu_11 ambiguity

wrong raw center/D/nonprimitive K
  rejected because it emits neither theta2 nor theta2 inverse

raw Kubert-Lang exponent balance only
  rejected because exponent sums are saturated by wrong packets

generic Robert/Siegel/KSY source-family claim
  not accepted until instantiated as exact C/D/K payload or stronger data
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_theorem_hit_router_rows=1/1
```

Candidate examples:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type raw-divisor \
  --center-right 47 --center-c 28 \
  --d-right 22 --d-c 3 \
  --k-multiplier 1

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py \
  --output-type raw-value \
  --center-right 47 --center-c 28 \
  --d-right 22 --d-c 3 \
  --k-multiplier 1 \
  --period-156-context
```

## Interpretation

This does not prove the missing arithmetic producer.  It prevents the next
theorem hit from being judged by the wrong interface: divisor/additive data,
finite values, finite-spine payloads, and broad source-family claims now route
through different obligations.
