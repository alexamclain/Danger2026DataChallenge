# P25 v2 Exact-P Theorem Interface Contract

Updated: 2026-06-16

## Purpose

Promote the exact-P finite contract that was still buried in archived Lane B
gates: what a source theorem must emit, which equivalent finite interfaces are
accepted, and which tempting shortcuts are now falsified.

This is not the missing arithmetic producer. It is the compact target an
arithmetic producer must hit.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md`
- `archive/notes/subsqrt_moonshot_laneB_robert_ksy_theta2_product_certificate_chain.md`
- `archive/notes/subsqrt_moonshot_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity.md`

## Commands

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_product_certificate_chain_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py
```

All six gates returned their expected `rows=1/1` markers.

## Compact Finite Target

The anti-invariant exact-P target can be named by the compact packet:

```text
raw center C = (47, 28)
raw D        = (22, 3)
raw K        = (57, 0), primitive modulo 25
raw base     = C - D = (25, 25)
raw T        = -2*C + K = (38, 113)

quotient center = (2, 28) in C_3 x C_169
quotient D      = (1, 3)
quotient base   = (1, 25)
quotient T      = -2*C = (2, 113)
quotient T/2    = (1, 141) = -C
```

The finite target accepts the exact equal-weight `K`-traced
anti-invariant normalized-y product. Raw Kubert-Lang exponent balance alone is
not a selector.

## Accepted Equivalent Interfaces

The arithmetic producer contract accepts these finite interfaces once a theorem
emits them as genuine arithmetic objects:

```text
Hilbert-90 two signs
six signed source cells on C_3 x C_169 plus primitive K
quotient factor classes: base, D, T plus primitive K
source factor tuple: base * K_trace * D_segment * (1 - T), budget 31
sparse theta2 divisor/additive payload, 300 terms
sparse theta2^-1 divisor/additive payload, 300 terms
compact KSY theta2 certificate skeleton, 975 cells
```

The product-to-certificate chain is verified:

```text
forward y(A)/y(A+T)  -> theta2^-1 -> recovers -bridge
reverse y(A+T)/y(A)  -> theta2    -> recovers  bridge
theta2 payload support = 300
bridge support = 150
support-period resolvent budget = 46800 terms
support-period resolvent union = 11700 cells
compact telescoping certificate budget = 975 cells
```

## Selector Rigidity

Scanning all `507 * 507 = 257049` center/D pairs in `C_3 x C_169` leaves only
the expected symmetries:

```text
forward theta2^-1:
  center = (2, 28),  D = (1, 3)
  center = (2, 28),  D = (2, 166)   # D reversal

reverse theta2:
  center = (1, 141), D = (1, 3)     # inverse center
  center = (1, 141), D = (2, 166)   # inverse center and D reversal
```

Support-only matching gives no extra unsigned hits, and `D=0` gives no match.

## Orientation And Value Route

The raw orientation router classifies the four accepted branches:

```text
C,  y(A)/y(-A)    -> theta2^-1, sign -1
C,  y(-A)/y(A)    -> theta2,    sign +1
-C, y(A)/y(-A)    -> theta2,    sign +1
-C, y(-A)/y(A)    -> theta2^-1, sign -1
```

Wrong center, wrong `D`, and nonprimitive `K` do not route.

For value-level theorem hits, the period matters:

```text
support period = 156
gcd(4^156 - 1, p - 1) = 1
ambient period = 780
gcd(4^780 - 1, p - 1) = 11
```

So a divisor/additive theorem can route through the existing certificate path.
A value-only theorem is viable only if it supplies the period-156
theta2 fixedness/telescoping context; the ambient period-780 value route still
has an 11-branch ambiguity.

## Falsifiers

Reject a proposed exact-P theorem shape if its first output is any of:

```text
raw KL exponent balance without finite theta2 intake
missing, collapsed, or nonprimitive K trace
truncated, wrong, missing, doubled, or reweighted D segment
shifted or inverted center without matching orientation
nonuniform K-layer or atom weights
q-cycle/source-coordinate convention confusion
plain bridge submitted as theta2
value-only unit without period-156 branch selection
```

## Verdict

Exact-P is still open, but the source ask is now much sharper:

```text
continue_exactp = yes
positive_artifact = compact theorem-output interface and certificate router
still_missing = challenge-legal Robert/Siegel/Kubert-Lang/KSY identity for the
                exact equal-weight K-traced anti-invariant normalized-y product
discard_condition = any source that cannot emit the compact C,D,K,orientation
                    packet, an accepted equivalent finite interface, or a
                    period-156 theta2 divisor/additive payload
```

## Recommendation

Ask experts or source searches for this exact interface, not for a generic
"75-atom construction." The finite side now knows where a theorem must land;
the missing piece is an arithmetic theorem that lands there legally.
