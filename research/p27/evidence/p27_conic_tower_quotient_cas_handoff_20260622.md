# P27 Conic Tower Quotient CAS Handoff

Date: 2026-06-22

## Claim

The conic-chain lane now has one precise sqrt-beating test left:

```text
find a low-genus quotient, recurrence, or direct sampler for the legal
repeated Kummer tower
```

Do not spend more effort on free `(R,L)` buckets or short sign words.  The
selector tower is exact, but p27 prefix counts still thin like independent
half-gates unless a quotient/source is found.

## Manifest

Machine-readable CAS queue:

```text
research/p27/archive/fixtures/p27_conic_tower_quotient_cas_suite_20260622.json
```

## Tower

Use:

```text
A = 2 - c^2
x_j = r_j^2
```

One conic transition is:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

With:

```text
a_j = r_{j+1} - 1/r_{j+1}
L_j = h_j - g_j - 2*r_j
```

the repeated selector divisor is:

```text
Z_j^2 = -(L_j + a_j)*(L_j - a_j)*c*r_{j+1}
```

and, because p27 has `chi(2)=+1`,

```text
chi(r_{j+1}^2 + c*r_{j+1} + 1)
  = chi(-(L_j+a_j)(L_j-a_j)c*r_{j+1}).
```

## Evidence Boundary

Positive structure:

```text
d4 selector product is exact
d5 selector product repeats with zero mismatches
legal conic-chain lift existence matches selected-prefix bits through depth 5
obvious sign quotients preserve d5 on p27 train/heldout samples
d6 also descends to A after d4-plus/d5-plus on p27 train/heldout samples
p27 selected gates d3..d14 have zero mixed A groups in 12000/12000 samples
```

Negative boundary:

```text
free random (R,L) hits legal rows only at constant/q density
simple pair/triple Kummer coordinate screens are full-rank
p27 conic prefixes still thin like independent half-gates through useful counts
selected one-step and two-step coordinates do not re-enter the original legal source
sign quotients collapse only finite multiplicity and do not shrink A-space
d6 A-descent still thins like ordinary A-prefix half-loss without a source law
deeper A-prefix descent also stays near geometric half-loss through robust counts
visible degree <=4 A-line branch support is killed for d3 in q1607/q1847/q2087
```

## CAS Tasks

1. Depth-1 legal pullback quotient.

Compute dimension, components, obvious sign involutions, quotient maps, and
genus for:

```text
legal label-2/compactD source + one conic transition
```

Promotion requires a low-genus quotient or explicit sampler of legal d3-plus
rows.

Start by quotienting the finite sign cover documented in
[P27 Conic Tower Sign-Quotient Probe](p27_conic_tower_sign_quotient_20260622.md).
That quotient is selector-preserving but not source-shrinking by itself.

2. Depth-2 repeated selector quotient.

Compute whether adding the repeated selector layer

```text
Z0^2 = -(L0+a0)(L0-a0)c*r1
```

and the second transition makes d5 a pullback/reuse of d4 on a low-genus
quotient.

3. Legal tower sampler test.

Before treating this as a sampler, run the A-level class extraction forced by
[P27 Conic Tower D6 A-Descent](p27_conic_tower_d6_a_descent_20260622.md):
compute the normalized A-level cover carrying d4, d5, and d6, then compare
their quadratic branch divisors/classes.  Promote only if the characters are
pullbacks, translates, coboundaries, or iterates of one low-genus/sourceable
class.  Kill if they are independent fresh half-covers.

[P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md) extends
the target to d3..d14 in samples.  For a first CAS pass, compute d3..d10 where
sample counts are still healthy; use d11..d14 as routing evidence only.
[P27 A-Line Character Support Screen](p27_a_line_character_support_20260622.md)
kills the nearest visible degree `<= 4` branch-support shortcut, so the CAS
pass should extract divisor/Kummer classes directly instead of widening blind
A-polynomial scans.
[P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)
is the concrete input packet for this pass.  Its JSON fixture records
q1607/q1847/q2087 A-labeled d3/d4 rows and the exact promote/kill criteria.
[P27 A-Line Named-Transform Recurrence Screen](p27_a_line_named_transform_recurrence_20260622.md)
then closes the cheap visible branch-orbit shortcut: the S3 transforms
preserving `A in {-2,2,infinity}` do not preserve or relate the selected
A-classes in guard fields or p27 samples.  The CAS pass should compute the
actual normalized-cover/Kummer classes, not an A-branch orbit quotient.

If a quotient/source map appears, measure:

```text
source_draw denominator
legal rows emitted
prefix depth distribution
target/source_draw versus raw X1(16)
```

## Promote / Kill

Promote:

```text
low-genus/sourceable quotient
reusable Kummer class coupling d4,d5,...
direct legal tower sampler beating independent half-loss by >=1.25x
```

Kill:

```text
high-genus/generic legal pullback after quotienting obvious symmetries
d5 is a fresh independent half-cover on every low-genus quotient
sampler pays the same constant/q legal-incidence denominator as free (R,L)
```

## Linked Artifacts

- [P27 Conic-Pair D4 Recurrence](p27_conic_pair_d4_recurrence_20260621.md)
- [P27 Conic-Pair D5 Tower](p27_conic_pair_d5_tower_20260621.md)
- [P27 Legal Conic Tower Depth](p27_legal_conic_tower_depth_20260621.md)
- [P27 Conic Sign-Word Coupling Probe](p27_conic_signword_coupling_20260622.md)
- [P27 Conic Tower Sign-Quotient Probe](p27_conic_tower_sign_quotient_20260622.md)
- [P27 Conic Tower D6 A-Descent](p27_conic_tower_d6_a_descent_20260622.md)
- [P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md)
- [P27 A-Line Character Support Screen](p27_a_line_character_support_20260622.md)
- [P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)
- [P27 A-Line Named-Transform Recurrence Screen](p27_a_line_named_transform_recurrence_20260622.md)
- [P27 Conic-Pair Two-Step Kummer Screen](p27_conic_pair_two_step_kummer_20260621.md)
- [P27 Conic-Pair Two-Step Kummer Trivariate Screen](p27_conic_pair_two_step_kummer_trivar_20260621.md)

```text
p27_conic_tower_quotient_cas_handoff_rows=1/1
```
