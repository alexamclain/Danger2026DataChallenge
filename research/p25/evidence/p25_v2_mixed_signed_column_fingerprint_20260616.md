# P25 v2 Mixed Signed-Column Fingerprint

Updated: 2026-06-16

## Purpose

Promote a sharper mixed-tensor fingerprint for the unified H0/conductor-39
target.  The group-ring payload already fixes the four legal support-156 rows;
this page records the conductor-39 source-side shape that future source
snippets must preserve before they can be treated as theorem candidates.

This is not the missing arithmetic value/divisor theorem.  It is a compact
falsifier for projection-only, pullback-only, additive-separated, or formal
one-coset answers.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate.py`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_mixed_signed_column_fingerprint_gate.py
```

The gate returned `p25_v2_mixed_signed_column_fingerprint_rows=1/1`.

## Fingerprint

For each legal conductor-39 source potential:

```text
support = 12
boundary = W = 6 * (1_{7<2>} - 1_{<2>})
pushforward mod 3 = 0
pushforward mod 13 = 0
live C_13 columns = 6
each live column has opposite C_3 signs: (+,-) or (-,+)
empty C_13 columns = 6
pullback from mod 3 = false
pullback from mod 13 = false
additive separated = false
```

So the live source object is not merely a sparse Hilbert-90 gauge.  It is a
signed six-column matching in the CRT grid `C_3 x C_13`.

## Legal Rows

```text
m=1
  live columns      = (4:-,+), (7:+,-), (8:+,-), (10:-,+), (11:+,-), (12:-,+)
  row1 plus columns = (7, 8, 11)
  row1 minus columns = (4, 10, 12)

m=2
  live columns      = (1:-,+), (3:-,+), (7:+,-), (8:+,-), (9:-,+), (11:+,-)
  row1 plus columns = (7, 8, 11)
  row1 minus columns = (1, 3, 9)

m=4
  live columns      = (1:-,+), (2:+,-), (3:-,+), (5:+,-), (6:+,-), (9:-,+)
  row1 plus columns = (2, 5, 6)
  row1 minus columns = (1, 3, 9)

m=8
  live columns      = (2:+,-), (4:-,+), (5:+,-), (6:+,-), (10:-,+), (12:-,+)
  row1 plus columns = (2, 5, 6)
  row1 minus columns = (4, 10, 12)
```

All four rows share the same Hilbert-90 boundary `W`.  The row differences are
the doubling-orbit presentations already normalized in
`p25_v2_row_orbit_normalization_20260616.md`.

## Formal Controls

The formal one-coset gauges remain useful boundary controls but fail this
fingerprint:

```text
positive_one_coset_boundary_control
  boundary = W
  pushforward mod 3 != 0
  pushforward mod 13 != 0
  signed-column fingerprint = false

negative_one_coset_boundary_control
  boundary = W
  pushforward mod 3 != 0
  pushforward mod 13 != 0
  signed-column fingerprint = false
```

This explains why a boundary-only or one-coset answer is not enough: it can
match `(1-Frob_p)V = W` while losing the mixed conductor-39 tensor structure.

## Source-Theorem Routing

A future conductor-39 source theorem should preserve one of the normalized
legal signed-column rows, or explicitly transform its output into one before
the source-snippet intake.  Reject the following as first-pass closers:

```text
prime projection
conductor-3 or conductor-13 pullback
additive separated explanation
one-coset Hilbert-90 boundary control
boundary statement with no finite value/divisor theorem
```

## Verdict

```text
legal_rows_ok = 4/4
formal_controls_rejected = 2/2
source_theorem_in_hand = 0
direct_closer = 0
next = ask for a finite value/divisor theorem preserving one normalized
       signed-column row with boundary W = Norm_156(Y_507)
```
