# P27 B-Line Localized Cover Layer Count

Date: 2026-06-22

## Claim

The localized reduced B-line cover has one important simplification:
`compactD_R` is not a fresh obstruction after the reduced `U_next` layer is
imposed.

On the parent chart, the compactD_R squareclass and the beta squareclass are
not equal.  Instead, the probe finds:

```text
chi(compactD_R_rhs / beta_rhs) = chi(d_next)
```

with zero mismatches in every tested field, where:

```text
d_next = x5^2 + A*x5 + 1
```

The reduced cover imposes `d_next` square through:

```text
(U_next - 2*x5)^2 = 4*d_next
```

Therefore, after passing to the reduced `U_next` cover, `compactD_R` has the
same squareclass as the already-adjoined beta branch.  Point counts confirm
the consequence: the full compactD_R cover is essentially a clean double of
the no-R reduced cover, with only zero-root degeneracies.

This does not produce a sampler, but it shrinks the offline CAS object: first
normalize the no-R reduced cover; add compactD_R later as a redundant/twinned
quadratic layer rather than treating it as an independent class.

## Probe

Probe:

```text
research/p27/archive/gates/p27_b_line_localized_cover_layer_count_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_localized_cover_layer_count_probe.py \
  --fields 607,7^3,7^4,7^5,7^6,23^2,23^3 \
  --fiber-limit 16 \
  | tee research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_20260622.txt
```

## Results

The squareclass identity held with zero mismatches:

```text
field   compact_beta_ratio_dnext_mismatch
607     0
7^3     0
7^4     0
7^5     0
7^6     0
23^2    0
23^3    0
```

The parent-chart mismatch count equals the `d_next` nonsquare count:

```text
field   compact_beta_squareclass_mismatch   reduced_U_roots_0
607     360                                 360
7^3     168                                 168
7^4     1344                                1344
7^5     8400                                8400
7^6     57792                               57792
23^2    192                                 192
23^3    6080                                6080
```

Once `d_next` is square, the full/no-R ratio is two up to zero-root
degeneracies:

```text
field   noR_reduced_U   full_reduced_U   full/noR
607     1044            2084             1.996168582
7^3     288             576              2.000000000
7^4     1688            3368             1.995260664
7^5     18880           37760            2.000000000
7^6     124808          249608           1.999935902
23^2    648             1288             1.987654321
23^3    12768           25536            2.000000000
```

The gamma/materialization coupling persists in the layer split:

```text
field   noR_gamma/noR_reduced_U   full_gamma/full_reduced_U
607     0.992337165               0.992322457
7^3     0.500000000               0.500000000
7^4     0.995260664               0.995249406
7^5     1.033898305               1.033898305
7^6     1.015383629               1.015384122
23^2    0.802469136               0.801242236
23^3    1.041353383               1.041353383
```

## Interpretation

Positive:

```text
The full localized cover is less independent than it looked.
compactD_R becomes a twinned/redundant quadratic layer after reduced_U.
The offline CAS model can be staged through the no-R reduced cover first.
The exact symbolic proof target is now sharply stated:
  compactD_R_rhs / beta_rhs differs from d_next by a square.
```

Negative:

```text
This is not a direct source sampler.
The no-R reduced cover still needs normalization/genus/component extraction.
gamma remains coupled to x6 materialization, not a cheap source stratum.
No GPU production mode follows from this count.
```

## CAS Consequence

The next offline CAS proof should verify the finite-field identity symbolically:

```text
compactD_R_rhs / beta_rhs = d_next * square
```

on the denominator-localized B-line source chart.

Update:
[P27 B-Line CompactD/Beta/Dnext Squareclass](p27_b_line_compact_beta_dnext_squareclass_20260622.md)
performs this as a Magma function-field `IsSquare` smoke over `GF(7)` and
`GF(23)`.  In the `Z=x5` coordinate, with `beta=Z-1/Z` and
`d_next=Z*(U+A)`, Magma verifies
`compactD_R_rhs / (beta^2*d_next)` is a square and checks the returned root
in both fields.

If proved, the normalization order becomes:

```text
1. Normalize the no-R reduced cover.
2. Prove compactD_R is obtained by the existing beta and reduced_U square roots.
3. Add x6/gamma only after the no-R reduced f3 cover is understood.
4. Compare f4/f3 on that normalized no-R base.
```

Promote only if the no-R cover has a low-genus/sourceable quotient or if
`f4/f5` recur on the normalized base.  Kill if the no-R cover is high genus
and later classes are fresh half-covers.

Genus-pressure follow-up:
[P27 B-Line No-R Genus Pressure](p27_b_line_noR_genus_pressure_20260622.md)
applies a one-component Hasse-Weil pressure test to these same counts.  Five
of seven tested fields violate the genus-one bound under a one-component
interpretation, with strongest pressure `g >= 11`.  If the cover is not one
component, the counts instead indicate nontrivial component/field-of-definition
behavior.  Either way, the no-R cover no longer looks like an obvious
genus-0/1 source.

## Continue / Kill

```text
continue = symbolic proof of compactD_R/beta/d_next square relation
continue = lift the q7/q23 function-field square witness to characteristic 0 or p27
continue = offline normalize no-R reduced cover before full compactD_R cover
continue = compute no-R components/quotients/Prym structure, not only genus
continue = compare f4/f3 after no-R normalization

kill = treating compactD_R as an independent first CAS layer after reduced_U
kill = expecting the no-R reduced cover to be an obvious genus-0/1 source
kill = GPU production from the layer-count simplification alone
kill = gamma bucket/source search without a normalized quotient
```

## Linked Artifacts

- Charted Magma staging: [P27 B-Line Reduced-Cover Charted Magma Staging](p27_b_line_reduced_cover_charted_magma_20260622.md)
- Reduced symbolic packet: [P27 B-Line Reduced-Cover Symbolic Packet](p27_b_line_reduced_cover_symbolic_packet_20260622.md)
- Gamma extension count: [P27 B-Line Gamma Extension Count](p27_b_line_gamma_extension_count_20260622.md)

```text
p27_b_line_localized_cover_layer_count_rows=1/1
```
