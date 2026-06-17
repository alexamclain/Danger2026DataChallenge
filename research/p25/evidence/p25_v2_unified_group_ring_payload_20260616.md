# P25 v2 Unified Group-Ring Payload

Updated: 2026-06-16

## Purpose

Record the algebraic payload behind the unified theorem review packet.  The
review packet says what an expert should assess; this page pins the exact
group-ring object: the conductor-39 Hilbert-90 word, the level-507 Yang lift,
the period norm of `Y_507`, and the four support-156 product rows.

This is still not the missing arithmetic theorem.  It is the finite object that
the theorem must evaluate or identify.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_period_norm_character_gate.py`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_unified_group_ring_payload_gate.py
```

The gate returned `p25_v2_unified_group_ring_payload_rows=1/1`.

## Ambient Data

```text
level = 507
conductor = 39
lift_length = 13
support_period = 156
p mod 39 = 23
Hilbert-90 character support = 24
balanced potential support = 24
sparse potential support = 12
period norm support = 312
period norm coefficient counts = (-6, 156), (6, 156)
```

The conductor-39 character word is an integral Hilbert-90 boundary:

```text
W = (1 - Frob_p) V
```

The legal sparse potentials on `X_1(39)` lift through Yang's 13-fiber
distribution to level `507`, where their boundaries equal the period norm
`Norm_156(Y_507)`.

## Product Rows

For each row, the lifted product is:

```text
prod_{a in P, k=0..12} E_{a+39k}^6
/
prod_{b in N, k=0..12} E_{b+39k}^6
```

Rows:

```text
m=1
constants = (3, 3, -3, -3)
P = (7, 17, 23, 34, 37, 38)
N = (4, 8, 10, 11, 20, 25)
lifted = +78 / -78
sha256 = eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e

m=2
constants = (-3, 3, 3, -3)
P = (7, 14, 29, 34, 35, 37)
N = (1, 8, 11, 16, 20, 22)
lifted = +78 / -78
sha256 = 97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9

m=4
constants = (-3, -3, 3, 3)
P = (14, 19, 28, 29, 31, 35)
N = (1, 2, 5, 16, 22, 32)
lifted = +78 / -78
sha256 = 28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6

m=8
constants = (3, -3, -3, 3)
P = (17, 19, 23, 28, 31, 38)
N = (2, 4, 5, 10, 25, 32)
lifted = +78 / -78
sha256 = ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

The four rows are one doubling orbit:

```text
quotient_representatives = (1, 2, 4, 8)
canonical_stabilizer = (1, 16, 22)
formal_one_coset_controls_rejected = yes
```

## Theorem Meaning

The source theorem now has a fully pinned finite object.  It must supply one
of:

```text
divisor/additive identity for one row above
with (1 - Frob_p)H = Norm_156(Y_507)
```

or:

```text
period-156 value identity for one row above
with branch/root/telescoping context
```

The group-ring payload is a positive artifact because it removes ambiguity in
the target.  It is not a source-stage close.

## Stop Signs

Do not treat any of these as progress unless they also supply the missing
theorem:

```text
another H0 or conductor-39 source certificate
another Hilbert-90 boundary computation
another Yang-lift product normal form
formal one-coset/projection/suborbit shortcut
finite payload with no arithmetic source theorem
```

## Verdict

```text
payload_rows = 4
payload_rows_ok = 4
source_theorem_in_hand = 0
direct_closer = 0
next = source theorem or expert falsifier for the exact payload above
```
