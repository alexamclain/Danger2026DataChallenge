# P25 v2 Unified Value / Divisor Theorem Interface

Updated: 2026-06-16

## Purpose

Promote the exact theorem interface for the missing first-pass arithmetic
statement.  The H0/conductor-39 target is fixed; this page says what would
count as a source-stage close, what is only a repair row, and what remains
after source stage.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`
- `evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md`
- `archive/notes/p25_ksy_y_h90_value_theorem_intake_20260614.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_unified_value_divisor_interface_gate.py
```

The gate returned `p25_v2_unified_value_divisor_interface_rows=1/1`.

## Fixed Target

```text
support_period = 156
H90 support = 156
product shape = 78 positive / 78 negative Yang-fiber factors
target rows = 4
support-period root gcd in F_p^* = 1
ambient-period root gcd in F_p^* = 11
```

The support-period value route has unique root behavior over `F_p`; the ambient
period-780 value route keeps a `mu_11` ambiguity.

## Source-Stage Closers

Three theorem shapes would move the frontier:

```text
1. unified divisor/additive theorem
   target = one legal support-156 H0/conductor-39 product
   payload = finite divisor/additive identity with Hilbert-90 boundary
             (1-Frob_p)H = Norm_156(Y_507)
   source = arithmetic theorem
   then missing = DANGER3 framing and extraction

2. unified period-156 value theorem
   target = one legal support-156 H0/conductor-39 product
   payload = finite value identity with period-156 branch/root/telescoping
             context and boundary Norm_156(Y_507)
   source = arithmetic theorem
   then missing = DANGER3 framing and extraction

3. exact-P upstream theorem
   target = compact exact-P C,D,K,orientation or accepted period-156 theta2
            payload
   payload = challenge-legal exact-P theorem feeding the
             75 -> 300 -> 12 -> 312 -> 156 bridge
   then missing = DANGER3 framing and extraction
```

The preferred next ask is the first row: a divisor/additive theorem avoids the
value-branch ambiguity entirely.

## Repair Or Reject Rows

These do not close source stage:

```text
source legality only:
  missing = finite value/divisor theorem

boundary only:
  missing = finite value/divisor identity for the legal product

value without period-156 context:
  missing = support-period branch/root/telescoping data

formal one-coset or projection:
  reject = wrong legality or lost mixed tensor

seed or proper suborbit shortcut:
  reject = not a standalone X_1(39) unit without the full norm or legality repair

finite payload without source:
  missing = challenge-legal arithmetic source theorem
```

## Downstream Boundary

Even after a source-stage theorem:

```text
post-source theorem with no extraction:
  decision = danger3_unblocked_extraction_missing
  missing = same-j X1(8112), practical X1(16), halving/direct x0, vpp.py

official vpp verified triple:
  decision = submission_ready
```

Current rows:

```text
current_source_theorem_rows = 0
current_submission_ready_rows = 0
```

## Verdict

```text
continue_first_pass = yes
preferred_next_ask = finite divisor/additive theorem, or period-156 value
                     theorem, for one legal support-156 H0/conductor-39
                     product with Norm_156(Y_507) boundary
discard_condition = source legality, boundary-only, selector/gauge,
                    seed/suborbit, ambient-value, or finite-payload-only
                    claim that does not add the arithmetic theorem
```
