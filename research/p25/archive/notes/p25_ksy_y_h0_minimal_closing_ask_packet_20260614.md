# P25 KSY-y H0 Minimal Closing Ask Packet

Updated: 2026-06-14 16:13 PDT

## Purpose

This is the compact Drew/source-matching packet for the current H0 lane.  It
amortizes the Koo-Shin 6.2 screen, exact H0 product targets, boundary/value
ambiguity gate, and final `X_1(16)` certificate boundary into the smallest set
of questions that can still move the moonshot.

## Target Family

```text
exact_product_targets        = 4
canonical_targets            = 1
H0_translate_targets         = 3
all_exact_targets_78_over_78 = yes
support_period               = 156
ambient_period               = 780
gcd(4^156 - 1, p - 1)        = 1
gcd(4^780 - 1, p - 1)        = 11
```

Koo-Shin 6.2 now certifies these four exact H0 products as legal
conductor-39 source words.  That is real progress, but it is still source
certification only.

## Minimal Positive Asks

```text
ask_value_period156_identity:
  ask     = exact finite-field value of one exact legal H0 product
  require = support-period-156 branch/root/telescoping context
  result  = source theorem closed; route to DANGER3 framing and extraction

ask_divisor_additive_identity:
  ask     = exact divisor/additive identity for one exact legal H0 product
  require = Hilbert-90 boundary to Norm_156(Y_507)
  result  = source theorem closed; route to DANGER3 framing and extraction
```

## Downstream After A Yes

```text
same-j extraction:
  need = X_1(8112) bridge tied through the same j-invariant to X_1(16)
  emit = X_1(16) y/x/A/xP16, or direct A,x0

official boundary:
  need = official vpp.py verification of concrete p25 (p,A,x0)
  reject = internal verifier, branch word, x-chain, or direct x0 without vpp.py
```

## Falsifiers

```text
Koo-Shin 6.2 legality only:
  decision = source_certified_value_or_divisor_missing

bare or ambient-period-780 value:
  decision = conditional_missing_period_156_context
  reason   = ambient period 780 leaves 11 F_p^* branches

computed payload without source theorem:
  decision = conditional_finite_payload_without_source_theorem

odd-level theorem without same-j X1 bridge:
  decision = downstream_cross_level_extraction_required
```

## Counts

```text
row_count                        = 7
source_closing_yes_rows          = 2
source_certified_only_rows       = 1
downstream_followup_rows         = 2
reject_or_conditional_rows       = 2
final_submission_boundary_rows   = 1
current_submission_ready_rows    = 0
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_minimal_closing_ask_packet_gate.py
```

Marker:

```text
ksy_y_h0_minimal_closing_ask_packet_rows=1/1
```
