# P25 KSY-y Yang Y507 Conductor-39 Mixed Tensor Character

Updated: 2026-06-14 09:35 PDT

## Purpose

The primitive conductor-`39` unit is:

```text
U_chi = -chi_39 = -chi_3 * chi_13
```

This checkpoint verifies that `U_chi` is genuinely mixed.  It is not a
conductor-`3` pullback, not a conductor-`13` pullback, and not an additive
separation of the two axes.

## Proper Axis Tests

Both proper pushforwards vanish:

```text
pushforward mod 3  = 0
pushforward mod 13 = 0
```

Both proper pullback tests fail:

```text
mod 3 pullback failure:   residues 1 and 7 have coefficients -1 and +1
mod 13 pullback failure:  residues 1 and 14 have coefficients -1 and +1
```

So neither proper axis can see the character by projection, and neither proper
axis can reconstruct it by pullback.

## Tensor Table

Indexed by `mod 3` rows and nonzero `mod 13` columns:

```text
row mod 3 = 1:
-1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1

row mod 3 = 2:
 1,-1,  1,  1,-1,-1,-1,-1,  1,  1,-1,  1
```

The two rows are negatives.  All row sums and column sums are zero.  The row
differences are not constant, so this is not an additive separation
`A(mod 3)+B(mod 13)`.

The exact surviving structure is the tensor:

```text
U_chi(r) = -chi_3(r) * chi_13(r)
```

## Verdict

Positive payload:

```text
U_chi is a genuine mixed conductor-39 tensor character: -chi_3 * chi_13
```

First missing clause:

```text
mixed tensor structure is not the finite-field value/divisor theorem or
DANGER3 extraction
```

Practical effect:

```text
ask source theorems for a mixed chi_3 tensor chi_13 character unit; reject
conductor-3-only, conductor-13-only, projection-only, pullback-only, or additive
separated explanations
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_mixed_tensor_character_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_mixed_tensor_character_rows=1/1
```
