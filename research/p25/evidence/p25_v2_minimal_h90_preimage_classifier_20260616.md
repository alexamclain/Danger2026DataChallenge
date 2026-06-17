# P25 v2 Minimal H90 Preimage Classifier

Updated: 2026-06-16

## Purpose

Close the remaining selector ambiguity around the conductor-39 Hilbert-90
boundary `W`.  The quotient-H90 mechanism identifies four legal preimages; this
page classifies all minimal integral sparse preimages of `W` and records which
ones preserve the mixed tensor.

This is still not the missing arithmetic value/divisor theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_unified_source_theorem_gap_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_minimal_h90_preimage_classifier_gate.py
```

The gate returned `p25_v2_minimal_h90_preimage_classifier_rows=1/1`.

## Preimage Space

The boundary word `W` has four Frobenius orbits on conductor-39 residues, each
of length six:

```text
(1, 23, 22, 38, 16, 17)
(2, 7, 5, 37, 32, 34)
(4, 14, 10, 35, 25, 29)
(8, 28, 20, 31, 11, 19)
```

On each orbit, there are exactly two support-three local primitives.  Therefore
there are:

```text
2^4 = 16
```

minimal support-12 integral preimages of `W`.

## Classification

```text
minimal_preimage_count = 16
mixed_legal_rows = 4
formal_one_coset_rows = 2
mod3_balanced_only_rows = 2
axis_leaking_rows = 8
```

The four mixed legal rows are exactly the rows already named by the mod-13
rectangle and quotient-H90 mechanism.  They are the only minimal preimages
whose pushforwards to both proper axes vanish:

```text
pushforward mod 3 = 0
pushforward mod 13 = 0
```

The remaining twelve rows are boundary controls, not first-pass source closers:

```text
formal one-coset rows:
  match the boundary but leak to both proper axes

mod3-balanced-only rows:
  vanish on mod 3 but leak on mod 13

axis-leaking rows:
  leak to both mod 3 and mod 13
```

## Routing Rule

The first-pass source ask is now selector-rigid:

```text
one of four mixed legal minimal H90 preimages of W
+ Yang lift / support-156 product
+ finite divisor/additive theorem, or period-156 value theorem
+ DANGER3 framing and extraction
```

Do not spend more effort searching for another sparse Hilbert-90 selector
unless a source theorem changes the legality condition itself.

## Verdict

```text
all_minimal_preimages_classified = yes
hidden_sparse_selector_freedom_remaining = no
source_theorem_in_hand = 0
direct_closer = 0
next = arithmetic value/divisor theorem for one of the four mixed legal
       minimal H90 preimages
```
