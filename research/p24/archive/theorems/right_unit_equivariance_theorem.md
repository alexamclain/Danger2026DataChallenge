# Right-Unit Equivariance Theorem

This note records the next compression after the opposite-conjugation tail
theorem.

## Right-Orbit Action

For p24,

```text
p mod 211 = 114,
ord_211(p)=35,
```

so `F_p[mu_211]` splits into six degree-35 Frobenius factors.  The factor
labels are the six right orbits:

```text
O1,O2,O3,O4,O5,O6.
```

Frobenius fixes each factor label.  The unit `2 mod 211` acts by

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

Inversion is the third power in this quotient action:

```text
O1 <-> O4,
O2 <-> O5,
O3 <-> O6.
```

This is audited by:

```text
p24/right_orbit_unit_action_audit.py
```

with output:

```text
unit=2 perm=(2,3,4,5,6,1)
unit_2_cycles_opposite_pairs=1
unit_2_cycles_opposite_prefixes=1
unit_2_cycles_representative_tails_up_to_inversion=1
```

## Prefix Compression

The opposite-pair prefixes are complements of opposite pairs:

```text
B1: exclude {O1,O4}, prefix {O2,O3,O5,O6}
B2: exclude {O2,O5}, prefix {O1,O3,O4,O6}
B3: exclude {O3,O6}, prefix {O1,O2,O4,O5}
```

The unit `2` cycles these three prefixes:

```text
B1 -> B2 -> B3 -> B1.
```

Therefore, in the full product algebra and with equivariant coordinate
choices, p-unitness of one representative prefix factor implies p-unitness of
all three `B` factors.

The finite implication is recorded in:

```text
p24/lean/UnitOrbitGate.lean
```

## Tail Compression

The six opposite-pair deletion rows form one unit-2 cycle if tail windows are
chosen equivariantly in Lang coordinates:

```text
delete O4, tail O1
  -> delete O5, tail O2
  -> delete O6, tail O3
  -> delete O1, tail O4
  -> delete O2, tail O5
  -> delete O3, tail O6
  -> delete O4, tail O1.
```

Thus one representative tail p-unit implies all six tail p-units, combining
the unit action with the inversion/Lang compatibility from:

```text
p24/opposite_conjugation_tail_theorem.md
```

## Coordinate Caveat

This compression is not a statement inside one selected degree-35 factor
`R=F_p(mu_211)` alone.  The automorphism `mu_211 -> mu_211^2` permutes the six
irreducible factors.  Therefore the certificate must be stated in the full
right cyclotomic product algebra, or the verifier must explicitly record the
factor permutation and the compatible Lang-basis changes.

With arbitrary per-factor coordinate choices, the scalar residual products may
differ by determinant/unit factors.  The invariant statement is p-unit
nonvanishing, not literal equality of the printed scalar representatives.

There is also a tail-window convention caveat.  The unit-2 orbit from the
representative row

```text
deleted O4, tail O1
```

uses the natural first-16 Lang coordinates in `O1`, `O2`, and `O3`, and their
unit-2 images in `O4`, `O5`, and `O6`.  These are not always the same raw
frequency slices as the direct inversion windows printed in the
opposite-pair manifest.  The two conventions differ by an internal Frobenius
rotation in the target right factor.  After Lang trivialization, that internal
Frobenius acts coordinatewise, so it preserves tail zero predicates and
p-unit nonvanishing when the Lang bases are chosen equivariantly.

The representative manifest is printed by:

```text
p24/p24_factorized_certificate_manifest.py
```

under `equivariant_1B1T_representative_certificate`.

## Current Sharpest Proof Surface

Modulo the finite equivariance gates, the p24 mixed Hermitian certificate now
has the following arithmetic proof target:

```text
1 representative leading Moore p-unit L = B*T.
```

The finite symmetries then propagate these to all six deletion rows:

```text
unit-2 action propagates L around the right factor orbit;
inversion/Lang compatibility matches the opposite tail windows;
representative L nonzero gives each delete-one Moore minor;
delete-one Moore minors give right support >= 2;
right support >= 2 gives rank_Fp C_{157,211}=156.
```

This is a major compression of the proof surface, but it still leaves the
hard selected-prime arithmetic theorem: the representative 156-coordinate
Moore determinant must be proved nonzero modulo `p=10^24+7` without
enumerating the class set.  The factorization `L=B*T` remains the best visible
proof strategy for that determinant.

## Transversality Boundary

The unit action itself does not force the representative leading determinant
to be nonzero.  This is recorded in:

```text
p24/unit_orbit_transversality_toy.py
p24/unit_orbit_transversality_boundary.md
```

The toy model has cyclic block symmetry

```text
A_j = A D^j,
```

but the identity action makes all six blocks equal and fails the p24
four-block-plus-tail transversality test identically.  A permutation action
often passes random trials, so symmetry can make success plausible, but it is
not a formal proof.

Therefore this theorem should be used only as:

```text
one representative p-unit nonzero => all six deletion-row p-units nonzero.
```

It is not evidence that the representative p-unit is automatically nonzero.
