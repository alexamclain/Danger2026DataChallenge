# Exterior Character-Support Boundary

This note records a structural reason the sliding-window product does not have
a low-character-support compression.

## Exterior View

For one packet factor of `Phi_n`, multiplication by `X` has eigencharacters
given by a Frobenius orbit

```text
H = <p> in (Z/nZ)^*.
```

The coefficient-minor route works in an exterior power.  Beta-shifted Pluecker
coordinates can involve sums of packet exponents.  Thus additive sumsets such
as

```text
H + H
```

measure how much cyclic beta-character support is available before any CM
geometry is used.

If `H+H` already covers all of `Z/nZ`, then the exterior representation can
carry every beta character.  That rules out a proof based only on small
character support or a short universal recurrence.

## p24 Audit

I added:

```text
p24/exterior_character_support_audit.py
```

Run with the bundled Python NumPy runtime:

```text
PYTHONDONTWRITEBYTECODE=1 \
  /Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/exterior_character_support_audit.py
```

For p24:

```text
n=3107441
p mod n=2509452
orbit_size=388430
multiplicative_index=8

H+H:
  covered_residues=3107441
  full_coverage=1
  min_ordered_pair_count=48343
  max_ordered_pair_count=388430
```

So every residue modulo `n` is a sum of two packet exponents, with large
multiplicity.  In particular, distinct-pair representations exist for every
residue.

The small extra-coordinate row used in the sequence-complexity scan has the
same behavior:

```text
n=11
q mod n=2
orbit_size=10
H+H full_coverage=1
```

## Consequence

The full Berlekamp-Massey complexity seen in

```text
p24/axis_sliding_window_sequence_complexity.md
```

is not an accident of the chosen CM vector.  The exterior-power packet
representation already has full beta-character support available.  Therefore
`Pi_axis,a` remains a high-order packet-phase object unless a proof uses
specific CM arithmetic beyond packet character support.
