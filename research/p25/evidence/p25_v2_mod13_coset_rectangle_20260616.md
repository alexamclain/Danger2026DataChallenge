# P25 v2 Mod-13 Coset Rectangle

Updated: 2026-06-16

## Purpose

Compress the mixed signed-column fingerprint one step further.  The six live
`C_13` columns in each legal conductor-39 row are not arbitrary: they are one
order-3 coset with row-1 plus signs and one order-3 coset with row-1 minus
signs.

This is a source-snippet filter, not the missing theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_mod13_coset_rectangle_gate.py
```

The gate returned `p25_v2_mod13_coset_rectangle_rows=1/1`.

## Coset Geometry

Let:

```text
H = <3> = (1, 3, 9) in (Z/13Z)^*
2H = (2, 5, 6)
4H = (4, 10, 12)
7H = (7, 8, 11)
```

The square cosets are `H` and `4H`; the nonsquare cosets are `2H` and `7H`.

The four legal rows are exactly the rectangle edges:

```text
m=1: row1 plus = 7H, row1 minus = 4H
m=2: row1 plus = 7H, row1 minus = H
m=4: row1 plus = 2H, row1 minus = H
m=8: row1 plus = 2H, row1 minus = 4H
```

Equivalently, a legal row chooses one nonsquare order-3 coset for row-1 plus
columns and one square order-3 coset for row-1 minus columns; row-2 signs are
opposite.

## Controls

These are rejected as first-pass source closers:

```text
pure quadratic character:
  too broad; uses both nonsquare cosets against both square cosets

same-parity coset pair:
  plus and minus are both square or both nonsquare cosets

non-coset triple:
  row columns are not an order-3 coset
```

So the source theorem cannot merely say "quadratic character mod 13" or
"some six signed columns."  It must preserve, or transform into, one rectangle
edge after row normalization.

## Routing Rule

Accepted source-stage shape now has this column-level form:

```text
one normalized legal support-156 row
+ one nonsquare order-3 C_13 coset as row1 plus
+ one square order-3 C_13 coset as row1 minus
+ opposite row2 signs
+ Hilbert-90 boundary W = Norm_156(Y_507)
+ finite value/divisor theorem
```

## Verdict

```text
legal_rows_ok = 4/4
control_rows_ok = 3/3
current_source_theorem_rows = 0
direct_closer = 0
next = source theorem preserving one mod-13 rectangle edge, or a falsifier for
       that exact theorem shape
```
