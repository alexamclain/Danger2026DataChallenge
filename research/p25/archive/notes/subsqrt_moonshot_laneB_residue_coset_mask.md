# Subsqrt Moonshot Lane B Residue-Coset Mask

Date: 2026-06-12

## Result

The canonical half-arc target is not just a log-coordinate pattern.  It is a
union of actual local residue coset rectangles.

For the first lab:

```text
C_3 x C_13
right source: mod 151, inert
C source:     mod 677, split
B:            325
```

the source residue classes are:

```text
mod 151:
  3 quotient classes
  each class has 25 residues

mod 677:
  13 quotient classes
  each class has 13 residues

one quotient point:
  25 * 13 = 325 residue pairs
```

So the canonical `theta_{3,1}` half-arc mask is a union of product rectangles
inside the actual local residue data.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_residue_coset_mask_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_residue_coset_mask_gate.py
```

Observed:

```text
tiny_C3xC13:
  quotient_rectangles = 39/39
  residue_rectangle_size = 325
  block_constancy_hits = 39/39
  carry_constancy_hits = 39/39
  raw_carry_count = 5850
  mod151 class sizes = [25]
  mod677 class sizes = [13]
  zone rectangles:
    zero     = 12
    one_hot  = 9
    two_hot  = 9
    all_rows = 9
  carry rectangles:
    zero     = 0
    one_hot  = 3
    two_hot  = 6
    all_rows = 9

prime_axis_C3xC53:
  quotient_rectangles = 159/159
  residue_rectangle_size = 25
  raw_carry_count = 1950
  mod7 class sizes = [1]
  mod151 class sizes = [25]
  mod107 class sizes = [1]

square_axis_C3xC169:
  quotient_rectangles = 507/507
  residue_rectangle_size = 25
  raw_carry_count = 6300
  mod151 class sizes = [25]
  mod677 class sizes = [1]

residue_coset_mask_rows = 3/3
conclusion=reported_p25_laneB_residue_coset_mask_gate
```

## Consequence

The first producer target can be stated without hidden coordinate choices:

```text
produce a local residue-coset mask on mod151 x mod677
whose 39 quotient rectangles are:
  12 zero-zone rectangles;
  9 one-hot-zone rectangles, 3 carrying;
  9 two-hot-zone rectangles, 6 carrying;
  9 all-rows-zone rectangles, 9 carrying.
```

This gives a concrete falsifier for any proposed ray-local CM-Artin or
modular-unit pullback:

```text
it must be constant on the 25 x 13 residue rectangles;
it must select exactly the 18 carrying quotient rectangles;
it must have exactly 5850 raw carry-one positions;
it must trace back to the canonical theta_{3,1} packet.
```

Discard conditions:

```text
kill candidates that only match log coordinates but not residue cosets;
kill candidates whose mask is not rectangle-constant;
kill candidates with the right raw count but wrong one-hot/two-hot/all-rows split;
kill candidates that collapse the inert 151 side or split 677 side separately.
```

This still is not the missing producer.  It makes the local target concrete
enough that a proposed arithmetic object can be checked directly on residue
cosets, before spending effort on certificate packaging.

The coupling checkpoint for this same mask is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_residue_mask_coupling.md
```

It verifies that the rectangle mask is not right-only, not C-only, and not a
row-plus-column separated mask.  The producer must genuinely couple the inert
`151` side to the split `677` side.
