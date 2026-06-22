# P27 B-Line Reduced-Cover Symbolic Packet

Date: 2026-06-22

## Claim

The reduced B-line d3 cover has an explicit symbolic handoff that avoids the
heavier reverse `z,Y` source.

Let `x5` be the current selected x-coordinate and let:

```text
Unext = x6 + 1/x6
```

for the next halving branch.  Then:

```text
(Unext - 2*x5)^2 = 4*(x5^2 + A*x5 + 1)
```

and the selected squareclass is:

```text
f3 = chi(Unext + 2)
```

The packet writes this equation in the existing B-line source variables
`X,W,T,beta,R,eta,Bline,Unext` so CAS can normalize the reduced 4-u cover over
`P1_Bline`.

## Artifacts

Generator:

```text
research/p27/archive/gates/p27_b_line_reduced_cover_symbolic_packet.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_symbolic_packet_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_reduced_cover_symbolic_packet.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_cover_symbolic_packet_20260622.txt
```

## Reduced Equation

The packet emits:

```text
eta_branch
E_W
T_cover
compactD_R
Bline_relation
first_half_beta
reduced_Unext
```

where the reduced equation is printed in compact named form:

```text
reduced_Unext =
  A_den*(Unext*U_den - x5_num)^2
  - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2)
```

with:

```text
x5 = x5_num / x5_den
x5_den = 2*U_den
A = A_num / A_den
selector = Unext + 2
optional materialization: x6^2 - Unext*x6 + 1 = 0
```

## Validation

The guard-field validation checks the reduced equation and selector on all
enumerated legal branches:

```text
q1607:
  d2_plus_candidates = 784
  validated_branches = 1568
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0

q1847:
  d2_plus_candidates = 1008
  validated_branches = 2016
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0

q2087:
  d2_plus_candidates = 912
  validated_branches = 1824
  A_B_identity_mismatch = 0
  reduced_equation_mismatch = 0
  selector_mismatch = 0
```

## Interpretation

Positive:

```text
The reduced 4-u cover is now an explicit symbolic CAS target.
It removes the reverse z/Y materialization from the first normalization pass.
It preserves the exact f3 selector as chi(Unext+2).
```

Online Magma follow-up:
[P27 B-Line Reduced-Cover Magma Smoke](p27_b_line_reduced_cover_magma_smoke_20260622.md).
The q7 saturation-only fixture is submit-ready, but the online calculator
terminates at the memory limit during `Saturation(I, bad)`.  This moves the
next step to offline Magma/Sage or specialized elimination; it does not promote
GPU production.

Charted Magma follow-up:
[P27 B-Line Reduced-Cover Charted Magma Staging](p27_b_line_reduced_cover_charted_magma_20260622.md).
The first saturation wall is specifically the `X=0` artifact.  Replacing it
with `X*iX=1` lets the no-R reduced cover saturate online as a dimension-1
scheme with 6 basis equations.  The full compactD_R cover is dimension 1
before saturation, and the fully localized full model, with inverse variables
for all denominator factors, is immediately dimension 1 with 12 equations.
Thus the next offline attack should normalize the localized model or the
X-inverted no-R base, not restart product saturation.

Layer-count follow-up:
[P27 B-Line Localized Cover Layer Count](p27_b_line_localized_cover_layer_count_20260622.md).
Across the tested prime and extension fields,
`chi(compactD_R_rhs / beta_rhs) = chi(d_next)` with zero mismatches.  Since
the reduced `U_next` equation makes `d_next` square, compactD_R becomes a
twinned beta layer on the reduced cover.  The first CAS model should therefore
be the no-R reduced cover; compactD_R can be added only after that base is
understood.

Function-field squareclass follow-up:
[P27 B-Line CompactD/Beta/Dnext Squareclass](p27_b_line_compact_beta_dnext_squareclass_20260622.md).
Magma verifies over `GF(7)` and `GF(23)` that
`compactD_R_rhs/(beta^2*d_next)` is square in the staged function field.
This strengthens the compactD_R demotion, but still does not compute genus or
sourceability.

Genus/component pressure follow-up:
[P27 B-Line No-R Genus Pressure](p27_b_line_noR_genus_pressure_20260622.md).
Treating the existing no-R layer counts as affine counts, the one-component
Hasse-Weil pressure test violates genus `<= 1` in `5/7` fields and reaches
`g_min = 11` in the strongest field.  If the counted object splits, the same
numbers are evidence for component or field-of-definition structure.  The
offline CAS target should compute components, quotients, and Prym factors, not
assume the no-R base is an obvious genus-0/1 source.

Direct finite-field point-count follow-up:
[P27 B-Line Reduced-Cover Point Count](p27_b_line_reduced_cover_pointcount_20260622.md).
The `U_next` layer is a clean two-valued cover over the legal chart in the
promotion fields, but materialization through `x6^2-U*x6+1` and the selector
cover `gamma^2=U+2` split by B-fiber.  Offline CAS should keep these layers
attached; the bare `U` cover is not itself a source.

Negative:

```text
This is not yet a sampler or proof of low genus.
The prior reduced-fiber relation screen still kills visible plane models
through degree 20.
Promotion requires normalization/genus/quotient output from this symbolic
cover.
The online calculator cannot provide that output for the reduced q7 fixture.
```

## Continue / Kill

```text
continue = run CAS normalization of the reduced_Unext cover over P1_Bline
continue = use offline Magma/Sage or elimination; online Magma is too small
continue = prefer the localized complete-intersection chart over product saturation
continue = normalize the no-R reduced cover before compactD_R
continue = lift compactD_R_rhs/(beta^2*d_next) squareclass beyond q7/q23 if possible
continue = attach x6-materialization and gamma^2=Unext+2 to the offline model
continue = compute genus/components/quotients and compare against the fixture
continue = compute no-R quotient/Prym structure after genus pressure
continue = only then pull back f4/f3

kill = full reverse z/Y normalization as the first CAS attempt if reduced_Unext is feasible
kill = saturation-first online workflow after the charted Magma smoke
kill = GPU production before reduced-cover genus/sourceability is known
kill = expecting the no-R reduced cover to be an obvious genus-0/1 source
```

```text
p27_b_line_reduced_cover_symbolic_packet_rows=1/1
```
