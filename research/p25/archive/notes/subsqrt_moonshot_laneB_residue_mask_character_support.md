# Subsqrt Moonshot Lane B Residue-Mask Character Support

Date: 2026-06-12

## Result

The binary residue-coset carry mask has full character support, except for the
pure-right characters forced to vanish by equal row sums.

For the first `C_3 x C_13` lab:

```text
nonzero character coefficients = 37
scalar = 1
pure right = 0
pure C = 12 / 12
mixed right-C = 24 / 24
```

So the local mask is not only coupled; it uses every nontrivial C character and
every mixed right/C character.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_residue_mask_character_support_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_residue_mask_character_support_gate.py
```

Observed:

```text
tiny_C3xC13:
  nonzero = 37
  scalar = 1
  pure_right = 0
  pure_c = 12/12
  mixed = 24/24

prime_axis_C3xC53:
  nonzero = 157
  scalar = 1
  pure_right = 0
  pure_c = 52/52
  mixed = 104/104

square_axis_C3xC169:
  nonzero = 505
  scalar = 1
  pure_right = 0
  pure_c = 168/168
  mixed = 336/336

residue_mask_character_support_rows = 3/3
conclusion=reported_p25_laneB_residue_mask_character_support_gate
```

## Consequence

This rules out a sparse-character local producer:

```text
no pure-right-only payload;
no small subset of C characters;
no small subset of mixed right/C characters;
no low-frequency or orbit-sparse character expansion.
```

For the first `151 x 677` lab, a candidate producer must realize:

```text
the coupled 39-rectangle residue mask
with full nontrivial C_13 character support
and full mixed C_3 x C_13 character support.
```

This complements the previous coupling gate: nonzero mixed second differences
rule out separated row/column masks, and full character support rules out sparse
character masks.

The stabilizer checkpoint for this same mask is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_residue_mask_stabilizer.md
```

It records the next obstruction: the mask has trivial stabilizer under the full
right/C product-affine action, so hidden affine quotient compressions are also
ruled out.
