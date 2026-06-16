# P25 Lane B: Robert KSY Kubert-Lang Inversion Pairs

Updated: 2026-06-13 16:52 PDT

## Purpose

The primitive-D crosswalk rewrites the KL source packet as:

```text
z^121 * (1 + z + z^2) * (1 - z^263)
```

This gate asks which subpackets of those six cells already pass the elementary
Kubert-Lang exponent congruence screen.

## Result

The legal subpackets are exactly the nonempty unions of these three inversion
pairs:

```text
z^121 - z^386
z^122 - z^385
z^123 - z^384
```

Equivalently, each legal atom is `z^a - z^-a` in the primitive `D` coordinate.
There are therefore `2^3 - 1 = 7` legal target-support subpackets, and all
seven are precisely unions of those atoms.

## Contrast With T Edges

The KSY product is naturally written as three parallel `T` edges:

```text
z^121 - z^384
z^122 - z^385
z^123 - z^386
```

Only the middle `T` edge is itself KL-legal.  The outer two fail the elementary
quadratic congruence screen.

So the KL/Siegel-unit screen does not see three independent `T`-edge units. It
sees three anti-invariant inversion-pair units whose union is the same final
six-cell packet.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_inversion_pair_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_inversion_pair_rows=1/1
```

## Interpretation

This is a positive theorem-search hint, not a producer proof.  The next
Kubert-Lang/Sprang/Robert attempt can target anti-invariant Siegel/Robert
pairs `z^a-z^-a`, but it still has to identify their sum with the KSY
`T=(2,113)` normalized-y product and the period-156 theta2 certificate.

Reject a proposed KL explanation that factors the packet into three independent
legal `T` edges; that is not what the congruence screen supports.
