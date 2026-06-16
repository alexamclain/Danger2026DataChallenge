# Subsqrt Moonshot Lane B Residue-Mask Stabilizer

Date: 2026-06-12

## Result

The canonical residue-coset carry mask has no hidden affine stabilizer under
the natural product action:

```text
right -> alpha * right + beta mod 3
C     -> u * C + v mod c
```

For the first `C_3 x C_13` lab:

```text
right translation stabilizers = [0]
C translation stabilizers = [0]
C diamond stabilizers = [1]
linear stabilizers = [(1, 0, 1)]
affine stabilizers = [(1, 0, 1, 0)]
full affine group size = 936
orbit size = 936
```

So the `39`-rectangle mask is rigid: it does not descend through a quotient by
a right shift, C-axis shift, diamond action, or combined affine symmetry.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_residue_mask_stabilizer_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_residue_mask_stabilizer_gate.py
```

Observed:

```text
tiny_C3xC13:
  right_translation_stabilizers = [0]
  c_translation_stabilizers = [0]
  c_diamond_stabilizers = [1]
  linear_stabilizer_count = 1
  linear_stabilizers = [(1, 0, 1)]
  affine_stabilizer_count = 1
  affine_stabilizers = [(1, 0, 1, 0)]
  group_size = 936
  orbit_size = 936

prime_axis_C3xC53:
  right_translation_stabilizers = [0]
  c_translation_stabilizers = [0]
  c_diamond_stabilizers = [1]
  linear_stabilizer_count = 1
  linear_stabilizers = [(1, 0, 1)]
  affine_stabilizer_count = 1
  affine_stabilizers = [(1, 0, 1, 0)]
  group_size = 16536
  orbit_size = 16536

square_axis_C3xC169:
  right_translation_stabilizers = [0]
  c_translation_stabilizers = [0]
  c_diamond_stabilizers = [1]
  linear_stabilizer_count = 1
  linear_stabilizers = [(1, 0, 1)]
  affine_stabilizer_count = 1
  affine_stabilizers = [(1, 0, 1, 0)]
  group_size = 158184
  orbit_size = 158184

residue_mask_stabilizer_rows = 3/3
conclusion=reported_p25_laneB_residue_mask_stabilizer_gate
```

## Consequence

This rules out one more compression route:

```text
no hidden right-translation quotient;
no hidden C-translation quotient;
no hidden diamond quotient;
no hidden combined product-affine quotient.
```

The first viable arithmetic producer must therefore realize the coupled
residue-coset mask essentially at full quotient resolution.  For the first
`151 x 677` lab, that means the actual `3 x 13` rectangle pattern, selecting
the `18` carrying quotient rectangles and `5850` raw carry-one positions, not a
smaller orbit representative inflated by symmetry.

Reject candidate producers whose degree saving depends on identifying the
canonical half-arc mask by a nontrivial affine symmetry of the right/C
coordinates.

The candidate-facing pullback harness is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_ray_local_theta31_pullback_falsifier.md
```

It packages the source-coordinate, rectangle-constancy, character-payload,
product-formula, and degree-13 Kummer checks into one finite gate for future
raw producer attempts.
