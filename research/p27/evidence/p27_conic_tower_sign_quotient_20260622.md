# P27 Conic Tower Sign-Quotient Probe

Date: 2026-06-22

## Claim

The obvious sign quotients of the conic tower are coherent but not
sqrt-beating.

On p27 train/heldout samples, the d5 selector remains well-defined after
forgetting the natural conic signs, reciprocal signs, and first Kummer-root
signs.  In fact the screened d5 values already descend to the `A` and `(A,x)`
projections on the d4-plus slice.

That is positive structure, but it is not a source shrink.  It collapses only
finite sign multiplicities; the surviving `A` and `(A,x)` sets still thin like
ordinary half-gates, as recorded in
[P27 A-Projection Selected-Prefix Profile](p27_a_projection_prefix_profile_20260621.md).

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_conic_tower_sign_quotient_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_conic_tower_sign_quotient_probe_q1607_q1847_q2087_p27_300_20260622.txt
research/p27/archive/probe_outputs/p27_conic_tower_sign_quotient_probe_p27_1000_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_tower_sign_quotient_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 300 \
  --p27-heldout-target 300 \
  --p27-max-draws 700000 \
  | tee research/p27/archive/probe_outputs/p27_conic_tower_sign_quotient_probe_q1607_q1847_q2087_p27_300_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_conic_tower_sign_quotient_probe.py \
  --small-primes '' \
  --p27-target 1000 \
  --p27-heldout-target 1000 \
  --p27-max-draws 1500000 \
  | tee research/p27/archive/probe_outputs/p27_conic_tower_sign_quotient_probe_p27_1000_20260622.txt
```

## Systems Screened

The probe groups d4-plus/two-step selector rows by:

```text
base_A
base_Ax
first_signed
first_unsigned
first_square
two_signed
two_drop_L1_sign
two_square
two_reciprocal
two_selector_signless
z0_signless
```

For each grouping it reports whether both d5 signs occur in the same group.
A mixed group would kill that quotient as a selector-preserving source.

## P27 Results

In the larger p27 run, every screened quotient had:

```text
mixed_groups = 0
mixed_rows = 0
```

The strongest collapse is already at the `A` projection:

```text
p27 train, 1000 unique (A,x):
  base_A groups = 122
  target plus/minus rows = 50,176 / 74,752
  mixed groups = 0

p27 heldout, 1000 unique (A,x):
  base_A groups = 116
  target plus/minus rows = 55,296 / 63,488
  mixed groups = 0
```

The `(A,x)` projection is similarly unmixed:

```text
p27 train base_Ax groups = 244
p27 heldout base_Ax groups = 232
mixed groups = 0
```

The deeper sign quotients are also unmixed, but they retain many more groups:

```text
p27 train:
  first_unsigned groups = 1,952
  two_reciprocal groups = 7,808
  two_signed groups = 15,616

p27 heldout:
  first_unsigned groups = 1,856
  two_reciprocal groups = 7,424
  two_signed groups = 14,848
```

So these quotients are selector-preserving finite covers, not smaller sources.

## Guard Fields

The guard fields are less decisive for this question because d5 is locally
constant on the screened d4-plus slice:

```text
q1607: all d5 plus
q1847: all d5 minus
q2087: all d5 plus
```

They still validate the multiplicity bookkeeping:

```text
base_Ax group size = 512
first_unsigned group size = 64
two_reciprocal group size = 16
two_signed group size = 8
```

but the p27 train/heldout samples are the real anti-overfit check.

## Interpretation

Positive:

```text
The repeated conic selector descends through the obvious sign quotients.
The d5 selector is not hidden in individual h/g/r/Z sign choices.
The conic tower can be staged over smaller quotient coordinates for CAS.
```

Negative:

```text
The quotient collapse is only finite multiplicity.
The earliest useful quotient, A or (A,x), still has random-looking half-loss.
This does not justify an A-bucket, sign-bucket, or GPU production search.
```

This result sharpens the CAS handoff:
[P27 Conic Tower Quotient CAS Handoff](p27_conic_tower_quotient_cas_handoff_20260622.md).
The CAS target should quotient obvious signs immediately, then ask whether the
remaining `A`-level or legal-pullback curve has a low-genus/sourceable
structure.  The sign quotient alone is not the win.

## Continue / Kill

```text
continue = quotient signs before staged normalization of the legal conic tower
continue = extract the actual A/legal-pullback Kummer class if CAS can
continue = compare d4,d5,d6 classes after quotienting the finite sign cover

kill = sign choices as the missing sqrt-beating obstruction
kill = GPU sign-bucket searches in h/g/r/Z signs
kill = treating A descent as source shrink without a low-genus/source law
```

```text
p27_conic_tower_sign_quotient_rows=1/1
```
