# P25 v2 H0 Theorem Interface Contract

Updated: 2026-06-16

Marker: `p25_v2_h0_theorem_interface_contract_rows=1/1`

## Purpose

Promote the current H0 front into a compact theorem contract: the exact legal
H0 products, the two source-stage closing shapes, the period-156/Hilbert-90
boundary requirements, and the downstream `X_1(8112)` bridge payload needed
before any H0 theorem can become a DANGER3 certificate.

This is not the missing H0 value/divisor theorem. It is the interface that a
source theorem must satisfy.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `sources/koo-shin-2010.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`
- `archive/notes/p25_ksy_y_h0_source_to_danger3_handoff_20260614.md`
- `archive/notes/p25_ksy_y_x1_8112_torsion_gluing_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md`
- `archive/notes/p25_ksy_y_x1_16_halving_certificate_payload_20260614.md`

## Commands

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_source_theorem_candidate_matcher_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_period156_value_compatibility_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_translate_value_compatibility_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_translate_boundary_value_ambiguity_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_translate_source_obligation_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_translate_theorem_query_packet_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_y507_to_x16_extraction_boundary_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_source_to_danger3_handoff_gate.py

PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_ksy_y_h0_x18112_bridge_payload_contract_gate.py
```

All nine gates returned their expected `rows=1/1` markers after the archive-path
fallback was restored for the post-wiki gate dependencies.

The lightweight v2 contract gate returned
`p25_v2_h0_theorem_interface_contract_rows=1/1`.

## Legal H0 Products

The legal H0 objects are exactly four 78-over-78 products in one doubling
orbit. The canonical row is:

```text
m = 1
constants = (3, 3, -3, -3)
positive residues = (7, 17, 23, 34, 37, 38)
negative residues = (4, 8, 10, 11, 20, 25)
```

The other legal translates are:

```text
m = 2  constants = (-3,  3,  3, -3)  P=(7,14,29,34,35,37)  N=(1,8,11,16,20,22)
m = 4  constants = (-3, -3,  3,  3)  P=(14,19,28,29,31,35) N=(1,2,5,16,22,32)
m = 8  constants = ( 3, -3, -3,  3)  P=(17,19,23,28,31,38) N=(2,4,5,10,25,32)
```

Anything outside these legal H0 products is not a first-pass H0 closer.

## Source-Stage Closing Shapes

There are two acceptable source-stage exits:

```text
exact finite H0 value identity
+ period-156 branch/root/telescoping context
+ boundary (1 - Frob_p) H0 = Norm_156(Y_507)
```

or:

```text
exact H0 divisor/additive identity
+ Hilbert-90 boundary to Norm_156(Y_507)
```

Koo-Shin 2010 Theorem 6.2 remains source-certification evidence. Boundary-only
H0 data, legality-only source results, or generic value language do not close
source stage.

## Period And Boundary Constraints

The period screen is decisive:

```text
Y_507 minimum doubling period = 156
H0 support period = 156
support-period root gcd = 1
ambient-period root gcd = 11
ord_39(p) = 6
primitive 39th roots first appear in degree 6
sqrt(-39) is not in F_p
```

Thus a period-156 H0 value theorem can be unambiguous over `F_p`, while an
ambient-period-780 value theorem keeps an 11-branch ambiguity unless it supplies
the period-156 branch data. Direct `F_p` order-39-root and `sqrt(-39)` shortcuts
are invalid.

## DANGER3 Handoff

Even a source-closed H0 theorem is not a DANGER3 certificate. It must still
pass through:

```text
DANGER3 finite-identity / non-CM framing
same-j X_1(8112) bridge
X_1(16) y, model root, A, and xP16 extraction
halving chain to x0
official vpp.py verification
```

The `X_1(8112)` bridge payload is now explicit:

```text
levels = 16 and 507, coprime
inv_507 mod 16 = 3
inv_16 mod 507 = 412
P16 = [3*507]R = [1521]R
Q507 = [412*16]R = [6592]R
1521 + 6592 = 1 mod 8112
```

A same-curve `P16,Q507` pair, or an order-8112 generator `R` with these
normalized projections, is the required cross-level payload. Independent
level-16 and level-507 data without same-`j` gluing is rejected.

## Falsifiers

Reject a proposed H0 theorem shape if its first output is any of:

```text
nonlegal H0 product or formal one-coset product
Koo-Shin 2010 source certification only
boundary-only H0 data with no finite value/divisor theorem
finite payload with no arithmetic source theorem
value theorem without period-156 branch/root/telescoping context
divisor/additive statement without Hilbert-90 boundary
direct F_p order-39-root or sqrt(-39) shortcut
same-j bridge missing after source closure
unglued level-16 and level-507 data
X_1(16) relation with no y/model-root/A/xP16 extraction
unverified concrete triple
```

## Verdict

H0 remains live and is now sharply targetable:

```text
continue_h0 = yes
positive_artifact = exact legal H0 product plus period-156 value theorem,
                    or H0 divisor/additive theorem with H90 boundary
still_missing = the arithmetic source theorem itself, then DANGER3 framing,
                same-j X_1(8112) bridge, X_1(16) extraction, halving, vpp.py
best_expert_ask = theorem for one legal H0/H0-translate product with
                  (1-Frob_p) boundary Norm_156(Y_507) and period-156 context
```
